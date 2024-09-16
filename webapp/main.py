from flask import Flask, render_template, Response
from picamera import PiCamera
from io import BytesIO

app = Flask(__name__)


def gen(camera):
    stream = BytesIO()
    for _ in camera.capture_continuous(stream, "jpeg", use_video_port=True):
        # Return current frame as response
        stream.seek(0)
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n"
        )
        stream.seek(0)
        stream.truncate()


@app.route("/video_feed")
def video_feed():
    return Response(
        gen(PiCamera()), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
