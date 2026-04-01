from threading import Lock
import time

from smbus2 import SMBus

from loggerthyst import info, warn, error, fatal


DEFAULT_ENABLE_PIN = 12
DEFAULT_PWM_PIN = 13

DEFAULT_I2C_BUS = 1
DEFAULT_I2C_ADDR = 0x2F

REG_PID = 0xFD
EMC2301_PID = 0x37
REG_FAN1_SETTING = 0x30
REG_PWM_OUTPUT_CONFIG = 0x2B
REG_FAN1_CONFIG1 = 0x32

REG_CONFIG    = 0x20   # Configuration register (WD_EN bit = 0x20)
REG_FAN1_SPIN = 0x36   # Fan1 Spin-Up Configuration (NKCK1 bit = 0x20)


def _percent_to_value(pct):
    if pct <= 0:
        return 0
    if pct >= 100:
        return 255
    return int(round(pct * 255.0 / 100.0))


class SIBSLED:
    def __init__(
        self,
        pwm_pin=DEFAULT_PWM_PIN,
        enable_pin=DEFAULT_ENABLE_PIN,
        freq=1000,
        start_pct=20.0,
        max_pct=90.0,
        i2c_bus=DEFAULT_I2C_BUS,
        i2c_addr=DEFAULT_I2C_ADDR,
    ):
        self.start_pct = max(0.0, min(100.0, float(start_pct)))
        self.max_pct = max(0.0, min(100.0, float(max_pct)))
        self.freq = int(freq)
        self.pwm_pin = pwm_pin
        self.enable_pin = enable_pin

        self.i2c_bus = int(i2c_bus)
        self.i2c_addr = int(i2c_addr)
        self.led_on = False
        self._brightness_pct = 0.0
        self._bus_lock = Lock()

        try:
            self.bus = SMBus(self.i2c_bus)
            self._configure_emc2301()
            self._write_percent(0.0)
        except Exception as e:
            fatal(f"Could not initialize EMC2301 on i2c-{self.i2c_bus} addr=0x{self.i2c_addr:02X}: {e}")
            raise

        info(
            f"SIBSLED initialized via EMC2301 i2c-{self.i2c_bus} addr=0x{self.i2c_addr:02X} "
            f"start={self.start_pct:.1f}% max={self.max_pct:.1f}%"
        )

    def _readb(self, reg):
        return self.bus.read_byte_data(self.i2c_addr, reg)

    def _writeb(self, reg, val):
        self.bus.write_byte_data(self.i2c_addr, reg, val & 0xFF)

    def _configure_emc2301(self):
        with self._bus_lock:
            pid = self._readb(REG_PID)
            if pid != EMC2301_PID:
                raise RuntimeError(
                    f"Unexpected EMC2301 Product ID 0x{pid:02X}; expected 0x{EMC2301_PID:02X}"
                )

            # Ensure closed-loop (ENAG1) is cleared so direct writes work
            cfg = self._readb(REG_FAN1_CONFIG1)
            if (cfg & 0x80) != 0:
                self._writeb(REG_FAN1_CONFIG1, cfg & ~0x80)
                time.sleep(0.05)

            # Ensure PWM1 push-pull for LED -> resistor -> GND wiring
            pwmcfg = self._readb(REG_PWM_OUTPUT_CONFIG)
            if (pwmcfg & 0x01) == 0:
                self._writeb(REG_PWM_OUTPUT_CONFIG, pwmcfg | 0x01)
                time.sleep(0.05)

            # --- NEW: Disable watchdog (clear WD_EN in reg 0x20) ---
            try:
                cfg20 = self._readb(REG_CONFIG)
                if (cfg20 & 0x20) != 0:              # WD_EN bit set?
                    new_cfg20 = cfg20 & ~0x20        # clear WD_EN
                    self._writeb(REG_CONFIG, new_cfg20)
                    time.sleep(0.02)
                    info(f"Cleared WD_EN (reg 0x20: 0x{cfg20:02X} -> 0x{new_cfg20:02X})")
            except Exception as e:
                # nonfatal: log and continue
                warn(f"Could not update watchdog bit (reg 0x20): {e}")

            # --- NEW: Enable No-Kick (NKCK1 bit) and set minimal spin level/time ---
            # NKCK1 = bit5 (0x20). SPLV[4:2] + SPT[1:0] occupy bits [4:0].
            # We clear bits 4..0 (spin-level/time -> SPLV=000 (30%), SPT=00 (250ms))
            # and set NKCK1 (bit5).
            try:
                spin = self._readb(REG_FAN1_SPIN)
                new_spin = (spin & ~0x1F) | 0x20   # clear SPLV/SPT, set NKCK1
                if new_spin != spin:
                    self._writeb(REG_FAN1_SPIN, new_spin)
                    time.sleep(0.02)
                    info(f"Set No-Kick & minimal spin (reg 0x36: 0x{spin:02X} -> 0x{new_spin:02X})")
            except Exception as e:
                warn(f"Could not update spin-up config (reg 0x36): {e}")

    def _write_percent(self, pct):
        pct_clamped = max(0.0, min(100.0, float(pct)))
        reg_val = _percent_to_value(pct_clamped)
        with self._bus_lock:
            self._writeb(REG_FAN1_SETTING, reg_val)
            time.sleep(0.02)
            rb = self._readb(REG_FAN1_SETTING)

        self._brightness_pct = (rb / 255.0) * 100.0
        self.led_on = rb > 0
        return rb

    def on(self, start_pct=None):
        req = self.start_pct if start_pct is None else float(start_pct)
        pct = max(0.0, min(100.0, req))
        if pct > self.max_pct:
            warn(
                f"Requested start_pct {pct:.1f}% greater than max {self.max_pct:.1f}% - clamping"
            )
            pct = self.max_pct
        try:
            rb = self._write_percent(pct)
            info(f"LED enabled - reg 0x30=0x{rb:02X} ({self._brightness_pct:.1f}%)")
        except Exception as e:
            error(f"Error enabling LED: {e}")
            raise

    def set_brightness(self, pct):
        try:
            pctf = float(pct)
        except Exception:
            error(f"set_brightness: invalid pct {pct!r}")
            return

        pct_clamped = max(0.0, min(100.0, pctf))
        if pct_clamped > self.max_pct:
            warn(f"Requested {pctf:.1f}% > max {self.max_pct:.1f}%; clamping")
            pct_clamped = self.max_pct

        try:
            rb = self._write_percent(pct_clamped)
            info(f"Brightness set - reg 0x30=0x{rb:02X} ({self._brightness_pct:.1f}%)")
        except Exception as e:
            error(f"Error setting brightness to {pct_clamped:.1f}%: {e}")
            raise

    def off(self):
        try:
            rb = self._write_percent(0.0)
            info(f"LED disabled - reg 0x30=0x{rb:02X}")
        except Exception as e:
            error(f"Error disabling LED: {e}")
            raise

    def is_on(self):
        try:
            return bool(self.led_on)
        except Exception:
            return False

    def close(self):
        try:
            self._write_percent(0.0)
            with self._bus_lock:
                self.bus.close()
            info("SIBSLED closed")
        except Exception as e:
            warn(f"Error closing SIBSLED: {e}")