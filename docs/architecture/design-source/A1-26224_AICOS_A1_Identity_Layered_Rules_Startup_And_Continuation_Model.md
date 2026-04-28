# A1-26224 — AICOS A1 Identity, Layered Rules, Startup, And Continuation Model

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** chuẩn hóa chi tiết mô hình A1 để Codex triển khai tiếp theo đúng hướng, trong bối cảnh AICOS đang chuẩn bị ingest một dự án thật như Crypto Trading và cần A1 đủ rõ để nhiều actors có thể làm việc trên cùng project mà không bị nhầm context, nhầm rules, hoặc nhầm continuation.

---

## 1. Current Context This Spec Builds On

The current repo state already establishes:

- `brain/` as durable project/system reality.
- `agent-repo/` as actor operations, tasks, rules, and packets; not project truth.
- project handoff is now normalized into:
  - `brain/projects/aicos/working/handoff/current.md` as H1 current handoff index
  - `brain/projects/aicos/working/handoff/episodes/` as H2 episodic handoffs
  - `brain/projects/aicos/working/` as H3 self-brain digest
- startup is packet-first and index-first
- `./aicos context start A2-Core-C projects/aicos` exists in MVP form
- `./aicos sync brain` and `./aicos option choose` are working MVP CLI flows
- handoff-ready task metadata is being normalized as a thin continuation layer, not as a separate takeover subsystem
- CHK-26216 real-project readiness pass has already created:
  - shared onboarding foundation
  - minimum viable A1 branch foundation
  - test templates
  - Crypto Trading bootstrap placeholder

This spec should build on that foundation and tighten A1 specifically.

---

## 2. Why A1 Needs A More Explicit Model

A1 is not a single agent.

A1 is an **agent class / agent type** that works on **project reality**.

In a real project, there may be many A1 participants:

- different actor families (Codex, Claude Code, OpenClaw, future others)
- different branches/work contexts
- different threads/sessions
- different workstreams
- different task scopes

If A1 is left under-specified, these failures become likely:

- a new A1 loads the wrong level of rules
- a new A1 confuses project rules with domain-specific rules
- a new A1 continues the wrong branch or wrong workstream
- a new A1 treats a continuation task as a fresh task
- A1 rules become accidentally “Crypto Trading rules” instead of reusable A1 rules
- one A1 actor hands off poorly to another A1 actor

### Conclusion

A1 needs a clear model for:

- identity
- startup layers
- rules layers
- task continuity
- continuation/handoff behavior
- distinction between generic A1 rules and project/workstream/task-specific rules

---

## 3. A1 Must Be Layered, Not Flat

The biggest long-term risk is to accidentally write:

- task rules
as if they were
- project rules

or write:

- project rules
as if they were
- global A1 rules

### Therefore, A1 must be modeled in layers.

---

## 4. A1 Identity Model

## 4.1. A1 is a class, not one singleton actor

A1 should be understood as:

> a project-work agent class

A1 instances are specific combinations of:

- actor family
- logical role
- scope
- work context
- session instance

---

## 4.2. Recommended A1 identity shape

### Report Code: A1-26225

Use this identity model:

```text
<actor_family> / a1-work / <scope> / <work_context> / <session_instance>
```

### Examples

- `codex / a1-work / projects/sample-project / branch-main / thread-01`
- `claude-code / a1-work / projects/sample-project / branch-main / session-02`
- `openclaw / a1-work / projects/sample-project / branch-scenario-b / session-03`

### Interpretation

- same actor family + same project + same branch + same thread = same immediate instance
- same actor family + same project + different branch = different work-context instance
- same actor family + same project + same branch + different thread = different session instance
- different actor family = different actor instance even if logical role is the same

---

## 4.3. Why this matters for A1

This helps AICOS answer:

- is this the same A1 continuing?
- is this a new A1 session in the same project?
- is this a new A1 on a different branch?
- is this a different actor family taking over?
- which startup/handoff/task packet should this A1 read first?

---

## 5. A1 Rule Layering

A1 rules must be separated into **three layers**.

## 5.1. Layer A — A1 core rules

These are reusable across projects.

They describe what A1 is and how A1 generally behaves.

### Examples

- A1 works on project reality.
- A1 reads startup context lightly and packet-first.
- A1 does not bulk-load all docs/rules/handoffs at startup.
- A1 writes state on meaningful transitions, not on every chat turn.
- A1 updates project/shared truth in `brain/projects/<project_id>/...`.
- A1 updates actor execution state in `agent-repo/.../tasks/...`.
- A1 escalates to A2 when the issue is about AICOS system mechanics rather than project delivery.
- A1 does not treat backend/index/runtime substrate as project truth.

### Important

These rules must remain domain-neutral.

They must not contain assumptions like:

- market regime
- sample project package
- trading memo flow
- exchange-specific logic
- technical indicators
- domain-specific deliverables

Those belong in lower layers.

---

## 5.2. Layer B — Project-specific rules

These are rules for A1 in one project.

### Examples for a future Crypto Trading project

- what files are canonical truth
- what current-state/current-direction files matter
- what vocabulary the project uses
- where open questions / risks / research live
- what current project workstreams exist
- what project-level escalation patterns exist

### Rule

These rules may be specific to `projects/sample-project`, but they must still not hardcode one task’s workflow as if it were the whole project.

---

## 5.3. Layer C — Workstream / task-specific rules

These are the narrowest rules and should be loaded only when needed.

### Examples

- memo workflow rules
- package ingestion rules
- strategy review rules
- analytics pipeline rules
- research-review flow rules

### Rule

These should be loaded by:

- task packet
- workstream packet
- or explicit task selection

They should not be startup-default for every A1.

---

## 6. A1 Startup Model

A1 startup must also be layered.

## 6.1. Startup layer sequence

### Layer 1 — A1 core identity
Very short startup card.

### Layer 2 — project orientation
Project current-state, current-direction, project handoff current.

### Layer 3 — workstream index or task packet index
Only if needed.

### Layer 4 — concrete task packet
Load only after a task is selected or strongly implied.

### Layer 5 — task-triggered rule cards
Only the cards required by the selected task.

---

## 6.2. Rule for no-task-selected startup

If no concrete task has been selected yet, A1 should stop at:

- A1 startup card
- project orientation
- packet index / workstream index
- maybe current handoff current if continuation matters

Then ask the human which task or workstream to continue.

### Rule

Do not load all task packets at startup.

Do not load all old episodic handoffs at startup.

Do not load all domain docs at startup.

---

## 6.3. Minimal startup reading order for A1

### Report Code: A1-26226

A future A1 startup order should look like:

1. A1 startup card
2. project role/rules baseline if required
3. `brain/projects/<project_id>/working/current-state.md`
4. `brain/projects/<project_id>/working/current-direction.md`
5. `brain/projects/<project_id>/working/handoff/current.md` only if continuation-sensitive
6. A1 task packet index or workstream index
7. one concrete task packet after selection
8. only the rule cards named by that packet

---

## 7. A1 Continuation Model

A1 continuation must distinguish between:

- new task
- continuation in same project
- continuation in same branch
- continuation in different branch
- continuation by a different actor family

---

## 7.1. Minimum continuation metadata for A1 tasks

### Report Code: A1-26227

A1 task packets or A1 task-state files should support these minimal continuity fields:

- `actor_family`
- `logical_role`
- `scope`
- `work_context`
- `current_owner`
- `continuation_mode`
- `handoff_refs`
- `last_checkpoint_at`
- `next_actor_hint`
- `handoff_ready`
- `what_is_done`
- `what_is_blocked`
- `next_step`

### Why

Without these, one A1 actor continuing another A1 actor’s work will remain expensive and error-prone.

---

## 7.2. Recommended `continuation_mode` values for A1

Suggested values:

- `new_task`
- `continue_previous`
- `branch_followup`
- `review_followup`
- `handoff_followup`
- `research_followup`
- `blocked_recovery`

This allows a new A1 to know if a task is:

- fresh
- inherited
- branch-specific
- review-driven
- recovery-driven

---

## 7.3. Recommended A1 handoff rule

A1 should not write handoff for every tiny change.

But A1 must update continuation artifacts when:

- a meaningful milestone completes
- the task becomes blocked/waiting
- the task is likely to be continued by another actor
- the actor is switching scope / branch / session for a different task
- human choice changes project direction materially

---

## 8. Distinguishing Project, Workstream, Branch, And Task For A1

A1 confusion risk is highest when these layers are mixed.

## 8.1. Project layer

Examples:

- `projects/sample-project`
- `projects/melig`

This is the broadest scope.

## 8.2. Workstream layer

Examples within a project:

- memo workflow
- package ingestion
- scenario analysis
- performance review
- strategy research

This is narrower than the project, broader than one task.

## 8.3. Branch / work-context layer

Examples:

- `branch-main`
- `branch-scenario-a`
- `branch-ingestion-refactor`

This expresses continuity context.

## 8.4. Task layer

This is the concrete current work item.

### Rule

A1 startup must not assume that project = workstream = branch = task.

They are different layers and should be represented separately in packets/rules/handoffs.

---

## 9. Recommended A1 Artifact Set

Codex should not build a huge A1 system immediately.

But A1 needs a minimal coherent artifact set.

## 9.1. A1 startup card

Suggested lane:

- `agent-repo/classes/a1-work-agents/startup-cards/a1-work.md`

This should define:

- what A1 is
- what A1 is not
- what A1 reads first
- when A1 escalates to A2

---

## 9.2. A1 rule cards

Suggested lane:

- `agent-repo/classes/a1-work-agents/rule-cards/`

Suggested initial cards:

- `writeback.md`
- `handoff.md`
- `task-packet.md`
- `open-items-and-open-questions.md`
- `risk-and-research.md`
- `escalate-to-a2.md`

### Rule

Keep cards short and trigger-loaded.

---

## 9.3. A1 task packet index

Suggested lane:

- `agent-repo/classes/a1-work-agents/task-packets/README.md`

This should help a new A1:

- see current packet options
- load only one packet after selection
- avoid bulk packet loading

---

## 9.4. A1 task packet conventions

These should reuse the shared task packet model where possible, but clarify:

- A1-specific reading order
- project/workstream/task separation
- continuity fields needed for A1-to-A1 continuation

---

## 9.5. A1 project bootstrap requirements

Any project imported for A1 usage should have at minimum:

- `current-state.md`
- `current-direction.md`
- `handoff/current.md`
- `open-questions.md`
- `open-items.md`
- `active-risks.md`
- task packet index or workstream index

Without this, A1 startup will be too ambiguous.

---

## 10. What Codex Should Implement Next

### Checklist Code: A1-26228

- [ ] define A1 core identity and startup card
- [ ] define A1 layered rule model (core / project / workstream-task)
- [ ] define A1 startup reading order
- [ ] define minimal A1 continuation metadata
- [ ] define A1 packet/task continuity conventions
- [ ] define A1 escalation boundary to A2
- [ ] keep A1 generic-first, not Crypto-specific-first
- [ ] make room for project-specific instantiation later

---

## 11. What Codex Must Avoid

### Checklist Code: A1-26229

- [ ] do not turn A1 core rules into Crypto Trading rules
- [ ] do not make one project’s workflow the global A1 workflow
- [ ] do not bulk-load all A1 rules/packets/docs at startup
- [ ] do not build a large A1 orchestration runtime yet
- [ ] do not mix project truth with actor task execution lanes
- [ ] do not assume same project = same branch = same task continuity
- [ ] do not treat a new session/thread as fully continuous unless checkpoint/handoff supports it

---

## 12. How This Helps Future Real-Project Testing

If A1-26224 is implemented well, then when Crypto Trading is onboarded:

- a new A1 can start with much less ambiguity
- Codex and Claude Code can both act as A1 instances without mixing roles or scopes
- project-specific rules can be added cleanly on top of A1 core rules
- task continuation will be cheaper
- context loading will remain lighter and more reproducible
- future project onboarding will not require redesigning A1 from scratch

---

## 13. Final Rule

A1 must be:

- generic enough to reuse across projects
- scoped enough to avoid cross-project confusion
- layered enough to avoid rule mixing
- light enough to keep startup efficient
- explicit enough to make continuation and handoff cheap

Do not solve A1 by writing one giant rulebook.

Solve A1 by separating:

- A1 core identity
- project startup context
- workstream/task context
- continuation metadata

and loading each layer only when needed.

---
