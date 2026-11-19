"""Tests for task 20. They use a local practice server, so no internet needed."""
import asyncio
import time

from app.async_client import fetch_many
from app.demo_server import start_server


def test_fetch_many_returns_all_results_in_order():
    server, base = start_server(delay=0.1)
    try:
        urls = [f"{base}/ok/{i}" for i in range(5)]
        results = asyncio.run(fetch_many(urls))
    finally:
        server.shutdown()
    assert [r["data"]["n"] for r in results] == [0, 1, 2, 3, 4]
    assert all(r["ok"] for r in results)


def test_requests_run_together_not_one_by_one():
    server, base = start_server(delay=0.4)
    try:
        urls = [f"{base}/ok/{i}" for i in range(5)]
        start = time.perf_counter()
        asyncio.run(fetch_many(urls, max_concurrent=5))
        took = time.perf_counter() - start
    finally:
        server.shutdown()
    # one by one would need 5 x 0.4 = 2.0s; together it is about 0.4s
    assert took < 1.2


def test_one_bad_url_does_not_stop_the_others():
    server, base = start_server(delay=0.05)
    try:
        urls = [f"{base}/ok/1", f"{base}/missing", f"{base}/ok/2"]
        results = asyncio.run(fetch_many(urls))
    finally:
        server.shutdown()
    assert [r["ok"] for r in results] == [True, False, True]
    assert "404" in results[1]["error"]
