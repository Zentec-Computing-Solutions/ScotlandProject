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

