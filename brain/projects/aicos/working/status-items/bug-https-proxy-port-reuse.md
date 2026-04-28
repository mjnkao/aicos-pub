# Status Item: BUG-HTTPS-PROXY-PORT-REUSE

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `BUG-HTTPS-PROXY-PORT-REUSE`
Title: HTTPS proxy port reuse fixed
Last write id: `20260423T064824Z-9ede22ca85`
Last updated at: `2026-04-23T06:48:24+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `ops-stability`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added allow_reuse_address=True to the HTTPS proxy HTTPServer subclass, matching the daemon server. This avoids avoidable restart crashes from TIME_WAIT/port reuse after LaunchAgent or manual restarts.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Implemented by Codex during AICOS HTTP/embedding hardening pass on 2026-04-23.

## Next Step

Retest HTTPS proxy after the human runs LaunchAgent install outside sandbox; proxy code path itself is fixed.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_https_proxy.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
