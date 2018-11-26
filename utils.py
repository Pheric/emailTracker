import time


def current_millis():
    """
    Gets the current time in milliseconds since the unix epoch
    """
    return int(round(time.time() * 1000))
