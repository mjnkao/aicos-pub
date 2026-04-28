# Status Item: BUG-PG-DSN-INCONSISTENCY

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `BUG-PG-DSN-INCONSISTENCY`
Title: PostgreSQL DSN inconsistency resolved
Last write id: `20260423T064747Z-c3684244ec`
Last updated at: `2026-04-23T06:47:47+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `ops-config`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Unified bootstrap, daemon start, LaunchAgent wrapper, and env template around postgresql://aicos:aicos@127.0.0.1:5432/aicos. The runtime env now carries the same DSN plus explicit PG connect/statement/lock timeouts so startup does not hang indefinitely on bad PG state or schema locks.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Implemented by Codex during AICOS HTTP/embedding hardening pass on 2026-04-23.

## Next Step

Keep Postgres.app as recommended no-sudo path for macOS standard accounts; use ./aicos brain status after changes to confirm PG freshness.

## Trace Refs

- artifact_refs:
  - `scripts/aicos-bootstrap-full`
  - `scripts/aicos-daemon-start`
  - `scripts/aicos-daemon-start.sh`
  - `integrations/mcp-daemon/aicos-daemon.env.example`
  - `packages/aicos-kernel/aicos_kernel/pg_search/config.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
