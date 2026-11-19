"""Run:  python demo_async.py
Compares fetching 5 slow URLs one by one vs all together."""
import asyncio
import time

from app.async_client import fetch_json, fetch_many
from app.demo_server import start_server

server, base = start_server(delay=1.0)  # every request takes 1 second
urls = [f"{base}/ok/{i}" for i in range(5)]

start = time.perf_counter()
for u in urls:
    fetch_json(u)
print(f"One by one  : {time.perf_counter() - start:.1f}s")

start = time.perf_counter()
results = asyncio.run(fetch_many(urls))
print(f"All together: {time.perf_counter() - start:.1f}s  ({sum(r['ok'] for r in results)} ok)")

server.shutdown()
