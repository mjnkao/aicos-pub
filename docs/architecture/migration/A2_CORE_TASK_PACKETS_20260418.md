# A2-Core Task Packets Implementation Note

Date: 2026-04-18
Status: implemented-small-step

## Placement

Packets were placed in:

```text
agent-repo/classes/a2-service-agents/task-packets/
```

Files:

- `a2-core-writeback-self-brain-refresh.md`
- `a2-core-option-choose-decision-commit.md`
- `a2-core-sync-brain-serving-refresh.md`

## Why This Lane

These packets are operational handoff/startup context for A2 service agents.
They are not canonical project truth, not generated serving output, and not
kernel code. Keeping them beside A2 startup cards and rule cards is the smallest
coherent lane.

## Weak Fields

- `task_type` is still stringly typed.
- `allowed_write_lanes` mixes exact files, directories, and runtime paths.
- `access_paths` is useful but not yet distinguished by read/write/command.

## Packet-First Result

Packet-first startup feels lighter for these tasks. A co-worker can start from a
packet plus one or two rule cards, instead of reading long design docs before
knowing the task boundary.

## Fresh-Thread Context Start Test

A later fresh-thread test used:

```text
./aicos context start A2-Core-C projects/aicos
```

The bare command form failed in that environment:

```text
aicos context start A2-Core-C projects/aicos
```

Observed result:

- `./aicos context start ...` returned usable hot context.
- The sync task packet plus `sync-brain` rule card was enough to run
  `./aicos sync brain`.
- Packet-first startup stayed lighter than loading long design docs.

Recorded follow-ups:

- improve task packet list with one-line summaries;
- improve PATH/command consistency for bare `aicos ...`;
- tighten Suggested Next Reads for the smallest startup path;
- decide when task packet metadata should become richer.
