# Status Item: AICOS-THIN-RELATION-MODEL

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-THIN-RELATION-MODEL`
Title: Keep thin relation model audit-only until real adjacency misses justify a read tool
Last write id: `20260428T154359Z-a2fcc6cb41`
Last updated at: `2026-04-28T15:43:59+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-trace-ref-hygiene`
Agent display name: `Codex Desktop`
Work type: `code`
Work lane: `aicos-search-query-architecture`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `main`
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

Trace Ref hygiene pass completed. Added scope_refs and session_refs parsing/write support, clarified docs/contracts, moved existing symbolic refs out of source_ref, and re-ran relation audit. AICOS now has 49 source refs, 139 artifact refs, 2 session refs, and 0 broken source refs. sample project now has 109 artifact refs, 1 scope ref, and 0 broken source refs.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

The audit-only relation layer is now cleaner, but there is still no repeated A1 feedback showing adjacency misses that justify adding aicos_get_related_context.

## Next Step

Keep relation audit as a regression check. Do not add a related-context read surface until real A1 feedback/eval shows repeated adjacent-context misses.

## Trace Refs

- artifact_refs:
  - `.runtime-home/aicos/relations-index__projects__aicos.json`
  - `.runtime-home/aicos/relations-index__projects__sample-project.json`
- source_ref: `brain/projects/aicos/evidence/research/aicos-thin-relation-audit-measurement-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
