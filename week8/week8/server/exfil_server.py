#!/usr/bin/env python3
"""
Week 8 - Vidar emulation - Lab C2 simulator.

This is a minimal, fully local HTTP server used ONLY inside the isolated
lab network to:
  1. Serve a "dead drop" text file at /deaddrop.txt containing the fake
     C2 upload address (simulates Vidar resolving its C2 from a public
     profile page).
  2. Accept the POSTed "loot" archive at /upload and save it to disk so
     the group can show it arrived (for the demo / screenshots).

Usage:
    python3 exfil_server.py --port 8000

Then point step4_exfiltration.ps1's -DeadDropUrl at:
    http://<this-host-ip>:8000/deaddrop.txt

Do NOT expose this server outside your isolated lab network.
"""

import argparse
import datetime
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

RECEIVED_DIR = "received_loot"


class EmuHandler(BaseHTTPRequestHandler):
    def _log(self, msg):
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        print(f"[{ts}] {msg}")

    def do_GET(self):
        if self.path == "/deaddrop.txt":
            # The "dead drop" response: where the "stealer" should upload loot.
            host = self.headers.get("Host", "127.0.0.1:8000")
            c2_address = f"http://{host}/upload"
            body = c2_address.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self._log(f"Served dead-drop C2 address to {self.client_address[0]}: {c2_address}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/upload":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)

            os.makedirs(RECEIVED_DIR, exist_ok=True)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(RECEIVED_DIR, f"emu_loot_{ts}.zip")
            with open(out_path, "wb") as f:
                f.write(data)

            self._log(f"Received {length} bytes from {self.client_address[0]} -> saved to {out_path}")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence default noisy logging; we do our own via _log()
        pass


def main():
    parser = argparse.ArgumentParser(description="Week 8 lab C2 simulator")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--bind", default="0.0.0.0")
    args = parser.parse_args()

    server = HTTPServer((args.bind, args.port), EmuHandler)
    print(f"[*] Lab C2 simulator listening on {args.bind}:{args.port}")
    print(f"[*] Dead drop:  http://<host-ip>:{args.port}/deaddrop.txt")
    print(f"[*] Upload URL: http://<host-ip>:{args.port}/upload")
    print("[*] Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server.")
        server.server_close()


if __name__ == "__main__":
    main()
