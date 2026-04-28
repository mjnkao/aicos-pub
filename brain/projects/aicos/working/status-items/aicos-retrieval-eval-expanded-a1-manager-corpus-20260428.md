# Status Item: aicos-retrieval-eval-expanded-a1-manager-corpus-20260428

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-eval-expanded-a1-manager-corpus-20260428`
Title: Expanded A1/human-manager retrieval eval corpus and HTTP runner
Last write id: `aicos-retrieval-eval-expanded-20260428`
Last updated at: `2026-04-28T06:23:24+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-retrieval-eval`
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

Added a stdlib-only HTTP MCP retrieval eval runner and expanded the corpus to 23 A1/human-manager questions. Latest run: top-3 20/23, top-5 23/23, errors 0. This is the regression gate before small search/ranking changes.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

AICOS search work should be eval-driven and lightweight for the small-team profile instead of adding graph/reranker/substrate complexity prematurely.

## Next Step

Use scripts/aicos-retrieval-eval before search changes. Investigate the three top-3 misses with direct-read nudges and current controlling status-item ranking, without adding heavy infrastructure.

## Trace Refs

- artifact_refs:
  - `scripts/aicos-retrieval-eval`
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
  - `brain/projects/aicos/evidence/research/aicos-gbrain-search-patterns-for-a1-eval-20260428.md`
- source_ref: `brain/projects/aicos/evidence/research/aicos-retrieval-eval-run-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
