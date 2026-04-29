# A2-Core Context Ladder

Status: active onboarding ladder
Actor: `A2-Core`
Scope default: `projects/aicos`

## Purpose

Help a new A2-Core agent enter AICOS without loading too much context. This
ladder gives each read a small purpose summary, but does not duplicate volatile
state. Source files remain authoritative.

## Layer 0 — Identity And Boundary

Read:

- `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`

What you learn:

- You are a service/build agent improving AICOS itself.
- You are usually in `A2-Core-C`; briefly reason as `A2-Core-R` before material
  architecture decisions.
- You are not doing A1 project delivery, UI/API work, or external tool memory
  control unless explicitly assigned.

Stop here only if you are just confirming role.

## Layer 1 — Minimal Orientation

Read:

- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `agent-repo/classes/a2-service-agents/task-packets/README.md`

What you learn:

- Current AICOS repo reality and what is active versus not active yet.
- Current implementation direction and phase boundaries.
- Which task packets exist, without loading every packet.

Default command when available:

```bash
./aicos context start A2-Core-C projects/aicos
```

If no task is selected after this layer, ask the human what to continue.

## Layer 2 — Stable Rules And Role Model

Read when you need the stable project contract:

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`

What you learn:

- How A1, A2, A2-Core, A2-Serve, humans, and future actors are separated.
- The durable lane boundaries for `brain/`, `agent-repo/`, `backend/`,
  `serving/`, canonical, working, evidence, handoff, and writeback.

Use this layer before changing project rules, actor boundaries, or lane
semantics.

## Layer 3 — Current Handoff

Read only for continuation, migration/state alignment, repo-wide architecture,
or newest-vs-stale checks:

- `brain/projects/aicos/working/handoff/current.md`

What you learn:

- The current H1 handoff index for `projects/aicos`.
- What changed most recently and which older paths are stale.
- Which provenance notes are worth opening on demand.

Do not read all old handoffs, backups, or Git-history provenance at startup.

## Layer 4 — Chosen Task Packet

Read only one packet after the task is chosen or strongly implied:

- `agent-repo/classes/a2-service-agents/task-packets/<packet>.md`

What you learn:

- Task-specific objective, required context, allowed write lanes, success
  condition, handoff refs, and next step.

Do not bulk-load all task packets. The packet index is enough before task
selection.

## Layer 5 — Triggered Rule Cards

Read only the rule card triggered by the chosen task:

- `agent-repo/classes/a2-service-agents/rule-cards/writeback.md`
- `agent-repo/classes/a2-service-agents/rule-cards/handoff.md`
- `agent-repo/classes/a2-service-agents/rule-cards/sync-brain.md`
- `agent-repo/classes/a2-service-agents/rule-cards/idea-capture.md`
- `agent-repo/classes/a2-service-agents/rule-cards/option-choose.md`

What you learn:

- The small operating rule for the action you are about to perform.

Open longer files in `agent-repo/classes/a2-service-agents/rules/` only when the
rule card is not enough.

## Layer 6 — Current Architecture Overview

Read when you need a broader map before editing architecture:

- `docs/architecture/README.md`
- `brain/projects/aicos/working/architecture-working-summary.md`

What you learn:

- The current architecture digest and active design anchors.
- Which research/design docs are current implementation direction.

Do not use removed long-form design/migration files as current architecture. If
needed, inspect them only through Git history as provenance.

## Layer 7 — Source Code Or Specific Subsystem

Read only after the task points to a subsystem:

- `packages/aicos-kernel/` for kernel contracts, CLI, schemas, validators.
- `serving/` for generated capsules, option packets, branch/promotion helpers.
- `backend/` for local substrate/PGLite support.
- `integrations/` for local integration scaffolds.
- `tools/gbrain/` for GBrain/PGLite sync and retrieval support.

What you learn:

- Implementation details for the bounded subsystem you are changing.

Use `rg --files` and targeted reads. Do not load the whole repo as startup
context.

## Layer 8 — MCP Context/Control Plane

Read when the task touches A1 context delivery, cross-repo work, or local MCP
integration:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- `integrations/local-mcp-bridge/README.md`
- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

What you learn:

- Phase 1 read-serving returns bounded startup, handoff, packet index, and
  selected task-packet bundles.
- Phase 2/3 tools record semantic continuity updates: checkpoint, task update,
  compact handoff update, status-item update, artifact-ref registration, and
  bounded query/status/workstream reads.
- MCP is AICOS context/control-plane access, not a raw file RPC layer.
- A1 is MCP-first for AICOS-facing context/control-plane operations. A2-Core can
  still use direct repo access while maintaining AICOS.
- Shared coordination policy:
  `brain/shared/policies/agent-coordination-policy.md`.
- Coordination summary: `worktree_path` is an active checkout occupancy signal
  for code work, and `work_lane` is the cross-project coordination key for all
  work types. Use the shared coordination policy for the full reuse/separate
  worktree rule.

Useful debug read:

```bash
./aicos mcp read startup-bundle --actor A2-Core-C --scope projects/aicos
```

## Layer 9 — Provenance And Deep History

Read only when the current handoff, task packet, or human asks for provenance:

- specific historical files from Git history
- specific backup paths when available locally

What you learn:

- Why a decision or migration happened.

Historical files do not override current project truth in
`brain/projects/aicos/` or the current architecture index.
