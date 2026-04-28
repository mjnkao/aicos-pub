# Status Item: OPS-NO-MONITORING

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `OPS-NO-MONITORING`
Title: Minimum local health monitoring implemented
Last write id: `20260423T085929Z-dbd9ba2ffb`
Last updated at: `2026-04-23T08:59:29+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-ops-hardening`
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

Added a local health monitor that checks daemon /health, writes a status JSON, sends macOS notifications after repeated failures, and is installed by the LaunchAgent installer as ai.aicos.health-monitor. This gives AICOS a minimum viable local monitoring loop without external services.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Implemented as the minimum monitoring pass requested after daemon/search became operational and silent failures were identified as the most immediate ops gap.

## Next Step

Run scripts/aicos-install-launchagents outside the sandbox on the host machine to activate the monitor LaunchAgent and verify ~/Library/Application Support/aicos/health-status.json updates every 60 seconds.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_health_monitor.py`
  - `scripts/aicos-install-launchagents`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/mcp-daemon/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
