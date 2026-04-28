# AICOS On Top Of GBrain: Substrate Decision Memo

Status: architecture decision memo  
Date: 2026-04-24  
Scope: `projects/aicos`

## Executive Summary

AICOS is already strong in the places where GBrain is not opinionated enough:

- authority model;
- project/company/workspace control-plane semantics;
- actor/lane/worktree identity;
- structured write contracts;
- handoff/checkpoint/status/feedback discipline;
- project intake/import behavior.

At the same time, AICOS is increasingly rebuilding platform layers that GBrain
already implements or strongly informs:

- retrieval/search substrate;
- search operating modes;
- embedding/health/freshness discipline;
- maintenance loops and recurring review jobs;
- some MCP-serving and compatibility discipline.

The CTO judgment is:

1. **Do not discard AICOS.**
2. **Do not continue growing a large custom substrate by default.**
3. **Shift AICOS toward a thinner control-plane/product layer on top of a more
   GBrain-derived retrieval/runtime substrate.**

This does **not** mean "replace AICOS with GBrain". It means:

- keep AICOS semantics, authority, and write contracts;
- reduce custom AICOS substrate where GBrain already has proven leverage;
- decide explicitly which current AICOS components remain custom and which
  should be reused, wrapped, migrated, or retired.

## The Core Strategic Question

The relevant choice is no longer:

- "keep building AICOS from scratch" vs
- "use GBrain a little more".

The real choice is:

- **AICOS as a mostly custom full stack**, or
- **AICOS as a semantic/control-plane layer on top of a GBrain-derived
  substrate**.

## Current CTO Assessment

### What AICOS is doing well

AICOS is already ahead of a raw GBrain usage pattern in these areas:

1. **Authority model**
   - clear split between truth, working state, evidence, and history;
   - clear split between AICOS control-plane authority and external runtime
     authority.

2. **Multi-agent project semantics**
   - actor identity;
   - work lane/worktree/work branch semantics;
   - startup bundle and structured continuation;
   - feedback closure and continuity contracts.

3. **Project/control-plane object model**
   - status items;
   - checkpoints;
   - handoffs;
   - artifact refs;
   - project health;
   - intake/import flows.

These are real product differentiators. They should remain AICOS-owned.

### What AICOS is increasingly rebuilding

AICOS is also building more and more of:

1. retrieval/search runtime;
2. hybrid/embedding freshness discipline;
3. health/monitoring/maintenance loops;
4. relation-hygiene and adjacency indexing;
5. client compatibility docs and transport handling.

This is the warning sign.

If left unchanged, AICOS will continue to drift toward a custom platform that
rebuilds too much of the substrate layer.

## Why Not Replace AICOS With Plain GBrain

Using GBrain directly would be faster for:

- shared context storage;
- MCP exposure;
- search/query;
- maintenance jobs;
- knowledge routing.

But plain GBrain does not give AICOS enough of:

- project authority semantics;
- working/evidence/history separation;
- control-plane write contracts;
- multi-agent lane/worktree coordination;
- project intake/import operating model.

So the answer is not "replace AICOS with GBrain". The answer is:

- keep AICOS where AICOS is product-specific;
- stop letting AICOS grow a parallel substrate where GBrain is stronger.

## Proposed Direction

### AICOS should remain responsible for

1. **Authority and object semantics**
   - truth / working / evidence / history boundaries;
   - project/runtime authority split;
   - project/company/workspace object model.

2. **Control-plane contracts**
   - MCP read/write contracts;
   - structured status/checkpoint/handoff/feedback/artifact operations;
   - actor identity and write rules.

3. **Multi-agent coordination semantics**
   - agent family / instance;
   - work lane / worktree / branch behavior;
   - continuation and feedback closure rules.

4. **Onboarding and import discipline**
   - project intake/import flows;
   - startup bundles;
   - continuity and handoff behavior.

### GBrain-derived substrate should increasingly own

1. **Retrieval substrate**
   - indexing;
   - chunking;
   - hybrid retrieval;
   - direct/keyword/hybrid mode system;
   - freshness/coverage health.

2. **Operational search discipline**
   - doctor/verify loop;
   - retrieval eval loop;
   - stale embedding refresh;
   - maintenance jobs.

3. **Potential serving helpers**
   - parts of MCP search/read serving;
   - query behavior and health schemas;
   - recurring maintenance patterns.

## Concrete Plan

### Phase 0 — freeze the scope of the decision

Goal:
- stop accidental substrate sprawl before more custom code accumulates.

Actions:
1. declare that AICOS is evaluating a GBrain-derived substrate direction;
2. require new search/runtime additions to justify why they are not reuse-first;
3. keep current AICOS semantics unchanged during the evaluation period.

Needed changes:
- decision memo;
- status item;
- handoff/current-state note;
- open item for execution plan.

### Phase 1 — substrate inventory and boundary map

Goal:
- identify exactly which current AICOS pieces are substrate-like vs
  semantics-like.

Actions:
1. inventory current AICOS retrieval/runtime components:
   - search engine;
   - query/read flow;
   - embedding flow;
   - freshness/health;
   - jobs/maintenance;
   - relation audit;
   - MCP serving helpers.
2. classify each as:
   - keep in AICOS;
   - wrap/reuse from GBrain;
   - candidate for migration;
   - candidate for retirement.
3. produce a boundary map.

Needed changes:
- one implementation inventory note;
- one matrix for "keep vs migrate".

### Phase 2 — prove value on one narrow lane

Goal:
- test the strategy on retrieval first, not on the whole product.

Actions:
1. build an AICOS retrieval eval corpus;
2. benchmark current AICOS retrieval stack vs a more GBrain-derived path;
3. test which parts of search mode handling, chunking, and doctor/verify loops
   can be reused without touching AICOS truth or write contracts.

Needed changes:
- retrieval eval corpus;
- benchmark harness;
- query quality report;
- recommendation on which retrieval pieces move first.

### Phase 3 — migrate low-risk substrate pieces

Goal:
- reduce duplicate substrate code without destabilizing AICOS semantics.

Actions:
1. migrate or wrap low-risk pieces first:
   - search operating modes;
   - doctor/verify discipline;
   - maintenance job shape;
   - maybe chunking and query heuristics.
2. keep MCP contracts and AICOS object semantics intact;
3. introduce adapters/wrappers rather than a broad rewrite.

Needed changes:
- adapter layer or wrapper scripts;
- runtime config updates;
- docs refresh;
- regression checks.

### Phase 4 — evaluate deeper migration candidates

Goal:
- decide whether AICOS should continue as a thin semantic layer over a
  GBrain-derived runtime, or stop at partial reuse.

Actions:
1. review results from Phase 3;
2. decide whether deeper migration is justified for:
   - direct-get object fetch;
   - relation-aware retrieval;
   - more MCP-serving internals;
   - maintenance/job substrate.
3. reject any migration that weakens authority or object semantics.

Needed changes:
- ADR or final decision note;
- explicit "go/no-go" on deeper substrate reuse.

## What Would Change In The Current Product

### What should not change

These product behaviors should remain stable:

1. AICOS remains the control-plane authority.
2. Markdown in `brain/` remains truth.
3. MCP write semantics remain AICOS-owned.
4. Project/runtime authority split remains intact.
5. Status/checkpoint/handoff/feedback objects remain first-class and distinct.
6. Agent identity/lane/worktree rules remain AICOS-owned.

### What would change

These areas may change significantly:

1. **Retrieval engine internals**
   - less custom AICOS logic;
   - more GBrain-derived search/runtime behavior.

2. **Health/verify/maintenance**
   - stronger doctor/eval discipline;
   - more substrate-provided maintenance behavior.

3. **Chunking and query behavior**
   - richer snippet/chunk retrieval;
   - more explicit search mode behavior.

4. **Implementation ownership**
   - fewer AICOS-native substrate modules;
   - more wrappers/adapters and boundary docs.

## Why This Should Make AICOS Better

### Better

1. **Faster leverage**
   - more reuse of proven retrieval/search runtime.

2. **Less duplicate platform work**
   - fewer AICOS-specific implementations of generic substrate concerns.

3. **Stronger retrieval quality sooner**
   - better chance of reaching mature chunking/mode/doctor/eval behavior.

4. **More focus on true product differentiation**
   - semantics;
   - governance;
   - multi-agent control-plane behavior.

### Worse / tradeoffs

1. **More dependency on a GBrain-derived layer**
   - AICOS loses some implementation independence at the substrate level.

2. **Potential fork maintenance burden**
   - especially if the reuse path becomes a fork, not a wrapper.

3. **Boundary management becomes critical**
   - a sloppy migration could blur AICOS authority or turn high-churn surfaces
     into over-structured schema.

4. **Temporary architecture complexity**
   - during migration, the system may be harder to explain because old AICOS
     substrate and new reused substrate may coexist for a while.

## The Main Architectural Risk

The biggest risk is not "using GBrain".  
The biggest risk is using GBrain **without a hard boundary**.

If AICOS starts importing GBrain shape too literally:

- everything tends to become a generic page/entity;
- link graph pressure rises;
- summaries/compiled views risk becoming second truth surfaces;
- high-churn working surfaces become heavier and harder to operate.

That would be a real product regression.

So the rule is:

- **reuse substrate behavior aggressively;**
- **do not import product shape blindly.**

## Recommended Immediate Moves

1. Open a specific execution lane for "AICOS on GBrain-derived substrate".
2. Build the keep/migrate/retire inventory next.
3. Start with retrieval eval and runtime/doctor discipline, not with a
   large-scale schema migration.
4. Defer any deep object-model changes until the substrate reduction path proves
   value.

## Final Judgment

Continuing to build AICOS exactly as it is now is not economically optimal.

Forking or strongly reusing GBrain at the substrate layer is now a serious
candidate, because:

- AICOS already knows what semantics it must preserve;
- the current custom substrate surface is growing;
- retrieval/runtime is not where AICOS is most differentiated.

The recommended direction is:

**AICOS should evolve toward a thinner semantic/control-plane product on top of
a more GBrain-derived retrieval/runtime substrate.**

This should be done deliberately, with a hard boundary and phased migration, not
as ad hoc code borrowing.
