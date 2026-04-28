# AICOS GBrain Search Patterns For A1 Eval

Status: applied research note  
Date: 2026-04-28  
Scope: `projects/aicos`  
Actor: A2-Core-R/C

## Purpose

Translate the useful parts of GBrain's query/search/skill behavior into AICOS
retrieval evaluation questions for human managers and A1 agents.

This is not a proposal to move AICOS onto GBrain's full page schema, job
system, or link graph. It is a narrow Phase 0.5 search-quality pass.

## Sources Reviewed

- Local mirror: `tools/gbrain/skills/query/SKILL.md`
- Local mirror: `tools/gbrain/docs/guides/search-modes.md`
- Local mirror: `tools/gbrain/docs/guides/brain-first-lookup.md`
- Local mirror: `tools/gbrain/docs/guides/brain-agent-loop.md`
- Local mirror: `tools/gbrain/test/e2e/skills.test.ts`
- Local mirror: `tools/gbrain/test/search-limit.test.ts`
- Local mirror: `tools/gbrain/docs/GBRAIN_VERIFY.md`
- GitHub: `https://github.com/garrytan/gbrain`
- GitHub: `https://github.com/garrytan/gbrain/blob/master/skills/query/SKILL.md`
- GitHub: `https://github.com/garrytan/gbrain/blob/master/docs/guides/search-modes.md`
- GitHub: `https://github.com/garrytan/gbrain/blob/master/docs/guides/brain-agent-loop.md`

## GBrain Patterns Worth Adapting Now

### 1. Mode choice before search

GBrain separates:

- direct page fetch when the slug/object is known;
- keyword search for exact terms and names;
- hybrid query for semantic or fuzzy questions;
- structured graph/list/backlink queries for relational questions.

AICOS adaptation:

- direct MCP reads first for known surfaces:
  `aicos_get_startup_bundle`, `aicos_get_handoff_current`,
  `aicos_get_status_items`, `aicos_get_project_registry`,
  `aicos_get_project_health`;
- `aicos_query_project_context` only when the agent does not yet know the
  source ref;
- exact file read only after MCP points to a source or when A2 is doing deep
  implementation work.

Eval implication:

- Add questions that check whether A1 can find "which mode should I use" and
  "what should I read for manager/worker/architecture/next-work views."

### 2. Snippets first, full context second

GBrain search/query returns chunks and asks the agent to read top snippets
before opening full pages.

AICOS adaptation:

- `aicos_query_project_context` should be treated as ranked source pointers
  with snippets;
- A1 should open only the 1-3 refs that clearly matter;
- full raw file loading is a second step, not the default.

Eval implication:

- Measure whether expected source refs appear in top 3/top 5.
- Do not measure answer prose yet; first make sure A1 gets pointed to the
  right source.

### 3. Brain-first loop

GBrain's loop is: detect task, read brain, answer/work, write useful updates,
then sync/maintain.

AICOS adaptation:

- A1 reads AICOS through HTTP MCP first for AICOS-facing context/control-plane
  operations;
- A1 writes checkpoint/task/handoff/status/feedback through semantic MCP
  writes;
- A2 may fallback to direct files, but should still prefer MCP when testing
  A1-facing surfaces.

Eval implication:

- Include questions from a human manager asking "how should my A1 use MCP to
  read/write" and "what should the A1 do if search is missing expected
  context."

### 4. Retrieval as an operational surface

GBrain has doctor/verify/search-limit tests and a separate eval direction.

AICOS adaptation:

- Add a small checked-in corpus plus a stdlib-only runner that calls HTTP MCP.
- Use top-3/top-5 expected-ref hits as a cheap regression check.
- Keep this as a smoke/eval tool, not as a new retrieval framework.

Eval implication:

- Add questions for stale index, broken embeddings, and why eval exists before
  ranking changes.

### 5. Skills as behavior packaging

GBrain's strongest "skill" lesson is not the exact files. It is that retrieval
behavior should be explicit and repeatable.

AICOS adaptation:

- Keep `docs/install/AICOS_QUERY_SEARCH_GUIDE.md` as the current lightweight
  behavior card.
- Add corpus questions that encode the behavior human managers expect A1 to
  know.
- Defer a formal AICOS search skill until repeated A1 feedback shows guide-only
  behavior is not enough.

## A1 / Human Manager Question Families Added

The expanded corpus now covers:

1. How A1 uses MCP to read/write.
2. What projects exist and how to discover them.
3. What a project manager should read before assigning/reviewing work.
4. What a worker should read before continuing implementation.
5. What to read for architecture overview.
6. What to read for next work.
7. Which agents are active and how to avoid overlap.
8. How to continue a project without stepping on another agent.
9. How to report feedback/tool friction.
10. How to choose direct-read vs query.
11. How to debug stale search or embeddings.
12. What to do when search misses expected context.
13. Which source wins when search results conflict.
14. Why retrieval eval should gate search changes.

## What Not To Copy Now

Do not copy these into AICOS Phase 0.5:

- full GBrain page schema;
- full typed link graph runtime;
- LLM multi-query expansion;
- graph traversal as an A1 runtime dependency;
- minion/jobs substrate;
- page versioning;
- broad code indexing.

Reason:

- AICOS is a workspace/project context-control plane, not one uniform personal
  knowledge page system.
- Working state, handoff, status, feedback, policy, evidence, contracts, and
  project registry must keep distinct authority boundaries.
- Small-team profile should stay light: markdown truth, HTTP MCP, PG hybrid,
  artifact refs, and explicit eval.

## Applied Changes

- Added `scripts/aicos-retrieval-eval`.
- Expanded
  `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
  from the initial A1/A2 set into a broader A1-manager behavior corpus.

## Next Evaluation Rule

Before changing ranking, routing, or retrieval provider behavior:

1. sync/reindex the brain;
2. run `scripts/aicos-retrieval-eval`;
3. compare top-3/top-5 hit rate;
4. inspect misses by question family;
5. only make a search change if it improves A1 behavior without making the
   small-team stack heavier.
