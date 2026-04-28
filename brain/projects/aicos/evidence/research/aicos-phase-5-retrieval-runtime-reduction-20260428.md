# AICOS Phase 5 Retrieval Runtime Reduction

Status: phase-5 baseline and search workplan
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Focus AICOS search on practical A1 context retrieval quality while avoiding
custom substrate bloat.

The current user concern is correct: A1 context search is not yet effective
enough. The right next step is not to add another search engine blindly. The
right next step is to build an eval corpus, measure current failure modes, then
make small retrieval improvements that help A1 agents immediately.

## Current Search Stack

Current active stack:

- structured direct reads for known surfaces;
- `aicos_query_project_context`;
- markdown-direct fallback;
- PostgreSQL FTS;
- optional pgvector embeddings;
- intent/kind heuristics;
- authority/freshness ranking;
- compact snippets and source refs;
- GBrain sync/import as substrate refresh path.

Strength:

- works locally;
- has fallback;
- source refs are visible;
- does not force full context loading;
- can search Vietnamese/English with simple FTS plus embeddings.

Weakness:

- A1 queries are often task-shaped, not keyword-shaped;
- top results can be broad architecture notes instead of the exact working
  context an A1 needs;
- query guidance exists but is passive;
- no eval corpus yet;
- no A1 retrieval success metric yet;
- context kinds are useful but agents may not choose them;
- freshness/status signals can be confusing;
- relation/link context is mostly trace refs, not surfaced in retrieval.

## Eval Corpus

Create a small corpus before changing ranking heavily.

### Current Coverage Caveat

The current 54-item corpus is now a two-project regression gate for AICOS
operating search plus a larger coding-heavy managed project. It is more useful
than the first 29-item AICOS-heavy corpus, but it is still not a broad
company-wide benchmark.

Current distribution:

- `projects/aicos`: 25 items
- `projects/sample-project`: 28 items
- `projects/mjnclaw`: 1 item

Latest expanded run on 2026-04-28:

- all items: `top3 53/54`, `top5 54/54`, `errors 0`
- `projects/aicos`: `top3 25/25`, `top5 25/25`, `errors 0`
- `projects/sample-project`: `top3 27/28`, `top5 28/28`,
  `errors 0`
- `projects/mjnclaw`: `top3 1/1`, `top5 1/1`, `errors 0`

Therefore a result such as `top5 54/54, errors 0` means:

- AICOS self-project retrieval and current A1/A2 operating questions are in
  good shape;
- sample project managed-project retrieval has a meaningful coding-heavy regression slice;
- there is still only smoke coverage for mjnclaw;
- it does **not** prove retrieval quality across many company/project shapes
  yet.

From this point, search or A1 retrieval changes should be checked against both
`projects/aicos` and `projects/sample-project`. Aggregate score alone is
not enough; the runner must show per-scope results so sample project regressions are not
hidden by AICOS successes.

Before using retrieval eval as a company-wide quality claim, add more cases
from at least:

- one coding-heavy project;
- one non-code/research/content project;
- one project with multiple active agents/lanes;
- one project with sparse/immature AICOS context.

### Corpus Shape

Each eval item should include:

```yaml
id: "<stable id>"
scope: "projects/<project-id>"
actor_role: "A1|A2-Core-C|A2-Core-R"
functional_role: "<optional project role>"
work_type: "code|research|planning|ops|..."
work_lane: "<lane>"
question: "<what the agent asks>"
expected_refs:
  - "<file/ref that should appear>"
expected_answer_shape: "<what a good answer should include>"
failure_mode_if_missing: "<what goes wrong>"
priority: "high|medium|low"
```

### Initial Eval Questions

| ID | Scope | Query | Expected refs | Why it matters |
| --- | --- | --- | --- | --- |
| `a1-start-next-work` | `projects/aicos` | "what should a new A1 read before starting work?" | startup bundle/context ladder/current state | tests onboarding retrieval |
| `a1-write-feedback` | `projects/aicos` | "how do I report MCP feedback or tool friction?" | write cookbook, MCP contract, feedback docs | tests learning loop usability |
| `a1-sample-portable-repo` | `projects/sample-project` | "where is the canonical sample project repo and branch?" | project profile/current state/project registry | tests portable source metadata |
| `a1-openclaw-connect` | `projects/mjnclaw` | "how does OpenClaw connect to AICOS MCP?" | mjnclaw current state/install docs | tests client-specific setup |
| `a2-phase-next` | `projects/aicos` | "what phase should AICOS do next after provider sketch?" | transition checklist, Phase 3 note | tests planning continuity |
| `a1-task-handoff` | any project with task state | "what is ready for takeover?" | handoff/status/task-state | tests coworker handoff |
| `a1-search-failure` | `projects/aicos` | "why is brain status stale but search works?" | PG stale false-signal status item | tests ops/debug retrieval |
| `a1-role-confusion` | `projects/aicos` | "is A1 a profession or service role?" | actor model normalization, role definitions | tests actor model clarity |

## Benchmark Plan

Run each eval question against:

1. direct read, when applicable;
2. markdown-direct query;
3. PostgreSQL FTS;
4. PostgreSQL hybrid;
5. hybrid with explicit `context_kinds`;
6. future relation-assisted retrieval only if needed.

Measure:

- expected ref in top 3;
- expected ref in top 5;
- snippet usefulness;
- whether stale/closed items polluted results;
- whether direct read would have been better than query;
- whether agent needed follow-up raw file reads.

## Reduction Strategy

Use eval results to decide what to reduce or wrap.

Keep custom:

- AICOS semantic read surfaces;
- source authority/freshness labels;
- small intent-to-context-kind hints;
- feedback loop when retrieval fails;
- query output as refs/snippets, not full dumps.

Wrap or constrain:

- PG/embedding implementation details behind Retrieval Provider boundary;
- GBrain sync as provider substrate, not product identity;
- daemon reindex/freshness status behind clearer health semantics.

Avoid building now:

- full graph engine;
- page schema/link graph migration;
- custom LLM reranker;
- broad ingestion/search framework;
- enterprise search adapter before company-100 profile needs it.

## Immediate Search Improvements That Are Low-Risk

These should be considered first because they do not make the system heavy:

1. Add a checked-in eval corpus file under AICOS evidence/working.
2. Add a small CLI/MCP eval command only after corpus shape is stable.
3. Improve query guide with A1 examples per task type.
4. Add search feedback type examples: "expected ref missing", "result too
   broad", "stale result", "needed direct read."
5. Make `aicos_query_project_context` nudge direct read tools when query intent
   clearly maps to startup/handoff/status.
6. Improve status freshness signal so A1 does not distrust working search.
7. Add context-kind auto-filter examples for common A1 tasks.

## Search Backlog

| Item | Type | Difficulty | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| Retrieval eval corpus | docs/data | low | low | do next |
| Eval runner for current query stack | CLI/test | medium | low | do after corpus |
| Query guide A1 examples | docs | low | low | do now/soon |
| Direct-read recommendation in query output | runtime small | medium | low | do after eval confirms patterns |
| Freshness/status false-signal fix | ops | medium | low | do soon |
| Schema/constants dedupe for MCP tools | refactor | medium | medium | do before more tools |
| Relation-assisted search from trace refs | runtime | medium/high | medium | defer until eval proves need |
| Graph/page schema engine | substrate | high | high | do not build now |
| External search product adapter | provider | high | medium | defer until company-100 profile |

## CTO Judgment

Search should become the next implementation focus, but in an eval-driven way.

The first practical pass should be:

1. create eval corpus;
2. run current search against it;
3. identify misses;
4. make small ranking/routing/doc changes;
5. only then decide whether relation graph, GBrain page/link patterns, or
   external search providers are justified.

This avoids the trap of solving weak A1 search by adding a large custom search
platform.
