from flask import Response, render_template

from camera_handler import _gen_frames


def init_routes(app, picam2):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/video_feed")
    def video_feed():
        return Response(
            _gen_frames(picam2),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    @app.route("/inital_data")
    def inital_data():
        data = {
            "led_on": False  # Default value, will be managed via socket events
        }
        return data
