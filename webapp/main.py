from threading import Event
from picamera2 import Picamera2
import os
from flask import Flask
from flask_minify import Minify
from flask_socketio import SocketIO
from gpio import *
from routes import init_routes
from socketio_handler import init_socketio
from RPi import GPIO

# https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# Initialize Flask app
app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

# Set pin 22 to high to enable ethernet connection
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"}))
picam2.start()

# Initialize components (routes, socketio handlers)
led_light = SIBSLED()
init_routes(app, picam2, led_light)
init_socketio(socketio, picam2, led_light)

if __name__ == "__main__":
    Minify(app, html=True, cssless=True, js=True)
    socketio.run(app=app, debug=False, port=8080,
                 host="0.0.0.0", allow_unsafe_werkzeug=True)
