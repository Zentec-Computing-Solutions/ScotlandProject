from gpiozero import LED
from RPi import GPIO
from loggerthyst import info
import time


class KinacamLED:
    def __init__(self, pin=17):
        self.led: LED = LED(pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def is_on(self):
        return self.led.is_active


class KinacamWiper:
    def __init__(self, pin=5):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def wipe(self):
        GPIO.output(5, GPIO.HIGH)
        info("WIPING!")
        time.sleep(0.2)
        GPIO.output(5, GPIO.LOW)
