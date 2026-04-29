# Status Item: AICOS-CURRENT-MODULE-DECISION-INVENTORY

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-CURRENT-MODULE-DECISION-INVENTORY`
Title: Current module keep/reuse/migrate/retire inventory completed
Last write id: `20260428T161452Z-2a43d21061`
Last updated at: `2026-04-28T16:14:52+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-module-decision-inventory`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-product-architecture`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``
Runtime: `private-local-aicos`
MCP name: `aicos_http`
Agent position: `internal_agent`
Functional role: `AICOS maintainer`
Runtime identity map:
```json
{
  "identity_current": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "AICOS maintainer",
    "mcp_name": "aicos_http",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

## Summary

Created the concrete CTO decision inventory that maps current AICOS implementation surfaces to Keep/Core, Keep/Projection, Reuse/Wrap, Migrate Candidate, Defer, or Retire/No New Work decisions. The table identifies the current small-team provider bundle, code hotspots that must not gain broad responsibilities, execution order, and substrate-vs-core guardrails.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

The previous execution decision table was product-level; AICOS needed a module/surface-level table to guide implementation without drifting into dashboard, graph, PM-sync, or generic memory substrate work too early.

## Next Step

Use this inventory as the guardrail before new implementation work. Near-term next work should follow the execution order: boundary cleanup where drift exists, retrieval quality/eval loop, runtime/security hardening for wider team use, project intake path, then dashboard/PM integration contract.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-execution-decision-table-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-phase-1-module-inventory-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-module-inventory-provider-boundary-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
- source_ref: `brain/projects/aicos/evidence/research/aicos-current-module-decision-inventory-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
