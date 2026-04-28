# Sample Research Digest

Status: public example

This sample project demonstrates how an external project can use AICOS as a
context and coordination layer without storing the whole project repo inside
AICOS.

The sample domain is intentionally synthetic. It models a small team that
collects public research notes, normalizes them, and packages a daily digest for
an AI assistant.

## What This Example Shows

- A project profile with an explicit authority split.
- Compact canonical digests instead of a full source mirror.
- Working state for current project reality.
- A role-aware context ladder.
- A workstream slice.
- A task packet index.

## Authority Model

- AICOS owns context/control-plane surfaces: project digests, working state,
  context ladders, task packets, risks, open questions, and continuity.
- The external sample project repo owns runtime artifacts: source collectors,
  tests, scripts, generated digest files, and source provenance.
- Imported source notes remain evidence unless reviewed and promoted into
  compact AICOS project context.

## Project-Facing Roles

This example distinguishes AICOS-internal actor classes from project-facing
roles.

Project-facing roles include:

- CEO / sponsor
- Product owner
- CTO / architect
- Fullstack dev / worker
- Reviewer
- Operator

Each role should receive a bounded context pack appropriate to its job.

## Suggested Read Path

Start with:

```text
brain/project/canonical/project-profile.md
brain/project/working/context-ladder.md
brain/project/working/current-state.md
workstreams/default-digest-slice.md
task-packets/README.md
```
