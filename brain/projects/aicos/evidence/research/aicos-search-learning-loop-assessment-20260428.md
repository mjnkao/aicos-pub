# AICOS Search Learning Loop Assessment

Status: CTO assessment / proposed operating loop  
Date: 2026-04-28  
Scope: `projects/aicos`  
Actor: A2-Core-R/C

## Question

Are current AICOS search improvements self-built one-off fixes, learned from
other systems, reusable elsewhere, and can AICOS improve retrieval through a
learning loop instead of fixing every failed A1 query manually?

## Short Answer

AICOS is partly self-building, but not from scratch.

The current search direction adapts known retrieval patterns from GBrain and
general IR/RAG practice:

- direct get / structured read before broad search;
- keyword + vector hybrid retrieval;
- snippets first, full source second;
- source precedence;
- doctor/freshness checks;
- eval corpus and regression before ranking changes.

What is AICOS-specific is the object model and behavior target:

- human + AI agents working across projects;
- A1/A2 service boundary;
- MCP-first context/control-plane;
- handoff/status/task/feedback/project-registry surfaces;
- role-aware reading paths for manager, worker, CTO, CEO, and takeover flows.

So the search work is not "invent a search engine." It is "wrap a small hybrid
retrieval substrate with AICOS-specific role, authority, and workflow routing."

## What We Are Learning From

### GBrain

Reusable:

- search mode discipline;
- query skill behavior;
- brain-first lookup loop;
- doctor/verify/search-quality loop;
- snippets-first reading.

Not copied:

- full page schema;
- page/link graph runtime;
- minion/job substrate;
- full personal-brain object model.

### General retrieval practice

Reusable:

- FTS + vector hybrid search;
- RRF/fusion-style ranking;
- regression eval sets;
- top-k expected-source metrics;
- query intent routing;
- freshness and stale filtering.

### AICOS feedback

Reusable:

- A1 feedback about missing context, broad results, confusing tools, stale
  status, write friction, and MCP interop;
- human-manager task shapes that reveal what A1 actually needs to answer.

## What Can Be Applied Elsewhere

The reusable part is not the exact AICOS file list. It is the loop:

1. collect real human/A1 question;
2. classify the question family;
3. define expected source refs;
4. add it to a retrieval eval corpus;
5. run current retrieval;
6. adjust routing/ranking/docs lightly;
7. rerun regression;
8. record result and feedback.

This can apply to other projects such as sample project trading:

- replace AICOS strategic anchors with sample project project anchors;
- keep common question families:
  - current progress;
  - active work/owners;
  - next work;
  - architecture review;
  - risk review;
  - canonical repo/source;
  - handoff/takeover;
  - manager/worker role reads.

## Current Weakness

The current implementation still has too much hand-coded knowledge:

- direct-read nudge patterns are string/rule based;
- strategic anchors are curated manually;
- eval corpus is manually expanded;
- A1 feedback is recorded but not automatically converted into eval items or
  routing candidates.

This is acceptable for Phase 0.5 small-team operations, but it should not grow
into a pile of one-off if/else rules.

## Recommended Learning Loop

### Loop 1: Feedback-to-eval

Whenever an A1 records retrieval feedback:

- `context_missing`
- `context_overload`
- `stale_result`
- `query_failed`
- `tool_shape_confusing`

A2 should periodically turn high-signal feedback into a candidate eval item:

```yaml
question: "<exact human/A1 wording>"
scope: "projects/<id>"
functional_role: "<manager|worker|CTO|CEO|operator|...>"
expected_refs:
  - "<source A1 should have found>"
failure_mode_if_missing: "<what went wrong>"
```

Promotion rule:

- add to corpus only if it represents a repeatable question family or a high
  risk miss;
- do not add every noisy one-off query.

### Loop 2: Eval-to-routing

After new eval items are added:

1. run `scripts/aicos-retrieval-eval`;
2. inspect top-3/top-5 misses;
3. prefer docs/guide/context-kind examples first;
4. then small direct-read nudge/ranking changes;
5. only then consider relation graph or provider changes.

Promotion rule:

- a search change should improve target family without lowering existing top-5
  coverage;
- if it requires graph/reranker/external system, record an open item instead of
  silently expanding architecture.

### Loop 3: Query telemetry digest

Use existing daemon audit logs to produce a periodic retrieval digest:

- most common query families;
- queries with no results;
- queries with direct-read nudges;
- queries followed by feedback;
- query families with repeated missing-context feedback.

This can stay offline/batch at first. No need for real-time analytics.

### Loop 4: Role-aware reading maps

Each project should eventually have a compact role-aware map:

```yaml
role_views:
  manager:
    direct_reads: [startup_bundle, handoff_current, status_items, project_health]
    query_kinds: [current_state, current_direction, handoff, status_items]
  worker:
    direct_reads: [startup_bundle, handoff_current, task_packet]
    query_kinds: [task_state, canonical, current_state]
  CTO:
    direct_reads: [startup_bundle, handoff_current, status_items, project_health]
    query_kinds: [current_direction, canonical, policy, contract, evidence, status_items]
  CEO:
    direct_reads: [startup_bundle, handoff_current, status_items, project_health]
    query_kinds: [current_direction, canonical, evidence, status_items]
```

For Phase 0.5 this can stay in docs/corpus. Later it can become a project
metadata surface if repeated across projects.

## What Not To Automate Yet

Do not let AICOS automatically mutate ranking rules from feedback.

Reason:

- feedback can be noisy;
- one project role can conflict with another;
- a ranking fix for CTO review can hurt worker handoff;
- source authority must remain explicit.

Instead, automate the boring parts:

- feedback digest;
- candidate eval item generation;
- regression run;
- before/after report.

Keep promotion human/A2-reviewed until the pattern is stable.

## CTO Recommendation

Continue with this approach, but draw a clear line:

- AICOS should own role-aware context routing, source authority, MCP read/write
  behavior, and retrieval eval;
- AICOS should not own a large custom search platform;
- use GBrain/PG/vector/other providers as swappable substrate pieces;
- keep learning loop evidence-driven so the system improves from A1 usage.

The next practical step is not a new search engine. It is:

1. build feedback-to-eval digest;
2. make eval runner part of search-change regression;
3. add project-specific role-view maps only when at least two projects need
   them.
