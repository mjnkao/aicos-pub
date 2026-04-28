# AICOS Phase 3 Provider Interface Sketch

Status: phase-3 sketch
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Sketch minimal provider boundaries for Option C without building a provider
framework yet.

This pass is intentionally a contract sketch only:

- no new runtime code;
- no new adapters;
- no new dependency;
- no new queue/job/database;
- no migration away from the current small-team bundle.

## Design Rule

Provider interfaces should be extracted only where current implementation
already has real variation or likely replacement pressure.

Do not build a generic plugin platform before AICOS has stable semantic
contracts and at least one concrete reason to swap a provider.

## Provider Slots

## 1. Retrieval Provider

Purpose:

Return bounded context results for AICOS semantic queries.

Current implementation bundle:

- markdown-direct fallback in `mcp_read_serving.py`;
- PostgreSQL FTS/vector hybrid in `pg_search/`;
- GBrain import/sync as substrate refresh path.

Minimal interface shape:

```yaml
query:
  scope: "projects/<project-id>|shared"
  query: "<short query>"
  actor_context:
    actor_role: "<AICOS service actor>"
    agent_family: "<client family>"
    agent_instance_id: "<instance id>"
    work_type: "<work type>"
    work_lane: "<work lane>"
    logical_role: "<optional functional role>"
  filters:
    context_kinds: ["current_state|handoff|status_items|canonical|..."]
    include_stale: false
    max_results: 5

result:
  engine: "<provider id>"
  status: "fresh|stale|partial|degraded|unavailable"
  results:
    - ref: "<source ref>"
      title: "<short title>"
      summary: "<bounded summary>"
      kind: "<AICOS context kind>"
      authority: "high|medium|low"
      freshness: "fresh|aging|stale|stable"
      match_signals: ["fts|vector|metadata|graph|exact"]
  diagnostics:
    vector_status: "active|disabled|unavailable"
    warnings: []
```

Provider invariants:

- must return refs to authoritative objects;
- must return bounded summaries, not full dumps by default;
- must expose freshness/degraded state;
- must not define AICOS truth;
- must work without embeddings or degrade clearly.

What not to build now:

- no generic retrieval plugin loader;
- no Graphiti/Mem0/Onyx adapter yet;
- no custom ranking framework beyond current hybrid path;
- no eval-driven replacement until Phase 5.

## 2. Context Store Provider

Purpose:

Store and retrieve AICOS semantic objects.

Current implementation bundle:

- markdown files under `brain/`;
- generated derived views under `serving/`;
- runtime/index state outside authority.

Minimal interface shape:

```yaml
read_object:
  scope: "projects/<project-id>"
  object_type: "status_item|handoff|checkpoint|feedback|artifact_ref|..."
  object_id: "<id or path-safe key>"

write_object:
  scope: "projects/<project-id>"
  object_type: "<semantic object type>"
  semantic_payload: {}
  write_identity:
    actor_role: "<AICOS actor class>"
    agent_family: "<client family>"
    agent_instance_id: "<instance id>"
    work_type: "<work type>"
    work_lane: "<work lane>"

result:
  ref: "<canonical source ref>"
  write_id: "<id>"
  status: "success|rejected|conflict"
```

Provider invariants:

- must enforce semantic write contracts;
- must reject raw write bypasses for A1-facing continuity;
- must preserve source refs and audit identity;
- must not collapse canonical/working/evidence lanes;
- must support inspectability and portability at least for solo/small-team.

What not to build now:

- no PostgreSQL truth-store migration;
- no GBrain-as-truth migration;
- no multi-store replication system;
- no CRDT/conflict engine.

## 3. Jobs / Maintenance Provider

Purpose:

Run non-critical maintenance tasks.

Candidate jobs:

- sync/reindex;
- embedding refresh;
- health checks;
- feedback digest synthesis;
- stale status review;
- future connector imports.

Minimal interface shape:

```yaml
job_request:
  job_type: "sync|reindex|embedding_refresh|health_check|digest|import"
  scope: "projects/<project-id>|shared|all"
  priority: "low|normal|urgent"
  requested_by:
    actor_role: "<actor>"
    agent_family: "<family>"
    agent_instance_id: "<instance>"

job_status:
  job_id: "<id>"
  status: "queued|running|success|failed|skipped"
  started_at: "<timestamp>"
  finished_at: "<timestamp>"
  summary: "<bounded summary>"
  diagnostics: []
```

Provider invariants:

- jobs must not be required for semantic correctness unless explicitly marked
  critical;
- failures must be visible but not noisy;
- jobs must not mutate canonical truth silently;
- job output must be status/evidence, not hidden runtime state only.

What not to build now:

- no mandatory scheduler;
- no automation-driven architecture migration;
- no always-on worker fleet;
- no critical dependency on flaky desktop automation.

## 4. Auth / Audit Provider

Purpose:

Authenticate clients and preserve audit correlation.

Current implementation bundle:

- daemon bearer tokens;
- labeled extra tokens;
- request audit JSONL;
- health auth capabilities.

Minimal interface shape:

```yaml
auth_context:
  token_label: "<client token label>"
  client_profile: "codex-http|claude-desktop-local|openclaw-vm|..."
  remote_addr: "<ip>"

audit_event:
  timestamp: "<timestamp>"
  token_label: "<label>"
  tool: "<mcp tool>"
  scope: "<scope>"
  actor_role: "<actor>"
  agent_family: "<family>"
  agent_instance_id: "<instance>"
  work_type: "<work type>"
  work_lane: "<work lane>"
  status: "ok|tool_error|rpc_error|unauthorized"
  error: "<optional>"
  duration_ms: "<number>"
```

Provider invariants:

- auth identity and actor identity must stay separate;
- token labels help diagnose clients, but do not define project role;
- audit must preserve enough fields for feedback loop and handoff debugging;
- enterprise auth/SSO must not erase agent-family and instance identity.

What not to build now:

- no OAuth/SSO/RBAC system;
- no enterprise audit sink;
- no permission matrix beyond current semantic boundary rules.

## 5. Connector / Ingestion Provider

Purpose:

Bring external artifacts into AICOS as refs, evidence, or reviewed semantic
objects.

Possible sources:

- GitHub/repos;
- Plane/ClickUp;
- docs/wiki;
- chat/email;
- design artifacts;
- data outputs.

Minimal interface shape:

```yaml
ingest_ref:
  source_system: "github|plane|clickup|notion|google-docs|..."
  external_ref: "<url/id/path>"
  artifact_kind: "note|report|diff|output|analysis|design|content|other"
  scope: "projects/<project-id>"
  summary: "<why it matters>"
  authority_intent: "evidence|artifact_ref|working_candidate"

result:
  aicos_ref: "<stored ref>"
  status: "registered|queued_for_review|rejected"
```

Provider invariants:

- external sources do not become canonical truth without review;
- ingestion must preserve source refs;
- AICOS stores compact relevance, not full artifact bodies by default;
- connectors must not force one PM/tool model on all companies.

What not to build now:

- no Plane/ClickUp sync engine;
- no universal importer;
- no document lake;
- no company-wide knowledge ingestion before permission/authority rules are
  clearer.

## 6. Relation / Graph Provider

Purpose:

Represent links between AICOS objects and external artifacts.

Current implementation seed:

- trace refs in markdown;
- `relations/trace_refs.py`;
- status item/source refs;
- artifact refs.

Minimal interface shape:

```yaml
relation:
  from_ref: "<AICOS or external ref>"
  relation_type: "supports|blocks|updates|derived_from|mentions|supersedes"
  to_ref: "<AICOS or external ref>"
  confidence: "explicit|derived|inferred"
  source_ref: "<where relation came from>"
```

Provider invariants:

- explicit refs outrank inferred graph edges;
- graph output must cite source refs;
- graph must improve retrieval/handoff, not become a hidden authority layer;
- relation provider remains optional until retrieval evals prove it is needed.

What not to build now:

- no full page schema/link graph migration;
- no graph database;
- no inferred relation engine;
- no copying GBrain's page/link model wholesale.

## Current Bundle Mapping

| Provider slot | Current bundle | Profile |
| --- | --- | --- |
| Retrieval | markdown-direct + PG hybrid + optional embeddings | small-team |
| Context store | markdown truth under `brain/` | solo / small-team |
| Jobs | manual CLI + launchagents + optional maintenance scripts | small-team |
| Auth/audit | bearer tokens + JSONL audit | small-team |
| Connector/ingestion | manual docs + artifact refs + limited sync notes | solo / small-team |
| Relation/graph | trace refs only | solo / small-team |

## Scaling Guidance

For `solo`:

- keep markdown truth;
- local stdio/HTTP optional;
- no heavy provider requirements.

For `small-team`:

- keep current bundle;
- improve schema sharing and observability;
- avoid making desktop jobs critical.

For `company-100`:

- likely need stronger auth/audit provider;
- likely need more reliable jobs provider;
- likely need PM/dashboard connector;
- may need stronger retrieval provider;
- should still preserve AICOS semantic contracts.

## CTO Judgment

The current implementation should be treated as the first provider bundle, not
as the final architecture.

The highest-value next implementation work is not to build all providers. It is
to remove drift and duplication:

1. centralize shared MCP schema/constants;
2. stop duplicating tool schemas between HTTP daemon and stdio adapter;
3. keep PG/GBrain/search behavior behind retrieval-provider-like boundaries;
4. keep jobs/monitoring non-critical until a jobs provider is deliberately
   designed.

This keeps AICOS scalable without turning Phase 3 into a big self-built
platform.
