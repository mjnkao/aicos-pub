# A1 Task State Convention

A1 task lanes hold actor-owned execution state for project work. They are not
project truth.

Use:

- `current/` for actively owned work
- `backlog/` for actionable future work
- `blocked/` for work waiting on human/system/project condition
- `completed/` for finished task notes

Task state should follow:

```text
brain/shared/templates/task-state-template.md
```

Project reality belongs in `brain/projects/<project-id>/working/`. Actor
execution state belongs here.

## Continuation Fields

For A1-to-A1 continuation, always keep these clear when the task is active,
blocked, waiting, or handoff-ready:

- actor family
- logical role
- scope
- work context
- primary artifact(s)
- current owner
- continuation mode
- handoff refs
- last checkpoint
- next actor hint
- what is done
- what is blocked
- next step

Do not assume project = workstream = work context = task. Use `work_context` to
name route/workstream/session continuity when it matters.

Coding is supported, but A1 task state should also work for design concepts,
content drafts, research outputs, operational plans, and hybrid artifact sets.
