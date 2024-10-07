import os
import subprocess

from flask import Flask, Response, render_template, jsonify, request
from flask_minify import Minify
from flask_socketio import SocketIO, emit
from camera_handler import _gen_frames
from loggerthyst import *
from settings import _load_settings, _update_settings
from gpio import *

from picamera2 import Picamera2, Preview
import time
import gpiozero

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = (
    "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
)
import cv2

app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

picam2 = Picamera2()
picam2.configure(
    picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"})
)
picam2.start()

settings = _load_settings()

red_led = FisheyeLED(17)

@app.route("/inital_data")
def inital_data():
    data = {
        "led_on": red_led.is_on(),
    }
    return data
    

@socketio.on("update_setting")
def update_setting(data):
    setting_name = data["name"]
    setting_value = data["value"]
    if setting_name == "brightness":
        picam2.set_controls({"Brightness": float(setting_value)})
    elif setting_name == "contrast":
        picam2.set_controls({"Contrast": float(setting_value)})
    elif setting_name == "saturation":
        picam2.set_controls({"Saturation": float(setting_value)})
    elif setting_name == "sharpness":
        picam2.set_controls({"Sharpness": float(setting_value)})
    else:
        pass
@socketio.on("power")
def power(data):
    power = str(data["value"])
    if power == "shutdown":
        subprocess.run(["sudo", "shutdown", "now"])
    elif power == "restart":
        subprocess.run(["sudo", "reboot", "now"])
    return power

@socketio.on("led")
def led(data):
    led = bool(data["checked"])
    if led == True:
        red_led.on()
    elif led == False:
        red_led.off()
    return led

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        _gen_frames(settings, picam2),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    Minify(app, html=True, cssless=True, js=True)
    socketio.run(app=app, debug=False, port=8080, host="0.0.0.0")
