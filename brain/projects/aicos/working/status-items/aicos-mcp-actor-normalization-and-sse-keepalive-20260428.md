# Status Item: aicos-mcp-actor-normalization-and-sse-keepalive-20260428

Status: closed
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-actor-normalization-and-sse-keepalive-20260428`
Title: Normalize external MCP actors to A1 and reduce SSE false failures
Last write id: `20260428T071527Z-dffe87edda`
Last updated at: `2026-04-28T07:15:27+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-actor-sse-fix`
Agent display name: `unknown`
Work type: `ops`
Work lane: `mcp-http`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

External read actors may omit actor or send client names such as Antigravity; AICOS now normalizes them to service actor A1 while preserving client identity in agent_family. Write actor_role values from external client names also normalize to A1 and record the submitted value in markdown for audit. Read tool schemas expose actor as optional. SSE keepalive default is now 5 seconds and SSE close handling avoids noisy reset tracebacks. Smoke tests passed for tools/list schema, read with actor=Antigravity, read with actor omitted, write normalization, and SSE keepalive.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

AICOS still needs internal A1/A2 service actor classification for reads/writes, but external clients should not have to understand the A1/A2 naming model unless they maintain AICOS itself.

## Next Step

Ask Antigravity and other clients to reconnect or refresh tools/list so they drop any cached required actor schema. If Antigravity still reports SSE retry errors, capture whether it is using direct HTTP, HTTPS proxy, or stdio wrapper plus audit lines around the failure time.

## Trace Refs

- source_ref: `codex-thread-20260428-actor-sse-fix`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
