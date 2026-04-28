# A2-Core Task Packet: Sync Brain Serving Refresh

```yaml
schema_version: "0.1"
kind: "aicos.task_packet"
task_id: "a2-core-sync-brain-serving-refresh"
actor: "A2-Core-C"
actor_family: "a2-service-agents"
logical_role: "a2-core-c"
scope: "projects/aicos"
work_context: "main"
task_type: "sync | serving_refresh"
objective: "Refresh local serving/retrieval substrate from current `brain/` after meaningful AICOS state changes."
summary: "Refresh GBrain/PGLite serving substrate from current `brain/`."
continuation_mode: "continue_previous"
current_owner: "codex/a2-core-c/projects-aicos/main"
task_status: "handoff_ready"
last_checkpoint_at: "2026-04-18"
handoff_ready: true
next_actor_hint: "A2-Core-C"
required_context:
  - "agent-repo/classes/a2-service-agents/startup-cards/a2-core.md"
  - "brain/projects/aicos/canonical/project-working-rules.md"
  - "brain/projects/aicos/working/current-state.md"
  - "brain/projects/aicos/working/current-direction.md"
rules_to_load:
  - "agent-repo/classes/a2-service-agents/rule-cards/sync-brain.md"
allowed_write_lanes:
  - ".runtime-home/.gbrain/"
success_condition: "`./aicos sync brain` completes successfully and reports scanned/imported/updated `brain/` files; no truth, working state, canonical files, or external co-worker memory is mutated."
handoff_refs:
  - "brain/projects/aicos/working/handoff/current.md"
what_is_done: "MVP `./aicos sync brain` exists and has been verified after self-brain updates."
what_is_blocked: "Embedding/vector refresh is intentionally not forced in MVP sync."
next_step: "Run `./aicos sync brain` after meaningful `brain/` state changes, then verify zero errors."
access_paths:
  - "./aicos"
  - "brain/"
  - "tools/gbrain/"
  - ".runtime-home/.gbrain/"
notes: "Use after manager choices, self-brain refreshes, selected branch updates, or milestones that another agent should retrieve."
```
