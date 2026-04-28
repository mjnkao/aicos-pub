# Status Item: ARCH-R-02

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-02`
Title: Retrieval freshness and brain status implemented
Last write id: `20260423T024952Z-88d02974c1`
Last updated at: `2026-04-23T02:49:52+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-a2-core-20260423-arch-r-02-search-freshness`
Agent display name: `unknown`
Work type: `code`
Work lane: `search-retrieval-freshness`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented sync brain --text-only/--full, default full GBrain import, runtime sync ledger, ./aicos brain status, PG index freshness and embedding coverage stats, and daemon background embedding refresh so startup serves FTS immediately.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

ARCH-R-02 acceptance required agents to see last sync/staleness and distinguish text, FTS, and embedding refresh instead of silently serving stale retrieval context.

## Next Step

Validate full PG+pgvector+embedding runtime on a configured machine with psycopg2/OpenAI key and tune cost/rate-limit policy for background embedding refresh.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/kernel.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/indexer.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/engine.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/config.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/embedding.py`
  - `brain/projects/aicos/working/gbrain-search-reuse-review.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
