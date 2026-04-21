from flask import Flask, request, jsonify, render_template, Response, send_from_directory
import cv2
import numpy as np
import os
import config
import cam

flask_app = Flask(__name__)

def generate_frames(frames):
    while True:
        frame = frames.get() # Holt den nächsten Frame aus der Queue frames und speichert ihn in der Variable frame.
        # hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        _, buffer = cv2.imencode('.jpg', frame) # Kodiert den Frame als .jpg-Datei. Rückgae: Erfolg, Datei => _, buffer
        frame_bytes = buffer.tobytes()  # Variable frame_bytes enhält die bytes des Frames in einer .jpg Datei

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') # Gibt den Frame als Teil eines MJPEG-Streams zurück.

def pytojshsv(nparray): # Konvertiert ein cv2-Array eines Bildes in colorpicker-Array für js
    return np.array([round(nparray[0]*2), int(nparray[1]/2.55), int(nparray[2]/2.55)])

def jstopyhsv(nparray): # Konvertiert ein colorpicker-Array für js eines Bildes in cv2-Array
    return np.array([round(nparray[0]/2), int(nparray[1]*2.55), int(nparray[2]*2.55)])

def generate_frames_res(res_frames): # Generiert frames für js
    while True:
        res = res_frames.get() # Holt den nächsten Frame aus der Queue frames und speichert ihn in der Variable frame.
        _, buffer = cv2.imencode('.jpg', res) # Kodiert den Frame als .jpg-Datei. Rückgae: Erfolg, Datei => _, buffer
        frame_bytes = buffer.tobytes() # Variable frame_bytes enhält die bytes des Frames in einer .jpg Datei
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') # Gibt den Frame als Teil eines MJPEG-Streams zurück.


def host_webserver(frames, res_frames):
    @flask_app.route('/')
    def index():
        return render_template("index.html")

    @flask_app.route('/video_res')
    def video_feed_res():
        return Response(generate_frames_res(res_frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_app.route('/video')
    def video_feed():
        return Response(generate_frames(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_app.route('/set_value', methods=["POST"])
    def set_value():
        data = request.get_json()
        id = str(data.get("ID")) + str(data.get("CID"))
        h = data.get("H")
        s = data.get("S")
        v = data.get("V")

        arr = jstopyhsv(np.array([h, s, v]))

        Maske = int(id[0])
        Border = int(id[1])

        if len(config.mask_values) >= Maske and len(config.mask_values[Maske - 1]) >= Border:
            config.mask_values[Maske - 1][Border - 1] = arr
        else:
            print("Error while setting value: Id is not valid")
            return "error"
        return "done"

    @flask_app.route('/get_value')
    def get_value():
        id = request.args.get('id')

        if len(config.mask_values) >= int(id):
            arr1 = pytojshsv(config.mask_values[int(id) - 1][0])
            arr2 = pytojshsv(config.mask_values[int(id) - 1][1])
        else:
            print("Error while getting value: ID is not valid")
            return 400

        return jsonify({"UP": arr2.tolist(), "LOW": arr1.tolist()})

    @flask_app.route('/save', methods=["POST"])
    def savePreset():
        data = request.get_json()
        id = data.get("ID")

        try:
            os.mkdir("Preset")
        except FileExistsError:
            pass

        if len(config.mask_values) >= int(id):
            (Uh, Us, Uv), (Lh, Ls, Lv) = config.mask_values[int(id) - 1]
        else:
            print("Error while saving Preset: ID is not valid")

        with open(f"Preset/{id}_Preset.txt", "w") as file:
            file.write(f"{Lh}, {Ls}, {Lv}, {Uh}, {Us}, {Uv}")
            file.close()

        return jsonify({"sucess": True})

    @flask_app.route("/load")
    def loadPreset():
        id = request.args.get('id')

        arr1, arr2 = cam.load_preset(id)
        if arr1 is None:
            return jsonify({"sucess": False}), 404
        arr1 = pytojshsv(arr1)
        arr2 = pytojshsv(arr2)

        return jsonify({"UP": arr1.tolist(), "LOW": arr2.tolist()}), 200

    @flask_app.route("/send_tolerance", methods=["POST"])
    def tolerancer():
        data = request.get_json()
        id = data.get("ID")
        tolerance = data.get("TOLL")

        if len(config.tolerance_values) >= int(id):
            config.tolerance_values[int(id) - 1] = float(tolerance)
        else:
            print("Error while saving Tolerance: ID is not valid")

        with open(f"Preset/{id}_Tolerance.txt", "w") as file:
            file.write(f"{float(tolerance)}")
            file.close()

        return jsonify({"sucess": True})

    @flask_app.route("/get_tolerance")
    def loadToll():
        id = request.args.get('id')

        if len(config.tolerance_values) >= int(id):
            tolerance = config.tolerance_values[int(id) - 1]
        else:
            print("Error while getting value: ID is not valid")
            return 400

        return jsonify({"TOLL": tolerance}), 200

    flask_app.run(host='0.0.0.0', port=5000)
