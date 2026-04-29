# A2 Handoff Policy

Status: reference/deep policy, not startup-default

Handoff is a continuity layer for meaningful transitions between sessions or
agents. It is not a complete history and not the permanent home of stable truth.

## Layers

- H1 current handoff index: one concise current index for the active phase.
- H2 episodic handoff notes: bounded notes for specific passes, tests, or
  experiments.
- H3 self-brain digest: stable/current information digested into
  `brain/projects/aicos/working/`.

## Location And Naming

Project-scoped active handoff lives with the project.

- H1 current index: `brain/projects/<project-id>/working/handoff/current.md`
- H2 episodic notes: `brain/projects/<project-id>/working/handoff/episodes/`
- H2 naming: `YYYY-MM-DD_<actor-lane>_<topic>.md`
- Shared/system-wide handoffs only: `brain/shared/handoffs/`
- Migration and implementation provenance: Git history or explicit evidence
  refs, not default startup docs.

For `projects/aicos`, the sole H1 current handoff index is:

```text
brain/projects/aicos/working/handoff/current.md
```

`brain/projects/aicos/working/handoff-summary.md` is digest/reference only.

Superseded or stale handoffs are reference-only. They do not override the H1
current index or self-brain digest.

## Reading

Start packet-first. Read the current handoff index only for continuation,
migration/state alignment, repo-wide architecture, or newest-vs-stale checks.

Read old episodic handoffs only on demand.

If no concrete task has been chosen, stay at orientation plus packet index level
and ask the human which task to continue.

## Writing

Refresh the current index when the main current story changes. Create an
episodic note only for bounded work that needs provenance.

Do not append every small change to handoff files.
