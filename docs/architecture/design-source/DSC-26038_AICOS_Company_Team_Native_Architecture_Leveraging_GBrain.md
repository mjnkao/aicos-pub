# DSC-26038 — AICOS Company/Team-Native Architecture Leveraging GBrain

**Status:** draft-v1  
**Project:** AICOS  
**Date:** 2026-04-17  
**Purpose:** thiết kế lại AICOS theo thực thể company/team/workspace/project, vẫn học hỏi và tận dụng được thế mạnh của GBrain.

---

## 1. Executive Summary

GBrain gốc rất mạnh cho mô hình:

- một human
- nhiều agents phục vụ human đó
- một brain repo chứa world knowledge / personal-context-like knowledge
- một agent repo chứa config, skills, tasks, memory, cron, runtime operations

AICOS lại khác:

- thực thể chính là **company / workspace / team**
- trong đó có **nhiều humans**
- có **nhiều agents**
- có **nhiều projects**
- mỗi project có cả:
  - tầng tài liệu đã chốt / approved / source of truth
  - tầng tài liệu working / current state / hằng ngày
  - tầng task / queue / ongoing execution state

Do đó AICOS **không nên copy nguyên structure thinking của GBrain**, nhưng nên giữ lại các điểm rất mạnh của GBrain:

- brain repo vs agent repo boundary
- backend engine abstraction
- retrieval/search/sync layer
- page pattern kiểu compiled truth + timeline
- skill-oriented workflows

Kết luận:

> AICOS nên là một **company/team-native knowledge system** với:
> - 3 tầng knowledge state: `canonical`, `working`, `evidence`
> - 1 tầng agent control phân class rõ ràng
> - 1 serving layer dùng GBrain làm retrieval engine

---

## 2. Why AICOS Is Different From Original GBrain Framing

## 2.1. GBrain default framing

GBrain được tối ưu tốt cho mô hình:

- one human
- world knowledge around that human
- agent repo containing the operations of agents serving that human
- brain repo as permanent record

## 2.2. AICOS framing

AICOS cần mô hình:

- company as primary entity
- workspace/team as collaboration entity
- many humans
- many agents
- many projects
- layered knowledge states
- shared rules and approvals
- current project execution state

### Meaning

AICOS is not a personal brain.  
AICOS is a multi-human, multi-agent, multi-project work-brain.

---

## 3. What To Reuse From GBrain

### Table Code: DSC-26033

| Phần của GBrain | Mức độ reuse | Lý do |
|---|---:|---|
| `brain repo vs agent repo` boundary | rất cao | đúng với AICOS, chỉ cần mở rộng sang multi-human/multi-agent |
| `BrainEngine` abstraction | rất cao | hợp để chạy Postgres/self-hosted cho team |
| `compiled truth + timeline` page pattern | cao | rất hợp cho company/project knowledge có lịch sử thay đổi |
| hybrid retrieval / sync / search layer | rất cao | AICOS cần đúng thứ này để giảm token và tăng groundedness |
| skills/recipes cho query, ingest, maintain, enrich | cao | đặc biệt hữu ích cho A2 service agents |

---

## 4. What Not To Copy As-Is

### Table Code: DSC-26034

| Phần của GBrain | Không nên copy nguyên | Vì sao |
|---|---|---|
| ontology mặc định kiểu personal brain | đúng | AICOS không phải “one human world model” |
| assumption “agent repo của một human” | đúng | AICOS cần agent repo theo class/team/project |
| dùng brain làm nơi chứa mọi task/queue/transient ops | đúng | AICOS có current work state rất cao-churn, cần tách tốt hơn |
| xem markdown brain là nơi duy nhất chứa mọi transactional state | đúng | project queues/approval workflows/concurrency thường cần hệ chuyên hơn |

---

## 5. Five-Layer Architecture For AICOS

## 5.1. Layer 1 — Canonical Knowledge Layer

Đây là tầng “đã duyệt / đã chốt / source of truth”.

### Examples

- company policy
- workspace working rules
- approved project requirements
- approved decisions
- approved architecture state
- approved source manifests

### Notes

Đây là phần nên áp dụng mạnh pattern compiled truth + timeline.

---

## 5.2. Layer 2 — Working Knowledge Layer

Đây là tầng “dùng hàng ngày”, gần current reality, nhưng chưa chắc đều đã canonicalized hoàn toàn.

### Examples

- project current state
- daily working summaries
- current implementation direction
- current risks
- handoff state
- working project context

### Notes

Layer này vẫn là knowledge, nhưng là knowledge đang vận hành.

---

## 5.3. Layer 3 — Evidence / Intake Layer

Đây là tầng raw material và input để review/summarize/promote.

### Examples

- meeting transcripts
- raw notes
- imports
- external docs
- feedback bundles
- proposed updates
- raw observations

---

## 5.4. Layer 4 — Agent Control Layer

Đây là operational side.

### Examples

- A1 rules
- A2 rules
- MCP config
- runtime config
- queues
- task states
- session logs
- heartbeat
- jobs / cron
- hooks
- memory

---

## 5.5. Layer 5 — Serving / Retrieval Layer

Đây là lớp GBrain mạnh nhất.

### Examples

- sync
- hybrid search
- ranking
- indexing
- embeddings
- backend search serving
- context packet support

### Notes

Serving layer is not truth.  
It is the substrate that helps agents retrieve truth efficiently.

---

## 6. AICOS Knowledge Must Be Organized By State

AICOS không nên chỉ tổ chức theo topic.  
Nó nên tổ chức theo **knowledge state**.

## 6.1. State S1 — Approved / Canonical

### Includes

- signed-off requirements
- approved architecture
- official decisions
- official working rules
- verified source manifests

## 6.2. State S2 — Working / Current

### Includes

- current project status
- working summaries
- in-progress design understanding
- active risk register
- current handoff state

## 6.3. State S3 — Evidence / Intake

### Includes

- raw meeting notes
- imported docs
- feedback bundles
- drafts
- external evidence
- candidate facts

### Rule

Promotion path should usually be:

`evidence -> working -> canonical`

---

## 7. New AICOS Brain Structure

### Diagram Code: DSC-26035

```text
aicos-brain/
  companies/
    <company-id>/
      canonical/
      working/
      evidence/

  workspaces/
    <workspace-id>/
      canonical/
      working/
      evidence/

  projects/
    <project-id>/
      canonical/
      working/
      evidence/

  shared/
    concepts/
    sources/
    meetings/
    handoffs/

  service-knowledge/
    canonical/
    working/
    evidence/
```

### Meaning

- `canonical/` = approved truth
- `working/` = current working knowledge
- `evidence/` = raw/proposed/input material
- `service-knowledge/` = durable knowledge for AICOS self-improvement

---

## 8. New AICOS Agent Layer

### Diagram Code: DSC-26036

```text
aicos-agent/
  shared/
    shared-access-rules/
    shared-promotion-rules/
    shared-tool-policies/

  classes/
    a1-work-agents/
      rules/
      tasks/
      queues/
      session-logs/
      heartbeat/
      mcp/
      runtime/
      memory/

    a2-service-agents/
      rules/
      tasks/
      queues/
      session-logs/
      heartbeat/
      mcp/
      runtime/
      memory/

    humans/
      role-policies/
      review-queues/
      approvals/
```

### Why `humans/` should exist

Humans are first-class operators in AICOS.  
They are not merely external reviewers.

---

## 9. A1, A2, and Human Roles

## 9.1. A1 — Work Agents

### Mission

- work on business/project tasks
- read company/workspace/project context
- use canonical and working knowledge
- produce outputs
- report delta/friction/proposals

## 9.2. A2 — Service Agents

### Mission

- improve AICOS brain/service quality
- improve retrieval/search/query/schema/source classification
- synthesize repeated feedback from A1
- propose rules/context/service updates

## 9.3. Humans

### Mission

- approve promotions
- approve shared rules
- approve important project truth changes
- arbitrate ambiguous or high-stakes updates

---

## 10. Read/Write Model

## 10.1. A1 Read Flow

A1 should typically:

1. query serving layer / backend
2. receive context packet / snippets / ranked hits
3. open raw canonical or working pages only when deeper verification is needed

### A1 writes to:

- `brain/.../working/` for durable working knowledge or proposals
- `aicos-agent/classes/a1-.../` for tasks, queues, sessions, heartbeat, runtime state

## 10.2. A2 Read Flow

A2 should typically:

1. query serving layer / backend
2. inspect service-knowledge and feedback patterns
3. open raw pages when auditing source truth or schema impact

### A2 writes to:

- `brain/service-knowledge/...` for durable service improvements
- `aicos-agent/classes/a2-.../` for maintenance tasks, jobs, session state
- serving layer refresh actions such as sync/reindex/re-embed

## 10.3. Human Read/Write Role

Humans should:

- review candidate promotions
- compare canonical vs working vs evidence
- approve or reject changes
- update policy when needed

---

## 11. AICOS Brain vs AICOS Agent vs AICOS Backend

### Table Code: DSC-26037

| Lớp | Vai trò | Có dùng GBrain không |
|---|---|---|
| AICOS Brain — Canonical | truth đã duyệt | dùng mạnh |
| AICOS Brain — Working | current working knowledge | dùng mạnh |
| AICOS Brain — Evidence | intake/raw/proposals | dùng được, nhưng nên có kiểm soát |
| AICOS Agent Layer | rules/tasks/queues/session theo class A1/A2/human | không nên nhét vào GBrain index |
| AICOS Serving Layer | query/sync/search/rank/index | dùng GBrain rất mạnh |
| Task/Workflow DB riêng | live queues, approvals, project current ops | nên dùng hệ riêng nếu nhu cầu cao |

---

## 12. Where GBrain Fits Best

GBrain nên đóng vai trò:

- brain/retrieval engine
- sync/index/search/query layer
- Postgres-backed serving substrate
- hybrid retrieval layer
- skills substrate cho query / ingest / maintain / enrich

GBrain không nên bị ép làm:

- full task queue system
- approval workflow system chính
- transactional operating system cho project execution
- complete company operating system

---

## 13. When To Use Separate Systems Instead Of GBrain

Nếu AICOS cần quản lý mạnh các phần sau:

- live task queue
- assignee states
- retries
- workflow approvals nhiều bước
- SLA / workflow state
- transaction-heavy project current state

thì nên dùng một system riêng như:

- project/task DB
- workflow DB
- kanban/task system
- approval system

rồi chỉ sync summary hoặc approved/promoted state vào AICOS brain.

---

## 14. Final Design Principle

### Principle 1

AICOS is not a personal brain.  
It is a company/team-native work-brain.

### Principle 2

AICOS knowledge should be organized by both:

- scope
- state

### Principle 3

AICOS must separate:

- canonical knowledge
- working knowledge
- evidence
- agent control
- serving/backend

### Principle 4

GBrain should be reused strongly as the serving/retrieval substrate, not stretched into a full company operating system.

---

## 15. Final Short Definition

AICOS is a company/team-native knowledge system with:

- 3 knowledge states: `canonical`, `working`, `evidence`
- class-based agent control for A1, A2, and humans
- a serving layer powered by GBrain
- clear promotion paths from working/evidence into canonical truth

---
