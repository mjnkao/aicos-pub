# Status Item: aicos-mcp-token-scope-authorization-20260428

Status: closed
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-token-scope-authorization-20260428`
Title: Add token-label scope authorization for protected AICOS writes
Last write id: `20260428T072426Z-82fe65d7c2`
Last updated at: `2026-04-28T07:24:26+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-token-scope-authz`
Agent display name: `unknown`
Work type: `ops`
Work lane: `mcp-http-authz`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

AICOS HTTP daemon now authorizes read/write by token label in addition to token validity. Authenticated tokens can read by default. External/A1 tokens cannot write protected service scopes such as projects/aicos unless explicitly granted. Product families such as codex, claude-code, antigravity, and openclaw are not internal authority by default. A dedicated access label a2-core-c is configured locally for AICOS maintainer writes.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Actor normalization alone is not enough. AICOS still needs internal A1/A2 classification for records, but protected write authority must come from token/access policy rather than actor_family or client product name.

## Next Step

Use dedicated access labels such as a2-core-c for AICOS-maintainer sessions. Use AICOS_DAEMON_TOKEN_SCOPE_POLICY when per-company or per-project read/write grants are needed.

## Trace Refs

- source_ref: `codex-thread-20260428-token-scope-authz`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
