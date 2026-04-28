# MAP-26031 — AICOS Brain vs AgentRepo vs Backend Read/Write Boundary

**Status:** draft-v1  
**Project:** AICOS  
**Date:** 2026-04-17  
**Purpose:** khóa lại boundary giữa `brain`, `agent-repo`, và `backend`, đồng thời làm rõ overlap giữa shared `working-rules` trong brain và operational `rules/tasks/queues` của A1/A2.

---

## 1. Executive Summary

Trong AICOS cần phân biệt rất rõ 3 lớp:

1. **AICOS Brain**  
   nơi giữ durable knowledge và source of truth theo domain company / workspace / project / service-knowledge

2. **AICOS AgentRepo**  
   nơi giữ operational setup của agents theo từng class như A1, A2, và sau này có thể là A3, A4...

3. **AICOS Backend**  
   serving substrate để query, index, search, rank, retrieve nhanh hơn; backend không phải truth layer

Boundary cốt lõi:

- **brain = knowledge truth**
- **agent-repo = cách agents vận hành**
- **backend = lớp phục vụ query/search**

---

## 2. Core Definitions

## 2.1. AICOS Brain

AICOS brain là knowledge layer.

### Chứa các loại nội dung như:

- company profile
- workspace current-state
- workspace working-rules
- project requirements
- project decisions
- architecture rationale
- sources-manifest
- handoffs / meetings có giá trị lâu dài
- service-knowledge đã đủ durable

### Bản chất

- durable
- reviewable
- provenance-sensitive
- có thể trở thành source of truth
- không phải runtime-local state

---

## 2.2. AICOS AgentRepo

AICOS agent-repo là operational layer của agents.

### Chứa các loại nội dung như:

- startup rules
- query rules
- writeback rules
- escalation rules
- MCP configs
- runtime configs
- env
- task queues
- current todo
- session logs
- heartbeat state
- per-agent memory
- class-specific jobs / cron / hooks

### Bản chất

- nói về cách agents hoạt động
- có thể transient hoặc semi-durable
- không phải business/project truth mặc định
- có thể thay đổi nhanh hơn brain

---

## 2.3. AICOS Backend

AICOS backend là serving layer.

### Chứa hoặc phục vụ các thứ như:

- indexes
- embeddings
- keyword search state
- vector search state
- ranking state
- query-serving state
- sync state

### Bản chất

- hỗ trợ query/search nhanh hơn
- không phải canonical source of truth
- không phải nơi nên coi là authority cuối cùng
- được refresh / sync từ brain và các ingestion flows

---

## 3. Boundary Rule

### Rule 1

Nếu nội dung mô tả **thế giới công việc** hoặc **truth của scope** thì nghiêng về **brain**.

### Rule 2

Nếu nội dung mô tả **cách agent vận hành** thì nghiêng về **agent-repo**.

### Rule 3

Nếu nội dung chỉ tồn tại để **phục vụ query/search/index** thì nghiêng về **backend**.

---

## 4. Shared Working Rules vs A1 Operational Rules

Đây là chỗ dễ nhầm nhất.

## 4.1. Shared Working Rules trong Brain

`working-rules` trong company / workspace / project brain là:

- shared truth
- governance truth
- rule của scope
- policy áp dụng cho con người và agents liên quan tới scope đó

### Ví dụ

- mọi thay đổi requirement phải qua review
- decision locked có precedence cao hơn report draft
- sources-manifest là nơi ghi representative source
- project X ưu tiên market US trước VN

### Kết luận

Đây là **luật của công việc**.

---

## 4.2. A1 Operational Rules trong AgentRepo

Rules của A1 là:

- cách A1 query context
- tool order
- escalation behavior
- writeback behavior
- startup sequence
- các operational constraints riêng của A1

### Ví dụ

- A1 phải query project context trước rồi mới query company context bổ sung
- A1 không được tự sửa canonical file
- nếu thiếu source rõ ràng, A1 phải tạo friction report thay vì tự kết luận
- khi task là implementation, A1 phải đọc requirements + decisions trước code

### Kết luận

Đây là **luật để A1 làm việc**.

---

## 4.3. Summary

`working-rules` trong brain là **shared truth của scope**.  
`rules` của A1 trong agent-repo là **operational rules của A1**.

Hai cái liên quan nhau nhưng không cùng tầng.

---

## 5. Where To Store What

### Table Code: MAP-26029

| Khu vực | Lưu cái gì |
|---|---|
| `brain/workspaces/...` | workspace truth, current-state, shared working-rules, source-of-truth policy, active context |
| `brain/projects/...` | project requirements, decisions, architecture rationale, active context, sources-manifest, durable handoffs |
| `agent-repo/classes/a1-.../rules/` | startup rules, query rules, writeback rules, escalation rules, tool usage rules của A1 |
| `agent-repo/classes/a1-.../tasks/` | current task list, task breakdown, current todo của A1 |
| `agent-repo/classes/a1-.../queues/` | backlog, retry queue, review queue local của A1 |
| `agent-repo/classes/a1-.../session-logs/` | log làm việc theo phiên của A1 |
| `agent-repo/classes/a1-.../heartbeat/` | heartbeat state, periodic status của A1 |
| `agent-repo/classes/a2-.../rules/` | service boundaries, maintenance rules, retrieval-improvement rules của A2 |
| `agent-repo/classes/a2-.../tasks/queues/...` | maintenance jobs, feedback synthesis work, reindex/review queues, session and runtime state của A2 |
| `backend/...` | indexes, embeddings, retrieval/search state, sync state |

---

## 6. MCP Config / Runtime Config / Env Belong To Which Agent Types?

### Answer

Các loại config này có thể tồn tại cho:

- A1
- A2
- và sau này A3, A4...

Nhưng **không được để chung một cục**.

### Recommended structure

```text
agent-repo/
  shared/
    mcp-shared/
    env-shared/
    tool-policies/

  classes/
    a1-work-agents/
      codex/
        mcp/
        env/
        runtime/
      claude/
        mcp/
        env/
        runtime/
      openclaw/
        mcp/
        env/
        runtime/

    a2-service-agents/
      ingest-agent/
        mcp/
        env/
        runtime/
      retrieval-agent/
        mcp/
        env/
        runtime/
      feedback-synth-agent/
        mcp/
        env/
        runtime/
```

### Rule

- shared only when truly shared
- otherwise classify by agent class
- ideally classify further by agent instance

---

## 7. Task Queue / Current Todo / Session Logs / Heartbeat State

Những thứ này có thể tồn tại cho cả A1 và A2.  
Chúng **phải tách riêng theo class**.

### Recommended structure

```text
agent-repo/
  classes/
    a1-work-agents/
      tasks/
      queues/
      session-logs/
      heartbeat/
      memory/

    a2-service-agents/
      tasks/
      queues/
      session-logs/
      heartbeat/
      memory/
```

### Meaning

- A1 task = business/project work
- A2 task = service/maintenance/improvement work

Không nên trộn chung.

---

## 8. Do A1 and A2 Read Raw Brain Files Directly?

### Short answer

**Không nên theo default.**

A1 và A2 không nên mặc định mở hàng loạt file markdown nguyên văn trong brain.

### Better default path

1. query qua backend/retrieval layer
2. lấy ranked snippets / candidate pages / context packet ngắn
3. chỉ khi cần verify sâu mới mở raw brain page

### Why

- tiết kiệm token
- tăng tốc
- giảm over-reading
- vẫn giữ được authority vì raw brain page luôn còn đó để verify

---

## 9. Brain vs Backend in Read Flow

## 9.1. Brain

- authority layer
- raw knowledge source
- canonical page source
- final verify source when needed

## 9.2. Backend

- default query path
- fast retrieval
- ranked search
- search serving
- snippet and context-packet support

### Key rule

Backend should be the **default read path**.  
Brain should remain the **authority and deep-verification path**.

---

## 10. Brain vs Backend in Write Flow

## 10.1. Durable knowledge write

Nếu thông tin là durable knowledge:

- write to `brain/` (or proposal flow leading to brain)

Examples:

- approved requirement clarification
- approved decision
- durable handoff summary
- durable service-quality note

## 10.2. Operational state write

Nếu thông tin là operational state:

- write to `agent-repo/`

Examples:

- current task
- retry queue state
- session log
- heartbeat
- runtime-local notes

## 10.3. Backend write

Backend có thể được:

- synced
- reindexed
- re-embedded
- refreshed

Nhưng không nên là “canonical truth write surface” chính.

---

## 11. A1 and A2 Read/Write Matrix

### Table Code: MAP-26030

| Agent class | Đọc mặc định từ đâu | Mở sâu khi nào | Ghi vào đâu |
|---|---|---|---|
| A1 | query qua backend để lấy context packet, snippets, ranked hits | khi cần verify raw source, audit decision, đọc full requirement/decision/source page | work truth vào `brain/`; task/session/queue vào `agent-repo/classes/a1-.../` |
| A2 | query qua backend để phân tích retrieval, source quality, service knowledge, feedback patterns | khi cần sửa page model, review canonical update, audit source lineage | durable service knowledge vào `brain/service-knowledge/`; maintenance/task/runtime state vào `agent-repo/classes/a2-.../` |

---

## 12. Recommended AICOS Structure

### Diagram Code: MAP-26027

```text
AICOS
├── brain/                         # durable knowledge, source of truth
│   ├── companies/
│   ├── workspaces/
│   ├── projects/
│   ├── meetings/
│   ├── handoffs/
│   ├── sources/
│   ├── concepts/
│   └── service-knowledge/
│
├── agent-repo/                    # operational layer
│   ├── shared/
│   └── classes/
│       ├── a1-work-agents/
│       │   ├── rules/
│       │   ├── tasks/
│       │   ├── queues/
│       │   ├── session-logs/
│       │   ├── heartbeat/
│       │   ├── mcp/
│       │   ├── env/
│       │   └── runtime/
│       │
│       ├── a2-service-agents/
│       │   ├── rules/
│       │   ├── tasks/
│       │   ├── queues/
│       │   ├── session-logs/
│       │   ├── heartbeat/
│       │   ├── mcp/
│       │   ├── env/
│       │   └── runtime/
│       │
│       └── a3-.../
│
└── backend/                       # serving substrate only
    ├── pglite/ or postgres/
    ├── indexes
    ├── embeddings
    └── search state
```

---

## 13. Final Rules To Remember

### Rule A

`brain` is not where A1/A2 should dump runtime state.

### Rule B

`agent-repo` is not where business/project truth should live by default.

### Rule C

`backend` is not the truth layer; it is the serving layer.

### Rule D

Shared `working-rules` in brain != operational rules of A1.

### Rule E

A1/A2 should usually read through backend first and only open raw brain pages when they need deep verification.

---

## 14. Final Short Definition

- **Brain** = truth and durable knowledge  
- **AgentRepo** = operational setup and state of agents  
- **Backend** = query/index/search substrate  
- **A1 rules** = how A1 works  
- **Brain working-rules** = rules of the work world

---
