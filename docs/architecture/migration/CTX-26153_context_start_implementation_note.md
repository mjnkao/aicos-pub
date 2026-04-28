# CTX-26153 Context Start Implementation Note

Date: 2026-04-18
Status: implemented-small-step

## Command Shape

```text
./aicos context start <actor> [scope]
```

MVP supported values:

- actor: `A2-Core`, `A2-Core-C`, or `A2-Core-R`
- scope: `projects/aicos` by default

## Why This Is Smallest Correct

The command prints one concise startup bundle and exits. It does not resolve
arbitrary context graphs, mutate files, call network services, or manage an
external co-worker runtime.

## Read Lanes

- `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`
- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `agent-repo/classes/a2-service-agents/task-packets/`
- `agent-repo/classes/a2-service-agents/rule-cards/`

## Intentionally Not Done

- no full resolver API
- no JSON Schema expansion
- no UI, network, MCP, or public API scope
- no long design docs auto-loaded
- no mutation of truth, working state, runtime memory, or external agent memory

## Future Extension Points

- support A1 and A2-Serve actor lanes
- add `--packet <task-id>` once packet identifiers stabilize
- add machine-readable output only after real packet examples settle
