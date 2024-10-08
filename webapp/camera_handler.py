import time
import cv2
import os
from picamera2 import Picamera2

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = (
    "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
)


def new_gen_frames(camera: Picamera2, fps: int = 30):
    """Yield frames from the camera in MJPEG format at the specified fps."""
    capture_interval = 1.0 / fps
    while True:
        start_time = time.time()

        # Capture frame-by-frame
        frame = camera.capture_array()

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        frame = buffer.tobytes()

        # Yield frame in byte format
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        # Sleep to match the target fps
        time_taken = time.time() - start_time
        if time_taken < capture_interval:
            time.sleep(capture_interval - time_taken)
