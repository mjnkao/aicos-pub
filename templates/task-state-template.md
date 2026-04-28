# Task State Template

Status: shared reusable foundation

Use this for actor task files in `current/`, `blocked/`, or `waiting` lanes.
Do not create a transfer/takeover subsystem.

```yaml
task_id: ""
actor_family: ""          # example: a1-work-agents / a2-service-agents
logical_role: ""          # example: a1-work / a2-core-c
scope: ""                 # example: projects/<project-id>
work_context: ""          # branch/slice/module if useful
session_instance: ""
primary_artifacts:
  - ""
current_owner: ""
task_status: ""           # owned_current | checkpointed_current | blocked_waiting_human | blocked_waiting_system | handoff_ready | taken_over
continuation_mode: ""     # new_task | continue_previous | migration_followup | review_followup | branch_followup | handoff_followup
handoff_ready: false
last_checkpoint_at: ""
next_actor_hint: ""
handoff_refs:
  - ""
what_is_done: ""
what_is_blocked: ""
blocked_reason: ""
next_step: ""
touched_lanes:
  - ""
touched_artifacts:
  - ""
success_condition: ""
```

Update this metadata only at meaningful checkpoints.
