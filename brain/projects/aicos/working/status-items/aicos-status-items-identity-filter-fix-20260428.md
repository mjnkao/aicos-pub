# Status Item: aicos-status-items-identity-filter-fix-20260428

Status: closed
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-status-items-identity-filter-fix-20260428`
Title: Fix status-items read identity fields accidentally filtering results
Last write id: `20260428T075745Z-a65b887af4`
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

aicos_get_status_items no longer treats read identity fields work_lane and agent_family as implicit status item filters. Explicit filters are now status_work_lane_filter and status_agent_family_filter. Smoke test: read with work_lane=aicos-checklist-review returns open items; explicit status_work_lane_filter for that lane returns 0 as expected.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

A1 agents must be able to ask what is open in a project from their current lane without accidentally hiding most project status items.

## Next Step

Keep read identity fields separate from query filters in future MCP schema work.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
