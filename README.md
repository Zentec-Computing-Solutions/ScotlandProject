# Kinacam
Kincam uses Raspberry Pi OS Lite 64Bit. Kinacam and Marine Deisgn Engineering LTD are not affliated with Raspberry Pi Holdings plc or The Pi Foundation in any way - we just think they are really cool.

## Setup/Installation
Flash an SD card that is at least 16GB in size with Raspberry Pi OS Lite 64Bit using the [Raspberry Pi Imager software](https://www.raspberrypi.com/software/). Make sure you enable some sort of SSH access in the OS settings during flashing and set the hostname to `kinacam`. Insert the SD card into the Pi and boot it up. Once the Pi is booted SSH into it from your computer. The command will be something similar to this:
```sh
ssh <username>@kinacam
```
Once logged in, run these few commands to make sure everything is up to date.
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
```
Then we need to get the Kinacam software download. Use the below commands to install the software. This may take a while and you may need to press `y` to confirm a step.
```sh
git clone https://github.com/Bluemethyst/Fisheye.git
cd Fisheye
./install.sh
```
Once complete you should see an output like this in green.
```
Service added to systemd.
Kinacam install complete, reboot to start Kinacam.
```
Reboot the system with this command.
```
sudo reboot now
```
Wait for the device to come back online again and then ssh into it again. You should be able to make sure Kinacam is running by running this command.
```
sudo systemctl status kinacam
```
If it says the service is active and running you can go to the Pi's IP address or the hostname, kinacam, in this example, on port 8080 through your web browser to see the control panel.
![image](https://github.com/user-attachments/assets/37708569-3682-41f4-bde3-512d48bd3746)


# Developer Notes - IGNORE

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
