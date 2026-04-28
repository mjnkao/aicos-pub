# A2-Core Task Packet: Option Choose Decision Commit

```yaml
schema_version: "0.1"
kind: "aicos.task_packet"
task_id: "a2-core-option-choose-decision-commit"
actor: "A2-Core-C"
actor_family: "a2-service-agents"
logical_role: "a2-core-c"
scope: "projects/aicos"
work_context: "main / blocker option flow"
task_type: "option_choose | decision_commit"
objective: "Commit a clear human/manager option choice into AICOS working state using the existing option choose flow."
summary: "Commit a clear human/manager option choice into AICOS working state."
continuation_mode: "review_followup"
current_owner: "codex/a2-core-c/projects-aicos/main"
task_status: "checkpointed_current"
last_checkpoint_at: "2026-04-18"
handoff_ready: true
next_actor_hint: "A2-Core-C"
required_context:
  - "agent-repo/classes/a2-service-agents/startup-cards/a2-core.md"
  - "brain/projects/aicos/canonical/role-definitions.md"
  - "brain/projects/aicos/canonical/project-working-rules.md"
  - "brain/projects/aicos/working/current-state.md"
  - "brain/projects/aicos/working/current-direction.md"
  - "serving/branching/option-packets/aicos__blocker-001.md"
rules_to_load:
  - "agent-repo/classes/a2-service-agents/rule-cards/option-choose.md"
  - "agent-repo/classes/a2-service-agents/rule-cards/writeback.md"
allowed_write_lanes:
  - "agent-repo/classes/humans/approvals/"
  - "agent-repo/classes/a1-work-agents/tasks/blocked/"
  - "brain/projects/aicos/branches/"
  - "brain/projects/aicos/working/current-state.md"
  - "brain/projects/aicos/working/current-direction.md"
  - "brain/projects/aicos/working/open-questions.md"
success_condition: "The selected option is committed with `./aicos option choose aicos <blocker-id> <option-id>`; approval, branch state, blocker/open-question status, and working direction are consistent; other options remain preserved."
handoff_refs:
  - "brain/projects/aicos/working/handoff/current.md"
what_is_done: "`blocker-001` -> `option-a` has a proven local manager-choice flow."
what_is_blocked: "No current blocker; future choices may need richer actor registry/review signature policy."
next_step: "Use `./aicos option choose aicos <blocker-id> <option-id>` only after a clear human/manager choice."
access_paths:
  - "./aicos"
  - "agent-repo/classes/a1-work-agents/tasks/blocked/blocker-001.md"
  - "agent-repo/classes/humans/approvals/manager-choice-blocker-001.md"
  - "brain/projects/aicos/branches/blocker-001-option-a/selection-state.md"
notes: "Current proven example is `blocker-001` -> `option-a`. Do not promote canonical truth or delete unselected option branches in this task."
```
