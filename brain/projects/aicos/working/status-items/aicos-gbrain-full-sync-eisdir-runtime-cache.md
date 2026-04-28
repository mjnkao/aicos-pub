# Status Item: aicos-gbrain-full-sync-eisdir-runtime-cache

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-gbrain-full-sync-eisdir-runtime-cache`
Title: GBrain full sync can fail on Bun runtime cache EISDIR
Last write id: `20260428T075745Z-f7bb392590`
Last updated at: `2026-04-28T07:57:45+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-checklist-5-step`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-checklist-5-step`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

GBrain import path is now hardened to skip non-file/unreadable paths instead of crashing on EISDIR-like cases, and scripts/gbrain_local.sh loads the local daemon env so full sync has the same embedding environment as the daemon. Verified both ./aicos sync brain --text-only and full ./aicos sync brain complete successfully.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

The original provider hygiene issue no longer blocks sync. Full sync now reports success with 351 files scanned and daemon PG reindex completed.

## Next Step

Keep this closed unless EISDIR recurs with a new path; future GBrain work should stay behind provider hygiene boundaries.

## Trace Refs

- source_ref: `tools/gbrain/src/core/import-file.ts`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
