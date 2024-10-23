# Kinacam

https://github.com/raspberrypi/picamera2/blob/main/examples

https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/

https://getcssscan.com/css-checkboxes-examples

Framerate issue is coming from python being singlethreaded, it has to stream one frame to one client, and then one frame to another client, one by one instead of at the same time. Would have to rework entire backend to use multithreading - unsure how long this would take

## Things to do:

-   [x] Run on Pi startup
-   [ ] Wiper via scheduled gpio - Should be pretty easy, already implemented basic GPIO LEDs, dropdown with times, test button
-   [ ] Time and temp overlays - Can be done with `cv2.putText()`
-   [ ] LEDs - Via CLI
-   [ ] Stream to VLC - Works, not the best with multiple clients, fixed delay issue with VLC setting
-   [ ] Record video somehow to client - OBS/VLC?
-   [x] Ability to turn off camera from control panel

## Solutions

-   [ ] [MJPEG instead of JPEG](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/) - hm not really, this uses multithreading

Timer logic:

```python
"""Threading. Minimal example."""

import sys
from time import sleep
from threading import Thread


def timer(seconds):
    """Simple timer."""
    count = 0
    while True:
        print(count, 'seconds')
        count += seconds
        sleep(seconds)


# Create a new thread for the timer.
# Thread is running as a daemon so it will quit when the
# main thread terminates.
timer_thread = Thread(target=timer, args=(2,), daemon = True)

# Start the timer thread.
timer_thread.start()

# Do other stuff
print('Enter "q" to quit.')
while True:
    value = input('\nType something and press Enter:\n')
    if value.lower() == 'q':
        sys.exit('Bye.')
    print(f'\nYou entered "{value}"\n')
```
