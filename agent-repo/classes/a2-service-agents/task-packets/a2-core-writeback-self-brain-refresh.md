# A2-Core Task Packet: Writeback Self-Brain Refresh

```yaml
schema_version: "0.1"
kind: "aicos.task_packet"
task_id: "a2-core-writeback-self-brain-refresh"
actor: "A2-Core-C"
actor_family: "a2-service-agents"
logical_role: "a2-core-c"
scope: "projects/aicos"
work_context: "main / self-brain"
task_type: "writeback | self_brain"
objective: "Refresh concise AICOS self-brain after a meaningful A2-Core state transition, without turning working files into chat logs."
summary: "Refresh concise self-brain after a meaningful A2-Core state transition."
continuation_mode: "continue_previous"
current_owner: "codex/a2-core-c/projects-aicos/main"
task_status: "handoff_ready"
last_checkpoint_at: "2026-04-18"
handoff_ready: true
next_actor_hint: "A2-Core-C"
required_context:
  - "agent-repo/classes/a2-service-agents/startup-cards/a2-core.md"
  - "brain/projects/aicos/canonical/role-definitions.md"
  - "brain/projects/aicos/canonical/project-working-rules.md"
  - "brain/projects/aicos/working/current-state.md"
  - "brain/projects/aicos/working/current-direction.md"
rules_to_load:
  - "agent-repo/classes/a2-service-agents/rule-cards/writeback.md"
allowed_write_lanes:
  - "brain/projects/aicos/working/current-state.md"
  - "brain/projects/aicos/working/current-direction.md"
  - "brain/projects/aicos/working/implementation-status.md"
  - "brain/projects/aicos/working/open-questions.md"
  - "brain/projects/aicos/working/open-items.md"
  - "brain/projects/aicos/working/active-risks.md"
  - "brain/projects/aicos/working/potential-risks.md"
  - "brain/projects/aicos/working/tech-debt.md"
success_condition: "Only meaningful state changes are recorded; self-brain remains short, current, and startup-useful; canonical truth is untouched unless explicitly reviewed."
handoff_refs:
  - "brain/projects/aicos/working/handoff/current.md"
what_is_done: "Self-brain lanes exist for current state, direction, open questions, open items, risks, tech debt, and handoff."
what_is_blocked: "Do not promote working state to canonical without explicit review."
next_step: "After meaningful A2-Core state transitions, update only the smallest correct self-brain lanes."
access_paths:
  - "brain/projects/aicos/working/handoff/current.md"
  - "packages/aicos-kernel/contracts/task-packet-template.md"
notes: "Use W3 working-state writeback only for clear transitions such as completed milestone, changed direction, confirmed risk, or durable open question."
```
