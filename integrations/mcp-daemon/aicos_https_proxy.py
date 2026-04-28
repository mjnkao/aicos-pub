#!/usr/bin/env python3
"""
AICOS HTTPS proxy — wraps the HTTP daemon with TLS.

Listens on HTTPS (default :8443), forwards every request to the
HTTP daemon (default http://127.0.0.1:8000).

Usage:
    python3 aicos_https_proxy.py \
        --cert ~/.local/share/mkcert/localhost+2.pem \
        --key  ~/.local/share/mkcert/localhost+2-key.pem \
        --https-port 8443 \
        --daemon-url http://127.0.0.1:8000
"""
from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import ssl
import urllib.request
import urllib.error
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key:
            os.environ.setdefault(key, value.strip().strip("'").strip('"'))


class _ProxyHandler(http.server.BaseHTTPRequestHandler):
    daemon_url: str = "http://127.0.0.1:8000"
    upstream_token: str = ""

    def log_message(self, fmt, *args):
        import sys, datetime
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {self.address_string()} {fmt % args}", file=sys.stderr, flush=True)

    def _forward(self) -> None:
        target = self.daemon_url.rstrip("/") + self.path
        body_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(body_len) if body_len else None

        headers = {
            k: v for k, v in self.headers.items()
            if k.lower() not in ("host", "content-length")
        }
        if self.upstream_token and "Authorization" not in headers and "authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.upstream_token}"

        req = urllib.request.Request(
            target,
            data=body,
            method=self.command,
            headers=headers,
        )
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() in ("content-type", "content-length", "cache-control"):
                        self.send_header(k, v)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as exc:
            self.send_response(exc.code)
            self.end_headers()
            self.wfile.write(exc.read())
        except Exception as exc:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Proxy error: {exc}".encode())

    def do_GET(self) -> None:
        self._forward()

    def do_POST(self) -> None:
        self._forward()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()


class _ThreadingHTTPS(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> None:
    ap = argparse.ArgumentParser(description="AICOS HTTPS proxy")
    default_env_file = Path(os.environ.get("AICOS_DAEMON_ENV_FILE", str(Path(__file__).resolve().parents[2] / ".runtime-home/aicos-daemon.env")))
    ap.add_argument("--env-file", default=str(default_env_file))
    args, remaining = ap.parse_known_args()
    load_env_file(Path(args.env_file).expanduser())

    default_cert = os.environ.get("AICOS_HTTPS_CERT", str(Path.home() / ".local/share/mkcert/localhost+2.pem"))
    default_key = os.environ.get("AICOS_HTTPS_KEY", str(Path.home() / ".local/share/mkcert/localhost+2-key.pem"))
    ap = argparse.ArgumentParser(description="AICOS HTTPS proxy")
    ap.add_argument("--cert", default=default_cert)
    ap.add_argument("--key",  default=default_key)
    ap.add_argument("--https-port", type=int, default=8443)
    ap.add_argument("--host", default=os.environ.get("AICOS_HTTPS_HOST", "127.0.0.1"))
    ap.add_argument("--daemon-url", default="http://127.0.0.1:8000")
    ap.add_argument("--env-file", default=str(default_env_file))
    args = ap.parse_args()

    _ProxyHandler.daemon_url = args.daemon_url
    _ProxyHandler.upstream_token = os.environ.get("AICOS_HTTPS_UPSTREAM_TOKEN", os.environ.get("AICOS_DAEMON_TOKEN", ""))

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=args.cert, keyfile=args.key)

    server = _ThreadingHTTPS((args.host, args.https_port), _ProxyHandler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    print(f"[aicos-https] HTTPS proxy started")
    print(f"[aicos-https]   https://{args.host}:{args.https_port}/mcp")
    if args.host != "localhost":
        print(f"[aicos-https]   https://localhost:{args.https_port}/mcp")
    print(f"[aicos-https]   -> forwarding to {args.daemon_url}")
    print(f"[aicos-https]   upstream auth: {'static bearer token' if _ProxyHandler.upstream_token else 'passthrough only'}")
    server.serve_forever()


if __name__ == "__main__":
    main()
