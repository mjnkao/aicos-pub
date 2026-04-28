# AICOS Phase 0.5 Stabilization Pass

Status: initial stabilization pass  
Date: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Start Phase 0.5 from the Option C transition checklist by testing the current
HTTP MCP operating surface before deeper modularization work.

Phase 0.5 exists to keep real client and daemon friction visible. A1-style
work should not hide AICOS-facing read/write problems behind direct markdown
edits.

## Current Operating Rule

- A1 agents should use the HTTP daemon MCP path for AICOS-facing reads/writes.
- A1 agents should not directly write AICOS markdown truth as a convenience
  fallback.
- Only `A2-Core-R` and `A2-Core-C` may fall back to direct AICOS file writes
  when HTTP MCP is genuinely blocked or when restructuring AICOS internals
  requires it.
- Even A2-Core should default to HTTP MCP first when recording AICOS-facing
  state, so operational friction is discovered early.

## Smoke Scope

This pass tested daemon-level HTTP MCP behavior for the current main token
labels:

- `codex`
- `claude-code`
- `antigravity`
- `openclaw-vm`
- `reserved-01`
- `reserved-02`

It also checked the local Claude Desktop HTTPS proxy health path.

## Results

### Health

Result: pass.

- daemon `/health` returned `status=ok`
- all accepted token labels returned authenticated health
- Claude Desktop local HTTPS proxy returned `status=ok`

Important runtime detail:

- current daemon search engine is `markdown_direct`
- PostgreSQL is currently unavailable on `127.0.0.1:5432`
- vector and embedding indexes are not initialized in the current runtime

This does not block HTTP MCP connectivity, but it means this pass did not
validate PostgreSQL hybrid retrieval.

### Tool Listing

Result: pass for main labeled tokens.

The following token paths could call `tools/list` and see
`aicos_get_startup_bundle`:

- `codex`
- `claude-code`
- `antigravity`
- `openclaw-vm`

### Read Smoke

Result: pass.

The following read surfaces were smoke-tested through HTTP MCP:

- `aicos_get_startup_bundle`
- `aicos_get_project_health`
- `aicos_get_handoff_current`
- `aicos_get_status_items`
- `aicos_query_project_context`

Read bootstrap used:

- `work_type=orientation`
- `work_lane=intake`

### Write Smoke

Result: pass after payload correction.

Semantic status-item write smoke succeeded for:

- `codex`
- `claude-code`
- `antigravity`
- `openclaw-vm`

Each path wrote a resolved smoke status item through
`aicos_update_status_item` without direct markdown fallback.

## Findings

### Finding 1 — Read bootstrap and write payloads differ on `work_type`

Read bootstrap accepts `work_type=orientation`, but semantic writes currently
reject `work_type=orientation`.

Observed failure:

- `aicos_update_status_item`
- error: `invalid_enum`
- field: `work_type`
- received: `orientation`
- allowed write values include `ops`, `planning`, `research`, `review`,
  `code`, `content`, `data`, `design`, and `mixed`

Corrected write smoke used:

- `work_type=ops`
- `work_lane=intake`

Impact:

- A new A1 may reasonably reuse the first-contact read payload for an early
  write and hit this error.
- The error is explicit and useful, but the read/write bootstrap distinction
  should be documented or simplified.

Suggested follow-up:

- Decide whether write bootstrap should allow `work_type=orientation`, or
  whether docs/templates should clearly tell agents to use `ops` for
  first-contact setup/friction/status writes.

### Finding 2 — Current runtime validates HTTP MCP but not PG hybrid search

The daemon is healthy, but PostgreSQL is down in the current local runtime.

Impact:

- HTTP MCP connectivity and semantic write behavior are usable.
- Search quality is not being validated against PG hybrid retrieval in this
  pass.

Suggested follow-up:

- Keep this as a known Phase 0.5 finding.
- Analyze PG/rate-limit/runtime freshness separately before using search
  quality as an architecture signal.

### Finding 3 — Daemon-level smoke is not the same as UI/client-level smoke

This pass validates token and HTTP MCP behavior at the daemon level. It does
not prove that every client UI/runtime has refreshed its MCP connector, schema,
or local wrapper correctly.

Suggested follow-up:

- Run real-client smoke for each configured client when available:
  - Codex Desktop
  - Claude Code
  - Claude Desktop
  - Antigravity
  - OpenClaw / mjnclaw

## Follow-Up Fixes Applied

### PostgreSQL / hybrid search restored

Follow-up on 2026-04-28 restored the local PostgreSQL path:

- started Postgres.app PostgreSQL 18 using the existing local data directory;
- restarted AICOS launch agents;
- confirmed daemon health reports `search_engine=postgresql_hybrid`;
- confirmed `pgvector active`;
- confirmed embedding coverage is `1.0`;
- fixed a PostgreSQL FTS SQL bug where `ORDER BY fts_score * authority_mult`
  referenced a SELECT alias in a way PostgreSQL rejected;
- confirmed `aicos_query_project_context` now returns hybrid FTS + vector
  results through HTTP MCP;
- ran `./aicos sync brain --text-only`, which completed successfully;
- confirmed `./aicos brain status` reports:
  - GBrain sync: fresh
  - PG index: fresh
  - embedding freshness: fresh
  - missing/stale embeddings: 0

### Duplicate dev proxy removed

The stale `dev.aicos.https-proxy` and `dev.aicos.mcp-daemon` launch labels were
removed. The active launch labels are now the `ai.aicos.*` services.

### Portable sample project source metadata added

The high-severity sample project feedback about machine-specific project paths was valid.
The active project registry and sample project project profile now include canonical repo
metadata:

- `git@github.com:mjnkao/sample project-Trading-Framework.git`
- default branch: `main`

Historical absolute paths remain in evidence/checkpoints as provenance, but
new startup/profile metadata should prefer canonical source URL plus optional
local checkout hints.

## Current Status

Phase 0.5 is materially complete enough to proceed to Phase 1.

Current confidence:

- daemon health: good
- token mapping: good
- MCP read surface: good at daemon level
- MCP write surface: usable, with one bootstrap payload friction
- search runtime: restored to PostgreSQL hybrid + pgvector
- freshness: GBrain, PG index, and embeddings fresh
- real client UX: still needs per-client confirmation as agents continue using
  AICOS

## Next Step

Move into Phase 1 module inventory. Keep the client compatibility matrix alive
and let A1 agents continue using the HTTP MCP path. If real client use exposes
new Phase 0.5 friction, record it and fix it as a follow-up instead of keeping
all work blocked in stabilization.
