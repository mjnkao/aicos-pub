#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except ValueError:
        return default


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display notification "{message}" with title "{title}"',
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def env_flag(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def check_health(url: str, token: str) -> tuple[bool, dict[str, Any] | None, str]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
        payload = json.loads(body)
        return True, payload, ""
    except HTTPError as exc:
        return False, None, f"HTTP {exc.code}"
    except URLError as exc:
        return False, None, f"network error: {exc.reason}"
    except Exception as exc:
        return False, None, str(exc)


def trim_log(path: Path, max_bytes: int, backups: int, keep_bytes: int) -> None:
    if not path.exists() or path.stat().st_size <= max_bytes:
        return
    for idx in range(backups, 0, -1):
        older = path.with_name(f"{path.name}.{idx}")
        newer = path.with_name(f"{path.name}.{idx - 1}") if idx > 1 else path
        if older.exists():
            older.unlink()
        if newer.exists():
            shutil.copy2(newer, older)
    data = path.read_bytes()
    tail = data[-keep_bytes:] if len(data) > keep_bytes else data
    path.write_bytes(tail)


def rotate_logs(log_dir: Path) -> None:
    max_bytes = env_int("AICOS_DAEMON_LOG_MAX_BYTES", 5_000_000)
    keep_bytes = env_int("AICOS_DAEMON_LOG_KEEP_BYTES", 1_000_000)
    backups = max(1, env_int("AICOS_DAEMON_LOG_BACKUPS", 3))
    for name in [
        "mcp-daemon.out.log",
        "mcp-daemon.err.log",
        "https-proxy.out.log",
        "https-proxy.err.log",
    ]:
        trim_log(log_dir / name, max_bytes=max_bytes, backups=backups, keep_bytes=keep_bytes)


def main() -> int:
    default_status = Path.home() / "Library/Application Support/aicos/health-status.json"
    default_log_dir = Path.home() / "Library/Logs/aicos"
    default_env_file = REPO_ROOT / ".runtime-home/aicos-daemon.env"
    ap = argparse.ArgumentParser(description="AICOS local health monitor")
    ap.add_argument("--daemon-url", default=os.environ.get("AICOS_MCP_DAEMON_URL", "http://127.0.0.1:8000/mcp").replace("/mcp", "/health"))
    ap.add_argument("--status-file", default=str(default_status))
    ap.add_argument("--log-dir", default=str(default_log_dir))
    ap.add_argument("--env-file", default=os.environ.get("AICOS_DAEMON_ENV_FILE", str(default_env_file)))
    ap.add_argument("--failure-threshold", type=int, default=env_int("AICOS_DAEMON_MONITOR_FAILURE_THRESHOLD", 3))
    ap.add_argument("--alert-repeat-minutes", type=int, default=env_int("AICOS_DAEMON_MONITOR_ALERT_REPEAT_MINUTES", 30))
    args = ap.parse_args()

    status_file = Path(args.status_file).expanduser()
    log_dir = Path(args.log_dir).expanduser()
    env_file = Path(args.env_file).expanduser()
    load_env_file(env_file)
    token = os.environ.get("AICOS_DAEMON_TOKEN", "")

    rotate_logs(log_dir)

    state = load_state(status_file)
    ok, payload, error = check_health(args.daemon_url, token)
    failures = int(state.get("consecutive_failures", 0))
    was_alert_open = bool(state.get("alert_open", False))
    should_emit = False
    if ok:
        previous_failures = failures
        state = {
            "checked_at": now_iso(),
            "daemon_url": args.daemon_url,
            "status": "ok",
            "consecutive_failures": 0,
            "health": payload,
        }
        if was_alert_open and env_flag("AICOS_DAEMON_MONITOR_NOTIFY_RECOVERY", True):
            notify("AICOS Monitor", f"AICOS daemon recovered after {previous_failures} failed checks.")
            state["recovered_at"] = now_iso()
        should_emit = previous_failures > 0
    else:
        failures += 1
        previous_error = str(state.get("error", ""))
        previous_alert_at = str(state.get("last_alert_at", ""))
        state = {
            "checked_at": now_iso(),
            "daemon_url": args.daemon_url,
            "status": "error",
            "consecutive_failures": failures,
            "error": error,
        }
        should_alert = False
        if failures >= max(1, args.failure_threshold):
            if not was_alert_open:
                should_alert = True
            elif error != previous_error:
                should_alert = True
            elif env_flag("AICOS_DAEMON_MONITOR_REPEAT_ALERTS", False):
                try:
                    previous_alert = datetime.fromisoformat(previous_alert_at.replace("Z", "+00:00"))
                    minutes_since = (datetime.now(timezone.utc) - previous_alert).total_seconds() / 60
                    should_alert = minutes_since >= max(1, args.alert_repeat_minutes)
                except ValueError:
                    should_alert = True
        if should_alert:
            message = f"AICOS daemon health failed {failures} times: {error}"
            notify("AICOS Monitor", message)
            state["last_alert_at"] = now_iso()
            state["last_alert_error"] = error
            state["alert_open"] = True
            should_emit = True
        else:
            state["alert_open"] = was_alert_open
            should_emit = failures == 1 or error != previous_error
    save_state(status_file, state)
    if should_emit:
        print(json.dumps(state, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
