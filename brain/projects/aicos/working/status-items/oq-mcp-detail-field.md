# Status Item: OQ-MCP-DETAIL-FIELD

Status: open
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `OQ-MCP-DETAIL-FIELD`
Title: Should status items have a separate detail field (3000 chars) for technical depth?
Last write id: `20260423T043446Z-db789decaf`
Last updated at: `2026-04-23T04:34:46+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `claude-code-ops-20260423-infra`
Agent display name: `unknown`
Work type: `ops`
Work lane: `mcp-write-ux`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

After increasing summary limit (UX-MCP-SUMMARY-CHAR-LIMIT), should we also add an optional detail field? Design: summary=compact always-visible digest (1500 chars), detail=optional technical depth (3000 chars) only loaded on demand. Benefit: startup bundle and status digest stay compact; Codex can read detail when it needs to act on a specific item. Cost: MCP schema change, write tool update, reader update. Alternative: just use artifact_refs to point to a file in brain/evidence/research/ for deep technical items — no schema change needed, works today.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

Open question before investing in Option B (add detail field). The artifact_refs workaround may be good enough, making a detail field unnecessary complexity.

## Next Step

Human decision: (1) artifact_refs workaround is sufficient — close this item; (2) add detail field — Codex implements after UX-MCP-SUMMARY-CHAR-LIMIT is done. Recommend: try artifact_refs first for 2-3 real technical items, decide based on actual friction.

## Trace Refs

- none

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
