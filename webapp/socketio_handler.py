import subprocess
from threading import Thread
import time
from wiper_timer import set_new_timer


def init_socketio(socketio, picam2, red_led):

    @socketio.on("update_setting")
    def update_setting(data):
        setting_name = data["name"]
        setting_value = data["value"]
        if setting_name == "brightness":
            picam2.set_controls({"Brightness": float(setting_value)})
        elif setting_name == "contrast":
            picam2.set_controls({"Contrast": float(setting_value)})
        elif setting_name == "saturation":
            picam2.set_controls({"Saturation": float(setting_value)})
        elif setting_name == "sharpness":
            picam2.set_controls({"Sharpness": float(setting_value)})

    @socketio.on("power")
    def power(data):
        power = str(data["value"])
        if power == "shutdown":
            subprocess.run(["sudo", "shutdown", "now"])
        elif power == "restart":
            subprocess.run(["sudo", "reboot", "now"])
        return power

    @socketio.on("restart_webserver")
    def restart_webserver():
        subprocess.run(["sudo", "systemctl", "restart", "kinacam"])

    @socketio.on("led")
    def led(data):
        led = bool(data["checked"])
        if led:
            red_led.on()
        else:
            red_led.off()
        socketio.emit("led", data, include_self=False)
        return led

    @socketio.on("wiper")
    def wiper(data: dict):
        wiper_time = int(data["time"])
        if wiper_time == -1:
            red_led.on()
            time.sleep(3)
            red_led.off()
        else:
            socketio.emit("wiper", data, include_self=False)
            wiper_time
            set_new_timer(wiper_time, red_led)
            return wiper
