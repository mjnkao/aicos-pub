# AICOS Phase 1 Module Inventory

Status: phase-1 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-C

## Purpose

Classify the current AICOS repo against the Option C north-star before deeper
modularization. This pass is intentionally an inventory and decision map, not a
runtime refactor.

Guardrail for this pass:

- do not add new runtime layers;
- do not add new providers;
- do not introduce new daemons, queues, databases, or background jobs;
- do not grow large modules while their boundaries are still unclear;
- report before doing work that would slow the system, expand maintenance
  scope, hurt scalability, or force AICOS to self-build substrate that should
  be provider-owned.

## Phase 1 Summary

AICOS is not far from the Option C direction, but current implementation still
has several responsibilities collapsed into a few large files:

- `packages/aicos-kernel/aicos_kernel/kernel.py`
  combines CLI, generated serving helpers, sync orchestration, daemon status,
  MCP debug calls, audit summary, and feedback summary.
- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
  combines semantic read assembly, markdown parsing, context routing, feedback
  loop logic, fallback search, and project-health serving.
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  combines write contract validation, semantic write formatting, markdown file
  writes, feedback-closure policy, status-item warnings, and trace metadata.
- `integrations/mcp-daemon/aicos_mcp_daemon.py`
  combines HTTP transport, auth, audit logging, read identity validation,
  pg_search provider wiring, cache, reindex scheduling, health endpoint, and
  MCP tool schema publication.

This shape is acceptable for the current small-team MVP, but these modules
should not absorb new product responsibilities until Phase 2/3 boundaries are
defined.

## Layer Classification Matrix

| Area | Current modules | Option C layer | Decision | Why | Growth guardrail |
| --- | --- | --- | --- | --- | --- |
| Semantic contracts | `packages/aicos-kernel/contracts/`, `schemas/` | semantic core | keep | These describe AICOS-owned object and coordination semantics. | Add invariants here before implementing new runtime behavior. |
| MCP read semantics | `mcp_read_serving.py` | semantic core + runtime service | refactor behind boundary | It is the real read contract implementation, but also contains file parsing, fallback query, feedback loop, and health assembly. | Do not add new read surfaces here unless they are contract-stable and small. |
| MCP write semantics | `mcp_write_serving.py` | semantic core + runtime service | refactor behind boundary | It owns validation and semantic write normalization, but writes directly to markdown and embeds policy checks. | Do not add broad write tools; keep writes semantic and bounded. |
| Contract status | `mcp_contract_status.py` | semantic core | keep | Small, stable compatibility surface for client schema refresh. | Keep simple; avoid making it a version-negotiation framework too early. |
| Context registry | `context_registry.py`, `serving/context-registry/` | runtime service + derived serving | refactor behind boundary | Useful derived source map; should become a provider-facing source registry later. | Avoid adding graph/page schema responsibilities here yet. |
| Relation extraction | `relations/trace_refs.py` | optional relation provider seed | keep, do not grow heavily | Lightweight trace-ref parser is useful and low cost. | Do not turn this into a full graph engine in Phase 1/2. |
| CLI orchestration | `kernel.py`, `cli.py`, `scripts/aicos` | runtime operations shell | refactor behind boundary | Useful operator surface, but currently too many responsibilities. | Add new CLI commands only when backed by stable service functions. |
| GBrain adapter | `gbrain-adapter/README.md`, `scripts/gbrain_local.sh`, `tools/gbrain/` | provider implementation | migrate toward provider layer | Current small-team substrate; useful but not AICOS identity. | Do not fork/deepen GBrain coupling unless it is wrapped as a provider capability. |
| PostgreSQL hybrid search | `pg_search/` | retrieval provider implementation | migrate toward provider layer | Valuable current retrieval substrate; should become the first Retrieval Provider bundle. | Do not let semantic decisions depend on PG table shape or pgvector details. |
| Embeddings | `pg_search/embedding.py` | retrieval provider implementation | keep behind provider | Supports hybrid retrieval; not core semantics. | Keep optional and observable; do not make AICOS unusable without embeddings. |
| Search intent | `pg_search/intent.py` | retrieval provider assist + semantic hint | refactor later | Useful low-latency routing, but intent taxonomy should align with semantic context kinds. | Keep heuristic; do not build a large classifier before eval corpus exists. |
| HTTP MCP daemon | `integrations/mcp-daemon/aicos_mcp_daemon.py` | runtime service + deployment/profile concern | refactor behind boundary | Needed for small-team profile, but mixes transport, auth, audit, cache, provider wiring, and schema publication. | Do not add dashboard, jobs, or PM sync logic into this daemon directly. |
| HTTPS proxy | `aicos_https_proxy.py` | deployment/profile concern | keep | Practical compatibility layer for Claude Desktop. | Keep narrow; do not turn into generic gateway/auth layer. |
| Health monitor | `aicos_health_monitor.py` | ops/profile concern | keep, simplify if noisy | Useful local ops signal, but can create false-alert noise. | Monitor should observe, not define product behavior. |
| Local stdio bridge | `integrations/local-mcp-bridge/aicos_mcp_stdio.py` | runtime transport adapter | keep, reduce duplication later | Important for stdio-only clients and fallback. | Keep schema generated or synced with daemon eventually; avoid independent logic drift. |
| HTTP-first stdio proxy | `aicos_mcp_http_first.py`, `aicos_mcp_http_stdio_wrapper.py` | transport adapter | keep | Good compatibility path that preserves HTTP-first A1 behavior. | Keep as thin proxy; no separate semantics. |
| Install docs | `docs/install/`, `integrations/local-mcp-bridge/install/` | deployment/profile concern | keep | Needed for multi-client adoption. | Split by profile/client; avoid burying architecture rules in install docs. |
| Agent repo rules | `agent-repo/classes/` | semantic operating policy + actor onboarding | keep, refactor later | Useful actor ladders and policies; currently AICOS-specific. | Phase 2 must normalize actor model so A1/A2 does not leak into all projects. |
| Serving generated outputs | `serving/capsules/`, `serving/branching/`, `serving/feedback/`, `serving/query/`, `serving/truth/` | derived serving/review surfaces | keep as generated, stop growing ad hoc | Helpful review artifacts, not authority. | Do not make generated serving files a second truth store. |
| Backend substrate notes | `backend/` | provider/deployment substrate | keep as notes only | Documents PGLite/GBrain sync direction; not active authority. | Do not build a parallel backend truth layer here. |
| Nightly maintenance | `integrations/nightly-maintenance/` | jobs/maintenance provider seed | refactor behind provider later | Useful concept, but automation reliability is still immature. | Do not add critical behavior until jobs provider semantics are defined. |
| Chat sync folders | `integrations/chatgpt-sync/`, `claude-chat-sync/` | connector/ingestion provider seed | keep as manual/deferred | Potential connector class, not current core. | Keep manual until ingestion authority and privacy rules are explicit. |
| Client-specific docs | `integrations/codex/`, `claude-code/`, `openclaw/` | deployment/client adapters | keep | Needed to support heterogeneous A1 clients. | Avoid custom behavior per agent family unless there is a real client limitation. |

## Keep / Reuse / Migrate / Retire Matrix

| Module group | Near-term decision | Pass | Notes |
| --- | --- | --- | --- |
| Contracts and schemas | keep | Phase 2 | Promote stable invariants into a core boundary note. |
| MCP read/write serving | keep, then split boundaries | Phase 2 | Split semantic validation/assembly from markdown store details later. |
| PG hybrid search | keep as current retrieval provider | Phase 3/5 | First concrete Retrieval Provider; benchmark before replacing. |
| GBrain sync/import | reuse as provider substrate | Phase 3/5 | Do not make GBrain the product identity. |
| HTTP daemon | keep as small-team runtime | Phase 3/4 | Split transport/auth/audit/provider wiring later. |
| Stdio bridge/proxy | keep as client compatibility | Phase 3/4 | Eventually generate schemas from one source. |
| Health monitor | keep but do not expand | Phase 0.5/4 | Fix noisy behavior only when observed. |
| Serving generated surfaces | keep as derived artifacts | Phase 2/6 | Useful for review/dashboard thinking, not authority. |
| Backend folder | keep as substrate notes | Phase 3 | Avoid parallel backend until provider boundaries exist. |
| Nightly maintenance | defer as Jobs Provider seed | Phase 3 | Do not rely on it for critical state yet. |
| Chat sync connectors | defer | Phase 3/7 | Need connector/ingestion authority model first. |
| Large monolithic CLI | refactor behind service modules | Phase 2+ | Do not add heavy behavior to `kernel.py`. |

## Modules That Should Not Gain New Responsibilities Yet

These files are already carrying too many mixed concerns:

- `packages/aicos-kernel/aicos_kernel/kernel.py`
- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
- `integrations/mcp-daemon/aicos_mcp_daemon.py`
- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

Allowed changes before boundary cleanup:

- small bug fixes;
- schema alignment;
- compatibility fixes for real A1 clients;
- narrowly-scoped observability improvements;
- corrections that prevent feedback or write loss.

Not allowed without explicit architecture review:

- dashboard/task orchestration logic;
- PM tool sync logic;
- new graph/page schema engine;
- new long-running jobs subsystem;
- provider-specific semantic assumptions;
- broad custom memory or retrieval framework growth.

## Scalability / Bloat / Speed Review

### Current good news

- Markdown truth keeps the system inspectable and portable.
- PG hybrid search is optional and has markdown-direct fallback.
- Feedback loop is lightweight and event-driven, not a polling/survey system.
- HTTP MCP centralizes multi-agent access without forcing a hosted platform yet.

### Current risks

- Runtime code duplication between HTTP daemon and stdio bridge can drift.
- `kernel.py` is becoming an operator kitchen sink.
- `mcp_read_serving.py` mixes semantic object serving with fallback search.
- `mcp_write_serving.py` mixes semantic validation with markdown storage.
- The daemon mixes transport, auth, audit, search provider, cache, and lifecycle.
- Generated `serving/` artifacts could become confusing if treated as truth.

### Do not do yet

- Do not create a generic plugin/provider framework before defining the first
  small provider interfaces.
- Do not build a dashboard backend inside the current MCP daemon.
- Do not add a graph database or page-schema engine until retrieval evals prove
  the relation layer is the bottleneck.
- Do not replace markdown truth with PostgreSQL truth during Phase 1.
- Do not make background automations required for correctness.

## CTO Judgment

The current stack is compatible with Option C as an MVP implementation bundle
for the `small-team` profile, but not yet modular enough for `company-100`.

The gap is manageable if the next passes preserve this order:

1. define semantic core boundaries;
2. define provider slots only where real variation exists;
3. treat PG/GBrain/HTTP/token auth as the current provider bundle;
4. keep dashboard/Plane/ClickUp integration above the control-plane semantics,
   not inside transport or retrieval code.

The highest-risk mistake would be continuing to add new product behavior into
the daemon and kernel files because they are convenient. That would make AICOS
look productive short-term but more expensive to scale, test, replace, or adapt
for a 100-person company later.

## Immediate Next Step

Move to Phase 2 only after this inventory is accepted as the baseline:

- draft the Semantic Core Boundary note;
- normalize actor-role dimensions;
- identify invariants that provider implementations must obey;
- list the concrete extraction points from the current large modules.
