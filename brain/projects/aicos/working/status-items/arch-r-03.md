# Status Item: ARCH-R-03

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-03`
Title: Truth store strategy ADR accepted
Last write id: `20260423T015947Z-ea3304173e`
Last updated at: `2026-04-23T01:59:47+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-20260423-roadmap-reconcile`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-roadmap-reconciliation`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

ADR-001 now defines markdown/agent-repo as current truth, MCP as semantic mutation boundary, and DB/FTS/vector/cache/daemon as serving/index layers until explicit migration triggers are met.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Pass 4 created accepted ADR-001 and answered the requested truth-store, GBrain, migration trigger, and concurrency boundaries.

## Next Step

Keep ADR-001 current when DB-backed write paths or remote/server MCP become authoritative.

## Trace Refs

- none

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
