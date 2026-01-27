# SIBS V4.0
SIBS V4.0 uses Raspberry Pi OS Lite 64Bit. Kinacam and Marine Deisgn Engineering LTD are not affliated with Raspberry Pi Holdings plc or The Pi Foundation in any way - we just think they are really cool.

Check out the [Wiki](https://github.com/Bluemethyst/Fisheye/wiki) for installing and setup.

# Developer Notes - IGNORE

## Todo
LEDs
Release System x3
If time: 1080p

run.sh

https://github.com/raspberrypi/picamera2/blob/main/examples

https://www.reddit.com/r/learnpython/comments/zxxsal/comment/l5xscrp/

https://getcssscan.com/css-checkboxes-examples

Framerate issue is coming from python being singlethreaded, it has to stream one frame to one client, and then one frame to another client, one by one instead of at the same time. Would have to rework entire backend to use multithreading - unsure how long this would take

## Things to do:

-   [x] Run on Pi startup
-   [x] Fix rotation of camera, make it 90, 180, 270
-   [x] Wiper via scheduled gpio - Should be pretty easy, already implemented basic GPIO LEDs, dropdown with times, test button
-   [ ] Time and temp overlays - Can be done with `cv2.putText()`
-   [ ] LEDs - Via CLI
-   [x] Stream to VLC - Works, not the best with multiple clients, fixed delay issue with VLC setting
-   [ ] Record video somehow to client - OBS/VLC?
-   [x] Ability to turn off camera from control panel

## Solutions

-   [ ] [MJPEG instead of JPEG](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/) - hm not really, this uses multithreading
