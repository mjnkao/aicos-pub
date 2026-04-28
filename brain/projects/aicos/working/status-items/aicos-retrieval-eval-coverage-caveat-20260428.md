# Status Item: aicos-retrieval-eval-coverage-caveat-20260428

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-eval-coverage-caveat-20260428`
Title: Retrieval eval coverage expanded with sample project project slice
Last write id: `codex-sample-retrieval-eval-20260428-1`
Last updated at: `2026-04-28T08:23:32+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-sample-retrieval-eval`
Agent display name: `Codex Desktop A2-Core`
Work type: `ops`
Work lane: `retrieval-eval`
Coordination status: `completed`
Artifact scope: `AICOS retrieval eval corpus and runner`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Expanded the retrieval eval corpus from 29 to 54 items: 25 AICOS, 28 Sample Project, and 1 mjnclaw smoke item. Runner now reports per-scope top3/top5/error metrics so aggregate success cannot hide sample project regressions. Latest run: all top3 53/54, top5 54/54, errors 0; AICOS top3/top5 25/25; sample project top3 27/28 and top5 28/28.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

The previous 29/29 result was mostly AICOS coverage with only sample project smoke coverage. Search/A1 retrieval changes now need a larger sample project regression slice because sample project is a bigger coding-heavy managed project.

## Next Step

For future search changes, run scripts/aicos-retrieval-eval --max-results 5 and inspect per-scope results for both projects/aicos and projects/sample-project.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
  - `scripts/aicos-retrieval-eval`
  - `brain/projects/aicos/evidence/research/aicos-phase-5-retrieval-runtime-reduction-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
