from threading import Thread, Event
from loggerthyst import info
import time

current_interval = None
timer_thread = None
stop_event = Event()


def get_current_interval():
    info(current_interval)
    return current_interval


def start_timer(interval_mins, wiper):
    """Background timer that runs the specified action at the given interval."""
    interval_seconds = interval_mins  # * 60  # Convert mins to seconds
    while not stop_event.wait(interval_seconds):
        wipe(wiper)


def set_new_timer(interval_mins, wiper):
    """Stop the current timer and start a new one if interval is set."""
    global timer_thread, stop_event, current_interval

    # Stop the current timer thread if it exists
    if timer_thread and timer_thread.is_alive():
        info("Stopping the current timer...")
        stop_event.set()  # Signal the thread to stop
        timer_thread.join()  # Wait for it to finish

    # If the new interval is "off," just update the current interval
    if interval_mins == 0:
        current_interval = None
        info("Timer turned off.")
        return

    # Start a new timer thread with the updated interval
    stop_event.clear()  # Reset the event flag for the new timer
    current_interval = interval_mins
    timer_thread = Thread(target=start_timer, args=(
        interval_mins, wiper,), daemon=True)
    timer_thread.start()
    info(f"Timer set to run every {interval_mins} mins.")


def wipe(wiper):
    info("Wiping the camera lens...")
    wiper.wipe()
