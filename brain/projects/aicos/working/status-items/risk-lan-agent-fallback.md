# Status Item: RISK-LAN-AGENT-FALLBACK

Status: open
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `RISK-LAN-AGENT-FALLBACK`
Title: LAN agents have no fallback when daemon is down (complete MCP failure for remote machines)
Last write id: `20260423T042911Z-c0f487118b`
Last updated at: `2026-04-23T04:29:11+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `claude-code-ops-20260423-infra`
Agent display name: `unknown`
Work type: `ops`
Work lane: `concurrency-safety`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

aicos_mcp_http_first.py (with stdio fallback) only runs on the AICOS host machine. LAN agents connect via: claude mcp add --transport http aicos http://192.168.1.X:8000/mcp — HTTP only, no fallback. When daemon crashes or restarts (LaunchAgent ThrottleInterval=10s), all LAN agents lose MCP access completely for ~10s. During a daemon restart triggered by crash, agents may be mid-task and lose context. Compound risk: if daemon crashes due to concurrent write contention (file lock bug), all LAN agents go blind simultaneously.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Identified during 10-agent LAN concurrency analysis. LaunchAgent auto-restarts daemon but 10s blind window affects all remote agents simultaneously — worse than single-agent downtime.

## Next Step

Options (pick one): (1) Add health-check retry loop in HTTP transport clients — retry up to 30s before declaring failure; (2) Document a secondary daemon URL fallback for LAN agents (e.g. configure two daemon instances on different ports); (3) Add /mcp endpoint graceful drain — daemon signals shutdown via SSE before stopping so clients can retry. Minimal viable: option 1, retry loop in aicos_mcp_http_first.py extended for LAN use.

## Trace Refs

- artifact_refs:
  - `integrations/local-mcp-bridge/aicos_mcp_http_first.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
