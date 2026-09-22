#!/usr/bin/env python3
"""A reverse proxy that makes CHAP's model configuration reach a chapkit service.

CHAP and this model disagree about where a configuration's values live, and each end
refuses the other's shape:

* `chap eval --model-configuration-yaml` validates against chap-core's `ModelConfiguration`,
  which is `extra="forbid"` with exactly two fields, so the values must be **nested** under
  `user_option_values`. A flat mapping is rejected before any request is made.
* The model's service stores a **flat** mapping. Handed the nested one it returns HTTP 201,
  fills every option from its own defaults, keeps the nested block as an inert extra, and
  fits with the defaults. Nothing reports this.

So the one shape CHAP will send is the one the model discards, and a configured run is
indistinguishable from an unconfigured one. This proxy sits between them and rewrites exactly
one thing: the body of `POST /api/v1/configs`, lifting `data.user_option_values` up into
`data`. Every other request and response is forwarded untouched.

**Neither the model nor the platform is modified.** This is a workaround outside both, and it
is the only way to ask what a configured run of this model does.

    python config_proxy.py --listen 8100 --upstream http://localhost:8000

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "http://localhost:8000"
HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "content-length", "host",
}
REWRITES: list[str] = []


def flatten(body: bytes) -> tuple[bytes, str | None]:
    """Lift data.user_option_values into data. Returns the body and what changed, if anything."""
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        return body, None
    if not isinstance(payload, dict):
        return body, None
    data = payload.get("data")
    if not isinstance(data, dict):
        return body, None
    nested = data.get("user_option_values")
    if not isinstance(nested, dict) or not nested:
        return body, None

    merged = {k: v for k, v in data.items() if k != "user_option_values"}
    merged.update(nested)          # the operator's values win over anything alongside them
    payload["data"] = merged
    return json.dumps(payload).encode(), ", ".join(f"{k}={v!r}" for k, v in nested.items())


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):      # one line per rewrite is enough noise
        return

    def _proxy(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        if body and self.command == "POST" and self.path.rstrip("/").endswith("/configs"):
            body, changed = flatten(body)
            if changed:
                REWRITES.append(changed)
                print(f"[proxy] flattened config: {changed}", flush=True)

        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP_BY_HOP}
        req = urllib.request.Request(
            UPSTREAM + self.path, data=body, method=self.command, headers=headers
        )
        try:
            with urllib.request.urlopen(req, timeout=1800) as resp:
                payload, status, out_headers = resp.read(), resp.status, resp.headers
        except urllib.error.HTTPError as e:
            payload, status, out_headers = e.read(), e.code, e.headers
        except Exception as e:                                  # upstream unreachable
            payload, status, out_headers = str(e).encode(), 502, {}

        self.send_response(status)
        for k, v in (out_headers.items() if out_headers else []):
            if k.lower() not in HOP_BY_HOP:
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = _proxy


def main() -> int:
    global UPSTREAM
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--listen", type=int, default=8100)
    ap.add_argument("--upstream", default=UPSTREAM)
    a = ap.parse_args()
    UPSTREAM = a.upstream.rstrip("/")
    print(f"[proxy] :{a.listen} -> {UPSTREAM}, flattening POST /api/v1/configs", flush=True)
    try:
        ThreadingHTTPServer(("127.0.0.1", a.listen), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
