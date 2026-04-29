# Rule Card: Handoff

Load when a task is about continuation, migration/state alignment, repo-wide
architecture, or preparing another agent to continue.

## Model

- H1: current handoff index
- H2: episodic handoff notes
- H3: self-brain digest

## Current Index

```text
brain/projects/aicos/working/handoff/current.md
```

This is the sole H1 current handoff index for `projects/aicos`.

## Naming Convention

- Project current index: `brain/projects/<project-id>/working/handoff/current.md`
- Project episodic notes:
  `brain/projects/<project-id>/working/handoff/episodes/YYYY-MM-DD_<actor-lane>_<topic>.md`
- Shared/system-wide handoffs only: `brain/shared/handoffs/`
- Historical migration/implementation provenance is not default active handoff.
  Use Git history or explicit evidence refs only when provenance is needed.
- `brain/projects/aicos/working/handoff-summary.md` is digest/reference only,
  not H1 authority.
- Superseded/stale handoffs are reference-only unless the current index points
  to them.

## Write When

- meaningful implementation pass completes
- current vs stale story changes
- CLI/startup/operating model changes
- fresh-thread test has meaningful learning
- another agent/session is likely to continue

## Do Not Write For

- tiny wording fixes
- every chat clarification
- micro test runs
- facts that should only update self-brain

## Reading Rule

Do not read all old handoffs at startup. Read episodic handoffs only when the
current index points to them or the task needs provenance/detail.

If no concrete task has been selected, stay at index/suggestion level and ask
the human what to continue. Handoff should help continuation, not become another
startup burden.

## Digest Rule

Stable/current handoff facts should move into `brain/projects/aicos/working/`.
