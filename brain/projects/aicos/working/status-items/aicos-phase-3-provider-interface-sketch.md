# Status Item: AICOS-PHASE-3-PROVIDER-INTERFACE-SKETCH

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-PHASE-3-PROVIDER-INTERFACE-SKETCH`
Title: Phase 3 provider interface sketch completed
Last write id: `phase-3-provider-sketch-status-20260428`
Last updated at: `2026-04-28T05:51:34+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-phase-3-provider-sketch`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-phase-3-provider-interfaces`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Sketched minimal provider slots for retrieval, context store, jobs/maintenance, auth/audit, connector/ingestion, and relation/graph without adding runtime code or a plugin framework.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Option C needs provider boundaries, but AICOS should avoid self-building a broad platform before real variation and evals justify it.

## Next Step

Use the sketch to guide small implementation hygiene: centralize MCP schema/constants and reduce daemon/stdio drift before building provider adapters.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-phase-3-provider-interface-sketch-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
