# ARC-26291 — AICOS MCP Expansion Architecture For Scalable Multi-Project Work

**Status:** architecture-brief-v1  
**Project:** AICOS  
**Date:** 2026-04-19  
**Primary scope:** MCP expansion after current Phase 1/2  
**Purpose:** hướng dẫn Codex triển khai mở rộng MCP theo hướng:
- scalable
- modular
- project-neutral
- local-first but online-ready
- useful for many project types, not only sample project and not only coding projects

---

## 1. Executive Summary

AICOS hiện đã có:

### Read surface
- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_packet_index`
- `aicos_get_task_packet`

### Write surface
- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

Bộ này đủ để A1 làm việc thật ở mức cơ bản, nhưng chưa đủ mượt cho:
- query context linh hoạt
- ghi working signals có cấu trúc hơn
- đăng ký artifact refs
- manager insight / learning loop
- điều hướng dự án khi có nhiều workstreams

### Recommended next surfaces

#### Implement soon
1. `aicos_query_project_context`
2. `aicos_upsert_working_item`
3. `aicos_register_artifact_ref`

#### Design now, optional early implementation
4. `aicos_get_current_direction`
5. `aicos_get_workstream_index`

#### Design now, implement later
6. `aicos_get_feedback_digest`
7. `aicos_get_project_health`

---

## 2. Core Design Principles

### 2.1. Project-neutral
Contracts must not assume:
- crypto only
- coding only
- markdown-heavy only

They should work for:
- coding projects
- research projects
- document-heavy projects
- operations projects
- mixed workflow projects

### 2.2. Scope-first
Every MCP operation should anchor around:

```yaml
scope: "projects/<project-id>"
```

Optional context may add:
- `workstream_id`
- `task_ref`
- `artifact_kind`
- `item_type`

### 2.3. Semantic, not file-like
Do not implement MCP as:
- remote file browser
- file append bridge
- raw markdown dump pipe

Implement:
- semantic query
- structured write/update
- artifact registration
- manager digests

### 2.4. Modular operations layer
Keep transport separate from logic:
- contracts
- operations/services
- local stdio adapter
- later online transport adapter

### 2.5. Family-neutral
The same MCP surface should make sense for:
- Codex
- Claude
- OpenClaw
- future runtimes

### 2.6. Token-efficient
Bundles, queries, and writes should:
- reduce broad raw reading
- reduce repeated wandering
- keep payloads small
- still preserve enough context for correct action

---

## 3. Implement Soon

## 3.1. `aicos_query_project_context`

### Purpose
Flexible bounded query primitive for project context when startup bundle + packet bundle are not enough.

### Why it matters
Without it, agents tend to:
- broad-read files
- guess from partial context
- drift back to raw repo navigation

### Recommended inputs
```yaml
scope: "projects/<project-id>"                # required
query: "<natural language or compact query>"  # required
actor: "A1 | A2-Core-C | A2-Core-R"           # optional
workstream_id: "<optional>"
context_kinds:                                # optional
  - current_state
  - current_direction
  - handoff
  - packets
  - working_items
  - artifacts
max_results: 5                                # optional
```

### Recommended outputs
```yaml
metadata:
  schema_version: "0.1"
  kind: "aicos.mcp.query_result"
  query_id: "<generated>"
  served_at: "<utc-iso-time>"
  scope: "projects/<project-id>"
  query: "<echoed>"
results:
  - rank: 1
    kind: "working_state|handoff|packet|working_item|artifact"
    ref: "<path or id>"
    title: "<short>"
    summary: "<compact answer-bearing summary>"
```

### Rules
- bounded, ranked, useful
- no giant file dump
- no raw file bodies by default

---

## 3.2. `aicos_upsert_working_item`

### Purpose
Create or update a structured working item.

### Why it matters
Current write tools capture:
- checkpoint
- task continuity
- handoff continuity

But A1 still needs a structured way to register:
- open questions
- open items
- active risks

Without this, those signals leak into:
- free-form notes
- handoff noise
- task update overload

### Recommended item types
Start with:
- `open_question`
- `open_item`
- `active_risk`

Optional later:
- `assumption`
- `candidate_decision`
- `dependency`

### Recommended inputs
```yaml
scope: "projects/<project-id>"          # required
item_type: "open_question|open_item|active_risk"  # required
title: "<short>"                        # required
summary: "<compact>"                    # required
status: "open|in_progress|resolved|deferred"  # required
severity: "low|medium|high"             # optional
workstream_id: "<optional>"
task_ref: "<optional>"
startup_bundle_ref: "<optional>"
packet_ref: "<optional>"
handoff_ref: "<optional>"
artifact_refs: ["<optional>"]
client_request_id: "<optional>"
```

### Recommended outputs
```yaml
metadata:
  kind: "aicos.mcp.write_result"
  tool: "aicos_upsert_working_item"
  write_id: "<generated-or-client-id>"
  written_at: "<utc-iso-time>"
  scope: "projects/<project-id>"
status: "success"
normalized_summary: "<compact summary>"
item_ref: "<working-item-id-or-path>"
```

### Rules
- server owns lane mapping
- payload stays structured and small
- no long markdown body as the main write form

---

## 3.3. `aicos_register_artifact_ref`

### Purpose
Register a bounded artifact reference relevant to project continuity.

### Why it matters
A1 often produces:
- validation note
- diff note
- comparison result
- result artifact in another repo

Those should be registered without:
- pasting the whole artifact body into MCP
- bloating checkpoint notes
- requiring raw file edits into AICOS

### Recommended inputs
```yaml
scope: "projects/<project-id>"          # required
artifact_kind: "note|report|diff|output|analysis|contract_check|other"  # required
title: "<short>"                        # required
artifact_ref: "<path/url/id>"           # required
summary: "<compact relevance summary>"  # required
task_ref: "<optional>"
workstream_id: "<optional>"
startup_bundle_ref: "<optional>"
packet_ref: "<optional>"
handoff_ref: "<optional>"
client_request_id: "<optional>"
```

### Recommended outputs
```yaml
metadata:
  kind: "aicos.mcp.write_result"
  tool: "aicos_register_artifact_ref"
  write_id: "<generated-or-client-id>"
  written_at: "<utc-iso-time>"
  scope: "projects/<project-id>"
status: "success"
normalized_summary: "<compact summary>"
artifact_registry_ref: "<id-or-path>"
```

### Rules
- artifact body is not the payload
- MCP stores ref + compact meaning
- full artifact remains in its natural home

---

## 4. Should We Also Design `aicos_get_current_direction` And `aicos_get_workstream_index`?

## Short answer
Long-term: yes, both are useful.
Immediate next step: design now, implement only if cheap.

They are not exact duplicates of current tools.

---

## 4.1. `aicos_get_current_direction`

### Why it is useful
Agents often need the current project direction without:
- re-reading startup bundle
- inferring from handoff + current state
- broad reading raw project notes

### Is it duplicated already?
Not exactly.

- `aicos_get_startup_bundle` may include a digest of direction
- but startup bundle is broader and actor-oriented
- `aicos_get_current_direction` would be a focused read primitive

### Recommendation
Design now.
Implement if low effort after the 3 core tools above.

---

## 4.2. `aicos_get_workstream_index`

### Why it is useful
As projects grow, agents need to know:
- what workstreams exist
- what each workstream is for
- which packets or surfaces attach to each workstream
- what the hot path is for current work

### Is it duplicated already?
Not exactly.

- `aicos_get_packet_index` is execution-facing
- `aicos_get_workstream_index` should be routing/context-facing

### Recommendation
Design now.
Implement if workstream complexity is already real enough.

---

## 5. `aicos_get_feedback_digest` vs `aicos_get_project_health`

These should remain separate, not merged.

## 5.1. `aicos_get_feedback_digest`

### Purpose
Summarize what A1/A2 workers have been telling the system.

### Questions it answers
- what context gaps keep appearing?
- what workstreams generate repeated confusion?
- which packets produce blockers most often?
- what working items cluster over time?
- what artifacts keep showing up as relevant?

### Nature
This is a learning / synthesis tool.

### Recommended timing
Implement after the 3 core tools above.

---

## 5.2. `aicos_get_project_health`

### Purpose
Summarize whether the project context/control-plane is operationally healthy.

### Questions it answers
- is startup path stale?
- are handoff/current surfaces fresh enough?
- are too many fallback raw-file reads occurring?
- are working items accumulating without resolution?
- is MCP adoption actually happening?
- are continuity writes present and healthy?

### Nature
This is an ops / governance tool.

### Recommended timing
Implement after `feedback_digest`, unless operations pain becomes urgent earlier.

---

## 5.3. Long-term: both or one?

### Long-term answer
Do both.

Because they solve different manager questions:
- `feedback_digest` = what are agents teaching us?
- `project_health` = how healthy is the context/control plane?

### If forced to choose one first
Implement `aicos_get_feedback_digest` first.

---

## 6. Why This Design Is Scalable

### 6.1. Not sample project-specific
All tools are anchored by:
- `scope`
- optional `workstream_id`
- optional `task_ref`

Nothing assumes crypto or coding only.

### 6.2. Modular
These tools can be grouped into modules like:
- `mcp_query_context.py`
- `mcp_working_items.py`
- `mcp_artifact_registry.py`
- `mcp_manager_insights.py`

### 6.3. Online-ready
Inputs/outputs remain:
- structured
- serializable
- small
- explicit

So the same operations layer can later sit behind:
- local `stdio`
- local daemon
- online transport

### 6.4. Family-neutral
Codex, Claude, OpenClaw, and future runtimes can all call the same surface.

---

## 7. Recommended Implementation Order

### Tier 1 — implement now
1. `aicos_query_project_context`
2. `aicos_upsert_working_item`
3. `aicos_register_artifact_ref`

### Tier 2 — design now, implement if cheap
4. `aicos_get_current_direction`
5. `aicos_get_workstream_index`

### Tier 3 — manager surfaces later
6. `aicos_get_feedback_digest`
7. `aicos_get_project_health`

---

## 8. Recommended Repo Shape

Possible layout:

```text
packages/aicos-kernel/contracts/mcp-bridge/
  local-mcp-bridge-contract.md
  phase3-query-and-working-items.md
  manager-insight-surfaces.md

packages/aicos-kernel/aicos_kernel/
  mcp_query_context.py
  mcp_working_items.py
  mcp_artifact_registry.py
  mcp_manager_insights.py

integrations/local-mcp-bridge/
  aicos_mcp_stdio.py
```

### Rule
Keep contracts and implementation separate.
Keep transport adapter thin.

---

## 9. Recommended Review Questions For Codex

### Checklist Code: ARC-26292

- [ ] Is the tool truly project-neutral?
- [ ] Is the payload small and structured?
- [ ] Does the tool avoid becoming a file-edit proxy?
- [ ] Does the tool help A1 work more smoothly?
- [ ] Does the tool help A2 learn from A1 outputs over time?
- [ ] Is the tool still useful beyond sample project?
- [ ] Does the logic belong in MCP, or is it actually A2-only maintenance work?
- [ ] Is the implementation modular enough for future online transport?

---

## 10. Final Recommendation

For the next MCP expansion pass, Codex should implement:

1. `aicos_query_project_context`
2. `aicos_upsert_working_item`
3. `aicos_register_artifact_ref`

And also design, but not necessarily implement immediately:

4. `aicos_get_current_direction`
5. `aicos_get_workstream_index`

And keep as next-layer manager surfaces:

6. `aicos_get_feedback_digest`
7. `aicos_get_project_health`

### Final rule
Do not turn MCP into a giant universal file API.

Build it as:
- compact context serving
- structured continuity writing
- artifact registration
- and eventually manager insight surfaces

This is the most scalable path for AICOS across many projects and many agent families.

---
