from flask import Flask, request, jsonify, send_file
import cv2
import time

flask_app = Flask(__name__)

def generate_frames(frames):
    while True:
        if not frames.empty():
            frame = frames.get()
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            return (frame_bytes)
        else:
            time.sleep(0.1)


def host_webserver(frames):
    @flask_app.route('/')
    def index():
        return send_file('index.html')

    @flask_app.route('/video')
    def video_feed():
        return Flask.Response(generate_frames(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    flask_app.run(host='0.0.0.0', port=5000)