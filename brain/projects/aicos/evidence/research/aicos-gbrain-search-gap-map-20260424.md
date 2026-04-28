# AICOS vs GBrain Search Gap Map

Status: research / architecture mapping  
Date: 2026-04-24  
Scope: `projects/aicos`

## Purpose

Make the reuse decision concrete:

- what GBrain does well;
- what AICOS already has;
- what is still missing;
- what can be copied directly, what must be adapted, and what should not be
  copied.

This note is intentionally specific to search, query, retrieval discipline, and
 context adjacency. It is not a proposal to replace AICOS truth or MCP
 boundaries with GBrain.

## Overall Judgment

GBrain is strongest as:

1. a retrieval operating model;
2. a search/query discipline with clear mode boundaries;
3. a resolver/link-oriented knowledge discipline;
4. a maintenance/verification loop for search quality and freshness.

AICOS has already reused the safest and highest-leverage parts:

- direct vs bounded query guidance;
- hybrid search + FTS fallback;
- embedding freshness/coverage observability;
- snippets-first reading discipline;
- primary-home / resolver direction;
- lightweight relation-hygiene audit.

AICOS has **not** yet fully reused the harder parts:

- retrieval evaluation discipline;
- strong direct-get object model;
- chunk-aware long-doc retrieval;
- relation-aware serving, not just relation audit.

## Mapping Table

| GBrain part | GBrain strength | AICOS equivalent | AICOS already has | AICOS still lacks | Reuse decision | Difficulty | Suggested pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Search mode split (`get` / `search` / `query`) | Forces exact-vs-keyword-vs-semantic discipline; avoids overusing one mode | MCP read tools + `aicos_query_project_context` + raw file fallback | Direct structured reads, bounded query guide, fallback rules | No single "known-ref direct get" primitive; mode arbitration still mostly guide-level, not behavior-level | Adapt | Medium | Pass 1 |
| Brain-first lookup discipline | Keeps agent from broad over-reading or jumping to raw repo too early | `AICOS_QUERY_SEARCH_GUIDE.md`, startup bundles, bounded query | Smallest-correct-path guide, snippets-first guide | Not enforced strongly in tooling; depends on agent compliance | Adapt | Low | Pass 1 |
| Verify / doctor / stats loop | Retrieval quality treated as an operational surface, not a side effect | `./aicos brain status`, sync, health, audit | Freshness/coverage/stale visibility, sync and audit commands | No search eval harness; no query benchmark set; no regression loop for retrieval quality | Adapt | Medium | Pass 1 |
| Stale-only embedding refresh | Controls cost; keeps embeddings current without full rebuild every write | Background embedding refresh, stale detection, coverage reporting | `text-embedding-3-small` default, stale-only behavior, cost guardrails | Better rate-limit policy and retry policy still open | Copy/adapt lightly | Low | Already in place; tune in Pass 1 |
| Hybrid search with keyword fallback | Robust retrieval when embeddings are unavailable or weak | PG hybrid + FTS + markdown fallback | Implemented in daemon/runtime | Need proof via eval, not just runtime health | Copy/adapt lightly | Low | Already in place; evaluate in Pass 1 |
| Query expansion / query shaping | Helps semantic retrieval when user wording differs from stored wording | `aicos_query_project_context` heuristics | Basic bounded query only | No explicit query expansion or reformulation layer | Adapt cautiously | Medium | Pass 3 |
| Chunk-first retrieval | Returns the right passage quickly; reduces whole-doc loading | Snippets from query results, summary extraction | Compact snippets, summary extraction improved | No real chunk model per context kind; still mostly doc-level retrieval | Adapt heavily | High | Pass 2 |
| Direct object fetch by stable id/slug | Known object can be fetched directly without search | Potential future `get` primitive for known refs | Some specific reads by surface exist | No universal direct-get for status item/checkpoint/artifact/contract known refs | Adapt heavily | Medium | Pass 2 |
| Primary home + resolver | Prevents duplicate truth; makes adjacency reliable | `brain/RESOLVER.md`, current AICOS primary homes | Resolver note and architecture direction exist | Needs more explicit resolver usage in docs/templates and maybe per-lane README discipline | Adapt | Low | Pass 1 |
| Link graph / typed adjacency | Better answers to "what is related to this?" | Thin relation model, Trace Refs, artifact/source refs | Proposal exists, `./aicos audit relations` exists, derived audit index exists | Relation vocabulary still small; no relation-aware serving; many relations still implicit in prose | Adapt heavily | High | Pass 2 |
| Skills encode retrieval behavior | Good search behavior lives in instructions/skills, not only engine code | Query/search guide, install docs, MCP cookbook | AICOS has guide docs and some routing discipline | No dedicated search skill or stronger query behavior card for agents yet | Adapt | Medium | Pass 2 |
| Jobs / recurring maintenance | Search quality, stale links, compatibility drift reviewed continuously | Nightly maintenance helper, health monitor, paused automation experiments | Light maintenance helpers exist | Automation semantics unstable; no stable recurring eval loop yet | Adapt cautiously | Medium | Pass 3 |
| Page schema / compiled pages / personal-brain model | Strong for one knowledge domain with page homes and cross-links | AICOS markdown truth across many context kinds | AICOS keeps markdown truth and object homes | AICOS objects are heterogeneous; direct page schema import would blur authority and over-canonicalize working surfaces | Do not copy directly | High | Never directly; only learn principles |
| Skillpack / integrations ecosystem | Rich product surface around personal knowledge work | AICOS MCP + project control-plane | Some client-specific install and query docs | Not the same product shape; ingestion stack does not map cleanly to AICOS needs | Do not copy directly | High | Never directly |

## Concrete Examples: What AICOS Can Reuse

### Safe to reuse now

1. **Mode discipline**
   - exact/direct read when the object is already known
   - keyword search when terms are known
   - hybrid search when the question is semantic or approximate

2. **Search health discipline**
   - stale vs fresh is visible
   - coverage is visible
   - missing embeddings are visible
   - sync/refresh is a named operation, not an implicit side effect

3. **Resolver thinking**
   - each AICOS object has a primary home
   - links/refs provide adjacency
   - avoid duplicate truth pages

4. **Maintenance discipline**
   - retrieval drift should be reviewed
   - compatibility drift should be reviewed
   - stale relation/index issues should be surfaced

## Concrete Examples: What AICOS Cannot Copy Blindly

### A. Eval corpus

An AICOS retrieval eval set must reflect **AICOS work**, not GBrain's page
model.

Examples of AICOS eval queries:

1. "Where is the current rule that requires feedback closure before a
   session-close write?"
2. "Which file explains why `worktree_path` is required for `work_type=code`?"
3. "What is the current guidance for Claude Desktop vs Claude Code vs Codex
   MCP install?"
4. "Which status item tracks LAN security hardening?"
5. "What evidence explains why query-token auth was rejected?"
6. "What current file tells an A2-Core maintainer where to start reading?"
7. "What in AICOS currently says relation audit should remain audit-only?"
8. "Which docs mention `orientation/intake` bootstrap values for first-contact
   reads?"

These are not directly copyable from GBrain because GBrain's natural eval
questions look more like:

- find page by slug/topic;
- locate notes, people, companies, calls, or meetings;
- answer over personal-knowledge pages and compiled summaries.

AICOS has a different object mix:

- status items
- handoff
- policy/contract docs
- task packets
- checkpoints
- feedback
- workstream indexes
- project registry
- project health

So the **discipline** is reusable, but the **eval corpus** must be authored for
AICOS reality.

### B. Retrieval questions that cannot be copied directly

Questions GBrain is naturally good at:

- "What do I know about person X?"
- "Show the page for company Y."
- "What happened across these notes over time?"

AICOS-specific retrieval questions are structurally different:

- "What should an A1 agent read first for this project and role?"
- "Which currently-open status item is the control-plane owner for this risk?"
- "What active handoff and checkpoint evidence support this rule?"
- "Which workstream or packet is authoritative for this lane?"
- "Is this result current working truth, policy, evidence, or history?"

These require stronger object typing and authority mapping than a generic page
retrieval stack.

## Why AICOS Would Drift If It Imported GBrain Page Schema / Link Graph Directly

This is the main architectural caution.

### 1. GBrain page model assumes a more uniform object world

GBrain is comfortable treating knowledge objects as "pages" with a strong
primary home plus links.

AICOS does **not** live in one uniform page world. Its context kinds are very
different:

- `current-state`
- `current-direction`
- handoff
- status item
- task packet
- checkpoint
- feedback
- policy doc
- contract doc
- artifact ref
- project registry entry
- workstream index entry

If AICOS imported a page-first model too literally, it would pressure these
different surfaces to behave like one generalized page system. That would blur
their purpose and make authority weaker.

### 2. AICOS must preserve authority boundaries

AICOS is not only a knowledge base. It is a control-plane.

It must preserve:

- `brain/` markdown truth;
- MCP read/write contract boundaries;
- project/runtime authority split;
- difference between working truth, evidence, history, and policy.

A broad page/link graph import tends to flatten these distinctions:

- working state starts to look like a page;
- evidence starts to look like a peer truth object;
- summaries and graph views risk turning into second truth surfaces.

That would be a real architectural drift.

### 3. AICOS would over-canonicalize high-churn working surfaces

Handoff, status items, feedback, and checkpoints are high-churn surfaces.

If those get recast too early into a canonical graph/page model:

- writes become heavier;
- agents must satisfy more structure before they can make progress;
- the system becomes slower to operate;
- graph maintenance starts competing with actual project work.

The right move is to keep these surfaces lightweight and derive relation power
from them, not force them into a large canonical entity system.

### 4. Link graph power is still useful, but must stay derived first

The right adaptation is:

1. keep markdown truth in current homes;
2. improve explicit refs and resolver discipline;
3. derive typed relation indexes from those refs;
4. only later add bounded relation-aware read primitives if the audit path
   proves useful.

That is why `./aicos audit relations` is aligned with AICOS, while "import a
page/link graph model" would be overreach.

## Recommended Pass Order

### Pass 1 — strengthen discipline, not architecture

- clean freshness/health/retry discipline;
- create AICOS retrieval eval corpus and benchmark harness;
- sharpen resolver and mode-selection docs.

### Pass 2 — improve retrieval quality without changing truth

- add direct-get for known refs where clearly justified;
- introduce chunking rules by context kind;
- strengthen relation hygiene and typed adjacency vocabulary.

### Pass 3 — add bounded serving improvements if Pass 2 proves value

- relation-aware read primitive;
- query expansion for difficult semantic retrieval;
- maintenance jobs / recurring eval loop once runtime semantics are stable.

## Practical Recommendation

Do **not** frame the next step as "use more GBrain code".

Frame it as:

1. reuse more of GBrain's operating discipline;
2. add the minimum AICOS-native primitives that GBrain's discipline exposes as
   missing;
3. keep truth and control-plane boundaries unchanged.

That gives AICOS more of GBrain's strength without importing the wrong product
shape.
