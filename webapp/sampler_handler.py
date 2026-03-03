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
        error("send_sampler_trigger: invalid sampler %r (must be 1,2,3)", sampler)
        return False

    cmd_text = f"*SSCTRG{sampler}\r\n"
    cmd_bytes = cmd_text.encode("ascii")

    info("send_sampler_trigger: sampler=%d port=%s baud=%d", sampler, port, baud)
    try:
        ser = serial.Serial(port, baud, timeout=read_timeout)
    except PermissionError as e:
        fatal("Permission denied opening serial port %s: %s", port, e)
        return False
    except serial.SerialException as e:
        error("Could not open serial port %s: %s", port, e)
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
            info("Sent TX -> %s", cmd_text.replace("\r\n", "\\r\\n"))
        except Exception as e:
            error("Failed to write to serial port: %s", e)
            return False

        # collect any unsolicited RX for a short window
        deadline = time.time() + read_after
        collected = b""
        while time.time() < deadline:
            try:
                waiting = ser.in_waiting or 0
            except (serial.SerialException, OSError) as e:
                error("Error checking in_waiting: %s", e)
                break

            if waiting:
                try:
                    chunk = ser.read(waiting)
                except serial.SerialException as e:
                    error("Serial read error: %s", e)
                    break

                if chunk:
                    collected += chunk
                    time.sleep(0.01)
                else:
                    warn("read() returned no data though in_waiting=%d", waiting)
                    break
            else:
                time.sleep(0.02)

        if collected:
            try:
                decoded = collected.decode("utf-8", errors="replace")
            except Exception:
                decoded = repr(collected)
            info("RX (serial unsolicited) from %s: %s", port, decoded)
        else:
            info("No unsolicited RX received after TX.")

    finally:
        try:
            ser.close()
            info("Closed serial port %s", port)
        except Exception as e:
            warn("Error closing serial port %s: %s", port, e)

    return True