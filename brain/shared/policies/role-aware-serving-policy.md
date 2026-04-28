# Role-Aware Serving Policy

Status: active MVP policy
Updated: 2026-04-22

## Purpose

Let AICOS serve context by service boundary and project/company role without
turning role labels into rigid universal law.

## Role Layers

- `actor` / `actor_role`: AICOS service boundary, such as `A1`,
  `A2-Core-C`, or `A2-Core-R`.
- `project_role`: human-like responsibility in the project, such as
  `developer`, `qa`, `designer`, `writer`, `product-owner`, `architect`,
  `manager`, `analyst`, `operator`, or `reviewer`.

Do not collapse these layers. `A1` is not an agent family and not a project
role.

## MVP Behavior

Read tools may accept optional `project_role`. When present, AICOS may:

- include the role in metadata;
- filter or rank registry/query results using role tags;
- recommend role-relevant context;
- keep `all` role-tagged sources visible.

If role metadata is missing, serve the default project context rather than
blocking the agent.

## Artifact-Neutral Rule

Role-aware serving must work for code, content, design, research, ops, data,
review, planning, and mixed projects. Coding-specific fields such as branch or
worktree must not become mandatory for non-code roles.

## Future Direction

Role-aware behavior should mature through context registry metadata, task packet
metadata, feedback signals, and reviewed project profiles. It should not become
hardcoded per-project business logic in the kernel.
