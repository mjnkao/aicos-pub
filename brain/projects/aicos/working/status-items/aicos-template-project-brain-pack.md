# Status Item: aicos-template-project-brain-pack

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-template-project-brain-pack`
Title: Create first-class template/sample project brain pack
Last write id: `20260428T145634Z-066fa32c85`
Last updated at: `2026-04-28T14:56:34+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-template-pack-and-loop`
Agent display name: `Codex Desktop`
Work type: `code`
Work lane: `brain-modularity`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
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
  "identity_private": {
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

Created a first-class reusable project brain pack under brain/shared/templates/project-brain-pack with a manifest, README, and synthetic sample-project brain skeleton covering canonical profile, context ladder, current state/direction, handoff, open items/questions, status item, feedback lane, task-state lane, and evidence lane. No generator or public export refactor was added.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

This is the minimal modularity step after AICOS_BRAIN_ROOT: new projects can copy or mount a clean brain shape without copying private project context.

## Next Step

Use this pack as the starting point for future project intake/import docs. Add a generator only after repeated real project creation makes manual copy error-prone.

## Trace Refs

- source_ref: `brain/shared/templates/project-brain-pack/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
