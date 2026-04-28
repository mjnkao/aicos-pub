# Status Item: BUG-SUMMARY-LIMIT-INCONSISTENT

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `BUG-SUMMARY-LIMIT-INCONSISTENT`
Title: MCP summary limit inconsistency resolved
Last write id: `20260423T064921Z-3282bf227e`
Last updated at: `2026-04-23T06:49:21+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `mcp-write-ux`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Standardized the write-serving summary policy behind constants instead of scattered 500/600/700-char values. General summary fields use SUMMARY_MAX_LEN=1500 and handoff uses HANDOFF_SUMMARY_MAX_LEN=1200, making future changes explicit and auditable.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

Implemented together with UX-MCP-SUMMARY-CHAR-LIMIT by Codex on 2026-04-23.

## Next Step

If agents still need deeper technical bodies, revisit OQ-MCP-DETAIL-FIELD after observing real use with 1500-char summaries.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
