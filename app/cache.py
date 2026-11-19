"""Task 21: a simple caching mechanism with expiry (TTL)."""
import functools
import time

from app.logger import log


def cache_with_ttl(ttl_seconds=60):
    """Remember a function's result for `ttl_seconds`.

    Same arguments within that time -> the stored result is returned
    and the function is NOT run again. After the time ends, it runs again.
    """

    def decorator(func):
        store = {}  # key -> (time_saved, result)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in store:
                saved_at, result = store[key]
                if now - saved_at < ttl_seconds:
                    log.info("CACHE HIT %s", func.__name__)
                    return result
            log.info("CACHE MISS %s", func.__name__)
            result = func(*args, **kwargs)
            store[key] = (now, result)
            return result

        wrapper.cache_clear = store.clear  # lets you empty the cache manually
        return wrapper

    return decorator
