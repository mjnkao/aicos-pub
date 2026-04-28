# AICOS GBrain-Inspired Search Checklist

Status: implementation checklist
Date: 2026-04-28
Scope: `projects/aicos`
Actor: A2-Core-C

## Purpose

Apply the strongest GBrain search/context ideas to AICOS without changing the
AICOS source-of-truth model.

AICOS keeps:

- `brain/` markdown as durable truth;
- MCP semantic tools as the controlled read/write interface;
- PostgreSQL/GBrain-derived indexes as projections;
- project/workspace/company boundaries as AICOS product semantics.

Do not let GBrain database links, tags, pages, or jobs become a second truth
store unless the same information is durably represented in AICOS markdown or
an explicit external provider contract.

## Current Embedding Reality

Embedding is currently useful, not just decorative.

Measured on the 54-item retrieval corpus:

- FTS-only direct engine run: `top3 25/54`, `top5 25/54`
- Hybrid vector + FTS direct engine run: `top3 53/54`, `top5 54/54`
- Current daemon eval: `top3 53/54`, `top5 54/54`, `errors 0`

Per-scope daemon eval:

- `projects/aicos`: `top3 25/25`, `top5 25/25`
- `projects/sample-project`: `top3 27/28`, `top5 28/28`
- `projects/mjnclaw`: `top3 1/1`, `top5 1/1`

Embedding helps most on semantic/project questions where keyword FTS often
returns nothing:

- sample project canonical repo/authority split;
- sample project product posture and non-goals;
- sample project architecture pipeline/module boundaries;
- sample project package sections/default delivery view;
- sample project macro-calendar gap and browser/CDP risk;
- openai-pipeline current status/fixes.

Known caution: vector search can move current-control surfaces around. Some
strategic review questions rank direct/current surfaces above architecture
evidence, which can be acceptable for startup orientation but should be watched
with per-scope eval and query-intent tests.

## Checklist

### Pass 0 — Keep The Boundary Explicit

- [x] Treat markdown + MCP semantic writes as AICOS truth.
- [x] Treat GBrain/PG search tables as projections.
- [x] Require search changes to pass the AICOS + sample project eval corpus.
- [x] Add a short provider-boundary note to search docs: index metadata and
  graph edges are derived views unless explicitly represented in markdown.

### Pass 1 — AICOS-Native Page Schema Projection

Goal: get GBrain-style page schema benefits without replacing AICOS file
homes.

- [x] Extend index metadata extraction for AICOS object types:
  `current_state`, `current_direction`, `handoff`, `status_item`,
  `task_state`, `checkpoint`, `artifact_ref`, `policy`, `contract`,
  `canonical`, `evidence`.
- [x] Extract stable fields from markdown into indexed columns or JSON:
  `item_id`, `task_ref`, `status`, `item_type`, `work_lane`, `work_type`,
  `actor_role`, `agent_family`, `agent_instance_id`, `coordination_status`,
  `last_updated_at`, `next_step`.
- [x] Do not require existing markdown files to become GBrain compiled-truth
  pages.
- [x] Add eval cases that require field-aware filtering:
  open-only status items, active work lane, agent instance ownership, stale
  suppression.
- [x] Keep the first implementation read-only/projection-only.

### Pass 2 — Retrieval Recipes For Common A1 Questions

Goal: make A1 behavior reliable by routing common questions through structured
read sequences before broad search.

- [x] Define recipe: `manager_progress_review`.
  Reads startup/current state, handoff/current, active status items, task-state,
  recent checkpoints, open items/questions.
- [x] Define recipe: `worker_takeover`.
  Reads handoff/current, active task-state/status, coordination policy, then
  worktree/source refs.
- [x] Define recipe: `architecture_review`.
  Reads current direction, north-star/architecture evidence, semantic core,
  provider boundary, recent decision follow-ups.
- [x] Define recipe: `mcp_usage_and_feedback`.
  Reads install/query/write cookbook, MCP contract, learning loop docs.
- [x] Add query output hints that recommend these recipes when intent matches.
- [x] Evaluate recipes on both `projects/aicos` and
  `projects/sample-project`.

### Pass 3 — Derived Link Graph

Goal: get GBrain link-graph value while preserving markdown truth.

- [ ] Extract relation edges from existing markdown fields:
  `trace_refs`, `artifact_refs`, `task_ref`, `item_id`, `work_lane`,
  `agent_instance_id`, `source_ref`.
- [ ] Store edges as a derived relation index, not as primary truth.
- [ ] Support graph views such as:
  `project -> active work lanes -> status items -> task states -> checkpoints
  -> artifacts`.
- [ ] Add a relation audit command that reports broken refs and orphaned active
  items.
- [ ] Add eval questions that require adjacency, not just text match:
  "what is connected to this openai-pipeline issue?", "which checkpoint backs
  this status item?"

### Pass 4 — Job View, Not Job Truth

Goal: answer "who is doing what and what should happen next?" without creating
a premature PM system.

- [ ] Build a read-only job-like view from:
  `status_item + task_state + handoff + checkpoint + artifact_ref`.
- [ ] Define minimum job-view fields:
  `project`, `work_lane`, `title`, `status`, `owner/observed_agent`,
  `next_step`, `blockers`, `latest_checkpoint`, `related_artifacts`.
- [ ] Do not introduce new mandatory A1 write tools for jobs yet.
- [ ] Compare job-view output against direct status/task/handoff reads in eval.
- [ ] Only consider first-class `job` primitive after repeated A1 usage proves
  the view is the correct abstraction.

### Pass 5 — GBrain Skills Adaptation

Goal: adapt GBrain's operational discipline, not its personal-brain product
shape.

- [ ] Translate GBrain `query` skill into AICOS "brain-first, MCP-first"
  project context lookup.
- [ ] Translate GBrain `maintain` skill into AICOS retrieval health checks:
  stale index, stale embeddings, orphan refs, closed status pollution,
  eval regression.
- [ ] Translate GBrain `ingest` idea into AICOS project-context import:
  compact canonical digests, provenance refs, no repo mirror.
- [ ] Keep skill examples actor-neutral for external A1 agents.
- [ ] Add "what not to do" examples: raw markdown writes by A1, treating PG
  graph as truth, broad repo mirroring.

### Pass 6 — Embedding Governance

Goal: keep vector search helpful without making the system opaque or expensive.

- [ ] Keep `./aicos brain status` showing embedding coverage/freshness.
- [ ] Add eval mode or report comparing FTS-only vs hybrid periodically.
- [ ] Track which eval items are vector-dependent.
- [ ] Add warning if embedding coverage is low but query engine reports hybrid.
- [ ] Consider per-kind weighting so vector does not over-promote old evidence
  above current-control surfaces.
- [ ] Do not add LLM reranking until eval shows repeated failures that
  metadata/recipes/link graph cannot fix.

## Implementation Update 2026-04-28

Completed first implementation pass:

- PostgreSQL search schema now has derived `index_metadata` and
  `index_schema_version` columns.
- Indexer extracts AICOS object metadata from markdown truth into projection
  JSON.
- Query results expose compact `object_metadata` for agents.
- PG hybrid and markdown-direct fallback both return `retrieval_recipes`.
- Retrieval eval corpus now includes field-aware cases for open status items,
  active work lane, agent instance ownership, and resolved-baseline
  suppression.
- Query engine now injects a narrow exact metadata lookup for audit questions
  such as `agent_instance_id`, `work_lane`, `agent_family`, and `item_id`.
- MCP schema extension constants are centralized in
  `aicos_kernel.mcp_tool_schema`.
- `scripts/aicos-mcp-tool-schema-parity` verifies HTTP daemon and stdio schemas
  still match.
- Latest regression after this pass: 58 items, top3 56/58, top5 58/58,
  errors 0.

## Decision Rule

Implement in this order:

1. schema projection;
2. retrieval recipes;
3. derived link graph;
4. job view;
5. recurring maintenance/eval loop;
6. only then consider heavier graph/job primitives.

This preserves the Option C architecture: AICOS remains the modular
context/control-plane, while GBrain-style schema/search/graph patterns improve
retrieval quality as replaceable projections.
