# ACT-26200 — AICOS Actor Mapping, Mandatory Checkpoint Discipline, and Thin Takeover Layer Design

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** chốt rõ:
- cách map actor / role / scope / branch / session trong AICOS
- mandatory checkpoint discipline để giảm mất continuity khi actor dừng giữa chừng
- thiết kế một takeover layer mỏng, đủ để mở rộng sau này nhưng không đồ sộ ngay

---

## 1. Executive Summary

AICOS hiện đã đi đúng hướng ở chỗ:

- tách `brain/` khỏi `agent-repo/`
- dùng `brain/` cho project/system reality
- dùng `agent-repo/` cho actor execution reality
- dùng packet-first startup
- dùng handoff model H1 / H2 / H3

Tuy nhiên, để multi-agent work thực sự mượt hơn, AICOS cần thêm 2 thứ:

1. **Actor mapping model rõ ràng**
2. **Mandatory checkpoint discipline**
3. **Thin takeover layer** cho tương lai, nhưng không overbuild ngay

### Câu chốt

Takeover chỉ mượt nếu actor trước đó đã checkpoint đủ.  
Vì vậy checkpoint discipline là lớp nền quan trọng hơn takeover engine.

---

## 2. Core Principles

### Principle A — Actor family khác với logical role

- `codex`, `claude-code`, `openclaw`, `human` là **actor families**
- `a2-core-c`, `a2-core-r`, `a2-serve`, `a1-work` là **logical roles**

### Principle B — Scope là first-class dimension

Một actor family có thể làm nhiều scope khác nhau:

- `projects/aicos`
- `projects/melig`
- `workspace/foo`

Scope khác nhau phải được coi là context khác nhau.

### Principle C — Branch và session là continuation boundaries

- branch khác nhau = work-context khác nhau
- thread/session khác nhau = session instance khác nhau

### Principle D — Takeover không thay thế checkpoint

Không có checkpoint đủ tốt thì takeover chỉ là đọc lại rất tốn công.

---

## 3. Actor Mapping Model

## 3.1. Layers

### Layer 1 — Actor Family

Ví dụ:

- `codex`
- `claude-code`
- `openclaw`
- `human`

### Layer 2 — Logical Role

Ví dụ:

- `a2-core-c`
- `a2-core-r`
- `a2-serve`
- `a1-work`

### Layer 3 — Scope Binding

Ví dụ:

- `projects/aicos`
- `projects/melig`
- `workspace/foo`

### Layer 4 — Work Context

Ví dụ:

- `branch-main`
- `branch-handoff-refactor`
- `branch-experiment-a`

### Layer 5 — Session Instance

Ví dụ:

- `thread-01`
- `thread-02`
- `headless-run-003`
- `local-cli-session-04`

---

## 3.2. Recommended Identity Shape

### Report Code: ACT-26201

Use this logical identity model:

```text
<actor_family> / <logical_role> / <scope> / <work_context> / <session_instance>
```

### Examples

- `codex / a2-core-c / projects/aicos / branch-main / thread-01`
- `claude-code / a2-core-c / projects/aicos / branch-main / session-02`
- `openclaw / a2-serve / projects/aicos / service-loop / gateway-session-01`
- `codex / a1-work / projects/melig / branch-feature-foo / thread-07`

---

## 3.3. Practical Interpretation Rules

### Switching project

Switching from `projects/aicos` to `projects/melig` does **not** create a new actor family, but it **does** create a different scoped actor instance.

### Switching branch in one project

Usually same actor family and same role, but a different work-context instance.

### Switching thread in one project

Usually same actor family, same role, same scope, but a different session instance.

### Switching from Codex to Claude Code

Different actor family, even if logical role is the same.

---

## 4. Why This Mapping Matters

This mapping is not just taxonomy.

It helps AICOS:

### 4.1. Decide when checkpoint is mandatory

If scope, work context, or session changes, AICOS can require checkpoint first.

### 4.2. Serve the correct startup bundle

The right startup card, handoff, rule cards, and task packets depend on:

- actor family
- role
- scope
- continuation mode

### 4.3. Prevent cross-project or cross-branch confusion

Without mapping, it is too easy to:

- read the wrong handoff
- continue the wrong task
- update the wrong project state
- mix branch realities

### 4.4. Support future transfer/takeover

If AICOS cannot tell who is handing off to whom across what scope and session, takeover remains ad hoc.

---

## 5. Mandatory Checkpoint Discipline

## 5.1. Why This Matters

The real continuity failure is usually not “takeover does not exist”.

The real failure is:

- actor did too much work
- actor did not checkpoint enough
- actor stopped unexpectedly
- next actor must reconstruct too much context

So checkpoint discipline should come before a large takeover system.

---

## 5.2. Recommended Trigger Types

### A. Milestone trigger

Checkpoint after a meaningful milestone.

Examples:

- a task packet is completed
- a bounded subtask is completed
- a meaningful repo change is stabilized
- task status changes
- a W3 state transition occurs

### B. Scope-switch trigger

Checkpoint before:

- switching project
- switching branch for a different work item
- switching thread to do different work
- handing work to a different actor family

### C. Repo-delta trigger

Checkpoint when repo change exceeds a small practical threshold.

Recommended soft threshold:

- changed files >= 3
or
- net changed lines >= 150

### D. Pause/blocked trigger

Checkpoint before:

- pausing for long enough that continuity may be lost
- waiting for human decision
- blocked state
- likely tool/runtime interruption

### E. Optional provider-budget trigger

Use only if the runtime exposes reliable budget/usage signals.  
Do not make this the main portable rule.

---

## 5.3. Hard Rule

### Report Code: ACT-26202

```text
Do not accumulate more than one meaningful uncheckpointed milestone in the same scoped actor session.
```

This is stronger and more portable than vague context-window percentages.

---

## 5.4. What A Checkpoint Must Do

A good checkpoint should update the smallest correct lanes:

### Shared/project-facing updates

- `brain/projects/<project_id>/working/current-state.md`
- `brain/projects/<project_id>/working/current-direction.md`
- `brain/projects/<project_id>/working/open-questions.md`
- `brain/projects/<project_id>/working/active-risks.md`
- `brain/projects/<project_id>/working/potential-risks.md`
- `brain/projects/<project_id>/working/handoff/current.md` if continuation matters

### Actor-facing updates

- `agent-repo/.../tasks/current/`
- `agent-repo/.../tasks/blocked/`
- `agent-repo/.../tasks/waiting/`
- `agent-repo/.../tasks/backlog/`

### Git checkpoint

- local commit after a bounded milestone
- push before continuity must cross session/machine/actor boundaries

---

## 5.5. Push Policy

### Always do

- write state
- update task status
- checkpoint meaningful changes locally

### Push when

- switching actor family
- stopping because another actor may continue
- stopping for long enough that local continuity is fragile
- switching machine/environment
- needing remote continuity

### Do not require

- push after every micro-step
- push after every wording fix

---

## 6. Thin Takeover Layer: Why And What

## 6.1. Why still define takeover now?

Even if checkpoint discipline is more important now, a thin takeover design is still valuable because:

- the future system will need it
- it clarifies what continuity information is missing
- it helps keep checkpoint outputs takeover-friendly
- it avoids having to reinvent the whole model later

### Important

This does **not** mean build a large orchestration system now.

---

## 6.2. Takeover Layer Goal

The goal is simple:

> If actor A stops, actor B should be able to continue with low reconstruction cost.

### Not the goal

- full workflow engine
- autonomous actor routing system
- giant assignment marketplace
- heavy agent graph

---

## 7. Minimal Takeover Model

## 7.1. Takeover Preconditions

Takeover should rely on these existing or near-existing artifacts:

- current project state
- current direction
- current handoff index
- bounded episodic handoffs if relevant
- task packet
- actor task status
- rule cards
- explicit blocked/waiting reason

If these are missing, takeover cost rises sharply.

---

## 7.2. Takeover Event Model

### Report Code: ACT-26203

A takeover event can be represented conceptually as:

```text
from_actor -> to_actor
for_scope
for_task
with_continuation_state
```

### Example

```text
codex / a2-core-c / projects/aicos / branch-main / thread-01
  ->
claude-code / a2-core-c / projects/aicos / branch-main / session-02
for task: handoff normalization refinement
```

---

## 7.3. Minimal Transfer Payload

A thin takeover payload should contain:

- `from_actor_family`
- `from_role`
- `to_actor_family` (optional if undecided)
- `scope`
- `work_context`
- `task_ref`
- `task_status`
- `what_is_done`
- `what_is_blocked`
- `next_step`
- `rules_to_load`
- `handoff_refs`
- `files_or_lanes_touched`

### Note

This does not need to become a huge standalone system now.  
It can begin as metadata in task packets or blocked/waiting task files.

---

## 8. Where Thin Takeover Data Should Live

## 8.1. Shared continuation state

Should stay in:

- `brain/projects/<project_id>/working/handoff/current.md`
- and working summaries when needed

## 8.2. Task execution transfer state

Should live with the actor task lane:

- `agent-repo/.../tasks/current/`
- `agent-repo/.../tasks/blocked/`
- `agent-repo/.../tasks/waiting/`

### Why

Because takeover is usually about continuing a task, not redefining the whole project truth.

---

## 8.3. Suggested Minimal Addition

Codex can later normalize a small set of fields in task packets or task state files:

- `actor_family`
- `logical_role`
- `scope`
- `work_context`
- `continuation_mode`
- `handoff_refs`
- `next_actor_hint`
- `current_owner`
- `last_checkpoint_at`

This is enough to support thin takeover later without building a large engine.

---

## 9. Suggested Future Transfer States

### Table Code: ACT-26204

| State | Meaning |
|---|---|
| `owned_current` | current actor is working the task |
| `checkpointed_current` | task is current and safely checkpointed |
| `blocked_waiting_human` | blocked on human input |
| `blocked_waiting_system` | blocked on system/tool/runtime issue |
| `handoff_ready` | another actor could continue now |
| `handoff_in_progress` | transfer is happening |
| `taken_over` | another actor is now the active owner |

### Important

Do not build this full state machine immediately unless real usage proves it necessary.

---

## 10. How Thin Takeover Should Interact With Handoff

### Rule

Takeover should not invent a second continuity system.

It should use:

- H1 current handoff index
- H2 episodic handoffs if needed
- H3 self-brain digest
- task packet
- task execution state

### Short rule

Project continuity stays in project working/handoff.  
Execution continuity stays in actor task lanes.

---

## 11. Recommended Rollout Plan

## 11.1. Phase 1 — Now

Implement or normalize:

- actor mapping policy
- mandatory checkpoint policy
- metadata additions to task/task-packet/handoff files
- no heavy takeover engine

## 11.2. Phase 2 — Near future

Add:

- thin transfer metadata
- handoff-ready task state
- current owner / next actor hint
- continuation references

## 11.3. Phase 3 — Later

Only if usage proves necessary:

- lightweight takeover helper commands
- actor registry
- task transfer validation
- history/event registry
- automated takeover suggestions

---

## 12. What Not To Build Yet

Do not build now:

- giant orchestration runtime
- complex actor graph
- mandatory central takeover daemon
- full takeover workflow engine
- heavy DB-first ownership system
- broad automation of actor assignment

---

## 13. Concrete Questions Codex Should Be Able To Answer Later

A mature but still thin system should later answer:

- Who owns this task now?
- Is this task safely checkpointed?
- Which actor family can continue this task?
- What must the next actor read first?
- Which branch/work context is current?
- Is this a continuation in the same session, a new session, or a new actor family?

---

## 14. Recommended Immediate Repo Normalization

### Checklist Code: ACT-26205

- [ ] define actor mapping policy in repo-visible form
- [ ] define mandatory checkpoint policy in repo-visible form
- [ ] add minimal identity/continuation metadata to task packets or task files
- [ ] avoid broad engine work
- [ ] keep takeover model documented but thin
- [ ] ensure project continuity and actor execution continuity remain distinct

---

## 15. Final Reminder To Codex

Do not solve continuity by assuming one actor will finish everything.

Do not solve continuity by building a giant takeover engine too early either.

Solve it in this order:

1. map actors clearly
2. force meaningful checkpoints
3. keep project and actor lanes distinct
4. add thin transfer metadata
5. only later automate takeover more deeply

AICOS should make multi-actor continuation cheap before trying to make it fancy.

---
