# AICOS Project Context Ladder

Status: active project context ladder
Scope: `projects/aicos`

## Purpose

This ladder helps A2-Core, A2-Serve candidates, A1 support agents, humans, and
reviewers understand where to start in the AICOS project without loading the
whole repo. Summaries describe file purpose, not full contents.

## Layer 0 — Actor Entry

Read based on actor:

- A2-Core: `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
- A2-Serve: `agent-repo/classes/a2-service-agents/onboarding/a2-serve-context-ladder.md`
- A1: `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`

What you learn:

- which actor class you are
- which startup path applies
- what not to load by default

## Layer 1 — Current AICOS Reality

Read:

- `brain/projects/aicos/working/aicos-architecture-overview.md`
- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`

What you learn:

- current high-level product/architecture definition: AICOS as a
  workspace/project context intelligence layer
- active repo state, implemented scaffolds, current focus, and not-yet-active
  areas
- current working direction and writeback discipline

## Layer 2 — Stable Project Rules

Read when changing structure, rules, or architecture:

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`

What you learn:

- stable actor roles and boundaries
- lane rules, handoff rules, state/writeback rules, and implementation limits

## Layer 3 — Continuation Handoff

Read only for continuation, migration/state alignment, repo-wide architecture,
or newest-vs-stale checks:

- `brain/projects/aicos/working/handoff/current.md`

What you learn:

- current H1 handoff index
- recent meaningful changes
- stale paths and provenance notes to open only on demand

## Layer 4 — Task And Rules

Read after task selection:

- `agent-repo/classes/a2-service-agents/task-packets/README.md`
- one selected task packet
- triggered rule cards in `agent-repo/classes/a2-service-agents/rule-cards/`

What you learn:

- task objective, context, allowed lanes, success condition, and exact operating
  rules for the work

## Layer 5 — Architecture And Policy Provenance

Read only when overview or provenance is needed:

- `brain/projects/aicos/working/architecture-working-summary.md`
- `brain/projects/aicos/evidence/policy-sources/policy-source-index.md`

What you learn:

- architecture digest and source-doc index
- where long design/policy docs live without bulk-loading them

## Layer 6 — Implementation Source

Read only for bounded implementation tasks:

- `packages/aicos-kernel/`
- `serving/`
- `backend/`
- `integrations/`
- `tools/gbrain/`

What you learn:

- concrete implementation details for the subsystem being changed

Use targeted search first. Do not use source-tree reading as startup context.

## Layer 7 — MCP Context/Control Plane

Read when the task involves A1 onboarding, cross-repo work, context serving, or
writeback through local MCP:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- `integrations/local-mcp-bridge/README.md`
- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

What you learn:

- Phase 1 đã có read-serving bundle cho startup, handoff, packet index, và một
  task packet đã chọn.
- Phase 2 đã có semantic write tools cho checkpoint, task update, handoff
  update, status-item update, và artifact-ref registration.
- Phase 3 đã có bounded markdown-direct query/status/workstream reads:
  `aicos_query_project_context`, `aicos_get_status_items`, và
  `aicos_get_workstream_index`.
- A1 nên dùng MCP-first cho AICOS-facing context/control-plane; A2-Core vẫn có
  thể đọc/sửa repo trực tiếp khi bảo trì AICOS.
- Handoff writeback không phải backlog/status lane. Dùng
  `aicos_update_status_item` cho open items, open questions, tech debt, và
  decision follow-ups.
- MCP hiện là local-first/stdio scaffold, chưa có online transport, auth,
  daemon, cache lớn, vector/GBrain-backed MCP query, hoặc raw file write API.
