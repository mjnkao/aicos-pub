# RUL-26088 — AICOS Temporary Role Rules For Codex

**Status:** temporary-operational-rules-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** file này dùng để giúp Codex và các agents đang làm việc trên repo AICOS **không bị lẫn vai trò giữa A1 và A2**, đặc biệt trong giai đoạn hiện tại khi Codex đang được dùng để build, update, refactor, và cấu hình chính AICOS.

---

## 1. Project Overview

AICOS là một **company/workspace intelligence layer**.

AICOS không phải là personal brain cho một human duy nhất.  
AICOS được thiết kế cho bối cảnh:

- nhiều humans cùng làm việc
- nhiều AI agents cùng làm việc
- nhiều projects cùng tồn tại
- mỗi project có thể có nhiều branches / experiments
- human đóng vai manager / reviewer / approver
- agents đóng vai co-workers

Mục tiêu của AICOS là:

- giữ shared project reality
- giảm mất context khi chuyển giữa nhiều projects
- giảm việc phải đọc lại quá nhiều tài liệu mỗi lần đổi task
- hỗ trợ branch-aware work
- hỗ trợ agents có controlled autonomy
- hỗ trợ flow blocked -> options -> manager choice
- tách rõ:
  - canonical truth
  - working reality
  - evidence
  - execution state
  - branch / experiment state
  - serving / retrieval layer

Trong giai đoạn hiện tại:

- local MVP only
- dùng GBrain làm substrate
- dùng PGLite trước
- chưa cần Manager UI riêng
- chưa cần Project/task UI riêng
- chưa cần public API riêng
- Codex, Claude Code, OpenClaw là các co-workers local chính
- ChatGPT và Claude chat vẫn là manager-facing layers, sync tay trước

---

## 2. Definition Of A1 And A2 In This Project

## 2.1. A1 — Work Agents / Project Execution Agents

A1 là các agents làm việc **cho company / workspace / project**.

### A1 does

- đọc project reality
- đọc requirements / decisions / working state
- thực thi task của project
- tạo deliverables
- ghi blocker, findings, handoff, option packet
- nếu bị block thì sinh ra các options / MVP directions cho **project**

### A1 does not primarily do

- sửa cấu trúc AICOS
- sửa kernel của AICOS
- sửa service skills của AICOS
- đổi query / capsule / promotion logic của hệ
- đổi config/runtime/MCP chung của AICOS
- tự xem mình là owner của system-serving changes

### Short definition

**A1 works on project reality.**

---

## 2.2. A2 — AICOS Service / Improvement Agents

A2 là các agents làm việc **cho chính AICOS**.

### A2 does

- coding
- build
- config
- refactor
- improve
- maintain

cho các phần như:

- AICOS kernel
- service skills
- serving logic
- capsule flow
- promotion helpers
- branch / option helpers
- integrations
- MCP/runtime/config lanes
- system quality of AICOS

### A2 does not primarily do

- làm deliverable chính cho project business
- quyết định requirement business
- chốt direction sản phẩm của project
- làm thay vai trò project executor của A1

### Short definition

**A2 works on system reality of AICOS.**

---

## 2.3. Important clarification for Codex

Trong giai đoạn hiện tại, khi Codex đang được dùng để:

- build AICOS
- update AICOS
- refactor AICOS
- change config / runtime / structure of AICOS

thì mặc định hãy hiểu **Codex đang ở A2 lane**, cụ thể thường là:

- **A2-C** = coding / build / config / refactor mode

Nếu Codex đang chỉ phân tích, review tradeoff, hoặc đề xuất policy/service logic mà chưa code lớn, hãy hiểu là:

- **A2-R** = service reasoning mode

---

## 3. Startup Reading Order For Agents

Trước khi làm bất kỳ công việc nào trong repo AICOS, agent phải đọc đúng thứ tự sau để tránh lẫn vai trò.

## 3.1. Step 1 — Read this file first

Always read:

- `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`

Purpose:

- hiểu A1 là gì
- hiểu A2 là gì
- hiểu mình đang ở lane nào
- tránh đọc sai loại dữ liệu từ đầu

---

## 3.2. Step 2 — Determine current role

Agent phải tự xác định mình đang ở role nào:

### If the task is about:

- building AICOS
- updating AICOS
- refactoring AICOS
- restructuring repo
- changing config/runtime/integration
- changing capsule / promotion / branch / serving mechanics

Then the agent is in:

- **A2 lane**

### If the task is about:

- doing work inside a specific business/project scope
- implementing project deliverables
- using project truth and current-state to complete a business task

Then the agent is in:

- **A1 lane**

### Rule

If unclear, assume **A2** only when the work clearly changes AICOS itself.  
Otherwise assume **A1** for project execution work.

---

## 3.3. Step 3 — Read architecture summary files

After this file, read:

1. `ARC-26071_AICOS_Kernel_ServiceSkills_GBrain_GStack_Architecture.md`
2. `PLN-26072_Codex_Implementation_Plan_Checklist_For_AICOS_Current_Repo.md`

Purpose:

- hiểu kiến trúc hiện đã chốt
- hiểu MVP direction
- hiểu non-goals
- hiểu migration safety requirements

---

## 3.4. Step 4 — Read project-wide reality files

Then read the high-level project reality and boundary docs:

3. `DSC-26040_AICOS_AI_Native_CoWorker_Architecture_Detail_Spec.md`
4. `MAP-26031_AICOS_Brain_vs_AgentRepo_vs_Backend_ReadWrite_Boundary.md`
5. `DSC-26038_AICOS_Company_Team_Native_Architecture_Leveraging_GBrain.md`
6. `AGT-26016_AICOS_Agent_Classes_Knowledge_Boundaries_and_Rules_Matrix.md`

Purpose:

- hiểu overall project reality
- hiểu layer model
- hiểu boundaries giữa brain / agent-repo / backend
- hiểu actor model

---

## 3.5. Step 5 — Read current repo structure

Only after the above, inspect the current repo:

- repo root structure
- `canonical/`
- `brains/`
- `gateway/`
- `bridges/`
- `reports/`
- `scripts/`
- existing GBrain wrapper scripts
- local integration scripts if relevant

Purpose:

- map current repo into target architecture
- avoid reading raw repo too early without role clarity

---

## 3.6. Step 6 — Read lane-specific data only after role is clear

### If agent is in A1 lane

Read next:

- relevant company/workspace/project truth
- relevant project canonical
- relevant project working state
- relevant branch state if branch task
- only then read evidence if needed

### If agent is in A2 lane

Read next:

- A2 rules
- current AICOS architecture files
- service-knowledge if present
- current repo structure and migration notes
- existing scripts / integrations / kernel-relevant files
- only then inspect deeper repo implementation details

### Rule

Do **not** start by reading random raw docs or large repo areas before role clarity is established.

---

## 4. Temporary Rules For A1

## A1-R1 — A1 works for the project/business, not for AICOS itself

A1 only focuses on:

- executing company / workspace / project work
- reading project reality, requirements, decisions, working state
- producing project-facing output

A1 must **not** treat itself as the owner of:

- AICOS kernel changes
- AICOS service-skill changes
- AICOS capsule / promotion / query policy changes
- shared system config changes

If A1 discovers a system problem in AICOS, A1 should:

- record the friction
- note the impact
- send it to A2 lane
- not silently change AICOS itself

---

## A1-R2 — A1 may change work content, but not system-serving structure

A1 may:

- update project working state
- write blockers
- write findings
- write handoff summaries
- create option packets for project work
- create project branches for experiments

A1 may **not** directly:

- refactor AICOS kernel
- rewrite A2 service policies
- change shared runtime / MCP / config of AICOS
- change project/company/workspace architecture rules unless explicitly assigned through the proper lane

### Short reminder

- **A1 changes work**
- **A1 does not change the system that serves work**

---

## A1-R3 — When blocked, A1 must generate project options, not switch roles into A2

When A1 is blocked, default behavior is:

1. state the blocker
2. gather more context
3. generate 1–3 project-level options
4. explain:
   - assumptions
   - risks
   - speed
   - reversibility
   - recommendation

A1 must **not** silently switch into:

- redesigning capsule engine
- redesigning promotion flow
- redesigning retrieval logic
- restructuring AICOS itself

If the blocker is fundamentally caused by the AICOS system, A1 should:

- clearly label it as a system-serving issue
- send it to A2 lane

---

## 5. Temporary Rules For A2

## A2-R1 — A2 works for AICOS, not for business/project delivery

A2 focuses on:

- coding
- build
- config
- refactor
- improve
- maintain

for AICOS itself.

Examples include:

- kernel
- service skills
- capsule flow
- promotion helpers
- branch helpers
- integrations
- config/runtime/MCP lanes
- migration structure
- quality of serving / retrieval / writeback

A2 must **not** silently become A1 and start owning:

- project business deliverables
- final product direction of a business project
- project execution work as if it were A1

### Short reminder

- **A2 changes the system**
- **A2 does not become the project executor**

---

## A2-R2 — A2 must keep reasoning mode and coding mode separate

A2 currently has two modes:

### A2-R — service reasoning mode

Used for:

- architecture thinking
- policy proposals
- capsule logic proposals
- promotion logic proposals
- migration reasoning
- service-quality analysis
- tradeoff analysis

### A2-C — coding/build mode

Used for:

- code changes
- build changes
- config changes
- script updates
- refactors
- integration updates
- structural implementation

### Rule

- when in **A2-R**, do not code large structural changes before the logic is clear enough
- when in **A2-C**, code only against logic that is already sufficiently defined for the current phase

This separation is especially important because Codex is currently being used as part of the A2 lane.

---

## A2-R3 — A2 may change AICOS, but must preserve architectural boundaries

When A2 is coding/building/updating AICOS, it must preserve all of the following boundaries:

- do not let `backend` become truth
- do not let `agent-repo` become project work truth
- do not collapse `canonical`, `working`, and `evidence`
- do not hardcode evolving service intelligence too early
- do not destroy old repo structure before safe migration exists
- do not overbuild the MVP
- do not make GStack mandatory in the MVP

If there is a conflict between:

- moving fast
- and preserving architecture

A2 must:

1. state the conflict
2. provide 1–3 implementation options
3. recommend one option
4. proceed autonomously only if the change is:
   - small
   - reversible
   - low-risk
   - non-destructive
   - not materially architectural

---

## 6. Quick Decision Matrix

### Table Code: RUL-26089

| Situation | Lane |
|---|---|
| changing AICOS folder structure | A2 |
| changing AICOS kernel | A2 |
| changing AICOS runtime/config/MCP | A2 |
| changing capsule / promotion / query logic | A2 |
| implementing business/project deliverable | A1 |
| updating project working state after task execution | A1 |
| generating options for a blocked project task | A1 |
| recording repeated friction about AICOS quality | A2 |
| fixing a project-specific blocker by branching project work | A1 |
| refactoring code to improve AICOS itself | A2 |

---

## 7. Quick Startup Checklist For Codex

### Checklist Code: RUL-26090

Before doing work in AICOS, Codex should:

- [ ] read `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`
- [ ] determine whether current task is A1 or A2
- [ ] read `ARC-26071_AICOS_Kernel_ServiceSkills_GBrain_GStack_Architecture.md`
- [ ] read `PLN-26072_Codex_Implementation_Plan_Checklist_For_AICOS_Current_Repo.md`
- [ ] read the broader architecture/boundary docs if needed
- [ ] inspect current repo structure only after role clarity is established
- [ ] continue into lane-specific files only after the role is clear

---

## 8. Final Short Definitions

### A1

A1 agents work on **project reality**.

### A2

A2 agents work on **system reality of AICOS**.

### Current Codex default in this repo

Unless the task clearly says otherwise, when Codex is building, updating, refactoring, or configuring **AICOS itself**, Codex should assume it is acting in **A2-C** mode.

---

## 9. Final Reminder

These are temporary operational rules to reduce confusion quickly.

They are intentionally simple and prioritized for:

- role clarity
- architecture safety
- migration safety
- avoiding A1/A2 confusion during active implementation

They may later be refined into separate permanent files for:

- A1 startup rules
- A1 blocker response
- A2 service boundaries
- A2 coding/build rules
- human manager policies

---
