# Status Item: AICOS-BRAIN-STATUS-PG-STALE-FALSE-SIGNAL

Status: open
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-BRAIN-STATUS-PG-STALE-FALSE-SIGNAL`
Title: brain status can report PG index stale while daemon health and query are healthy
Last write id: `phase-1-pg-status-false-stale-20260428`
Last updated at: `2026-04-28T05:46:35+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-phase-1-module-inventory`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-runtime-provider-hygiene`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

After Phase 1 text-only sync and daemon reindex, ./aicos brain status still reported PG index stale, while /health showed search_engine=postgresql_hybrid, stale_docs=0, embedding coverage=1.0, and query returned the new Phase 1 note.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Status/monitor freshness logic should not create false alarms for A1/A2 operators. This is observability debt, not a confirmed retrieval outage.

## Next Step

In a focused ops pass, align CLI brain status freshness with daemon health/index row state instead of relying on a misleading timestamp comparison.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-phase-1-module-inventory-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
