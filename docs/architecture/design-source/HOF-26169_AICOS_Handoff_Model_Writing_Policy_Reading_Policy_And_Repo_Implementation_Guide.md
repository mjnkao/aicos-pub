# HOF-26169 — AICOS Handoff Model, Writing Policy, Reading Policy, and Repo Implementation Guide

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** hướng dẫn Codex chuẩn hóa cách AICOS ghi, đọc, lưu, và tiêu hóa handoff để handoff không bị ad hoc, không biến thành file quá dài, không bị stale quá nhanh, và không bắt agent mới phải đọc lại quá nhiều handoff cũ không cần thiết.

---

## 1. Executive Summary

AICOS hiện đã có một file đóng vai **current handoff index** khá tốt:

- `docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md`

File này hiện đã phản ánh khá đầy đủ trạng thái mới nhất sau:

- packet-first context loading
- A2-Core startup card
- rule cards
- task packet template
- three real A2-Core task packets
- MVP helper `./aicos context start A2-Core-C projects/aicos`
- fresh-thread tests cho packet-first startup
- updated CLI surface and open questions

Tuy nhiên, AICOS vẫn chưa có một **handoff model** thực sự chuẩn.

### Vấn đề hiện tại

- handoff hiện vẫn mang tính “note theo đợt” nhiều hơn là một lane/model chuẩn
- chưa có policy rõ cho:
  - khi nào phải ghi handoff
  - khi nào không nên ghi
  - handoff nào là current
  - handoff nào là episodic/reference
  - khi nào agent phải đọc current handoff
  - khi nào agent không cần đọc handoff cũ
- chưa có metadata/contract nhẹ cho handoff
- chưa có sự phân biệt đủ rõ giữa:
  - handoff index
  - episodic handoff notes
  - self-brain digest sau handoff

### Kết luận

AICOS cần một **handoff model 3 lớp** + **writing policy** + **reading policy**.

---

## 2. Current Repo Reality This Model Must Respect

The current repo already has the following true state:

- `docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md` is acting as the current handoff index.
- `brain/projects/aicos/working/current-state.md` and related working files are the startup-critical self-brain summaries.
- `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md` is already a hot-context startup artifact.
- Packet-first testing has already happened and is now reflected in the handoff note.
- `./aicos context start A2-Core-C projects/aicos` exists in MVP form.
- `./aicos option choose ...` and `./aicos sync brain` are working MVP CLI surface elements.
- A2-Core is active; A2-Serve is not yet a fully active runtime lane.

This handoff model must build on that reality, not replace it.

---

## 3. The Core Problem Handoff Must Solve

Handoff in AICOS is not just “a summary file”.

Handoff must solve these problems:

### 3.1. Problem A — state transition continuity

When one agent or session stops, the next one needs to know:

- what changed
- what did not change
- what is current
- what is stale
- what to do next
- what not to reopen

### 3.2. Problem B — startup efficiency

A new agent should not need to read:

- all old handoffs
- all long design docs
- all migration notes
- all working files

just to continue one bounded task.

### 3.3. Problem C — no giant stale omnibus file

If handoff is always appended into one long file:

- it becomes unreadable
- it becomes startup burden
- old information mixes with new information
- agents re-read stale material unnecessarily

### 3.4. Problem D — self-brain digestion

AICOS should not keep all stable truths only inside handoff notes.

Handoff should transfer reality into:

- current-state
- current-direction
- open-questions
- active-risks
- implementation-status
- migration-status

so that startup-critical self-brain stays short and useful.

---

## 4. Handoff Model: Three Layers

## 4.1. H1 — Current Handoff Index

This is the single file that tells a new agent:

- what is newest/current
- what is still current
- what is stale/reference only
- what was just implemented
- what changed recently
- what open questions remain
- what the next agent should know first

### Current repo example

- `docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md`

### Rule

At any given time, AICOS should have one clear current handoff index for the active phase/scope.

### Important clarification

The current handoff index is not the same as the entire history.

It is an **index and transition summary**, not a full archive.

---

## 4.2. H2 — Episodic Handoff Notes

These are smaller handoff notes for specific passes, tests, or implementation episodes.

### Examples

- packet-first context-loading implementation note
- task packet creation note
- future A2-Serve contract handoff
- future thin worker prototype handoff

### Properties

- bounded scope
- dated
- concise
- not required at every startup
- used for provenance, review, or follow-up of a specific pass

### Examples already present

- `docs/migration/CTX-26153_context_loading_implementation_note.md`
- `docs/migration/A2_CORE_TASK_PACKETS_20260418.md`

---

## 4.3. H3 — Self-Brain Digest

Stable or current information from handoffs must be digested into self-brain.

### That means

After a meaningful pass, the stable/currenly relevant outcome should be reflected in:

- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/implementation-status.md`
- `brain/projects/aicos/working/migration-status.md`

### Rule

Handoff is a transfer layer.  
Self-brain is the durable short-form startup layer.

---

## 5. Where Handoffs Should Live

## 5.1. Current Handoff Index

For now, it is acceptable to keep the current handoff index in:

- `docs/migration/`

because the repo is still in a migration-heavy architecture-building phase.

### However

Codex should treat it as a first-class handoff object, not just “another migration note”.

---

## 5.2. Episodic Handoffs

Keep them in:

- `docs/migration/`

for now, unless a future phase creates a more explicit `handoffs/` lane.

### Rule

Do not overbuild a new folder tree immediately if the current lane works.

---

## 5.3. Digest Target

The digested current truth belongs in:

- `brain/projects/aicos/working/`
- and in rare stable cases, `brain/projects/aicos/canonical/`

---

## 6. Handoff Writing Policy

## 6.1. Do not write handoff after every small change

Handoff should not be created for:

- tiny wording fixes
- trivial file moves
- micro implementation changes
- chat clarifications
- every small test run

Those should be handled by normal writeback into self-brain or implementation notes only when appropriate.

---

## 6.2. Write or refresh handoff only on handoff-worthy transitions

### A handoff-worthy transition includes:

- completion of a meaningful implementation pass
- completion of a bounded architecture pass
- completion of a fresh-thread usability test with meaningful architectural learning
- CLI surface change that affects startup or operating model
- change in what is current vs stale
- change in active direction
- change in repo-visible truth that next agent must know
- pause/transfer point where another agent/session is likely to continue

---

## 6.3. Handoff update can be one of two kinds

### Type A — refresh current handoff index

Use when:

- the main current story changed
- what is newest/current changed
- open questions changed
- CLI surface changed
- stale statements must be marked stale

### Type B — create a new episodic handoff note

Use when:

- a bounded pass needs its own record
- a test or experiment deserves provenance
- implementation details are too narrow for the current index

---

## 7. Handoff Reading Policy

## 7.1. Default startup rule

A new agent should **not** read all historical handoffs.

### Default reading path

1. startup card
2. canonical role/rules
3. working current-state
4. working current-direction
5. current handoff index only if the task is continuation/migration/follow-up sensitive
6. task packet
7. rule cards triggered by the task

---

## 7.2. When to read the current handoff index

Read the current handoff index when:

- continuing a previous A2-Core pass
- working on repo-wide architecture changes
- working on migration/state alignment
- checking what is newest/current vs stale
- needing a quick continuation summary

---

## 7.3. When to read old episodic handoffs

Read older episodic handoffs only when:

- the current handoff index points to them
- the task is about provenance
- the task is about comparing implementation passes
- the task needs deeper detail that self-brain does not carry
- the task is specifically about a prior episode/test

### Rule

Old handoffs are on-demand, not startup-default.

---

## 8. Metadata Contract For Handoff Files

To keep handoffs understandable and traversable, Codex should normalize a lightweight metadata/header structure.

### Minimal metadata fields

- title
- date
- status
- purpose
- scope
- actor or lane
- what changed
- what did not change
- next suggested actions
- stale/reference-only notes if needed

### Optional but useful

- supersedes
- superseded_by
- related_handoffs
- related_task_packets
- related_rules

### Rule

Do not over-schema this too early.  
Markdown structure is enough at MVP phase.

---

## 9. Suggested Structure For Current Handoff Index

### Report Code: HOF-26170

The current handoff index should aim to look like this:

1. Purpose
2. Read This First
3. Newest / Current
4. Still Current
5. Old / Reference Only
6. What Was Implemented
7. Current Architecture
8. Current CLI Surface
9. Current Verification
10. Open Questions
11. Notes For Next Agent

### This is already close to current repo state

Codex should preserve this shape and improve consistency rather than redesigning it.

---

## 10. Suggested Structure For Episodic Handoffs

### Report Code: HOF-26171

A bounded episodic handoff note should be much smaller:

1. Title
2. Date
3. Status
4. Scope
5. Purpose
6. What changed
7. What did not change
8. What still feels weak
9. Next suggested action
10. Related files/packets/commands

### Rule

Do not turn episodic notes into full duplicate architecture essays.

---

## 11. Handoff vs Self-Brain Rules

## 11.1. What belongs in handoff

- what changed in the last pass
- what is newly current
- what is newly stale
- what the next agent needs to continue
- what the meaningful frictions were
- what next actions make sense

## 11.2. What belongs in self-brain

- stable startup summaries
- current state
- current direction
- active risks
- open questions
- implementation status
- migration status

## 11.3. Rule

Do not use handoff as the permanent home of stable truths.

Digest stable/current information into self-brain.

---

## 12. Handoff vs Task Packets

Task packets are not handoffs.

### Task packets are for:

- bounded task startup
- one task
- one actor
- one scope
- one success condition

### Handoffs are for:

- continuity across passes/sessions/agents
- what just changed
- where the current repo state stands
- what the next agent should know about recent changes

### Rule

A task packet may reference a handoff.  
A handoff may mention task packets.  
But they are not the same object.

---

## 13. Handoff vs Startup Cards

Startup cards are not handoffs.

### Startup cards answer

- who am I
- what lane am I in
- what am I doing
- what do I read first

### Handoffs answer

- what just changed
- what is current now
- what is stale now
- what next agent should know about recent changes

---

## 14. What Codex Should Implement Now

### Checklist Code: HOF-26172

- [ ] treat `docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md` explicitly as the current handoff index
- [ ] ensure current handoff index stays concise and index-like, not a giant omnibus log
- [ ] define a lightweight handoff writing policy in the repo
- [ ] define a lightweight handoff reading policy in the repo
- [ ] define the distinction between current handoff index, episodic handoffs, and self-brain digest
- [ ] ensure startup-critical docs do not require reading all old handoffs
- [ ] ensure new stable/current information from handoffs is digested into self-brain where appropriate
- [ ] avoid creating unnecessary new folders unless current lanes prove insufficient

---

## 15. Concrete Repo Changes Codex Should Consider

Codex should choose the smallest correct set of changes, but likely candidates include:

### 15.1. Update canonical/working rules if needed

Potential target:
- `brain/projects/aicos/canonical/project-working-rules.md`

Add a concise statement that handoff is a first-class continuity layer and should be handled through current index + episodic notes + self-brain digest.

### 15.2. Add a short handoff policy reference in the appropriate lane

Possible lane:
- `agent-repo/classes/a2-service-agents/rules/`
or
- `brain/projects/aicos/evidence/policy-sources/`
or another smallest coherent place

### 15.3. Optionally add a very small handoff reference note

Only if useful, for example:
- `docs/migration/HANDOFF_MODEL_AND_POLICY.md`

But do not create this unless the repo truly needs a dedicated reference doc.

### 15.4. Ensure startup artifacts do not point broadly to all handoffs

Startup cards should stay concise and not force handoff history loading.

---

## 16. Things Codex Must Not Do In This Step

### Checklist Code: HOF-26173

- [ ] do not rewrite all self-brain files around handoff
- [ ] do not create a giant handoff framework
- [ ] do not append everything forever into one current handoff file
- [ ] do not make old episodic handoffs startup-default reading
- [ ] do not duplicate stable truths across too many places
- [ ] do not over-canonicalize handoff details
- [ ] do not require full historical reading for normal continuation tasks

---

## 17. Definition of Done

This handoff work is done only if:

- [ ] the repo has a clear concept of current handoff index
- [ ] the repo has a clear concept of episodic handoffs
- [ ] the repo has a clear rule that stable/current information should be digested into self-brain
- [ ] agents are not required to read all old handoffs at startup
- [ ] the current handoff index stays concise and useful
- [ ] handoff is no longer purely ad hoc
- [ ] the repo remains lighter, not heavier

---

## 18. Final Reminder To Codex

Do not solve handoff by writing more and more summary files.

Solve it by:

- separating current index from episodic history
- keeping current index concise
- digesting stable information into self-brain
- reading old handoffs only on demand

AICOS should remember recent transitions clearly without forcing every new agent to reread the whole past.

---
