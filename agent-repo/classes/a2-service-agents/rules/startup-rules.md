# A2 Startup Rules

Status: reference/deep policy, not startup-default

A2 agents improve AICOS itself. They should read only the smallest context that
matches the task, then expand if the task proves it needs more.

## Current A2-Core Startup

For current repo build/refactor/config work, Codex is usually `A2-Core-C`.

Read first:

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`
- relevant `brain/projects/aicos/working/*` files for the task

Long source docs in `docs/New design/` are reference/provenance, not default
startup context.

Read the current handoff index only for continuation, migration/state
alignment, repo-wide architecture, or newest-vs-stale checks:

```text
brain/projects/aicos/working/handoff/current.md
```

Do not load old episodic handoffs or backup handoff provenance by default.

## A2-Serve Status

A2-Serve is target architecture for future service support to A1. It is not yet
a fully active runtime lane.
