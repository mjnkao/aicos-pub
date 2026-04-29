# Status Item: AICOS-BRAIN-STATUS-PG-STALE-FALSE-SIGNAL

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-BRAIN-STATUS-PG-STALE-FALSE-SIGNAL`
Title: brain status can report PG index stale while daemon health and query are healthy
Last write id: `20260428T120647Z-b030b95f30`
Last updated at: `2026-04-28T12:06:47+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-p0-stabilization`
Agent display name: `Codex Desktop`
Work type: `ops`
Work lane: `aicos-runtime-provider-hygiene`
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

Resolved by changing brain status freshness to prefer PG latest_source_mtime for index freshness and missing_or_stale_embeddings for embedding freshness. Verified ./aicos brain status now reports GBrain sync success/fresh (full), PG index available/fresh, embedding freshness fresh, coverage 1.0, missing/stale embeddings 0.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

The previous timestamp-only comparison could produce false stale alarms after rapid write/reindex cycles even when PG had seen the latest source files.

## Next Step

Keep closed unless brain status again disagrees with daemon health or retrieval behavior.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/kernel.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
