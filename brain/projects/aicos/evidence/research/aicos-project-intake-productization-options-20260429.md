# AICOS Project Intake Productization Options

Status: options memo, no implementation
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Define the minimal productization path for adding a new project to AICOS
without creating a heavy project-management or onboarding platform.

Related surfaces:

- `aicos_propose_project` MCP write tool;
- project brain pack template;
- project registry;
- project context ladder;
- token/access policy.

## Current State

AICOS already has:

- project proposal write tool;
- reusable project brain pack template;
- project registry surface;
- context ladders;
- A1/A2 actor model;
- MCP read/write path;
- token/access policy concepts.

The gap is the end-to-end flow. A proposed project can be recorded, but there
is not yet a clean lifecycle from proposal to active project pack and access
policy.

## Minimal Flow

```text
project proposal
-> human/A2 review
-> approval / reject / needs-more-info
-> project brain pack creation/import
-> project registry entry
-> token/access scope decision
-> project context ladder
-> first open items/tasks/questions
-> sync/index
```

## Options

| Option | Description | Pros | Cons | Fit |
| --- | --- | --- | --- | --- |
| A. Manual checklist flow | Keep proposal tool; A2 manually copies project brain pack and updates registry | Lowest risk, transparent | Manual errors, repeated steps | Best now |
| B. Semi-automated scaffold CLI | Add a CLI that creates project pack from template after approval | Reduces errors, still controlled | Adds code and edge cases | Next after 2-3 real projects |
| C. Full MCP project creation tool | A1/A2 can create project brain directly through MCP | Smooth UX | Risky permissions, accidental project sprawl | Later |
| D. Import connector framework | Import from external repos/docs/PM tools | Powerful | Too broad and heavy | Company-100+ only |

## Recommended Near-Term Direction

Use Option A now, design Option B later.

Do not let A1 agents create active project brain directly. They can propose.
A2/human approves and creates/imports.

## Required States

Project proposal lifecycle:

- `proposed`
- `needs_more_info`
- `approved`
- `rejected`
- `created`
- `imported`
- `deferred`

## Minimum Approval Checklist

Before a project becomes active:

- project id is stable and path-safe;
- project owner/manager is known;
- project type is known: coding/content/design/research/ops/mixed;
- external authority is known:
  - code repo;
  - docs system;
  - design artifact;
  - content workspace;
  - research folder;
- AICOS authority boundary is clear;
- token/access scope is decided;
- first context ladder exists;
- first open items/questions exist.

## What Can Be Automated Later

Safe later automation:

- generate project brain pack from template;
- generate context ladder skeleton;
- create registry entry draft;
- create first status item/open question skeleton;
- run sync/index after creation.

Keep human/A2 approval for:

- final project activation;
- token/access policy;
- cross-project context sharing;
- importing private/sensitive materials;
- deleting/renaming project brain.

## Next Step

Keep the current proposal tool. After one or two more project proposals, add a
manual approval checklist doc or CLI dry-run that prints the planned project
pack changes without writing them.
