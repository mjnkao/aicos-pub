# A1-26224 A1 Identity And Layered Rules Implementation Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Source

Normalized from:

```text
docs/New design/A1-26224_AICOS_A1_Identity_Layered_Rules_Startup_And_Continuation_Model.md
```

## What Was Normalized

- A1 identity shape:
  `<actor_family> / a1-work / <scope> / <work_context> / <session_instance>`
- A1 layered rule model:
  A1 core -> future company/workspace -> project -> workstream/task.
- A1 startup card wording so startup remains light and packet-first.
- A1 task packet guidance so project, workstream, branch/work context, and task
  are not collapsed.
- A1 continuation guidance with owner, work context, continuation mode, handoff
  refs, done/blocked/next-step fields.

## Where It Was Placed

- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`
- `agent-repo/classes/a1-work-agents/rule-cards/layered-rules.md`
- `agent-repo/classes/a1-work-agents/rules/layered-rules.md`
- `agent-repo/classes/a1-work-agents/task-packets/README.md`
- `agent-repo/classes/a1-work-agents/tasks/README.md`
- `brain/shared/templates/scope-layer-note-template.md`
- `packages/aicos-kernel/contracts/task-packet-template.md`

## Future Company / Workspace Expansion

The repo now names company/workspace scope layers as future extension points,
but does not require A1 startup to load them by default and does not create a
large governance tree.

Future layers can use a small scope note or project bootstrap pointer when a
real company/workspace rule exists.

## Intentionally Left For Later

- full company/workspace rule systems
- A1 registry engine
- orchestration runtime
- Crypto-specific A1 rules
- automated rule-stack resolver

## Remaining Risk

Until real A1 tasks exist, the layered model is still policy/convention rather
than heavily validated behavior. The next real Crypto Trading slice should test
whether the task packet and task-state metadata are enough for A1-to-A1
continuation.
