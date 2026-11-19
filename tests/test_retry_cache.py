"""Tests for tasks 21 (cache) and 22 (retry)."""
import time

import pytest

from app.cache import cache_with_ttl
from app.retry import retry


def test_retry_succeeds_after_failures():
    calls = {"n": 0}

    @retry(max_attempts=3, delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("temporary problem")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_retry_gives_up_and_raises():
    calls = {"n": 0}

    @retry(max_attempts=3, delay=0)
    def always_fails():
        calls["n"] += 1
        raise ValueError("broken")

    with pytest.raises(ValueError):
        always_fails()
    assert calls["n"] == 3


def test_retry_only_for_chosen_exceptions():
    calls = {"n": 0}

    @retry(max_attempts=3, delay=0, exceptions=(ConnectionError,))
    def wrong_error():
        calls["n"] += 1
        raise KeyError("not retried")

    with pytest.raises(KeyError):
        wrong_error()
    assert calls["n"] == 1


def test_cache_returns_stored_result():
    calls = {"n": 0}

    @cache_with_ttl(ttl_seconds=5)
    def slow_square(x):
        calls["n"] += 1
        return x * x

    assert slow_square(4) == 16
    assert slow_square(4) == 16
    assert calls["n"] == 1          # second call came from the cache
    assert slow_square(5) == 25     # different argument -> runs again
    assert calls["n"] == 2


def test_cache_expires():
    calls = {"n": 0}

    @cache_with_ttl(ttl_seconds=0.05)
    def get_value():
        calls["n"] += 1
        return calls["n"]

    get_value()
    time.sleep(0.08)
    get_value()
    assert calls["n"] == 2


def test_cache_clear():
    calls = {"n": 0}

    @cache_with_ttl(ttl_seconds=5)
    def f():
        calls["n"] += 1

    f()
    f.cache_clear()
    f()
    assert calls["n"] == 2
