from flask import Flask, request, jsonify, render_template, Response, send_from_directory
import cv2
import numpy as np
import os

flask_app = Flask(__name__)
# Werte der ersten Maske
lower_blue1 = np.array([int(280 / 2), int(255 * 0.5), int(255 * 0.4)]) #179, 100, 100
upper_blue1 = np.array([min(int(360 / 2), 179), 255, 255]) 
# Werte der zweiten Maske
lower_blue2 = np.array([0, 100, 100])
upper_blue2 = np.array([70, 255, 255])
# Werte der dritten Maske
lower_blue3 = np.array([0, 100, 100])
upper_blue3 = np.array([70, 255, 255])

def manipulate_pixels(hsv_frame):
    # H-Kanal verdoppeln (OpenCV: 0-179 → iro: 0-358)
    hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] * 2)

    # S- und V-Kanal auf 0-100 skalieren (und clippen)
    hsv_frame[:, :, 1] = np.clip(hsv_frame[:, :, 1] / 2.55, 0, 100)
    hsv_frame[:, :, 2] = np.clip(hsv_frame[:, :, 2] / 2.55, 0, 100)

    # Datentyp anpassen (iro.ColorPicker erwartet Zahlen, kein uint8 nötig)
    return hsv_frame.astype(np.float32)  # oder einfach hsv_frame, je nach Bedarf

def generate_frames(frames):
    while True:
        frame = frames.get() # Holt den nächsten Frame aus der Queue frames und speichert ihn in der Variable frame.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        transformed_frame = manipulate_pixels(hsv_frame)
        _, buffer = cv2.imencode('.jpg', transformed_frame) # Kodiert den Frame als .jpg-Datei. Rückgae: Erfolg, Datei => _, buffer
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
        hsv = manipulate_pixels(hsv)
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

    @flask_app.route('/set_value')
    def set_value():
        value = request.args.get('value')
        id = request.args.get('id')
        numbers = [int(x) for x in value.split(",")]
        # convert incoming JS HSV (h:0-360, s/v:0-100) to OpenCV HSV (h:0-179, s/v:0-255)
        arr = jstopyhsv(np.array(numbers))
        # parse id as int so comparisons are consistent
        try:
            id_int = int(id)
        except Exception:
            print("Unsupported Id (not int):", id)
            return "error"

        # modify module-level arrays
        global lower_blue1, upper_blue1, lower_blue2, upper_blue2
        if id_int == 11:
            lower_blue1 = arr
        elif id_int == 12:
            upper_blue1 = arr
        elif id_int == 21:
            lower_blue2 = arr
        elif id_int == 22:
            upper_blue2 = arr
        elif id_int == 31:
            lower_blue3 = arr
        elif id_int == 32:
            upper_blue3 = arr
        else:
            print("Unsupported Id: ", id_int)
            return "error"
        return "done"

    @flask_app.route('/get_value')
    def get_value():
        id = request.args.get('id')
        try:
            id_int = int(id)
        except Exception:
            return ",".join(map(str, np.array([0, 0, 0])))

        if id_int == 11:
            ret = pytojshsv(lower_blue1)
            return ",".join(map(str, ret))
        elif id_int == 12:
            ret = pytojshsv(upper_blue1)
            return ",".join(map(str, ret))
        elif id_int == 21:
            ret = pytojshsv(lower_blue2)
            return ",".join(map(str, ret))
        elif id_int == 22:
            ret = pytojshsv(upper_blue2)
        elif id_int == 31:
            ret = pytojshsv(lower_blue3)
            return ",".join(map(str, ret))
        elif id_int == 32:
            ret = pytojshsv(upper_blue3)
            return ",".join(map(str, ret))
        else:
            return ",".join(map(str, np.array([0, 0, 0])))


    flask_app.run(host='0.0.0.0', port=5000)
