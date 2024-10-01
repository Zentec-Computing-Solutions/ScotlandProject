import os
import subprocess

from flask import Flask, Response, render_template, jsonify, request
from flask_minify import Minify
from camera_handler import _gen_frames
from loggerthyst import *
from settings import _load_settings, _update_settings

from picamera2 import Picamera2, Preview
import time

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = (
    "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
)
import cv2

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(
    picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
)
picam2.start()

settings = _load_settings()


@app.route("/set_brightness")
def set_brightness():
    brightness = float(request.args.get("value"))
    picam2.set_controls({"Brightness": brightness})
    return "Brightness set!"


@app.route("/set_contrast")
def set_contrast():
    constrast = float(request.args.get("value"))
    picam2.set_controls({"Contrast": constrast})
    return "Contrast set!"


@app.route("/set_saturation")
def set_saturation():
    saturation = float(request.args.get("value"))
    picam2.set_controls({"Saturation": saturation})
    return "Saturation set!"


@app.route("/set_sharpness")
def set_sharpness():
    sharpness = float(request.args.get("value"))
    picam2.set_controls({"Sharpness": sharpness})
    return "Sharpness set!"


@app.route("/update_settings", methods=["POST"])
def update_settings():
    return jsonify(_update_settings(settings))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/power")
def power():
    power = str(request.args.get("value"))
    if power == "shutdown":
        subprocess.run(["sudo", "shutdown", "now"])
    elif power == "restart":
        subprocess.run(["sudo", "reboot", "now"])
    return power


@app.route("/video_feed")
def video_feed():
    return Response(
        _gen_frames(settings, picam2),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    Minify(app, html=True, cssless=True, js=True)
    app.run(debug=False, port=8080, host="0.0.0.0")
