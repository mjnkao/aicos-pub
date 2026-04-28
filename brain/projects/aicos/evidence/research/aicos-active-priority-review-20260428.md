# AICOS Active Priority Review

Status: current priority review
Date: 2026-04-28
Scope: `projects/aicos`
Actor: A2-Core-C

## Purpose

Keep the latest GBrain-inspired search checklist and the broader AICOS open work
sequenced so future agents do not drift into whichever status item is loudest.

This review uses the current state, current direction, current handoff, and
active status items. It does not reopen the Phase 0 direction unless a future
decision explicitly revises one of the anchor artifacts.

## Direction Anchors

Treat these as the current decision baseline:

1. Product framing / build-vs-buy:
   `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
2. Execution decision table:
   `brain/projects/aicos/evidence/research/aicos-execution-decision-table-20260428.md`
3. Option C north-star:
   `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`
4. Option C transition checklist:
   `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
5. GBrain-inspired search checklist:
   `brain/projects/aicos/evidence/research/aicos-gbrain-inspired-search-checklist-20260428.md`

## Current Read

AICOS is in a useful but still delicate state:

- Phase 0 direction is materially locked.
- Phase 0.5 is good enough to move forward while fixing real client issues as
  they appear.
- HTTP MCP + PostgreSQL hybrid search + embeddings are working and fresh.
- Retrieval eval is now meaningful across `projects/aicos` and
  `projects/sample-project`.
- The biggest near-term risk is not lack of ideas; it is adding more tools and
  surfaces before schema, retrieval recipes, and provider boundaries are
  cleaned up.

## Priority Order

### P0 — Keep The Running Surface Stable

Do this before deeper architecture work if there is a fresh client/runtime
failure.

- Fix real MCP client connection/read/write failures from Codex, Claude Code,
  Claude Desktop, Antigravity, or OpenClaw.
- Keep forcing A1 agents through HTTP MCP for AICOS-facing context/control-plane
  operations.
- Keep A2 fallback-to-file as an exception, not the normal path.
- Keep `./aicos brain status`, daemon health, and retrieval eval green.

Relevant status items:

- `AICOS-OPTION-C-TRANSITION-CHECKLIST`
- `AICOS-BRAIN-STATUS-PG-STALE-FALSE-SIGNAL`
- `AICOS-MCP-SSE-AUTH-INTEROP`
- `AICOS-LAN-SECURITY-HARDENING`
- `RISK-LAN-AGENT-FALLBACK`

Recommended stance: fix concrete friction as it appears, but do not camp in
Phase 0.5 unless client failures block real A1 usage.

### P1 — Search / Retrieval Quality For A1

This is the most important product-quality work right now because AICOS only
helps if agents can quickly find the right context without over-reading.

Next steps:

1. Implement GBrain-inspired Pass 1: AICOS-native schema metadata projection.
2. Implement GBrain-inspired Pass 2: retrieval recipes for common A1 questions.
3. Keep running the two-project eval gate after each change:
   `scripts/aicos-retrieval-eval --max-results 5`.
4. Track FTS-only vs hybrid contribution periodically; current evidence shows
   embeddings are materially useful.
5. Defer graph/reranker/external search providers until eval misses justify
   them.

Relevant status items:

- `aicos-gbrain-inspired-search-checklist-20260428`
- `aicos-search-eval-two-project-regression-gate-20260428`
- `aicos-phase-5-retrieval-runtime-reduction`
- `AICOS-SEARCH-FOCUS-A1-CONTEXT-RETRIEVAL`
- `aicos-retrieval-direct-read-nudges-human-manager-startup-20260428`

Recommended stance: do this next unless a P0 client failure blocks usage.

### P2 — Module Inventory And Provider Boundary

Do this after the next search pass has a stable schema/recipe shape. The goal is
to reduce custom substrate work without weakening AICOS-owned semantics.

Next steps:

1. Produce the module inventory requested by the execution decision table:
   keep / reuse-wrap / migrate-fork candidate / retire.
2. Classify current retrieval/runtime components against GBrain and other
   providers.
3. Keep AICOS-owned surfaces clear: semantic core, MCP contracts, authority
   mapping, actor/access model, project/workspace/company packs.
4. Avoid moving markdown truth into PostgreSQL or a GBrain DB graph as truth.

Relevant status items:

- `AICOS-EXECUTION-DECISION-TABLE`
- `AICOS-MARKET-LANDSCAPE-SUBSTRATE-COMPARISON`
- `aicos-gbrain-substrate-decision`
- `AICOS-OPTION-C-NORTH-STAR`
- `RISK-PG-TRUTH-STORE`

Recommended stance: start after P1 Pass 1/2 so the inventory is grounded in the
real retrieval architecture, not abstract comparison.

### P3 — MCP Schema/Constants Dedupe

This is a small but important engineering-quality pass before adding more tools.

Next steps:

1. Centralize MCP tool schemas and shared constants.
2. Generate or share `tools/list` definitions between HTTP daemon and stdio
   adapter.
3. Add parity checks so daemon/stdio schemas do not drift.
4. Keep this as a focused refactor; do not turn it into a provider framework.

Relevant status item:

- `aicos-mcp-schema-constants-dedupe-next`

Recommended stance: do either immediately before or immediately after P1 schema
projection. If P1 adds fields/tool hints, this dedupe becomes more valuable.

### P4 — Reliability And Concurrency Hardening

Important, but should follow real usage unless failures are recurring.

Next steps:

1. Decide the minimum reliability stance for small-team profile:
   accept single-machine SPOF for now, add read-only replica, or move daemon to
   cloud/VPS.
2. Add per-scope write queue / optimistic concurrency if concurrent writes
   become common.
3. Improve LAN fallback/retry behavior if remote agents repeatedly lose MCP
   during daemon restarts.
4. Keep security hardening proportional to the deployment profile.

Relevant status items:

- `ARCH-SINGLE-MACHINE-SPOF`
- `RISK-CONCURRENT-WRITE-QUEUE`
- `RISK-LAN-AGENT-FALLBACK`
- `AICOS-LAN-SECURITY-HARDENING`

Recommended stance: do not overbuild. For current small-team stage, document
the SPOF and maintain git/sync discipline unless real remote work is blocked.

### P5 — Long-Form Write / Detail Field Decisions

These are UX and MCP ergonomics improvements. They matter, but they should be
driven by repeated friction rather than anticipation.

Next steps:

1. Continue using artifact refs for long-form docs.
2. Observe whether A1/A2 agents repeatedly struggle to write long architecture
   or research memos through MCP.
3. Only then add a dedicated long-form memo/research write surface or optional
   status `detail` field.

Relevant status items:

- `AICOS-MCP-LONGFORM-WRITE-BARRIER`
- `OQ-MCP-DETAIL-FIELD`

Recommended stance: defer until concrete repeated friction.

### P6 — Dashboard / PM Integration

Still strategically important, but not next.

Reason:

- AICOS is not a PM tool.
- Human+AI dashboard integration needs stable task/job/coworker semantics first.
- The job view should be derived from status/task/handoff/checkpoint before any
  PM integration contract becomes operational.

Relevant anchors:

- `brain/projects/aicos/evidence/research/aicos-phase-6-human-ai-coworker-model-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-phase-7-pm-integration-contract-20260428.md`
- GBrain-inspired checklist Pass 4 job view.

Recommended stance: defer implementation until after P1/P2/P3. Keep only
architecture notes and integration contract sketches active.

## Recommended Next Five Work Items

1. **P1.1 Search schema projection**:
   extract AICOS object fields from markdown into indexed metadata/JSON.
2. **P1.2 Retrieval recipes**:
   implement manager progress review, worker takeover, architecture review,
   MCP usage/feedback recipes.
3. **P3 MCP schema/constants dedupe**:
   prevent daemon/stdio tool schema drift before more retrieval/tool surfaces.
4. **P2 Module inventory**:
   classify keep/reuse-wrap/migrate/retire against Option C and GBrain-derived
   substrate direction.
5. **P4 Reliability decision note**:
   explicitly accept current small-team SPOF for now or choose a minimal
   mitigation. Do not silently leave it ambiguous forever.

## What Not To Do Next

- Do not start dashboard implementation before job view and task/status
  semantics are stable.
- Do not move working truth to PostgreSQL.
- Do not create a full custom graph engine before derived relation projection
  and eval misses prove it is needed.
- Do not add more MCP tools before schema/constants dedupe unless a real A1
  blocker requires it.
- Do not judge search quality from AICOS-only eval; use AICOS + sample project.

## Operating Rule

Default next work should be:

```text
P0 if current client runtime is broken;
otherwise P1 search schema projection + retrieval recipes;
then P3 schema/constants dedupe;
then P2 module inventory/provider boundary.
```

This keeps AICOS moving toward Option C while improving the part that matters
most today: A1 agents finding and using the right project context quickly.
