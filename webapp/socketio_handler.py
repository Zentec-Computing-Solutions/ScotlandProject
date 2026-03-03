import subprocess
from threading import Thread
from loggerthyst import info, warn
from sampler_handler import send_sampler_trigger

def init_socketio(socketio, picam2, led_light):

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
        elif setting_name == "ledBrightness":
            led_light.set_brightness(float(setting_value))
        else:
            warn(f"Unknown setting name: {setting_name}")

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
        
    @socketio.on("sample_button_confirmed")
    def sample_button_confirmed(data):
        button = int(data["button"])
        if send_sampler_trigger(button):
            info(f"Sampler trigger sent for button {button}")
        else:
            info(f"Failed to send sampler trigger for button {button}")

    @socketio.on("led")
    def led(data):
        led = bool(data["checked"])
        if led:
            led_light.on()
        else:
            led_light.off()
        socketio.emit("led", data, include_self=False)
        return led
