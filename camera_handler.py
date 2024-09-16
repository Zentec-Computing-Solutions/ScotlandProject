import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"  # https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
import cv2


def _gen_frames(cap, settings):
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