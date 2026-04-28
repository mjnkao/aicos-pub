# Status Item: AICOS-LAN-SECURITY-HARDENING

Status: open
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-LAN-SECURITY-HARDENING`
Title: Harden LAN-facing AICOS MCP security beyond shared bearer token
Last write id: `20260423T130150Z-e8d0a9d606`
Last updated at: `2026-04-23T13:01:50+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-runtime-hardening`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Labeled client tokens, request audit JSONL, and optional IP/CIDR allowlist are now in place. LAN exposure is still MVP-level because transport, token model, and audit policy remain lightweight.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Initial hardening landed, but LAN security is not yet at stronger team-grade baseline.

## Next Step

Promote HTTPS/default secure path for non-local clients and define minimal auth/audit operating policy.

## Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/README.md`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos-daemon.env.example`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
