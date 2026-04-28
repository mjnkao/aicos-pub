# AICOS Option C Transition Checklist

Status: execution checklist  
Date: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Turn the Option C north-star into a concrete execution checklist so future
passes can move from architecture debate into implementation without drifting.

This checklist assumes the current direction remains:

- AICOS owns semantic/control-plane behavior;
- substrate concerns become more modular and more reusable;
- current stack is treated as the first real implementation bundle for the
  `small-team` profile;
- future dashboard/PM integrations should sit on top of AICOS control-plane
  behavior, not replace it.

## Phase 0 — Lock The Direction

### Must be true

- [ ] The product framing note remains the reference for "what AICOS is for".
- [ ] The Option C north-star remains the reference for "how AICOS should be
      structured".
- [ ] The execution decision table remains the reference for
      keep/reuse/migrate/retire decisions.

### Deliverables

- [ ] Keep `current-state.md`, `current-direction.md`, and `handoff/current.md`
      aligned with the north-star.
- [ ] Reject or defer architectural proposals that collapse AICOS into either:
      - a PM tool clone;
      - a generic memory/search product;
      - a single fixed implementation stack.

## Phase 0.5 — Stabilize The Current Operating Surface

Goal: make the current stack stable enough to keep using, observing, and
learning from real agent behavior before deeper modularization work.

### Operating rule

- [ ] Treat HTTP daemon MCP as the default AICOS interaction path.
- [ ] Require A1 agents to read and write AICOS-facing context/control-plane
      state through the HTTP daemon only.
- [ ] Disallow direct markdown writeback for A1 agents, even as a convenience
      fallback.
- [ ] Allow direct file-write fallback only for `A2-Core-R` and `A2-Core-C`
      when MCP HTTP is genuinely blocked or when they are restructuring AICOS
      internals directly.
- [ ] Keep even A2-Core on HTTP MCP by default, so friction is discovered
      early instead of hidden behind direct edits.

### Stabilization checklist

- [ ] Run a connectivity sanity pass for the main clients:
      - Codex Desktop
      - Claude Code
      - Claude Desktop
      - Antigravity
      - OpenClaw / mjnclaw
- [ ] Verify that each client can:
      - connect
      - read startup bundle
      - read handoff/status/query surfaces
      - write semantic updates
- [ ] Review read/write friction around:
      - actor identity requirements
      - `mcp_contract_ack`
      - feedback closure
      - long-form write ergonomics
      - error-message quality
- [ ] Review search/runtime stability around:
      - daemon health
      - stale/freshness behavior
      - embedding coverage
      - rate-limit/retry behavior
- [ ] Review monitor/ops noise and remove false-alert behavior where possible.
- [ ] Keep a client compatibility matrix current as a first-class operating
      artifact.

### Concrete outputs

- [ ] One stabilization pass note for the current operating surface
- [ ] One client compatibility matrix for the HTTP daemon path
- [ ] One shortlist of MCP friction items that should be fixed before deeper
      modularization work

## Phase 1 — Module Inventory

Goal: classify the current repo into semantic core, runtime services,
providers, profile-specific concerns, and transitional legacy.

### Checklist

- [ ] Inventory AICOS code modules under `packages/aicos-kernel/`,
      `integrations/`, `serving/`, and `backend/`.
- [ ] Classify each module as one of:
      - semantic core
      - runtime service
      - provider implementation
      - deployment/profile concern
      - migration/legacy residue
- [ ] Mark each module with a decision:
      - keep
      - refactor behind boundary
      - migrate toward provider layer
      - retire / stop growing

### Concrete outputs

- [ ] One module inventory note
- [ ] One keep/reuse/migrate/retire matrix at code/module level
- [ ] One shortlist of modules that should not gain new responsibilities until
      boundaries are cleaned

## Phase 2 — Extract Semantic Core Boundaries

Goal: make it obvious what AICOS owns regardless of substrate choice.

### Checklist

- [ ] Formalize semantic core boundaries around:
      - authority model
      - object model
      - coordination semantics
      - read/write contracts
- [ ] Normalize the actor model so `A1` / `A2` is treated as AICOS-internal
      maintenance taxonomy, not the universal role taxonomy for every project
      using AICOS.
- [ ] Separate at least three role dimensions clearly:
      - AICOS-internal actor class
      - project-facing functional role
      - service role (`internal actor`, `external actor`, equivalent)
- [ ] Identify which current modules are the de facto semantic core today.
- [ ] Reduce direct coupling from semantic logic into PG/GBrain/search-specific
      assumptions.

### Concrete outputs

- [ ] Core boundary note or ADR
- [ ] Actor model normalization note
- [ ] Refactor map for semantic core extraction
- [ ] List of invariants that future providers must never violate

## Phase 3 — Define Provider Interfaces

Goal: make substrate replacement or reuse possible without product drift.

### Checklist

- [ ] Define a minimal Retrieval Provider boundary
- [ ] Define a minimal Memory / Context Store Provider boundary
- [ ] Define a minimal Jobs / Maintenance Provider boundary
- [ ] Define a minimal Auth / Audit Provider boundary
- [ ] Keep Relation / Graph Provider optional and explicitly second-wave

### Constraints

- [ ] Do not over-abstract before real variation is needed
- [ ] Do not build adapters for every product immediately
- [ ] Start with the current stack as the first provider bundle

### Concrete outputs

- [ ] Interface sketch or contract note
- [ ] First mapping of current implementation to provider slots

## Phase 4 — Formalize Profiles

Goal: stop treating current deployment behavior as one implicit stack.

### Profile checklist

- [ ] Define `solo` profile clearly
- [ ] Define `small-team` profile clearly
- [ ] Define `company-100` profile clearly
- [ ] Keep `enterprise` as future target, not near-term build scope

### Current-stack checklist

- [ ] Document the current implementation as the first concrete bundle for the
      `small-team` profile:
      - markdown truth
      - GBrain sync/import
      - PG hybrid retrieval
      - HTTP MCP
      - token auth
      - background embedding/freshness path

### Concrete outputs

- [ ] Profile matrix
- [ ] Required vs optional capabilities per profile
- [ ] Which providers each profile expects

## Phase 5 — Retrieval/Runtime Reduction Pass

Goal: reduce custom substrate growth first where AICOS is least differentiated.

### Checklist

- [ ] Build AICOS retrieval eval corpus
- [ ] Benchmark markdown-direct vs FTS vs hybrid
- [ ] Review current chunking/summary behavior
- [ ] Review doctor/verify/freshness loop gaps
- [ ] Decide what retrieval/runtime logic stays custom vs gets wrapped or
      replaced

### Concrete outputs

- [ ] Eval corpus
- [ ] Benchmark report
- [ ] Retrieval/runtime refactor recommendation

## Phase 6 — Human + AI Coworker Model

Goal: prepare for dashboard and PM-tool integration without turning AICOS into
a PM clone.

### Checklist

- [ ] Define task/coworker model explicitly
- [ ] Define ownership model for humans and agents
- [ ] Define takeover / handoff-ready / blocked-by-human / blocked-by-agent
      semantics
- [ ] Define the minimum operational read surfaces needed for a dashboard:
      - active workers
      - active lanes
      - takeover-ready items
      - human attention queue
      - project board summary

### Concrete outputs

- [ ] Human+AI coworker model note
- [ ] Dashboard-facing read-surface proposal

## Phase 7 — Plane / ClickUp Integration Contract

Goal: integrate with shared task tools without surrendering AICOS control-plane
identity.

### Checklist

- [ ] Decide the sync authority model:
      - AICOS-first
      - PM-tool-first
      - hybrid
- [ ] Define which task fields belong to AICOS
- [ ] Define which task fields can live in Plane/ClickUp only
- [ ] Define sync conflict rules
- [ ] Define human-visible activity model for AI coworkers

### Concrete outputs

- [ ] PM integration contract note
- [ ] First target integration shortlist (Plane / ClickUp)

## Phase 8 — Company / Workspace / Project Packs

Goal: make AICOS adaptable across many companies without product forks.

### Checklist

- [ ] Identify what belongs in company pack
- [ ] Identify what belongs in workspace pack
- [ ] Identify what belongs in project pack
- [ ] Keep packs lightweight and configuration-like at first

### Concrete outputs

- [ ] Pack model note
- [ ] First pack schema draft

## Items Already Deferred Or Intentionally Not Pursued Right Now

- [ ] Keep `RISK-PG-TRUTH-STORE` deferred under current Option C direction.
- [ ] Do not introduce heavy graph truth or page-centric universal schema.
- [ ] Do not turn AICOS into a PM tool clone.
- [ ] Do not build multi-provider support broadly before the first provider
      boundaries are proven useful.

## Suggested Execution Order

1. Phase 0.5 — Stabilize the current operating surface
2. Phase 1 — Module inventory
3. Phase 2 — Semantic core boundaries
4. Phase 3 — Provider boundaries
5. Phase 4 — Profile formalization
6. Phase 5 — Retrieval/runtime reduction pass
7. Phase 6 — Human+AI coworker model
8. Phase 7 — PM tool integration contract
9. Phase 8 — Company/workspace/project packs

## Final Rule

Every future implementation pass should be explainable in one of two ways:

1. it strengthens AICOS semantic/control-plane ownership, or
2. it reduces duplicated substrate work without weakening AICOS semantics.

If a proposed change does neither, it should not be prioritized.
