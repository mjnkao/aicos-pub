# Status Item: aicos-retrieval-direct-read-nudges-human-manager-startup-20260428

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-direct-read-nudges-human-manager-startup-20260428`
Title: Direct-read nudges and human-manager startup retrieval pass
Last write id: `aicos-direct-read-nudges-human-manager-startup-20260428-v2`
Last updated at: `2026-04-28T06:43:14+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-direct-read-nudges`
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

Added direct_read_nudges for startup/project-discovery/current-work/next-work/coordination intents, PG project_registry shared search inclusion, current-control ranking boosts, and PG filtering for resolved/closed/stale/deferred status items. Expanded eval to 24 items. Latest result: top-3 23/24, top-5 24/24, errors 0. Human-manager startup query now nudges startup_bundle, handoff_current, status_items, project_health, and feedback_digest; handoff/current ranks #1.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Human managers commonly ask A1 to check project progress, active work, who is doing what, and what to do next. AICOS should guide A1 to direct current-control reads before broad search.

## Next Step

Keep using scripts/aicos-retrieval-eval before search changes. Next pass should focus on answer synthesis/playbook for A1 after it receives direct_read_nudges, not a heavier search engine.

## Trace Refs

- artifact_refs:
  - `scripts/aicos-retrieval-eval`
  - `docs/install/AICOS_QUERY_SEARCH_GUIDE.md`
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
- source_ref: `brain/projects/aicos/evidence/research/aicos-retrieval-eval-run-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
