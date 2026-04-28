# Status Item: ARCH-R-09

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-09`
Title: Status item type guide and soft validation
Last write id: `20260421T153638Z-0454823ed0`
Last updated at: `2026-04-21T15:36:38+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-c-20260421-item-4-5`
Agent display name: `A2-Core Codex`
Work type: `code`
Work lane: `aicos-mcp-query-status-items`
Coordination status: `completed`
Artifact scope: `MCP query/status item serving`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Resolved by adding status item type guidance, persisted type guidance in status item files, and MCP-level soft warnings when item_type appears suspicious.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Agents need artifact-neutral guidance for coding, content, design, research, and mixed projects so filters do not become unreliable from wrong item_type values.

## Next Step

Agents should use aicos_update_status_item and review warnings before relying on item_type filters.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
