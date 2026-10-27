"""A dependency-free WSGI app for learning Git, testing, and delivery."""

import json
import os
from html import escape
from wsgiref.simple_server import make_server

APP_VERSION = "0.1.0"
DEFAULT_MESSAGE = "Hello from my home lab!"


def application(environ, start_response):
    """Handle one request; WSGI lets us swap servers in a later lab."""
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    headers = []
    status = "200 OK"
    content_type = "application/json; charset=utf-8"

    if method not in ("GET", "HEAD"):
        status = "405 Method Not Allowed"
        headers.append(("Allow", "GET, HEAD"))
        body = json.dumps({"error": "method not allowed"})
    elif path == "/":
        content_type = "text/html; charset=utf-8"
        message = escape(os.environ.get("APP_MESSAGE", DEFAULT_MESSAGE))
        body = (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Lab Status</title></head><body><h1>Lab Status</h1>'
            f'<p>{message}</p><p>Version: {APP_VERSION}</p>'
            '<nav><a href="/health">Health</a> | '
            '<a href="/version">Version details</a></nav></body></html>'
        )
    elif path == "/health":
        body = json.dumps({"status": "ok"})
    elif path == "/version":
        body = json.dumps({
            "version": APP_VERSION,
            "commit": os.environ.get("GIT_COMMIT", "unknown"),
        })
    else:
        status = "404 Not Found"
        body = json.dumps({"error": "not found"})

    encoded = body.encode("utf-8")
    headers.extend([
        ("Content-Type", content_type),
        ("Content-Length", str(len(encoded))),
    ])
    start_response(status, headers)
    return [b"" if method == "HEAD" else encoded]


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    # This simple server is for the lab, not production hosting.
    with make_server(host, port, application) as server:
        print(f"Lab Status listening on http://{host}:{port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
