# sibs_led_simple.py
from rpi_hardware_pwm import PWM
from RPi import GPIO
from loggerthyst import info, warn, error, fatal
import time

# HAT pin assignments (BCM)
DEFAULT_ENABLE_PIN = 12   # IO12   
DEFAULT_PWM_PIN    = 13   # IO13 (maps to PWM1)
DEFAULT_PWM_CHIP   = 0    # PWM chip 0
DEFAULT_PWM_CHANNEL = 1   # PWM1 channel (GPIO13)

class SIBSLED:
    def __init__(self, pwm_pin=DEFAULT_PWM_PIN, enable_pin=DEFAULT_ENABLE_PIN,
                 freq=1000, start_pct=5.0, max_pct=70.0):
        self.start_pct = max(0.0, min(100.0, float(start_pct))) / 100.0
        self.max_pct = max(0.0, min(100.0, float(max_pct))) / 100.0
        self.freq = int(freq)
        self.enable_pin = enable_pin
        self.is_enabled = False

        # Initialize hardware PWM (GPIO 13 = PWM1, chip 0, channel 1)
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(enable_pin, GPIO.OUT, initial=GPIO.LOW)
            self.pwm = PWM(DEFAULT_PWM_CHIP, DEFAULT_PWM_CHANNEL, frequency=self.freq)
            self.pwm.start(0)  # Start with 0% duty
        except Exception as e:
            fatal(f"Could not initialize GPIO devices: {e}")
            raise

        info(f"SIBSLED initialized enable={enable_pin} pwm={pwm_pin} freq={self.freq}Hz "
             f"start={self.start_pct*100.0:.1f}% max={self.max_pct*100.0:.1f}%")

    def on(self, start_pct=None):
        start_val = self.start_pct if start_pct is None else max(0.0, min(100.0, float(start_pct))) / 100.0
        if start_val > self.max_pct:
            warn(f"Requested start_pct {start_val*100.0:.1f}% greater than max {self.max_pct*100.0:.1f}% — clamping")
            start_val = self.max_pct
        try:
            GPIO.output(self.enable_pin, GPIO.HIGH)
            time.sleep(0.01)
            self.pwm.ChangeDutyCycle(start_val * 100.0)
            self.is_enabled = True
            info(f"LED enabled — start duty {start_val*100.0:.1f}%")
        except Exception as e:
            error(f"Error enabling LED: {e}")
            raise

    def set_brightness(self, pct):
        try:
            pctf = float(pct)
        except Exception:
            error(f"set_brightness: invalid pct {pct!r}")
            return
        val = max(0.0, min(100.0, pctf)) / 100.0
        if val > self.max_pct:
            warn(f"Requested {pctf:.1f}% > max {self.max_pct*100.0:.1f}%; clamping")
            val = self.max_pct
        try:
            self.pwm.ChangeDutyCycle(val * 100.0)
            info(f"Brightness set to {val*100.0:.1f}%")
        except Exception as e:
            error(f"Error setting brightness to {val*100.0:.1f}%: {e}")
            raise

    def off(self):
        try:
            self.pwm.ChangeDutyCycle(0)
            time.sleep(0.01)
            GPIO.output(self.enable_pin, GPIO.LOW)
            self.is_enabled = False
            info("LED disabled")
        except Exception as e:
            error(f"Error disabling LED: {e}")
            raise

    def is_on(self):
        return self.is_enabled

    def close(self):
        try:
            self.pwm.stop()
            GPIO.output(self.enable_pin, GPIO.LOW)
            GPIO.cleanup([self.enable_pin])
            info("SIBSLED closed")
        except Exception as e:
            warn(f"Error closing SIBSLED: {e}")