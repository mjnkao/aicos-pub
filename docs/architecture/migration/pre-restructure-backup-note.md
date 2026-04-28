# Pre-Restructure Backup Note

Status: active migration note

Old AICOS data has been moved out of the active root to reduce ambiguity during
the new architecture build.

Backup location:

```text
backup/pre-restructure-20260418/
```

Remote backup branch:

```text
backup/pre-restructure-main
```

## Rule For Agents

Do not read old data by default. The backup is reference material only.

If a task needs old content:

1. inspect only the relevant path inside the backup;
2. cite the backup source path;
3. copy or migrate only the reviewed piece into the new structure;
4. keep `canonical`, `working`, `evidence`, runtime, backend, and service
   knowledge boundaries explicit.

## Current Active Structure

The active structure is the new MVP structure at repo root:

- `brain/`
- `agent-repo/`
- `packages/aicos-kernel/`
- `serving/`
- `backend/`
- `integrations/`
- `docs/New design/`
- `docs/migration/`
