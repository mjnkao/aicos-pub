# Status Item: AICOS-LEARNING-LOOP-MVP

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-LEARNING-LOOP-MVP`
Title: Add lightweight proactive learning loop for A1/A2 agent friction feedback
Last write id: `20260423T140526Z-e4edc31672`
Last updated at: `2026-04-23T14:05:26+00:00`

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

Startup bundle and project health now expose feedback_loop nudges, write results can emit feedback_nudge at session-close boundaries, feedback taxonomy is broader, and CLI now supports feedback summary aggregation.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

This delivers a lightweight pull-based learning loop without adding a heavy scheduler or survey subsystem.

## Next Step

Monitor real feedback usage and promote repeated patterns into status items, policy candidates, or tool candidates.

## Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/kernel.py`
  - `<AICOS_PRIVATE_REPO>/docs/install/AICOS_MCP_WRITE_COOKBOOK.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
