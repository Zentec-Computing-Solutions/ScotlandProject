from gpiozero import LED
from signal import pause


red = LED(17)

def led_on():
    red.on()
def led_off():
    red.off()
