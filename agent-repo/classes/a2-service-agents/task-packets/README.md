# A2-Core Task Packet Index

Use this index to choose one task packet. Do not load every packet at startup.

If no concrete task has been selected, stay at orientation level and ask the
human which task to continue.

## Packets

- `a2-core-writeback-self-brain-refresh.md` — refresh concise self-brain after a meaningful A2-Core state transition.
- `a2-core-option-choose-decision-commit.md` — commit a clear human/manager option choice into AICOS working state.
- `a2-core-sync-brain-serving-refresh.md` — refresh GBrain/PGLite serving substrate from current `brain/`.

## Loading Rule

Load a full task packet only after the task is chosen or strongly implied.

Load only the rule cards named by that packet.

## Handoff-Ready Metadata

Task packets may include thin continuation metadata:

- `actor_family`
- `logical_role`
- `work_context`
- `current_owner`
- `task_status`
- `last_checkpoint_at`
- `handoff_ready`
- `next_actor_hint`
- `what_is_done`
- `what_is_blocked`
- `next_step`

This metadata does not create a takeover layer. It only makes actor switching
cheaper when a task is paused, blocked, or continued by another A2/A1 later.

Keep `handoff_refs` small. Do not point to many handoffs by default.
