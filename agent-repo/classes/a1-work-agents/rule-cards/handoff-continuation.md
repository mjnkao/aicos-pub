# Rule Card: A1 Handoff And Continuation

Load when continuing a previous task, handing off work, or recovering after an
interruption.

## Read

- Prefer MCP when available:
  `./aicos mcp read handoff-current --actor A1 --scope projects/<project-id>`
- Fallback direct file:
  `brain/projects/<project-id>/working/handoff/current.md`
- selected task packet or task state
- project `current-state.md` and `current-direction.md`

If the task belongs to a workstream, artifact route, branch, or task-specific
context, read only the packet/note that names that context. Do not infer it from
project scope alone.

## Write

Prefer Phase 2 semantic MCP write tools:

- `aicos_write_handoff_update` for the compact continuation update.
- `aicos_write_task_update` when task status/owner/blocker/next step changes.
- `aicos_record_checkpoint` when a meaningful artifact or validation
  checkpoint was reached.

Checkpoint the task state with:

- actor family and current owner
- project scope and work context
- continuation mode
- primary artifact(s) and meaningful work delta
- what is done
- what is blocked
- next step
- handoff refs
- touched lanes
- whether another actor can continue

If MCP is unavailable, use the smallest correct direct-file fallback and record
that fallback in the update.

Do not read old handoffs or raw history unless the current handoff/task packet
points there.
