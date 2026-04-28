# Status Item: aicos-current-push-20260423

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-current-push-20260423`
Title: AICOS current implementation state prepared for git push
Last write id: `20260423T031025Z-c1bb4acc13`
Last updated at: `2026-04-23T03:10:25+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-a2-core-20260423-push-current-state`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-http-mcp-pg-search-rollout`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

AICOS self-brain, MCP daemon/search, HTTP MCP install docs, context registry, and coordination/status items have been updated for the current rollout state. Native Codex HTTP MCP can be tested against http://127.0.0.1:8000/mcp when daemon is running.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Human requested git push and AICOS MCP update for the current project state.

## Next Step

After push, continue by installing PostgreSQL/pgvector through Postgres.app, user-owned Homebrew, Docker/OrbStack, or a remote DSN if full hybrid search is needed on this standard Mac account.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/checkpoints/20260423t031015z-382bd9d480.md`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/codex/README.md`
  - `integrations/mcp-daemon/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
