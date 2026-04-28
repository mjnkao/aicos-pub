# Agent Coordination Policy

Status: shared hot-path policy

Use this policy when multiple agents may work on the same project, workstream,
or artifact set. It applies to A1, A2, and future actor classes unless a
stricter project or workspace rule exists.

This policy is artifact-neutral. It covers code, content, design, research,
operations, data, review, planning, and mixed work. Code-specific worktree rules
apply only when `work_type` is `code`.

## Required Identity For MCP Continuity Writes

Every AICOS MCP semantic write must include:

- `actor_role`: role lane, for example `A1`, `A2-Core-C`, or `A2-Core-R`
- `agent_family`: agent/client product family, for example `codex`,
  `claude-code`, `gemini-antigravity`, or `openclaw`
- `agent_instance_id`: unique session or instance id for this agent run
- `work_type`: `code`, `content`, `design`, `research`, `ops`, `review`,
  `planning`, `data`, or `mixed`
- `work_lane`: generic coordination lane

Do not put role labels into `agent_family`. For example:

- correct: `actor_role: "A1"`, `agent_family: "claude-code"`
- correct: `actor_role: "A2-Core-C"`, `agent_family: "codex"`
- wrong: `agent_family: "A1"`
- wrong: `agent_family: "a1-work"`

`actor_family` and `logical_role` are legacy optional compatibility fields. New
agents should omit them unless a task explicitly asks for them.

## Work Lane

`work_lane` is the cross-artifact coordination key.

For code, it may match a git branch:

```text
pipeline-telegram
workstream/openai-pipeline
coinglass-api
```

For non-code work, it should name the bounded lane:

```text
homepage-copy-v1
figma-dashboard-mobile
competitor-pricing-research
launch-email-campaign
ops-project-settings
```

Use `artifact_scope` and `artifact_refs` to identify the concrete artifact or
sub-scope for content, design, research, data, ops, or mixed work.

Examples:

```text
artifact_scope: "Figma dashboard mobile frames"
artifact_refs: ["figma:file/abc123#page=Dashboard"]
```

```text
artifact_scope: "Homepage launch copy, hero/pricing/FAQ"
artifact_refs: ["google-drive:doc/launch-copy"]
```

## Code Worktree Coordination

For `work_type: code`, `worktree_path` is required.

`worktree_path` is an active checkout occupancy signal, not permanent ownership.
Before editing code, read `active_task_state` from the AICOS startup bundle and
check active lanes.

Reuse an existing worktree only for:

- explicit continuation of the same `work_lane`
- completed or handoff-ready previous state
- explicit handoff
- human-approved takeover
- review
- pair-work

Create or use a separate worktree for:

- parallel implementation
- a different `work_lane`
- a different branch
- unclear dirty state
- likely overlapping file edits

This applies even when both instances have the same `agent_family`, such as two
different Codex threads.

## Non-Code Coordination

For non-code work, do not invent a code worktree requirement. Instead:

- keep `work_lane` specific and bounded;
- set `artifact_scope` to the document, design surface, research topic, ops
  lane, data slice, or review scope;
- include `artifact_refs` when a stable reference exists;
- use `coordination_status` to show whether the lane is active, paused,
  blocked, handoff-ready, or completed.

## Startup Rule

Before starting work that may overlap with other agents:

1. Read AICOS startup context.
2. Check `mcp_contract_status`.
3. Inspect `active_task_state`.
4. Choose a safe `work_lane`.
5. For code work, choose a safe `worktree_path`.
6. Write continuity through AICOS MCP when work state changes.

If `mcp_contract_status.write_schema_refresh_required` is true and the client
loaded MCP tools before a known AICOS update, refresh/list MCP tools again or
restart/re-enable the MCP server before writing. Also refresh after any write
error that returns `details.mcp_contract_status`. Do not add a mandatory schema
preflight before every ordinary write in a short session.
