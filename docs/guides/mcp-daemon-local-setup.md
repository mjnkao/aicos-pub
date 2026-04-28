# MCP Daemon Local Setup

Status: public staging guide

This guide covers the optional HTTP daemon for local or trusted-LAN use. It is
written as a public setup path and intentionally omits private machine state,
handoffs, and project-specific operations.

## What This Adds

The daemon exposes the same AICOS MCP surface as the local stdio bridge, but
over HTTP:

- local loopback access for desktop clients
- optional LAN access with bearer-token auth
- PostgreSQL-backed search when available
- markdown fallback when PostgreSQL is unavailable
- local health monitoring and log trimming on macOS

## Prerequisites

- `python3`
- either Docker or Homebrew if you want the helper to attempt PostgreSQL setup
- optional: an MCP client that supports HTTP or SSE transports

## Quick Start

From the repo root:

```bash
scripts/aicos-bootstrap-full --without-embeddings
scripts/aicos-daemon-start
```

The bootstrap helper creates:

- `.runtime-home/aicos-venv/`
- `.runtime-home/aicos-daemon.env`

It also attempts a local PostgreSQL + pgvector setup when Docker or Homebrew is
available. If that setup fails, the daemon still starts in markdown-fallback
mode.

## Environment File

If you prefer a committed template, start from:

```bash
cp integrations/mcp-daemon/aicos-daemon.env.example .runtime-home/aicos-daemon.env
```

The default public-safe shape is:

```bash
AICOS_DAEMON_HOST=127.0.0.1
AICOS_DAEMON_PORT=8000
AICOS_DAEMON_CACHE_TTL=30
AICOS_DAEMON_TOKEN=<set-a-strong-token>
AICOS_PG_DSN=postgresql://aicos:aicos@127.0.0.1:5432/aicos
AICOS_PG_CONNECT_TIMEOUT_SECONDS=5
AICOS_PG_STATEMENT_TIMEOUT_MS=15000
AICOS_PG_LOCK_TIMEOUT_MS=5000
AICOS_EMBEDDINGS=auto
OPENAI_API_KEY=
```

With `AICOS_EMBEDDINGS=auto`, embeddings remain disabled until you add
`OPENAI_API_KEY` and restart the daemon.

## Local Access

Start the daemon:

```bash
scripts/aicos-daemon-start
```

Verify:

```bash
curl http://127.0.0.1:8000/health
```

Loopback mode on `127.0.0.1` does not require a token by default. Set
`AICOS_REQUIRE_LOCAL_TOKEN=1` if you want token auth for local-only clients too.

## Trusted LAN Access

LAN mode should always use a token:

```bash
integrations/mcp-daemon/start-lan.sh
```

That helper:

- loads `.runtime-home/aicos-daemon.env`
- refuses to start if `AICOS_DAEMON_TOKEN` is empty
- binds to `0.0.0.0` by default
- prints the macOS VM bridge URL when `bridge100` is present

Example health check:

```bash
curl -H "Authorization: Bearer <token>" http://192.168.1.100:8000/health
```

## macOS Auto-Start

To install LaunchAgents plus a lightweight monitor:

```bash
scripts/aicos-install-launchagents
```

This installs:

- `~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist`
- `~/Library/LaunchAgents/ai.aicos.health-monitor.plist`
- `~/Library/LaunchAgents/ai.aicos.https-proxy.plist` when mkcert certs exist

Logs go to:

```text
~/Library/Logs/aicos/
```

Monitor status goes to:

```text
~/Library/Application Support/aicos/health-status.json
```

## Health Monitor

For a one-shot local run:

```bash
python3 integrations/mcp-daemon/aicos_health_monitor.py
```

The monitor checks the daemon `/health` endpoint, writes a compact status JSON,
sends a macOS notification after repeated failures, and trims oversized
daemon/proxy logs.

## Verification

Run:

```bash
./aicos --help
python3 -m py_compile integrations/mcp-daemon/aicos_health_monitor.py
python3 -m py_compile integrations/mcp-daemon/aicos_mcp_daemon.py
```

If PostgreSQL is available, also verify:

```bash
curl http://127.0.0.1:8000/reindex
```

## Privacy Boundary

Do not export:

- real tokens or `.env` files
- local log files
- handoffs, checkpoints, or evidence
- machine-specific paths beyond generic examples
