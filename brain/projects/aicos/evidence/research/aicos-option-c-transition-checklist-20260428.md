# AICOS Option C Transition Checklist

Status: execution checklist, CTO-reviewed 2026-04-28
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

## CTO Review Update — 2026-04-28

The checklist remains directionally correct, but its execution state has moved
forward. Future agents should not restart from Phase 0.5 or redo baseline search
work unless new evidence shows a regression.

Current state:

- Phase 0 direction lock is materially established.
- Phase 0.5 operating surface is good enough for continued real A1 usage.
- Phase 1 module inventory exists.
- Phase 2 semantic core boundary and actor model normalization exist.
- Phase 3 provider interface sketch exists.
- Phase 4 deployment profiles exist.
- Phase 5 retrieval eval and first search-quality loop exist.
- Phase 6/7 baseline notes exist as contracts, not implementation approval.

Current CTO priority:

1. keep current MCP/search/feedback surfaces stable;
2. use feedback-to-eval before changing retrieval behavior;
3. harden runtime/security before wider team rollout;
4. productize project intake minimally before company/workspace packs;
5. defer dashboard/PM implementation until coworker/job read surfaces are
   stable.

The new module decision inventory is now the practical guardrail for future
implementation:

`brain/projects/aicos/evidence/research/aicos-current-module-decision-inventory-20260428.md`

## Phase 0 — Lock The Direction

### Must be true

- [x] The product framing note remains the reference for "what AICOS is for".
- [x] The Option C north-star remains the reference for "how AICOS should be
      structured".
- [x] The execution decision table remains the reference for
      keep/reuse/migrate/retire decisions.

### Deliverables

- [x] Keep `current-state.md`, `current-direction.md`, and `handoff/current.md`
      aligned with the north-star.
- [x] Reject or defer architectural proposals that collapse AICOS into either:
      - a PM tool clone;
      - a generic memory/search product;
      - a single fixed implementation stack.

## Phase 0.5 — Stabilize The Current Operating Surface

Goal: make the current stack stable enough to keep using, observing, and
learning from real agent behavior before deeper modularization work.

### Operating rule

- [x] Treat HTTP daemon MCP as the default AICOS interaction path.
- [x] Require A1 agents to read and write AICOS-facing context/control-plane
      state through the HTTP daemon only.
- [x] Disallow direct markdown writeback for A1 agents, even as a convenience
      fallback.
- [x] Allow direct file-write fallback only for `A2-Core-R` and `A2-Core-C`
      when MCP HTTP is genuinely blocked or when they are restructuring AICOS
      internals directly.
- [x] Keep even A2-Core on HTTP MCP by default, so friction is discovered
      early instead of hidden behind direct edits.

### Stabilization checklist

- [x] Run a connectivity sanity pass for the main clients:
      - Codex Desktop
      - Claude Code
      - Claude Desktop
      - Antigravity
      - OpenClaw / mjnclaw
- [x] Verify that each client can:
      - connect
      - read startup bundle
      - read handoff/status/query surfaces
      - write semantic updates
- [x] Review read/write friction around:
      - actor identity requirements
      - `mcp_contract_ack`
      - feedback closure
      - long-form write ergonomics
      - error-message quality
- [x] Review search/runtime stability around:
      - daemon health
      - stale/freshness behavior
      - embedding coverage
      - rate-limit/retry behavior
- [x] Review monitor/ops noise and remove false-alert behavior where possible.
- [ ] Keep a client compatibility matrix current as a first-class operating
      artifact.

### Concrete outputs

- [x] One stabilization pass note for the current operating surface
- [x] One client compatibility matrix for the HTTP daemon path
- [x] One shortlist of MCP friction items that should be fixed before deeper
      modularization work

## Phase 1 — Module Inventory

Goal: classify the current repo into semantic core, runtime services,
providers, profile-specific concerns, and transitional legacy.

### Checklist

- [x] Inventory AICOS code modules under `packages/aicos-kernel/`,
      `integrations/`, `serving/`, and `backend/`.
- [x] Classify each module as one of:
      - semantic core
      - runtime service
      - provider implementation
      - deployment/profile concern
      - migration/legacy residue
- [x] Mark each module with a decision:
      - keep
      - refactor behind boundary
      - migrate toward provider layer
      - retire / stop growing

### Concrete outputs

- [x] One module inventory note
- [x] One keep/reuse/migrate/retire matrix at code/module level
- [x] One shortlist of modules that should not gain new responsibilities until
      boundaries are cleaned

## Phase 2 — Extract Semantic Core Boundaries

Goal: make it obvious what AICOS owns regardless of substrate choice.

### Checklist

- [x] Formalize semantic core boundaries around:
      - authority model
      - object model
      - coordination semantics
      - read/write contracts
- [x] Normalize the actor model so `A1` / `A2` is treated as AICOS-internal
      maintenance taxonomy, not the universal role taxonomy for every project
      using AICOS.
- [x] Separate at least three role dimensions clearly:
      - AICOS-internal actor class
      - project-facing functional role
      - service role (`internal actor`, `external actor`, equivalent)
- [x] Identify which current modules are the de facto semantic core today.
- [ ] Reduce direct coupling from semantic logic into PG/GBrain/search-specific
      assumptions.

### Concrete outputs

- [x] Core boundary note or ADR
- [x] Actor model normalization note
- [x] Refactor map for semantic core extraction
- [x] List of invariants that future providers must never violate

## Phase 3 — Define Provider Interfaces

Goal: make substrate replacement or reuse possible without product drift.

### Checklist

- [x] Define a minimal Retrieval Provider boundary
- [x] Define a minimal Memory / Context Store Provider boundary
- [x] Define a minimal Jobs / Maintenance Provider boundary
- [x] Define a minimal Auth / Audit Provider boundary
- [x] Keep Relation / Graph Provider optional and explicitly second-wave

### Constraints

- [x] Do not over-abstract before real variation is needed
- [x] Do not build adapters for every product immediately
- [x] Start with the current stack as the first provider bundle

### Concrete outputs

- [x] Interface sketch or contract note
- [x] First mapping of current implementation to provider slots

## Phase 4 — Formalize Profiles

Goal: stop treating current deployment behavior as one implicit stack.

### Profile checklist

- [x] Define `solo` profile clearly
- [x] Define `small-team` profile clearly
- [x] Define `company-100` profile clearly
- [x] Keep `enterprise` as future target, not near-term build scope

### Current-stack checklist

- [x] Document the current implementation as the first concrete bundle for the
      `small-team` profile:
      - markdown truth
      - GBrain sync/import
      - PG hybrid retrieval
      - HTTP MCP
      - token auth
      - background embedding/freshness path

### Concrete outputs

- [x] Profile matrix
- [x] Required vs optional capabilities per profile
- [x] Which providers each profile expects

## Phase 5 — Retrieval/Runtime Reduction Pass

Goal: reduce custom substrate growth first where AICOS is least differentiated.

### Checklist

- [x] Build AICOS retrieval eval corpus
- [x] Benchmark markdown-direct vs FTS vs hybrid
- [x] Review current chunking/summary behavior
- [x] Review doctor/verify/freshness loop gaps
- [ ] Decide what retrieval/runtime logic stays custom vs gets wrapped or
      replaced

### Concrete outputs

- [x] Eval corpus
- [x] Benchmark report
- [ ] Retrieval/runtime refactor recommendation

## Phase 5.5 — A1 Learning Loop Operating Discipline

Goal: ensure AICOS actively asks A1 agents for service/search/tool friction and
turns useful feedback into retrieval or product improvements without adding a
heavy survey/workflow system.

### Checklist

- [x] Expose `feedback_loop.ask_now` during first-contact/startup situations.
- [x] Require session-close feedback closure or `feedback_type=no_issue` for
      completed/blocked/waiting continuity writes.
- [x] Provide `aicos_record_feedback` and `aicos_get_feedback_digest`.
- [x] Provide feedback-to-eval digest script for A2 review.
- [x] Add feedback records to searchable/indexed context.
- [ ] Before search/retrieval changes, run feedback digest and check whether
      new A1 feedback should become eval cases.
- [ ] Add explicit A1-oriented prompt examples for:
      - missing expected context;
      - overly broad results;
      - stale results;
      - confusing tool schema;
      - missing tool or project.
- [ ] Track whether real A1 agents actually submit non-`no_issue` feedback
      after first contact and session close.
- [ ] If repeated A1 feedback is absent despite known friction, consider adding
      one more nudge boundary before adding heavier workflow.

### Concrete outputs

- [x] Phase 0.5 learning-loop check
- [x] Feedback closure gate
- [x] Feedback-to-eval digest
- [ ] Learning-loop effectiveness review after more real A1 sessions

## Phase 6 — Human + AI Coworker Model

Goal: prepare for dashboard and PM-tool integration without turning AICOS into
a PM clone.

### Checklist

- [x] Define task/coworker model explicitly
- [x] Define ownership model for humans and agents
- [x] Define takeover / handoff-ready / blocked-by-human / blocked-by-agent
      semantics
- [x] Define the minimum operational read surfaces needed for a dashboard:
      - active workers
      - active lanes
      - takeover-ready items
      - human attention queue
      - project board summary

### Concrete outputs

- [x] Human+AI coworker model note
- [x] Dashboard-facing read-surface proposal

## Phase 7 — Plane / ClickUp Integration Contract

Goal: integrate with shared task tools without surrendering AICOS control-plane
identity.

### Checklist

- [x] Decide the sync authority model:
      - AICOS-first
      - PM-tool-first
      - hybrid
- [x] Define which task fields belong to AICOS
- [x] Define which task fields can live in Plane/ClickUp only
- [x] Define sync conflict rules
- [x] Define human-visible activity model for AI coworkers

### Concrete outputs

- [x] PM integration contract note
- [x] First target integration shortlist (Plane / ClickUp)

## Phase 8 — Company / Workspace / Project Packs

Goal: make AICOS adaptable across many companies without product forks.

### Checklist

- [ ] Identify what belongs in company pack
- [ ] Identify what belongs in workspace pack
- [x] Identify what belongs in project pack
- [ ] Keep packs lightweight and configuration-like at first

### Concrete outputs

- [ ] Pack model note
- [ ] First pack schema draft

## Items Already Deferred Or Intentionally Not Pursued Right Now

- [x] Keep `RISK-PG-TRUTH-STORE` deferred under current Option C direction.
- [x] Do not introduce heavy graph truth or page-centric universal schema.
- [x] Do not turn AICOS into a PM tool clone.
- [x] Do not build multi-provider support broadly before the first provider
      boundaries are proven useful.

## Suggested Execution Order From Here

1. Continue Phase 5 / 5.5 as an operating loop:
   - run retrieval eval before search changes;
   - run feedback digest before search/tooling changes;
   - add eval cases only from repeated or high-risk A1 misses.
2. Harden runtime/security for small-team and company-100 readiness:
   - token scope clarity;
   - SSE/HTTPS client compatibility;
   - LAN risk and single-machine SPOF decision;
   - noisy monitor behavior only when observed.
3. Productize project intake/import minimally:
   - project proposal -> human/A2 approval;
   - project brain pack creation/import;
   - registry entry;
   - token/access policy.
4. Define read-only job/coworker views only after current
   status/task/handoff quality stays stable.
5. Start Plane/ClickUp/dashboard connector work only after the read-only views
   are useful and authority conflicts are explicit.
6. Keep company/workspace packs lightweight until at least two external
   projects need the same pack abstraction.

## Final Rule

Every future implementation pass should be explainable in one of two ways:

1. it strengthens AICOS semantic/control-plane ownership, or
2. it reduces duplicated substrate work without weakening AICOS semantics.

If a proposed change does neither, it should not be prioritized.
