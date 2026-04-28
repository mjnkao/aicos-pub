# A1 Writeback Rules

Status: reference/deep policy, not startup-default

A1 writes:

- project working updates to `brain/projects/<project-id>/working/`;
- blockers and tasks to `agent-repo/classes/a1-work-agents/tasks/`;
- option packets through `serving/branching/option-packets/`.

A1 follows the shared checkpoint policy:

```text
brain/shared/policies/checkpoint-writeback-policy.md
```

Do not write every chat turn. Checkpoint at meaningful artifact milestones,
blocked or waiting states, scope/work-context switches, likely handoffs, and
long pauses.

A1 must not mix project truth with actor task execution. Project/workstream
facts go to project lanes; owner/status/next-step continuity goes to A1 task
state.
