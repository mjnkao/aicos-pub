# Task Packet Template

Status: minimal MVP contract

Use this template to hand a co-worker the smallest useful task context.

```yaml
schema_version: "0.1"
kind: "aicos.task_packet"
task_id: ""
actor_role: ""           # example: A1 / A2-Core-C / A2-Core-R
agent_family: ""         # optional hint, example: codex / claude-code / gemini-antigravity
agent_instance_id: ""    # optional when packet is pre-assigned to an instance
scope: ""                # example: projects/aicos
work_type: ""            # example: code / content / design / research / ops / review / planning / data / mixed
work_lane: ""            # generic coordination lane, not necessarily a git branch
coordination_status: ""  # optional, example: planned / active / blocked / handoff_ready
artifact_scope: ""       # document/design/research/code/output scope
artifact_refs:
  - ""
work_branch: ""          # optional, code-specific
worktree_path: ""        # required when work_type is code and packet assigns a concrete checkout
task_type: ""            # example: writeback | option_choose | sync | kernel | migration | self_brain
objective: ""
summary: ""              # one-line packet index summary
continuation_mode: ""    # example: new_task | continue_previous | migration_followup | review_followup
current_owner: ""        # lightweight current owner label, not a permanent identity system
task_status: ""          # example: owned_current | checkpointed_current | blocked_waiting_human | blocked_waiting_system | handoff_ready | taken_over
last_checkpoint_at: ""   # ISO timestamp or date when a safe checkpoint was last recorded
handoff_ready: false     # true only when another actor can continue without reconstructing the whole session
next_actor_hint: ""      # optional, example: A2-Core-C / A2-Core-R / A2-Serve later
required_context:
  - ""
rules_to_load:
  - ""
allowed_write_lanes:
  - ""
success_condition: ""
handoff_refs:
  - ""
what_is_done: ""
what_is_blocked: ""
next_step: ""
touched_artifacts:
  - ""
access_paths:
  - ""
notes: ""
```

## Rule

Prefer packet-first loading. Do not require a co-worker to read all source docs
at startup.

`rules_to_load` should name only the cards needed for this task.

If no concrete task has been selected, show the packet index or summaries and
ask which task to continue. Do not load all full packets by default.

## Handoff-Ready Metadata Rule

These fields do not create a transfer/takeover subsystem. They are a thin
continuation contract so another actor can cheaply answer:

- who owns this task now
- which actor role / agent family / agent instance / scope / work lane is active
- which primary artifact(s) are being changed or reviewed
- what status/checkpoint exists
- what is done or blocked
- what to load next
- what immediate next step is safe

Do not require every field everywhere on day one. Add or refresh the smallest
useful subset when a task reaches a meaningful checkpoint, becomes blocked, or
is likely to switch actors.

Keep `handoff_refs` selective. Prefer the current project handoff index and at
most one relevant episodic note.

## Compatibility Note

Older task packets may still contain legacy metadata names such as
`actor_family`, `logical_role`, `work_context`, or `session_instance`. Treat
those as compatibility/provenance fields. New packets should use
`actor_role`, `agent_family`, `agent_instance_id`, `work_type`, `work_lane`,
`artifact_scope`, and `artifact_refs`.

MCP semantic writes have their own stricter schema. Do not use legacy task
packet fields as a substitute for required MCP write identity fields.
