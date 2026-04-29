# AICOS MCP Write Cookbook

Status: operator-facing quick payload guide  
Last updated: 2026-04-23

Use this file when an external agent already has MCP access and needs to write
back into AICOS without guessing the semantic write payload shape.

## Core Rule

Use the smallest tool that matches the intent:

- `aicos_record_checkpoint`
  - meaningful checkpoint, review point, validation point, or blocked moment
- `aicos_write_task_update`
  - progress on one concrete task/packet
- `aicos_write_handoff_update`
  - compact continuity for the next actor
- `aicos_update_status_item`
  - open item / open question / tech debt / decision follow-up lifecycle
- `aicos_register_artifact_ref`
  - artifact lives outside AICOS; store only a compact reference
- `aicos_record_feedback`
  - report MCP/context/routing/service problems back into AICOS

Do not use `handoff_update` as a substitute for open items or backlog tracking.

Before session-close writes, record one feedback closure for the same
`scope + agent_family + agent_instance_id + work_lane`.

Session-close writes are:

- `aicos_record_checkpoint` when `status=completed|blocked`
- `aicos_write_task_update` when `task_status=completed|blocked|waiting`
- `aicos_write_handoff_update` when `status=completed|blocked|ready_for_next`

If there is no real issue, use `feedback_type=no_issue` instead of inventing
friction.

## Shared Base Fields

Every write payload needs this base:

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/<project-id>",
  "actor_role": "A1",
  "agent_family": "openclaw",
  "agent_instance_id": "vm-alpha-01",
  "work_type": "ops",
  "work_lane": "telegram-pipeline",
  "execution_context": "openclaw-vm",
  "runtime_context": {
    "runtime": "private-local-aicos",
    "mcp_name": "aicos_local_private",
    "agent_position": "external_agent",
    "functional_role": "pipeline worker"
  }
}
```

If `actor_role` is `A2-Core-C` or `A2-Core-R`, also include
`runtime_identity_map`:

```json
{
  "runtime_identity_map": {
    "identity_current": {
      "runtime": "private-local-aicos",
      "mcp_name": "aicos_local_private",
      "project_scope": "projects/aicos",
      "agent_position": "internal_agent",
      "actor_role": "A2-Core-C",
      "functional_role": "AICOS maintainer"
    }
  }
}
```

If `work_type=code`, add:

```json
{
  "worktree_path": "/workspace/<project-worktree>",
  "work_branch": "feature/<branch>"
}
```

## Fastest Helper

Instead of building JSON from scratch, generate a template first:

```bash
./aicos mcp template checkpoint --scope projects/sample-project
./aicos mcp template task-update --scope projects/sample-project --work-type code --work-lane telegram-pipeline --execution-context openclaw-vm --worktree-path /workspace/sample-workspace --work-branch feature/openclaw
./aicos mcp template status-item --scope projects/aicos
```

Then fill the placeholders and pass the JSON to:

```bash
./aicos mcp write <tool> '<json-payload>'
```

## Examples

### 1. Checkpoint

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/sample-project",
  "actor_role": "A1",
  "agent_family": "openclaw",
  "agent_instance_id": "vm-alpha-01",
  "work_type": "code",
  "work_lane": "telegram-pipeline",
  "worktree_path": "/workspace/sample-workspace",
  "work_branch": "feature/openclaw",
  "execution_context": "openclaw-vm",
  "checkpoint_type": "artifact",
  "summary": "Telegram pipeline parser now handles empty update batches.",
  "status": "completed",
  "notes": "Ready for review."
}
```

### 2. Task Update

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/sample-project",
  "actor_role": "A1",
  "agent_family": "openclaw",
  "agent_instance_id": "vm-alpha-01",
  "work_type": "code",
  "work_lane": "telegram-pipeline",
  "worktree_path": "/workspace/sample-workspace",
  "work_branch": "feature/openclaw",
  "execution_context": "openclaw-vm",
  "task_ref": "telegram-pipeline-hardening",
  "task_status": "in_progress",
  "what_is_done": "Added retry guard around Telegram polling startup.",
  "next_step": "Run end-to-end pipeline test."
}
```

### 3. Handoff Update

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/aicos",
  "actor_role": "A2-Core-C",
  "agent_family": "codex",
  "agent_instance_id": "codex-thread-01",
  "work_type": "ops",
  "work_lane": "aicos-runtime-hardening",
  "execution_context": "codex-desktop",
  "summary": "Daemon health now exposes auth capabilities and supported client profiles.",
  "status": "ready_for_next",
  "next_step": "Continue with LAN security baseline and auth/audit policy."
}
```

### 4. Status Item

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/aicos",
  "actor_role": "A2-Core-C",
  "agent_family": "codex",
  "agent_instance_id": "codex-thread-01",
  "work_type": "ops",
  "work_lane": "aicos-runtime-hardening",
  "execution_context": "codex-desktop",
  "item_id": "AICOS-LAN-SECURITY-HARDENING",
  "item_type": "tech_debt",
  "item_status": "open",
  "title": "Harden LAN-facing AICOS MCP security beyond shared bearer token",
  "summary": "Labeled client tokens and audit logging are in place, but LAN policy is still light.",
  "next_step": "Decide default allowlist and minimal non-local auth policy."
}
```

### 5. Artifact Ref

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/aicos",
  "actor_role": "A2-Core-C",
  "agent_family": "codex",
  "agent_instance_id": "codex-thread-01",
  "work_type": "review",
  "work_lane": "search-eval",
  "execution_context": "codex-desktop",
  "artifact_kind": "report",
  "title": "Hybrid search evaluation notes",
  "artifact_ref": "<AICOS_PRIVATE_REPO>/reports/search-eval-20260423.md",
  "summary": "External evaluation notes comparing FTS and hybrid retrieval."
}
```

### 6. Feedback

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/aicos",
  "actor_role": "A1",
  "agent_family": "openclaw",
  "agent_instance_id": "vm-alpha-01",
  "work_type": "orientation",
  "work_lane": "intake",
  "execution_context": "openclaw-vm",
  "feedback_type": "bootstrap_confusing",
  "severity": "medium",
  "title": "Client could not infer bootstrap read identity",
  "summary": "The agent did not know what to use for work_type/work_lane during first contact."
}
```

For external IDE agents such as Antigravity:

- copy `feedback_type` exactly from the allowed list below
- if the feedback is about setup, MCP interop, or bootstrap friction after the
  first read succeeds, prefer `work_type=ops`
- keep `work_lane=intake` until a real lane is known

Example setup-friction payload for Antigravity:

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/agents-dashboard",
  "actor_role": "A1",
  "agent_family": "gemini-antigravity",
  "agent_instance_id": "vm-alpha-01",
  "work_type": "ops",
  "work_lane": "intake",
  "execution_context": "antigravity-vm",
  "feedback_type": "bootstrap_confusing",
  "severity": "medium",
  "title": "Clarify Antigravity MCP config for stdio vs HTTP SSE",
  "summary": "The IDE expects serverUrl plus headers; url/transport-shaped config can fail silently."
}
```

Useful `feedback_type` values:

- `no_issue`
- `tool_missing`
- `tool_shape_confusing`
- `tool_too_heavy`
- `bootstrap_confusing`
- `write_schema_confusing`
- `interop_problem`
- `routing_confusing`
- `context_missing`
- `work_state_missing`
- `work_state_ambiguous`
- `work_state_stale`
- `work_state_conflict`
- `ownership_unclear`

Use the work-state labels when the agent cannot quickly answer practical
coordination questions such as what is next, what is already done, who owns an
item, whether a checklist/status is stale, or which duplicate-looking item is
canonical. Do not use feedback as a workaround for updating real task/status
state.

No-issue closure example:

```json
{
  "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
  "scope": "projects/aicos",
  "actor_role": "A1",
  "agent_family": "codex",
  "agent_instance_id": "thread-aicos-pub",
  "work_type": "orientation",
  "work_lane": "intake",
  "execution_context": "codex-desktop",
  "feedback_type": "no_issue",
  "severity": "low",
  "title": "No significant friction",
  "summary": "Bootstrap/read/write flow was clear enough for this pass."
}
```

## Minimal Heuristics

Use these defaults unless the real value is already known:

- first read: `work_type=orientation`, `work_lane=intake`
- non-code operational maintenance: `work_type=ops`
- architecture/review pass: `work_type=review` or `planning`
- code work: `work_type=code` and always include `worktree_path`

## Common Mistakes

1. Using `handoff_update` to create backlog items  
Use `aicos_update_status_item` instead.

2. Omitting `worktree_path` for code work  
This is required so parallel agents do not overlap the same checkout silently.

3. Guessing a very specific lane too early  
For first contact, use `orientation/intake`, then switch to the real lane later.

4. Writing raw markdown/file path payloads  
The MCP write layer is semantic, not a raw file editor.
