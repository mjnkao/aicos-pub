# Status Item: AICOS-PHASE-2-ACTOR-MODEL-NORMALIZATION

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-PHASE-2-ACTOR-MODEL-NORMALIZATION`
Title: Phase 2 actor model normalization baseline completed
Last write id: `phase-2-actor-model-status-20260428`
Last updated at: `2026-04-28T05:50:08+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-phase-2-boundary`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-phase-2-actor-model`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Separated AICOS-internal actor class, project-facing functional role, and service relationship role. Clarified that A1/A2 is AICOS service-boundary taxonomy, not a universal project role taxonomy.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

External projects should use AICOS as context/control-plane without being forced into AICOS internal maintenance labels; dashboards and providers must preserve role dimensions instead of flattening them.

## Next Step

Update future docs/examples to keep actor_role, agent_family, logical_role, work_type, and work_lane distinct; defer formal service_role field until real usage requires it.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-phase-2-actor-model-normalization-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
