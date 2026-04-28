# ADR-001: Truth Store Strategy

Status: accepted
Date: 2026-04-22

## Context

AICOS is moving from local restructuring into multi-agent, multi-project use.
Markdown files currently hold canonical truth, working state, evidence,
handoff, task state, status items, and policy. MCP read/write tools provide a
semantic control plane over those files. PostgreSQL/GBrain style stores are
serving/index substrates.

The main risk is letting indexes, daemon cache, or concurrent file writes become
implicit truth without a clear decision.

## Decision

Markdown under `brain/` and actor/task material under `agent-repo/` remain the
authoritative source of truth for the current phase.

Database, FTS, vector, cache, daemon, and generated serving outputs are
serving/index layers only. They may accelerate query, summarize context, and
expose freshness metadata, but they must not silently replace source truth.

Semantic MCP write tools are the preferred mutation boundary for AICOS-facing
continuity writes. They validate intent, require actor identity, map writes to
owned lanes, and format records. Direct A2 repo edits remain allowed when A2 is
maintaining AICOS itself.

## Concurrency Policy

- Project truth changes should prefer small, lane-owned files over appending to
  broad shared files.
- Status lifecycle changes belong in `working/status-items/`.
- Task continuation belongs in `working/task-state/`.
- Compact handoff belongs in `working/handoff/current.md`.
- Evidence/checkpoint material belongs in `evidence/`.
- Feedback/improvement signals belong in `working/feedback/`.
- Generated indexes in `serving/` can be regenerated from truth files.

If two agents need to edit the same authority file or same code worktree at the
same time, they must coordinate through handoff, task-state, status-item, or
human-approved takeover before writing.

## Migration Trigger

AICOS should consider a structured authoritative store only when at least one is
true:

- multiple agents regularly conflict on the same authority files;
- project registry, status items, feedback, or task state require atomic
  transactions;
- remote/server MCP becomes the normal team path rather than optional LAN mode;
- audit/event history needs queryable append-only guarantees beyond markdown;
- generated indexes cannot be kept fresh enough from file mtimes and write
  hooks.

Until then, structured stores remain indexes and caches.

## Consequences

- Source refs and freshness metadata are mandatory for serving/index outputs.
- Query results are references and compact summaries, not promoted truth.
- MCP daemon/HTTP mode must expose health/freshness and degrade gracefully.
- Any future DB-backed write path needs a new ADR or explicit update to this
  ADR before becoming authoritative.
