# ARC-26071 — AICOS Kernel / Service Skills / GBrain / GStack Architecture

**Status:** draft-v1  
**Project:** AICOS  
**Date:** 2026-04-17  
**Purpose:** khóa kiến trúc mới của AICOS theo hướng AI-native co-worker system, với phân tách rõ giữa `AICOS Kernel`, `A2 Service Skills`, `GBrain`, và `GStack`, đồng thời mô tả cách áp dụng kiến trúc này lên repo `aicos` hiện tại.

---

## 1. Executive Summary

AICOS không nên được hiểu là một “brain cho một human”.

AICOS nên được hiểu là một **company/workspace intelligence layer** nơi:

- nhiều humans cùng làm việc
- nhiều AI agents cùng làm việc
- nhiều projects cùng tồn tại
- mỗi project có thể có nhiều branches / experiments
- human đóng vai manager / team lead / reviewer / approver
- agents đóng vai co-workers

Kiến trúc mới của AICOS cần giải 4 bài toán lõi:

1. **Shared project reality**  
   humans và agents cùng nhìn vào cùng một project reality

2. **Controlled autonomy**  
   agents không hỏi lại manager quá sớm; khi blocked phải sinh options / MVP paths

3. **Multi-project switching**  
   manager và agents không phải reload quá nhiều context mỗi lần đổi project

4. **Branch-aware work**  
   project có thể rẽ nhiều nhánh thử nghiệm mà không làm mất coherence của shared reality

Để làm điều đó, AICOS cần:

- một lớp truth và knowledge rõ ràng
- một lớp branch / experiment reality
- một lớp capsule để giảm token load
- một lớp actor contracts cho human, A1, A2
- một lớp serving/retrieval mạnh
- một lớp deterministic kernel đủ nhỏ
- và một lớp service skills đủ “sống” để tự tiến hóa theo thời gian

---

## 2. Core Architectural Decision

### 2.1. Use GBrain as substrate

AICOS dùng **GBrain** làm nền cho:

- repo-as-truth
- retrieval
- indexing
- sync
- MCP / CLI access
- backend abstraction
- compiled truth + timeline style pages

### 2.2. Do not hardcode evolving intelligence too early

Những logic thay đổi theo thời gian như:

- scope resolution
- capsule building policy
- option generation policy
- promotion recommendation policy
- branch comparison policy

không nên bị đóng cứng sớm thành deterministic code.

### 2.3. Split AICOS into two internal layers

AICOS phải tách thành:

- **AICOS Kernel**  
  phần deterministic, stable, structural

- **AICOS Service Skills**  
  phần evolving intelligence, do A2 service agents sử dụng và cải tiến theo thời gian

### 2.4. Use GStack only when A2 is doing coding work

GStack không phải dependency bắt buộc cho mọi tác vụ A2.

GStack chỉ nên được gọi khi A2 chuyển từ:

- service reasoning / service policy / service synthesis

sang:

- coding / refactoring / generating scripts / modifying AICOS codebase

---

## 3. Primary Components

Kiến trúc mới của AICOS có 4 khối chính:

1. **GBrain**
2. **AICOS Kernel**
3. **A2 Service Skills**
4. **GStack (optional execution backend for coding work)**

### 3.1. GBrain

Vai trò:

- knowledge substrate
- retrieval engine
- sync/index/search layer
- MCP / CLI interface to brain content
- backend abstraction via engine layer
- source-of-truth repository convention

### 3.2. AICOS Kernel

Vai trò:

- define stable structure
- define schemas and contracts
- define deterministic packet formats
- define promotion primitives
- define actor / lane boundaries
- adapt repo layout
- wrap GBrain for AICOS-specific workflows

### 3.3. A2 Service Skills

Vai trò:

- resolve scope
- build capsules
- compare branches
- generate options
- synthesize blockers
- recommend promotions
- improve query behavior
- improve retrieval quality
- update service-knowledge

### 3.4. GStack

Vai trò:

- coding workflow execution
- only when an agent is actually modifying code/scripts/tools
- not the first-line substrate for service reasoning

---

## 4. What Each Component Owns

### Table Code: ARC-26073

| Component | Owns | Does Not Own |
|---|---|---|
| GBrain | retrieval, indexing, sync, search, serving substrate | actor contracts, project reality logic, option policies |
| AICOS Kernel | schemas, contracts, lanes, packet renderers, validators, stable folder model | high-level evolving service reasoning |
| A2 Service Skills | capsule policies, branch compare logic, option generation logic, promotion recommendation, service improvement | final hard authority over canonical truth, backend engine implementation |
| GStack | code modification workflows, refactors, test/update scripts, coding execution | shared truth model, project reality model, serving substrate |

---

## 5. Layer Model

AICOS nên có ít nhất 7 layers.

## 5.1. Layer A — Canonical Truth

- approved company truth
- approved workspace truth
- approved project truth
- approved source manifests
- approved decisions
- approved architecture

## 5.2. Layer B — Working Reality

- project current-state
- current direction
- active risks
- handoff state
- current milestones
- current synthesized understanding

## 5.3. Layer C — Evidence / Intake

- imported docs
- notes
- transcripts
- candidate facts
- candidate updates
- raw analysis

## 5.4. Layer D — Execution State

- tasks
- queues
- retries
- session logs
- heartbeat
- assignment state
- open blockers

## 5.5. Layer E — Branch / Experiment Reality

- branch identity
- inherited state
- overrides
- assumptions
- findings
- experiments run
- recommendation
- compare-to-main

## 5.6. Layer F — Capsule Layer

- manager capsule
- A1 execution capsule
- A2 service capsule
- project capsule
- branch capsule
- task capsule

## 5.7. Layer G — Serving Layer

- retrieval
- ranking
- query
- sync
- snippets
- graph traversal
- promotion support
- capsule support

---

## 6. Actor Model

## 6.1. Humans

Roles:

- manager
- reviewer
- approver
- team lead

Responsibilities:

- set priorities
- choose between options
- approve promotions
- resolve high-stakes conflicts
- arbitrate tradeoffs

## 6.2. A1 Work Agents

Responsibilities:

- execute project work
- read project/workspace/company reality
- use capsules
- when blocked, generate 1–N viable options
- write working updates and blockers
- deliver recommendations

## 6.3. A2 Service Agents

Responsibilities:

- improve AICOS itself
- improve capsules
- improve retrieval/query
- improve service-knowledge
- synthesize repeated friction
- recommend updates to rules and structures
- call GStack only when code must change

## 6.4. Future A3/A4

Architecture must allow future agent classes.

---

## 7. A2 Must Be Split Into Two Modes

### 7.1. A2-R — Service Reasoner

A2-R handles:

- scope resolution
- capsule policy
- branch reasoning
- option generation
- promotion recommendation
- source ambiguity reasoning
- service-quality analysis

A2-R uses:

- GBrain
- AICOS service skills
- AICOS kernel

A2-R does **not** require GStack by default.

### 7.2. A2-C — Service Engineer

A2-C handles:

- modifying capsule renderer code
- updating scripts
- refactoring kernel helpers
- adding CLI commands
- changing validators
- building adapters
- test/update loops

A2-C uses:

- GBrain for context
- GStack for coding workflow

---

## 8. AICOS Kernel: What Must Be Code

Phần sau nên là deterministic code trong kernel.

### 8.1. Structural contracts

- folder contracts
- state lane contracts
- actor lane contracts
- packet schemas
- promotion packet schema
- option packet schema
- capsule schema

### 8.2. Validators

- branch packet validation
- capsule validation
- promotion packet validation
- write-lane validation
- required field validation

### 8.3. GBrain adapter

- query wrapper
- search wrapper
- snippet wrapper
- sync wrapper
- page lookup wrapper
- service helper wrappers

### 8.4. Read/write primitives

- evidence write primitives
- working write primitives
- canonical promotion primitives
- queue item write primitives
- review packet write primitives

### 8.5. Minimal CLI

- build capsule
- compare branches
- generate option packet
- promote state
- validate paths
- sync brain

---

## 9. A2 Service Skills: What Should Stay Flexible

Phần sau không nên hardcode sớm thành code logic cứng.

### 9.1. Scope resolution policy

- project inference
- workspace inference
- branch inference
- context prioritization

### 9.2. Capsule assembly policy

- what to include
- how compact to make it
- what to omit by actor type
- freshness logic
- escalation when ambiguity is high

### 9.3. Branch comparison policy

- what dimensions to compare
- how to weight speed vs risk vs reversibility
- what counts as meaningful divergence

### 9.4. Option generation policy

- how many options to create
- when to stop exploring
- what a viable MVP branch looks like
- recommendation strategy

### 9.5. Promotion recommendation policy

- when evidence is enough
- when working state should be promoted
- what conflicts block promotion
- what must go to human review

### 9.6. Retrieval improvement policy

- where search is failing
- where source manifests are weak
- where summaries are too long or too stale
- where capsules underperform

---

## 10. Recommended Repo Shape For New Architecture

### Diagram Code: ARC-26074

```text
AICOS/
├── apps/
│   ├── control/                    # optional later; not required in MVP
│   └── dashboard/                  # optional later; not required in MVP
│
├── packages/
│   ├── aicos-kernel/
│   │   ├── contracts/
│   │   ├── schemas/
│   │   ├── validators/
│   │   ├── packet-renderers/
│   │   ├── promotion-primitives/
│   │   ├── write-lanes/
│   │   └── gbrain-adapter/
│   │
│   ├── project-reality/
│   ├── service-reality/
│   ├── branching/
│   ├── capsules/
│   └── actor-contracts/
│
├── brain/
│   ├── companies/
│   ├── workspaces/
│   ├── projects/
│   ├── shared/
│   └── service-knowledge/
│
├── agent-repo/
│   ├── shared/
│   ├── classes/
│   │   ├── a1-work-agents/
│   │   ├── a2-service-agents/
│   │   ├── humans/
│   │   └── a3-template/
│   └── instances/
│
├── serving/
│   ├── query/
│   ├── capsules/
│   ├── promotion/
│   ├── branching/
│   ├── truth/
│   └── feedback/
│
├── backend/
│   ├── engine/
│   ├── indexes/
│   ├── sync/
│   ├── embeddings/
│   ├── health/
│   └── migrations/
│
├── integrations/
│   ├── codex/
│   ├── claude-code/
│   ├── openclaw/
│   ├── chatgpt-sync/
│   └── claude-chat-sync/
│
├── scripts/
├── docs/
└── archive/
```

---

## 11. How This Maps To The Current `aicos` Repo

Repo `aicos` hiện tại đang có các khối như:

- `canonical/`
- `brains/`
- `gateway/`
- `bridges/`
- `reports/`
- `backup/`
- `scripts/`

Kiến trúc mới không nên xóa ngay những thứ này.

### Recommended migration interpretation

- `canonical/` -> migrate dần vào `brain/.../canonical` và `brain/.../working`
- `brains/` -> dùng như current GBrain-facing material trong giai đoạn chuyển tiếp
- `gateway/` -> phần deterministic nên di chuyển dần vào `packages/aicos-kernel/` hoặc `serving/`
- `bridges/` -> migrate vào `integrations/` + `agent-repo/classes/.../mcp`
- `reports/` -> chia lại thành:
  - `brain/.../evidence`
  - `agent-repo/.../queues`
  - `serving/feedback`
- `backup/` -> giữ nguyên là reference lane
- `scripts/` -> giữ lại nhưng dần quy về AICOS kernel commands

---

## 12. Practical CTO Rule

### Rule 1

Use code for:
- stability
- validation
- boundaries
- packet formats
- safe write lanes

### Rule 2

Use A2 service skills for:
- reasoning
- policy
- synthesis
- evolving heuristics
- capsule quality
- recommendation quality

### Rule 3

Use GStack only for:
- code change
- script change
- refactor
- engineering actions

### Rule 4

Do not hardcode logic too early if it is expected to evolve.

---

## 13. Example Workflows

## 13.1. A1 blocked on a project

1. A1 queries project capsule
2. A1 queries branch capsule if branch exists
3. A1 inspects relevant snippets and current blockers
4. A1 invokes option generation skill
5. A1 produces 2–3 options
6. A1 writes blocker + option packet
7. human manager selects option
8. selected option updates branch reality or execution state

## 13.2. A2 improving capsule quality

1. A2 reads service-knowledge working summaries
2. A2 reads repeated friction clusters
3. A2 tests improved capsule composition via service skills
4. A2 proposes update to capsule policy
5. if only policy changes -> update service knowledge
6. if code change is needed -> escalate to A2-C and use GStack

## 13.3. A2 needs code change

1. A2-R determines that a code change is needed
2. creates engineering packet
3. A2-C reads engineering packet + context
4. A2-C uses GStack to modify code
5. tests / validates
6. writes results back to working state + service-knowledge
7. promotion/review follows normal path

---

## 14. Final Definition

### AICOS Kernel

The deterministic structural layer of AICOS.

### A2 Service Skills

The evolving intelligence layer of AICOS.

### GBrain

The knowledge and retrieval substrate.

### GStack

The optional coding workflow engine used when agents must actually modify code.

---

## 15. Suggested Next Files

1. `CTO-26070_A2_Service_Reasoner_vs_A2_Service_Engineer_GBrain_GStack_Split.md`
2. `DSC-26049_AICOS_Capsule_Spec.md`
3. `DSC-26050_AICOS_Autonomy_Contract_Spec.md`
4. `PLN-26072_Codex_Implementation_Plan_Checklist_For_AICOS_Current_Repo.md`

---
