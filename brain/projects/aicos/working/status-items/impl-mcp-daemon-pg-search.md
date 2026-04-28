# Status Item: IMPL-MCP-DAEMON-PG-SEARCH

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `IMPL-MCP-DAEMON-PG-SEARCH`
Title: MCP HTTP daemon + PostgreSQL FTS search engine — ready to merge
Last write id: `20260422T032914Z-179003509e`
Last updated at: `2026-04-22T03:29:14+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `charming-nobel-eeb666`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-mcp-daemon-http-pg-search`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `feat/pg-search-engine`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Both branches pushed. `feat/pg-search-engine` is the superset — includes HTTP daemon (ThreadingHTTPServer + TTL cache) AND full pg_search package (schema, indexer, intent routing, FTS engine). Vietnamese-safe `'simple'` text config. Authority boost (canonical=2.0, handoff=1.5). Freshness penalty (stale=0.5×). Graceful PG fallback. Docker Compose included. Schema is pgvector-ready (Phase 3: just ADD COLUMN embedding vector(1536)).

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

none

## Next Step

Codex: merge `feat/pg-search-engine` into main. `feat/mcp-daemon-http-cache` can be closed (redundant). See integrations/mcp-daemon/README.md merge notes section for file-by-file guidance.

## Trace Refs

- artifact_refs:
  - `feat/pg-search-engine`
  - `integrations/mcp-daemon/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
