# Status Item: aicos-search-eval-two-project-regression-gate-20260428

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-search-eval-two-project-regression-gate-20260428`
Title: Require AICOS and sample project eval before search/A1 retrieval changes
Last write id: `20260428T102745Z-9c47e667e7`
Last updated at: `2026-04-28T10:27:45+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `aicos-checklist-autopilot-20260428`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-checklist-autopilot`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added a built-in regression gate to scripts/aicos-retrieval-eval: --gate enforces required scopes (projects/aicos + projects/sample-project) plus minimum hit-rate thresholds and exits non-zero on regression.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

none

## Next Step

Keep the eval corpus up to date when real A1 misses appear; avoid heavier infra unless repeated misses justify it.

## Trace Refs

- source_ref: `scripts/aicos-retrieval-eval`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
