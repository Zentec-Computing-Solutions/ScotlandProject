from picamera2 import Picamera2
import os
from flask import Flask
from flask_minify import Minify
from flask_socketio import SocketIO
from gpio import *
from routes import init_routes
from socketio_handler import init_socketio

# https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# Initialize Flask app
app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(
    picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"}))
picam2.start()

# Initialize components (routes, socketio handlers)
red_led = FisheyeLED(17)
init_routes(app, picam2, red_led)
init_socketio(socketio, picam2, red_led)

if __name__ == "__main__":
    Minify(app, html=True, cssless=True, js=True)
    socketio.run(app=app, debug=False, port=8080,
                 host="0.0.0.0")
