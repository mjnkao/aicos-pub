# IMP-26269 / KIT Readiness Audit Note

Date: 2026-04-19
Actor: A2-Core Codex 1
Scope: `projects/aicos`

## Readiness Conclusion Before This Pass

NOT READY.

The shared Import Kit templates existed and were coherent, but the repo did not
yet give an independent A2-Core Codex 2 a single sample project-specific execution hub.
The templates also did not yet make the new `full active context import +
isolated external checkout` strategy explicit enough.

## What Was Added

Created sample project-specific import execution cluster:

```text
brain/projects/sample-project/evidence/import-kit/
```

This cluster includes:

- `README.md`
- `import-master-checklist.md`
- `import-identity.md`
- `source-inventory.md`
- `authority-and-lane-mapping.md`
- `slice-definition.md`
- `bootstrap-output-checklist.md`
- `a1-import-startup.md`
- `import-validation.md`

## Shared Kit Refinement

Refined shared Import Kit templates to explicitly cover:

- full active context import
- explicit excluded historical/reference surfaces
- isolated checkout facts
- A2-Core Codex 1 vs A2-Core Codex 2 role separation
- independent execution validation
- no reliance on old-thread context

## What Was Not Done

- no real sample project import
- no isolated checkout inspection
- no source truth digestion
- no MCP runtime/server implementation
- no automation/generator work
- no A1 importer execution

## Next Expected Pass

The next pass should be written for A2-Core Codex 2.

A2-Core Codex 2 should use:

```text
brain/projects/sample-project/evidence/import-kit/README.md
```

as the import hub, then perform the real sample project import under:

- full active context import
- isolated external checkout
- no MCP runtime implementation yet

## Readiness Conclusion After This Pass

READY for a separate A2-Core Codex 2 execution brief.

This does not mean the sample project import is complete. It means the repo now contains a
single project-specific hub and enough checklist detail for an independent
operator to run the real import without inheriting A2-Core Codex 1 context.
