#!/usr/bin/env python3
"""Compatibility shim between chap-core 2.1.0 and a chapkit 2.0.0 service.

Why this exists
---------------
chap-core 2.1.0 validates a chapkit service's ``GET /api/v1/info`` payload with
``chapkit.api.service_builder.MLServiceInfo`` -- the model class from *the chapkit
package pinned inside chap-core's own virtualenv*, which is chapkit **1.1.0**.
That class is declared with ``extra="forbid"``.

chapkit **2.0.0** (what chapkit_ghr_model 60b16a2 is built on) adds three fields to
that payload: ``git_revision``, ``chapkit_version`` and ``servicekit_version``.
chap-core therefore rejects the service outright:

    ValidationError: 3 validation errors for MLServiceInfo
      git_revision      Extra inputs are not permitted
      chapkit_version   Extra inputs are not permitted
      servicekit_version Extra inputs are not permitted

which surfaces as::

    ValueError: URL http://localhost:8000 was provided but could not be reached as
    a chapkit service.

and also defeats ``--run-config.is-chapkit-model``, because that flag only skips the
*probe*; ``ExternalChapkitModelTemplate.name`` calls ``client.info()`` with the same
strict model.

What it does
------------
A transparent reverse proxy. Every request is forwarded verbatim to the real
service. The ONE thing it changes is that the three chapkit-2.0-only keys are
dropped from the JSON body of ``GET /api/v1/info``. Nothing else is touched, and
the model image itself is untouched and unmodified.

Usage:  info_shim.py <listen_port> <upstream_base_url>
"""

import json
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Exactly the keys chapkit 2.0.0 added to MLServiceInfo relative to 1.1.0.
DROPPED_KEYS = ("git_revision", "chapkit_version", "servicekit_version")

UPSTREAM = "http://localhost:8000"
HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
    "content-encoding",
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # quieter
        sys.stderr.write("shim %s\n" % (fmt % args))

    def _proxy(self, method):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        headers = {
            k: v for k, v in self.headers.items() if k.lower() not in HOP_BY_HOP and k.lower() != "host"
        }
        req = urllib.request.Request(UPSTREAM + self.path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=7200) as resp:
                status = resp.status
                raw = resp.read()
                out_headers = [(k, v) for k, v in resp.getheaders() if k.lower() not in HOP_BY_HOP]
        except urllib.error.HTTPError as e:  # forward error responses unchanged
            status = e.code
            raw = e.read()
            out_headers = [(k, v) for k, v in e.headers.items() if k.lower() not in HOP_BY_HOP]
        except Exception as e:  # upstream unreachable
            self.send_response(502)
            msg = json.dumps({"detail": f"shim upstream error: {e}"}).encode()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            return

        # The one and only rewrite.
        if method == "GET" and self.path.rstrip("/") == "/api/v1/info" and status == 200:
            try:
                payload = json.loads(raw)
                for key in DROPPED_KEYS:
                    payload.pop(key, None)
                raw = json.dumps(payload).encode()
            except Exception:
                pass

        self.send_response(status)
        for k, v in out_headers:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        if method != "HEAD":
            self.wfile.write(raw)

    def do_GET(self):
        self._proxy("GET")

    def do_POST(self):
        self._proxy("POST")

    def do_PUT(self):
        self._proxy("PUT")

    def do_DELETE(self):
        self._proxy("DELETE")

    def do_HEAD(self):
        self._proxy("HEAD")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8010
    if len(sys.argv) > 2:
        UPSTREAM = sys.argv[2].rstrip("/")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
