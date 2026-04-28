# Status Item: aicos-strategic-review-search-learning-loop-20260428

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-strategic-review-search-learning-loop-20260428`
Title: Strategic CTO/CEO review search pass and learning-loop assessment
Last write id: `aicos-strategic-search-learning-loop-20260428-v2`
Last updated at: `2026-04-28T06:59:15+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-strategic-search-loop`
Agent display name: `unknown`
Work type: `ops`
Work lane: `retrieval-eval`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added strategic CTO/CEO review intent support, five eval cases, strategic anchors, and a learning-loop assessment. Latest retrieval eval: 29 items, top-3 28/29, top-5 29/29, errors 0. CTO/CEO queries now nudge startup/handoff/status/health reads and retrieve architecture/product anchors.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

AICOS had enough raw context for CTO/CEO review but did not yet guide A1 reliably through role-aware strategic context. Search improvements should become feedback/eval-driven instead of one-off fixes.

## Next Step

Build a lightweight feedback-to-eval digest and keep scripts/aicos-retrieval-eval as the regression gate before future search/routing changes. Do not add graph/reranker/search-platform complexity unless eval misses prove it is needed.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-run-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
  - `docs/install/AICOS_QUERY_SEARCH_GUIDE.md`
- source_ref: `brain/projects/aicos/evidence/research/aicos-search-learning-loop-assessment-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
