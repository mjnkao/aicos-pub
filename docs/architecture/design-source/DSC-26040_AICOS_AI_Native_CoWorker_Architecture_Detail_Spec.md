# DSC-26040 — AICOS AI-Native Co-Worker Architecture Detailed Spec

**Status:** draft-v1  
**Project:** AICOS  
**Date:** 2026-04-17  
**Purpose:** lưu chi tiết thiết kế mới của AICOS theo mô hình company/workspace/team-native, trong đó humans và AI agents cùng làm việc như co-workers trên nhiều projects và nhiều experimental branches.

---

## 1. Executive Summary

AICOS không nên được thiết kế như một “brain cho một human”.

AICOS nên được thiết kế như một **company/workspace intelligence layer** nơi:

- nhiều humans cùng làm việc
- nhiều AI agents cùng làm việc
- nhiều projects cùng tồn tại
- mỗi project có thể có nhiều experimental branches
- humans đóng vai manager / team lead / reviewer / approver
- agents đóng vai team members / service operators / system improvers

Mục tiêu chính của AICOS là:

1. giữ **shared project reality** cho humans và agents
2. giảm việc agents phải đọc lại hàng loạt tài liệu mỗi lần đổi project
3. giúp agents có **controlled autonomy**
4. giúp agents khi gặp blocker có thể:
   - tự điều tra
   - tự sinh ra 1–N options / MVP branches
   - trình manager các options có giải thích, risk, tradeoff, recommendation
5. tách rất rõ:
   - canonical truth
   - working reality
   - execution state
   - branch / experiment state
   - serving / retrieval substrate
6. tận dụng GBrain ở nơi GBrain mạnh nhất:
   - retrieval
   - indexing
   - sync
   - hybrid search
   - compiled truth + timeline page model
   - backend abstraction, đặc biệt với Postgres

---

## 2. Why This New Design Is Needed

## 2.1. Current pain points

Trong mô hình agent hiện nay thường xảy ra các vấn đề:

- agent đổi project là mất context
- agent phải load lại rất nhiều tài liệu
- project có nhiều nhánh thử nghiệm thì context bị phân mảnh
- manager phải nhắc lại quá nhiều
- agent gặp blocker thì thường hỏi lại ngay, thay vì chủ động điều tra và sinh options
- nhiều hệ thống thiếu shared state giữa humans và agents

## 2.2. Root causes

Nguyên nhân không chỉ là prompt chưa tốt.

Các nguyên nhân sâu hơn thường là:

- chưa có project reality model rõ
- chưa có branch reality model rõ
- chưa có autonomy contract rõ cho agents
- chưa có capsule layer để nén context theo actor và task
- chưa tách đúng giữa truth, working state, execution state, và serving state

---

## 3. Core Design Principle

### 3.1. Principle 1

AICOS là **company/workspace intelligence layer**, không phải personal brain.

### 3.2. Principle 2

Humans và agents đều là co-workers trong cùng project reality, nhưng với quyền và trách nhiệm khác nhau.

### 3.3. Principle 3

Manager không nên là bottleneck cho mọi blocker nhỏ.  
Agents phải có autonomy có kiểm soát.

### 3.4. Principle 4

Mọi project cần có nhiều tầng reality:

- canonical
- working
- execution
- branch / experiment

### 3.5. Principle 5

Serving layer phải mạnh để:

- query nhanh
- giảm token
- giảm reread docs
- nhưng không được thay thế source of truth

### 3.6. Principle 6

AICOS phải đủ rõ ràng để sau này hỗ trợ thêm nhiều classes agents hơn A1, A2.

---

## 4. Actor Model

## 4.1. Human Manager / Team Lead

### Primary role

- giao mục tiêu
- chọn hướng
- chọn options / MVP paths khi cần
- approve promotions
- approve important decisions
- arbitrate tradeoffs
- review outputs của agents

### Human is not supposed to do

- lặp lại project context quá nhiều lần
- làm context relay thủ công cho mọi project
- giải quyết mọi blocker nhỏ giúp agent
- tự nhớ trạng thái của tất cả branches bằng tay

---

## 4.2. A1 — Work Agents / Project Execution Agents

### Primary role

A1 là các agents thực thi công việc cho company / workspace / project.

### Typical examples

- Codex
- Claude
- OpenClaw work agents
- implementation agents
- research agents
- PM support agents
- doc writing agents
- analysis agents

### Expected behavior

- nhận task
- tự gather context đủ dùng
- đọc project reality qua capsule
- làm việc
- nếu gặp blocker:
  - không dừng ngay để hỏi
  - mà phải tự điều tra thêm
  - sinh ra các options / branches / MVP directions
  - nêu assumptions, risks, costs, tradeoffs
  - recommend một hướng để manager chọn

### A1 should output

- deliverable
- findings
- blockers
- options
- recommendations
- writeback updates to working layer

---

## 4.3. A2 — AICOS Service / Improvement Agents

### Primary role

A2 là các agents phục vụ cho chính AICOS.

### Typical examples

- retrieval improvement agent
- indexing / embedding improvement agent
- query recipe improver
- source classification improver
- feedback synthesis agent
- capsule quality improver
- promotion hygiene agent
- branch comparison agent

### Expected behavior

- đọc repeated friction từ A1 và humans
- cải thiện serving quality
- cải thiện retrieval quality
- cải thiện schema / page model / folder organization
- cải thiện capsule generation
- cải thiện source classification
- đề xuất updates cho working rules, service policies, working reality

### A2 should output

- service improvements
- better query flows
- better capsules
- schema proposals
- source proposals
- promotion candidates
- maintenance artifacts

---

## 4.4. Future A3 / A4 / ...

AICOS phải mở cho nhiều agent classes hơn.

### Examples

- A3 — Review / QA agents
- A4 — Experiment orchestration agents
- A5 — Communication / reporting agents
- A6 — Deployment / ops agents

### Design requirement

Không hardcode kiến trúc chỉ cho A1 và A2.

---

## 5. Layer Model Of AICOS

AICOS nên có ít nhất 7 layers.

## 5.1. Layer A — Canonical Truth Layer

Đây là tầng đã duyệt, authoritative, stable.

### Contains

- company policy
- workspace shared working rules
- approved project requirements
- approved architecture
- approved decisions
- approved source manifests
- approved glossary / concepts
- approved final summaries

### Character

- authoritative
- review-gated
- low-churn relative to working layer
- long-lived
- provenance-sensitive

---

## 5.2. Layer B — Working Reality Layer

Đây là tầng dùng hàng ngày.

### Contains

- project current-state
- current implementation direction
- active known risks
- current milestones
- current open questions
- latest synthesized understanding
- current handoff state
- current roadmap interpretation

### Character

- medium-churn
- read often
- updated more frequently than canonical
- may later be promoted into canonical

---

## 5.3. Layer C — Evidence / Intake Layer

Đây là tầng raw material, imported material, candidate material.

### Contains

- raw meeting notes
- transcripts
- imported docs
- feedback bundles
- raw reports
- candidate observations
- proposed facts
- candidate requirement changes
- candidate source links

### Character

- high-churn
- noisy
- not trusted by default
- used for evidence, synthesis, promotion

---

## 5.4. Layer D — Execution State Layer

Đây là tầng task / queue / runtime / in-flight work.

### Contains

- tasks
- current todo
- backlog
- retry queues
- assignee state
- heartbeat
- job status
- session logs
- branch-local execution state
- open blockers
- option-generation jobs

### Character

- very high-churn
- operational
- not canonical truth
- often runtime- or agent-local

---

## 5.5. Layer E — Branch / Experiment Layer

Đây là tầng rất quan trọng và thường bị thiếu trong nhiều hệ.

### Contains

- branch identity
- branch purpose
- branch owner(s)
- parent branch / inherited state
- overrides vs main project reality
- branch-specific assumptions
- branch-specific decisions
- experimental outcomes
- comparison with other branches
- recommendation for manager

### Character

- experiment-aware
- branch-scoped
- sometimes short-lived
- extremely valuable for option generation

---

## 5.6. Layer F — Capsule Layer

Đây là layer để giảm token load và context reload.

### Contains

- company capsule
- workspace capsule
- project capsule
- branch capsule
- task capsule
- manager capsule
- A1 execution capsule
- A2 service capsule

### Character

- derived
- compressed
- actor-aware
- task-aware
- not a new truth layer
- served from canonical + working + evidence + branch state

---

## 5.7. Layer G — Serving / Retrieval Layer

Đây là layer dùng GBrain mạnh nhất.

### Contains / provides

- indexing
- sync
- hybrid search
- snippets
- ranking
- retrieval
- graph traversal
- embeddings
- context assembly helpers

### Character

- high performance
- query-oriented
- not canonical authority
- powered by backend engine

---

## 6. State Model

AICOS nên tổ chức theo **knowledge state**, không chỉ theo topic.

## 6.1. S1 — Canonical

### Meaning

Approved, authoritative, stable enough.

### Example artifacts

- approved requirements
- official architecture
- signed-off decisions
- approved working rules

---

## 6.2. S2 — Working

### Meaning

Current best working understanding, frequently used.

### Example artifacts

- current-state
- working summary
- active issues
- in-progress interpretation
- working handoff

---

## 6.3. S3 — Evidence

### Meaning

Raw or candidate evidence.

### Example artifacts

- transcripts
- notes
- imports
- raw analysis
- proposed updates

---

## 6.4. S4 — Execution

### Meaning

Task / queue / session / runtime activity.

### Example artifacts

- todo
- queue entries
- blockers
- retry jobs
- logs

---

## 6.5. S5 — Branch

### Meaning

Alternative path / experiment / variation / MVP option.

### Example artifacts

- branch hypotheses
- branch plans
- branch outcomes
- branch comparisons

---

## 7. Folder Structure — Top Level

### Diagram Code: DSC-26041

```text
AICOS/
├── brain/
├── agent-repo/
├── serving/
├── backend/
├── integrations/
├── scripts/
├── docs/
└── archive/
```

### Meaning

- `brain/` = durable and semi-durable knowledge
- `agent-repo/` = operational layer for humans and agents
- `serving/` = retrieval/capsule/query/promotion services
- `backend/` = engine, DB config, sync/index infra
- `integrations/` = connectors and runtime bindings
- `scripts/` = local automation utilities
- `docs/` = design, policies, review notes
- `archive/` = legacy or superseded material

---

## 8. Detailed Folder Structure — Brain

### Diagram Code: DSC-26042

```text
brain/
├── companies/
│   └── <company-id>/
│       ├── canonical/
│       │   ├── company-profile.md
│       │   ├── company-policies.md
│       │   ├── org-structure.md
│       │   ├── official-glossary.md
│       │   └── source-manifest.md
│       ├── working/
│       │   ├── current-state.md
│       │   ├── current-priorities.md
│       │   ├── current-risks.md
│       │   ├── open-questions.md
│       │   └── working-summary.md
│       └── evidence/
│           ├── imported-docs/
│           ├── meeting-notes/
│           ├── raw-observations/
│           └── candidate-updates/
│
├── workspaces/
│   └── <workspace-id>/
│       ├── canonical/
│       │   ├── workspace-profile.md
│       │   ├── working-rules.md
│       │   ├── source-of-truth-policy.md
│       │   ├── promotion-policy.md
│       │   └── workspace-glossary.md
│       ├── working/
│       │   ├── current-state.md
│       │   ├── active-projects-summary.md
│       │   ├── current-risks.md
│       │   ├── active-questions.md
│       │   └── manager-dashboard-summary.md
│       └── evidence/
│           ├── imported-docs/
│           ├── notes/
│           ├── snapshots/
│           └── candidate-summaries/
│
├── projects/
│   └── <project-id>/
│       ├── canonical/
│       │   ├── project-profile.md
│       │   ├── requirements.md
│       │   ├── architecture.md
│       │   ├── decisions.md
│       │   ├── source-manifest.md
│       │   ├── glossary.md
│       │   └── project-working-rules.md
│       ├── working/
│       │   ├── current-state.md
│       │   ├── current-direction.md
│       │   ├── active-risks.md
│       │   ├── open-questions.md
│       │   ├── handoff-summary.md
│       │   ├── current-milestones.md
│       │   └── synthesis-log.md
│       ├── evidence/
│       │   ├── meetings/
│       │   ├── imports/
│       │   ├── raw-analysis/
│       │   ├── candidate-facts/
│       │   ├── candidate-decisions/
│       │   └── candidate-requirement-updates/
│       └── branches/
│           └── <branch-id>/
│               ├── branch-profile.md
│               ├── inherited-context.md
│               ├── overrides.md
│               ├── assumptions.md
│               ├── experiments-run.md
│               ├── findings.md
│               ├── recommendation.md
│               └── compare-to-main.md
│
├── shared/
│   ├── concepts/
│   ├── sources/
│   ├── meetings/
│   └── handoffs/
│
└── service-knowledge/
    ├── canonical/
    │   ├── service-policies.md
    │   ├── approved-query-patterns.md
    │   ├── approved-schema-conventions.md
    │   └── approved-source-classification-rules.md
    ├── working/
    │   ├── retrieval-quality-summary.md
    │   ├── capsule-quality-summary.md
    │   ├── repeated-friction-clusters.md
    │   ├── service-open-questions.md
    │   └── proposed-improvements.md
    └── evidence/
        ├── raw-feedback/
        ├── retrieval-failure-cases/
        ├── source-quality-reviews/
        └── candidate-service-updates/
```

---

## 9. Explanation Of Brain Folders

## 9.1. `companies/<company-id>/canonical/`

Lưu các tài liệu chính thức cấp công ty.

### Important files

- `company-profile.md`
- `company-policies.md`
- `org-structure.md`
- `official-glossary.md`
- `source-manifest.md`

### Use cases

- A1 cần hiểu công ty đang là gì
- A2 cần biết boundary chung để không tối ưu sai hướng
- humans review/approve chính sách

---

## 9.2. `workspaces/<workspace-id>/canonical/`

Lưu shared truth của workspace/team.

### Important files

- `workspace-profile.md`
- `working-rules.md`
- `source-of-truth-policy.md`
- `promotion-policy.md`
- `workspace-glossary.md`

### Notes

Đây là nơi chứa **shared working rules** của workspace, không phải operational rules riêng cho A1/A2.

---

## 9.3. `projects/<project-id>/canonical/`

Lưu truth đã chốt của dự án.

### Important files

- `project-profile.md`
- `requirements.md`
- `architecture.md`
- `decisions.md`
- `source-manifest.md`
- `glossary.md`
- `project-working-rules.md`

### Notes

- `project-working-rules.md` = shared truth của dự án
- không phải runtime rules của agents

---

## 9.4. `projects/<project-id>/working/`

Lưu reality đang dùng hàng ngày.

### Important files

- `current-state.md`
- `current-direction.md`
- `active-risks.md`
- `open-questions.md`
- `handoff-summary.md`
- `current-milestones.md`
- `synthesis-log.md`

### Notes

Đây là nơi A1 và human manager đọc rất thường xuyên.

---

## 9.5. `projects/<project-id>/evidence/`

Lưu evidence và candidate material.

### Important subfolders

- `meetings/`
- `imports/`
- `raw-analysis/`
- `candidate-facts/`
- `candidate-decisions/`
- `candidate-requirement-updates/`

### Notes

Đây là input cho synthesis và promotion.

---

## 9.6. `projects/<project-id>/branches/<branch-id>/`

Lưu reality của từng experimental branch.

### Important files

- `branch-profile.md`
- `inherited-context.md`
- `overrides.md`
- `assumptions.md`
- `experiments-run.md`
- `findings.md`
- `recommendation.md`
- `compare-to-main.md`

### Why this matters

Khi agent bị blocker và rẽ nhánh thử nghiệm, mọi thứ phải được giữ thành branch reality, không bị lẫn với project main reality.

---

## 9.7. `service-knowledge/`

Đây là knowledge dành cho A2 và cho việc cải tiến AICOS.

### Important files in `canonical/`

- `service-policies.md`
- `approved-query-patterns.md`
- `approved-schema-conventions.md`
- `approved-source-classification-rules.md`

### Important files in `working/`

- `retrieval-quality-summary.md`
- `capsule-quality-summary.md`
- `repeated-friction-clusters.md`
- `service-open-questions.md`
- `proposed-improvements.md`

### Important folders in `evidence/`

- `raw-feedback/`
- `retrieval-failure-cases/`
- `source-quality-reviews/`
- `candidate-service-updates/`

---

## 10. Detailed Folder Structure — Agent Repo

### Diagram Code: DSC-26043

```text
agent-repo/
├── shared/
│   ├── shared-access-rules/
│   │   ├── source-of-truth-access.md
│   │   ├── write-lane-policy.md
│   │   └── scope-resolution-policy.md
│   ├── shared-promotion-rules/
│   │   ├── evidence-to-working-policy.md
│   │   ├── working-to-canonical-policy.md
│   │   └── review-required-cases.md
│   ├── shared-tool-policies/
│   │   ├── tool-usage-policy.md
│   │   ├── query-policy.md
│   │   └── safety-boundaries.md
│   └── capsule-policies/
│       ├── capsule-schema.md
│       ├── capsule-freshness-policy.md
│       └── capsule-priority-policy.md
│
├── classes/
│   ├── a1-work-agents/
│   │   ├── rules/
│   │   │   ├── startup-rules.md
│   │   │   ├── autonomy-contract.md
│   │   │   ├── blocker-response-policy.md
│   │   │   ├── option-generation-policy.md
│   │   │   ├── writeback-rules.md
│   │   │   └── escalation-rules.md
│   │   ├── tasks/
│   │   │   ├── current/
│   │   │   ├── backlog/
│   │   │   ├── blocked/
│   │   │   └── completed/
│   │   ├── queues/
│   │   │   ├── assignment-queue/
│   │   │   ├── retry-queue/
│   │   │   ├── proposal-queue/
│   │   │   └── branch-option-queue/
│   │   ├── session-logs/
│   │   ├── heartbeat/
│   │   ├── mcp/
│   │   ├── runtime/
│   │   ├── memory/
│   │   └── capsules/
│   │       ├── company/
│   │       ├── workspace/
│   │       ├── project/
│   │       ├── branch/
│   │       └── task/
│   │
│   ├── a2-service-agents/
│   │   ├── rules/
│   │   │   ├── startup-rules.md
│   │   │   ├── service-boundaries.md
│   │   │   ├── improvement-policy.md
│   │   │   ├── no-silent-promotion-policy.md
│   │   │   ├── service-writeback-rules.md
│   │   │   └── escalation-rules.md
│   │   ├── tasks/
│   │   │   ├── current/
│   │   │   ├── backlog/
│   │   │   ├── blocked/
│   │   │   └── completed/
│   │   ├── queues/
│   │   │   ├── feedback-intake-queue/
│   │   │   ├── retrieval-review-queue/
│   │   │   ├── source-classification-queue/
│   │   │   ├── promotion-candidate-queue/
│   │   │   └── capsule-quality-queue/
│   │   ├── session-logs/
│   │   ├── heartbeat/
│   │   ├── mcp/
│   │   ├── runtime/
│   │   ├── memory/
│   │   └── capsules/
│   │       ├── service/
│   │       ├── company/
│   │       ├── workspace/
│   │       └── project/
│   │
│   ├── humans/
│   │   ├── role-policies/
│   │   │   ├── manager-role.md
│   │   │   ├── reviewer-role.md
│   │   │   └── approver-role.md
│   │   ├── review-queues/
│   │   ├── approvals/
│   │   ├── dashboards/
│   │   └── capsules/
│   │       ├── company/
│   │       ├── workspace/
│   │       ├── project/
│   │       └── branch/
│   │
│   └── a3-template/
│       ├── rules/
│       ├── tasks/
│       ├── queues/
│       ├── session-logs/
│       ├── heartbeat/
│       ├── mcp/
│       ├── runtime/
│       ├── memory/
│       └── capsules/
│
└── instances/
    ├── a1/
    │   ├── codex-main/
    │   ├── claude-main/
    │   └── openclaw-worker-1/
    ├── a2/
    │   ├── retrieval-agent-1/
    │   ├── capsule-agent-1/
    │   └── feedback-agent-1/
    └── humans/
        ├── manager-min/
        └── reviewer-...
```

---

## 11. Explanation Of Agent Repo Folders

## 11.1. `shared/`

Lưu policies dùng chung.

### Important subfolders

- `shared-access-rules/`
- `shared-promotion-rules/`
- `shared-tool-policies/`
- `capsule-policies/`

### Notes

Đây là chỗ dùng chung cho mọi actors, nhưng không nên nhồi các policies class-specific vào đây.

---

## 11.2. `classes/a1-work-agents/`

Lưu contract chung cho class A1.

### Important files in `rules/`

- `startup-rules.md`
- `autonomy-contract.md`
- `blocker-response-policy.md`
- `option-generation-policy.md`
- `writeback-rules.md`
- `escalation-rules.md`

### Meaning

Đây là operational rules của A1, khác với `working-rules` trong workspace/project brain.

---

## 11.3. `classes/a2-service-agents/`

Lưu contract chung cho class A2.

### Important files in `rules/`

- `startup-rules.md`
- `service-boundaries.md`
- `improvement-policy.md`
- `no-silent-promotion-policy.md`
- `service-writeback-rules.md`
- `escalation-rules.md`

### Meaning

A2 cần rules riêng vì role của nó là cải thiện AICOS, không phải trực tiếp quyết định truth của business/project.

---

## 11.4. `classes/humans/`

Lưu role policies và review/approval flows cho humans.

### Important subfolders

- `role-policies/`
- `review-queues/`
- `approvals/`
- `dashboards/`
- `capsules/`

### Meaning

Humans là first-class actors trong AICOS, không chỉ là external operator.

---

## 11.5. `instances/`

Lưu phân chia theo instance cụ thể.

### Why needed

- Codex-main và Claude-main cùng là A1 nhưng không phải cùng một instance
- Retrieval-agent-1 và capsule-agent-1 cùng là A2 nhưng có behavior và ownership khác nhau

### Notes

Thiết kế cần tách được:
- class-level policies
- instance-level runtime setup

---

## 12. Detailed Folder Structure — Serving Layer

### Diagram Code: DSC-26044

```text
serving/
├── query/
│   ├── project-query/
│   ├── workspace-query/
│   ├── company-query/
│   └── service-query/
│
├── capsules/
│   ├── company/
│   ├── workspace/
│   ├── project/
│   ├── branch/
│   ├── task/
│   ├── manager/
│   ├── a1/
│   └── a2/
│
├── promotion/
│   ├── evidence-to-working/
│   ├── working-to-canonical/
│   └── review-packets/
│
├── branching/
│   ├── branch-create/
│   ├── branch-compare/
│   ├── branch-summary/
│   └── option-packets/
│
├── truth/
│   ├── source-resolution/
│   ├── conflict-check/
│   ├── precedence/
│   └── lineage/
│
└── feedback/
    ├── a1-feedback/
    ├── a2-feedback/
    ├── manager-feedback/
    └── synthesis/
```

---

## 13. Explanation Of Serving Layer

## 13.1. `query/`

Là các query services theo scope.

### Important services

- `project-query/`
- `workspace-query/`
- `company-query/`
- `service-query/`

### Meaning

Không phải mọi query đều giống nhau.  
Query cho project work khác query cho service maintenance.

---

## 13.2. `capsules/`

Đây là layer rất quan trọng.

### Capsule types

- company
- workspace
- project
- branch
- task
- manager
- a1
- a2

### Why capsules matter

Capsules là context package nén, actor-aware, task-aware.  
Chúng giúp giảm việc phải load lại nhiều tài liệu thô.

---

## 13.3. `promotion/`

Quản lý flow promotion giữa các states.

### Important services

- `evidence-to-working/`
- `working-to-canonical/`
- `review-packets/`

### Meaning

Promotion không nên làm thủ công hoàn toàn nếu muốn AI-native hơn, nhưng cũng không được silent.

---

## 13.4. `branching/`

Quản lý branch intelligence.

### Important services

- `branch-create/`
- `branch-compare/`
- `branch-summary/`
- `option-packets/`

### Meaning

Đây là phần hỗ trợ agents khi gặp blocker phải rẽ nhiều hướng và trình manager options rõ ràng.

---

## 13.5. `truth/`

Quản lý source resolution, precedence, lineage.

### Important services

- `source-resolution/`
- `conflict-check/`
- `precedence/`
- `lineage/`

### Meaning

Giúp agents và humans biết cái nào authoritative hơn khi có conflict.

---

## 13.6. `feedback/`

Gom feedback từ các actor classes.

### Important services

- `a1-feedback/`
- `a2-feedback/`
- `manager-feedback/`
- `synthesis/`

### Meaning

A2 sẽ dùng layer này để cải thiện AICOS.

---

## 14. Detailed Folder Structure — Backend

### Diagram Code: DSC-26045

```text
backend/
├── engine/
│   ├── pglite/
│   └── postgres/
├── indexes/
│   ├── keyword/
│   ├── vector/
│   ├── graph/
│   └── hybrid/
├── sync/
│   ├── brain-sync/
│   ├── service-knowledge-sync/
│   └── branch-sync/
├── embeddings/
│   ├── models/
│   ├── jobs/
│   └── quality-checks/
├── health/
│   ├── engine-health/
│   ├── sync-health/
│   ├── index-health/
│   └── retrieval-health/
└── migrations/
```

### Notes

- backend là serving substrate
- backend không phải truth layer
- backend có thể dùng mạnh Postgres nếu muốn multi-user / company-scale hơn

---

## 15. Read / Write Model By Actor

## 15.1. Human Manager

### Reads

- manager capsule
- project capsule
- branch capsule
- workspace current-state
- decision-needed packets

### Writes

- approvals
- selections between options
- canonical promotions
- manager comments / priorities

---

## 15.2. A1 Work Agents

### Reads by default

- A1 execution capsule
- project capsule
- branch capsule nếu task nằm trong branch
- relevant snippets qua serving layer

### Reads more deeply when needed

- canonical requirements
- canonical decisions
- canonical architecture
- working current-state
- evidence linked to current blocker

### Writes

- working layer updates
- task execution state
- blockers
- generated options
- branch results
- deliverables
- recommendations

---

## 15.3. A2 Service Agents

### Reads by default

- A2 service capsule
- service-knowledge working layer
- repeated friction
- retrieval failure cases
- source quality reviews
- capsule quality summaries

### Reads more deeply when needed

- canonical service policies
- canonical project/workspace truth impacted by improvements
- raw evidence for source audits

### Writes

- service working layer updates
- maintenance tasks
- retrieval improvement proposals
- capsule improvements
- promotion candidates
- backend refresh actions

---

## 16. Autonomy Contract

AICOS cần formalize autonomy contracts.

## 16.1. Allowed autonomy

Agents có thể tự:

- gather evidence
- run checks
- produce drafts
- generate reversible MVP options
- synthesize risks
- recommend one option

## 16.2. Must-escalate conditions

Agents phải escalate khi:

- action is destructive
- action is irreversible
- external cost / exposure rises materially
- policy conflict exists
- canonical conflicts are unresolved
- strategic direction would change

## 16.3. Blocker default response

Khi gặp blocker, default không phải “ask manager immediately”.

Default nên là:

1. state blocker
2. gather more context
3. create options
4. mark assumptions
5. estimate speed/risk/reversibility
6. recommend one option
7. present decision packet to manager

---

## 17. Option Packet Structure

### File code: DSC-26046

Mỗi option packet nên có:

- option title
- goal
- why this branch exists
- assumptions
- what changes
- expected benefit
- risks
- cost / speed
- reversibility
- MVP scope
- evidence references
- recommended choice
- manager decision needed

---

## 18. Capsule Structure

### File code: DSC-26047

## 18.1. Manager Capsule

Should include:

- project identity
- current objective
- current working state
- top blockers
- active branches
- options needing decision
- top risks
- next likely choices

## 18.2. A1 Execution Capsule

Should include:

- relevant scope
- relevant requirements
- relevant decisions
- relevant working state
- active branch if any
- writeback lane
- autonomy contract summary
- blocker response rules

## 18.3. A2 Service Capsule

Should include:

- service goals
- current friction clusters
- current retrieval issues
- open source quality issues
- open capsule quality issues
- service writeback lane
- no-silent-promotion rules

## 18.4. Branch Capsule

Should include:

- branch identity
- parent branch / project
- branch purpose
- inherited context
- overrides
- assumptions
- experiments run
- findings
- recommendation
- compare-to-main
- compare-to-sibling-branches

---

## 19. Promotion Flow

## 19.1. Evidence -> Working

When:

- raw material has been synthesized enough
- repeated evidence converges
- a candidate update becomes useful for daily work

## 19.2. Working -> Canonical

When:

- reviewed
- approved
- provenance is adequate
- manager or authorized reviewer accepts it

## 19.3. Rule

No actor should silently skip promotion layers.

---

## 20. Example Project Layout

### Diagram Code: DSC-26048

```text
brain/projects/project-alpha/
├── canonical/
│   ├── project-profile.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── decisions.md
│   ├── source-manifest.md
│   └── project-working-rules.md
├── working/
│   ├── current-state.md
│   ├── current-direction.md
│   ├── active-risks.md
│   ├── open-questions.md
│   ├── handoff-summary.md
│   └── synthesis-log.md
├── evidence/
│   ├── meetings/
│   ├── imports/
│   ├── raw-analysis/
│   └── candidate-facts/
└── branches/
    ├── branch-mvp-fast/
    │   ├── branch-profile.md
    │   ├── inherited-context.md
    │   ├── overrides.md
    │   ├── assumptions.md
    │   ├── findings.md
    │   ├── recommendation.md
    │   └── compare-to-main.md
    └── branch-quality-first/
        ├── branch-profile.md
        ├── inherited-context.md
        ├── overrides.md
        ├── assumptions.md
        ├── findings.md
        ├── recommendation.md
        └── compare-to-main.md
```

---

## 21. Why This Design Still Reuses GBrain Well

AICOS vẫn tận dụng rất tốt GBrain ở các điểm:

- brain as durable knowledge repo
- retrieval/indexing/search/sync
- compiled truth + timeline
- backend abstraction
- service recipes / skill thinking

Nhưng AICOS không ép GBrain làm:

- company operating system hoàn chỉnh
- task queue system chính
- approval engine nhiều bước
- authoritative execution-state DB

---

## 22. What Should Stay Outside GBrain-Native Brain

Những phần sau không nên ép vào brain như truth layer mặc định:

- live task queues
- transient heartbeat
- runtime-local logs
- raw session scratchpads
- fast-changing job execution state
- low-level MCP/env/runtime config

Những thứ này nên ở `agent-repo/` hoặc systems chuyên biệt hơn.

---

## 23. Final Summary

AICOS mới nên được hiểu là:

- company/team-native
- multi-human
- multi-agent
- multi-project
- branch-aware
- capsule-driven
- promotion-aware
- strongly served by GBrain
- but not reduced to GBrain's original default framing

AICOS should become the shared intelligence layer that lets humans manage many projects while agents act more like real co-workers.

---

## 24. Suggested Next Files To Create Later

1. `DSC-26049_AICOS_Capsule_Spec.md`
2. `DSC-26050_AICOS_Autonomy_Contract_Spec.md`
3. `DSC-26051_AICOS_Promotion_and_Review_Flow.md`
4. `DSC-26052_AICOS_Project_and_Branch_Reality_Model.md`

---
