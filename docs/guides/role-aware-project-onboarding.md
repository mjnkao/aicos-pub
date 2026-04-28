# Role-Aware Project Onboarding

Status: draft guide

## Problem

AICOS has internal actor classes such as A1 and A2. External projects have their
own project-facing roles such as CEO, product owner, CTO, fullstack dev,
reviewer, worker, and operator.

Those two role systems should not be conflated.

## Principle

Use AICOS actor classes to control access patterns and writeback behavior. Use
project-facing roles to decide which project context an agent should read.

## Minimum Role Context Request

A role-aware context request should include:

- project id
- project-facing role
- mode
- workstream or task area
- selected task packet, if known
- desired depth

Example:

```text
project_id: sample-project
project_role: cto
mode: onboarding
workstream: default-digest-slice
depth: compact
```

## Suggested Role Reads

| Role | Primary Context |
| --- | --- |
| CEO / sponsor | project profile, current state, risks, decisions |
| Product owner | project brief, delivery baseline, open items, acceptance criteria |
| CTO / architect | architecture baseline, source/data scope, technical risks |
| Fullstack dev / worker | selected task packet, current state, relevant source paths |
| Reviewer | task packet, acceptance criteria, changed artifacts, test evidence |
| Operator | delivery surface, runbook, active risks, reliability notes |

## Expected Tool Shape

Future AICOS role-aware query tools should return bounded context packs.

Possible interface:

```text
aicos_get_role_context(project_id, project_role, mode, workstream?, task_id?, depth?)
aicos_search_project_context(project_id, project_role, query, filters?)
```

The result should cite source paths and explain why each item is included for
that role.

## Safety

Role-aware onboarding should still respect privacy and authority boundaries.
It should not bulk-read private evidence, handoffs, generated outputs, logs, or
source repo internals unless the selected task requires them.
