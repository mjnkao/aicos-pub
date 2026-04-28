# Status Item: AICOS-OPTION-C-TRANSITION-CHECKLIST

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-OPTION-C-TRANSITION-CHECKLIST`
Title: Use Option C transition checklist to sequence AICOS modularization
Last write id: `20260428T044420Z-47d99c9ad6`
Last updated at: `2026-04-28T04:44:20+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-phase-0-5`
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

The Option C transition checklist now includes Phase 0.5 to stabilize the current operating surface before deeper modularization. A1 agents are expected to use the HTTP daemon path for AICOS-facing reads and writes so MCP friction stays visible; only A2-Core-R and A2-Core-C may fall back to direct file writes when HTTP MCP is genuinely blocked.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Lock the stabilization-first rule into AICOS working state so future architecture work does not hide MCP friction behind direct markdown edits.

## Next Step

Run Phase 0.5 first: verify Codex, Claude Code, Claude Desktop, Antigravity, and OpenClaw can all connect through HTTP MCP, read the required surfaces, and write semantic updates without direct markdown fallback.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`
  - `AGENTS.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
