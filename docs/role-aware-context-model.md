# Role-Aware Context Model

Status: design stub

## Problem

A1 and A2 are AICOS-internal actor classes. External projects need their own
role model: CEO, product owner, CTO, fullstack dev, reviewer, worker, operator,
and domain-specific roles.

Each role needs different context during onboarding, continuation, search, and
task execution.

There is a second boundary: A1/A2 is also relative to the AICOS runtime that
receives the MCP call. The same Codex session can be an external `A1` when it
talks to a private/local AICOS runtime about the `projects/aicos-pub` export
project, and an internal `A2-Core-C` when it talks to the public Railway AICOS
runtime to maintain that public runtime.

Do not treat `A1`, `A2`, `Codex`, `Claude`, or `OpenClaw` as one global actor
identity across every runtime.

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

## Runtime Identity Rule

For MCP writes, keep these fields separate:

- `actor_role`: AICOS actor class relative to the current runtime.
- `agent_family`: client family, such as `codex`, `claude-code`, or `openclaw`.
- `execution_context`: client plus runtime alias, such as
  `codex-desktop via aicos_railway_public`.
- `work_context`: compact runtime and functional-role details, such as
  `runtime=aicos_railway_public; agent_position=external_agent; functional_role=reviewer`.

See:

```text
docs/architecture/runtime-agent-identity-boundary.md
```
