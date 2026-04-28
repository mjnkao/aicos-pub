# AICOS MCP Client Compatibility Matrix

Status: working matrix  
Updated: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Track the current AICOS HTTP MCP compatibility surface for agent clients.

This matrix is part of Phase 0.5 stabilization. It should remain practical and
operational: which client uses which path, what is known to work, and what
still needs real-client confirmation.

## Operating Rule

- A1 agents use HTTP daemon MCP for AICOS-facing reads/writes.
- A1 agents do not write AICOS markdown truth directly.
- Only `A2-Core-R` and `A2-Core-C` may fall back to direct AICOS file writes
  when HTTP MCP is genuinely blocked or AICOS internals are being
  restructured.

## Matrix

| Client | Token label | Transport/path | Auth shape | Daemon health | Tools/list | Startup read | Semantic write | Real-client confirmation | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Codex Desktop | `codex` | `http://127.0.0.1:8000/mcp` or LAN HTTP | Bearer header | pass | pass | pass | pass | partial | Daemon-level smoke passed. Current thread can use HTTP daemon by curl; app connector state should still be verified when needed. |
| Claude Code | `claude-code` | HTTP MCP | Bearer header | pass | pass | pass | pass | pending | Token path works at daemon level. Real `claude-code` client smoke still needed after connector refresh. |
| Claude Desktop | `claude-code` via local proxy | `https://localhost:8443/mcp` | local proxy injects upstream bearer | pass | not tested in this pass | not tested in this pass | not tested in this pass | pending | HTTPS proxy health passed. Tool-level smoke should be done from Claude Desktop itself because UI/header behavior differs. |
| Antigravity | `antigravity` | HTTP/SSE config using `serverUrl` + `headers.Authorization` | Bearer header | pass | pass | pass | pass | partial | Daemon-level smoke passed. Prior feedback showed Antigravity needs its exact config shape; real client smoke should confirm tools load. |
| OpenClaw / mjnclaw | `openclaw-vm` | LAN/VM HTTP MCP | Bearer header | pass | pass | pass | pass | pending | Daemon-level smoke passed. Real VM/client runtime still needs confirmation because previous issues involved client-side cancellation/config. |
| Reserved 01 | `reserved-01` | HTTP MCP | Bearer header | pass | not tested | not tested | not tested | not assigned | Spare token only. |
| Reserved 02 | `reserved-02` | HTTP MCP | Bearer header | pass | not tested | not tested | not tested | not assigned | Spare token only. |

## Phase 0.5 Findings

### Read/write bootstrap mismatch

Read bootstrap accepts:

- `work_type=orientation`
- `work_lane=intake`

Semantic writes currently reject `work_type=orientation`. First-contact writes
should use a write-allowed type such as:

- `work_type=ops`
- `work_lane=intake`

This is a real A1 friction point. It should be either documented more clearly
or simplified in the schema.

### Search runtime restored

Initial Phase 0.5 smoke found:

- `search_engine=markdown_direct`
- PostgreSQL connection refused on `127.0.0.1:5432`
- vector/embedding indexes not initialized

Follow-up restored Postgres.app PostgreSQL and restarted the daemon. Current
status:

- `search_engine=postgresql_hybrid`
- PostgreSQL active
- pgvector active
- embeddings enabled
- embedding coverage `1.0`
- GBrain sync fresh
- PG index fresh
- embedding freshness fresh

The daemon-level query smoke now returns hybrid FTS + vector results.

## Next Checks

1. Run actual connector-level smoke from each real client as they continue
   using AICOS.
2. Confirm each client refreshes `tools/list` after schema changes.
3. Decide whether `orientation` should be allowed for early write payloads or
   whether templates should steer agents to `ops/intake`.
4. Keep this matrix updated whenever token labels, auth paths, or client
   config shapes change.
