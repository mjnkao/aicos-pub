# HMD-26210 Handoff-Ready Task Metadata Implementation Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Source

Normalized from:

```text
docs/New design/HMD-26210_AICOS_Handoff_Ready_Task_Metadata_Model_And_Implementation_Guide.md
```

## Metadata Normalized

Added a thin continuation vocabulary for task packets and actor task state:

- `actor_family`
- `logical_role`
- `work_context`
- `current_owner`
- `task_status`
- `continuation_mode`
- `last_checkpoint_at`
- `next_actor_hint`
- `handoff_ready`
- `what_is_done`
- `what_is_blocked`
- `next_step`

Status vocabulary normalized:

- `owned_current`
- `checkpointed_current`
- `blocked_waiting_human`
- `blocked_waiting_system`
- `handoff_ready`
- `taken_over`

## Where It Was Placed

- `packages/aicos-kernel/contracts/task-packet-template.md`
- `agent-repo/classes/a2-service-agents/task-packets/README.md`
- `agent-repo/classes/a2-service-agents/tasks/README.md`
- `agent-repo/classes/a2-service-agents/tasks/backlog/README.md`
- `brain/projects/aicos/canonical/project-working-rules.md`
- current A2-Core task packets in
  `agent-repo/classes/a2-service-agents/task-packets/`

## Intentionally Not Built

- no `transfer/` lane
- no takeover daemon
- no dedicated transfer queue
- no large registry
- no API/UI surface
- no DB-first handoff engine

## Remaining Risk / Later Work

The metadata is now visible but still lightweight. After a few real blocked,
waiting, and actor-switch cases, A2-Core should refine which fields are required
for which task types and whether validation belongs in the kernel.
