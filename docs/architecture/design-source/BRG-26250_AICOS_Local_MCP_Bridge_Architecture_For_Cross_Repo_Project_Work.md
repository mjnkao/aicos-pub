# BRG-26250 — AICOS Local MCP Bridge Architecture For Cross-Repo Project Work

**Status:** working-architecture-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** mô tả chi tiết mô hình local MCP cho AICOS để giải quyết bài toán:
- project thật sống ở repo khác, folder khác
- worker (Codex / Claude Code / future A1 workers) làm việc trực tiếp trong repo external đó
- nhưng vẫn phải:
  - lấy context authority từ AICOS
  - update writeback / handoff / task continuity vào AICOS
- mà không cần merge repo hoặc dựa vào raw cross-folder edit như assumption chính

---

## 1. Executive Summary

AICOS should not try to absorb an external project repo as if it were the same working tree.

Instead:

- the external repo remains the **code/runtime authority**
- AICOS remains the **context / coordination authority**
- a **local MCP bridge** provides the controlled interface between the two

### Key conclusion

Do **not** assume a worker launched in folder X can reliably or portably read/write raw files in folder Y as the main architecture.

Different workers have different permission and sandbox models.
Therefore, a local MCP bridge is the correct architectural path.

---

## 2. Problem This Bridge Solves

The core problem is:

- project code and working files live in external repo/folder
- AICOS truth lives in the AICOS repo/folder
- a worker should not need to bulk-open both repos and manually route edits
- continuity and writeback must still land in AICOS correctly

Without a bridge, you get one of two bad outcomes:

### Outcome A — merge repos
Too heavy, confusing, and difficult to maintain.

### Outcome B — manual copy/paste / raw cross-folder edits
Too fragile, too worker-specific, too easy to break.

### Therefore

AICOS needs a cross-repo bridge contract.

---

## 3. Authority Model

## 3.1. External project repo authority

The external project repo remains authority for:

- source code
- scripts
- tests
- environment/bootstrap
- runtime execution
- generated runtime artifacts
- repo-local implementation files

## 3.2. AICOS authority

AICOS remains authority for:

- imported project canonical truth
- imported project working truth
- handoff/current continuity
- open questions / open items / risks
- A1 startup / packets / continuation guidance
- project-level coordination and writeback
- future company/workspace/shared layering

## 3.3. Session/worker authority

The live worker session remains authority for:

- immediate in-memory execution state
- current local task execution
- local tool outputs in the working session

### Rule

The bridge must help convert session execution into AICOS continuity, without pretending session memory itself is durable truth.

---

## 4. Why Local MCP Is Preferred

## 4.1. Raw cross-folder access is not a reliable foundation

Different workers have different permission models.
A worker opened in one repo may not have the same portable access pattern to another repo.

Even if one worker can be configured to access multiple folders, that does not create a general contract that all workers can safely follow.

## 4.2. Local MCP creates a controlled contract

Instead of telling workers to “go edit files in the AICOS repo directly”, the bridge can expose explicit operations such as:

- get startup bundle
- get task packet
- get handoff current
- write task update
- write handoff update
- record checkpoint

This is much safer and much more scalable.

## 4.3. Local MCP keeps AICOS semantics centralized

The MCP bridge can:

- know the correct lane mapping
- enforce scope boundaries
- refuse obviously invalid writes
- keep naming and structure coherent
- evolve without forcing every worker to memorize raw file paths

---

## 5. Design Principle: Bridge, Not Merge

### Rule 1

Do not merge the external project repo into AICOS.

### Rule 2

Do not make AICOS directly own the external project runtime tree.

### Rule 3

Do not make workers depend on raw multi-folder editing as the main integration model.

### Rule 4

Use AICOS local MCP as the primary contract for cross-repo context read/write.

---

## 6. Recommended Local Bridge Shape

## 6.1. Main components

### A. AICOS repo
Holds truth and coordination lanes.

### B. External project repo
Holds code/runtime/artifacts.

### C. Local MCP bridge process
Runs locally and exposes controlled AICOS operations to workers.

### D. Optional local bridge cache/staging in external repo
For convenience only, not as primary authority.

---

## 6.2. Optional `.aicos/` local bridge folder

The external project repo may include a lightweight `.aicos/` folder for:

- current startup snapshot
- current task packet snapshot
- writeback staging drafts
- local pointer/config to AICOS

### Important

`.aicos/` is optional cache/staging.
It is not the primary source of truth.

---

## 7. Core MCP Responsibilities

The bridge should do 3 categories of work.

## 7.1. Read-serving responsibilities

Provide compact, role-aware, scope-aware context from AICOS to the worker.

Examples:

- project startup bundle
- current handoff
- current state summary
- task packet
- selected workstream/slice references

## 7.2. Writeback responsibilities

Accept structured updates from the worker and map them into the right AICOS lanes.

Examples:

- task status update
- blocked/waiting update
- handoff update
- checkpoint record
- working-state update

## 7.3. Validation responsibilities

Ensure writes are at least minimally coherent.

Examples:

- scope matches project id
- task packet id exists or is recognized
- handoff update is not obviously malformed
- writeback goes to the correct lane type

---

## 8. Minimal MCP Tool Surface For MVP

### Report Code: BRG-26251

The MVP bridge should start with a very small tool set.

| Tool | Purpose |
|---|---|
| `aicos_get_startup_bundle` | return compact startup capsule for a project + role |
| `aicos_get_handoff_current` | return H1 current handoff for a project |
| `aicos_get_task_packet` | return one task packet |
| `aicos_get_packet_index` | return compact packet index or packet list |
| `aicos_write_task_update` | write/update task continuity info |
| `aicos_write_handoff_update` | write/update handoff continuity info |
| `aicos_record_checkpoint` | record a meaningful checkpoint event |

### Optional later
- `aicos_get_workstream_index`
- `aicos_get_current_direction`
- `aicos_get_open_questions`
- `aicos_generate_startup_cache`

### Rule

Do not add a large MCP tool surface before the MVP proves useful.

---

## 9. Suggested Read Flow

### Step 1
Worker starts in external repo.

### Step 2
Worker reads local repo guidance as appropriate.

### Step 3
Worker calls AICOS MCP to get:

- startup bundle for the relevant role/scope
- current handoff if continuation-sensitive
- packet index if task is not yet selected
- one task packet once selected

### Step 4
Worker proceeds with task execution inside the external repo.

### Rule

A worker should not need to browse large parts of the AICOS repo directly just to start work.

---

## 10. Suggested Write Flow

### Step 1
Worker completes a meaningful milestone in the external repo.

### Step 2
Worker writes structured update through MCP, not raw file editing by default.

### Step 3
Bridge maps that update to:

- task lane update
- handoff update if needed
- project working-state update if needed

### Step 4
AICOS truth is now current enough for another worker to continue.

### Rule

Workers should update AICOS via bridge operations, not by freely editing any cross-repo file path as the default habit.

---

## 11. Data Model Of A Writeback

A writeback should be thin and structured.

### Example categories

- task update
- task blocked update
- task waiting update
- checkpoint event
- handoff summary update
- project working-state note

### Minimum fields often needed

- `project_id`
- `actor_family`
- `logical_role`
- `work_context`
- `task_ref`
- `status`
- `what_is_done`
- `what_is_blocked`
- `next_step`
- `handoff_refs`
- `artifact_refs`
- `checkpoint_type`

### Rule

Do not turn this into a large workflow engine yet.
Keep payloads small and explicit.

---

## 12. Where GBrain/GStack Patterns Help

AICOS should not reuse all of GBrain/GStack wholesale, but several patterns are useful:

### 12.1. Shared operations layer
Like GBrain’s CLI + MCP dual surface, AICOS should ideally have:

- one operations layer
- CLI and MCP both call into that layer

### 12.2. Local stdio MCP first
Like GBrain’s `serve` model, AICOS should start with:

- local stdio MCP
- no remote service assumptions
- no big infra

### 12.3. Local-first storage mindset
Local-first + optional DB-assisted substrate is appropriate for MVP.

### 12.4. Bridge/host mindset
A bridge should help workers consult the brain before and after project work.

### Rule

Reuse architecture patterns, not the full GBrain data model.

---

## 13. What Not To Build Yet

Do not build now:

- remote multi-tenant MCP infra
- full auth system
- company-wide orchestration runtime
- large assignment engine
- full event bus
- central daemon for all workers
- full DB-first authority model
- broad registry-heavy automation

### Reason

The immediate goal is just to make cross-repo project work viable and cheap.

---

## 14. Relationship To `.aicos/` Local Cache

A local `.aicos/` folder in the external repo can be useful for:

- cached startup capsule
- cached task packet snapshot
- writeback draft file
- pointer/config for the bridge

### But

It should remain secondary to AICOS truth.

### Suggested local files

- `.aicos/project-link.json`
- `.aicos/START-HERE.md`
- `.aicos/current-capsule.md`
- `.aicos/current-task-packet.md`
- `.aicos/writeback-draft.json`

### Rule

Do not let `.aicos/` become a shadow authority that diverges from AICOS.

---

## 15. Recommended MVP Implementation Plan

### Phase 1 — bridge contract only
- define MCP tool names
- define request/response shape
- define writeback mapping
- no heavy automation

### Phase 2 — local stdio MCP
- implement minimal read tools
- implement minimal writeback tools
- keep scope to one imported project first

### Phase 3 — optional local cache/staging
- add `.aicos/` convenience files if useful
- keep them generated or bridge-managed where possible

### Phase 4 — real-project validation
- use bridge with `sample-project`
- test startup efficiency
- test writeback correctness
- test continuity across two workers

---

## 16. Validation Questions For The Bridge

The bridge is good enough only if it answers yes to these:

1. Can a worker in the external repo start work without manually browsing the AICOS repo broadly?
2. Can the worker get the right compact context from AICOS?
3. Can the worker write back continuity without raw manual cross-repo edits?
4. Can a second worker continue cheaply after the first worker stops?
5. Does AICOS remain the context authority while the external repo remains the code authority?

---

## 17. Final Recommendation

For cross-repo project work, AICOS should adopt this model:

- AICOS repo = context/control-plane authority
- external repo = code/runtime authority
- local stdio MCP = primary bridge
- optional `.aicos/` = cache/staging only

This is the smallest architecture that is:

- more robust than manual copy/paste
- more portable than direct cross-folder assumptions
- more scalable than per-worker hacks
- still light enough for MVP

---
