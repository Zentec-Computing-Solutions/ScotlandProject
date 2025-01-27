import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(5, GPIO.OUT)  # Set pin 22 as an output

i = 2
while i > 0:
    GPIO.output(5, GPIO.HIGH)
    print(i)
    i -= 1
    time.sleep(0.1)
GPIO.output(5, GPIO.LOW)
