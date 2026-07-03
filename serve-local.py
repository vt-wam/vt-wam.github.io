#!/usr/bin/env python3
"""Local static server with HTTP Range support (required for video seeking)."""

from __future__ import annotations

import http.server
import os
import re
import socket
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_PORT = int(os.environ.get("PORT", "8080"))
PORT_SCAN_END = int(os.environ.get("PORT_SCAN_END", "8090"))


class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    range_start: int = 0
    range_length: int | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        if os.environ.get("SERVE_QUIET") == "1":
            return
        super().log_message(format, *args)

    def end_headers(self) -> None:
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "public, max-age=0")
        super().end_headers()

    def copyfile(self, source, outputfile):
        if self.range_length is not None:
            remaining = self.range_length
            while remaining > 0:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
            return
        super().copyfile(source, outputfile)

    def send_head(self):
        self.range_start = 0
        self.range_length = None

        path = self.translate_path(self.path.split("?", 1)[0])
        if os.path.isdir(path):
            return super().send_head()

        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return None

        file_size = os.path.getsize(path)
        ctype = self.guess_type(path)
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else file_size - 1
                end = min(end, file_size - 1)

                if start > end or start >= file_size:
                    self.send_error(416, "Requested Range Not Satisfiable")
                    return None

                length = end - start + 1
                file_obj = open(path, "rb")
                file_obj.seek(start)

                self.range_start = start
                self.range_length = length

                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.end_headers()
                return file_obj

        file_obj = open(path, "rb")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(file_size))
        self.end_headers()
        return file_obj


class ThreadingReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", port))
        except OSError:
            return False
    return True


def pick_port(requested: int) -> int:
    if port_is_free(requested):
        return requested

    if os.environ.get("PORT"):
        raise SystemExit(
            f"Port {requested} is already in use.\n"
            "Stop the other server first (often `python -m http.server` in another terminal),\n"
            "or choose another port: `$env:PORT=8090; .\\serve-local.ps1`"
        )

    for port in range(requested + 1, PORT_SCAN_END + 1):
        if port_is_free(port):
            print(
                f"Port {requested} is busy (maybe `python -m http.server` is still running).",
                flush=True,
            )
            print(f"Using http://127.0.0.1:{port}/ instead.", flush=True)
            return port

    raise SystemExit(
        f"No free port found between {requested} and {PORT_SCAN_END}.\n"
        "Close other local servers and try again."
    )


def main() -> None:
    os.chdir(ROOT)
    port = pick_port(DEFAULT_PORT)
    with ThreadingReusableTCPServer(("", port), RangeRequestHandler) as httpd:
        print(f"Serving {ROOT}", flush=True)
        print(f"Open http://127.0.0.1:{port}/", flush=True)
        print("Use this server (not `python -m http.server`) so video seeking works.", flush=True)
        print("Press Ctrl+C to stop.", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()

