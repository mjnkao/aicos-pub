# A1-26233 — AICOS A1 Artifact-Neutral Model For Coding And Non-Coding Workers

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** bổ sung và siết lại A1-26224 theo hướng **artifact-neutral**, để A1 không vô tình bị thiết kế như một “coding-first worker model”, mà có thể áp dụng đúng cho cả:

- coding workers
- design workers
- marketing/content writers
- research workers
- operations / planning workers
- các project thật không lấy code repo làm artifact trung tâm

---

## 1. Executive Summary

AICOS hiện có một nền kiến trúc đúng cho A1:

- `brain/` là project truth / working reality
- `agent-repo/` là actor execution state
- startup theo hướng light + packet-first
- handoff theo H1 / H2 / H3
- task continuity đi theo metadata mỏng, không build subsystem lớn

Tuy nhiên, ở mức triển khai hiện tại, một số wording và default assumptions vẫn còn hơi **coding-biased**.

### Rủi ro chính

Nếu không chỉnh, A1 rất dễ bị hiểu sai thành:

- agent làm việc chủ yếu trên code repo
- dùng git branch làm work context mặc định
- dùng changed files / changed lines làm delta mặc định
- dùng commit/push làm checkpoint mặc định

Điều đó sẽ gây lệch khi A1 làm việc trên:

- design projects
- marketing/content projects
- research-heavy projects
- document-centric hoặc asset-centric projects
- hybrid projects không có repo code làm source chính

### Kết luận

A1 phải được chuẩn hóa thành:

> **project-work architecture**
> không phải
> **coding-work architecture**

Coding chỉ là **một loại project work**, không phải default model cho toàn bộ A1.

---

## 2. Core Problem This Spec Solves

A1-26224 đã làm rõ:

- A1 identity
- layered rules
- startup layers
- continuation model

Nhưng vẫn cần thêm một lớp trung hòa để tránh việc:

- rule của coding worker trở thành rule chung cho mọi A1
- project onboarding mặc định ngầm coi repo code là trung tâm
- checkpoint rules trở nên vô nghĩa với non-coding workers
- handoff/task packets thiếu thông tin đúng loại cho design/content/research work

### This spec solves:

1. neutralizing coding-biased defaults
2. defining artifact-neutral language
3. making checkpoint discipline reusable across artifact types
4. making startup, handoff, and task continuity portable beyond code work

---

## 3. Design Principle: A1 Is Project-Work, Not Code-Work

### Principle A

A1 works on **project reality**, not on “code” specifically.

### Principle B

A1 may operate on different primary artifact types depending on the project or task.

### Principle C

A1 core rules must remain neutral across artifact types.

### Principle D

Project-specific or workstream-specific rules may define artifact details, but A1 core must not assume one artifact type as universal.

---

## 4. Artifact-Neutral Vocabulary

### Report Code: A1-26234

The following vocabulary should replace coding-biased defaults where possible.

| Coding-biased wording | Artifact-neutral replacement |
|---|---|
| code branch | work context / route / scenario / branch |
| repo code | primary project artifact(s) |
| changed files / changed lines | artifact delta / meaningful work delta |
| commit / push | artifact checkpoint / remote continuity checkpoint |
| code task | task / work item / deliverable task |
| repo root | project working surface / primary working surface |
| implementation change | work change / artifact change |
| code review | review / approval / critique / validation |
| refactor branch | alternate work context / branch reality / route |
| coding packet | task packet |

### Rule

Do not ban coding terms when the task is actually coding.

But do not let coding terms become the assumed meaning of all A1 work.

---

## 5. Primary Artifact Types A1 Must Support

A1 should be able to work on multiple artifact categories.

### 5.1. Code-centric artifacts
Examples:

- source code
- scripts
- configs
- test suites
- structured runtime outputs

### 5.2. Document-centric artifacts
Examples:

- PRDs
- requirements docs
- memos
- strategy docs
- meeting summaries
- analysis notes

### 5.3. Design-centric artifacts
Examples:

- design concepts
- wireframes
- mockups
- Figma explorations
- design systems notes
- asset sets

### 5.4. Content-centric artifacts
Examples:

- copy drafts
- campaign messaging
- social post batches
- blog drafts
- email sequences
- ad variants

### 5.5. Research-centric artifacts
Examples:

- evidence packets
- comparison notes
- summaries
- structured findings
- research questions and review outputs

### 5.6. Hybrid artifacts
Examples:

- projects that mix code + docs + design + analysis
- product launches
- content systems with automation
- trading systems with docs, prompts, data, scripts, and memos

### Rule

A1 must not assume one of these categories is always primary.

---

## 6. Work Context Must Be Broader Than Git Branch

A1-26224 already defines `work_context`, but here we make the meaning explicit.

## 6.1. `work_context` is the neutral concept

`work_context` is the continuation boundary for the current work route.

It may be:

- a git branch
- a scenario route
- a concept route
- a campaign angle
- a design exploration route
- a review lane
- a research path

### Examples

- `branch-main`
- `scenario-bullish-route-a`
- `concept-minimalist-landing-page`
- `campaign-angle-gen-z-a`
- `research-comparison-v2`

### Rule

Git branch is only one concrete form of work context.

Do not write A1 core rules as if `work_context` always means a git branch.

---

## 7. Artifact Checkpoint Model

This is the most important neutralization.

## 7.1. Why “git checkpoint” is not enough

For coding work, checkpoint often means:

- local commit
- push
- updated task state
- updated handoff

But for non-coding work, the same logic must survive even when git is not the primary artifact surface.

So A1 must use a broader concept:

> **artifact checkpoint**

---

## 7.2. Definition of artifact checkpoint

An artifact checkpoint is a meaningful saved/recorded state of the current work artifact(s), plus the corresponding continuity metadata needed so another actor can continue.

### It usually includes:

- artifact state has been saved or stabilized enough
- task state has been updated
- next step is explicit
- blocked state is explicit if relevant
- project continuity was updated if the change matters at project level

---

## 7.3. Artifact checkpoint examples by artifact type

### Coding work
Artifact checkpoint may include:

- local commit
- push when needed
- task state update
- handoff/current update when continuation matters

### Writing/content work
Artifact checkpoint may include:

- saved draft version
- review-ready draft milestone
- task state update
- relevant working-state update

### Design work
Artifact checkpoint may include:

- named concept version
- design route chosen/rejected
- saved frame/set/milestone
- task state update
- review blocker captured

### Research work
Artifact checkpoint may include:

- saved research digest
- evidence packet updated
- comparison summary checkpoint
- task state update
- open question/risk update if relevant

### Rule

“Checkpoint” must remain meaningful across artifact types.
Do not define checkpoint only as commit/push in A1 core rules.

---

## 8. Shared Checkpoint Triggers vs Artifact-Specific Triggers

## 8.1. Shared triggers

These apply across artifact types:

- meaningful milestone completed
- task status changed
- blocked/waiting state
- scope switch
- work-context switch
- session/thread switch
- actor-family switch
- significant new risk / open question / direction change

## 8.2. Artifact-specific triggers

These depend on artifact type:

### Coding
- meaningful repo delta
- stable code milestone
- commit-worthy change

### Writing/content
- new draft milestone
- revision milestone
- review-ready version

### Design
- concept checkpoint
- route choice checkpoint
- review-ready design packet

### Research
- digest checkpoint
- evidence packet checkpoint
- comparison milestone

### Rule

A1 core policy should define shared triggers.
Project/workstream rules may add artifact-specific triggers.

---

## 9. A1 Startup Must Be Artifact-Neutral

Startup should not assume:

- repo code is always primary
- branch is always git branch
- task packet is always about code
- current direction is always technical architecture

### Instead startup should load:

1. A1 startup card
2. project current-state
3. project current-direction
4. current handoff if continuation-sensitive
5. packet index / workstream index
6. one task packet after task selection
7. rule cards triggered by the task

This works for both:

- coding
- non-coding
- hybrid projects

---

## 10. A1 Continuation Must Be Artifact-Neutral

Continuation metadata should not care whether the task was code, design, writing, or research.

### Minimum continuation questions remain the same

1. Who owns this task now?
2. What is the current status?
3. What is done?
4. What is blocked?
5. What is the next step?
6. Which rules should be loaded?
7. Which handoff refs matter?
8. Which work context is current?

### Rule

The metadata shape may stay stable, while project/workstream packets define artifact-specific details.

---

## 11. A1 Core Rules Must Stay Domain-Neutral

This is the part that protects against future Crypto Trading leakage.

## 11.1. A1 core rules should talk about

- project reality
- current state
- current direction
- handoff
- task packets
- work context
- artifact checkpoint
- task continuity
- review / approval / escalation
- open questions / risks / research

## 11.2. A1 core rules should not assume

- market regime
- sample project packages
- exchange symbols
- campaign channels
- Figma-specific flows
- ad-copy templates
- repo code as default
- git commit as universal checkpoint

Those belong in:

- project-specific rules
- workstream-specific rules
- task packets

---

## 12. Recommended A1 Rule Architecture

### Report Code: A1-26235

A1 should now be understood as having:

#### Layer A — A1 core rules
Artifact-neutral, reusable across projects.

#### Layer B — scope-specific rules
Future-extensible to:
- company
- workspace
- project

Currently likely active mainly at project scope.

#### Layer C — workstream/task-specific rules
Artifact-type and task-specific.

### Important

This means future company/workspace layers can fit naturally without redefining A1.

---

## 13. Future Scope Expansion Compatibility

This spec should support future higher-scope rule stacks such as:

- shared/global policy layer
- company rules
- workspace rules
- project rules
- workstream/task rules

### Rule

Do not build all those layers now.

But do not write A1 in a way that makes future higher-scope layers awkward or impossible.

### Therefore

Use language such as:

- scope-specific rules
- higher-scope rules
- project rules
- workstream/task rules

instead of locking the model to “project only forever”.

---

## 14. What Codex Should Implement

### Checklist Code: A1-26236

- [ ] review A1-26224 and neutralize coding-biased wording where needed
- [ ] preserve the layered A1 model, but make it artifact-neutral
- [ ] update A1 startup wording so it does not assume code repo as default
- [ ] update A1 rule guidance to use artifact checkpoint, not git checkpoint as the universal concept
- [ ] keep `work_context` broader than git branch
- [ ] ensure continuation metadata remains portable across artifact types
- [ ] explicitly keep room for future company/workspace/project/task scope layers
- [ ] do not build a large new subsystem

---

## 15. What Codex Must Avoid

### Checklist Code: A1-26237

- [ ] do not rewrite A1 as a sample-project worker model
- [ ] do not rewrite A1 as a coding-only worker model
- [ ] do not ban coding-specific language where code work is real
- [ ] do not create many new empty folders for future scope layers
- [ ] do not create a broad governance framework now
- [ ] do not make startup heavier
- [ ] do not introduce artifact-type-specific branches into A1 core unless they are abstracted properly

---

## 16. How This Helps Future Projects

If A1 is artifact-neutral:

- Crypto Trading can onboard cleanly as a hybrid project
- a design project can use the same A1 foundation
- a marketing/content project can use the same A1 foundation
- future company/workspace rule layers can be added without redesigning A1
- task packets and continuation/handoff remain reusable across domains

---

## 17. Final Rule

A1 core should define **how project work is handled**.

Project/workstream/task layers should define **what kind of work it is**.

That separation is what keeps A1 scalable across:

- coding projects
- design projects
- writing/marketing projects
- research projects
- hybrid projects

Do not make A1 “universal” by making it vague.  
Make A1 reusable by making it **artifact-neutral at core** and **specific only at the lower layers**.

---
