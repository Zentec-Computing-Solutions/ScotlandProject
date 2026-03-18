#!/usr/bin/env python3
"""
Initialize the Ethernet HAT on startup by setting GPIO pin 22 to HIGH.
This enables the ethernet connection on the SIBS device.
"""

import sys
import time
from RPi import GPIO
from webapp.loggerthyst import info, error, fatal

def init_ethernet():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.OUT)
        
        # Turn off the HAT
        GPIO.output(22, GPIO.LOW)
        info("Ethernet HAT powered down - pin 22 set to LOW")
        
        # Wait for HAT to reset
        time.sleep(2)
        
        # Turn on the HAT
        GPIO.output(22, GPIO.HIGH)
        info("Ethernet HAT powered up - pin 22 set to HIGH")
        info("Ethernet HAT reboot sequence completed")
        return True
    except Exception as e:
        fatal(f"Failed to initialize ethernet HAT: {e}")
        return False

if __name__ == "__main__":
    info("Starting ethernet HAT initialization...")
    
    if init_ethernet():
        info("Ethernet HAT is ready.")
        sys.exit(0)
    else:
        sys.exit(1)
