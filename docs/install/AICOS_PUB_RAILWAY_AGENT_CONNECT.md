# Connect Agents to aicos-pub on Railway

This guide lets another agent connect to the public `aicos-pub` Railway MCP
daemon without needing access to the private local AICOS checkout.

## Endpoint

```text
https://aicos-pub-production.up.railway.app/mcp
```

Health endpoint:

```text
https://aicos-pub-production.up.railway.app/health
```

The service requires bearer auth. Unauthenticated health and MCP calls return
`401`.

## Runtime Identity Boundary

Use the MCP server alias:

```text
aicos_railway_public
```

This distinguishes the public Railway runtime from a private/local AICOS
runtime such as:

```text
aicos_local_private
```

`actor_role` is relative to the runtime receiving the MCP call. It is not a
global identity for Codex, Claude, or OpenClaw across every AICOS deployment.

For this public Railway runtime:

- use `actor_role: "A1"` when the agent is an external/public work agent
  writing feedback, status, or handoff into `projects/aicos-pub`;
- use `actor_role: "A2-Core-C"` only when the token and assignment explicitly
  make the agent an internal maintainer of the public Railway AICOS runtime;
- keep `agent_family` as the product/client family such as `codex`,
  `claude-code`, or `openclaw`;
- include runtime context in `execution_context` and `work_context` on writes.

Reference:

```text
docs/architecture/runtime-agent-identity-boundary.md
```

## Token Labels

Current dedicated agent token labels:

| Label | Intended user | Read scope | Write scope |
|---|---|---|---|
| `codex-agent-01` | Codex-compatible agents | `projects/*` | `projects/aicos-pub` |
| `claude-agent-01` | Claude-compatible agents | `projects/*` | `projects/aicos-pub` |
| `openclaw-agent-01` | OpenClaw/VM agents | `projects/*` | `projects/aicos-pub` |

Token values are **not committed**. On the maintainer machine, the generated
tokens are stored in:

```text
.runtime-home/aicos-pub-agent-tokens.md
```

That file is ignored by git through `.runtime-home/`. Share one token per agent
over a private channel. Do not paste token values into issues, commits, docs, or
MCP context.

## Quick Smoke Test

Replace `<TOKEN>` with one bearer token from the local secret file:

```bash
TOKEN="<TOKEN>"

curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  https://aicos-pub-production.up.railway.app/health
```

Expected high-level response:

```json
{
  "status": "ok",
  "search_engine": "postgresql_hybrid"
}
```

The full health payload should also report:

```text
search_status.postgresql: active
search_status.vector: pgvector active
search_status.embeddings: enabled
index.embedding_coverage: 1.0
```

## MCP JSON-RPC Smoke Test

List tools:

```bash
TOKEN="<TOKEN>"

curl -fsS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  https://aicos-pub-production.up.railway.app/mcp
```

Query project context:

```bash
TOKEN="<TOKEN>"

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
        "agent_family": "codex",
        "agent_instance_id": "agent-smoke-test",
        "work_type": "orientation",
        "work_lane": "intake",
        "execution_context": "railway-agent-smoke",
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

## Generic MCP Client Configuration

Use Streamable HTTP transport with a bearer header:

```json
{
  "mcpServers": {
    "aicos_railway_public": {
      "type": "http",
      "url": "https://aicos-pub-production.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer <TOKEN>"
      }
    }
  }
}
```

If a client UI does not support custom HTTP headers, use a local proxy that
injects the bearer token, or choose a client profile that supports bearer
headers.

## Write Boundary

Dedicated public agent tokens may write only to:

```text
projects/aicos-pub
```

They may read:

```text
projects/*
```

They are intentionally not internal maintainer tokens. Writes to protected
private service scopes such as `projects/aicos` should be rejected.

## Useful Read Tools

Start with these tools:

```text
aicos_get_project_health
aicos_get_handoff_current
aicos_query_project_context
aicos_get_feedback_digest
```

Use this standard metadata on first contact:

```json
{
  "scope": "projects/aicos-pub",
  "agent_family": "<client-family>",
  "agent_instance_id": "<unique-agent-id>",
  "work_type": "orientation",
  "work_lane": "intake",
  "execution_context": "<client-runtime> via aicos_railway_public",
  "work_context": "runtime=aicos_railway_public; agent_position=external_agent"
}
```

For write tools, include `actor_role` as runtime-relative identity:

```json
{
  "actor_role": "A1",
  "agent_family": "codex",
  "execution_context": "codex-desktop via aicos_railway_public",
  "work_context": "runtime=aicos_railway_public; agent_position=external_agent; functional_role=reviewer"
}
```

## Troubleshooting

`401 Unauthorized`:

- The bearer token is missing, malformed, or not loaded by the current Railway
  deployment.
- Confirm the header is exactly `Authorization: Bearer <TOKEN>`.
- If tokens were just changed, redeploy or restart the Railway service.

`search_engine: markdown_direct`:

- PostgreSQL schema setup may have hit a transient Railway/Postgres lock
  timeout.
- Restart the Railway `aicos-pub` service and retest `/health`.

`search_engine: postgresql_fts`:

- PostgreSQL is active but embeddings are not active.
- Confirm `OPENAI_API_KEY`, `AICOS_EMBEDDINGS=auto`, and embedding variables are
  set on the Railway `aicos-pub` service.

Expected healthy retrieval state:

```text
search_engine: postgresql_hybrid
search_status.postgresql: active
search_status.vector: pgvector active
search_status.embeddings: enabled
index.embedding_coverage: 1.0
```
