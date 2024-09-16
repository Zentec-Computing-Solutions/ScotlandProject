import os

from flask import Flask, Response, render_template, jsonify
from camera_handler import _gen_frames
from loggerthyst import *
from settings import _load_settings, _update_settings

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = (
    "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
)
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

settings = _load_settings()


@app.route("/update_settings", methods=["POST"])
def update_settings():
    return jsonify(_update_settings(settings))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/raw_video")
def video_feed():
    return Response(
        _gen_frames(cap, settings), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
