# A1 Layered Rules Model

Status: reference/deep policy, not startup-default

A1 is a project-work agent class, not a singleton actor and not one project's
workflow.

## Identity Shape

Use this lightweight identity shape when describing an A1 instance:

```text
<actor_role> / <agent_family> / <scope> / <work_type> / <work_lane> / <agent_instance_id>
```

Examples:

- `A1 / codex / projects/<project-id> / code / branch-main / thread-01`
- `A1 / claude-code / projects/<project-id> / research / scenario-a / session-02`
- `A1 / openclaw / projects/<project-id> / design / concept-route-a / session-03`

For current MCP write identity and worktree coordination rules, use:

```text
brain/shared/policies/agent-coordination-policy.md
```

## Rule Layers

Load rules from broad to narrow, but only as needed:

1. shared/global operating policy
2. A1 core rules
3. company-scoped rules, if present and relevant
4. workspace-scoped rules, if present and relevant
5. project-scoped rules
6. workstream/task-specific rules

Current MVP does not implement full company/workspace rule systems. The model
keeps room for them by using scope-neutral wording and by not hardcoding A1 as
project-only forever.

## Boundary

- A1 core rules are domain-neutral.
- A1 core rules are artifact-neutral: code, docs, design, content, research, and
  hybrid work are all valid lower-layer artifact choices.
- Project rules belong with the project.
- Workstream/task rules are trigger-loaded by task packet or explicit task
  selection.
- Coding, Crypto Trading, design, content, or research rules must not leak into
  A1 core.
