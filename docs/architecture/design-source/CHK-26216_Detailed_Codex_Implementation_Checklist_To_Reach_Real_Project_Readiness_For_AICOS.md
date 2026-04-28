# CHK-26216 — Detailed Codex Implementation Checklist To Reach Real-Project Readiness For AICOS

**Status:** execution-checklist-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** checklist triển khai chi tiết để Codex thực hiện tuần tự, giúp AICOS đạt mức sẵn sàng đưa một dự án thật như Crypto Trading vào để chạy thử với A1 agents.

---

## 1. Working Context

Current intent for this phase:

- AICOS is no longer being refined only for itself
- the next major milestone is to bring a **real existing project** into AICOS
- the first real candidate project is **Crypto Trading**
- the purpose is to test AICOS under real usage:
  - context sufficiency
  - context efficiency
  - rule compliance
  - continuity quality
  - operational friction

### Rule

Do not overbuild large new systems before this real-project test milestone.

---

## 2. Implementation Order

### Phase A — Core discipline hardening
1. mandatory checkpoint/writeback policy
2. task-state convention hardening
3. `context start` hardening

### Phase B — Minimum viable A1 branch
4. A1 role/startup card
5. A1 rule cards
6. A1 task/startup conventions

### Phase C — Real project onboarding standard
7. project import/onboarding checklist
8. project-to-AICOS lane mapping spec
9. imported project bootstrap state

### Phase D — Real usage test readiness
10. startup/token test plan
11. rule compliance test plan
12. continuity/interruption test plan
13. real task quality test plan

---

## 3. Phase A — Core Discipline Hardening

## A1. Mandatory checkpoint / writeback policy

### Goals
- define when an actor must checkpoint
- define when project state must be updated
- define when actor task state must be updated
- define when handoff current must be updated
- define when local commit is expected
- define when push is expected

### Checklist Code: CHK-26217

- [ ] create or normalize a repo-visible checkpoint policy
- [ ] encode milestone trigger
- [ ] encode scope-switch trigger
- [ ] encode repo-delta trigger
- [ ] encode pause/blocked trigger
- [ ] state clearly that more than one meaningful uncheckpointed milestone is not acceptable
- [ ] keep the policy portable and not dependent on provider-specific context percentages
- [ ] avoid using vague trigger language like “thread too long” as the main rule

### Expected output
- a repo-visible checkpoint policy
- updated rules/startup guidance if needed
- short implementation note

---

## A2. Task-state convention hardening

### Goals
Make actor task continuity cheaper without creating a new subsystem.

### Checklist Code: CHK-26218

- [ ] normalize minimal task-state fields
- [ ] ensure task status vocabulary is coherent
- [ ] ensure blocked/waiting/current lanes use consistent semantics
- [ ] clarify owner / next step / blocked reason / continuation refs
- [ ] keep the design thin; do not build a transfer engine

### Expected fields to consider
- current owner
- status
- blocked reason
- next step
- continuation mode
- handoff refs
- handoff readiness
- last checkpoint marker if useful

### Expected output
- updated task-state guidance and/or template
- short implementation note

---

## A3. `context start` hardening

### Goals
Make startup reliable and light enough for a real project test.

### Checklist Code: CHK-26219

- [ ] review current `./aicos context start` output
- [ ] improve packet summaries or packet selection guidance if needed
- [ ] keep startup orientation-first when no concrete task is selected
- [ ] ensure startup does not bulk-load packets/rules/handoffs
- [ ] keep the scope narrow; do not broaden to many actor families yet unless clearly needed

### Expected output
- refined startup behavior or guidance
- short implementation note

---

## 4. Phase B — Minimum Viable A1 Branch

## B1. A1 role/startup card

### Goals
Allow an A1 actor to start work on a real project correctly.

### Checklist Code: CHK-26220

- [ ] define A1 startup card
- [ ] define what A1 reads first
- [ ] define what A1 is and is not doing
- [ ] define when A1 escalates to A2
- [ ] keep startup packet-first and light

### Expected output
- A1 startup card in the correct lane

---

## B2. A1 rule cards

### Goals
Give A1 enough operating rules to work correctly on a real project.

### Checklist Code: CHK-26221

- [ ] create minimal A1 rule cards
- [ ] include writeback/checkpoint rule
- [ ] include handoff/continuation rule
- [ ] include task packet loading rule
- [ ] include project open-items/open-questions/risk handling rule
- [ ] include escalation-to-A2 rule
- [ ] avoid overbuilding broad A1 policy packs

### Expected output
- minimal A1 rule cards in the correct lane

---

## B3. A1 task/startup conventions

### Goals
Make A1 project work operationally coherent.

### Checklist Code: CHK-26222

- [ ] decide how A1 task packets will be represented
- [ ] decide A1 task lane structure
- [ ] define how A1 uses project working state vs actor task state
- [ ] define the minimum continuity path for A1
- [ ] keep conventions compatible with packet-first and handoff-current model

### Expected output
- A1 task/startup convention note or normalized repo rules

---

## 5. Phase C — Real Project Onboarding Standard

## C1. Project import/onboarding checklist

### Goals
Create a reusable checklist to bring an existing project into AICOS.

### Checklist Code: CHK-26223

- [ ] define required identity metadata for an imported project
- [ ] define source inventory checklist
- [ ] define canonical/working/evidence/branches mapping checklist
- [ ] define bootstrap state checklist
- [ ] keep the checklist reusable for future projects beyond Crypto Trading

### Expected output
- onboarding/import checklist file

---

## C2. Mapping spec from existing project into AICOS lanes

### Goals
Map an existing real project’s materials into the correct AICOS lanes.

### Checklist Code: CHK-26224

- [ ] define mapping from existing docs/code/notes/packages into `brain/projects/<id>/...`
- [ ] define mapping into `agent-repo/.../tasks/...`
- [ ] define what remains in evidence/reference only
- [ ] define how candidate branches/experiments are represented
- [ ] keep shared vs project-specific boundaries explicit

### Expected output
- project-to-AICOS lane mapping spec

---

## C3. Imported project bootstrap state

### Goals
After import, the project should be startup-usable in AICOS.

### Checklist Code: CHK-26225

- [ ] require `current-state.md`
- [ ] require `current-direction.md`
- [ ] require `handoff/current.md`
- [ ] require `open-questions.md`
- [ ] require `open-items.md`
- [ ] require `active-risks.md`
- [ ] require minimal packet index or startup path if needed

### Expected output
- bootstrap-state checklist/spec

---

## 6. Phase D — Real Usage Test Readiness

## D1. Startup and token test plan

### Checklist Code: CHK-26226

- [ ] define how to test startup loading
- [ ] define what “too much loading” means
- [ ] define how to observe whether packet-first reduces burden
- [ ] keep the test runnable with Codex and Claude Code

---

## D2. Rule compliance test plan

### Checklist Code: CHK-26227

- [ ] define what rules must be followed during project work
- [ ] define how violations will be noticed
- [ ] define how to distinguish architecture flaw vs actor-discipline flaw

---

## D3. Continuity/interruption test plan

### Checklist Code: CHK-26228

- [ ] define a controlled interruption scenario
- [ ] define how actor switching will be tested
- [ ] define what a “cheap continuation” means
- [ ] keep the test thin and repo-coherent

---

## D4. Real task quality test plan

### Checklist Code: CHK-26229

- [ ] choose one real project slice
- [ ] define one or more real tasks to attempt
- [ ] define success criteria
- [ ] define failure patterns to watch for
- [ ] define what human intervention should be measured

---

## 7. Crypto Trading Project Slice Recommendation

The first real-project test should **not** import everything at once.

### Checklist Code: CHK-26230

- [ ] choose a bounded Crypto Trading slice
- [ ] ensure the slice is real enough to test context quality
- [ ] ensure the slice is small enough to debug
- [ ] avoid onboarding the full project at once
- [ ] keep slice choice explicit in the repo-visible plan

---

## 8. General Constraints

### Do not
- [ ] do not build full A2-Serve runtime now
- [ ] do not build UI now
- [ ] do not build public API now
- [ ] do not migrate all backups deeply now
- [ ] do not create a large transfer engine now
- [ ] do not create a DB-first ownership system now
- [ ] do not broaden scope before a real-project slice is ready

### Do
- [ ] keep changes incremental
- [ ] keep repo coherent
- [ ] prefer normalized repo-visible truth over long ad hoc notes
- [ ] keep startup light
- [ ] prefer evidence from real usage over architecture speculation

---

## 9. Suggested Working Method For Codex

### Report Code: CHK-26231

For each major item above, Codex should:

1. read only the smallest current repo context needed
2. normalize the change into the smallest correct lane
3. write a short implementation note
4. avoid broad redesign
5. pause for review after each major item or phase boundary

---

## 10. Definition of Done For This Phase

This phase is complete only when:

- [ ] core checkpoint/writeback discipline is normalized
- [ ] A1 minimum viable branch exists
- [ ] project onboarding/import checklist exists
- [ ] project mapping spec exists
- [ ] imported project bootstrap requirements are clear
- [ ] a real-project test plan exists
- [ ] the next concrete step toward Crypto Trading onboarding is obvious

---

## 11. Final Reminder To Codex

This phase is not about making AICOS look complete in theory.

It is about making AICOS ready enough to ingest one real project and test whether:

- context loads fast enough
- context is sufficient
- token cost stays reasonable
- rules are followed in practice
- continuity works across actors

Prioritize the smallest changes that make that real-project test possible.

---
