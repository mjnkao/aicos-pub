#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
env_file="${AICOS_DAEMON_ENV_FILE:-$repo_root/.runtime-home/aicos-daemon.env}"

if [[ -f "$env_file" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a
fi

bridge_vm_ip="$(ifconfig bridge100 2>/dev/null | awk '/inet /{print $2; exit}')"
export AICOS_DAEMON_HOST="${AICOS_DAEMON_HOST:-0.0.0.0}"
export AICOS_DAEMON_PORT="${AICOS_DAEMON_PORT:-8000}"
export AICOS_DAEMON_CACHE_TTL="${AICOS_DAEMON_CACHE_TTL:-30}"

if [[ -z "${AICOS_DAEMON_TOKEN:-}" ]]; then
  echo "AICOS_DAEMON_TOKEN is required for LAN mode." >&2
  echo "Set it in $env_file or export it before running this script." >&2
  exit 2
fi

echo "Starting AICOS LAN daemon"
echo "- bind host: ${AICOS_DAEMON_HOST}"
echo "- port: ${AICOS_DAEMON_PORT}"
if [[ -n "$bridge_vm_ip" ]]; then
  echo "- VM bridge URL: http://${bridge_vm_ip}:${AICOS_DAEMON_PORT}/mcp"
fi

exec "$repo_root/scripts/aicos-daemon-start" "$@"
