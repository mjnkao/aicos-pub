# Status Item: PERF-PG-REINDEX-DEBOUNCE

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `PERF-PG-REINDEX-DEBOUNCE`
Title: PG reindex debounce and embedding background path implemented
Last write id: `20260423T064722Z-ab9511d7cd`
Last updated at: `2026-04-23T06:47:22+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `ops-stability`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented per-scope debounced reindex scheduling in the HTTP daemon. Rapid writes now coalesce through AICOS_REINDEX_DEBOUNCE_SECONDS, one reindex runs per scope, and pending writes schedule a follow-up pass instead of spawning unbounded concurrent reindex threads. Embeddings remain background-only; daemon startup indexes text first and schedules embedding refresh separately.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Implemented by Codex during AICOS HTTP/embedding hardening pass on 2026-04-23.

## Next Step

Watch /health search_status.reindex and embedding_index under multi-agent write load; only add a durable queue if real contention appears.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `integrations/mcp-daemon/aicos-daemon.env.example`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
