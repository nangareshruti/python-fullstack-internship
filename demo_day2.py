"""Run:  python demo_day2.py   -> shows retry and cache working."""
import random
import time

from app.cache import cache_with_ttl
from app.retry import retry


@retry(max_attempts=4, delay=0.2)
def unreliable_service():
    if random.random() < 0.6:
        raise ConnectionError("server busy")
    return "got the data"


@cache_with_ttl(ttl_seconds=3)
def slow_lookup(name):
    time.sleep(1)  # pretend this is a slow database call
    return f"result for {name}"


print("--- retry demo ---")
try:
    print(unreliable_service())
except ConnectionError:
    print("Gave up after 4 attempts (see app.log)")

print("--- cache demo ---")
for i in (1, 2):
    start = time.perf_counter()
    print(slow_lookup("asha"), f"-> took {time.perf_counter() - start:.2f}s")
