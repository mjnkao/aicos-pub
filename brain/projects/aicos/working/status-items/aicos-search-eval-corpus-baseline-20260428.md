# Status Item: AICOS-SEARCH-EVAL-CORPUS-BASELINE-20260428

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-SEARCH-EVAL-CORPUS-BASELINE-20260428`
Title: Initial AICOS retrieval eval corpus and baseline completed
Last write id: `search-eval-baseline-status-20260428`
Last updated at: `2026-04-28T06:02:55+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-search-focus`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-search-focus`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Created a 10-item A1/A2 retrieval eval corpus and ran HTTP MCP baseline. Result after correcting startup work_type: top-3 hit 9/10, top-5 hit 10/10. Applied low-risk fixes by adding query guide A1 examples and registering artifact refs for A1-critical install/search guides.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

A1 search needs measured improvement; eval-driven work avoids adding heavy graph/reranker/provider complexity before knowing failure modes.

## Next Step

Next search pass should implement a small repeatable eval runner and decide whether query output should include direct-read suggestions for startup/handoff/status intents.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-retrieval-baseline-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
