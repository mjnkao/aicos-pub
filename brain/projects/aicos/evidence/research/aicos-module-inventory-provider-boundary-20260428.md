# AICOS Module Inventory And Provider Boundary

Status: P2 baseline inventory
Date: 2026-04-28
Scope: `projects/aicos`
Actor: A2-Core-C

## Purpose

Classify current AICOS implementation surfaces into keep, reuse/wrap,
migrate/fork candidate, defer, or retire, using the Option C north-star and the
GBrain-inspired search checklist.

This is not a migration approval. It is a sequencing tool so future work knows
which parts are AICOS-owned semantics and which parts are replaceable substrate.

## Decision Legend

- **Keep/Core**: AICOS-owned semantic/control-plane responsibility.
- **Keep/Projection**: useful implementation, but must remain derived from
  markdown/MCP truth.
- **Reuse/Wrap**: prefer provider/substrate reuse behind an AICOS boundary.
- **Migrate Candidate**: evaluate migration after eval/usage evidence.
- **Defer**: do not build now.
- **Retire/No New Work**: keep only for compatibility/provenance.

## Inventory

| Area | Current Surface | Decision | Reason | Next Action |
| --- | --- | --- | --- | --- |
| Markdown truth | `brain/`, `agent-repo/`, contracts, policies | Keep/Core | Durable, human-readable source of truth; aligned with GBrain repo-as-system-of-record model | Preserve; do not move working truth to PG |
| MCP semantic read/write | `mcp_read_serving.py`, `mcp_write_serving.py`, HTTP daemon, stdio bridge | Keep/Core | AICOS product wedge: controlled context/control-plane access for heterogeneous agents | Continue hardening; keep A1 HTTP-first |
| Actor/access model | actor roles, token labels, protected write scopes | Keep/Core | AICOS-specific boundary between external A1 use and internal A2 maintenance | Normalize further; keep `codex/claude/antigravity` as agent family, not actor class |
| Project/workspace/company packs | `brain/projects/*`, project registry, context ladders | Keep/Core | AICOS is a project/workspace context layer, not generic memory only | Extend carefully after search/retrieval stabilizes |
| PostgreSQL FTS/hybrid search | `packages/aicos-kernel/aicos_kernel/pg_search/` | Keep/Projection | Works now and eval-proven; must remain projection from markdown truth | Continue P1 metadata projection and recipes |
| Embeddings/pgvector | embedding refresh, vector columns, hybrid query | Keep/Projection | Measured useful: FTS-only top5 25/54 vs hybrid top5 54/54 | Keep; add governance and FTS-vs-hybrid reports |
| GBrain/PGLite import | `tools/gbrain`, `scripts/gbrain_local.sh`, `./aicos sync brain` | Reuse/Wrap | Good substrate and source of search discipline; should not become AICOS product identity | Keep behind sync/provider boundary; avoid direct DB truth |
| GBrain page/link/job model | page schema, links, graph, skills | Reuse/Wrap | Valuable patterns, but AICOS objects have different authority levels | Adapt as AICOS-native schema projection, derived links, job view |
| Retrieval eval runner | `scripts/aicos-retrieval-eval`, corpus | Keep/Core for quality gate | Critical regression guard for search changes across AICOS + sample project | Keep expanding from real A1 misses |
| MCP schema definitions | duplicated in HTTP daemon and stdio | Keep/Core, needs dedupe | Tool contract drift is dangerous; parity checker now exists | Use parity checker now; later move schemas to shared module/generator |
| Tool schema parity checker | `scripts/aicos-mcp-tool-schema-parity` | Keep/Projection | Low-risk guardrail before full dedupe | Run before adding/modifying MCP tools |
| Status/task/handoff files | `working/status-items`, `working/task-state`, `handoff/current` | Keep/Core | Current continuity primitives; proven useful for A1 handoff | Add job view as derived read, not new truth yet |
| Derived relation graph | `./aicos audit relations`, future trace-ref graph | Migrate Candidate | Useful for adjacency, but should be derived first | Implement only after schema projection and recipes |
| Job primitive | none; implicit via status/task/handoff/checkpoint | Defer | Premature as source of truth; may become PM-tool-shaped too early | Build read-only job view first |
| Dashboard / PM integration | notes/contracts only | Defer | Needs stable job/coworker semantics first; AICOS is not PM tool | Revisit after job view and provider boundary |
| LAN auth/security | token labels, audit JSONL, allowlist | Keep/Core small-team MVP | Required for multi-agent access; not enterprise auth yet | Harden HTTPS/client profile only when real deployment needs it |
| Single-machine daemon | local Mac + Postgres.app + LaunchAgent | Accept for now | Small-team profile can tolerate with discipline; cloud/VPS later | Document SPOF; avoid HA work unless usage demands |
| Long-form MCP writes | artifact refs + direct A2 fallback | Defer | Friction exists conceptually, not enough repeated evidence | Continue artifact refs; decide after real A1/A2 cases |
| Legacy backup/import history | `backup/`, old migration docs | Retire/No New Work | Reference/provenance only; not startup truth | Do not load by default; cite only when reused |

## Provider Boundary

AICOS-owned semantics:

- actor identity and scope authorization;
- project/workspace/company context boundaries;
- startup/handoff/status/task/checkpoint semantics;
- MCP contracts and write validation;
- authority mapping across current/canonical/evidence/policy surfaces;
- retrieval recipes for A1 operating questions;
- feedback/learning loop signals.

Replaceable substrate:

- keyword/vector search engine;
- embedding provider/model;
- page/chunk storage;
- graph traversal implementation;
- long-term object store;
- PM/dashboard UI provider;
- enterprise knowledge connector.

Boundary rule:

```text
If a component decides what AICOS means, keep it in AICOS core.
If it only stores, indexes, searches, embeds, syncs, or displays AICOS truth,
wrap it behind a provider boundary.
```

## Near-Term Implementation Sequence

1. Keep P1 schema metadata projection and compact object metadata in search
   results as read-only projection.
2. Keep retrieval recipes for manager progress review, worker takeover,
   architecture review, and MCP usage/feedback in both PG and fallback query
   paths.
3. Keep `scripts/aicos-mcp-tool-schema-parity` as required check before MCP
   tool/schema changes.
4. Move MCP schema definitions into a shared generator/module only after the
   parity checker has caught the current surface as stable.
5. Add derived relation graph/job view only after eval shows adjacency misses
   or A1 usage repeatedly asks "what is connected to this?".

## What This Changes

This inventory confirms that AICOS should not replace itself with GBrain, but
also should not keep building substrate blindly.

Immediate product work stays focused on:

- A1 retrieval quality;
- schema/recipe discipline;
- clear provider boundaries;
- lightweight reliability appropriate for small-team use.

Dashboard, full graph, first-class job primitive, cloud HA, and PG-as-truth are
not next.

## Implementation Update 2026-04-28

P1/P3 first implementation pass completed:

- `aicos_context_docs.index_metadata` now stores derived AICOS object metadata.
- Query results now expose compact `object_metadata`.
- Query responses now include `retrieval_recipes` for common A1/human-manager
  intents.
- MCP schema extension constants moved into
  `packages/aicos-kernel/aicos_kernel/mcp_tool_schema.py`.
- Base MCP tool definitions are centralized in
  `packages/aicos-kernel/aicos_kernel/mcp_tool_definitions.py` and consumed by
  both the HTTP daemon and the stdio bridge.
- `scripts/aicos-mcp-tool-schema-parity` remains the guardrail for contract
  drift between daemon and stdio surfaces.
