import time
import serial
from loggerthyst import info, error, fatal, warn

def send_sampler_trigger(sampler, port="/dev/serial0", baud=9600,
                         read_after=0.20, read_timeout=0.1):
    """
    Send "*SSCTRG{sampler}\\r\\n" to `port`@`baud`.
    - sampler: int 1..3
    - read_after: seconds to collect unsolicited RX after send
    - read_timeout: pyserial timeout when opening the port

    Returns True on success, False on failure.
    """
    if sampler not in (1, 2, 3):
        error(f"send_sampler_trigger: invalid sampler {sampler} (must be 1,2,3)")
        return False

    cmd_text = f"*SSCTRG{sampler}\r\n"
    cmd_bytes = cmd_text.encode("ascii")

    info(f"send_sampler_trigger: sampler={sampler} port={port} baud={baud}")
    try:
        ser = serial.Serial(port, baud, timeout=read_timeout)
    except PermissionError as e:
        fatal(f"Permission denied opening serial port {port}: {e}")
        return False
    except serial.SerialException as e:
        error(f"Could not open serial port {port}: {e}")
        return False

    try:
        # clear buffers if available
        try:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
        except Exception:
            pass

        try:
            ser.write(cmd_bytes)
            ser.flush()
            info(f"Sent TX -> {cmd_text.replace(chr(13)+chr(10), '\\r\\n')}")
        except Exception as e:
            error(f"Failed to write to serial port: {e}")
            return False

        # collect any unsolicited RX for a short window
        deadline = time.time() + read_after
        collected = b""
        while time.time() < deadline:
            try:
                waiting = ser.in_waiting or 0
            except (serial.SerialException, OSError) as e:
                error(f"Error checking in_waiting: {e}")
                break

            if waiting:
                try:
                    chunk = ser.read(waiting)
                except serial.SerialException as e:
                    error(f"Serial read error: {e}")
                    break

                if chunk:
                    collected += chunk
                    time.sleep(0.01)
                else:
                    warn(f"read() returned no data though in_waiting={waiting}")
                    break
            else:
                time.sleep(0.02)

        if collected:
            try:
                decoded = collected.decode("utf-8", errors="replace")
            except Exception:
                decoded = repr(collected)
            info(f"RX (serial unsolicited) from {port}: {decoded}")
        else:
            info("No unsolicited RX received after TX.")

    finally:
        try:
            ser.close()
            info(f"Closed serial port {port}")
        except Exception as e:
            warn(f"Error closing serial port {port}: {e}")

    return True