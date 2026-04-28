# AICOS Phase 2 Semantic Core Boundary

Status: phase-2 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Define what AICOS owns regardless of substrate choice, and what must remain
provider-owned. This is the Phase 2 boundary document after the Phase 1 module
inventory.

This pass is intentionally documentation and architecture framing only. It does
not add runtime code, providers, daemons, jobs, queues, databases, dashboard
logic, or PM sync logic.

## Core Principle

AICOS owns project-context semantics and coordination semantics.

AICOS does not need to own every implementation substrate that can support
those semantics.

The semantic core must stay stable enough that a company can swap or vary
retrieval, memory store, graph, jobs, auth, audit, and connector providers
without changing what AICOS means.

## AICOS Semantic Core Owns

### 1. Authority Model

AICOS owns the meaning and precedence of:

- company / workspace / project / workstream scope;
- canonical truth;
- working state;
- evidence and raw intake;
- historical/handoff continuity;
- generated serving views;
- runtime/provider state;
- external artifact references.

Invariant:

- `brain/` remains the durable context/control-plane authority in the current
  small-team bundle.
- `serving/` remains derived and review-facing, not authority.
- `backend/` and provider indexes remain substrate state, not truth.
- external project repos remain code/runtime authority for their own artifacts.
- PM tools can be shared collaboration surfaces, but do not automatically become
  AICOS semantic authority.

### 2. Object Model

AICOS owns these object semantics:

- company
- workspace
- project
- workstream
- task packet
- status item
- checkpoint
- handoff
- feedback
- artifact ref
- context registry entry
- project registry entry
- startup bundle
- project health
- audit/trace correlation record

Invariant:

- providers may store, index, summarize, or display these objects;
- providers must not redefine what these objects mean;
- provider-specific fields must remain implementation metadata unless promoted
  through an AICOS semantic contract.

### 3. Coordination Semantics

AICOS owns the coordination fields and their meanings:

- `actor_role`
- `agent_family`
- `agent_instance_id`
- `agent_display_name`
- `work_type`
- `work_lane`
- `execution_context`
- `artifact_scope`
- `artifact_refs`
- `worktree_path`
- `work_branch`
- `coordination_status`
- `startup_bundle_ref`
- `packet_ref`
- `handoff_ref`

Invariant:

- `agent_family` is the client/tool/product family, not the AICOS actor class.
- `agent_instance_id` is required for audit and handoff correlation.
- `work_lane` is a stable coordination key across code and non-code work.
- code work must expose `worktree_path`; non-code work should expose
  `artifact_scope` and `artifact_refs`.
- empty active task state does not prove a project is idle; continuity and
  status-item surfaces must also be checked.

### 4. Read/Write Contracts

AICOS owns semantic read/write contracts:

- startup bundle;
- handoff current;
- packet index;
- task packet;
- status items;
- workstream index;
- context registry;
- project registry;
- feedback digest;
- project health;
- bounded project context query;
- checkpoint write;
- task update write;
- handoff update write;
- status item update;
- artifact reference registration;
- feedback record.

Invariant:

- MCP write tools are semantic intent writes, not raw file-write APIs.
- session-close writes require a feedback closure or `feedback_type=no_issue`.
- clients must include write contract acknowledgement.
- read surfaces must include audit identity fields.
- write tools must remain bounded enough that external A1 agents can use them
  without understanding internal markdown paths.

## Providers Own

The following are provider or runtime-service responsibilities, not semantic
core identity:

- retrieval/search implementation;
- embedding model and vector store;
- markdown-direct fallback mechanics;
- GBrain import/sync mechanics;
- graph/relation engine implementation;
- background job scheduling;
- daemon transport;
- auth token storage;
- audit sink storage;
- dashboard UI implementation;
- PM tool connector implementation;
- chat/doc/repo ingestion implementation.

Invariant:

- AICOS can depend on providers operationally, but semantic truth must not be
  encoded only in provider-specific tables, caches, pages, or generated output.

## Current De Facto Semantic Core Modules

These modules currently carry semantic core behavior:

| Module | Current semantic responsibility | Boundary issue |
| --- | --- | --- |
| `packages/aicos-kernel/contracts/` | contracts for actor classes, lanes, MCP bridge, promotion, branching | good place for stable invariants |
| `packages/aicos-kernel/schemas/` | object shape hints for capsules, feedback, project reality, options | schemas need future normalization around semantic object model |
| `mcp_contract_status.py` | write contract compatibility | small and healthy |
| `mcp_read_serving.py` | read surfaces, startup, status, feedback digest, query fallback, health | mixes semantic assembly, markdown parsing, feedback loop, and fallback retrieval |
| `mcp_write_serving.py` | write validation, semantic write mapping, feedback closure, markdown writes | mixes semantic contract with markdown storage implementation |
| `context_registry.py` | source registry generation | should later become semantic registry + provider source metadata |
| `agent-repo/classes/` | actor operating rules/onboarding | useful, but A1/A2 taxonomy must remain AICOS-internal |
| `brain/projects/aicos/canonical/role-definitions.md` | current role boundary | should be aligned with this Phase 2 note |

These modules are provider/runtime rather than semantic core:

| Module | Current role |
| --- | --- |
| `pg_search/` | current Retrieval Provider implementation |
| `integrations/mcp-daemon/` | HTTP runtime service and deployment concern |
| `integrations/local-mcp-bridge/` | transport/client adapter |
| `tools/gbrain/` and GBrain wrapper | current small-team substrate provider |
| `backend/` | substrate notes/state, not authority |
| `serving/` | generated review/serving surfaces, not authority |

## Extraction Map

When implementation refactor begins, prefer this sequence:

1. Extract semantic constants and enums from daemon/stdout adapters into one
   shared contract source.
2. Split `mcp_read_serving.py` into:
   - semantic read assembly;
   - markdown source parsing;
   - fallback retrieval;
   - feedback loop/project health helpers.
3. Split `mcp_write_serving.py` into:
   - write contract validation;
   - semantic write object normalization;
   - markdown store writer;
   - feedback-closure policy.
4. Split `aicos_mcp_daemon.py` into:
   - HTTP MCP transport;
   - auth/audit;
   - tool schema publication;
   - provider wiring;
   - reindex/health operations.
5. Keep `pg_search/` as the first Retrieval Provider implementation until an
   eval corpus proves replacement or deeper abstraction is worth it.

Do not start by building a generic plugin framework. Start by moving repeated
semantic constants and provider-specific logic behind narrow seams that already
exist in the code.

## Provider Invariants

Any future provider must obey these invariants:

1. **Authority preservation**
   - A provider may index or cache AICOS objects, but must expose source refs
     back to the authoritative AICOS object or external artifact.

2. **Bounded context**
   - A provider must not force agents to load entire repos, whole histories, or
     unbounded generated bundles for normal startup.

3. **Freshness visibility**
   - A provider must expose whether its view is fresh, stale, partial, or
     degraded.

4. **Degraded operation**
   - Retrieval/search providers must degrade without making AICOS unusable.

5. **Traceability**
   - A provider must preserve enough identity and source metadata for handoff,
     audit, and debugging.

6. **No hidden promotion**
   - A provider must not promote working/evidence/generated material into
     canonical truth.

7. **No raw write bypass for A1**
   - A provider must not encourage external A1 agents to write AICOS-facing
     continuity by editing markdown files directly.

8. **Project/runtime split**
   - A provider must not confuse external project repo/runtime artifacts with
     AICOS context/control-plane authority.

9. **No single-provider lock-in**
   - A provider must not introduce semantic behavior that cannot be described
     in AICOS contracts.

10. **Operator clarity**
   - Health/status reports must distinguish actual retrieval failure from
     provider freshness warning or monitor false signal.

## Scalability / Bloat Judgment

This Phase 2 boundary reduces risk rather than adding weight:

- no runtime code was added;
- no new provider was introduced;
- no dashboard/PM integration was started;
- no graph/page schema was added;
- no background job dependency was made mandatory.

The main scalability risk remains architectural drift: adding convenient
features into `kernel.py`, `mcp_read_serving.py`, `mcp_write_serving.py`, or
`aicos_mcp_daemon.py` before extracting the semantic/provider boundary.

## Next Step

Use this note plus the actor model normalization note as input for:

- a small shared contract/constants extraction plan;
- provider interface sketches for retrieval, context store, jobs, auth/audit;
- dashboard/PM integration semantics later, not now.
