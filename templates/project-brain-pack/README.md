# AICOS Project Brain Pack Template

Status: shared reusable template

## Purpose

This pack is the minimal project-brain shape for creating or publishing a new
AICOS-managed project without copying private project context.

Use it when a new company, workspace, or project needs a clean starting brain
that can be mounted through `AICOS_BRAIN_ROOT`, copied into
`brain/projects/<project-id>/`, or included in a public template repo.

## Contents

- `pack-manifest.md`: boundary, copy rules, and required files.
- `sample-project/`: synthetic sample project brain with no private data.

## Non-Goals

- No generator or installer logic.
- No public export manifest rewrite.
- No project-specific truth.
- No copied sample project, AICOS private, or customer context.

## Copy Rule

Copy `sample-project/` to:

```text
brain/projects/<project-id>/
```

Then replace `sample-project` identifiers and summaries with real project
facts. Do not leave sample placeholders in a production project brain.

## Required Runtime Boundary

The pack assumes AICOS code resolves the active brain root through:

```text
AICOS_BRAIN_ROOT
```

Default remains `<repo>/brain`.

## Validation Smoke

After copying a project brain:

```bash
./aicos brain status
./aicos mcp read startup-bundle --actor A1 --scope projects/<project-id>
./aicos mcp read status-items --actor A1 --scope projects/<project-id>
```

If the project is served through the HTTP daemon, run:

```bash
./aicos sync brain --text-only
scripts/aicos-retrieval-eval --max-results 5 --gate
```
