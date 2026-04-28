# Status Item: UX-MCP-SUMMARY-CHAR-LIMIT

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `UX-MCP-SUMMARY-CHAR-LIMIT`
Title: MCP summary char limits increased
Last write id: `20260423T064851Z-1ad0c64a54`
Last updated at: `2026-04-23T06:48:51+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `mcp-write-ux`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented larger summary limits in MCP write serving: general summary fields now use 1500 chars and handoff summary uses 1200 chars. This removes the most common pressure that pushed agents to misuse handoff/task-state for detailed open-item bodies.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Implemented by Codex during AICOS HTTP/embedding hardening pass on 2026-04-23.

## Next Step

Use artifact_refs for long evidence; do not add an optional detail field until real post-change friction proves it is needed.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
