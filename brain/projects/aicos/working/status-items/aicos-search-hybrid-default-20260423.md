# Status Item: aicos-search-hybrid-default-20260423

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-search-hybrid-default-20260423`
Title: HTTP daemon PostgreSQL hybrid search is default when available
Last write id: `20260423T023026Z-078d881aa9`
Last updated at: `2026-04-23T02:30:26+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-20260423-hybrid-search`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-search-hybrid-default`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented daemon search preference order: PostgreSQL hybrid search with pgvector embeddings when OPENAI_API_KEY and pgvector are available, PostgreSQL FTS fallback when embeddings are unavailable, and markdown-direct fallback when PostgreSQL is unavailable.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

User requested making HTTP daemon + PostgreSQL + embedding the default search direction, with other modes as fallback.

## Next Step

Implement retrieval freshness/status next so agents can see text, FTS, and embedding index freshness/coverage before relying on semantic search.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/pg_search/embedding.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/engine.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/indexer.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `integrations/mcp-daemon/docker-compose.yml`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
