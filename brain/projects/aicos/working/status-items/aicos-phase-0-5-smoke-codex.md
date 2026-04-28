# Status Item: AICOS-PHASE-0-5-SMOKE-CODEX

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-PHASE-0-5-SMOKE-CODEX`
Title: Phase 0.5 HTTP MCP smoke for codex
Last write id: `20260428T050128Z-a87b2ddaf4`
Last updated at: `2026-04-28T05:01:28+00:00`

## Actor Identity

Actor role: `A1`
Agent family: `codex`
Agent instance id: `phase-0-5-codex`
Agent display name: `unknown`
Work type: `ops`
Work lane: `intake`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A1`
Work context: ``

## Summary

HTTP MCP token path for codex can call tools/list, read startup bundle, and perform semantic status-item write during Phase 0.5 stabilization smoke.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Validate the client token path without direct markdown fallback.

## Next Step

Keep this token path in the compatibility matrix and investigate only if future real client usage diverges from this daemon-level smoke.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
