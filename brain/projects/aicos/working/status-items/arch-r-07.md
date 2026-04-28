# Status Item: ARCH-R-07

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-07`
Title: Canonical docs (policy/contract/design) queryable via aicos_query_project_context
Last write id: `20260421T153638Z-7f7e705baa`
Last updated at: `2026-04-21T15:36:38+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-c-20260421-item-4-5`
Agent display name: `A2-Core Codex`
Work type: `code`
Work lane: `aicos-mcp-query-status-items`
Coordination status: `completed`
Artifact scope: `MCP query/status item serving`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Resolved by extending aicos_query_project_context with canonical, policy, and contract context_kinds. Project canonical docs, shared policies, and kernel contracts can now be queried without agents knowing exact paths first.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Implemented bounded markdown source collection for project canonical, shared policy, and kernel contract surfaces; updated MCP stdio schema and local MCP bridge contract.

## Next Step

Use context_kinds canonical, policy, or contract for targeted lookup; no further action for this item.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
