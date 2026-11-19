"""A tiny local web server used ONLY for practice and tests.

  /ok/<n>     -> waits `delay` seconds, then returns {"n": <n>}
  anything else -> 404
So we can test the async client without internet.
"""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def start_server(delay: float = 0.3):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/ok/"):
                time.sleep(delay)
                body = json.dumps({"n": int(self.path.split("/")[-1])}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):  # keep the console quiet
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}"
