# Status Item: aicos-gbrain-full-sync-eisdir-runtime-cache

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-gbrain-full-sync-eisdir-runtime-cache`
Title: GBrain full sync can fail on Bun runtime cache EISDIR
Last write id: `20260428T120703Z-585c85de96`
Last updated at: `2026-04-28T12:07:03+00:00`

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

Reconfirmed and hardened. Full ./aicos sync brain now succeeds with 412 files scanned, 0 import errors, and daemon PostgreSQL reindex completed. The wrapper now separates GBRAIN_HOME from HOME, uses an isolated Bun install cache, and bootstraps GBrain node_modules only when missing.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

The recurring failure was Bun/runtime-cache related, not an AICOS brain markdown traversal error. Keeping GBrain config under GBRAIN_HOME preserves local PGLite state without forcing Bun to use the old .runtime-home/.bun cache.

## Next Step

Keep closed unless full sync fails again; if it recurs, capture the exact Bun module/cache path before changing importer logic.

## Trace Refs

- source_ref: `scripts/gbrain_local.sh`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
