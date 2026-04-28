# Status Item: AICOS-FEEDBACK-CLOSURE-GATE

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-FEEDBACK-CLOSURE-GATE`
Title: Require feedback closure before session-close MCP writes
Last write id: `20260423T170248Z-b3fdf3c3c0`
Last updated at: `2026-04-23T17:02:48+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-learning-loop`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented feedback closure gating for session-close writes. Agents must record either a real feedback item or feedback_type=no_issue before completed/blocked checkpoint, completed/blocked/waiting task update, or completed/blocked/ready_for_next handoff writes. Error responses now include a quick no_issue example.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Learning loop prompts alone were too weak; agents could ignore them and never write back any feedback signal.

## Next Step

Watch real agent behavior. If this still proves too easy to skip, consider extending the same closure rule to more write boundaries later.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
  - `docs/install/AICOS_MCP_WRITE_COOKBOOK.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
