# Rule Card: Writeback

Load when the task may change AICOS state.

## Rule

Do not write every chat turn. Write only at meaningful state transitions.

## Commit Points

- decision made
- blocker confirmed
- option packet ready
- selected branch or direction changed
- milestone completed
- risk confirmed
- open question worth preserving
- backlog item clear enough for later

## Lanes

- scratch/runtime: `agent-repo/`
- working reality: `brain/projects/aicos/working/`
- canonical truth: only after review/promotion

## Never

- use `current-state.md` as a general inbox
- silently promote working to canonical
- treat backend/index state as authority
