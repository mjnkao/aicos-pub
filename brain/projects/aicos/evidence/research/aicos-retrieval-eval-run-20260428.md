# AICOS Retrieval Eval Run

Status: completed baseline run  
Date: 2026-04-28  
Scope: `projects/aicos`  
Actor: A2-Core-C

## Purpose

Run the expanded A1/human-manager retrieval corpus through the same HTTP MCP
query path that external A1 agents use.

## Command

```bash
./aicos sync brain --text-only
scripts/aicos-retrieval-eval --token <redacted>
```

## Result

- Items: 29
- Top-3 expected-ref hits: 28/29
- Top-5 expected-ref hits: 29/29
- Tool/runtime errors: 0

## Top-3 Misses

These are not top-5 failures, but they show where ranking can still improve.

| ID | Expected rank | Observation |
| --- | ---: | --- |
| `gbrain-search-health-check` | 4 | Health-check query finds the GBrain/AICOS search pattern note and backlog before query guide. Acceptable top-5, but operational guide could rank higher. |
| `strategic-cto-architecture-review` | 4 | Strategic review now nudges direct reads and retrieves architecture north-star in top-5. Orientation docs still rank before deep architecture anchors, which is acceptable because A1 should read startup/handoff first. |
| `strategic-ceo-product-review` | 3 | CEO review now retrieves build-vs-buy/product strategy status in top-3. It still needs answer synthesis discipline to separate product, business, and architecture concerns. |

## Issues Caught While Building Runner

The runner caught two integration-shape problems before the real eval run:

1. Read calls must include `agent_family`, `agent_instance_id`, and
   `execution_context`. The runner now sends default eval identity:
   `codex / aicos-retrieval-eval / cli`.
2. `aicos_query_project_context` expects `query`, while the eval corpus stores
   human-readable `question`. The runner now maps `question` to MCP `query`.

Both are useful because they are exactly the kind of shape mismatch an external
A1 can hit when using MCP manually.

## Applied Light Fix

`docs/install/AICOS_QUERY_SEARCH_GUIDE.md` now includes a short "search misses
expected context" path:

1. retry with tighter `context_kinds`;
2. use direct read surface if one exists;
3. record structured feedback with expected missing ref/query/top wrong refs;
4. do not patch raw markdown from A1 just to hide retrieval gaps.

The latest runtime pass also adds:

- `direct_read_nudges` in `aicos_query_project_context` for startup,
  project-discovery, current-work, next-work, and coordination intents;
- PG search inclusion for shared `project_registry` when requested;
- small current-control boosts for `context-ladder`, `current-state`,
  `current-direction`, `handoff/current`, and active status surfaces;
- PG-side filtering of resolved/closed/stale/deferred status items by default,
  matching markdown-direct behavior;
- one Vietnamese human-manager startup eval item:
  "kiểm tra xem dự án đang làm đến đâu rồi, có những việc gì đang làm, ai đang
  làm, chúng ta nên làm việc gì tiếp?"
- five strategic review eval items:
  - CTO architecture review;
  - CEO product strategy review;
  - build-vs-buy/substrate review;
  - scalability/risk review;
  - Option C / coworker-dashboard misalignment review;
- a small strategic-anchor map for known AICOS architecture/product review
  sources, without adding graph engine, reranker, or a broader search platform.

For that human-manager question, AICOS now returns `handoff/current` as rank #1
and nudges A1 toward:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_status_items`
- `aicos_get_project_health`
- `aicos_get_feedback_digest`

## CTO Judgment

Current retrieval is good enough to keep A1 agents using it while Phase 1 work
continues:

- top-5 is strong for the expanded manager/A1 corpus;
- no runtime errors after runner shape fixes;
- current weakness is now mostly answer synthesis/use of direct reads, not
  search availability.

Next search work should stay small:

- add direct-read nudges for startup/handoff/status/project-registry intents;
- improve ranking for current controlling status items;
- keep eval runner as a regression check before each search/ranking change.
