# AICOS Agent Install Quickstart

Status: public install front door for new agents.

Use this guide when you are a fresh agent or human operator and need AICOS
running without reading every setup document first.

This guide covers three paths:

- Local solo: run AICOS from one checkout on one machine.
- Trusted LAN: expose the local daemon to nearby agents on the same trusted
  network.
- Railway small-team: deploy AICOS as a hosted HTTP MCP server.

For detailed local client setup, use
`docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`.

For the full Railway runbook, use
`docs/install/AICOS_PUB_RAILWAY_SETUP_RUNBOOK.md`.

## 0. Choose The Path

| Goal | Use this path | Required services |
|---|---|---|
| One agent/human on one machine | Local solo | Python 3; optional PostgreSQL/pgvector; optional OpenAI key |
| Several agents on the same trusted network | Trusted LAN | Local solo plus daemon token and reachable host IP |
| Hosted small-team MCP server | Railway small-team | Railway CLI/account, Railway PostgreSQL, OpenAI key for hybrid embeddings |

Recommended default for a new evaluator:

1. Start with local solo without embeddings.
2. Add PostgreSQL/pgvector.
3. Add embeddings if an OpenAI key is available.
4. Move to LAN or Railway only after local smoke tests pass.

## 1. Common Prerequisites

Install or verify:

```bash
git --version
python3 --version
python3 -m venv --help
curl --version
```

Expected:

- Python 3.10+ is recommended.
- `python3 -m venv --help` must work. If it fails on Linux, install the
  distribution package that provides `venv`, often `python3-venv`.
- `curl` is used for health and MCP smoke tests.

Clone:

```bash
git clone <AICOS_GITHUB_REPO_URL> ~/aicos
cd ~/aicos
./aicos --help
```

If `./aicos --help` fails:

- confirm you are in the repo root;
- run `python3 packages/aicos-kernel/aicos_kernel/kernel.py --help` to see if
  Python itself can execute the CLI;
- check executable bit with `ls -l aicos scripts/aicos`.

## 2. Local Solo Install

### 2.1 Bootstrap Without Embeddings

This is the lowest-friction path. It gives you MCP tools and markdown fallback
even if PostgreSQL is not ready.

```bash
scripts/aicos-bootstrap-full --without-embeddings
```

The script creates:

```text
.runtime-home/aicos-venv/
.runtime-home/aicos-daemon.env
```

It also tries to start PostgreSQL/pgvector if Docker or Homebrew is available.
If that part fails, do not panic. AICOS can still run in `markdown_direct`
fallback while you fix PostgreSQL.

### 2.2 Start The Daemon

```bash
scripts/aicos-daemon-start
```

Keep this terminal open. In another terminal:

```bash
cd ~/aicos
curl -fsS http://127.0.0.1:8000/health | python3 -m json.tool
```

Expected minimum:

```text
"status": "ok"
"search_engine": "markdown_direct" OR "postgresql_fts" OR "postgresql_hybrid"
```

Meaning:

- `markdown_direct`: AICOS is usable, PostgreSQL is not active.
- `postgresql_fts`: PostgreSQL search is active, embeddings are not active.
- `postgresql_hybrid`: PostgreSQL + pgvector embeddings are active.

### 2.3 Run MCP Doctor

```bash
TOKEN="$(awk -F= '/^AICOS_DAEMON_TOKEN=/{print $2}' .runtime-home/aicos-daemon.env)"
./aicos mcp doctor --mode daemon --daemon-url http://127.0.0.1:8000 --token "$TOKEN"
./aicos brain status
```

If doctor reports auth failure on local loopback, verify whether
`AICOS_REQUIRE_LOCAL_TOKEN=1` is set. Local loopback normally runs without a
required token unless that env var is enabled.

## 3. PostgreSQL / pgvector Options

AICOS works without PostgreSQL, but PostgreSQL improves search. pgvector plus
embeddings enables `postgresql_hybrid`.

### Option A: Docker

Use this when Docker is available and you do not want to install PostgreSQL on
the host:

```bash
cd ~/aicos/integrations/mcp-daemon
docker compose up -d
cd ~/aicos
```

Expected DSN:

```text
postgresql://aicos:aicos@127.0.0.1:5432/aicos
```

### Option B: Postgres.app On macOS

Use this when Docker is unavailable or you do not have admin access.

1. Install Postgres.app from `https://postgresapp.com`.
2. Open Postgres.app and initialize the server.
3. Enable "Start at Login".
4. Add binaries to the current shell:

```bash
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
```

Create database and extension:

```bash
psql -c "CREATE ROLE aicos WITH LOGIN PASSWORD 'aicos';" 2>/dev/null || true
psql -c "CREATE DATABASE aicos OWNER aicos;" 2>/dev/null || true
psql -d aicos -c "CREATE EXTENSION IF NOT EXISTS vector;"
psql -U aicos -d aicos -c "SELECT extname, extversion FROM pg_extension WHERE extname='vector';"
```

Set or confirm in `.runtime-home/aicos-daemon.env`:

```env
AICOS_PG_DSN=postgresql://aicos:aicos@127.0.0.1:5432/aicos
```

Restart the daemon and recheck `/health`.

### Option C: Existing PostgreSQL

Add a DSN to `.runtime-home/aicos-daemon.env`:

```env
AICOS_PG_DSN=postgresql://USER:PASSWORD@HOST:5432/aicos
```

The database user needs permission to create tables and run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

If pgvector is unavailable, AICOS should still run as `postgresql_fts`.

## 4. Optional Embeddings

Embeddings require an OpenAI API key and PostgreSQL with pgvector.

Bootstrap with embeddings:

```bash
scripts/aicos-bootstrap-full --with-embeddings
```

Or edit `.runtime-home/aicos-daemon.env` manually:

```env
AICOS_EMBEDDINGS=auto
OPENAI_API_KEY=<real-openai-api-key>
AICOS_EMBEDDING_MODEL=text-embedding-3-small
AICOS_EMBEDDING_DIMENSIONS=1536
AICOS_EMBEDDING_BATCH_SIZE=32
```

Restart daemon:

```bash
scripts/aicos-daemon-start
```

Expected `/health`:

```text
search_engine: postgresql_hybrid
search_status.vector: pgvector active
search_status.embeddings: enabled
index.embedding_coverage: 1.0
```

If the first health check shows `embedding_index: running`, wait 30-60 seconds
and poll again.

## 5. Trusted LAN Mode

Use LAN mode only on a trusted network. Non-loopback mode must have a bearer
token.

Start:

```bash
cd ~/aicos
integrations/mcp-daemon/start-lan.sh
```

Find host IP:

```bash
# macOS
ipconfig getifaddr en0

# Linux
hostname -I
```

From another machine:

```bash
TOKEN="<token-from-.runtime-home/aicos-daemon.env>"
curl -fsS -H "Authorization: Bearer $TOKEN" \
  http://<AICOS_LAN_IP>:8000/health \
  | python3 -m json.tool
```

If this fails:

- confirm both machines are on the same network;
- confirm the daemon printed a `0.0.0.0` bind;
- confirm firewall allows inbound TCP port `8000`;
- confirm the token includes the `Bearer ` prefix in the header.

## 6. Local MCP Client Setup

Use one of these depending on client support.

### Claude Code

HTTP-first with stdio fallback:

```bash
claude mcp add aicos \
  python3 ~/aicos/integrations/local-mcp-bridge/aicos_mcp_http_first.py \
  -s user
claude mcp list
```

Pure HTTP:

```bash
claude mcp add --transport http aicos http://127.0.0.1:8000/mcp -s user
```

### Codex Desktop

Use Streamable HTTP:

```text
Name: aicos
URL: http://127.0.0.1:8000/mcp
Headers: none for local loopback no-auth mode
```

For LAN/token mode, add:

```text
Authorization: Bearer <token>
```

### Claude Desktop

Local stdio is the most reliable path:

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/aicos/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ]
    }
  }
}
```

Restart Claude Desktop after editing config.

## 7. Railway Small-Team Deploy

Use this path when a team needs a hosted MCP endpoint.

### 7.1 Prerequisites

Install Railway CLI using one official method:

- Homebrew on macOS;
- npm on macOS/Linux/Windows with Node.js 16+;
- Railway shell installer;
- prebuilt binary.

Then:

```bash
railway login
railway status
```

If login is not possible from a browserless machine, use Railway's browserless
login or a project token according to the Railway CLI docs.

You also need:

- a GitHub repo connected to this checkout;
- a Railway app service for AICOS;
- a Railway PostgreSQL service;
- an OpenAI API key if you want `postgresql_hybrid`;
- one bearer token per external agent/client.

### 7.2 Link Or Create Railway Project

```bash
cd ~/aicos
railway init
# or, for an existing project:
railway link
railway status
```

Expected shape:

```text
Project: aicos-pub
Environment: production
Service: aicos-pub
```

### 7.3 Set Primary Daemon Token

```bash
openssl rand -hex 24 | railway variable set \
  --service aicos-pub \
  AICOS_DAEMON_TOKEN \
  --stdin \
  --skip-deploys
```

Do not commit or paste this token into docs.

### 7.4 Add PostgreSQL

```bash
railway add --database postgres --json
railway service list
railway variable set --service aicos-pub \
  'AICOS_PG_DSN=${{Postgres.DATABASE_URL}}' \
  --skip-deploys
```

The daemon applies schema on startup and attempts:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 7.5 Configure Embeddings

```bash
mkdir -p .runtime-home
cp docs/deploy/railway-embedding.env.example .runtime-home/railway-embedding.env
$EDITOR .runtime-home/railway-embedding.env
scripts/aicos-railway-apply-embedding-env
```

`.runtime-home/railway-embedding.env` must include:

```env
OPENAI_API_KEY=<real-openai-api-key>
AICOS_EMBEDDINGS=auto
AICOS_EMBEDDING_MODEL=text-embedding-3-small
AICOS_EMBEDDING_DIMENSIONS=1536
AICOS_EMBEDDING_BATCH_SIZE=32
```

### 7.6 Create Public Agent Tokens

For a fresh setup:

```bash
mkdir -p .runtime-home
umask 077

codex_token="$(openssl rand -hex 24)"
claude_token="$(openssl rand -hex 24)"
openclaw_token="$(openssl rand -hex 24)"

cat > .runtime-home/aicos-pub-agent-tokens.md <<EOF
# aicos-pub Agent Tokens

Endpoint: https://aicos-pub-production.up.railway.app/mcp

| Label | Bearer token | Scope |
|---|---|---|
| \`codex-agent-01\` | \`$codex_token\` | read/write \`projects/templates\` and \`projects/agents-dashboard\` |
| \`claude-agent-01\` | \`$claude_token\` | read/write \`projects/templates\` and \`projects/agents-dashboard\` |
| \`openclaw-agent-01\` | \`$openclaw_token\` | read/write \`projects/templates\` and \`projects/agents-dashboard\` |
EOF

railway variable set --service aicos-pub \
  "AICOS_DAEMON_EXTRA_TOKENS=codex-agent-01:$codex_token,claude-agent-01:$claude_token,openclaw-agent-01:$openclaw_token" \
  --skip-deploys

railway variable set --service aicos-pub \
  'AICOS_DAEMON_TOKEN_SCOPE_POLICY={"codex-agent-01":{"read":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"],"write":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"]},"claude-agent-01":{"read":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"],"write":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"]},"openclaw-agent-01":{"read":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"],"write":["projects/templates","projects/templates/*","projects/agents-dashboard","projects/agents-dashboard/*"]}}' \
  --skip-deploys
```

Public tokens should not read or write `projects/aicos` unless they are
explicitly maintainer/internal tokens.

### 7.7 Deploy

```bash
railway up --ci --service aicos-pub --message "Deploy AICOS MCP"
```

If only variables changed and code did not:

```bash
railway redeploy --service aicos-pub --yes
```

### 7.8 Railway Health Smoke

```bash
TOKEN="$claude_token"
curl -fsS -H "Authorization: Bearer $TOKEN" \
  https://aicos-pub-production.up.railway.app/health \
  | python3 -m json.tool
```

Expected:

```text
status: ok
search_engine: postgresql_hybrid
search_status.postgresql: active
search_status.vector: pgvector active
search_status.embeddings: enabled
index.embedding_coverage: 1.0
```

If you get `markdown_direct` after deploy and health says schema lock timeout:

```bash
railway restart --service aicos-pub --yes
sleep 20
```

Then run health again.

## 8. Railway MCP Smoke

List tools:

```bash
curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  https://aicos-pub-production.up.railway.app/mcp
```

Read public project context:

```bash
curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "aicos_get_handoff_current",
      "arguments": {
        "actor": "A1",
        "project_slug": "agents-dashboard",
        "agent_family": "smoke",
        "agent_instance_id": "railway-smoke",
        "work_type": "orientation",
        "work_lane": "intake",
        "execution_context": "railway-smoke via aicos_railway_public"
      }
    }
  }' \
  https://aicos-pub-production.up.railway.app/mcp
```

Expected:

```text
result.content exists
isError is false
```

Verify public tokens cannot read protected core context:

```bash
curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "aicos_get_handoff_current",
      "arguments": {
        "actor": "A1",
        "scope": "projects/aicos",
        "agent_family": "smoke",
        "agent_instance_id": "railway-smoke",
        "work_type": "orientation",
        "work_lane": "intake",
        "execution_context": "railway-smoke via aicos_railway_public"
      }
    }
  }' \
  https://aicos-pub-production.up.railway.app/mcp
```

Expected:

```text
scope_read_denied
```

## 9. Common Failures

| Symptom | Meaning | Fix |
|---|---|---|
| `python3: command not found` | Python missing | Install Python 3.10+ |
| `venv` creation fails | `venv` package missing | Install `python3-venv` or equivalent |
| `/health` connection refused | daemon not running or wrong port | Start `scripts/aicos-daemon-start`; check `AICOS_DAEMON_PORT` |
| `markdown_direct` | PG unavailable | Start Docker/Postgres.app or set `AICOS_PG_DSN` |
| `postgresql_fts` | PG works, embeddings missing | Add `OPENAI_API_KEY`, ensure pgvector, restart |
| `401 Unauthorized` | missing/stale token | Use `Authorization: Bearer <token>` and redeploy/restart after env changes |
| `missing_read_identity` | MCP payload lacks audit fields | Add `agent_family`, `agent_instance_id`, `work_type`, `work_lane`, `execution_context` |
| `missing_project_scope` | scope directory absent | Use `projects/agents-dashboard` or add project brain files |
| Railway schema lock timeout | transient PG lock on startup | `railway restart --service aicos-pub --yes`, then retest |
| Claude Desktop remote connector cannot add bearer header | UI limitation | use stdio locally or local HTTPS proxy that injects the token |

## 10. Minimum Completion Checklist

Local:

- `./aicos --help` works.
- `scripts/aicos-daemon-start` starts without crashing.
- `curl http://127.0.0.1:8000/health` returns `status: ok`.
- `./aicos brain status` prints index freshness.
- At least one MCP client can list AICOS tools.

Railway:

- `railway status` is linked to the right project/service.
- `/health` with bearer token returns `status: ok`.
- `search_engine` is `postgresql_hybrid` if embeddings are expected.
- `tools/list` works through `/mcp`.
- public token can read `projects/agents-dashboard`.
- public token cannot read `projects/aicos`.
