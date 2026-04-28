# Status Item: AICOS-AUDIT-OBSERVABILITY-CLI

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-AUDIT-OBSERVABILITY-CLI`
Title: Add audit-log query surface for MCP activity
Last write id: `20260423T130150Z-0961137de7`
Last updated at: `2026-04-23T13:01:50+00:00`

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

Added ./aicos audit recent with token/agent/scope/lane filters and wired MCP request audit logging to JSONL for operational inspection.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Audit observability follow-up is now implemented at usable MVP level.

## Next Step

None.

## Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/kernel.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `<USER_HOME>/Library/Logs/aicos/mcp-audit.jsonl`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
