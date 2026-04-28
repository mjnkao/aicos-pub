# FLW-26124 Implementation Note

Date: 2026-04-18
Status: implemented-mvp

## Summary

Implemented the first local MVP behavior for chat decision writeback:

```text
human chat choice -> aicos option choose -> AICOS state update -> aicos sync brain
```

No UI, public API, canonical promotion, or backend authority layer was added.

## `aicos option choose`

Command:

```text
aicos option choose <project-id> <blocker-id> <option-id>
```

Optional flags:

```text
--actor <id>
--reason <text>
```

The command reads:

- `serving/branching/option-packets/<project-id>__<blocker-id>.json`
- `brain/projects/<project-id>/branches/<selected-branch>/`

The command updates:

- `agent-repo/classes/humans/approvals/manager-choice-<blocker-id>.md`
- `brain/projects/<project-id>/branches/<selected-branch>/selection-state.md`
- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`
- `brain/projects/<project-id>/working/open-questions.md`
- `agent-repo/classes/a1-work-agents/tasks/blocked/<blocker-id>.md` when present

The command does not change:

- `brain/projects/*/canonical/*`
- other option branches
- backend truth
- GBrain/PGLite index

## `aicos sync brain`

Command:

```text
aicos sync brain
```

The command now:

- scans markdown files under `brain/`
- initializes local GBrain/PGLite in `.runtime-home/.gbrain/` if needed
- imports `brain/` into GBrain/PGLite with `--no-embed`
- reports scanned lanes, import counts, skipped policy lanes, and result

Excluded by default:

- `agent-repo/`
- `backend/`
- `backup/`
- `imports/`
- `scripts/`
- `integrations/`

## Verification

Verified locally:

```text
PYTHONPYCACHEPREFIX=/tmp/aicos-pycache python3 -m py_compile packages/aicos-kernel/aicos_kernel/*.py
./aicos option choose aicos blocker-001 option-a --actor manager-min --reason "..."
./aicos sync brain
```

`sync brain` imported 61 markdown files from `brain/` into local GBrain/PGLite
with 0 errors.
