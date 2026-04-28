# A1 Context Ladder

Status: active onboarding ladder
Actor: `A1`

## Purpose

Help an A1 work agent enter a scoped project without confusing company,
workspace, project, workstream, and task layers. This ladder gives overview
summaries so an A1 can orient before reading deeply.

## Layer 0 — Actor Identity

Read:

- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`

What you learn:

- You are an A1 work agent doing bounded deliverable work.
- You are artifact-neutral: code, docs, design, content, research, operations,
  and hybrid work are all possible.
- You do not change AICOS kernel/rules unless escalated or reassigned as A2.

## Layer 1 — Scope Binding

Before reading deeply, identify:

- company scope, if provided
- workspace scope, if provided
- project scope, usually `projects/<project-id>`
- workstream or work context, if provided
- task packet, if selected

What you learn:

- Which reality lane is authoritative for this work.
- Whether higher-scope rules exist or whether project scope is enough.

MVP default: project scope first. Future company/workspace layers are optional
and not startup-default unless the task or human points to them.

## Layer 2 — Project Minimal Orientation

Prefer the local MCP read surface for AICOS-facing context/control-plane
orientation when available:

```bash
./aicos mcp read startup-bundle --actor A1 --scope projects/<project-id>
./aicos mcp read packet-index --actor A1 --scope projects/<project-id>
```

If MCP is unavailable, read the minimal project files directly:

- `brain/projects/<project-id>/canonical/project-profile.md`
- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`
- `agent-repo/classes/a1-work-agents/task-packets/README.md`

What you learn:

- What the project is.
- What is currently true enough to work from.
- What direction is active.
- Which project task packets are available.
- Whether direct-file fallback was needed because MCP was unavailable.

If no task is selected after this layer, ask the human what to continue.

## Layer 3 — Project Context Ladder

Read if the project provides one:

- `brain/projects/<project-id>/working/context-ladder.md`

What you learn:

- Project-specific startup order.
- Which project files are hot, conditional, or deep.
- Which sources are current truth versus evidence/reference.

If no project-specific ladder exists, use this generic A1 ladder and the project
profile/current-state/current-direction.

## Layer 4 — Handoff For Continuation

Read only for continuation, interruption recovery, migration/state alignment,
or newest-vs-stale checks:

- `brain/projects/<project-id>/working/handoff/current.md`

What you learn:

- Current continuation story for this project.
- What changed most recently.
- Which older handoffs or evidence files matter on demand.

Do not read all old handoffs at startup.

## Layer 5 — Chosen Task Packet

Read exactly one packet after the task is chosen or strongly implied. Prefer:

```bash
./aicos mcp read task-packet --actor A1 --scope projects/<project-id> --packet-id <packet-id>
```

Fallback direct path:

- `agent-repo/classes/a1-work-agents/task-packets/<project-id>/<packet>.md`

What you learn:

- Task objective, work context, required context, allowed write lanes, success
  condition, continuation metadata, and next step.

## Layer 6 — Triggered Rule Cards

Read only the rule card triggered by the task:

- `agent-repo/classes/a1-work-agents/rule-cards/writeback-checkpoint.md`
- `agent-repo/classes/a1-work-agents/rule-cards/handoff-continuation.md`
- `agent-repo/classes/a1-work-agents/rule-cards/task-packet-loading.md`
- `agent-repo/classes/a1-work-agents/rule-cards/project-state-routing.md`
- `agent-repo/classes/a1-work-agents/rule-cards/layered-rules.md`
- `agent-repo/classes/a1-work-agents/rule-cards/escalation-to-a2.md`

What you learn:

- The specific rule for writing state, continuing work, routing project state,
  interpreting layered rules, or escalating to A2.

## Layer 7 — Evidence And Source Artifacts

Read only when the task packet or project ladder points to them:

- `brain/projects/<project-id>/evidence/`
- external repo or artifact source paths
- project-specific import kit or workstream notes

What you learn:

- Raw or review-heavy evidence needed for the selected task.

Evidence is not automatically canonical truth. Normalize meaningful results
back into project working/canonical lanes according to review status.

## Layer 8 — MCP-First Writeback And Escalation

For AICOS-facing continuity, write only meaningful state transitions and prefer
the Phase 2 semantic MCP write tools:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`
- `aicos_update_status_item`
- `aicos_register_artifact_ref`

What you learn:

- A1 sends small structured intent; AICOS maps it to the correct lane.
- Every semantic write must include the current `mcp_contract_ack` value from
  `mcp_contract_status`. If a write fails with `write_contract_ack_required`,
  refresh `tools/list` or restart/re-enable the AICOS MCP server, then retry
  with the current schema. Do not fall back to older write patterns.
- Checkpoint does not always mean git commit/push. It can be an artifact,
  validation, research, design, content, blocked, or continuation checkpoint.
- MCP write tools are not raw file edit tools.
- Handoff writeback is not a backlog/status lane. Do not use
  `aicos_write_handoff_update` to create, update, close, defer, or list open
  items, open questions, tech debt, or decision follow-ups. Use
  `aicos_update_status_item` for those.
- If `aicos_update_status_item` is missing from the available MCP tools, refresh
  `tools/list` or restart/re-enable the AICOS MCP server before writing. If it
  is still missing, report the blocker instead of writing status items into the
  handoff.
- Shared coordination policy:
  `brain/shared/policies/agent-coordination-policy.md`.
- Coordination summary: read `active_task_state` before code work;
  `worktree_path` is an active checkout occupancy signal, and `work_lane` is the
  cross-project coordination key for all work types. Use the shared coordination
  policy for the full reuse/separate worktree rule.

Direct file writeback is a fallback or A2 maintenance path, not the normal A1
interface for AICOS context/control-plane state. If MCP is unavailable, record
the fallback explicitly in the handoff/task update.

A1 may still use direct local access for the project artifact itself: external
repo code, design files, content drafts, research sources, runtime logs, or
other task-specific artifacts.

Escalate to A2 when:

- AICOS context delivery, rules, packets, CLI, sync, or lane structure is the
  blocker.
- The project task requires changing AICOS itself.
- Rules conflict or authority boundaries are unclear.
