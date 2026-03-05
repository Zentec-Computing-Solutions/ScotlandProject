# sibs_led_simple.py
from gpiozero import PWMLED, DigitalOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from loggerthyst import info, warn, error, fatal
import time

# HAT pin assignments (BCM)
DEFAULT_ENABLE_PIN = 12   # IO12   
DEFAULT_PWM_PIN    = 13   # IO13

class SIBSLED:
    def __init__(self, pwm_pin=DEFAULT_PWM_PIN, enable_pin=DEFAULT_ENABLE_PIN,
                 freq=1000, start_pct=5.0, max_pct=70.0):
        self.start_pct = max(0.0, min(100.0, float(start_pct))) / 100.0
        self.max_pct = max(0.0, min(100.0, float(max_pct))) / 100.0
        self.freq = int(freq)

        # Use gpiozero default backend (RPi.GPIO) — no pigpiod required
        try:
            self.enable = DigitalOutputDevice(enable_pin, active_high=True,
                                              initial_value=False)
            self.led = PWMLED(pwm_pin, frequency=self.freq, initial_value=0.0, pin_factory=LGPIOFactory())
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
            self.enable.on()
            time.sleep(0.01)
            self.led.value = start_val
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
            self.led.value = val
            info(f"Brightness set to {val*100.0:.1f}%")
        except Exception as e:
            error(f"Error setting brightness to {val*100.0:.1f}%: {e}")
            raise

    def off(self):
        try:
            self.led.value = 0.0
            time.sleep(0.01)
            self.enable.off()
            info("LED disabled")
        except Exception as e:
            error(f"Error disabling LED: {e}")
            raise

    def is_on(self):
        try:
            return bool(self.enable.value)
        except Exception:
            return False

    def close(self):
        try:
            self.led.value = 0.0
            self.enable.off()
            self.led.close()
            self.enable.close()
            info("SIBSLED closed")
        except Exception as e:
            warn(f"Error closing SIBSLED: {e}")