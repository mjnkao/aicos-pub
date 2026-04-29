# AICOS Current Module Decision Inventory

Status: execution decision inventory
Date: 2026-04-28
Scope: `projects/aicos`
Actor: `A2-Core-C`

## Purpose

Translate the product-level execution decision table into a concrete
module/surface-level inventory.

This is the practical CTO table for deciding what AICOS should keep owning,
what should be wrapped as substrate, what should be migrated later, and what
should stop growing.

This file does not approve a large refactor. It is a sequencing and guardrail
artifact for future implementation passes.

## Decision Key

| Decision | Meaning |
| --- | --- |
| Keep/Core | AICOS must own this semantic/control-plane responsibility. |
| Keep/Projection | Useful derived implementation; must stay downstream of AICOS truth. |
| Reuse/Wrap | Prefer external or substrate implementation behind an AICOS boundary. |
| Migrate Candidate | Keep current path now, evaluate replacement after usage/eval evidence. |
| Defer | Directionally valid, but not next. |
| Retire/No New Work | Keep only for compatibility/provenance; do not grow. |

## Current Provider Bundle

The current running bundle is:

```text
markdown brain truth
+ HTTP MCP daemon
+ local stdio/proxy adapters
+ token auth/audit
+ PostgreSQL FTS/vector hybrid search
+ GBrain/PGLite sync/import substrate
+ lightweight eval/doctor scripts
```

This is the first real `small-team` implementation bundle. It is not the whole
AICOS architecture.

## Decision Matrix

| Surface | Current implementation | Option C layer | Decision | Pass | Next action | Risk if wrong |
| --- | --- | --- | --- | --- | --- | --- |
| Authority model | `brain/`, `agent-repo/`, contracts, working/evidence/canonical lanes | Semantic core | Keep/Core | Phase 2 | Preserve markdown truth and lane precedence; document invariants before moving storage. | AICOS becomes a generic search DB or PM tool with unclear truth. |
| Semantic object model | status items, handoffs, checkpoints, feedback, project registry, artifact refs | Semantic core | Keep/Core | Phase 2 | Normalize object names and required metadata in contracts/schemas. | Providers redefine AICOS objects differently. |
| MCP semantic read/write contracts | `mcp_read_serving.py`, `mcp_write_serving.py`, MCP contract docs | Semantic core + runtime service | Keep/Core, then split | Phase 2 | Extract validation/normalization constants before adding broad tools. | A1 agents get inconsistent behavior across clients. |
| Actor/access model | actor role, agent family, token label, protected scopes, runtime identity metadata | Semantic core + auth/audit | Keep/Core | Phase 2 | Keep A1/A2 as AICOS actor class; keep Codex/Claude/Antigravity as `agent_family`; maintain token scope rules. | External agents confuse family with authority and write into wrong scope. |
| Project/workspace/company packs | `brain/projects/*`, workspace/company folders, templates | Semantic core + profile pack | Keep/Core | Phase 4/8 | Keep packs lightweight; define pack schema only after current project import path is stable. | AICOS becomes hardcoded to this one repo/company shape. |
| Startup/orientation ladders | A1/A2 ladders, project context ladders, startup bundle | Semantic core + serving | Keep/Core | Phase 2 | Keep small and actor-appropriate; do not bulk-load historical context. | Agent startup becomes slow or context-poisoned. |
| Handoff/status/checkpoint continuity | `working/handoff`, `working/status-items`, task-state/checkpoints | Semantic core | Keep/Core | Phase 2/6 | Keep as current continuity primitives; add dashboard read views later as derived surfaces. | Humans and agents cannot safely continue each other's work. |
| Feedback/learning loop | feedback write tool, feedback digest, eval candidate digestion | Semantic core + quality loop | Keep/Core | Phase 5 | Keep lightweight; convert repeated retrieval misses into eval cases before building new tools. | Search quality depends on manual one-off fixes forever. |
| Retrieval eval gate | `scripts/aicos-retrieval-eval`, AICOS/sample project eval corpus | Quality gate | Keep/Core | Phase 5 | Expand from real A1 misses; run before search/ranking/provider changes. | Search regressions remain invisible. |
| PostgreSQL FTS/vector hybrid | `packages/aicos-kernel/aicos_kernel/pg_search/` | Retrieval provider | Keep/Projection | Phase 5 | Keep as first retrieval provider; benchmark before replacing or abstracting further. | Semantic logic leaks into PG schema or vector behavior. |
| Embedding refresh | `pg_search/embedding.py`, freshness checks | Retrieval provider | Keep/Projection | Phase 5 | Keep optional and observable; AICOS must degrade without embeddings. | AICOS becomes unusable without one external embedding path. |
| GBrain/PGLite sync/import | `tools/gbrain`, `scripts/gbrain_local.sh`, `./aicos sync brain` | Substrate provider | Reuse/Wrap | Phase 3/5 | Keep behind sync/provider boundary; borrow search/link/job ideas, not authority model wholesale. | AICOS either underuses good substrate or gets swallowed by GBrain shape. |
| Search intent and recipes | `pg_search/intent.py`, retrieval recipes in query results | Retrieval assist | Keep/Projection | Phase 5 | Keep heuristic and eval-driven; align with common A1/human-manager questions. | Query UX becomes brittle or over-classified too early. |
| Trace refs / relation audit | `relations/trace_refs.py`, `./aicos audit relations` | Optional relation provider seed | Keep/Projection | Phase 5 | Maintain source/artifact/scope/session ref hygiene; keep relation graph derived. | AICOS invents a graph engine before relations are clean. |
| Related context read surface | proposed `aicos_get_related_context` | Optional relation provider | Defer | Phase 5+ | Build only after eval or A1 feedback shows repeated adjacency misses. | Extra tool increases cognitive/tooling load without real retrieval gain. |
| HTTP MCP daemon | `integrations/mcp-daemon/aicos_mcp_daemon.py` | Runtime service + profile | Keep, split later | Phase 3/4 | Keep small-team runtime; split transport/auth/audit/provider wiring when changes touch those seams. | Daemon becomes a monolith for dashboard, jobs, auth, search, and PM sync. |
| HTTPS proxy / LAN scripts | `aicos_https_proxy.py`, `start-lan.sh`, env examples | Deployment profile concern | Keep narrow | Phase 4 | Harden only when real client/profile need appears; document risk. | Premature gateway work distracts from core semantics. |
| Local stdio bridge/proxy | `aicos_mcp_stdio.py`, `aicos_mcp_http_first.py`, wrapper | Client adapter | Keep | Phase 3/4 | Keep thin; derive schemas from shared definitions where possible. | Stdio and HTTP tools drift and agents see different contracts. |
| MCP tool schema definitions | `mcp_tool_schema.py`, `mcp_tool_definitions.py`, parity script | Contract guardrail | Keep/Core | Phase 3 | Keep parity check required before tool changes; avoid independent schemas. | Client integrations silently break. |
| CLI/operator shell | `kernel.py`, `cli.py`, `scripts/aicos` | Runtime operations shell | Keep, refactor behind service funcs | Phase 2/3 | Add only thin commands backed by stable functions; avoid more mixed concerns. | `kernel.py` becomes an untestable kitchen sink. |
| Generated serving surfaces | `serving/capsules`, `serving/query`, `serving/branching`, `serving/promotion` | Derived serving/projection | Keep/Projection | Phase 2/6 | Keep generated/review-facing; never treat as truth. | AICOS grows a second conflicting truth store. |
| Context registry | `context_registry.py`, `serving/context-registry` | Runtime registry/projection | Keep/Projection | Phase 3/8 | Use as source map and provider input; avoid page-schema/graph expansion here. | Registry becomes an accidental graph/page system. |
| Backend substrate notes | `backend/`, PGLite docs | Provider/deployment substrate | Retire/No New Work for now | Phase 3 | Keep as notes until a real provider/service extraction needs it. | Parallel backend grows beside markdown truth. |
| Nightly maintenance | `integrations/nightly-maintenance` | Jobs provider seed | Defer | Phase 3/5 | Keep non-critical; no correctness dependency on automation. | Flaky jobs become hidden authority. |
| Health monitor | `aicos_health_monitor.py`, doctor/status checks | Ops/profile concern | Keep narrow | Phase 0.5/4 | Observe and reduce false noise; monitors should not define product behavior. | Agents ignore alerts or chase false failures. |
| Chat sync connectors | `integrations/chatgpt-sync`, `claude-chat-sync` | Connector/ingestion seed | Defer | Phase 7/8 | Keep manual until ingestion authority/privacy rules exist. | Imported chat logs pollute truth or leak private context. |
| Project proposal/intake | `project-proposal` MCP write, project templates/import kit | Product lifecycle | Keep/Core | Phase 8 | Productize approval -> pack creation -> registry/token policy minimally. | Agents route missing projects through feedback/handoff again. |
| Dashboard/coworker view | notes/contracts only | Product surface above core | Defer | Phase 6/7 | Define read-only active-workers/tasks/attention views before PM sync. | AICOS turns into a PM clone or dashboard backend too early. |
| Plane/ClickUp integration | notes/contracts only | External collaboration provider | Defer | Phase 7 | Decide authority model before syncing fields. | Task tools overwrite AICOS semantics or create conflict loops. |
| Enterprise org knowledge connectors | no active implementation | Future provider/partner | Defer | Company-100+ | Partner/wrap Onyx/Atlan-like systems before self-building. | Scope explodes into generic enterprise search. |
| Legacy backup/pre-restructure | `backup/pre-restructure-*` | Provenance only | Retire/No New Work | Ongoing | Do not load by default; cite only when reused. | Old protocol silently overrides current restructuring direction. |

## Code Hotspots That Should Not Grow

These files are allowed to receive bug fixes, schema alignment, and small
compatibility patches, but should not receive new broad product responsibilities
without a boundary refactor:

- `packages/aicos-kernel/aicos_kernel/kernel.py`
- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
- `integrations/mcp-daemon/aicos_mcp_daemon.py`
- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

Do not add these directly into the hotspots:

- dashboard/task-board logic;
- PM tool sync;
- graph/page schema engine;
- critical background job system;
- broad external connector ingestion;
- provider-specific semantic rules.

## Execution Order

1. **Boundary cleanup before expansion**
   - Extract shared semantic constants and MCP schema definitions where drift
     already exists.
   - Split only when changing a boundary anyway; avoid abstracting everything
     upfront.

2. **Retrieval quality before graph/tool expansion**
   - Keep the eval runner as the regression gate.
   - Promote repeated A1 misses into eval cases.
   - Add related-context tooling only when eval or feedback proves adjacency
     misses are real.

3. **Runtime/security before wider team rollout**
   - Harden token/auth/HTTPS/SSE/LAN behavior for `small-team` and
     `company-100` profiles before relying on dashboard/shared operation.
   - Keep single-machine daemon acceptable for small team, documented as SPOF.

4. **Project intake before broad company packs**
   - Complete lightweight project proposal -> approval -> project pack ->
     registry/token policy path.
   - Then generalize into company/workspace/project packs.

5. **Dashboard after coworker semantics**
   - First define active workers, active lanes, takeover-ready items,
     blocked-by-human/agent states, and human attention queue.
   - Then integrate Plane/ClickUp or similar tools through a sync contract.

## CTO Judgment

AICOS should keep building, but only where it owns semantics:

- multi-agent context/control-plane;
- project/workspace/company scope and authority;
- continuity and handoff;
- actor/access/coordination identity;
- A1-friendly context retrieval recipes;
- feedback-to-eval learning loop.

AICOS should aggressively reuse or wrap substrate:

- search engines;
- embeddings/vector stores;
- page/chunk stores;
- graph traversal;
- PM/task UI;
- enterprise knowledge connectors;
- scheduled job infrastructure.

The current repo is close enough to Option C that a rewrite or GBrain fork is
not justified. The highest leverage path is incremental boundary cleanup,
retrieval evaluation, and provider wrapping where current code already shows
real pressure.

## References

- `brain/projects/aicos/evidence/research/aicos-execution-decision-table-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-phase-1-module-inventory-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-module-inventory-provider-boundary-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-phase-2-semantic-core-boundary-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-phase-3-provider-interface-sketch-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
