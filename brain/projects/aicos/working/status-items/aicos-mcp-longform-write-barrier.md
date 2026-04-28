# Status Item: AICOS-MCP-LONGFORM-WRITE-BARRIER

Status: open
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-MCP-LONGFORM-WRITE-BARRIER`
Title: Should AICOS provide a better MCP path for long-form architecture/product writes?
Last write id: `20260428T030703Z-6a1efcf1f1`
Last updated at: `2026-04-28T03:07:03+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-product-framing`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-mcp-ux-boundary`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

A2 could write architecture and product memos directly into AICOS truth surfaces, but an A1 or external agent in a similar situation may hit friction if MCP write surfaces remain better for compact updates than for long-form multi-file research and product framing passes. We should track how often agents hit this boundary, whether HTTP MCP can support the needed write shape cleanly, and what upgrade path reduces the gap without weakening AICOS authority or structure.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

Operator requested that we prioritize MCP HTTP reads/writes going forward so we surface the same friction A1 agents will hit. This question tracks whether AICOS needs stronger MCP support for long-form architecture/research writeback instead of relying on direct repo edits by maintainers.

## Next Step

Observe future A1/A2 cases that need long-form research/product/architecture writeback, record where MCP becomes awkward, and then decide whether to add a dedicated long-form memo/research write surface, template flow, or multi-file write helper.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
