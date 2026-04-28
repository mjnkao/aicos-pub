# AICOS Thin Relation Model Proposal

Status: research / proposal  
Date: 2026-04-24  
Scope: `projects/aicos`

## Why this exists

AICOS already has good primary surfaces for:

- project registry
- context registry
- workstream index
- task packets
- status items
- checkpoints / handoffs
- artifact refs

But the relationships between those surfaces are still mostly implicit. For
larger projects with multiple lanes, this creates the usual costs:

- agents re-read too much because adjacency is weak
- evidence, decisions, tasks, and working items are connected by prose, not
  by a stable typed relation layer
- query surfaces can find relevant documents, but they are still weaker at
  answering "what is related to this active thing?"

GBrain is useful reference here. The right lesson is not "copy the whole
personal-brain schema", but:

1. every object should have a primary home
2. adjacency should be explicit
3. graph power should come from lightweight typed links before any large graph
   subsystem is introduced

## AICOS design constraint

Do not introduce:

- a second truth store
- a heavy graph database
- a universal entity system for everything
- a broad migration of existing markdown into a new canonical schema

Keep:

- markdown truth
- MCP as control-plane boundary
- PostgreSQL/FTS/vector as serving/index layer

## Proposed model

Add a **thin relation layer** that is:

- markdown-truth compatible
- derived/indexable
- typed
- cheap to add incrementally

The relation layer should treat existing AICOS primitives as nodes:

- project
- workstream
- task_packet
- status_item
- checkpoint
- handoff
- artifact
- evidence_doc
- policy_doc
- contract_doc
- actor_instance
- external_repo
- worktree
- decision_candidate

## Relation shape

Use typed edges with small stable fields:

```yaml
relation_type: "<typed edge>"
from_ref: "<repo-relative source ref>"
to_ref: "<repo-relative source ref or external artifact ref>"
scope: "projects/<project-id>"
status: "active|historical|candidate"
reason: "<short human-readable justification>"
```

## Recommended typed edges

Start with a very small set:

- `implements`
- `tracks`
- `blocks`
- `depends_on`
- `evidenced_by`
- `updates`
- `handoff_for`
- `belongs_to_workstream`
- `occupies_worktree`
- `targets_repo`
- `promotes_from`
- `related_to`

This set is enough to model most project continuity without pretending AICOS
already has a full knowledge graph.

## Primary-home rule

The source object stays in its current primary home:

- status item stays in `working/status-items/`
- task packet stays in `agent-repo/.../task-packets/`
- checkpoint stays in `evidence/checkpoints/`
- handoff stays in `working/handoff/current.md` or `episodes/`

The thin relation layer does **not** replace those homes.

## Low-risk implementation path

### Phase 1 — relation hygiene using existing fields

Use and normalize existing fields first:

- `source_ref`
- `artifact_refs`
- `Trace Refs`
- `source_refs` in MCP metadata
- workstream/task packet/project registry refs

Goal:

- write better explicit refs before inventing new primitives

### Phase 2 — derived relation index

Build a derived index from those refs, not a new truth store.

Possible output:

```yaml
source_ref: "brain/projects/aicos/working/status-items/aicos-learning-loop-mvp.md"
node_kind: "status_item"
outgoing:
  - relation_type: "evidenced_by"
    to_ref: "packages/aicos-kernel/aicos_kernel/mcp_read_serving.py"
  - relation_type: "evidenced_by"
    to_ref: "packages/aicos-kernel/aicos_kernel/mcp_write_serving.py"
  - relation_type: "belongs_to_workstream"
    to_ref: "workstream:aicos-learning-loop"
```

This can live initially as:

- generated JSON under runtime/index
- or a compact derived markdown/JSON registry for serving

### Phase 3 — targeted read/query primitive

Only if Phase 2 proves useful, add one read surface such as:

- `aicos_get_related_context`

with a bounded query:

```yaml
scope: "projects/<project-id>"
source_ref: "<known node ref>"
relation_types: ["blocks", "depends_on", "evidenced_by"] # optional
max_results: 10
```

## What not to do

- do not model every heading as a node
- do not turn free text into graph truth automatically without review
- do not introduce a second canonical source for tasks/status/handoffs
- do not require all historical documents to be backfilled before value exists

## Immediate practical gains if done well

- better "what should I read next?" routing
- better relation-aware startup bundles for active lanes
- easier task/evidence/status adjacency for large projects
- cleaner future search ranking features without changing truth architecture

## Best next step

Do not code a graph subsystem first.

Do this first:

1. normalize relation hygiene in write/docs/templates
2. define the thin relation edge vocabulary
3. test a derived relation index on AICOS + one active project
4. only then decide whether a read primitive is justified

## Judgment

This is compatible with AICOS direction.

It learns the right thing from GBrain:

- primary home
- explicit adjacency
- derived relation power

without importing GBrain's personal-brain schema or overbuilding a graph
platform too early.
