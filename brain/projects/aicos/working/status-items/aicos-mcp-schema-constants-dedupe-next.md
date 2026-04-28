# Status Item: aicos-mcp-schema-constants-dedupe-next

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-schema-constants-dedupe-next`
Title: Centralize MCP tool schemas and shared constants before adding more tools
Last write id: `20260428T102751Z-6f00d661cb`
Last updated at: `2026-04-28T10:27:51+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `aicos-checklist-autopilot-20260428`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-checklist-autopilot`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Centralized the MCP tool schema definitions into packages/aicos-kernel/aicos_kernel/mcp_tool_definitions.py and moved the stdio bridge to consume it. The HTTP daemon now sources TOOLS from the same shared definitions before applying schema extensions; scripts/aicos-mcp-tool-schema-parity still reports zero mismatches.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

none

## Next Step

If needed later, delete the now-dead inline TOOLS literal block in integrations/mcp-daemon/aicos_mcp_daemon.py (kept temporarily to keep the diff low-risk).

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_tool_definitions.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
