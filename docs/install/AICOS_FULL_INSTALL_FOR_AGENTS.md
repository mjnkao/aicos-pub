# AICOS Full Local Install Guide For Agents

Status: authoritative fresh-machine install runbook  
Last updated: 2026-04-23

This guide is the front door for a fresh agent that receives only the AICOS
GitHub repository link and a human request to install AICOS on a target machine.

If you need the shortest path first, start with:

```text
docs/install/AICOS_AGENT_INSTALL_QUICKSTART.md
```

Goal: install AICOS so the HTTP MCP daemon serves all tools, Claude Desktop uses
stdio transport, Claude Code uses HTTP-first with stdio fallback, the daemon
auto-starts on macOS login, and LAN agents can connect via HTTP.

Client defaults in this guide:

- `Claude Desktop`
  - local stdio by default
- `Claude Code`
  - local HTTP-first wrapper with stdio fallback
- `Codex Desktop`
  - direct HTTP / Streamable HTTP
- `Antigravity / Gemini IDE`
  - local stdio, or LAN/VM HTTP-SSE with `serverUrl` + `headers`

For a VM agent that only needs to connect to an already-running host daemon,
use:

```text
docs/install/AICOS_VM_AGENT_HTTP_MCP_CONNECT.md
```

For compact write payload examples and a template helper, use:

```text
docs/install/AICOS_MCP_WRITE_COOKBOOK.md
```

For query/search operating guidance after install, use:

```text
docs/install/AICOS_QUERY_SEARCH_GUIDE.md
```

## Current System Architecture

```
┌─────────────────────────────────────────────────┐
│ AICOS Machine (macOS)                           │
│                                                 │
│  Postgres.app (port 5432)   ← Start at Login   │
│    └─ DB: aicos  user: aicos  pgvector          │
│                                                 │
│  LaunchAgent: ai.aicos.mcp-daemon               │
│    └─ scripts/aicos-daemon-start.sh             │
│         └─ aicos_mcp_daemon.py (port 8000)      │
│              ├─ PG hybrid / FTS search          │
│              ├─ 30s TTL in-memory cache         │
│              └─ markdown fallback if PG down    │
│                                                 │
│  LaunchAgent: ai.aicos.https-proxy  [opt]       │
│    └─ aicos_https_proxy.py (port 8443)          │
│         └─ mkcert TLS → forwards to :8000       │
│                                                 │
│  Claude Desktop                                 │
│    └─ stdio → aicos_mcp_stdio.py               │
│                                                 │
│  Claude Code CLI                                │
│    └─ HTTP-first → aicos_mcp_http_first.py      │
│         ├─ tries http://127.0.0.1:8000/mcp      │
│         └─ fallback: aicos_mcp_stdio.py         │
└─────────────────────────────────────────────────┘
              │ port 8000 (HTTP, LAN)
              │ port 8443 (HTTPS, optional)
┌─────────────┴──────────────────────────┐
│ LAN Agents / Other Machines            │
│  claude mcp add --transport http aicos │
│  http://<AICOS_IP>:8000/mcp            │
└────────────────────────────────────────┘
```

The daemon supports both JSON-RPC POST and a minimal MCP SSE flow on `/mcp`.
Use stdio when a client cannot pass bearer headers or cannot connect to local
HTTP services.

## 0. Ask The Human First

Before installing, ask these questions in one message:

1. Target install path: default suggestion `~/aicos`.
2. macOS account type: standard user (no admin/sudo) or admin.
3. Access mode: local only, or trusted LAN with daemon token.
4. Embedding/vector search: yes or no (requires `OPENAI_API_KEY`).
5. PostgreSQL method: Postgres.app (recommended, no admin), Docker, Homebrew,
   or existing DSN.

If the human chooses embeddings, ask for `OPENAI_API_KEY` before starting the
install. If the human has no key, choose the no-embedding path: PostgreSQL FTS
and markdown fallback still work.

## 1. Clone And Orient

```bash
git clone <AICOS_GITHUB_REPO_URL> ~/aicos
cd ~/aicos
sed -n '1,220p' AGENTS.md
sed -n '1,220p' README.md
sed -n '1,260p' docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md
```

Do not bulk-load old backup/history. For install work, this guide plus the MCP
daemon/local bridge READMEs are enough.

## 2. Bootstrap Runtime

No embeddings:

```bash
scripts/aicos-bootstrap-full --without-embeddings
```

With embeddings:

```bash
scripts/aicos-bootstrap-full --with-embeddings
```

The script creates `.runtime-home/aicos-venv/`,
`.runtime-home/aicos-daemon.env`, a daemon token, and installs
`psycopg2-binary` into the local venv.

Embedding mode is controlled by `.runtime-home/aicos-daemon.env`:

```bash
AICOS_EMBEDDINGS=auto
OPENAI_API_KEY=
AICOS_EMBEDDING_MODEL=text-embedding-3-small
AICOS_EMBEDDING_DIMENSIONS=1536
AICOS_EMBEDDING_BATCH_SIZE=32
AICOS_PG_CONNECT_TIMEOUT_SECONDS=5
AICOS_PG_STATEMENT_TIMEOUT_MS=15000
AICOS_PG_LOCK_TIMEOUT_MS=5000
```

With `AICOS_EMBEDDINGS=auto`, embeddings stay disabled until
`OPENAI_API_KEY` is filled. After adding or changing the key, restart the
daemon and run `./aicos brain status` to check vector coverage. PG timeout
settings keep daemon startup from blocking forever on a bad network, stale DB,
or schema lock.

It also attempts PostgreSQL/pgvector setup through Docker or Homebrew. If a
system install is blocked by permissions, stop and ask the human to run the
blocked command. Do not silently call the install complete.

## 3. PostgreSQL Setup Details

### Option A: Postgres.app (macOS — no admin, pgvector 0.8.1 bundled) ✅ Recommended

This is the recommended path on macOS standard accounts. No sudo needed.

1. Download from **https://postgresapp.com** (free, native app).
2. Move to `/Applications/`.
3. Open the app → click **Initialize**.
4. Open **Server Settings** → enable **"Start at Login"** (important for auto-start).

Add binaries to your shell config (`~/.zshrc` or `~/.bash_profile`):

```bash
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
```

Create the AICOS database, user, and extension:

```bash
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"

# Create role and database
psql -c "CREATE ROLE aicos WITH LOGIN PASSWORD 'aicos';"
psql -c "CREATE DATABASE aicos OWNER aicos;"

# Enable pgvector
psql -d aicos -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Verify
psql -U aicos -d aicos -c "SELECT extname, extversion FROM pg_extension WHERE extname='vector';"
# Expected: vector | 0.8.1 (or similar)
```

After bootstrap, set the DSN in `.runtime-home/aicos-daemon.env`:

```bash
AICOS_PG_DSN=postgresql://aicos:aicos@127.0.0.1:5432/aicos
```

### Option B: Docker

```bash
cd integrations/mcp-daemon
docker compose up -d
cd ../..
```

Default DSN: `postgresql://aicos:aicos@127.0.0.1:5432/aicos`

### Option C: Homebrew (macOS, requires admin-owned Homebrew)

```bash
brew install postgresql@18 pgvector
brew services start postgresql@18
/opt/homebrew/opt/postgresql@18/bin/createdb aicos 2>/dev/null || true
psql -d aicos -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

> If `/opt/homebrew` is owned by another user (common on shared Macs), this
> will fail. Use Option A instead.

### Option D: Existing PostgreSQL DSN

```bash
mkdir -p .runtime-home
cat >> .runtime-home/aicos-daemon.env <<'EOF'
AICOS_PG_DSN=postgresql://USER:PASSWORD@HOST:5432/aicos
EOF
```

If embeddings are enabled, the database must have the `vector` extension.
AICOS applies `CREATE EXTENSION IF NOT EXISTS vector` at daemon startup.

### Linux

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
# Install pgvector from https://github.com/pgvector/pgvector
# Then: sudo -u postgres createdb aicos
```

## 4. Start The Daemon

```bash
scripts/aicos-daemon-start
```

This script reads `.runtime-home/aicos-daemon.env`, starts the venv Python,
and binds to `127.0.0.1:8000` by default.

Local loopback mode does not require a token by default so desktop clients can
connect without bearer-env wiring. Set `AICOS_REQUIRE_LOCAL_TOKEN=1` if you want
token auth even on `127.0.0.1`.

Trusted LAN mode (exposes to other machines on the LAN):

```bash
AICOS_DAEMON_HOST=0.0.0.0 scripts/aicos-daemon-start
```

LAN mode requires `AICOS_DAEMON_TOKEN`; the bootstrap script writes one to
`.runtime-home/aicos-daemon.env`. The daemon refuses non-loopback binds
without a token (unless `--allow-unauthenticated-lan` is passed explicitly).

## 5. Verify

In another shell:

```bash
TOKEN="$(awk -F= '/^AICOS_DAEMON_TOKEN=/{print $2}' .runtime-home/aicos-daemon.env)"
./aicos mcp doctor --mode daemon --daemon-url http://127.0.0.1:8000 --token "$TOKEN"
./aicos brain status
```

Expected full result:

- `postgresql_hybrid`: PG + pgvector + embedding key work.
- `postgresql_fts`: PG works, embeddings are disabled or unavailable.
- `markdown_direct`: fallback only; PostgreSQL is unavailable.

## 6. Configure Clients

### 6a. Claude Desktop (stdio)

Claude Desktop uses **stdio transport** — it spawns `aicos_mcp_stdio.py` as a
local subprocess. This works without the HTTP daemon.

Edit (create if needed):  
`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/aicos/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ]
    }
  },
  "preferences": {
    "bypassPermissionsModeEnabled": true
  }
}
```

Replace `/Users/YOUR_USERNAME/aicos` with your actual repo path (`echo ~/aicos`).

> ⚠️ **Critical**: JSON does not allow duplicate keys. Having two separate
> `"mcpServers"` blocks in the file causes the first to be silently ignored.
> Merge all MCP servers into a single `"mcpServers"` object.

Restart Claude Desktop (⌘Q → reopen). The `aicos_*` tools should appear in
the tools list.

### Claude Desktop HTTP connector (special-case only)

Claude Desktop does not follow the same direct bearer-header flow as Codex or
Claude Code. The supported path on the same machine is the localhost HTTPS
adapter in front of the daemon. Use stdio by default unless that adapter path
has been configured intentionally.

### 6b. Claude Code CLI (HTTP-first with fallback)

Claude Code supports HTTP transport natively. The HTTP-first wrapper tries
the daemon first and falls back to stdio if the daemon is down.

```bash
# HTTP-first (recommended — uses daemon if up, stdio if not)
claude mcp add aicos \
  python3 ~/aicos/integrations/local-mcp-bridge/aicos_mcp_http_first.py \
  -s user

# Verify
claude mcp list
# aicos: python3 .../aicos_mcp_http_first.py - ✓ Connected
```

Alternative — pure HTTP transport (daemon must always be running):

```bash
claude mcp add --transport http aicos http://127.0.0.1:8000/mcp -s user
```

Alternative — stdio only (no HTTP):

```bash
claude mcp add aicos \
  python3 ~/aicos/integrations/local-mcp-bridge/aicos_mcp_stdio.py \
  -s user
```

### 6c. Codex Desktop

Codex Desktop supports native Streamable HTTP MCP. For local testing, use the
daemon directly:

```text
Name: aicos
Transport: Streamable HTTP
URL: http://127.0.0.1:8000/mcp
Bearer token env var: leave blank for localhost no-auth mode
Headers: none
```

For token-protected LAN mode, set:

```text
Bearer token env var: AICOS_DAEMON_TOKEN
```

The Codex app process must actually have `AICOS_DAEMON_TOKEN` in its
environment, or use a direct `Authorization: Bearer <token>` header if the UI
allows storing a header value.

For stdio-only clients, use the HTTP-first proxy:

```toml
[mcp_servers.aicos]
command = "python3"
args = ["/ABS/PATH/TO/aicos/integrations/local-mcp-bridge/aicos_mcp_http_first.py"]
cwd = "/ABS/PATH/TO/aicos"
default_tools_approval_mode = "approve"
```

The proxy:

1. Sends JSON-RPC to `AICOS_MCP_DAEMON_URL` from
   `.runtime-home/aicos-daemon.env`, defaulting to
   `http://127.0.0.1:8000/mcp`.
2. Uses `AICOS_DAEMON_TOKEN` when present.
3. Falls back to `integrations/local-mcp-bridge/aicos_mcp_stdio.py` if HTTP is
   unavailable.

After changing Codex MCP config, restart or refresh Codex tools.

### 6d. Antigravity / Gemini IDE

On the same machine as the AICOS checkout, prefer local stdio config.

On VM/LAN setups, use the Antigravity-specific HTTP/SSE raw config shape:

```json
{
  "mcpServers": {
    "aicos": {
      "serverUrl": "http://<AICOS_LAN_IP>:8000/mcp",
      "headers": {
        "Authorization": "Bearer <AICOS_DAEMON_TOKEN>"
      }
    }
  }
}
```

Do not use:

- `url`
- `transport`
- `?token=...`

If Antigravity loads the connector but no tools appear, verify:

1. `serverUrl` is present
2. `headers.Authorization` includes the `Bearer ` prefix
3. `curl -H "Authorization: Bearer <token>" http://<AICOS_LAN_IP>:8000/health`
   returns `status: ok`
4. the Antigravity MCP runtime was restarted

## 7. Configure Other Agents (LAN)

Agents with native HTTP MCP support (e.g. Claude Code on another machine):

```bash
# Find the AICOS machine's LAN IP first:
# macOS: ipconfig getifaddr en0
# Linux: hostname -I

claude mcp add --transport http aicos http://<AICOS_LAN_IP>:8000/mcp -s user
```

With a token (required when `AICOS_DAEMON_TOKEN` is set):

```bash
curl -H "Authorization: Bearer <token>" http://<AICOS_LAN_IP>:8000/health
```

## Read identity requirements

Read calls now require minimum identity fields so audit logs can attribute
traffic to the correct agent and lane.

Required on every read:

```text
agent_family
agent_instance_id
work_type
work_lane
execution_context
```

For first-contact/bootstrap reads, when the agent has not yet identified the
real work lane, use:

```text
work_type=orientation
work_lane=intake
```

Required when `work_type=code`:

```text
worktree_path
```

Recommended when `work_type=code`:

```text
work_branch
```

If a read is rejected with `missing_read_identity`, the daemon response now
includes:

- `missing`
- `field_help`
- `example`

so the agent can repair the payload without guessing.

## Audit inspection

Operators can inspect recent MCP traffic without opening raw JSONL manually:

```bash
./aicos audit recent --limit 20
./aicos audit recent --token-label openclaw-vm
./aicos audit recent --scope projects/sample-project --status tool_error
./aicos audit summary --limit 500
./aicos feedback summary --limit 20
```

Use `audit summary` first when you need a quick answer to:

- which token/client is generating errors
- which MCP tool is noisy
- whether failures are concentrated in one project scope

Use `feedback summary` when you want the operator/A2 view of what agents are
explicitly reporting as friction, tool gaps, or schema confusion.

Startup bundle and project health now also include a `feedback_loop` hint. This
is a lightweight prompt from AICOS telling the agent when it is a good moment
to record friction or a tool-gap note through `aicos_record_feedback`.

Session-close writes now require one feedback closure per
`scope + agent_family + agent_instance_id + work_lane`. That closure can be a
real issue or `feedback_type=no_issue`; agents should not invent fake problems
just to pass the boundary.

This reads `~/Library/Logs/aicos/mcp-audit.jsonl` and supports filters for
token label, agent family, agent instance, scope, work lane, status, and error
substring.

Agents without HTTP MCP support:

```bash
python3 /ABS/PATH/TO/aicos/integrations/local-mcp-bridge/aicos_mcp_http_first.py
```

On the AICOS machine, restart the daemon with `0.0.0.0` to allow LAN
connections (set in `.runtime-home/aicos-daemon.env`):

```bash
AICOS_DAEMON_HOST=0.0.0.0
AICOS_DAEMON_TOKEN=<same-token-you-share-with-clients>
```

For team use, treat token labels as access-control subjects, not just names.
By default AICOS allows authenticated tokens to read, but blocks external/A1
tokens from writing protected service scopes such as `projects/aicos`.

Use `AICOS_DAEMON_INTERNAL_TOKEN_LABELS` only for AICOS-maintainer tokens, for
example:

```bash
AICOS_DAEMON_INTERNAL_TOKEN_LABELS=a2-core-c
```

Do not use product/client families such as `codex`, `claude-code`,
`antigravity`, or `openclaw` as implicit internal authority. Those belong in
`agent_family`. Use dedicated access labels such as `a2-core-c` for protected
AICOS-maintainer write authority.

Use `AICOS_DAEMON_TOKEN_SCOPE_POLICY` when a company/team needs explicit
per-token read/write scope grants:

```bash
AICOS_DAEMON_TOKEN_SCOPE_POLICY='{"antigravity":{"read":["projects/sample-project"],"write":["projects/sample-project"]},"a2-core-c":{"read":["projects/*"],"write":["projects/*"]}}'
```

Use the token helper for new agents instead of editing env and registry files
by hand:

```bash
# New external A1/client token.
./aicos mcp token create <label> --assigned-to "<agent or machine>"

# New AICOS maintainer access token.
./aicos mcp token create <access-label> --internal --assigned-to "AICOS maintainer"

# Review labels and rights. Use --show-tokens only when you need the secret.
./aicos mcp token list

# Activate changes.
launchctl kickstart -k gui/$(id -u)/ai.aicos.mcp-daemon
```

Portable LAN helper:

```bash
integrations/mcp-daemon/start-lan.sh
```

This helper loads `.runtime-home/aicos-daemon.env`, forces LAN bind mode only
when `AICOS_DAEMON_TOKEN` is present, and then delegates to
`scripts/aicos-daemon-start`.

On this machine class, if a VM network bridge exists (`bridge100` on macOS
Virtualization), the helper also prints the host bridge URL that VM guests can
use directly, for example `http://192.168.64.1:8000/mcp`.

## 8. macOS Auto-Start (LaunchAgents)

LaunchAgents make the daemon start automatically at login without admin access.
Skip this section if you prefer to start the daemon manually.

Recommended install:

```bash
scripts/aicos-install-launchagents
```

This writes and loads:

- `~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist`
- `~/Library/LaunchAgents/ai.aicos.health-monitor.plist`
- `~/Library/LaunchAgents/ai.aicos.https-proxy.plist` when mkcert cert/key exist

Persistent logs go to `~/Library/Logs/aicos/`.
Monitor status goes to `~/Library/Application Support/aicos/health-status.json`.

### 8a — PG-Wait Startup Wrapper

Postgres.app starts slightly after LaunchAgents on login (race condition). The
wrapper script waits up to 60 s for PostgreSQL before starting the daemon.

The script is at `scripts/aicos-daemon-start.sh` (tracked in repo). It uses
dynamic `REPO_ROOT` resolved from its own path. No edits needed unless your
PostgreSQL DSN is different.

Key variables you may need to adjust in the script:
- `AICOS_PG_DSN` — PostgreSQL connection string
- `PATH` — Add your PG binary path if not Postgres.app

Make it executable:

```bash
chmod +x ~/aicos/scripts/aicos-daemon-start.sh
```

### 8b — Daemon Plist

Manual alternative: create
`~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.aicos.mcp-daemon</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/YOUR_USERNAME/aicos/scripts/aicos-daemon-start.sh</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>AICOS_PG_DSN</key>
    <string>postgresql://aicos:aicos@127.0.0.1:5432/aicos</string>
    <key>PATH</key>
    <string>/Applications/Postgres.app/Contents/Versions/latest/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>10</integer>

  <key>StandardOutPath</key>
  <string>/Users/YOUR_USERNAME/Library/Logs/aicos/mcp-daemon.out.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/YOUR_USERNAME/Library/Logs/aicos/mcp-daemon.err.log</string>
</dict>
</plist>
```

Replace `YOUR_USERNAME` with your macOS username (`echo $USER`).

Load the LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist
```

Verify:

```bash
launchctl list | grep aicos
# Should show at least:
# -  0  ai.aicos.mcp-daemon
# -  0  ai.aicos.health-monitor
tail -20 ~/Library/Logs/aicos/mcp-daemon.err.log
cat ~/Library/Application\ Support/aicos/health-status.json
curl http://127.0.0.1:8000/health
```

To reload after editing:

```bash
launchctl unload ~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist
launchctl unload ~/Library/LaunchAgents/ai.aicos.health-monitor.plist
# Kill any leftover process holding the port:
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/ai.aicos.mcp-daemon.plist
launchctl load ~/Library/LaunchAgents/ai.aicos.health-monitor.plist
```

### 8c — Optional: HTTPS Proxy Plist (for HTTPS access on LAN)

Needed for Claude Desktop on the same machine, because the current custom
connector UI does not expose generic bearer-header configuration in the same
way Codex/OpenClaw-style clients do.

**Install mkcert first** (generates locally-trusted certs, no admin needed):

```bash
brew install mkcert
mkcert -install   # Adds root CA to login keychain
# Generate cert for your machine (replace 192.168.X.X with your LAN IP)
mkcert localhost 127.0.0.1 192.168.1.X
mkdir -p ~/.local/share/mkcert
mv localhost+2.pem localhost+2-key.pem ~/.local/share/mkcert/
```

Create `~/Library/LaunchAgents/ai.aicos.https-proxy.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.aicos.https-proxy</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/YOUR_USERNAME/aicos/integrations/mcp-daemon/aicos_https_proxy.py</string>
    <string>--host</string>
    <string>0.0.0.0</string>
    <string>--https-port</string>
    <string>8443</string>
    <string>--daemon-url</string>
    <string>http://127.0.0.1:8000</string>
  </array>

  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>10</integer>

  <key>StandardOutPath</key>
  <string>/tmp/aicos-https-proxy.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/aicos-https-proxy.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/ai.aicos.https-proxy.plist
# Test:
curl https://localhost:8443/health
```

The daemon `/health` payload now includes `auth_capabilities`, which makes the
supported auth model explicit:

- bearer token auth is supported
- OAuth is not supported by the daemon
- query-string token auth is not supported
- the localhost HTTPS proxy is the supported Claude Desktop path on the same
  machine

### 8d - Monitoring and log trimming

`ai.aicos.health-monitor` runs every 60 seconds. It:

- checks daemon health
- writes current status to `~/Library/Application Support/aicos/health-status.json`
- sends a macOS notification after repeated failures
- trims oversized daemon/proxy log files in `~/Library/Logs/aicos/`

## 9. First Context Read

After MCP is connected, call:

```text
aicos_get_startup_bundle(actor=<role>, scope=projects/<project-id>)
aicos_get_status_items(actor=<role>, scope=projects/<project-id>)
aicos_query_project_context(actor=<role>, scope=projects/<project-id>, query="<task/context question>")
```

For AICOS self-work:

```text
actor=A2-Core-C
scope=projects/aicos
```

For A1 project work:

```text
actor=A1
scope=projects/<project-id>
```

## 10. Troubleshooting

### Port already in use

```bash
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8443 | xargs kill -9 2>/dev/null || true
```

Then reload the LaunchAgent.

### Daemon starts but search is `markdown_direct`

- PostgreSQL is not running, `AICOS_PG_DSN` is wrong, or Python PG driver is
  missing.
- Check: `pg_isready -h 127.0.0.1 -p 5432 -U aicos`
- Check: `psql -U aicos -d aicos -c "SELECT 1;"` works.

### Daemon search is `postgresql_fts` but not hybrid

- Embeddings are disabled, `OPENAI_API_KEY` is missing, or pgvector is not
  available.
- This is acceptable if the human chose no embeddings.

### MCP tools not appearing in Claude Desktop

1. Quit Claude Desktop fully (⌘Q).
2. Open `~/Library/Application Support/Claude/claude_desktop_config.json`.
3. Ensure there is exactly **one** `"mcpServers"` key — having two causes the
   first to be silently ignored.
4. Verify the path to `aicos_mcp_stdio.py` is absolute and correct.
5. Reopen Claude Desktop.

### Agent only sees old tools/schema

- Restart/refresh the MCP client.
- Check it is using `aicos_mcp_http_first.py` or the current daemon URL.
- Run `claude mcp remove aicos && claude mcp add aicos ...` to reset.

### `aicos_update_status_item` missing from tool list

- Client has cached a stale tool schema. Restart/re-enable the MCP server.
- Or: `claude mcp remove aicos && claude mcp add aicos ...`

### Write fails with `mcp_contract_ack_required`

Every MCP write must include:
```json
"mcp_contract_ack": "mcp-v0.6-write-contract-ack"
```

### PostgreSQL times out on LaunchAgent startup

Postgres.app may not have started yet. The `scripts/aicos-daemon-start.sh`
wrapper waits up to 60 s for `pg_isready`. Check Postgres.app is set to
"Start at Login" in its Server Settings.

### System install is blocked (Homebrew/admin)

- Ask the human to run the blocked command, then continue.
- Do not edit AICOS truth to pretend the install is complete.
- Recommend Postgres.app (Option A) as the no-admin alternative.
