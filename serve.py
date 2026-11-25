#!/usr/bin/env python3
"""Local-only server. No account access, network downloads or public binding."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import functools
ROOT=Path(__file__).resolve().parent/'dist'
class Handler(SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('X-Content-Type-Options','nosniff')
  self.send_header('Referrer-Policy','no-referrer')
  self.send_header('Cache-Control','no-cache')
  super().end_headers()
print('VERSE ONE local pilot: http://127.0.0.1:8080/ — Ctrl+C to stop.',flush=True)
ThreadingHTTPServer(('127.0.0.1',8080),functools.partial(Handler,directory=str(ROOT))).serve_forever()
