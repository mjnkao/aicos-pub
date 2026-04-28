# Status Item: AICOS-MCP-SSE-AUTH-INTEROP

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-MCP-SSE-AUTH-INTEROP`
Title: Design a safer SSE auth/interoperability path for clients that cannot send headers
Last write id: `20260423T130616Z-e2a40ef14c`
Last updated at: `2026-04-23T13:06:16+00:00`

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

Daemon health now exposes explicit auth capabilities and recommended client profiles. Claude Desktop same-machine interop is routed through the localhost HTTPS proxy; first-class non-local/headerless client interop is still unsolved.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Current pass reduced configuration ambiguity but did not replace the local-proxy workaround with a broader transport/session design.

## Next Step

Choose whether to keep the localhost HTTPS adapter as the only special-case path or design a first-class streamable HTTP/session bootstrap for clients that cannot set bearer headers.

## Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos_https_proxy.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
