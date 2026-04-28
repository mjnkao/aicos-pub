# STR-26185 Storage Structure Implementation Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Source

Normalized from:

```text
docs/New design/STR-26185_AICOS_Storage_Structure_For_Handoff_Open_Items_Open_Questions_Risks_Research_And_Agent_Tasks.md
```

## What Changed

- Added project-scoped H1 current handoff index:
  `brain/projects/aicos/working/handoff/current.md`
- Added H2 episodic handoff lane:
  `brain/projects/aicos/working/handoff/episodes/`
- Added project working lanes:
  `brain/projects/aicos/working/open-items.md`
  `brain/projects/aicos/working/potential-risks.md`
  `brain/projects/aicos/working/tech-debt.md`
- Added research evidence lane:
  `brain/projects/aicos/evidence/research/`
- Marked shared handoffs as reserved for genuinely cross-project/system-wide
  handoffs:
  `brain/shared/handoffs/README.md`
- Updated handoff rules so active project continuity lives with the project,
  while old handoff files are outside the active loading path.
- Moved old handoff/provenance files to:
  `backup/handoff-provenance-20260418/`

## Architecture Conflict Resolved

Earlier HOF-26169 normalization kept H1/H2 in `docs/migration/` because the
repo was still migration-heavy. STR-26185 refines that direction: active project
handoff should live under `brain/projects/<project>/working/handoff/`.

Resolution chosen:

- create the new project-scoped H1/H2 lanes now
- move old handoff files to backup so new agents do not follow the old loading
  path
- keep only backup/audit access for old files

## Intentionally Left For Later

- Audit/extraction from old handoff backup if missing information is discovered
- DB-backed registries for handoffs/open items/tasks
- Full schema enforcement for handoff files
- Broader startup resolver behavior beyond current MVP

## Practical Rule

Use the smallest correct lane:

- project continuity: `brain/projects/<id>/working/handoff/`
- project unresolved knowledge: `brain/projects/<id>/working/`
- project evidence/research: `brain/projects/<id>/evidence/`
- actor execution: `agent-repo/.../tasks/...`
- true shared/system-wide knowledge: `brain/shared/...`
- migration/provenance notes: `docs/migration/`
