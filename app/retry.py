"""Task 22: retry and failure-recovery decorator.

Use it on any function that can fail for a short time
(network call, database busy, email server down).
"""
import functools
import time

from app.logger import log


def retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    """Call the function again if it raises one of `exceptions`.

    max_attempts : total tries (first call + retries)
    delay        : seconds to wait before the first retry
    backoff      : each wait is multiplied by this (1s, 2s, 4s ...)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        log.error("%s failed after %d attempts: %s",
                                  func.__name__, attempt, e)
                        raise  # give up: let the caller see the real error
                    log.warning("%s failed (attempt %d/%d): %s. Retrying in %.1fs",
                                func.__name__, attempt, max_attempts, e, wait)
                    time.sleep(wait)
                    wait *= backoff

        return wrapper

    return decorator
