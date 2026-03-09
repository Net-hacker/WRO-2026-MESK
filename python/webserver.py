from flask import Flask, request, jsonify, send_file, Response
import cv2
import numpy as np

flask_app = Flask(__name__)



def generate_frames(frames):
    while True:
        frame = frames.get()
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_frames_res(frames):
    while True:
        frame = frames.get()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue1 = np.array([int(315 / 2), int(255 * 0.6), int(255 * 0.6)])
        upper_blue1 = np.array([int(360 / 2), 255, 255])

        lower_blue2 = np.array([0, 100, 100], dtype=np.uint8)
        upper_blue2 = np.array([15, 255, 255], dtype=np.uint8)

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
    
    @flask_app.rounte('/change_value')
    def change_value():
        value = request.args.get('value')
        id = request.args.get('id')
        return "done"

    flask_app.run(host='0.0.0.0', port=5000)
