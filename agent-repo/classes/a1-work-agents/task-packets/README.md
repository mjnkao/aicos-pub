# A1 Task Packet Index

Use this index to choose one A1 project task packet. Do not load every packet at
startup.

Project-specific A1 packets should bind:

- `actor: A1`
- `actor_family`
- `logical_role: a1-work`
- `scope: projects/<project-id>`
- `work_context` for route/workstream/session continuity; a git branch is only
  one possible form
- primary artifact(s)
- one clear task
- required context
- rule cards to load
- allowed write lanes
- success condition
- handoff-ready metadata when useful

If no concrete task has been selected, stay at orientation level and ask the
human which task to continue.

## Project Packet Indexes

- `sample-project/` — first cross-repo real-project test scaffold.

Use the shared template:

```text
packages/aicos-kernel/contracts/task-packet-template.md
```

## Layering Rule

A1 task packets may point to:

- A1 core rule cards
- project-specific rules
- workstream/task-specific rules
- future company/workspace rules only when they actually exist and are relevant

Do not make all higher-scope or domain-specific rules startup-default.

## Continuation Rule

Packets should separate:

- `scope`: project or future higher/lower scope
- `work_context`: route, scenario, branch, design concept, campaign angle,
  research path, workstream, or other continuity context
- `primary_artifacts`: code, docs, design, content, research, operational, or
  hybrid artifacts touched by the task
- `task_type`: concrete work kind
- `continuation_mode`: new task vs inherited/review/route/research recovery
