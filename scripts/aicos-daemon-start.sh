#!/bin/bash
# AICOS MCP Daemon startup wrapper (LaunchAgent entrypoint)
# Waits for PostgreSQL (Postgres.app) before starting daemon — avoids race
# condition at login where LaunchAgents fire before Postgres.app is ready.
#
# Uses dynamic REPO_ROOT resolved from this script's location.
# Adjust AICOS_PG_DSN below if your PostgreSQL credentials differ.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${AICOS_DAEMON_ENV_FILE:-$REPO_ROOT/.runtime-home/aicos-daemon.env}"
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:/usr/bin:/bin:/usr/sbin:/sbin"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi
export AICOS_PG_DSN="${AICOS_PG_DSN:-postgresql://aicos:aicos@127.0.0.1:5432/aicos}"

DAEMON_SCRIPT="$REPO_ROOT/integrations/mcp-daemon/aicos_mcp_daemon.py"
MAX_WAIT=60  # Wait up to 60 s for PostgreSQL

echo "[aicos-start] Waiting for PostgreSQL..."
for i in $(seq 1 $MAX_WAIT); do
    if pg_isready -h 127.0.0.1 -p 5432 -U aicos -q 2>/dev/null; then
        echo "[aicos-start] PostgreSQL ready after ${i}s"
        break
    fi
    sleep 1
done

if ! pg_isready -h 127.0.0.1 -p 5432 -U aicos -q 2>/dev/null; then
    echo "[aicos-start] WARNING: PostgreSQL not ready after ${MAX_WAIT}s — starting daemon in fallback mode"
fi

PYTHON_BIN="${AICOS_PYTHON:-$REPO_ROOT/.runtime-home/aicos-venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="/usr/bin/python3"
fi

HOST="${AICOS_DAEMON_HOST:-127.0.0.1}"
PORT="${AICOS_DAEMON_PORT:-8000}"
CACHE_TTL="${AICOS_DAEMON_CACHE_TTL:-30}"
TOKEN="${AICOS_DAEMON_TOKEN:-}"

if [[ "$HOST" == "127.0.0.1" || "$HOST" == "localhost" || "$HOST" == "::1" ]]; then
    if [[ "${AICOS_REQUIRE_LOCAL_TOKEN:-0}" != "1" ]]; then
        TOKEN=""
    fi
fi

echo "[aicos-start] Starting AICOS MCP daemon..."
exec "$PYTHON_BIN" "$DAEMON_SCRIPT" --host "$HOST" --port "$PORT" --cache-ttl "$CACHE_TTL" --token "$TOKEN"
