# Status Item: RISK-PG-TRUTH-STORE

Status: deferred
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `RISK-PG-TRUTH-STORE`
Title: Should working state (handoff, status items) move to PostgreSQL as truth store?
Last write id: `20260428T043101Z-6c1acfc20d`
Last updated at: `2026-04-28T04:31:01+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-option-c-cleanup`
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

Deferred under the current Option C north-star. The active direction keeps markdown brain truth and treats retrieval/runtime stores as provider-backed substrate. Moving working state to PostgreSQL as truth would be a larger product-boundary change that conflicts with the current semantic-core-first direction unless a future ADR explicitly reopens it.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

Option C now frames AICOS as semantic core + runtime services + provider layers. Current priority is modularizing the substrate boundary, not replacing markdown truth for working state.

## Next Step

Do not pursue PG-as-truth while the current north-star is active. Reopen only if future scaling evidence shows markdown truth is no longer viable even after provider/profile modularization and bounded concurrency improvements.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
