import serial
import time
from loggerthyst import info, error

# Serial port configuration for SSC trigger controller
SERIAL_PORT = "/dev/ttyAMA0"  # Raspberry Pi Zero 2 W UART (GPIO 14/15)
BAUD_RATE = 9600
DATA_BITS = 8
STOP_BITS = 1
TIMEOUT = 2  # Read timeout in seconds

# Command templates for SSC trigger controller
TRIGGER_COMMANDS = {
    1: "*SSCTRG1",
    2: "*SSCTRG2",
    3: "*SSCTRG3",
}


def trigger_sample(trigger):
    """
    Triggers the specified sampler port via serial communication with SSC trigger controller.
    
    Args:
        trigger (int): Sampler port number (1, 2, or 3)
        
    Returns:
        bool: True if trigger was successful, False otherwise
    """
    # Validate trigger parameter
    if trigger not in TRIGGER_COMMANDS:
        error(f"Invalid trigger port: {trigger}. Must be 1, 2, or 3.")
        return False
    
    try:
        # Open serial connection with specified configuration
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=DATA_BITS,
            stopbits=STOP_BITS,
            parity=serial.PARITY_NONE,
            timeout=TIMEOUT
        )
        
        # Build command with CR+LF (end of line indicators)
        command = TRIGGER_COMMANDS[trigger] + "\r\n"
        
        # Send command to controller
        ser.write(command.encode('utf-8'))
        info(f"Sent trigger command for sampler port {trigger}: {command.strip()}")
        
        # Read response from controller
        try:
            response = ser.read(100).decode('utf-8', errors='ignore').strip()
            if response:
                info(f"SSC controller response: {response}")
        except Exception as e:
            error(f"Error reading response from SSC controller: {e}")
        
        # Close serial connection
        ser.close()
        return True
        
    except serial.SerialException as e:
        error(f"Serial communication error: {e}")
        return False
    except Exception as e:
        error(f"Unexpected error in trigger_sample: {e}")
        return False
    