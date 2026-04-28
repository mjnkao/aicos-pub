# Status Item: aicos-runtime-identity-schema-v06-20260428

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-runtime-identity-schema-v06-20260428`
Title: Promote runtime-relative identity to MCP write schema v0.6
Last write id: `codex-runtime-identity-schema-v06-20260428`
Last updated at: `2026-04-28T11:14:37+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-runtime-identity-schema-v06-20260428`
Agent display name: `unknown`
Work type: `code`
Work lane: `runtime-identity-schema`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop via aicos_local_private`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``
Runtime: `private-local-aicos`
MCP name: `aicos_local_private`
Agent position: `internal_agent`
Functional role: `AICOS maintainer`
Runtime identity map:
```json
{
  "identity_private": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "AICOS maintainer",
    "mcp_name": "aicos_local_private",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  },
  "identity_public": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "public AICOS runtime maintainer",
    "mcp_name": "aicos_railway_public",
    "project_scope": "projects/aicos",
    "runtime": "public-railway-aicos"
  }
}
```

## Summary

AICOS MCP write contract now requires structured runtime_context on all semantic writes and runtime_identity_map on A2 writes. Private and public docs/schema were updated so A1 stays lightweight while A2 cross-runtime work is auditable.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Free-form work_context was not enough to prevent A1/A2 confusion across private/local and public Railway AICOS runtimes.

## Next Step

Let A1 agents use the lightweight runtime_context path; watch feedback for friction before adding heavier identity fields to A1.

## Trace Refs

- source_ref: `docs/architecture/runtime-identity-schema.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
