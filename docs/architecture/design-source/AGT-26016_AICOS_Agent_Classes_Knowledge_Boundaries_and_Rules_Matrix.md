# AGT-26016 — AICOS Agent Classes, Knowledge Boundaries, and Rules Matrix

**Status:** draft-v1  
**Project:** AICOS  
**Purpose:** lưu chi tiết thiết kế phân lớp agents, knowledge, rules, boundaries, và interaction model cho AICOS  
**Date:** 2026-04-17

---

## 1. Executive Summary

AICOS nên được hiểu là một hệ thống work-brain dành cho:

- company knowledge
- workspace knowledge
- project knowledge
- requirements knowledge
- decisions knowledge
- handoff and meeting-derived knowledge

AICOS **không** nên được hiểu là một generic everything-brain.

AICOS cần phân biệt rất rõ 2 nhóm agents:

- **A1 — Work Agents / Project Agents**  
  các agents làm việc cho business, workspace, company, project

- **A2 — AICOS Service / Improvement Agents**  
  các agents phục vụ cho chính AICOS, giúp brain/search/query/schema/tools/retrieval tốt hơn cho A1

Điểm quan trọng nhất của thiết kế này là:

- A1 và A2 có **mục tiêu khác nhau**
- A1 và A2 cần **knowledge khác nhau**
- A1 và A2 phải obey một số shared truth chung
- nhưng A1 và A2 phải có **operational rules khác nhau**

Thiết kế đúng của AICOS là:

- **work knowledge** tách khỏi **service knowledge**
- **brain knowledge** tách khỏi **agent operational rules**
- **durable truth** tách khỏi **session/task/runtime state**
- **A1 agents work on the business**
- **A2 agents work on the brain that serves the business**

---

## 2. Design Background

Thiết kế này dựa trên một số boundary rất quan trọng rút ra từ cách tiếp cận của GBrain:

- markdown/repo knowledge là source of truth
- brain/retrieval layer không đồng nhất với knowledge tự thân
- agent operational behavior không được trộn lẫn với world/work knowledge
- cần tách:
  - brain knowledge
  - agent memory / operational memory
  - session context

Từ đó, AICOS không nên cố lưu "mọi thứ", mà nên chủ động giới hạn domain:

- company
- workspace
- projects
- requirements
- decisions
- meetings / handoffs
- trusted sources
- service-quality knowledge cho chính AICOS

---

## 3. Core Design Principle

### 3.1. Principle 1

**A1 agents work on the business. A2 agents work on the brain that serves the business.**

### 3.2. Principle 2

**A1 primarily consumes work knowledge. A2 primarily maintains service knowledge.**

### 3.3. Principle 3

**Both A1 and A2 obey shared workspace/company truth, but their operational rules are different.**

### 3.4. Principle 4

**No runtime config, task residue, or session-local artifact should silently become work knowledge.**

### 3.5. Principle 5

**AICOS brain should store durable work knowledge, not generic personal or operational noise.**

---

## 4. Agent Classes

## 4.1. A1 — Work Agents / Project Agents

A1 là các agents đang làm việc cho công ty, workspace, hoặc dự án.

### Typical examples

- Codex
- Claude
- OpenClaw-based agents
- code agents
- research agents
- PM/documentation agents
- workspace assistants
- project-scoped assistants

### Primary mission

- hiểu context công việc
- hiểu project scope
- hiểu requirements
- hiểu decisions
- hiểu sources
- thực hiện task
- trả feedback / delta / friction / proposal về hệ thống

### A1 is primarily

- work executor
- context consumer
- requirements consumer
- decision consumer
- source-grounded task performer

### A1 is not primarily

- schema designer
- retrieval optimizer
- embedding optimizer
- query-engine tuner
- canonical authority for system-wide truth changes

---

## 4.2. A2 — AICOS Service / Improvement Agents

A2 là các agents phục vụ cho chính AICOS.

### Typical examples

- ingestion optimizer
- embedding/retrieval optimizer
- query recipe improver
- schema/page-model improver
- feedback synthesizer
- source classification improver
- brain tooling improver
- system maintenance / self-service agents

### Primary mission

- giúp AICOS brain trả lời tốt hơn cho A1
- tối ưu query
- tối ưu retrieval
- tối ưu lưu trữ knowledge
- tổng hợp feedback từ A1
- đề xuất update cho company / workspace / working rules khi thật sự có cơ sở
- cải tiến tools và serving quality cho A1

### A2 is primarily

- knowledge system steward
- service optimizer
- schema/query/tooling improver
- feedback synthesizer
- improvement proposer

### A2 is not primarily

- final business authority
- direct owner of project direction
- silent promoter of truth
- unrestricted mutator of company/project truth

---

## 5. Main Difference Between A1 and A2

### A1 asks

- project này đang cần gì?
- task này đang bị constraint bởi rule nào?
- decision nào đã khóa?
- source nào authoritative?
- tôi cần context nào để làm việc đúng?

### A2 asks

- brain hiện phục vụ A1 tốt chưa?
- query có đủ chính xác chưa?
- retrieval có bị lệch không?
- source classification đã ổn chưa?
- schema/page model có cần sửa không?
- feedback nào đủ mạnh để đề xuất update rules/context?

### Core separation

- **A1 works on business reality**
- **A2 works on knowledge system quality**

---

## 6. Information Model: Three Main Layers

AICOS nên tách thông tin thành ít nhất 3 lớp.

## 6.1. Layer K1 — Work Knowledge

Đây là phần knowledge phục vụ business/work/project.

### Includes

- company profile
- org context
- workspace context
- workspace rules
- project profiles
- project requirements
- architecture decisions
- product decisions
- source manifests
- meeting summaries
- handoff knowledge
- glossary / concepts
- current best understanding of project/company/workspace truth

### Main consumers

- A1: very high
- A2: medium

### Nature

- durable
- reference-worthy
- provenance-sensitive
- should be searchable
- should support grounded work

---

## 6.2. Layer K2 — Service Knowledge

Đây là knowledge về chính hệ thống AICOS và chất lượng phục vụ của nó.

### Includes

- ingestion patterns
- retrieval quality findings
- query recipes
- source classification strategies
- schema conventions
- page model guidelines
- embedding quality notes
- search failure patterns
- answer quality observations
- feedback clusters from A1
- service decisions for improving AICOS

### Main consumers

- A1: low
- A2: very high

### Nature

- durable enough to retain
- useful for system improvement
- not primary business truth
- should not pollute A1 by default

---

## 6.3. Layer O — Operational / Runtime State

Đây là phần operational state, không nên trộn lẫn với work knowledge.

### Includes

- runtime configs
- MCP configs
- env vars
- launcher scripts
- approval policies
- sandbox settings
- task queues
- session notes
- runtime cache
- temporary work artifacts
- agent-specific execution instructions
- current transient assignment state

### Main consumers

- A1: medium or high depending on task
- A2: medium or high depending on maintenance task

### Nature

- often ephemeral
- tool/runtime-specific
- not durable truth by default
- should not be indexed into work knowledge blindly

---

## 7. Authority Model

AICOS nên có 4 authority tiers.

## 7.1. Tier 1 — Human / Company / Workspace Truth

Đây là authority cao nhất.

### Includes

- company policy
- workspace working rules
- approved project requirements
- approved project decisions
- approved source manifests
- approved active-context and current-state docs

### Applies to

- A1
- A2

---

## 7.2. Tier 2 — A1 Operational Rules

Rules riêng cho A1 agents.

### Includes

- how to query work knowledge
- when to ask for truth check
- when to escalate
- when to report delta
- when to propose rule/context update
- what A1 may never mutate directly

### Applies to

- A1 only

---

## 7.3. Tier 3 — A2 Operational Rules

Rules riêng cho A2 agents.

### Includes

- when to re-index or re-embed
- when to adjust retrieval behavior
- when to propose schema changes
- when a service agent may update derived layers
- when human review is required
- what A2 may never silently promote

### Applies to

- A2 only

---

## 7.4. Tier 4 — Session / Task State

### Includes

- current task
- task-local notes
- temporary problem framing
- current debugging state
- session continuity

### Rule

Tier 4 is never truth by default.

---

## 8. Agent Rules Must Be Different

## 8.1. A1 Rules

A1 should follow rules like:

- query work knowledge before guessing
- prioritize current requirements and decisions
- prioritize named authoritative sources
- do not directly mutate canonical truth
- send back delta, friction, and proposals
- report missing context instead of silently improvising
- stay scoped to assigned company / workspace / project boundaries
- do not optimize brain internals or change retrieval policy unless explicitly acting as A2

## 8.2. A2 Rules

A2 should follow rules like:

- improve service quality for A1, not abstract benchmark vanity
- analyze repeated failures and friction from A1
- improve ingestion, indexing, query recipes, and source classification
- maintain separation between work knowledge and service knowledge
- may update derived layers more freely than A1
- may propose updates to canonical rules and company/workspace context
- may not silently promote business truth or policy changes
- should optimize for groundedness, retrieval quality, explainability, and operator trust

---

## 9. Matrix: Agent Groups vs Mission

### Table Code: AGT-26013

| Nhóm agent | Vai trò chính | Mục tiêu chính | Đọc gì nhiều nhất | Ghi gì nhiều nhất | Không nên sở hữu |
|---|---|---|---|---|---|
| A1 — Work / Project Agents | thực thi công việc cho company/workspace/project | hoàn thành task đúng context, đúng requirement, đúng rule | company context, workspace context, project requirements, decisions, sources, active context | work delta, findings, task output, friction, rule/context proposals | knowledge model core, retrieval engine policy, embedding strategy |
| A2 — AICOS Service / Improvement Agents | bảo trì và cải tiến AICOS brain + serving quality | làm brain/query/tools tốt hơn cho A1 | schema conventions, source quality, retrieval failures, feedback logs, import quality, promotion backlog | index updates, feedback synthesis, improvement proposals, service metrics, structured maintenance outputs | business/project truth cuối cùng nếu chưa qua review |

---

## 10. Matrix: Information / Knowledge / Rules by Agent Group

### Table Code: AGT-26014

| Loại thông tin | Thuộc brain hay ops | A1 cần mức nào | A2 cần mức nào | Ghi chú |
|---|---|---|---|---|
| Company profile / org context | Brain | cao | trung bình | nền tảng cho mọi work task |
| Workspace working rules | Brain | cao | cao | shared truth cho cả A1 và A2 |
| Project requirements / PRD / scope | Brain | rất cao | trung bình | trọng tâm của A1 |
| Project decisions / architecture decisions | Brain | rất cao | trung bình | A1 phải bám chặt |
| Source manifests / provenance | Brain | cao | rất cao | A2 cần sâu hơn vì dùng để tối ưu trust/retrieval |
| Meeting summaries / handoff knowledge | Brain | cao | trung bình | A1 dùng để làm việc; A2 dùng gián tiếp |
| Query recipes / retrieval strategies | Service knowledge | thấp | rất cao | đây là kiến thức vận hành brain |
| Embedding / indexing quality notes | Service knowledge | rất thấp | rất cao | chỉ A2 cần sâu |
| Feedback clusters từ A1 | Service knowledge | thấp | rất cao | đầu vào cải tiến cho A2 |
| Runtime config / MCP wiring / env | Ops | thấp | cao | không nên là business truth |
| Agent escalation rules | Ops | cao | cao | nhưng rules khác nhau theo nhóm |
| Session task state / temporary todo | Ops | cao | cao | không promote vào brain nếu chưa cần |
| Proposal queue / review state | Ops + governance | trung bình | rất cao | A2 dùng nhiều hơn A1 |

---

## 11. What Goes Into AICOS Brain

AICOS brain chỉ nên lưu những loại knowledge đủ durable và đủ hữu ích cho grounded work.

### Should go into AICOS brain

- company profile
- workspace current-state
- workspace working-rules
- project requirements
- project active-context
- project decisions
- architecture rationale
- trusted sources manifests
- meeting summaries that matter
- handoff notes with durable value
- glossary / concepts
- service-knowledge related to retrieval/query/schema quality
- service decisions for improving AICOS

### Brain inclusion criteria

Một item nên vào AICOS brain nếu:

- nó có giá trị vượt quá 1 session
- nó giúp các agents làm việc tốt hơn trong tương lai
- nó có provenance hoặc có thể được review
- nó đại diện cho best-current-understanding
- nó thuộc company / workspace / project / service-knowledge domain

---

## 12. What Must Not Be Indexed As Work Knowledge

### Should not be blindly indexed

- MCP config
- runtime config
- launcher scripts
- env vars
- sandbox rules
- approval policies
- raw logs
- transient errors
- local machine residue
- temporary session scratchpads
- one-off debug outputs
- ephemeral task queue states
- personal noise outside work domain

### Rule

Nếu một item mô tả cách agent/runtime vận hành trong lúc này, thì thường nó là operational state, không phải work knowledge.

---

## 13. Work Knowledge vs Service Knowledge

## 13.1. Work Knowledge

Phục vụ business/project execution.

### Examples

- "Project A currently targets segment X."
- "Decision D-14 locked the naming convention."
- "Workspace uses source precedence A > B > C."
- "Requirement R-5 is mandatory for the MVP."

### Main user

- A1

## 13.2. Service Knowledge

Phục vụ cải tiến AICOS brain.

### Examples

- "Query recipe Q-3 performs poorly for requirement lookups."
- "Feedback cluster F-9 shows frequent ambiguity between current-state and old reports."
- "Meeting summaries need a stricter page template for retrieval quality."
- "Source manifests are under-maintained in project scopes."

### Main user

- A2

## 13.3. Key rule

Service knowledge should not dominate work-agent startup context by default.

---

## 14. Folder Tree Recommendation For AICOS Brain

### Tree Code: AGT-26015

```text
aicos-brain/
  companies/
    main-company/
      profile.md
      policies.md
      org-context.md

  workspaces/
    main/
      current-state.md
      working-rules.md
      source-of-truth.md
      active-context.md

  projects/
    aicos/
      requirements.md
      decisions.md
      architecture.md
      active-context.md
      sources-manifest.md

    sample-project/
      requirements.md
      decisions.md
      architecture.md
      active-context.md
      sources-manifest.md

  meetings/
  handoffs/
  concepts/
  sources/

  service-knowledge/
    brain-ops/
    retrieval-quality/
    source-classification/
    schema-conventions/
    query-recipes/
    feedback-synthesis/
    service-decisions/
```

### Notes

- `companies/`, `workspaces/`, `projects/` are part of work knowledge
- `service-knowledge/` is for A2-oriented durable knowledge
- operational agent configs should remain outside this brain tree
- not all meeting notes belong in brain; only those with durable work value

---

## 15. Recommended Operational Separation

AICOS nên có ít nhất 2 major zones:

### Zone 1 — Brain Zone

Contains:

- work knowledge
- service knowledge
- approved current-state
- decisions
- requirements
- trusted source references
- durable summaries

### Zone 2 — Agent / Ops Zone

Contains:

- AGENTS / runtime instructions
- MCP wiring
- launcher scripts
- runtime configs
- task state
- local env
- cron/jobs
- temporary operational memory

### Hard rule

Zone 2 may read from Zone 1.  
Zone 2 must not silently become Zone 1.

---

## 16. A1 ↔ A2 Interaction Model

### Standard loop

1. A1 receives a task
2. A1 queries AICOS brain for work context
3. A1 performs the task
4. A1 sends back:
   - delta
   - friction
   - missing context
   - proposals
5. A2 collects patterns across many A1 interactions
6. A2 determines whether the issue is caused by:
   - missing knowledge
   - stale knowledge
   - weak source classification
   - poor query recipe
   - poor schema/page model
   - missing or outdated rules
7. A2 produces:
   - service improvement
   - context proposal
   - rule proposal
   - source update proposal
8. human review or governance gate promotes what should become durable truth

### Key rule

A1 is not the optimizer of the system.  
A2 is not the final owner of business truth.

---

## 17. Promotion Rules

### A1 may directly create

- task outputs
- work findings
- context deltas
- friction reports
- rule proposals
- context update proposals

### A1 may not directly create as final truth

- approved company rule changes
- approved workspace rule changes
- approved project requirement changes
- approved final service policies

### A2 may directly create

- service-quality notes
- retrieval-quality findings
- query recipe proposals
- source classification proposals
- maintenance outputs
- improvement reports

### A2 may not directly promote as final truth

- company policy truth
- project requirement truth
- business direction truth
- authoritative working-rule changes without review

---

## 18. Startup Context Policy

## 18.1. A1 default startup context should include

- relevant company / workspace / project context
- relevant requirements
- relevant decisions
- relevant sources-manifest
- active-context
- only the minimum necessary rules

## 18.2. A2 default startup context should include

- service-knowledge relevant to current maintenance task
- feedback clusters
- retrieval / source classification notes
- applicable shared workspace/company truth
- strict mutation boundaries

## 18.3. Rule

A1 should not be overloaded with service-quality internals by default.  
A2 should not ignore business/work truth while optimizing the system.

---

## 19. Minimal Rule Sets To Create Later

AICOS should later formalize at least these rule documents:

### For shared truth

- company-shared-rules.md
- workspace-shared-rules.md
- source-of-truth-policy.md
- promotion-policy.md

### For A1

- a1-startup-rules.md
- a1-query-rules.md
- a1-writeback-rules.md
- a1-escalation-rules.md

### For A2

- a2-service-boundaries.md
- a2-retrieval-improvement-rules.md
- a2-proposal-rules.md
- a2-no-silent-promotion-rules.md

---

## 20. Anti-Drift Guardrails

### Drift risk 1

A1 starts carrying too much service internals.

**Guardrail:** keep A1 startup packs work-focused.

### Drift risk 2

A2 starts acting like final business authority.

**Guardrail:** no silent promotion of business truth.

### Drift risk 3

Operational configs get indexed as work knowledge.

**Guardrail:** explicit non-index list and separate ops zone.

### Drift risk 4

Service knowledge pollutes project truth.

**Guardrail:** keep `service-knowledge/` separate from `projects/`.

### Drift risk 5

Everything becomes “brain”.

**Guardrail:** require durable-value criteria before adding to brain.

---

## 21. Final Short Definition

### AICOS definition

AICOS is a work-brain system for company, workspace, and project knowledge, with a separate service-knowledge lane for maintaining and improving the brain itself.

### A1 definition

A1 agents do work for the business.

### A2 definition

A2 agents do work for the brain that serves the business.

---

## 22. Final Action Notes

The next practical step after this design is to turn it into 3 policy files:

1. `AICOS-AGENT-CLASSES.md`
2. `AICOS-KNOWLEDGE-BOUNDARIES.md`
3. `AICOS-RULES-MATRIX.md`

This current file is the unified design source that those files can later be derived from.

---
