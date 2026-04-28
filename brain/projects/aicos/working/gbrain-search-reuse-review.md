# GBrain Search Reuse Review

Status: active architecture note
Updated: 2026-04-23

## Purpose

Decide how AICOS should reuse or learn from GBrain for search/context
intelligence without making GBrain an implicit AICOS authority.

## Current Judgment

GBrain is valuable as an AI-native retrieval substrate and pattern source. AICOS
should reuse its proven ideas before expanding custom search code, but AICOS
must keep its own authority and MCP boundaries.

## Reuse Now

AICOS should reuse these GBrain patterns directly in design and implementation:

- search modes: direct/get, keyword search, hybrid semantic query;
- keyword-first fallback when embeddings are unavailable;
- vector plus keyword fusion using RRF;
- result snippets first, then load source/full context only when needed;
- explicit health/freshness/coverage reporting;
- embedding stale detection by content hash and embedded timestamp;
- HNSW/pgvector index pattern;
- search result boundary: chunks/snippets are evidence pointers, not truth.

## Deeper Review: Schema, Links, Jobs

After the first search review, the most useful additional lessons from GBrain
are not just ranking details. They are:

### 1. Primary home + resolver discipline

GBrain is strict that each knowledge object has one primary home and adjacency
is preserved through links instead of duplicate pages.

For AICOS, the lesson is:

- keep project truth in existing homes (`status-items`, task packets, handoff,
  checkpoints, evidence, registry files)
- do not create parallel summary or graph truth files casually
- strengthen routing/resolver rules so agents know where an object belongs
  before they create another representation of it

This is useful immediately for project-scale AICOS work because many AICOS
surfaces are already close to "one primary home", but cross-surface adjacency
is still weak.

### 2. Thin typed adjacency before heavy graph

GBrain's relationship/graph thinking is valuable, but AICOS should not jump to
a heavy graph subsystem. The right immediate move is:

- normalize explicit refs (`source_ref`, `artifact_refs`, workstream refs,
  packet refs, registry refs)
- define a small typed relation vocabulary
- derive relation/index views from existing truth surfaces

This gives AICOS better "what is related to this?" routing without changing the
truth-store strategy.

### 3. Jobs as maintenance discipline, not feature theater

GBrain's cron/maintain/live-sync model is strong because jobs are not random
automation. They enforce operational disciplines:

- sync after writes
- doctor/verify regularly
- refresh stale embeddings
- benchmark retrieval after major changes
- run maintenance loops that keep the knowledge graph from silently degrading

For AICOS, the useful translation is:

- recurring retrieval/health review
- recurring doc/client-compatibility drift review
- recurring search-eval review
- recurring relation-hygiene review

Do not import the full "dream cycle" or personal-brain ingestion stack into
AICOS. Use the maintenance discipline, not the product surface.

### 4. Skills define search behavior better than code alone

GBrain's query and maintain skills encode high-quality operational behavior:

- choose the right search mode
- chunks first, full page second
- compare keyword vs hybrid when quality seems off
- treat stale/coverage/health as first-class debugging signals

This is a strong fit for AICOS. AICOS should likely have its own lightweight
query/search operating guide or skill rather than relying only on daemon code
and CLI flags.

## Do Not Reuse Blindly

Do not import the whole GBrain page model into AICOS now.

Reasons:

- AICOS project truth is markdown under `brain/`, not GBrain pages.
- AICOS needs actor/project/lane/control-plane metadata that GBrain does not own.
- AICOS MCP tools must preserve project authority mapping and write contracts.
- AICOS has multi-project context boundaries that should not be hidden in a
  generic personal-brain schema.

## AICOS-Specific Code To Keep

Keep AICOS-owned code for:

- MCP read/write contracts and fallback behavior;
- actor identity and work-lane metadata;
- project registry and cross-project boundaries;
- context-kind/authority mapping from AICOS repo paths;
- status item, feedback, handoff, and artifact-ref surfaces;
- daemon auth and team/LAN serving behavior.

## Candidate Future Reuse

Review before adding more custom code:

- GBrain chunker for long docs;
- GBrain embedding batching/concurrency behavior;
- GBrain query expansion;
- GBrain health schema;
- GBrain stale-alert pattern;
- GBrain direct-get style for known context refs.
- GBrain eval/benchmark discipline for retrieval quality;
- GBrain maintenance workflow for stale links / stale synthesis checks.

## Immediate AICOS Actions Supported By This Review

Low-risk actions that fit AICOS now:

1. define and test a thin typed relation model derived from existing refs
2. add a lightweight AICOS query/search guide that teaches:
   - direct vs keyword vs hybrid
   - snippets first, full doc second
   - how to debug stale/embedding/freshness issues
3. add recurring review of retrieval quality and client-compatibility drift

Detailed architecture mapping and reuse judgment now live in:

- `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`

Higher-risk actions that should wait:

1. heavy graph traversal/runtime graph store
2. importing GBrain's personal-brain schema into AICOS truth surfaces
3. broad ingestion/job surface unrelated to AICOS control-plane needs

## Boundary

GBrain may serve as a substrate or pattern library. It must not become AICOS
source of truth unless a future ADR explicitly changes the truth-store strategy.
