# Status Item: BUG-DAEMON-AUTH-TOKEN-EMPTY

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `BUG-DAEMON-AUTH-TOKEN-EMPTY`
Title: AICOS daemon LAN auth token risk resolved at minimum level
Last write id: `20260423T080639Z-40137ce315`
Last updated at: `2026-04-23T08:06:39+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-status-reconcile`
Agent display name: `unknown`
Work type: `ops`
Work lane: `security`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Runtime env now contains a non-empty AICOS_DAEMON_TOKEN, startup scripts source the env file, daemon refuses non-loopback/LAN binds without a token unless explicitly overridden, and install docs/env template describe token-protected LAN use. Local loopback connector behavior remains configurable separately from LAN exposure.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Claude Code flagged empty-token LAN write exposure. Codex applied the minimum security fix during the HTTP/embedding hardening pass and verified token-protected daemon health/tool calls.

## Next Step

For production/team use, add audit/session hardening later; do not expose 0.0.0.0 without AICOS_DAEMON_TOKEN.

## Trace Refs

- artifact_refs:
  - `.runtime-home/aicos-daemon.env`
  - `scripts/aicos-daemon-start`
  - `scripts/aicos-daemon-start.sh`
  - `integrations/mcp-daemon/aicos-daemon.env.example`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
