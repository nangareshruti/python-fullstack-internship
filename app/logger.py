"""Tasks 15 + 24: structured logging and a logging decorator."""
import functools
import logging
import time

from app.config import settings


def get_logger(name: str = "student_manager") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(settings.LOG_LEVEL)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    file_handler = logging.FileHandler(settings.LOG_FILE)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    return logger


log = get_logger()


def log_call(func):
    """Log function name, arguments, duration and any exception."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        log.info("CALL %s args=%s kwargs=%s", func.__name__, args[1:], kwargs)
        try:
            result = func(*args, **kwargs)
        except Exception:
            log.exception("ERROR in %s", func.__name__)
            raise
        log.info("DONE %s in %.4fs", func.__name__, time.perf_counter() - start)
        return result

    return wrapper
