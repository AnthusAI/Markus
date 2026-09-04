"""Live preview server for Markus source."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import urlparse

from markusmd.api import convert
from markusmd.errors import MarkusError
from markusmd.render import default_css


def serve_preview(*, host: str, port: int, initial: str = "") -> None:
    playground = files("markusmd").joinpath("static", "playground.html").read_text(encoding="utf-8")
    if initial:
        playground = playground.replace("/*INITIAL_SOURCE*/", json.dumps(initial))
    else:
        playground = playground.replace("/*INITIAL_SOURCE*/", "null")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in {"/", "/index.html"}:
                self._send(200, "text/html; charset=utf-8", playground.encode("utf-8"))
            elif path == "/markus.css":
                self._send(200, "text/css; charset=utf-8", default_css().encode("utf-8"))
            elif path == "/health":
                self._send(200, "text/plain; charset=utf-8", b"ok\n")
            else:
                self._send(404, "text/plain; charset=utf-8", b"not found\n")

        def do_POST(self) -> None:  # noqa: N802
            if urlparse(self.path).path != "/convert":
                self._send(404, "text/plain; charset=utf-8", b"not found\n")
                return
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            source = payload.get("source", "")
            try:
                html = convert(source, include_css=False, full_document=False)
                body = json.dumps({"html": html}).encode("utf-8")
                self._send(200, "application/json; charset=utf-8", body)
            except MarkusError as exc:
                body = json.dumps({"error": str(exc), "line": exc.line}).encode("utf-8")
                self._send(400, "application/json; charset=utf-8", body)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            print(f"[markus] {self.address_string()} {format % args}")

        def _send(self, status: int, content_type: str, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Markus preview at http://{host}:{port}/")
    httpd.serve_forever()
