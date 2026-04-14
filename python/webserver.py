from flask import Flask, request, jsonify, render_template, Response, send_from_directory
import cv2
import numpy as np
import os

flask_app = Flask(__name__)
# Werte der ersten Maske
lower_blue1 = np.array([0, 0, 0]) #179, 100, 100
upper_blue1 = np.array([0, 0, 0])
# Werte der zweiten Maske
lower_blue2 = np.array([0, 0, 0])
upper_blue2 = np.array([0, 0, 0])
# Werte der dritten Maske
lower_blue3 = np.array([0, 0, 0])
upper_blue3 = np.array([0, 0, 0])


def generate_frames(frames):
    while True:
        frame = frames.get() # Holt den nächsten Frame aus der Queue frames und speichert ihn in der Variable frame.
        # hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        _, buffer = cv2.imencode('.jpg', frame) # Kodiert den Frame als .jpg-Datei. Rückgae: Erfolg, Datei => _, buffer
        frame_bytes = buffer.tobytes()  # Variable frame_bytes enhält die bytes des Frames in einer .jpg Datei

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') # Gibt den Frame als Teil eines MJPEG-Streams zurück.

def pytojshsv(nparray): # Konvertiert ein cv2-Array eines Bildes in colorpicker-Array für js
    return np.array([int(nparray[0]*2), int(nparray[1]/2.55), int(nparray[2]/2.55)])

def jstopyhsv(nparray): # Konvertiert ein colorpicker-Array für js eines Bildes in cv2-Array
    return np.array([int(nparray[0]/2), int(nparray[1]*2.55), int(nparray[2]*2.55)])

def generate_frames_res(frames): # Generiert frames für js
    while True:
        frame = frames.get() # Holt den nächsten Frame aus der Queue frames und speichert ihn in der Variable frame.

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #
        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        mask3 = cv2.inRange(hsv, lower_blue3, upper_blue3)
        mask = cv2.bitwise_or(mask1, mask2)
        mask = cv2.bitwise_or(mask, mask3)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        _, buffer = cv2.imencode('.jpg', res)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def host_webserver(frames):
    @flask_app.route('/')
    def index():
        return render_template("index.html")

    @flask_app.route('/video_res')
    def video_feed_res():
        return Response(generate_frames_res(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_app.route('/video')
    def video_feed():
        return Response(generate_frames(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_app.route('/cam')
    def cam_alias():
        # Alias to the processed result stream for compatibility with older clients
        return Response(generate_frames_res(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_app.route('/set_value', methods=["POST"])
    def set_value():
        data = request.get_json()
        id = str(data.get("ID")) + str(data.get("CID"))
        h = data.get("H")
        s = data.get("S")
        v = data.get("V")

        arr = jstopyhsv(np.array([h, s, v]))

        global lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3
        match id:
            case "11":
                lower_blue1 = arr
            case "12":
                upper_blue1 = arr
            case "21":
                lower_blue2 = arr
            case "22":
                upper_blue2 = arr
            case "31":
                lower_blue3 = arr
            case "32":
                upper_blue3 = arr
            case _:
                print("ERROR!")
                return "error"

        return "done"

    @flask_app.route('/get_value')
    def get_value():
        id = request.args.get('id')

        match int(id):
            case 1:
                arr1 = pytojshsv(lower_blue1)
                arr2 = pytojshsv(upper_blue1)
            case 2:
                arr1 = pytojshsv(lower_blue2)
                arr2 = pytojshsv(upper_blue2)
            case 3:
                arr1 = pytojshsv(lower_blue3)
                arr2 = pytojshsv(upper_blue3)
            case _:
                print("ERROR!")
                return

        return jsonify({"UP": arr1.tolist(), "LOW": arr2.tolist()})

    @flask_app.route('/save', methods=["POST"])
    def savePreset():
        data = request.get_json()
        id = data.get("ID")

        try:
            os.mkdir("Preset")
        except FileExistsError:
            print("Directory already exists!")

        match int(id):
            case 1:
                Uh, Us, Uv = upper_blue1[0], upper_blue1[1], upper_blue1[2]
                Lh, Ls, Lv = lower_blue1[0], lower_blue1[1], lower_blue1[2]
            case 2:
                Uh, Us, Uv = upper_blue2[0], upper_blue2[1], upper_blue2[2]
                Lh, Ls, Lv = lower_blue2[0], lower_blue2[1], lower_blue2[2]
            case 3:
                Uh, Us, Uv = upper_blue3[0], upper_blue3[1], upper_blue3[2]
                Lh, Ls, Lv = lower_blue3[0], lower_blue3[1], lower_blue3[2]
            case _:
                print("ERROR!")

        with open(f"Preset/{id}_Preset.txt", "w") as file:
            file.write(f"{Lh}, {Ls}, {Lv}, {Uh}, {Us}, {Uv}")
            file.close()

        return jsonify({"sucess": True})

    @flask_app.route("/load")
    def loadPreset():
        id = request.args.get('id')

        if not os.path.exists("Preset/"):
            return jsonify({"sucess": False}), 404

        try:
            with open(f"Preset/{id}_Preset.txt", "r") as file:
                content = file.read()
                file.close()
        except:
            return jsonify({"sucess": False}), 404

        werte = [int(w.strip()) for w in content.split(",")]

        lower = np.array(werte[:3])
        upper = np.array(werte[3:])

        arr1 = pytojshsv(upper)
        arr2 = pytojshsv(lower)

        return jsonify({"UP": arr1.tolist(), "LOW": arr2.tolist()}), 200

    flask_app.run(host='0.0.0.0', port=5000)
