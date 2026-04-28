# A2S-26102 — AICOS A2 Taxonomy, A2 Rules, and AICOS Self-Brain Working Spec

**Status:** working-spec-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** làm rõ taxonomy của A2 trong AICOS, phân biệt rõ các nhánh A2 hiện tại và tương lai, đồng thời chốt rules tạm thời và self-brain structure của AICOS để Codex có thể triển khai tiếp mà không bị lẫn giữa A1, A2, và các nhánh A2 con.

---

## 1. Executive Summary

A2 không nên được hiểu là một khối duy nhất.

A2 là **nhóm agents làm việc cho chính AICOS**.  
Điểm chung của tất cả A2 là:

- không làm business/project delivery thay cho A1
- không là owner của project reality của business
- primary customer của chúng là **AICOS**
- mục tiêu cuối cùng của chúng là làm cho:
  - AICOS tốt hơn
  - A1 làm việc tốt hơn
  - human manager quản lý tốt hơn

Tuy nhiên, bên trong A2 phải tách tiếp thành các nhánh con.

### Kết luận chính

A2 có thể chia thành ít nhất 2 nhánh lớn:

1. **A2-Core / A2-Self-Build**  
   làm việc trực tiếp trên chính AICOS:
   - coding
   - build
   - config
   - refactor
   - repo structure
   - kernel
   - integrations
   - runtime/config lanes

2. **A2-Serve / A2-Service-For-A1**  
   không trực tiếp build core system nhiều, mà vận hành và cải thiện AICOS như một hệ phục vụ A1:
   - capsule quality
   - retrieval quality
   - promotion hygiene
   - branch compare quality
   - option generation quality
   - feedback synthesis
   - source quality support
   - service support for A1

### Important clarification

Ở giai đoạn hiện nay:

- **A2-Core là nhánh đang active mạnh nhất**
- **A2-Serve mới là target architecture / future branch**, chưa phải nhánh fully active

Codex hiện tại, khi đang build/update/refactor AICOS, nên được hiểu chủ yếu là:

- **A2-Core**
- cụ thể thường là **A2-Core-Coding**

---

## 2. Project Overview

AICOS là một **company/workspace intelligence layer**.

AICOS không phải là personal brain cho một human.

AICOS phục vụ bối cảnh:

- nhiều humans
- nhiều AI agents
- nhiều projects
- nhiều branches / experiments
- human đóng vai manager / reviewer / approver
- agents đóng vai co-workers

AICOS phải giúp:

- giữ shared project reality
- giảm mất context khi đổi project
- giảm reread quá nhiều tài liệu
- hỗ trợ branch-aware work
- hỗ trợ blocked -> options -> manager choice
- hỗ trợ controlled autonomy
- hỗ trợ self-improvement của chính AICOS

---

## 3. A1 vs A2 At The Highest Level

## 3.1. A1

A1 là agents làm việc **trên project reality**.

A1 tập trung vào:

- project/business work
- requirements
- decisions
- working state của project
- deliverables
- blockers
- options cho project

### Short definition

**A1 works on project reality.**

---

## 3.2. A2

A2 là agents làm việc **trên system reality của AICOS**.

A2 tập trung vào:

- cấu trúc của AICOS
- service behavior của AICOS
- retrieval/capsule/promotion/branch helper quality
- integrations
- self-brain của AICOS
- system improvement for AICOS
- future service support for A1

### Short definition

**A2 works on AICOS system reality.**

---

## 4. Why A2 Must Be Split Further

Nếu không tách A2 thành các nhánh con, sẽ rất dễ xảy ra các nhầm lẫn sau:

- agent đang build kernel nhưng lại tự nghĩ mình là support bot cho A1
- agent đang làm service reasoning nhưng lại tự nhảy sang refactor code lớn
- agent đang tối ưu retrieval cho A1 nhưng lại vô tình đổi architecture gốc của AICOS
- Codex khi build repo sẽ bị lẫn giữa “tôi đang sửa system” và “tôi đang hỗ trợ work runtime”

Do đó, A2 phải có taxonomy rõ.

---

## 5. A2 Taxonomy

## 5.1. A2 Umbrella Definition

A2 = mọi agent có primary mission là **improve, maintain, or operate AICOS itself**.

A2 không trực tiếp sở hữu business/project deliverables của A1.

---

## 5.2. A2-Core / A2-Self-Build

Đây là nhánh A2 hiện đang active mạnh nhất.

### Mission

Build, change, refactor, configure, and evolve AICOS itself.

### Typical responsibilities

- repo structure migration
- kernel code
- packet schemas
- validators
- local CLI
- runtime/config/MCP lanes
- integration wrappers
- migration helpers
- safe write/read primitives
- service-skill scaffolding
- implementation of new AICOS commands

### Typical current actor

- Codex đang build repo AICOS
- Claude Code khi sửa structure / script / config của AICOS
- OpenClaw nếu được giao sửa runtime/config của AICOS

### Short definition

**A2-Core changes AICOS itself.**

---

## 5.3. A2-Serve / A2-Service-For-A1

Đây là nhánh A2 phục vụ A1.

### Mission

Operate and improve AICOS as a system that serves A1 well.

### Typical responsibilities

- build better capsules for A1
- improve retrieval relevance
- improve source selection
- improve promotion recommendations
- improve branch comparison quality
- improve blocker-to-options quality
- synthesize repeated friction from A1
- recommend changes to service rules or service knowledge

### Important note

Nhánh này **chưa active mạnh ở giai đoạn hiện nay**.  
Nó là một phần rất quan trọng của target architecture, nhưng chưa phải trọng tâm triển khai đầu tiên.

### Short definition

**A2-Serve improves how AICOS serves A1.**

---

## 5.4. A2 Submodes Inside A2-Core

Bên trong A2-Core nên còn tách nhỏ thành 2 mode:

### A2-Core-R — reasoning mode

Used for:

- architecture reasoning
- tradeoff analysis
- policy proposals
- migration planning
- structure design
- identifying risks
- deciding what should stay flexible vs what should be coded

### A2-Core-C — coding mode

Used for:

- code changes
- script updates
- config updates
- refactors
- folder migration
- command implementation
- adapter implementation

### Rule

Codex hiện nay phần lớn đang ở:

- **A2-Core-C**

Nhưng trước mỗi thay đổi lớn, Codex nên chuyển qua ngắn hạn sang:

- **A2-Core-R**

để kiểm tra tradeoff trước.

---

## 5.5. A2 Submodes Inside A2-Serve

Khi A2-Serve được kích hoạt sau này, có thể tách tiếp:

### A2-Serve-R — service reasoning

- capsule policy
- retrieval policy
- promotion recommendation policy
- branch option quality analysis
- service feedback synthesis

### A2-Serve-O — service operations

- refresh service summaries
- update serving packets
- maintain support queues
- run service checks
- update service-quality working knowledge

### Important note

This is future-facing.  
Do not force-build all of this now.

---

## 6. Current Active Reality Of A2 In This Project

In the current phase of AICOS:

### Active now

- A2-Core-R
- A2-Core-C

### Not yet active as a full lane

- A2-Serve-R
- A2-Serve-O

### Operational interpretation

If Codex is currently:

- restructuring the repo
- creating kernel packages
- creating schemas
- adding CLI commands
- setting migration lanes
- creating service-skill scaffolds
- updating integrations
- changing configs

then Codex is acting as:

- **A2-Core-C**

If Codex is currently:

- reviewing architecture
- deciding how to split lanes
- deciding what should be canonical vs working
- deciding how A2 should be separated

then Codex is acting as:

- **A2-Core-R**

---

## 7. A2 Rules At The Umbrella Level

These rules apply to all A2 branches.

## A2-U1 — A2 works for AICOS, not for business delivery

A2 may improve AICOS and its service quality, but A2 does not become the owner of business/project execution work.

## A2-U2 — A2 must preserve architecture boundaries

A2 must not blur:

- brain vs agent-repo
- canonical vs working vs evidence
- backend vs truth
- project reality vs system reality

## A2-U3 — A2 must write back to AICOS self-brain

Any meaningful A2 work must update AICOS self-brain in some lane:

- canonical
- working
- evidence
- branch reality

Otherwise system reality and code reality will drift apart.

---

## 8. A2-Core Rules

These rules apply specifically to A2-Core.

## A2C-R1 — A2-Core changes AICOS itself, not project business truth

A2-Core may change:

- structure
- kernel
- scripts
- validators
- config
- integration lanes
- packet renderers
- local CLI
- migration flow

A2-Core may not silently change:

- business/project truth for A1-owned work
- customer/project deliverables
- business requirements unrelated to AICOS itself

---

## A2C-R2 — A2-Core must separate reasoning from coding

Before large changes:

- reason first
- code second

Do not jump directly from vague architectural intention to large code changes without a reviewable intermediate reasoning step.

---

## A2C-R3 — A2-Core should code only the stable substrate

A2-Core should hardcode only:

- schema
- validators
- packet formats
- folder contracts
- write lanes
- safe primitives
- adapters
- CLI wrappers

A2-Core should avoid hardcoding too early:

- capsule intelligence
- option policy
- promotion recommendation heuristics
- branch ranking heuristics
- retrieval strategy heuristics

These should stay in A2 service skills or service knowledge first.

---

## 9. A2-Serve Rules

These rules define the future A2-Serve lane.

## A2S-R1 — A2-Serve serves A1, but still works for AICOS

A2-Serve is not A1.  
It supports A1 by improving how AICOS serves A1.

## A2S-R2 — A2-Serve may recommend changes, but should not silently re-architect AICOS

A2-Serve can identify repeated friction and recommend changes, but structural or architectural changes should escalate to A2-Core-R or human review.

## A2S-R3 — A2-Serve must write service improvements into service-knowledge

A2-Serve should keep its learning in:

- service-knowledge working
- service-knowledge evidence
- reviewable recommendation packets

not in hidden runtime-only notes.

---

## 10. AICOS Self-Brain: What It Means

AICOS itself is a project.

Therefore AICOS must have its own self-brain.

This self-brain holds:

- architecture of AICOS
- current status of AICOS
- risks of AICOS
- migration state
- open questions about AICOS
- role definitions for AICOS
- working rules for AICOS
- service knowledge about improving AICOS
- evidence/review packs about AICOS

### Important clarification

The architecture docs created recently are indeed part of AICOS brain.

However, most of them should currently be treated as:

- **working knowledge**
- or **evidence**

not automatically as canonical truth.

---

## 11. AICOS Self-Brain Structure

### Diagram Code: A2S-26103

```text
brain/projects/aicos/
  canonical/
    project-profile.md
    role-definitions.md
    project-working-rules.md
    source-manifest.md
    architecture.md
    decisions.md
    promotion-policy.md
    capsule-contract.md
    branch-contract.md

  working/
    current-state.md
    current-direction.md
    active-risks.md
    open-questions.md
    handoff-summary.md
    implementation-status.md
    migration-status.md
    architecture-working-summary.md
    service-skills-working-summary.md

  evidence/
    review-packs/
    codex-reports/
    raw-design-notes/
    candidate-rules/
    candidate-decisions/
    friction/
    test-runs/

  branches/
    <branch-id>/
      branch-profile.md
      inherited-context.md
      overrides.md
      assumptions.md
      findings.md
      recommendation.md
      compare-to-main.md
```

---

## 12. What Should Be Canonical First

Do not canonicalize too much too early.

### Safe early canonical candidates

- `project-profile.md`
- `role-definitions.md`
- `project-working-rules.md`
- `source-manifest.md`

### Keep in working first

- `architecture.md`
- `promotion-policy.md`
- `capsule-contract.md`
- `branch-contract.md`

Reason:

These are still evolving and should not constrain Codex too early.

---

## 13. Mapping Existing Documents Into AICOS Self-Brain

### Table Code: A2S-26104

| Existing document | Recommended lane in AICOS self-brain |
|---|---|
| `ARC-26071_*` | `working/architecture-working-summary.md` and/or `evidence/review-packs/` |
| `PLN-26072_*` | `working/implementation-status.md` and `evidence/review-packs/` |
| `DSC-26040_*` | `working/architecture-working-summary.md` |
| `MAP-26031_*` | `working/architecture-working-summary.md` or later canonical |
| `DSC-26038_*` | `evidence/review-packs/` plus summarized into `working/` |
| `AGT-26016_*` | `working/role-definitions-working.md` |
| `RUL-26088_*` | `canonical/role-definitions.md` or `working/role-definitions-working.md` depending on confidence |
| Codex build review pack | `evidence/review-packs/` |

### Important note

Do not necessarily copy every source file as-is into self-brain.

Prefer:

- keep source docs where they are
- create normalized summaries into self-brain
- keep references to source docs

---

## 14. Startup Reading Order For A2

When an A2 agent starts working on AICOS, it should read in this order.

### Step 1 — Role clarity

Read:

- `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`

### Step 2 — A2 taxonomy clarity

Read:

- `A2S-26102_AICOS_A2_Taxonomy_A2_Rules_and_AICOS_Self_Brain_Working_Spec.md`

### Step 3 — Current self-brain working state of AICOS

Read:

- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`

### Step 4 — Architecture working summary

Read:

- `brain/projects/aicos/working/architecture-working-summary.md`

### Step 5 — Implementation and migration status

Read:

- `brain/projects/aicos/working/implementation-status.md`
- `brain/projects/aicos/working/migration-status.md`

### Step 6 — Only then inspect raw repo/code

After the above, inspect:

- repo structure
- scripts
- kernel code
- integrations
- evidence/review packs when needed

### Rule

Do not start with raw repo traversal before reading role and self-brain context.

---

## 15. Immediate Operational Decision For Codex

Until further notice, Codex should assume:

### Default lane

- **A2-Core-C**

### When to switch temporarily into A2-Core-R

Before any of the following:

- large folder migration
- structural package split
- CLI surface redesign
- promotion flow redesign
- major rule rewrite
- new architecture boundary change

### Codex should not assume it is A2-Serve yet

Because A2-Serve is part of the architecture target, but not yet the primary active branch in the current implementation phase.

---

## 16. Immediate Next Steps For Codex

### Checklist Code: A2S-26105

- [ ] create or update AICOS self-brain working files
- [ ] create or update AICOS self-brain canonical identity/rules files
- [ ] place review packs into evidence lane or summarize them into evidence lane
- [ ] update startup reading order so A2 reads self-brain before raw repo
- [ ] explicitly mark Codex current lane as A2-Core-C in working status if useful
- [ ] avoid building A2-Serve as a full runtime lane yet
- [ ] preserve separation between A2-Core and future A2-Serve

---

## 17. Final Short Definitions

### A2 umbrella

A2 = any agent branch whose primary job is to improve or operate AICOS itself.

### A2-Core

A2-Core = the branch that changes AICOS itself.

### A2-Serve

A2-Serve = the branch that helps AICOS serve A1 better.

### Current project reality

At the current phase of the repo, Codex is mainly operating as:

- **A2-Core-C**

---

## 18. Final Reminder

This file exists to prevent a specific confusion:

- not all A2 are the same
- not every A2 serves A1 directly
- the currently active A2 branch is mainly the AICOS-building branch
- future A2 service branches should be separated early in the mental model, even if they are not fully implemented yet

This separation is important so that:

- Codex does not confuse AICOS self-build work with A1-serving operations
- the repo can grow without role collapse
- future A2 branches can be added cleanly

---
