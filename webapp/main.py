from flask import Flask, Response, render_template, jsonify, request
from loggerthyst import *
import os
import json
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# Load settings from file at startup
try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    info("Settings loaded successfully")
except FileNotFoundError:
    info("Settings file not found, creating a new one with default settings")
    settings = {
        'flip_video': False,
        # Add more settings here as needed
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)


@app.route('/update_settings', methods=['POST'])
def update_settings():
    global settings
    settings.update(request.get_json())  # Update settings with data from the POST request

    # Save settings to file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    return jsonify(settings)


def gen_frames():
    while True:
        if cap is None:
            continue
        success, frame = cap.read()
        if not success:
            break
        else:
            if settings['flip_video']:  # Only flip the frame if flip_video is True
                frame = cv2.flip(frame, 1)
            # Add more settings handling here as needed
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/raw_video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
