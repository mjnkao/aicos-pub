# Status Item: aicos-strategic-review-search-learning-loop-20260428

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-strategic-review-search-learning-loop-20260428`
Title: Strategic CTO/CEO review search pass and learning-loop assessment
Last write id: `20260428T122144Z-b741473e94`
Last updated at: `2026-04-28T12:21:44+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-feedback-to-eval`
Agent display name: `Codex Desktop`
Work type: `code`
Work lane: `retrieval-eval`
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

Implemented the first lightweight feedback-to-eval loop: scripts/aicos-feedback-to-eval-digest reads working/feedback, summarizes actionable friction, detects candidate eval cases, and writes an evidence digest. Added feedback as a first-class PG context_kind projection so A1/A2 can retrieve actual feedback records through query. Added an auth/token health/eval feedback case to the retrieval corpus. Regression gate passes: 59 items, top3 57/59, top5 59/59, errors 0.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Search quality should improve from real A1/A2 friction instead of manual one-off fixes. This keeps the loop lightweight: digest and eval candidates only, no graph/reranker/new provider.

## Next Step

Continue using feedback digest before search changes. Add new eval cases only when feedback is actionable and not already covered; keep derived link graph deferred until repeated adjacency misses appear.

## Trace Refs

- source_ref: `scripts/aicos-feedback-to-eval-digest`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
