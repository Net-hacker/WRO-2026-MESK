from flask import Flask, request, jsonify, send_file, Response
import cv2

flask_app = Flask(__name__)

def generate_frames(frames):
    while True:
        frame = frames.get()
        print("Getting frame from queue")
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') #Ich hab wirklich keine Ahnung was das macht


def host_webserver(frames):
    @flask_app.route('/')
    def index():
        return send_file('index.html')

    @flask_app.route('/video')
    def video_feed():
        return Response(generate_frames(frames), mimetype='multipart/x-mixed-replace; boundary=frame')

    flask_app.run(host='0.0.0.0', port=5000)