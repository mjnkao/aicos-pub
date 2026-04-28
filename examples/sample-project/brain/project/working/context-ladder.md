# Sample Research Digest Context Ladder

Status: public sample
Scope: `projects/sample-project`

## Purpose

This ladder shows how a new agent can enter a project through AICOS without
bulk-reading the whole source repo or all project history.

## Layer 0 - Project Identity

Read:

- `brain/project/canonical/project-profile.md`

What you learn:

- project identity
- authority split
- AICOS context/control-plane boundary
- external project artifact/runtime boundary

## Layer 1 - Role-Aware Entry

Choose the project-facing role before reading deeper:

| Role | Read First | Purpose |
| --- | --- | --- |
| CEO / sponsor | current state, risks, decisions | outcomes and project health |
| Product owner | project brief, delivery baseline, open items | scope and acceptance |
| CTO / architect | architecture baseline, source/data scope | technical boundary |
| Fullstack dev / worker | selected task packet, current state | concrete execution |
| Reviewer | task packet, acceptance criteria, test evidence | review and risk check |
| Operator | delivery surface, runbook, active risks | reliable operation |

## Layer 2 - Current Working Reality

Read:

- `brain/project/working/current-state.md`
- `brain/project/working/current-direction.md`

What you learn:

- what is active now
- known gaps
- current next steps
- what is intentionally out of scope

## Layer 3 - Workstream Slice

Read after a role and task are known:

- `workstreams/default-digest-slice.md`

What you learn:

- current active delivery slice
- relevant source/runtime boundaries
- what to avoid loading by default

## Layer 4 - Task Support

Read:

- `task-packets/README.md`
- one selected task packet, after task selection

What you learn:

- task objective
- required context
- allowed write lanes
- acceptance criteria

## Layer 5 - Evidence And Source

Open external project repo files only when the selected task requires them.

Examples:

- source collectors
- schemas
- tests
- generated digest outputs
- source provenance

## Not Read By Default

- all source repo files
- all evidence
- stale handoff trails
- generated output bulk
- old prompts or logs
- private user data
