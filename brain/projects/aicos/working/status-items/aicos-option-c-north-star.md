# Status Item: AICOS-OPTION-C-NORTH-STAR

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-OPTION-C-NORTH-STAR`
Title: Use Option C architecture north-star to guide future AICOS modularization
Last write id: `20260428T042843Z-69b0279234`
Last updated at: `2026-04-28T04:28:43+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-option-c-north-star`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-architecture-option-c`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

AICOS now has a clearer Option C north-star with deployment profiles framed as solo, small-team, company-100, and future enterprise. The current GBrain + PG hybrid + HTTP MCP + team auth path is treated as a substrate bundle inside the small-team profile, not as a profile name itself.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Operator clarified that profile naming should represent company/team scale, while gbrain-substrate is an implementation choice for the current small-team deployment path.

## Next Step

Use this naming consistently in future architecture and migration passes, then build the concrete module inventory and transition plan against the corrected profile model.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
