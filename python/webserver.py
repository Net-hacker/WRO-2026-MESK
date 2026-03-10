from flask import Flask, request, jsonify, send_file, Response, send_from_directory
import cv2
import numpy as np
import os

flask_app = Flask(__name__)

lower_blue1 = np.array([int(280 / 2), int(255 * 0.5), int(255 * 0.4)]) #179, 100, 100
upper_blue1 = np.array([int(360 / 2), 255, 255])

lower_blue2 = np.array([0, 100, 100])
upper_blue2 = np.array([70, 255, 255])

def generate_frames(frames):
    while True:
        frame = frames.get()
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def pytojshsv(nparray):
    return np.array([int(nparray[0]*2), int(nparray[1]), int(nparray[2])])

def jstopyhsv(nparray):
    return np.array([int(nparray[0]/2), int(nparray[1]), int(nparray[2])])

def generate_frames_res(frames):
    while True:
        frame = frames.get()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        mask = cv2.bitwise_or(mask1, mask2)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        _, buffer = cv2.imencode('.jpg', res)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def host_webserver(frames):
    @flask_app.route('/')
    def index():
        return send_file('index.html')

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
        arr = pytojshsv(np.array(numbers))
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
            return ",".join(map(str, lower_blue1))
        elif id_int == 12:
            return ",".join(map(str, upper_blue1))
        elif id_int == 21:
            return ",".join(map(str, lower_blue2))
        elif id_int == 22:
            return ",".join(map(str, upper_blue2))
        else:
            return ",".join(map(str, np.array([0, 0, 0])))


    flask_app.run(host='0.0.0.0', port=5000)
