# Tóm Tắt Kiến Trúc Đang Làm Việc

Trạng thái: working architecture summary, không thay thế source docs.
Ngày cập nhật: 2026-04-21.

## Identity

AICOS là context/control-plane và shared-reality layer cho humans, A1 work
agents, A2 service/build agents, nhiều projects, và nhiều
branches/experiments.

AICOS không phải code/runtime authority của mọi project. Với project bên ngoài
như `sample-project`, AICOS giữ project context, continuity, task
packets, status, handoff, và policy; external repo giữ code/runtime authority.

## Authority Model

- `brain/`: durable knowledge, canonical truth, working reality, evidence,
  project handoff, status-items, project registry material, and service
  knowledge.
- `agent-repo/`: actor operations, startup cards, rule cards, task packets, and
  task/backlog lanes. It is not project truth.
- `packages/aicos-kernel/`: deterministic contracts, validators, packet
  rendering, write/read serving operations, adapters, and thin CLI behavior.
- `integrations/`: runtime bindings such as local MCP stdio bridge.
- `serving/`: generated capsules/review/query/promotion/branching surfaces.
- `backend/` and GBrain/PGLite: serving/index/runtime substrate, not authority
  for current project truth.

## Layer Model

- Canonical truth: stable identity, role boundaries, working rules, accepted
  decisions, and future ADRs.
- Working reality: current state, direction, implementation status, risks,
  status-items, open questions, and current handoff.
- Evidence/intake: design docs, migration notes, research, candidate rules,
  review findings, and source inventories.
- Continuity layer: current handoff, task-state, checkpoints, and
  status-items. Handoff is compact current continuity, not a permanent event
  log.
- MCP context/control plane: local stdio read/write surface for bounded context
  serving and semantic writeback.
- Branch/option layer: option packets and branch reality for reversible
  decisions.
- Serving/retrieval layer: capsules, query, promotion review, and GBrain/PGLite
  indexes.

## MCP Context/Control Plane

Local MCP is now part of the active MVP architecture.

- Read surfaces provide startup bundles, current handoff, packet index, one
  selected task packet, status items, workstream index, and bounded project
  context query.
- Write surfaces accept semantic continuity events: checkpoint, task update,
  compact handoff update, status-item update, and artifact-ref registration.
- MCP is not raw file RPC. The server validates intent, maps it to lanes, and
  formats durable records.
- A1 should use MCP-first for AICOS-facing context/control-plane. A2-Core may
  still use direct repo access while maintaining AICOS itself.

Current write contract is `mcp-v0.6-write-contract-ack`. All semantic writes
must include actor identity (`actor_role`, `agent_family`,
`agent_instance_id`) and work identity (`work_type`, `work_lane`). Code work
must include `worktree_path`.

## Status And Handoff Architecture

Status-items are now the working-status lane for open items, open questions,
tech debt, and decision follow-ups. They should not be hidden in handoff
append blocks.

Handoff remains the H1 current continuity index for a project. It should stay
short enough for an agent to read when continuation is needed. `./aicos compact
handoff projects/<project-id>` exists as a manual compaction surface when MCP
handoff update blocks accumulate.

Startup bundle includes `continuity_signal` so an empty `active_task_state`
does not incorrectly imply a project is idle.

## Kernel vs Service Intelligence

`packages/aicos-kernel/` should stay deterministic:

- schemas/contracts
- validators and CLI adapters
- read/write serving operations
- packet rendering and safe lane mapping
- compaction primitives where behavior is mechanical and bounded

Service intelligence should not be hardcoded too early. Option quality,
promotion recommendation, retrieval strategy, A2-Serve heuristics, and
project-health interpretation should mature first as service knowledge,
skills, policy docs, or reviewed status-items.

## Storage / Retrieval Strategy

AICOS currently uses Markdown-first authority and DB-assisted serving.

- Markdown is appropriate for current restructuring truth: readable state,
  canonical rules, handoffs, status-items, task packets, decisions, and
  evidence references.
- GBrain/PGLite is appropriate for sync, retrieval substrate, cache/index
  state, and future registries.
- DB/vector systems should not silently become authority until an explicit
  truth-store ADR exists.

CTO concern: Markdown authority is good for this phase, but multi-agent scale
will stress conflict resolution, append-heavy handoffs, and stale retrieval.
ARCH-R-03 should be resolved before AICOS grows beyond a small number of active
projects/agents.

## A2 Taxonomy

- A2-Core: maintains AICOS itself; active now.
- A2-Core-R: architecture/policy/boundary reasoning before material changes.
- A2-Core-C: coding/build/config/refactor/documentation changes.
- A2-Serve: future service lane to improve how AICOS serves A1 and project
  work. It is not active as a full runtime lane yet.

CTO concern: A2-Serve should not remain a vague aspiration. Define graduation
criteria before onboarding a third active project or before multiple agent
instances depend on MCP context quality at the same time.

## Project Scaling Direction

The `sample-project` promotion proved the external-project authority
split. The next scaling step should not be “more ad hoc import kits.” It should
be:

1. project registry and dependency/isolation policy,
2. standardized project intake/import flows,
3. accepted workstream index per active project,
4. explicit cross-project context propagation rules.

Until that exists, agents should not infer shared context across projects
implicitly.

## Current Open Architectural Risks

- Retrieval freshness: `sync brain` does not guarantee embedding freshness.
- Truth store: no ADR yet for Markdown-vs-structured-store scale limits.
- A2-Serve: no activation criteria yet.
- Cross-project context: no registry/dependency propagation policy yet.
- Query coverage: canonical/policy/contract docs are still not first-class
  query contexts unless specifically wired.
- Status item taxonomy: type validation and guidance are still weak.
