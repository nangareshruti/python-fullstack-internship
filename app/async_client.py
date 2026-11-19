"""Task 20: asynchronous API client.

Fetches many URLs AT THE SAME TIME instead of one after another.
Uses only Python's standard library (asyncio + urllib), nothing to install.
"""
import asyncio
import json
import urllib.error
import urllib.request
from typing import List

from app.logger import log
from app.retry import retry


class ApiError(Exception):
    """The server answered, but with an error like 404 (retrying won't help)."""


@retry(max_attempts=3, delay=0.2, exceptions=(urllib.error.URLError, TimeoutError, ConnectionError))
def fetch_json(url: str, timeout: float = 10) -> dict:
    """Normal (blocking) request. Retries network problems and 5xx errors."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code >= 500:
            raise  # server problem -> @retry will try again
        raise ApiError(f"HTTP {e.code} for {url}") from e


async def fetch_json_async(url: str) -> dict:
    # to_thread runs the blocking request in a helper thread,
    # so the event loop can start other requests meanwhile.
    return await asyncio.to_thread(fetch_json, url)


async def fetch_many(urls: List[str], max_concurrent: int = 5) -> List[dict]:
    """Fetch all urls together (at most `max_concurrent` at once).

    One failing URL does NOT stop the others. Each result looks like:
      {"url": ..., "ok": True,  "data": {...}}
      {"url": ..., "ok": False, "error": "..."}
    """
    limit = asyncio.Semaphore(max_concurrent)

    async def one(url: str) -> dict:
        async with limit:
            try:
                return {"url": url, "ok": True, "data": await fetch_json_async(url)}
            except Exception as e:  # keep going, report the error instead
                log.warning("fetch failed %s: %s", url, e)
                return {"url": url, "ok": False, "error": str(e)}

    return await asyncio.gather(*(one(u) for u in urls))
