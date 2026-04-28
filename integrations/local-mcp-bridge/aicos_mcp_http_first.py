#!/usr/bin/env python3
"""AICOS MCP stdio proxy: HTTP daemon first, local stdio fallback.

Codex Desktop currently configures MCP servers as local commands. This proxy
keeps that stdio shape while preferring the AICOS HTTP daemon for every JSON-RPC
message. If the daemon is unavailable, the local stdio handler is used so agents
can keep working with bounded markdown-direct behavior.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_URL = "http://127.0.0.1:8000/mcp"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(REPO_ROOT / ".runtime-home/aicos-daemon.env")

sys.path.insert(0, str(Path(__file__).parent))
import aicos_mcp_stdio  # noqa: E402


def _daemon_request(message: dict[str, Any]) -> dict[str, Any] | None:
    url = os.environ.get("AICOS_MCP_DAEMON_URL", DEFAULT_URL).rstrip("/")
    token = os.environ.get("AICOS_DAEMON_TOKEN", "")
    body = json.dumps(message).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=float(os.environ.get("AICOS_MCP_HTTP_TIMEOUT", "2"))) as response:
        if response.status == 204:
            return None
        return json.loads(response.read().decode("utf-8"))


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    try:
        return _daemon_request(message)
    except (OSError, TimeoutError, urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return aicos_mcp_stdio.handle(message)


def main() -> int:
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped:
            continue
        try:
            message = json.loads(stripped)
        except json.JSONDecodeError as exc:
            print(json.dumps(aicos_mcp_stdio.error_response(None, -32700, f"Parse error: {exc}")), flush=True)
            continue
        result = handle(message)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
