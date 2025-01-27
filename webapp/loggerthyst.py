import datetime
import colorama
from colorama import Fore as f
import inspect

colorama.init(autoreset=True)


def _get_caller_info():
    """Returns the file name and line number of the caller."""
    frame = inspect.stack()[2]
    return frame.filename, frame.lineno


def info(message: str):
    """Prints as an info block with time and date.
    \nUseful for logging certain events to make sure they happen as expected

    Args:
        message (str): The string you want to be printed as info
    """
    now = datetime.datetime.now()
    filename, lineno = _get_caller_info()
    print(
        f.GREEN
        + f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')} | {filename}:{lineno}] "
        + f.WHITE
        + f"{message}"
    )


def warn(message: str):
    """Prints as a warning block with time and date.
    \nUseful for logging warnings on things that might not be ideal

    Args:
        message (str): The string you want to be printed as a warning
    """
    now = datetime.datetime.now()
    filename, lineno = _get_caller_info()
    print(
        f.YELLOW
        + f"[WARN | {now.strftime('%Y-%m-%d %H:%M:%S')} | {filename}:{lineno}] "
        + f.WHITE
        + f"{message}"
    )


def error(message: str):
    """Prints as an error block with time and date.
    \nUseful for logging errors such as features not working as expected

    Args:
        message (str): The string you want to be printed as an error
    """
    now = datetime.datetime.now()
    filename, lineno = _get_caller_info()
    print(
        f.RED
        + f"[ERROR | {now.strftime('%Y-%m-%d %H:%M:%S')} | {filename}:{lineno}] "
        + f.WHITE
        + f"{message}"
    )


def fatal(message: str):
    """Prints as a fatal error block with time and date.
    \nUseful for logging fatal errors such as crashes

    Args:
        message (str): The string you want to be printed as a fatal error
    """
    now = datetime.datetime.now()
    filename, lineno = _get_caller_info()
    print(
        f.LIGHTRED_EX
        + f"[FATAL | {now.strftime('%Y-%m-%d %H:%M:%S')} | {filename}:{lineno}] "
        + f.WHITE
        + f"{message}"
    )
