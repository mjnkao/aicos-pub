# ARC-26284 — AICOS MCP Phase 2 Write Tool Architecture

**Status:** architecture-brief-v1
**Project:** AICOS
**Date:** 2026-04-19
**Primary scope:** AICOS MCP writeback design
**Depends on:** local-first MCP architecture, A1 MCP-first context policy
**Purpose:** thiết kế phần **write tool** cho AICOS MCP để A1 có thể ghi context/control-plane updates về AICOS một cách:

- an toàn
- có kiểm soát
- ít token
- ít ambiguity
- phù hợp local-first
- online-ready về sau
- không biến MCP thành file-edit proxy thô

---

## 1. Executive Summary

File kiến trúc Phase 1 read-serving là cần thiết nhưng **chưa đủ** để A1 làm việc hoàn chỉnh qua MCP.

Muốn A1 thực sự dùng MCP cho vòng đời context/control-plane, AICOS phải có **write tools** cho:

- checkpoint
- task continuity update
- handoff continuity update

### Core principle

Write tools của AICOS MCP phải là:

- **structured**
- **small-payload**
- **lane-aware**
- **validation-first**
- **traceable**
- **idempotency-friendly where possible**

### Important rule

Do **not** implement MCP writeback as:
- “remote file edit”
- “raw append text anywhere”
- “free-form mutate any path”

Instead, write tools must:
- accept bounded structured payloads
- map them into approved AICOS lanes
- validate minimum context refs
- record enough trace to support continuity review

---

## 2. Why A Phase 2 Write Architecture Is Needed

Phase 1 read-serving solves:
- startup bundle retrieval
- packet retrieval
- handoff/current read
- reduced broad cross-folder reads

But without write tools:
- A1 still needs raw file writes into AICOS
- checkpoint/handoff discipline still depends on broad permissions
- stale or ad hoc writeback can bypass structure
- cross-family usage (Codex / Claude / OpenClaw) remains less portable

Therefore:
- read-only MCP is not enough for A1 lifecycle
- write tools are required for real A1 MCP-first operation

---

## 3. Design Goals

## 3.1. Small structured payloads
A1 should send small write payloads, not large prose blobs.

## 3.2. Lane-aware mapping
The server should decide where and how the update lands in AICOS.

## 3.3. Validation before write
The server should validate:
- scope/project id
- allowed write type
- minimum refs
- minimally coherent status fields

## 3.4. Traceability
Every accepted write should preserve:
- actor
- scope
- packet or task ref if relevant
- startup/packet/handoff refs if relevant
- timestamp
- write type

## 3.5. Local-first now, online-ready later
Write semantics should survive transport changes.

## 3.6. Multi-family neutral
Codex / Claude / OpenClaw should be able to call the same write tools.

---

## 4. Non-Goals

This phase should not:
- implement broad free-form text editing over MCP
- expose arbitrary path writes
- become a full workflow engine
- introduce event-bus level complexity
- solve merge conflicts for all future cases
- build auth/session systems now
- replace A2 direct maintenance behavior

---

## 5. Recommended Write Tool Set

### Report Code: ARC-26285

Phase 2 should begin with exactly these 3 write tools:

1. `aicos_record_checkpoint`
2. `aicos_write_task_update`
3. `aicos_write_handoff_update`

### Why only these 3
They correspond to the minimum continuity loop needed by A1.

Do not add more until these are proven useful.

---

## 6. Tool 1 — `aicos_record_checkpoint`

### Purpose
Record a meaningful checkpoint event for bounded A1 work.

### Recommended use cases
- bounded validation task completed
- artifact-producing task completed
- review task reached a meaningful checkpoint
- task blocked after concrete inspection

### Intended target lanes
Typically one of:
- project evidence/import-notes
- project working handoff/current (as a short checkpoint update)
- project-scoped checkpoint note location if such a lane exists

### Input payload shape (conceptual)
```json
{
  "scope": "projects/<project-id>",
  "actor_family": "a1-work-agents",
  "logical_role": "a1-work",
  "work_context": "<workstream or route>",
  "checkpoint_type": "review|validation|artifact|blocked|continuation",
  "summary": "<short bounded summary>",
  "status": "completed|blocked|partial",
  "startup_bundle_ref": "<optional>",
  "packet_ref": "<optional>",
  "handoff_ref": "<optional>",
  "artifact_refs": ["<optional file/path refs>"],
  "notes": "<optional short note>"
}
```

### Validation requirements
Must validate:
- `scope` exists and is recognized
- `checkpoint_type` is allowed
- `summary` is short and non-empty
- payload is not trying to perform broad text dump
- destination lane is valid for this write type

### Output shape
Should return:
- success/failure
- written target path(s)
- timestamp
- checkpoint id or write id
- any normalized refs added by the server

---

## 7. Tool 2 — `aicos_write_task_update`

### Purpose
Write or update task continuity state for bounded A1 task execution.

### Recommended use cases
- task now in progress
- task completed
- task blocked
- next step identified
- packet/task state refined after actual work

### Intended target lanes
Typically:
- project task-state or task continuity note
- project open-items/open-questions if the update implies one
- packet-related project state support lane

### Input payload shape (conceptual)
```json
{
  "scope": "projects/<project-id>",
  "task_ref": "<task id or packet ref>",
  "actor_family": "a1-work-agents",
  "logical_role": "a1-work",
  "work_context": "<route/workstream/session context>",
  "task_status": "planned|in_progress|completed|blocked|waiting",
  "what_is_done": "<short>",
  "what_is_blocked": "<short optional>",
  "next_step": "<short optional>",
  "startup_bundle_ref": "<optional>",
  "packet_ref": "<optional>",
  "handoff_ref": "<optional>",
  "artifact_refs": ["<optional>"]
}
```

### Validation requirements
Must validate:
- `task_ref` exists or is recognizable
- `task_status` is allowed
- `what_is_done` present when status implies progress/completion
- `next_step` present when helpful/required
- target lane is valid
- no attempt to dump huge task history

### Output shape
Should return:
- success/failure
- target file(s) updated
- normalized task state summary
- write id / timestamp

---

## 8. Tool 3 — `aicos_write_handoff_update`

### Purpose
Write a compact project handoff/current continuity update when a meaningful new state has been reached.

### Recommended use cases
- new current checkpoint affects the next actor
- current next step changed materially
- project working reality changed enough to update H1 current

### Important rule
This tool is **not** for dumping long history.
It should only write compact current-state/handoff relevant updates.

### Intended target lanes
Typically:
- `brain/projects/<project-id>/working/handoff/current.md`
- or project-specific handoff/current equivalent

### Input payload shape (conceptual)
```json
{
  "scope": "projects/<project-id>",
  "actor_family": "a1-work-agents",
  "logical_role": "a1-work",
  "work_context": "<optional>",
  "summary": "<short current continuity update>",
  "status": "completed|blocked|partial|ready_for_next",
  "next_step": "<short>",
  "startup_bundle_ref": "<optional>",
  "packet_ref": "<optional>",
  "artifact_refs": ["<optional>"],
  "notes": "<optional short note>"
}
```

### Validation requirements
Must validate:
- summary is short and current-focused
- next step is meaningful
- update is not trying to replace entire handoff file blindly
- handoff lane exists and is allowed
- payload is continuity-oriented, not essay-like

### Output shape
Should return:
- success/failure
- target path updated
- resulting handoff update id/timestamp
- possibly a short normalized confirmation

---

## 9. Why Not Raw File Write Tools

AICOS should not begin with tools like:
- `aicos_write_file`
- `aicos_append_text`
- `aicos_edit_any_path`

### Reason
Those tools:
- reintroduce ambiguity
- bypass lane semantics
- encourage stale/manual habits
- weaken validation
- make review harder
- are harder to keep safe across clients

### Rule
Prefer semantic write tools over generic file mutation tools.

---

## 10. Payload Design Rules

## 10.1. Short fields only
Payload fields should prefer:
- short bounded text
- enumerated statuses
- refs
- structured arrays

Avoid:
- large narratives
- full markdown documents in payload
- pasted raw history

## 10.2. Explicit refs preferred
Payload should include refs when possible:
- startup bundle ref
- packet ref
- handoff ref
- artifact refs

## 10.3. Server owns formatting
Client should provide:
- small structured intent

Server should own:
- lane mapping
- final write format
- minimal normalization

### Rule
Clients express intent.
Server formats authoritative writeback.

---

## 11. Validation Model

## 11.1. Pre-write validation
Before write, validate:
- scope/project exists
- write type allowed
- required fields present
- refs structurally valid if provided
- target lane known

## 11.2. Write-shape validation
Validate that:
- payload is bounded
- text length is reasonable
- write type matches lane type
- no broad history dump is attempted

## 11.3. Post-write confirmation
After write, return:
- exact target path(s)
- what was written in normalized summary form
- write id / timestamp

---

## 12. Idempotency And Duplicate Handling

Write tools do not need perfect distributed-systems idempotency right now, but should be **idempotency-friendly**.

### Recommended minimum
- allow optional client-generated request id
- include timestamp/write id in response
- avoid duplicate broad append behavior where possible
- prefer replace/update by structured slot when meaningful

### Rule
Do not overengineer now, but avoid obvious duplicate-spam patterns.

---

## 13. Lane Mapping Strategy

The server should own lane mapping.

### Example
- checkpoint write -> evidence/import-notes or checkpoint lane
- task update -> task continuity or working support lane
- handoff update -> working/handoff/current

### Important
Do not require A1 to understand raw path architecture deeply.

### Rule
A1 should provide:
- scope
- intent
- short structured payload

The server should decide:
- where it lands
- how it is formatted
- how it is normalized

---

## 14. Multi-Family Compatibility

Write tools must remain usable across:
- Codex
- Claude
- OpenClaw
- future runtimes

### Therefore
Avoid payload designs that assume:
- one client’s special metadata style
- one client’s hidden memory model
- one client’s proprietary file semantics

### Rule
Use family-neutral structured payloads.

---

## 15. Performance And Token Strategy

## 15.1. Keep writes small
Write tools should accept small payloads.

## 15.2. Do not echo giant files back
Responses should confirm:
- success
- target path
- normalized summary
- ids/refs

Not:
- full file contents by default

## 15.3. Minimize round trips
A checkpoint/write should ideally be one tool call, not multiple dependent steps.

### Rule
Write tools should be concise and low-token.

---

## 16. Relationship To A1 Policy

This phase operationalizes the A1 MCP-first context policy.

That policy says:
- A1 must use MCP for AICOS-facing context/control-plane operations

This write-tool phase provides the missing write side of that loop.

### After Phase 2 is complete
A1 can:
- read startup/handoff/packet through MCP
- write checkpoint/task/handoff through MCP
- keep local repo work direct

That is the intended steady-state architecture.

---

## 17. Online-Ready Considerations

To remain online-ready later:

## 17.1. Keep operations layer transport-neutral
Write logic should not depend heavily on local-only assumptions.

## 17.2. Keep payloads serializable and explicit
Do not rely on implicit host state.

## 17.3. Keep validation logic server-side
So later transport changes do not break semantics.

### Rule
Transport can change later.
Write semantics should not.

---

## 18. Recommended Implementation Sequence

## 18.1. Phase 2A — contract first
Define concrete contract/spec for:
- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

## 18.2. Phase 2B — operations layer
Implement minimal server-side logic for:
- validation
- lane mapping
- formatting
- write confirmation

## 18.3. Phase 2C — local integration
Expose local transport surface for these tools.

## 18.4. Phase 2D — one bounded usage test
After implementation, run one small A1 usage test for each write type or one combined bounded continuity test.

---

## 19. Recommended Review Questions

### Checklist Code: ARC-26286

- [ ] Are write tools semantic rather than raw file mutation tools?
- [ ] Are payloads small and structured?
- [ ] Does the server own lane mapping?
- [ ] Are required refs/fields clear enough for traceability?
- [ ] Are validation rules strong enough to prevent sloppy writeback?
- [ ] Are responses concise and useful?
- [ ] Is the design still local-first but online-ready?
- [ ] Is the surface family-neutral?

---

## 20. Final Recommendation

### Final recommendation

Phase 2 should implement exactly three semantic write tools first:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

These tools should:

- accept small structured payloads
- validate before write
- map into approved AICOS lanes
- preserve trace metadata
- remain family-neutral
- keep responses concise
- avoid raw file-edit semantics

### Final rule
Do not design writeback as “agent edits AICOS files through MCP.”
Design writeback as:

### **agent sends structured continuity intent; AICOS MCP validates, maps, formats, and records authoritative continuity.**

---
