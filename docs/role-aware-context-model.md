# Role-Aware Context Model

Status: design stub

## Problem

A1 and A2 are AICOS-internal actor classes. External projects need their own
role model: CEO, product owner, CTO, fullstack dev, reviewer, worker, operator,
and domain-specific roles.

Each role needs different context during onboarding, continuation, search, and
task execution.

## Direction

AICOS should provide a role-aware context/query surface that accepts:

- project id
- project-facing role
- task or workstream
- state/mode such as onboarding, continuation, review, execution, or decision
- desired depth
- artifact type when relevant

The result should be a bounded context pack, not a broad dump of project files.

## Public API Shape To Explore

```text
aicos_get_role_context(project_id, project_role, mode, workstream?, task_id?, depth?)
aicos_search_project_context(project_id, project_role, query, filters?)
```

The API should still preserve AICOS authority boundaries and scrub/private-data
policy.
