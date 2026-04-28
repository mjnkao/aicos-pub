# HMD-26210 — AICOS Handoff-Ready Task Metadata Model And Implementation Guide

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** thay thế ý tưởng “transfer/takeover layer” như một subsystem riêng bằng một hướng nhẹ hơn, thực dụng hơn và ít overlap hơn: **handoff-ready task metadata**.

---

## 1. Executive Summary

AICOS hiện đã có sẵn các lớp continuity chính:

- H1 current handoff index
- H2 episodic handoff notes
- H3 self-brain digest
- task packets
- actor task lanes

Vì vậy, ở phase hiện tại, AICOS **không nên build một transfer/takeover layer riêng** như một subsystem mới.

### Hướng đúng hơn

AICOS nên bổ sung một lớp rất mỏng gọi là:

- **handoff-ready task metadata**

Lớp này không phải lane mới, không phải engine mới, không phải daemon mới.

Nó chỉ là:

- metadata tối thiểu
- rule tối thiểu
- update discipline tối thiểu

để một task có thể được actor khác tiếp tục với chi phí thấp hơn khi actor hiện tại dừng giữa chừng.

### Câu chốt

Không build transfer layer riêng.  
Chỉ làm cho task state hiện có trở nên **handoff-ready**.

---

## 2. Why This Direction Is Better

## 2.1. Why not a separate takeover layer now?

AICOS already has:

- handoff
- task packet
- blocked/waiting task state
- current-state / current-direction
- startup cards
- rule cards

If a separate transfer/takeover layer is added now, it will likely overlap with:

- handoff
- task packet
- blocked/waiting/current task state
- project working summaries

So the cost is:

- more concepts
- more files
- more reading burden
- more ambiguity

without enough new value yet.

---

## 2.2. What is actually missing now?

What is still missing is not a large transfer engine.

What is missing is a small amount of **continuation metadata** such as:

- current owner
- last checkpoint time
- continuation mode
- handoff references
- next actor hint
- handoff readiness

These are small enough to add into existing task/task-packet/task-state structures.

---

## 3. Core Idea

A task should become easier to continue by another actor because:

- project continuity is already captured in project handoff/current-state/current-direction
- task continuity is already captured in task packet + task status lanes
- AICOS only needs a thin extra contract to show whether the task is safe to hand over

### Therefore

The goal is:

> Make task objects and task-adjacent artifacts **handoff-ready**.

Not:

> Build a whole new takeover subsystem.

---

## 4. What “Handoff-Ready Task Metadata” Means

A task is handoff-ready when another actor can answer the following cheaply:

1. Who owns this task now?
2. What is the current status?
3. What has already been done?
4. What is blocked, if anything?
5. What should be done next?
6. Which rules should be loaded?
7. Which handoff/current-state context matters?
8. Which files or lanes were touched?

This should be answerable without reconstructing the entire chat/session history.

---

## 5. Where This Metadata Should Live

## 5.1. Do not create a new lane for this

Do **not** create:

- `transfer/`
- `takeover/`
- `handoff-ready/`
- a new central engine folder

### Rule

This metadata should be embedded in the smallest correct existing artifacts.

---

## 5.2. Primary locations

### A. Task packets

The current task packet contract is already the most natural place for:

- continuation metadata
- handoff references
- next-step expectations

### B. Actor task state files

In:

- `agent-repo/.../tasks/current/`
- `agent-repo/.../tasks/blocked/`
- `agent-repo/.../tasks/waiting/`

The task state should reflect:

- owner
- checkpoint status
- blocked reason
- next actor hint if relevant

### C. Project handoff/current state

When a task is important enough to affect project continuity, relevant stable/current facts should also be digested into:

- `brain/projects/<project_id>/working/current-state.md`
- `brain/projects/<project_id>/working/current-direction.md`
- `brain/projects/<project_id>/working/handoff/current.md`

---

## 6. Recommended Minimal Metadata Fields

### Report Code: HMD-26211

The following fields are recommended as minimal continuation metadata for a task packet or task state object:

| Field | Purpose |
|---|---|
| `actor_family` | current actor family working the task |
| `logical_role` | current role, e.g. `a2-core-c` |
| `scope` | project/workspace scope |
| `work_context` | branch/work context if useful |
| `current_owner` | current owner identity or actor instance label |
| `continuation_mode` | e.g. `new_task`, `continue_previous`, `migration_followup`, `review_followup` |
| `handoff_refs` | relevant current/episodic handoff references |
| `last_checkpoint_at` | latest safe checkpoint moment |
| `next_actor_hint` | optional hint if another actor family is suitable |
| `handoff_ready` | whether the task is safe to continue by another actor |
| `what_is_done` | concise done-state |
| `what_is_blocked` | concise blocked-state |
| `next_step` | immediate next step |

### Important

Do not require all fields everywhere immediately.  
Adopt them progressively in the smallest coherent way.

---

## 7. Recommended Meanings Of Key Fields

## 7.1. `current_owner`

This is not a permanent identity system.  
It is just the best current label for who is carrying the task right now.

Example:

- `codex/a2-core-c/projects-aicos/branch-main/thread-01`

### Rule

Keep it lightweight and practical.

---

## 7.2. `continuation_mode`

This field helps avoid ambiguous continuation.

Suggested values:

- `new_task`
- `continue_previous`
- `migration_followup`
- `review_followup`
- `branch_followup`
- `handoff_followup`

### Purpose

This helps the next actor know whether the task is fresh or inherits prior continuity.

---

## 7.3. `handoff_refs`

This points to the smallest relevant handoff artifacts.

Examples:

- current handoff index
- one episodic handoff note if truly relevant

### Rule

Do not point to many handoffs by default.

---

## 7.4. `handoff_ready`

This should be interpreted narrowly.

### `handoff_ready: true`

Means:

- the task has enough continuation information
- another actor could continue without large reconstruction cost

### `handoff_ready: false`

Means:

- still too much implicit context remains in the current session
- checkpoint is insufficient
- the task should be checkpointed more before handoff

---

## 8. Recommended Status Vocabulary

### Report Code: HMD-26212

A lightweight vocabulary is enough:

| Value | Meaning |
|---|---|
| `owned_current` | current actor is actively working |
| `checkpointed_current` | current actor has checkpointed safely |
| `blocked_waiting_human` | waiting for human |
| `blocked_waiting_system` | waiting for system/tool/runtime |
| `handoff_ready` | another actor could continue |
| `taken_over` | another actor has started continuing |

### Rule

Do not build a large state machine right now.  
Only standardize vocabulary enough for repo coherence.

---

## 9. Relationship With Handoff, Task Packets, And Working State

## 9.1. Handoff-ready metadata is not the same as project handoff

Project handoff answers:

- what changed in the project
- what is current
- what is stale
- what the next agent should know broadly

Task handoff-ready metadata answers:

- can another actor continue this task cheaply
- what exactly is the next step for this task
- what should the next actor load first for this task

---

## 9.2. Handoff-ready metadata is not the same as the whole task packet

A task packet remains:

- the bounded startup/handoff object for a task

Handoff-ready metadata is only the subset of fields and update discipline that make task continuation cheap.

---

## 9.3. Handoff-ready metadata is not the same as project working summaries

Project working summaries stay in:

- `current-state`
- `current-direction`
- `open-questions`
- `active-risks`
- etc.

Handoff-ready metadata stays closer to actor task continuity.

---

## 10. When It Should Be Updated

## 10.1. Update after meaningful checkpoint

Whenever checkpoint discipline says a meaningful checkpoint is needed, update the smallest relevant continuation metadata too.

### Typical triggers

- meaningful milestone completed
- scope switch
- branch switch for another work item
- thread/session switch
- blocked/waiting state
- actor family change is likely
- pause before long interruption

---

## 10.2. Do not update on every micro-step

Do not update handoff-ready metadata for:

- tiny wording fix
- micro refactor with no continuity impact
- every shell command
- every tool call
- every chat clarification

---

## 11. Minimal Implementation Direction For Codex

## 11.1. Do first

- normalize the concept in repo-visible policy/rules
- add only minimal metadata to current task packet/task-state structures
- keep the naming consistent with current actor mapping model
- ensure startup remains light

## 11.2. Do not do yet

- no takeover service
- no dedicated transfer queue
- no heavy registry
- no global workflow daemon
- no broad API surface
- no DB-first transfer engine

---

## 12. Suggested Small Repo Changes

### Checklist Code: HMD-26213

- [ ] add or normalize handoff-ready task metadata guidance in repo-visible form
- [ ] update task packet template or nearby note to mention the minimal continuation fields
- [ ] normalize how actor task state expresses owner, blocked reason, and next step
- [ ] ensure handoff refs remain small and selective
- [ ] keep current startup and handoff guidance light
- [ ] avoid creating new lanes unless clearly necessary

---

## 13. Suggested Rollout

## Phase 1 — now

- document the model
- adopt minimal metadata
- make tasks checkpoint-friendly and handoff-friendly
- no new subsystem

## Phase 2 — next

- add clearer owner/checkpoint fields
- add `handoff_ready` where it helps
- refine blocked/waiting conventions

## Phase 3 — later if needed

- helper commands
- registry
- stronger validation
- history/event support
- selective automation

---

## 14. Final Rule

Use the smallest rule that solves the real problem.

The real problem is:

- another actor cannot continue cheaply when the first actor stops

The smallest current solution is:

- better checkpoint discipline
- better task continuity metadata
- better use of the handoff/project/task structures that already exist

Not a new engine.

---

## 15. Final Reminder To Codex

Do not build a transfer/takeover subsystem as a separate heavyweight concept.

Instead:

- make tasks handoff-ready
- make checkpoints meaningful
- make project continuity and task continuity align
- keep metadata thin
- keep startup light

AICOS should make actor switching cheaper by making continuity explicit, not by adding a large new layer too early.

---
