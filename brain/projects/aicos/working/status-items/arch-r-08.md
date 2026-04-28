# Status Item: ARCH-R-08

Status: resolved
Item type: `tech_debt`
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-08`
Title: Query/status default excludes stale and closed items
Last write id: `20260421T153128Z-cf6d131b9e`
Last updated at: `2026-04-21T15:31:28+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-a2-core-20260421-next-three`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-mcp-context-hardening`
Coordination status: `completed`
Artifact scope: `ARCH-R-08 stale status filtering`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

aicos_get_status_items and aicos_query_project_context now hide stale/closed status items by default. Callers can pass include_stale/include-stale or explicit status_filter for audit/recovery use cases.

## Reason

Default hot context should not surface stale/closed status items to ordinary agents.

## Next Step

Monitor whether resolved items should also be hidden by default; current change intentionally targets stale/closed only.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
