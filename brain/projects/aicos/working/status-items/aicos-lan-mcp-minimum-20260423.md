# Status Item: aicos-lan-mcp-minimum-20260423

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-lan-mcp-minimum-20260423`
Title: Minimal LAN MCP access hardened
Last write id: `20260423T020430Z-c3ecc58173`
Last updated at: `2026-04-23T02:04:30+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-20260423-roadmap-reconcile`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-lan-mcp-minimum`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

HTTP daemon now refuses non-loopback bind without token unless explicitly overridden. Docs describe minimum LAN rollout and token-protected doctor/health checks.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

User approved doing multi-machine/team MCP at the minimum level needed for people on a LAN to read/write through one AICOS control-plane server.

## Next Step

Run a real LAN usage test from another machine/client and then decide whether session/audit/deployment hardening is needed.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `integrations/mcp-daemon/README.md`
  - `integrations/local-mcp-bridge/install/AICOS_MCP_AGENT_INSTALL.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
