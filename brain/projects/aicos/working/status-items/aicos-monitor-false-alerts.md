# Status Item: AICOS-MONITOR-FALSE-ALERTS

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-MONITOR-FALSE-ALERTS`
Title: Fix false/noisy monitor alerts when MCP runtime remains usable
Last write id: `20260423T162532Z-7644a85947`
Last updated at: `2026-04-23T16:25:32+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-runtime-hardening`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Resolved. /health no longer crashes when PG index stats are on an aborted transaction, and monitor alerting now opens one outage alert per failure episode, resets on recovery, and stops repeating every cycle by default.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Monitor was repeatedly reporting daemon failures while MCP tool traffic still worked because /health could fail internally on PG index_stats and the monitor treated each cycle as a repeatable alert opportunity.

## Next Step

Keep monitor enabled in lightweight mode. Revisit only if operator wants stricter alerting or external monitoring integration.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_health_monitor.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/engine.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
