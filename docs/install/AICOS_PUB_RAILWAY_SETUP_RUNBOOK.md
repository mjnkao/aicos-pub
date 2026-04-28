# aicos-pub Railway Setup Runbook

This runbook turns the 2026-04-28 deployment pass into a repeatable setup guide
for running `aicos-pub` as a public Railway MCP server.

It covers:

- Railway app deployment
- Railway PostgreSQL + pgvector
- OpenAI embeddings for `postgresql_hybrid` retrieval
- Bearer token setup for agents
- MCP smoke tests
- Known Railway deploy failure modes and fixes

## Target Result

Healthy public runtime:

```text
MCP URL: https://aicos-pub-production.up.railway.app/mcp
Health URL: https://aicos-pub-production.up.railway.app/health
search_engine: postgresql_hybrid
search_status.postgresql: active
search_status.vector: pgvector active
search_status.embeddings: enabled
index.embedding_coverage: 1.0
```

## Prerequisites

- GitHub repo for `aicos-pub`
- Railway CLI logged in
- Railway project linked to this checkout
- OpenAI API key for embedding search
- A strong primary daemon bearer token
- One bearer token per external agent/client

Check Railway login:

```bash
railway status
```

Check repo state:

```bash
git status --short --branch
```

## Important Security Rules

- Never commit real bearer tokens, OpenAI keys, `.env` files, or local runtime
  homes.
- Store filled env/token files under `.runtime-home/`; this path is ignored by
  git.
- Public/community tokens may write only to `projects/aicos-pub`.
- Do not grant public/community tokens internal maintainer access.
- Do not write public-export continuity into private `projects/aicos`.

## Railway Files In The Repo

Expected tracked files:

```text
railway.toml
nixpacks.toml
scripts/aicos-railway-start
scripts/aicos-railway-apply-embedding-env
docs/deploy/railway-embedding.env.example
docs/install/AICOS_PUB_RAILWAY_AGENT_CONNECT.md
```

`scripts/aicos-railway-start` should:

- Require `AICOS_DAEMON_TOKEN`
- Bind to `0.0.0.0`
- Use `$PORT`
- Use PostgreSQL when `AICOS_PG_DSN` or `DATABASE_URL` exists
- Fall back to `--no-pg` only when no DSN exists

## 1. Create Or Link Railway Project

If the project does not exist yet:

```bash
railway init
```

If it already exists:

```bash
railway link
```

Confirm:

```bash
railway status
```

Expected:

```text
Project: aicos-pub
Environment: production
Service: aicos-pub
```

## 2. Set Primary Daemon Token

Generate a strong token without printing it into docs:

```bash
openssl rand -hex 24 | railway variable set --service aicos-pub AICOS_DAEMON_TOKEN --stdin --skip-deploys
```

Do not put this primary token in public guides.

## 3. Add Railway PostgreSQL

Create the database service:

```bash
railway add --database postgres --json
```

Confirm the service exists:

```bash
railway service list
```

Expected database service:

```text
Postgres
image: ghcr.io/railwayapp-templates/postgres-ssl:18
```

Configure the app service to use the database:

```bash
railway variable set --service aicos-pub 'AICOS_PG_DSN=${{Postgres.DATABASE_URL}}' --skip-deploys
```

The daemon will apply PostgreSQL schema and opportunistically run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

If pgvector is available, `/health` should later report:

```text
search_status.vector: pgvector active
```

## 4. Configure OpenAI Embeddings

Create a local ignored env file:

```bash
mkdir -p .runtime-home
cp docs/deploy/railway-embedding.env.example .runtime-home/railway-embedding.env
```

Edit:

```bash
$EDITOR .runtime-home/railway-embedding.env
```

Expected content shape:

```env
OPENAI_API_KEY=<real-openai-api-key>
AICOS_EMBEDDINGS=auto
AICOS_EMBEDDING_MODEL=text-embedding-3-small
AICOS_EMBEDDING_DIMENSIONS=1536
AICOS_EMBEDDING_BATCH_SIZE=32
```

Apply variables safely:

```bash
scripts/aicos-railway-apply-embedding-env
```

The script sends `OPENAI_API_KEY` through `railway variable set --stdin` and
does not print it.

## 5. Create Agent Bearer Tokens

Use one token label per agent/client. Recommended labels:

```text
codex-agent-01
claude-agent-01
openclaw-agent-01
codex-a2-core-pub
```

Recommended policy for public agents:

```json
{
  "codex-agent-01": {"read": ["projects/*"], "write": ["projects/aicos-pub"]},
  "claude-agent-01": {"read": ["projects/*"], "write": ["projects/aicos-pub"]},
  "openclaw-agent-01": {"read": ["projects/*"], "write": ["projects/aicos-pub"]},
  "codex-a2-core-pub": {"read": ["projects/*"], "write": ["projects/aicos-pub"]}
}
```

Do not add these public labels to `AICOS_DAEMON_INTERNAL_TOKEN_LABELS`.

Generate tokens locally:

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
| \`codex-agent-01\` | \`$codex_token\` | read \`projects/*\`, write \`projects/aicos-pub\` |
| \`claude-agent-01\` | \`$claude_token\` | read \`projects/*\`, write \`projects/aicos-pub\` |
| \`openclaw-agent-01\` | \`$openclaw_token\` | read \`projects/*\`, write \`projects/aicos-pub\` |
EOF
```

Set Railway variables. Preserve any existing labels when adding new ones.
Example for a fresh setup:

```bash
railway variable set --service aicos-pub \
  "AICOS_DAEMON_EXTRA_TOKENS=codex-agent-01:$codex_token,claude-agent-01:$claude_token,openclaw-agent-01:$openclaw_token" \
  --skip-deploys

railway variable set --service aicos-pub \
  'AICOS_DAEMON_TOKEN_SCOPE_POLICY={"codex-agent-01":{"read":["projects/*"],"write":["projects/aicos-pub"]},"claude-agent-01":{"read":["projects/*"],"write":["projects/aicos-pub"]},"openclaw-agent-01":{"read":["projects/*"],"write":["projects/aicos-pub"]}}' \
  --skip-deploys
```

For existing deployments, inspect labels without printing token values:

```bash
python3 - <<'PY'
import subprocess, json
out = subprocess.check_output(
    ["railway", "variable", "list", "--service", "aicos-pub", "--kv"],
    text=True,
)
extra = policy = ""
for line in out.splitlines():
    if line.startswith("AICOS_DAEMON_EXTRA_TOKENS="):
        extra = line.split("=", 1)[1]
    if line.startswith("AICOS_DAEMON_TOKEN_SCOPE_POLICY="):
        policy = line.split("=", 1)[1]
print("extra_labels=", [part.split(":", 1)[0] for part in extra.split(",") if ":" in part])
print("policy_labels=", sorted(json.loads(policy).keys()) if policy else [])
PY
```

## 6. Ensure Public MCP Scope Exists

The public write scope must exist in the exported corpus:

```text
brain/projects/aicos-pub/canonical/project-profile.md
brain/projects/aicos-pub/working/handoff/current.md
brain/projects/aicos-pub/working/status-items/README.md
brain/projects/aicos-pub/working/feedback/README.md
```

If this scope is missing, write tools return:

```text
missing_project_scope
```

Fix by adding the minimal scope files, committing, pushing, and redeploying.

## 7. Deploy

Deploy app source:

```bash
railway up --ci --message "Deploy aicos-pub Railway MCP"
```

If only variables changed, Railway may need redeploy, not just restart:

```bash
railway service redeploy --service aicos-pub --yes --json
```

After redeploy, wait for success:

```bash
railway service status --service aicos-pub --json
```

## 8. Known Railway Issue: Schema Lock Timeout

Observed failure after deploy/redeploy:

```text
PostgreSQL unavailable (Schema apply failed: canceling statement due to lock timeout)
search_engine: markdown_direct
```

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Then retest `/health`.

Future hardening task: add retry/backoff or longer lock timeout around schema
apply so manual restart is not required.

## 9. Health Smoke Test

Use any valid token:

```bash
TOKEN="<agent-token>"

curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  https://aicos-pub-production.up.railway.app/health
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

If `embedding_index` is `running`, wait and poll again:

```bash
for i in 1 2 3 4 5; do
  sleep 12
  curl -fsS -H "Authorization: Bearer $TOKEN" \
    https://aicos-pub-production.up.railway.app/health \
    | python3 -m json.tool \
    | rg 'search_engine|embedding_index|embedded_docs|embedding_coverage'
done
```

## 10. MCP Smoke Tests

List tools:

```bash
TOKEN="<agent-token>"

curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  https://aicos-pub-production.up.railway.app/mcp
```

Query context:

```bash
curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "aicos_query_project_context",
      "arguments": {
        "actor": "A1",
        "scope": "projects/aicos",
        "query": "current AICOS status and next tasks",
        "agent_family": "smoke",
        "agent_instance_id": "railway-smoke",
        "work_type": "orientation",
        "work_lane": "intake",
        "execution_context": "railway-smoke",
        "max_results": 8
      }
    }
  }' \
  https://aicos-pub-production.up.railway.app/mcp
```

Expected query metadata:

```text
engine: postgresql_hybrid
vector_status: active
```

Write smoke to the public scope:

```bash
curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "aicos_record_feedback",
      "arguments": {
        "mcp_contract_ack": "mcp-v0.5-write-contract-ack",
        "scope": "projects/aicos-pub",
        "agent_family": "smoke",
        "agent_instance_id": "railway-write-smoke",
        "actor_role": "A1",
        "work_type": "ops",
        "work_lane": "railway-setup-smoke",
        "execution_context": "railway-smoke",
        "feedback_type": "no_issue",
        "severity": "low",
        "title": "Railway write smoke",
        "summary": "Bearer token can write to projects/aicos-pub."
      }
    }
  }' \
  https://aicos-pub-production.up.railway.app/mcp
```

Expected:

```text
status: success
scope: projects/aicos-pub
```

## 11. Codex MCP Setup

Add a Codex MCP server in `<codex-home>/config.toml`:

```toml
[mcp_servers.aicos_pub]
enabled = true
url = "https://aicos-pub-production.up.railway.app/mcp"

[mcp_servers.aicos_pub.http_headers]
Authorization = "Bearer <agent-token>"

[mcp_servers.aicos_pub.tools.aicos_get_project_health]
approval_mode = "approve"

[mcp_servers.aicos_pub.tools.aicos_get_handoff_current]
approval_mode = "approve"

[mcp_servers.aicos_pub.tools.aicos_get_startup_bundle]
approval_mode = "approve"

[mcp_servers.aicos_pub.tools.aicos_query_project_context]
approval_mode = "approve"

[mcp_servers.aicos_pub.tools.aicos_write_handoff_update]
approval_mode = "approve"

[mcp_servers.aicos_pub.tools.aicos_record_feedback]
approval_mode = "approve"
```

Restart Codex/Codex Desktop after editing config.

Recommended naming:

```text
aicos_pub  -> Railway public MCP
aicos_http -> local/private AICOS MCP
```

## 12. Claude Code Setup

Claude Code supports remote HTTP MCP with bearer headers:

```bash
claude mcp add --transport http aicos-pub \
  https://aicos-pub-production.up.railway.app/mcp \
  --scope local \
  --header "Authorization: Bearer <agent-token>"
```

Fallback:

```bash
claude mcp add-json aicos-pub \
  '{"type":"http","url":"https://aicos-pub-production.up.railway.app/mcp","headers":{"Authorization":"Bearer <agent-token>"}}' \
  --scope local
```

Verify:

```bash
claude mcp list
claude mcp get aicos-pub
```

## 13. Claude Desktop Connector

The Claude Desktop custom connector UI may not expose a bearer header field.
When that is true, use a local HTTPS proxy that injects the bearer token:

```bash
TOKEN="<agent-token>"

AICOS_HTTPS_UPSTREAM_TOKEN="$TOKEN" \
python3 integrations/mcp-daemon/aicos_https_proxy.py \
  --daemon-url https://aicos-pub-production.up.railway.app \
  --https-port 8443 \
  --host 127.0.0.1
```

In Claude Desktop custom connector:

```text
Name: aicos-pub
Remote MCP server URL: https://localhost:8443/mcp
OAuth Client ID: blank
OAuth Client Secret: blank
```

## 14. Public-Safety Scan Before Push

Run before committing docs or setup changes:

```bash
rg -n --hidden \
  --glob '!.git/**' \
  --glob '!.runtime-home/**' \
  --glob '!*.lock' \
  --glob '!bun.lock' \
  -i '<private-path-or-secret-regex>' .
```

Expected: no matches.

Keep the concrete private marker regex in an ignored local note or shell
history, not in committed docs. The scan should cover private home paths,
private project names, private key blocks, OpenAI keys, GitHub tokens, cloud
access keys, daemon tokens, and literal bearer-token values.

## 15. Deployment Notes To Preserve

Record every setup/deploy failure and fix in:

```text
docs/deploy/railway-deploy-log.md
```

This log is the raw operational history. This runbook is the clean install path.

## Troubleshooting Summary

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` | Missing or stale bearer token | Confirm `Authorization: Bearer <token>` and redeploy/restart after variable changes |
| `markdown_direct` | PostgreSQL schema lock timeout or no DSN | Confirm `AICOS_PG_DSN`, then restart service |
| `postgresql_fts` | PostgreSQL active, embeddings missing | Set `OPENAI_API_KEY` and embedding vars, redeploy/restart |
| `missing_project_scope` | `brain/projects/aicos-pub` missing | Add minimal public scope files, commit, deploy |
| New token label not visible | Running deployment has old env snapshot | `railway service redeploy`, then restart if lock timeout occurs |
| Railway healthcheck fails | `/health` requires bearer token | Do not use unauthenticated Railway `healthcheckPath` |
