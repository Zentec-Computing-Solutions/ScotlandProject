from threading import Thread, Event
import time

current_interval = None
timer_thread = None
stop_event = Event()


def get_current_interval():
    return current_interval


def start_timer(interval_mins, led):
    """Background timer that runs the specified action at the given interval."""
    interval_seconds = interval_mins  # * 60 # Convert mins to seconds
    while not stop_event.wait(interval_seconds):
        wipe(led)


def set_new_timer(interval_mins, led):
    """Stop the current timer and start a new one if interval is set."""
    global timer_thread, stop_event, current_interval

    # Stop the current timer thread if it exists
    if timer_thread and timer_thread.is_alive():
        print("Stopping the current timer...")
        stop_event.set()  # Signal the thread to stop
        timer_thread.join()  # Wait for it to finish

    # If the new interval is "off," just update the current interval
    if interval_mins == 0:
        current_interval = None
        print("Timer turned off.")
        return

    # Start a new timer thread with the updated interval
    stop_event.clear()  # Reset the event flag for the new timer
    current_interval = interval_mins
    timer_thread = Thread(target=start_timer, args=(
        interval_mins, led,), daemon=True)
    timer_thread.start()
    print(f"Timer set to run every {interval_mins} hours.")


def wipe(led):
    print("Wiping the camera lens...")
    led.on()
    time.sleep(3)
    led.off()
