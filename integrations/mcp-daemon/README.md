# AICOS MCP HTTP Daemon

Optional team/LAN mode for serving the AICOS MCP surface over HTTP with:
- **In-memory TTL cache** — repeated agent startups served from RAM
- **PostgreSQL hybrid search** — `aicos_query_project_context` backed by
  pgvector embeddings when available, plus `tsvector`, authority boost, and
  freshness ranking
- **Markdown-direct fallback** — all tools work even without PostgreSQL

The daemon serves the same current read/write tools as the local stdio bridge,
including project registry, project health, feedback digest, and feedback write
surfaces.

## Quick start

```bash
# From repo root: creates .runtime-home venv/env file and attempts PG setup.
scripts/aicos-bootstrap-full --without-embeddings

# Or, if the human wants vector search and has a key ready:
scripts/aicos-bootstrap-full --with-embeddings

# Start daemon for same-machine access.
scripts/aicos-daemon-start

# LAN mode: require a token and bind intentionally
AICOS_DAEMON_HOST=0.0.0.0 scripts/aicos-daemon-start
```

For a fresh-agent install runbook, use
`docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`.
For compact write payload examples, use
`docs/install/AICOS_MCP_WRITE_COOKBOOK.md`.

The daemon refuses non-loopback binds without `AICOS_DAEMON_TOKEN` or `--token`.
Use `--allow-unauthenticated-lan` only on an isolated trusted network.

Daemon logs on startup whether PostgreSQL/embedding search is active or falling
back:
```
[INFO] PostgreSQL search engine active
[INFO] PG index ready: {'indexed': 87, 'skipped': 0, 'embedded': 87, 'embedding_errors': 0, 'errors': 0}
[INFO] Embedding search: enabled; pgvector active
[INFO] AICOS MCP daemon started
[INFO]   endpoint : http://127.0.0.1:8000/mcp
[INFO]   health   : http://127.0.0.1:8000/health
[INFO]   reindex  : GET http://127.0.0.1:8000/reindex
```

## Connect agents

```bash
# Same machine / Codex Desktop Streamable HTTP
# Name: aicos
# URL: http://127.0.0.1:8000/mcp
# Bearer token env var: blank for localhost no-auth mode

# LAN (replace IP with AICOS machine's IP; configure the client to send bearer token if supported)
claude mcp add --transport http aicos http://192.168.1.100:8000/mcp

# Remote via Tailscale
claude mcp add --transport http aicos http://100.x.x.x:8000/mcp
```

## Environment variables

| Variable       | Default                        | Description             |
|----------------|--------------------------------|-------------------------|
| `AICOS_PG_DSN` | `postgresql://localhost/aicos` | Full PG connection DSN  |
| `AICOS_PG_HOST`| `localhost`                    | PG host                 |
| `AICOS_PG_PORT`| `5432`                         | PG port                 |
| `AICOS_PG_DB`  | `aicos`                        | PG database name        |
| `AICOS_PG_USER`| *(os user)*                    | PG username             |
| `AICOS_PG_PASS`| *(empty)*                      | PG password             |
| `AICOS_DAEMON_TOKEN` | *(empty)* | Bearer/X-AICOS-Token required by daemon when set |
| `AICOS_DAEMON_EXTRA_TOKENS` | *(empty)* | Extra labeled tokens as `label:token,label2:token2` |
| `AICOS_DAEMON_ALLOWLIST` | *(empty)* | Optional comma-separated IP/CIDR allowlist for HTTP clients |
| `AICOS_DAEMON_INTERNAL_TOKEN_LABELS` | *(empty)* | Token labels allowed to write protected AICOS service scopes |
| `AICOS_DAEMON_TOKEN_SCOPE_POLICY` | *(empty)* | Optional JSON per-token read/write scope policy |
| `OPENAI_API_KEY` | *(empty)* | Enables default embedding index/query |
| `AICOS_EMBEDDINGS` | `auto` | `auto`/enabled by key, or `off` to disable embeddings |
| `AICOS_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `AICOS_EMBEDDING_DIMENSIONS` | `1536` | pgvector dimensions |

## CLI flags

```
--host        Bind address (default: 127.0.0.1; use 0.0.0.0 only for trusted LAN)
--port        Port (default: 8000)
--cache-ttl   Read-cache TTL seconds (default: 30, 0=disable)
--no-pg       Skip PostgreSQL, use markdown-direct search only
--token       Require this bearer/X-AICOS-Token for HTTP requests
--allow-unauthenticated-lan
             Allow non-loopback bind without auth; isolated trusted network only
--log-level   DEBUG|INFO|WARNING|ERROR (default: INFO)
```

## Health & reindex endpoints

```bash
curl http://localhost:8000/health
# {"status":"ok","search_engine":"postgresql_hybrid","cache_entries":14,...}

curl http://localhost:8000/reindex
# {"status":"reindex_started"}   ← runs full brain/ scan in background
```

For token-protected LAN mode:

```bash
curl -H "Authorization: Bearer <shared-secret>" http://192.168.1.100:8000/health
```

`/health` now also returns `auth_capabilities` so operators and thin clients can
see the supported auth model without guessing:

- labeled token names currently accepted by the daemon
- whether an IP/CIDR allowlist is active
- `oauth_supported: false`
- `query_token_supported: false`
- recommended client profiles for:
  - bearer-header HTTP clients
  - local Claude Desktop via HTTPS localhost proxy

Minimum LAN rollout:

1. Pick one AICOS machine and keep its repo checkout current.
2. Start the daemon with `AICOS_DAEMON_TOKEN` and `--host 0.0.0.0`.
3. Give agents the HTTP MCP URL and token through their MCP client config.
4. Run `./aicos mcp doctor --mode daemon --daemon-url http://<host>:8000 --token <shared-secret>`.
5. Treat `brain/` in that repo as the shared context/control-plane authority.

## Search engine architecture

```
aicos_query_project_context
        │
        ├─ PostgreSQL hybrid (default when daemon + PG are available)
        │    ├─ vector similarity via pgvector when OPENAI_API_KEY is set
        │    ├─ RRF fusion with FTS
        │    ├─ source refs + authority + freshness in every result
        │    └─ degrades to PostgreSQL FTS if embedding is unavailable
        │
        ├─ PostgreSQL FTS fallback (when pg available, embedding unavailable)
        │    ├─ intent detection (Vietnamese + English, zero latency)
        │    │    trạng thái → [current_state, handoff]
        │    │    quy tắc   → [canonical, policy, contract]
        │    ├─ websearch_to_tsquery('simple', query)
        │    │    'simple' config: lowercase only — works for Vietnamese
        │    ├─ ts_rank_cd with weights: title(A) > summary(B) > body(C)
        │    ├─ × authority_mult: canonical=2.0, handoff=1.5, evidence=0.5
        │    ├─ × freshness_mult: fresh=1.0, aging=0.85, stale=0.5
        │    └─ results include: kind, authority, freshness, mtime, ref
        │
        └─ Markdown-direct fallback (no pg / pg unavailable)
             current naive keyword search from mcp_read_serving.py
```

## PostgreSQL schema highlights

- `aicos_context_docs` — one row per indexed markdown file
- `search_vector tsvector` — auto-rebuilt by trigger on title/summary/body change
- optional `embedding vector(1536)` — enabled when pgvector extension exists
- `authority_mult REAL` — stored boost factor: canonical=2.0, working=1.0-1.8, evidence=0.5
- `freshness_label TEXT` — stable|fresh|aging|stale (recalculated on reindex)
- Full-text config: `'simple'` — no stemming, handles Vietnamese correctly

## Run as background service (macOS)

```xml
<!-- ~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>         <string>ai.aicos.mcp-daemon</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/path/to/aicos/integrations/mcp-daemon/aicos_mcp_daemon.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>AICOS_PG_DSN</key><string>postgresql://aicos:aicos@localhost/aicos</string>
  </dict>
  <key>RunAtLoad</key>   <true/>
  <key>KeepAlive</key>   <true/>
  <key>StandardErrorPath</key><string>/tmp/aicos-mcp-daemon.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist
```

For a manual portable LAN start, use:

```bash
integrations/mcp-daemon/start-lan.sh
```

It reads `.runtime-home/aicos-daemon.env`, requires `AICOS_DAEMON_TOKEN`, and
delegates to `scripts/aicos-daemon-start`.

For minimum local monitoring, run:

```bash
python3 integrations/mcp-daemon/aicos_health_monitor.py
```

It checks `/health`, writes a local status JSON, sends macOS notifications
after repeated failures, and trims oversized log files in `~/Library/Logs/aicos/`.

## Merge notes for Codex

When merging `feat/pg-search-engine` into `main`:

**New files (no conflicts):**
- `packages/aicos-kernel/aicos_kernel/pg_search/` — entire package
- `integrations/mcp-daemon/docker-compose.yml`

**Updated files:**
- `integrations/mcp-daemon/aicos_mcp_daemon.py` — complete rewrite with pg_search
  integrated. If `feat/mcp-daemon-http-cache` was merged first, use this version
  (superset — includes HTTP server + cache + pg_search).
- `integrations/mcp-daemon/README.md` — updated docs

**Dependency to add:**
```bash
pip install psycopg2-binary   # or psycopg2 for non-binary
```

**Embedding fallback rule:**
Embedding is the preferred daemon search enhancement when `OPENAI_API_KEY` and
pgvector are available. If either is missing, the daemon still starts and uses
PostgreSQL FTS. If PostgreSQL is unavailable, it falls back to markdown-direct
search.

## Embedding guardrails

AICOS currently keeps embedding broad, but with lightweight cost guardrails:

- default model is `text-embedding-3-small`
- daemon startup and write-triggered refresh index text first, then only embed
  documents that are new or stale
- background embedding refresh logs `docs_submitted`, `approx_input_chars`, and
  `approx_input_tokens` so operators can watch real usage before tightening
  budget controls

## Client tokens and audit logging

- `AICOS_DAEMON_TOKEN` remains the primary token
- `AICOS_DAEMON_EXTRA_TOKENS` can define labeled extra tokens as
  `label:token,label2:token2`
- daemon authorizes by token label as well as token validity:
  - authenticated tokens can read by default
  - external/A1 tokens cannot write protected service scopes such as
    `projects/aicos`
  - only access labels in `AICOS_DAEMON_INTERNAL_TOKEN_LABELS` can write
    protected service scopes by default
  - set `AICOS_DAEMON_TOKEN_SCOPE_POLICY` for explicit per-token scope rules
- daemon writes request audit events to `~/Library/Logs/aicos/mcp-audit.jsonl`
- each event includes token label, remote IP, tool name, actor identity fields,
  scope, work lane, status, error, and duration

Example explicit scope policy:

```bash
AICOS_DAEMON_TOKEN_SCOPE_POLICY='{"antigravity":{"read":["projects/sample-project"],"write":["projects/sample-project"]},"a2-core-c":{"read":["projects/*"],"write":["projects/*"]}}'
```

This is intentionally small. Product/client names such as Antigravity or
Claude Code are not AICOS actor roles; unless a token label is explicitly
internal or explicitly granted, it is treated as an external A1 service client
for protected write authorization. Do not use product families such as `codex`
or `claude-code` as implicit internal authority; use a role/access label such as
`a2-core-c` for AICOS-maintainer tokens.

## Audit CLI

Use the local CLI instead of opening raw JSONL by hand:

```bash
./aicos audit recent --limit 20
./aicos audit recent --token-label openclaw-vm --scope projects/sample-project
./aicos audit recent --agent-family openclaw --status tool_error
./aicos audit summary --limit 500
./aicos feedback summary --limit 20
```

`audit summary` is the quick operational view. It groups recent events by:

- status
- token label
- tool name
- scope
- repeated error text

Use it first when you need to answer "which client is failing?" or "which tool
is currently noisy?" before drilling into `audit recent`.

`feedback summary` is the companion operator view for explicit agent feedback.
Use it to see recurring tool gaps, bootstrap confusion, interop problems, or
write-schema friction reported back into AICOS.

Startup bundle and project health now include a small `feedback_loop` object so
clients can see when AICOS is explicitly asking for friction/tool-gap feedback
without adding a heavy push/survey subsystem.

## Auth profile notes

- The daemon itself supports bearer token auth, not OAuth.
- Query-string token auth is intentionally unsupported.
- Claude Desktop connector beta currently needs the same-machine HTTPS proxy
  because its custom connector UI does not expose a generic bearer-header field
  the same way Codex/OpenClaw-style clients do.
