# A2 Task State Convention

This lane holds actor-owned execution state. It is not project truth.

## Task State Fields

When a task state file in `current/`, `blocked/`, or `waiting/` needs to be
handoff-ready, include the smallest useful subset:

```yaml
actor_family: "a2-service-agents"
logical_role: "a2-core-c"
scope: "projects/aicos"
work_context: "main"
current_owner: ""
task_status: "owned_current"
continuation_mode: "continue_previous"
handoff_ready: false
last_checkpoint_at: ""
next_actor_hint: ""
handoff_refs:
  - "brain/projects/aicos/working/handoff/current.md"
what_is_done: ""
what_is_blocked: ""
next_step: ""
touched_lanes:
  - ""
```

## Status Vocabulary

- `owned_current`: current actor is actively working.
- `checkpointed_current`: current actor has checkpointed safely.
- `blocked_waiting_human`: waiting for human input or approval.
- `blocked_waiting_system`: waiting for tool/runtime/system state.
- `handoff_ready`: another actor can continue without large reconstruction.
- `taken_over`: another actor has started continuing.

## Rule

Do not update task metadata for every micro-step. Update it at meaningful
checkpoints: blocked/waiting state, actor switch likely, scope switch, branch
switch, milestone completed, or pause before a long interruption.

Do not create a transfer queue or takeover subsystem in this phase.
