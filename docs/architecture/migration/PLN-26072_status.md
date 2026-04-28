# PLN-26072 Migration Status

Status: initial MVP scaffold

## Completed

- Added target root lanes: `packages/`, `brain/`, `agent-repo/`, `serving/`,
  `backend/`, and `integrations/`.
- Added minimal `packages/aicos-kernel` contracts, schemas, validators notes,
  renderers notes, promotion primitives, write lanes, and GBrain adapter notes.
- Added thin local `aicos` CLI wrapper.
- Seeded project `aicos` brain files for reviewer inspection.
- Added class-based A1, A2, human operational lanes.
- Added A2 service skill markdown contracts.
- Moved old root data and old docs/scripts into
  `backup/pre-restructure-20260418/` so the active root now shows the new
  structure clearly.

## In Progress

- Harden blocked-to-options-to-manager-choice flow after first CLI-backed proof.
- Validate command outputs across additional blockers/projects.
- Selectively migrate old material from backup only when needed.

## Updated 2026-04-18

- Added `aicos option choose <project-id> <blocker-id> <option-id>`.
- `option choose` now records manager chat decisions into human approval,
  selected branch state, project working state/direction, open question status,
  and blocker status.
- `aicos sync brain` now scans/imports `brain/` into local GBrain/PGLite and
  excludes non-brain lanes by default.
