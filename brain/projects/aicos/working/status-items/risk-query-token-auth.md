# Status Item: RISK-QUERY-TOKEN-AUTH

Status: resolved
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `RISK-QUERY-TOKEN-AUTH`
Title: Query-string token auth rejected for AICOS daemon
Last write id: `20260423T083300Z-a0c947b1b3`
Last updated at: `2026-04-23T08:33:00+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-query-token-reject`
Agent display name: `unknown`
Work type: `review`
Work lane: `mcp-daemon-security-review`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Human decided to reject Claude's query-token auth workaround. AICOS daemon authorization now accepts only Authorization bearer header or X-AICOS-Token again; `?token=` acceptance was removed from code. Local daemon logs that contained token-in-URL traces were also removed from the workspace.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

Query-string bearer secrets are not acceptable as a default or fallback auth path for AICOS control-plane traffic because they leak into URLs and logs too easily.

## Next Step

If a client cannot send auth headers during SSE bootstrap, solve that with a safer interoperability design rather than URL tokens.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `brain/projects/aicos/evidence/checkpoints/20260423t075745z-7e7f55ba2c.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
