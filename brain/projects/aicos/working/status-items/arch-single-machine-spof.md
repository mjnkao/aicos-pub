# Status Item: ARCH-SINGLE-MACHINE-SPOF

Status: open
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-SINGLE-MACHINE-SPOF`
Title: Single machine SPOF: entire team loses MCP when the AICOS host goes down or sleeps
Last write id: `20260423T045756Z-8026ffdab9`
Last updated at: `2026-04-23T04:57:56+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `claude-code-ops-20260423-infra`
Agent display name: `unknown`
Work type: `ops`
Work lane: `arch-review`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

All LAN agents depend on one Mac running Postgres.app + HTTP daemon. If the machine sleeps (lid close), crashes, or is offline: all LAN agents lose MCP access completely with no fallback. Local machine agent (Claude Code) falls back to stdio, but loses PG search quality. No redundancy, no failover, no secondary daemon. Current team size makes this acceptable short-term, but any growth makes it fragile. Postgres.app also does not auto-start if machine was off (only "Start at Login" which requires user session). Brain/ git repo has no automated push — if machine dies without recent push, recent brain state may be lost.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

Identified in CTO review 2026-04-23. Not a crisis today with one active user, but a strategic constraint that limits team growth and reliability SLA.

## Next Step

Human decision needed on acceptable reliability model: (1) Accept current SPOF — document it, ensure git push discipline for brain/; (2) Add a second read-only replica daemon on another machine; (3) Move to a cloud/VPS host for the daemon so it is always on. Recommend (1) for now with explicit git push automation (cron or LaunchAgent) as minimum mitigation.

## Trace Refs

- none

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
