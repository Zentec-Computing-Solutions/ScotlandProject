# Kinacam

run.sh

https://github.com/raspberrypi/picamera2/blob/main/examples

https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/

https://getcssscan.com/css-checkboxes-examples

Framerate issue is coming from python being singlethreaded, it has to stream one frame to one client, and then one frame to another client, one by one instead of at the same time. Would have to rework entire backend to use multithreading - unsure how long this would take

## Things to do:

-   [x] Run on Pi startup
-   [ ] Fix rotation of camera, make it 90, 180, 270
-   [x] Wiper via scheduled gpio - Should be pretty easy, already implemented basic GPIO LEDs, dropdown with times, test button
-   [ ] Time and temp overlays - Can be done with `cv2.putText()`
-   [ ] LEDs - Via CLI
-   [x] Stream to VLC - Works, not the best with multiple clients, fixed delay issue with VLC setting
-   [ ] Record video somehow to client - OBS/VLC?
-   [x] Ability to turn off camera from control panel

## Solutions

-   [ ] [MJPEG instead of JPEG](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/) - hm not really, this uses multithreading
