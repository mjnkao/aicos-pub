# Status Item: aicos-search-eval-quality

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-search-eval-quality`
Title: Evaluate retrieval quality of hybrid search vs FTS on real AICOS queries
Last write id: `20260428T075745Z-847c57a37a`
Last updated at: `2026-04-28T07:57:45+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-checklist-5-step`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-checklist-5-step`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Retrieval eval corpus and HTTP runner are in place. Latest run after strategic-product anchor tuning: 29 items, top-3 29/29, top-5 29/29, errors 0. This resolves the initial missing-eval-quality item; ongoing search work continues under Phase 5 and feedback-to-eval loop items.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

The requested compact evaluation set exists and is now being used as a regression check before search/ranking changes.

## Next Step

Keep scripts/aicos-retrieval-eval as a regression gate. Do not add graph/reranker/provider complexity unless future eval misses prove it is needed.

## Trace Refs

- source_ref: `scripts/aicos-retrieval-eval`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
