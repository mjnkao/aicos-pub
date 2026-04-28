# AICOS Local MCP Bridge Contract

Status: Phase 3 lightweight query/artifact surfaces implemented

## Purpose

Support cross-repo project work where:

- AICOS repo is context/control-plane authority.
- External project repo is code/runtime authority.
- Workers use a local stdio MCP bridge instead of merging repos or relying on
  raw cross-folder edits as the main integration model.

## Phase 1 Tool Surface

Phase 1 is read-serving only. It is primarily for A1-facing AICOS
context/control-plane access.

| Tool | Purpose |
| --- | --- |
| `aicos_get_startup_bundle` | Return compact startup bundle for role + project scope |
| `aicos_get_handoff_current` | Return H1 current handoff for a project |
| `aicos_get_packet_index` | Return compact task packet index |
| `aicos_get_task_packet` | Return one task packet |
| `aicos_get_status_items` | Return filtered structured status items |
| `aicos_get_workstream_index` | Return project-declared workstream routing map when present |
| `aicos_get_context_registry` | Return metadata registry entries for project/shared context sources |
| `aicos_get_project_registry` | Return shared known-project registry and authority boundaries |
| `aicos_get_feedback_digest` | Return recent context-serving feedback signals |
| `aicos_get_project_health` | Return compact operational/control-plane health view |
| `aicos_query_project_context` | Return bounded keyword/metadata query results over hot context |

## Phase 1 Inputs

All Phase 1 read tools must now include these minimum audit-correlation
fields:

```yaml
agent_family: "<required, e.g. codex|claude-code|openclaw>"
agent_instance_id: "<required per-thread/per-worker id>"
work_type: "<required current work type; use orientation for first-contact/bootstrap reads>"
work_lane: "<required current lane; use intake for first-contact/bootstrap reads>"
execution_context: "<required, e.g. codex-desktop|claude-desktop|vm|cli>"
worktree_path: "<required when work_type=code>"
work_branch: "<recommended when work_type=code>"
```

These fields do not change read semantics, but the daemon now rejects read
requests that omit the minimum identity set. This keeps read-side audit trails
usable in multi-agent, multi-machine operation.

When an agent is connecting for the first time and does not yet know its real
lane, use this bootstrap pair:

```yaml
work_type: "orientation"
work_lane: "intake"
```

### `aicos_get_startup_bundle`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
```

### `aicos_get_handoff_current`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
```

### `aicos_get_packet_index`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
```

### `aicos_get_task_packet`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
packet_id: "<packet-id-without-md>"
```

### `aicos_get_status_items`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
status_filter: ["open|resolved|closed|stale|deferred|blocked"] # optional
item_type_filter: ["open_item|open_question|tech_debt|decision_followup"] # optional
work_lane: "<optional>"
agent_family: "<optional>"
include_stale: false # optional; default hides stale/closed unless status_filter is set
max_results: 20
```

### `aicos_get_workstream_index`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
include_candidate: false
status_filter: ["active|paused|deprecated|candidate"] # optional
```

### `aicos_get_context_registry`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
project_role: "<optional project/company role>"
max_results: 200
```

### `aicos_get_project_registry`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
```

### `aicos_get_feedback_digest`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
max_results: 10
```

### `aicos_get_project_health`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
```

### `aicos_query_project_context`

```yaml
actor: "A1 | A2-Core-C | A2-Core-R"
scope: "projects/<project-id>"
query: "<short query>" # required
project_role: "<optional project/company role>"
context_kinds:
  - current_state
  - current_direction
  - handoff
  - packets
  - status_items
  - task_state
  - workstreams
  - artifacts
  - open_items
  - open_questions
  - canonical
  - policy
  - contract
  - project_registry
max_results: 5
include_stale: false # optional; default hides stale/closed status items
```

## Phase 1 Output Shape

Each successful response returns a bounded bundle object:

```yaml
metadata:
  schema_version: "0.1"
  kind: "aicos.mcp.read_bundle"
  surface: "<tool-name>"
  bundle_id: "<surface>:<short-hash>"
  served_at: "<utc-iso-time>"
  actor: "<requested actor>"
  scope: "<requested scope>"
  source_refs:
    - path: "<repo-relative-source-path>"
      role: "<source role>"
      exists: true
      mtime: "<utc-iso-time>"
  authority: "AICOS brain/agent-repo source files; MCP is access/control-plane, not truth store."
  staleness_hint: "Refresh before continuation-sensitive work or before using a copied local context."
```

Then each surface adds its own compact payload:

- startup bundle: role summary, current state/direction digest, context ladders,
  conditional handoff pointer, lightweight continuity signal, MCP contract
  status, coordination rules, active task state, recent completed task state,
  packet index, rule-card refs, not-loaded list
- handoff current: H1 current handoff content and boundary statement
- packet index: packet ids, paths, titles, and summaries
- task packet: one selected packet content plus loading rule
- status items: filtered compact status item entries
- workstream index: project-declared or project-accepted lane map only
- context registry: source metadata including context kind, state, authority,
  role tags, refs, and compact summaries
- project registry: known project entries and authority boundaries
- feedback digest: structured service-improvement feedback signals
- project health: active status/task/feedback counts and compact refs
- query project context: ranked refs and compact snippets, not full source
  bodies

`aicos_query_project_context` can also include selected non-working surfaces
when requested through `context_kinds`:

- `canonical`: `brain/projects/<project-id>/canonical/**/*.md`
- `policy`: `brain/shared/policies/**/*.md`
- `contract`: `packages/aicos-kernel/contracts/**/*.md`

Status-item reads and project-context query hide `stale` and `closed` status
items by default. Set `include_stale: true` or an explicit `status_filter` for
audit/recovery work.

Startup bundles include `continuity_signal`, a compact latest handoff signal.
An empty `active_task_state` does not mean a project is idle; agents should
check `continuity_signal` and `active_status_items` before concluding there is
no active work.

Startup bundle also includes:

```yaml
mcp_contract_status:
  schema_version: "0.6"
  minimum_write_contract: "mcp-v0.6-write-contract-ack"
  coordination_policy_version: "2026-04-21.agent-coordination-v1"
  write_schema_refresh_required: true
  write_schema_refresh_recommended: false
  write_contract_ack_required: true
  write_contract_ack_field: "mcp_contract_ack"
  write_contract_ack_value: "mcp-v0.6-write-contract-ack"
  required_write_fields:
    - mcp_contract_ack
    - actor_role
    - agent_family
    - agent_instance_id
    - work_type
    - work_lane
    - runtime_context
  conditional_required_fields:
    worktree_path: "required when work_type is code"
    runtime_identity_map: "required when actor_role begins with A2-"
  semantic_write_tools:
    - aicos_record_checkpoint
    - aicos_write_task_update
    - aicos_write_handoff_update
    - aicos_update_status_item
    - aicos_register_artifact_ref
  semantic_read_tools:
    - aicos_get_startup_bundle
    - aicos_get_handoff_current
    - aicos_get_packet_index
    - aicos_get_task_packet
    - aicos_get_status_items
    - aicos_get_workstream_index
    - aicos_get_context_registry
    - aicos_get_project_registry
    - aicos_get_feedback_digest
    - aicos_get_project_health
    - aicos_query_project_context
  refresh_instruction: "If your client cached MCP tool schemas, call tools/list again or restart/re-enable the AICOS MCP server before writing."
```

If `write_schema_refresh_required` is true and the agent loaded MCP tools
before the current session or before a known AICOS update, it should refresh
`tools/list` or restart/re-enable the MCP server before writing. Agents do not
need to refresh before every write during a normal short session.

All Phase 2 write tools require:

```yaml
mcp_contract_ack: "mcp-v0.6-write-contract-ack"
```

This field is intentionally required so stale clients using cached old write
schemas fail before writing to the wrong lane. If the server rejects a write
with `write_contract_ack_required`, refresh `tools/list` or restart/re-enable
the AICOS MCP server, then retry with the current schema.

## Failure Behavior

Errors are structured:

```yaml
error:
  code: "unsupported_actor | unsupported_scope | missing_task_packet | ..."
  message: "human-readable summary"
  details: {}
```

The local stdio adapter returns MCP-style `isError: true` tool results for
domain errors.

## Phase 1 Source Mapping

- project truth: `brain/projects/<project-id>/`
- actor startup/rules/packets: `agent-repo/classes/...`
- shared policies/templates: `brain/shared/...`
- MCP operations layer:
  `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
- local stdio adapter:
  `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

## Deferred Writeback Surface

Phase 2 implements a small semantic write surface:

| Tool | Purpose | Target lane |
| --- | --- |
| `aicos_record_checkpoint` | Record a meaningful checkpoint event | `brain/projects/<project-id>/evidence/checkpoints/` |
| `aicos_write_task_update` | Write/update task continuity info | `brain/projects/<project-id>/working/task-state/` |
| `aicos_write_handoff_update` | Write/update handoff continuity info | `brain/projects/<project-id>/working/handoff/current.md` |
| `aicos_update_status_item` | Upsert status for open items, open questions, tech debt, or decision follow-ups | `brain/projects/<project-id>/working/status-items/` |
| `aicos_register_artifact_ref` | Register compact artifact refs without copying artifact bodies | `brain/projects/<project-id>/working/artifact-refs/` |
| `aicos_record_feedback` | Record context-serving/rule/routing feedback signals | `brain/projects/<project-id>/working/feedback/` |

Optional later:

- `aicos_get_current_direction`
- `aicos_get_open_questions`
- `aicos_generate_startup_cache`
- `aicos_record_framework_feedback`
- `aicos_get_feedback_digest`
- `aicos_get_project_health`

## Phase 2 Inputs

### `aicos_record_checkpoint`

```yaml
scope: "projects/<project-id>"              # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required, role lane doing the work
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
agent_display_name: "<human readable label>" # optional
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
runtime_context:                            # required for every write
  runtime: "<runtime receiving this MCP call>"
  mcp_name: "<client-side MCP server alias>"
  agent_position: "external_agent|internal_agent|human_operator|system"
  functional_role: "<optional task/business role>"
runtime_identity_map:                       # required for A2 writes only
  identity_current:
    runtime: "<runtime>"
    mcp_name: "<mcp alias>"
    project_scope: "projects/<project-id>"
    agent_position: "external_agent|internal_agent|human_operator|system"
    actor_role: "A1|A2-Core-C|A2-Core-R"
    functional_role: "<task/business role>"
coordination_status: "active|paused|blocked|handoff_ready|completed" # optional, default active
artifact_scope: "<artifact or sub-scope being worked on>" # optional but recommended
work_branch: "<git branch>"                  # optional, code-specific
worktree_path: "<local checkout/worktree path>" # required when work_type is code
execution_context: "<client/workstation/context>" # optional
checkpoint_type: "review|validation|artifact|blocked|continuation" # required
summary: "<short bounded summary>"          # required, max 500 chars
status: "completed|blocked|partial"         # required
actor_family: "<legacy optional; omit unless asked>" # optional
logical_role: "<legacy optional; omit unless asked>" # optional
work_context: "<workstream/session>"        # optional
client_request_id: "<idempotency-friendly id>" # optional
startup_bundle_ref: "<bundle id/ref>"       # optional
packet_ref: "<packet id/path/bundle>"       # optional
handoff_ref: "<handoff id/path/bundle>"     # optional
artifact_refs: ["<artifact/ref>"]           # optional
notes: "<short note>"                       # optional, max 1000 chars
```

### `aicos_write_task_update`

```yaml
scope: "projects/<project-id>"              # required
task_ref: "<task id or packet ref>"         # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required, role lane doing the work
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
agent_display_name: "<human readable label>" # optional
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
coordination_status: "active|paused|blocked|handoff_ready|completed" # optional, default active
artifact_scope: "<artifact or sub-scope being worked on>" # optional but recommended
work_branch: "<git branch>"                  # optional, code-specific
worktree_path: "<local checkout/worktree path>" # required when work_type is code
execution_context: "<client/workstation/context>" # optional
task_status: "planned|in_progress|completed|blocked|waiting" # required
what_is_done: "<short done/progress summary>" # required
actor_family: "<legacy optional; omit unless asked>" # optional
logical_role: "<legacy optional; omit unless asked>" # optional
work_context: "<workstream/session>"        # optional
what_is_blocked: "<short blocker>"          # optional
next_step: "<short next step>"              # optional
client_request_id: "<idempotency-friendly id>" # optional
startup_bundle_ref: "<bundle id/ref>"       # optional
packet_ref: "<packet id/path/bundle>"       # optional
handoff_ref: "<handoff id/path/bundle>"     # optional
artifact_refs: ["<artifact/ref>"]           # optional
```

### `aicos_write_handoff_update`

Use only for compact current continuity that a future actor needs to continue
from the handoff. Do not use this tool to create, update, close, defer, or list
open items, open questions, tech debt, decision follow-ups, or backlog-like
items. If a client cannot see `aicos_update_status_item`, it is using a stale or
incomplete MCP tool schema; refresh `tools/list` or restart/re-enable the AICOS
MCP server instead of using handoff as a substitute.

```yaml
scope: "projects/<project-id>"              # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required, role lane doing the work
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
agent_display_name: "<human readable label>" # optional
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
coordination_status: "active|paused|blocked|handoff_ready|completed" # optional, default active
artifact_scope: "<artifact or sub-scope being worked on>" # optional but recommended
work_branch: "<git branch>"                  # optional, code-specific
worktree_path: "<local checkout/worktree path>" # required when work_type is code
execution_context: "<client/workstation/context>" # optional
summary: "<compact current continuity update, not a status item list>" # required
status: "completed|blocked|partial|ready_for_next" # required
next_step: "<meaningful continuation step>" # required
actor_family: "<legacy optional; omit unless asked>" # optional
logical_role: "<legacy optional; omit unless asked>" # optional
work_context: "<workstream/session>"        # optional
client_request_id: "<idempotency-friendly id>" # optional
startup_bundle_ref: "<bundle id/ref>"       # optional
packet_ref: "<packet id/path/bundle>"       # optional
artifact_refs: ["<artifact/ref>"]           # optional
notes: "<short handoff note, not detailed status-item bodies>" # optional, max 1000 chars
```

### `aicos_update_status_item`

```yaml
scope: "projects/<project-id>"              # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required, role lane doing the work
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
agent_display_name: "<human readable label>" # optional
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
coordination_status: "active|paused|blocked|handoff_ready|completed" # optional, default active
artifact_scope: "<artifact or sub-scope being worked on>" # optional but recommended
work_branch: "<git branch>"                  # optional, code-specific
worktree_path: "<local checkout/worktree path>" # required when work_type is code
execution_context: "<client/workstation/context>" # optional
item_id: "<stable project-local id/key>"     # required
item_type: "open_item|open_question|tech_debt|decision_followup" # required
item_status: "open|resolved|closed|stale|deferred|blocked" # required
title: "<short title>"                       # required
summary: "<bounded current status summary>" # required
reason: "<why this status changed>"         # optional
next_step: "<remaining action or none>"     # optional
source_ref: "<handoff/open-items/doc source ref>" # optional
actor_family: "<legacy optional; omit unless asked>" # optional
logical_role: "<legacy optional; omit unless asked>" # optional
work_context: "<workstream/session>"        # optional
client_request_id: "<idempotency-friendly id>" # optional
startup_bundle_ref: "<bundle id/ref>"       # optional
packet_ref: "<packet id/path/bundle>"       # optional
handoff_ref: "<handoff id/path/bundle>"     # optional
artifact_refs: ["<artifact/ref>"]           # optional
```

Use `aicos_update_status_item` instead of appending a handoff section when the
agent needs to mark an open item, open question, tech debt, or decision
follow-up as resolved, stale, deferred, blocked, or reopened. This preserves the
handoff as continuity while giving status items stable IDs.

Status item type guide:

- `open_item`: new actionable work that is not primarily an existing
  defect/debt, unresolved question, or decision follow-up.
- `open_question`: unresolved question needing human, architecture, product, or
  project decision before the next clear action.
- `tech_debt`: known existing issue, friction, missing validation/coverage/docs,
  stale behavior, cleanup, or quality gap.
- `decision_followup`: a decision already made that needs tracking through
  implementation, rollout, verification, or cleanup.

The server returns soft `warnings` when `item_type` looks suspicious, for
example `open_item` text that appears to describe existing debt or missing
coverage/docs. The warning does not reject an otherwise valid write; agents
should correct obvious type mistakes before relying on filters.

### `aicos_register_artifact_ref`

```yaml
scope: "projects/<project-id>"              # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
artifact_kind: "note|report|diff|output|analysis|contract_check|dataset|design|content|other" # required
title: "<short title>"                       # required
artifact_ref: "<path/url/id>"                # required
summary: "<bounded relevance summary>"       # required
source_ref: "<optional source/ref>"          # optional
client_request_id: "<idempotency-friendly id>" # optional
startup_bundle_ref: "<bundle id/ref>"        # optional
packet_ref: "<packet id/path/bundle>"        # optional
handoff_ref: "<handoff id/path/bundle>"      # optional
artifact_refs: ["<related artifact/ref>"]    # optional
```

Use `aicos_register_artifact_ref` when the durable artifact belongs in another
repo, tool, document system, or output folder. AICOS stores only a compact
reference and relevance summary.

### `aicos_record_feedback`

```yaml
scope: "projects/<project-id>"              # required
mcp_contract_ack: "mcp-v0.6-write-contract-ack" # required
actor_role: "A1|A2-Core-C|A2-Core-R|..."    # required
agent_family: "codex|claude-code|gemini-antigravity|openclaw|..." # required
agent_instance_id: "<unique session/agent instance id>" # required
work_type: "code|content|design|research|ops|review|planning|data|mixed|orientation" # required
work_lane: "<generic coordination lane>"     # required
feedback_type: "no_issue|query_failed|stale_result|context_missing|context_overload|rule_confusing|tool_missing|tool_shape_confusing|tool_too_heavy|bootstrap_confusing|write_schema_confusing|interop_problem|packet_missing_ref|handoff_too_long|role_context_wrong|routing_confusing|other" # required
severity: "low|medium|high|critical"         # required
title: "<short title>"                       # required
summary: "<what failed or should improve>"   # required
observed_in: "<surface/session/task>"        # optional
recommendation: "<suggested improvement>"    # optional
source_ref: "<source/ref>"                   # optional
artifact_refs: ["<related artifact/ref>"]    # optional
```

Use feedback writes for learning/improvement signals. Do not use feedback as a
substitute for task state, handoff, status item lifecycle, or canonical policy
promotion.

Session-close writes require one feedback closure first for the same
`scope + agent_family + agent_instance_id + work_lane`.

- Required before:
  - `aicos_record_checkpoint` with `status=completed|blocked`
  - `aicos_write_task_update` with `task_status=completed|blocked|waiting`
  - `aicos_write_handoff_update` with `status=completed|blocked|ready_for_next`
- The closure may be a real issue or `feedback_type: no_issue`.
- If missing, AICOS rejects the write with `feedback_closure_required` and a
  `quick_no_issue_example`.

Read surfaces now also expose a compact `feedback_loop` object in startup bundle
and project health. This is a lightweight nudge, not a mandatory workflow. It
asks for feedback mainly on first-contact/orientation reads, repeated MCP
friction, or other low-signal situations where AICOS would otherwise learn
nothing from agent usage.

## Phase 2 Validation Rules

- `scope` must be `projects/<project-id>` and the project must exist.
- Required fields must be present and non-empty.
- Shared coordination policy:
  `brain/shared/policies/agent-coordination-policy.md`.
- All semantic write tools require actor identity:
  `actor_role`, `agent_family`, and `agent_instance_id`.
- `actor_role` is the AICOS role lane, for example `A1`, `A2-Core-C`, or
  `A2-Core-R`.
- `agent_family` is the client/agent product family, for example `codex`,
  `claude-code`, `gemini-antigravity`, or `openclaw`.
- `agent_family` must not be `A1`, `A2`, `a1-work`, or another role label.
- `actor_family` and `logical_role` are legacy optional compatibility fields.
  New agents should omit them unless a task explicitly asks for them; the MCP
  server derives legacy values from `agent_family` and `actor_role` when absent.
- All semantic write tools require a generic coordination lane:
  `work_type` and `work_lane`.
- `work_lane` is the cross-project coordination key. For code it may match a
  git branch; for content/design/research it should name the document, design,
  topic, campaign, review lane, or other bounded lane.
- Agents should include `artifact_scope` and `artifact_refs` for non-code work.
- Agents must include `worktree_path` when `work_type` is `code`.
- Agents should include `work_branch` when doing code work.
- Before starting or continuing code work, agents should read
  `active_task_state` from `aicos_get_startup_bundle` and avoid reusing another
  active agent's `worktree_path`/`work_lane` unless explicitly coordinating a
  handoff or pair-work lane.
- For the full worktree reuse/separate-worktree rule, use the shared
  coordination policy. The short rule is: reuse a code worktree only for
  explicit continuation, handoff, review, takeover, or pair-work; use a separate
  worktree for parallel implementation, different lane/branch, unclear dirty
  state, or likely overlapping file edits.
- Enum fields must use approved values.
- Text fields are intentionally short; large narratives are rejected.
- Refs must be small lists of strings.
- Raw file-edit keys are rejected:
  `path`, `target_path`, `file_path`, `content`, `markdown`, `raw_text`,
  `append_text`.
- Server owns lane mapping and final markdown formatting.
- Status-item updates are structured status upserts. They are not raw edits to
  `handoff/current.md`, `open-items.md`, or `open-questions.md`.
- Status-item writes include type guidance and may return soft warnings when
  the chosen `item_type` appears inconsistent with the item text.
- Artifact-ref writes are compact registrations. They must not paste artifact
  bodies into MCP payloads.
- Feedback writes are structured learning signals. They do not change project
  truth until reviewed and promoted through a later policy/context update.
- Query reads are bounded context discovery over AICOS hot context. In HTTP
  daemon mode they prefer PostgreSQL hybrid search with pgvector embeddings
  when available, then PostgreSQL FTS, then markdown-direct fallback. Query
  results are not canonical promotion and not a raw file browser.
- Context registry reads are metadata indexes over source files. They do not
  promote, copy, or replace source truth.

## Phase 2 Output Shape

Successful write tools return concise confirmation:

```yaml
metadata:
  schema_version: "0.1"
  kind: "aicos.mcp.write_result"
  tool: "<tool-name>"
  write_id: "<client-request-id-or-generated-id>"
  written_at: "<utc-iso-time>"
  scope: "projects/<project-id>"
  actor_role: "<role lane>"
  agent_family: "<agent/client family>"
  agent_instance_id: "<unique instance id>"
  agent_display_name: "<display label>"
  work_type: "<work type>"
  work_lane: "<generic coordination lane>"
  coordination_status: "<coordination status>"
  artifact_scope: "<artifact/sub-scope>"
  work_branch: "<branch>"
  worktree_path: "<checkout/worktree path, required for code work>"
  execution_context: "<client/workstation context>"
  actor_family: "<actor family>"
  logical_role: "<logical role>"
  work_context: "<work context>"
  task_ref: "<task ref if relevant>"
  target_paths:
    - "<repo-relative-target-path>"
  authority: "AICOS MCP validates, maps, formats, and records semantic continuity writes."
status: "success"
normalized_summary: "<surface-specific compact summary>"
```

Domain errors use the same structured error convention as Phase 1.
Write-domain errors include `details.mcp_contract_status` so stale clients can
see the active write contract and refresh/restart instruction instead of
guessing the current schema.

## Thin Writeback Payload

Legacy placeholder shape retained for old design provenance only. Do not use
this shape for new MCP writes; use the Phase 2 tool-specific inputs above.

```yaml
project_id: ""
actor_family: ""
logical_role: ""
work_context: ""
task_ref: ""
status: ""
what_is_done: ""
what_is_blocked: ""
next_step: ""
handoff_refs:
  - ""
artifact_refs:
  - ""
checkpoint_type: ""
```

## Rules

- Keep local-first and stdio-first.
- Keep operations layer transport-independent.
- Do not build remote infrastructure in MVP.
- Do not merge external project repos into AICOS.
- Do not make optional `.aicos/` cache/staging a source of truth.
- Bridge reads/writes AICOS continuity; workers execute project work in the
  external repo.
- Phase 1 reads are bundle-first, not raw file RPC.
- Phase 2 writes are semantic continuity writes, not raw file edits.
- A1 should use MCP for AICOS-facing context/control-plane reads. A2 may still
  access the repo directly when maintaining AICOS.
- Long-running agents should refresh MCP schemas before important writes when
  the startup bundle marks write schema refresh as required, the human says
  AICOS has changed, or a write error returns `mcp_contract_status`. This is a
  lightweight freshness rule, not a mandatory preflight before every write.
