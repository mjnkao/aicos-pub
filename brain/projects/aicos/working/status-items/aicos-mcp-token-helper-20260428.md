# Status Item: aicos-mcp-token-helper-20260428

Status: closed
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-token-helper-20260428`
Title: Add quick command for creating labeled MCP tokens
Last write id: `20260428T080858Z-83fa7b526e`
Last updated at: `2026-04-28T08:08:58+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-token-eval-coverage`
Agent display name: `unknown`
Work type: `ops`
Work lane: `mcp-token-and-eval-coverage`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added ./aicos mcp token create/list. The create command updates .runtime-home/aicos-daemon.env and .runtime-home/aicos-daemon-token-registry.json, supports external/client tokens by default, --internal maintainer access labels, optional read/write scope policy grants, and prints the restart command. Token list shows labels, masked tokens, assignments, and effective rights.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

New A1/A2 clients should not require hand-editing env token strings and registry JSON. Token label remains an access subject, not agent_family.

## Next Step

Use ./aicos mcp token create <label> for new A1 clients, and ./aicos mcp token create <access-label> --internal only for AICOS maintainer access.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/kernel.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
