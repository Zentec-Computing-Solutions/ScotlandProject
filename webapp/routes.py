from flask import Response, render_template, jsonify, send_from_directory
from camera_handler import new_gen_frames


def init_routes(app, picam2, red_led):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/video_feed")
    def video_feed():
        return Response(
            new_gen_frames(picam2),
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    @app.route("/inital_data")
    def inital_data():
        data = {
            "led_on": red_led.is_on(),
        }
        return data
    
    @app.route("/manifest.json")
    def manifest():
        return send_from_directory('static', 'manifest.json', mimetype='application/manifest+json')
