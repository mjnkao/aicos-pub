# Status Item: aicos-phase-5-retrieval-runtime-reduction

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-phase-5-retrieval-runtime-reduction`
Title: Improve A1 context search through eval-driven retrieval work
Last write id: `20260428T154359Z-c0a8a64733`
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

Completed the relation/ref hygiene sub-step for Phase 5: source_ref is now path-only in docs/schema guidance, scope_refs/session_refs are supported by Trace Ref parsing and semantic writes, and AICOS/sample project relation audits report 0 broken source refs. Retrieval/runtime expansion remains deferred until real misses justify it.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

This preserves the GBrain-inspired adjacency direction without adding a heavy graph, reranker, or new read tool prematurely.

## Next Step

Continue feedback-to-eval and relation audit regression. Only consider aicos_get_related_context or derived link graph after repeated adjacency misses appear in A1 feedback/eval.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-thin-relation-audit-measurement-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
