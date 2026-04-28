# Status Item: aicos-active-priority-review-20260428

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-active-priority-review-20260428`
Title: Use active priority review to sequence near-term AICOS work
Last write id: `codex-active-priority-review-20260428`
Last updated at: `2026-04-28T09:04:18+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-active-priority-review`
Agent display name: `Codex Desktop A2-Core`
Work type: `planning`
Work lane: `portfolio-priority-review`
Coordination status: `completed`
Artifact scope: `AICOS active priority review`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Created a current priority review across active AICOS status items. Recommended order: P0 fix real MCP client/runtime blockers if present; otherwise P1 GBrain-inspired search schema projection and retrieval recipes; then P3 MCP schema/constants dedupe; then P2 module inventory/provider boundary; then reliability/concurrency and dashboard work later.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

AICOS has many active status items. The project needs a clear sequence so agents do not drift into dashboard, graph, or reliability overbuild before search/retrieval and schema/provider boundaries are stable.

## Next Step

Default next work: start P1.1 search schema projection and P1.2 retrieval recipes unless a fresh P0 client failure blocks current A1 usage.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-active-priority-review-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-gbrain-inspired-search-checklist-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
