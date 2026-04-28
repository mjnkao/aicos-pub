# AICOS Retrieval Baseline

Status: initial baseline
Date: 2026-04-28
Scope: projects/aicos
Corpus: `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`

## Purpose

Record the first AICOS retrieval baseline after Phases 4-7, focused on whether
A1/A2 agents can find expected context refs through HTTP MCP
`aicos_query_project_context`.

## Method

- Query surface: `aicos_query_project_context`
- Transport: HTTP MCP daemon
- Engine observed: `postgresql_hybrid`
- Max results: 5
- Corpus size: 10 questions
- Hit metric:
  - top-3 hit: at least one expected ref appears in top 3
  - top-5 hit: at least one expected ref appears in top 5

## Result

- Top-3 hit: 9/10
- Top-5 hit: 10/10

This is better than expected for the first small corpus, but the misses reveal
useful product issues.

## Per-Item Summary

| ID | Priority | Top-3 | Top-5 | Notes |
| --- | --- | --- | --- | --- |
| `a1-aicos-start-next-work` | high | yes | yes | `context-ladder` ranked #1; `current-state` #3. Good enough, but `current-direction` did not appear. |
| `a1-aicos-report-feedback` | high | yes | yes | Learning-loop note ranked #1. Cookbook/contract did not rank because install docs are not indexed through `brain/`. |
| `a1-sample-canonical-repo` | high | yes | yes | Project profile #1, current-state #2. Good. |
| `a1-mjnclaw-connect-openclaw` | high | no | yes | Setup LAN task ranked #4; current-state/context-ladder did not appear. Needs search improvement. |
| `a2-aicos-next-phase` | high | yes | yes | Transition checklist ranked #3. Search focus status did not rank. Good but could be more directive. |
| `a1-aicos-role-confusion` | high | yes | yes | Actor model note ranked #2. Good. |
| `a1-aicos-brain-status-stale` | high | yes | yes | False-stale status #1 and GBrain EISDIR #3. Good. |
| `a1-aicos-dashboard-coworker` | medium | yes | yes | Coworker #1, PM integration #2. Good. |
| `a2-aicos-provider-boundary` | medium | yes | yes | Provider sketch #1, semantic boundary #2. Good. |
| `a1-aicos-deployment-profile` | medium | yes | yes | Phase 4 profile #1, status #3. Good. |

## Findings

### 1. Context-kind filtering helps but is not enough

The mjnclaw query used `current_state`, `current_direction`, `handoff`,
`task_state`, and `canonical`, but task-state and current-direction outranked
current-state/context-ladder. This is acceptable for some operational queries,
but weak for startup/setup guidance.

### 2. Install docs are not in the indexed brain set

The feedback/cookbook query expected:

- `docs/install/AICOS_MCP_WRITE_COOKBOOK.md`
- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`

The learning-loop note ranked #1, which is useful. But A1 agents still need
payload examples from install/cookbook docs. Those docs currently live outside
the default `brain/` sync/index path.

This does not mean all `docs/` should be indexed. It means AICOS needs either:

- explicit artifact refs for important non-brain docs; or
- a curated index allowlist for A1-facing docs/install files.

### 3. Read identity can distort evals if not modeled correctly

Initial sample project eval used `work_type=code` without `worktree_path`, causing a read
identity error instead of a search result. For startup/source discovery before
a checkout exists, eval should use `work_type=orientation`.

This is not a search ranking bug. It is an eval/caller-shape issue.

## Low-Risk Next Fixes

1. Add artifact refs or curated brain-facing pointers for A1-critical install
   docs:
   - MCP write cookbook;
   - query/search guide;
   - full install guide;
   - VM/OpenClaw HTTP MCP guide.
2. Improve mjnclaw current-state/context-ladder retrieval:
   - add clearer setup/search terms in current-state or context ladder;
   - or add a status item pointing to canonical OpenClaw MCP setup refs.
3. Add query guide examples from this corpus.
4. Add a small eval runner only after the corpus stabilizes.
5. Add direct-read suggestions in query output only after confirming repeated
   patterns.

## Quick Fixes Applied In This Pass

These were done immediately because they do not add a new search engine,
provider, daemon, graph, or indexing of the whole `docs/` tree:

- Added an A1-oriented examples section to
  `docs/install/AICOS_QUERY_SEARCH_GUIDE.md`.
- Registered searchable AICOS artifact refs for:
  - `docs/install/AICOS_MCP_WRITE_COOKBOOK.md`
  - `docs/install/AICOS_QUERY_SEARCH_GUIDE.md`
  - `docs/install/AICOS_VM_AGENT_HTTP_MCP_CONNECT.md`
- Registered a project-local mjnclaw artifact ref for the VM/OpenClaw MCP
  guide.

After registering the mjnclaw artifact ref, the query
`how does OpenClaw connect to AICOS MCP` returned the guide ref at rank #1
inside `projects/mjnclaw`, while the existing setup task remained in top 5.

## Do Not Do Yet

- Do not add graph/page schema based on one top-3 miss.
- Do not add an LLM reranker.
- Do not replace PG hybrid.
- Do not index all repository docs indiscriminately.
- Do not make A1 agents read more context to compensate for ranking.

## Judgment

Search is not broken, but it is not yet A1-native.

The next best improvement is not heavier retrieval. It is better routing and
better availability of A1-facing guide refs inside the searchable AICOS context
surface.
