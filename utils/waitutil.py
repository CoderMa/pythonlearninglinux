import time
from collections.abc import Callable


class TimeoutException(Exception):

    def __init__(self, msg, timeout):
        self.value = "{}\nTimed out after {} seconds".format(msg, timeout)

    def __str__(self):
        return self.value


def wait_for(condition, timeout=5, poll_frequency=0.5, msg=None):
    wait_till = time.time() + timeout
    if not isinstance(condition, Callable):
        raise TimeoutException("Cannot wait for condition " + repr(condition), 0)

    while wait_till > time.time():
        return_value = condition()
        if return_value:
            return return_value
        time.sleep(poll_frequency)

    raise TimeoutException(msg or repr(condition), timeout)
