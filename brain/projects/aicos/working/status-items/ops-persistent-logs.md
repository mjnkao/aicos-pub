# Status Item: OPS-PERSISTENT-LOGS

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `OPS-PERSISTENT-LOGS`
Title: Persistent logs and basic log trimming implemented
Last write id: `20260423T085915Z-60d2d1f726`
Last updated at: `2026-04-23T08:59:15+00:00`

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

LaunchAgent installer now writes daemon/proxy/monitor logs to ~/Library/Logs/aicos instead of /tmp, and the new health monitor trims oversized log files in place so logs survive reboot and remain bounded. HTTPS proxy defaults were also made portable instead of hardcoded to one machine path.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Implemented as the minimum observability/logging hardening pass requested after daemon/search became usable.

## Next Step

Run scripts/aicos-install-launchagents outside the sandbox on the host machine to activate the new LaunchAgent plists and persistent log paths.

## Trace Refs

- artifact_refs:
  - `scripts/aicos-install-launchagents`
  - `integrations/mcp-daemon/aicos_health_monitor.py`
  - `integrations/mcp-daemon/aicos_https_proxy.py`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/mcp-daemon/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
