# KIT-26261 Import Kit Template System Note

Date: 2026-04-19
Actor: A2-Core-C
Scope: `projects/aicos`

## What Was Added

Created shared reusable Import Kit templates at:

```text
brain/shared/templates/project-import-kit/
```

Files added:

- `import-master-checklist-template.md`
- `import-identity-template.md`
- `source-inventory-template.md`
- `authority-and-lane-mapping-template.md`
- `slice-definition-template.md`
- `bootstrap-output-checklist-template.md`
- `a1-import-startup-template.md`
- `import-validation-template.md`

## Why This Pass Exists

AICOS is preparing for repeatable cross-repo project onboarding. The shared kit
lets A2-Core instantiate a bounded import cluster for projects such as
`sample-project` without reinventing checklist structure each time.

## Constraints Preserved

- no MCP runtime implemented
- no generator/script automation added
- no sample project-specific wording in shared templates
- no external repo mirroring
- packet-first, startup-light, authority-separated logic preserved
- external repo remains code/runtime authority
- AICOS remains context/control-plane authority

## Next Expected Step

Instantiate this kit for:

```text
brain/projects/sample-project/evidence/import-kit/
```

That next pass should be project-specific. This pass only creates the shared
template system.
