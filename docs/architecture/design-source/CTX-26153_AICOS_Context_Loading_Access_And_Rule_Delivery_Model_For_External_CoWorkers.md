# CTX-26153 — AICOS Context Loading, Access, and Rule Delivery Model For External Co-Workers

**Status:** working-design-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** hướng dẫn Codex triển khai mô hình loading context phù hợp cho AICOS, trong đó AICOS **không can thiệp và không quyết định cách Codex / Claude Code / OpenClaw quản lý context nội bộ**, mà chỉ cung cấp đúng thông tin, rules, và access paths cần thiết cho co-workers khi làm việc trong một project cụ thể.

---

## 1. Mục tiêu của mô hình này

AICOS cần giải bài toán sau:

- trong một project lớn có rất nhiều rules, policy, docs, state, backlog, risks, branch, evidence
- nếu co-worker phải load tất cả mọi thứ cùng lúc thì context sẽ quá lớn
- nhưng nếu không được cung cấp đủ thông tin thì co-worker sẽ làm sai hướng, lẫn rule, hoặc mất state

### Kết luận

AICOS không nên cố “quản lý trí nhớ” của Codex, Claude Code, OpenClaw, hay các co-worker khác.

Thay vào đó, AICOS nên:

- cung cấp **đúng context tối thiểu cần thiết**
- cung cấp **đúng rules cần thiết**
- cung cấp **đúng access path** để co-worker có thể:
  - tra cứu
  - hỏi lại
  - truy vấn
  - load sâu hơn khi cần

### Cách hiểu ngắn

AICOS làm giống như một công ty hoặc team:

- khi một human hoặc agent vào project, họ được cấp:
  - role
  - rules
  - current state
  - task packet
  - đường dẫn để tra cứu thêm

AICOS **không** quyết định người đó nhớ bằng cách nào ở trong đầu hay trong tool nội bộ của họ.

---

## 2. Current Repo State That This Model Must Respect

The current repo already has the following real state:

- `aicos option choose` đã được triển khai như một command first-class để commit manager/human choice từ chat vào AICOS state.
- `aicos sync brain` đã được nâng từ preflight placeholder thành MVP serving refresh dùng GBrain/PGLite cho `brain/`.
- policy pack gần đây đã được normalize vào canonical/working/evidence/A2 lanes thay vì chỉ để ở docs rời.
- `AGENTS.md` hiện đã chuyển sang incremental reading và yêu cầu A2 đọc self-brain trước raw repo.
- self-brain của AICOS đã tồn tại dưới `brain/projects/aicos/` và đã có canonical/working state đủ dùng cho startup context.

Mô hình context loading mới phải kế thừa trạng thái này, không phá nó.

---

## 3. Nguyên tắc kiến trúc phải chốt

## 3.1. Principle 1 — External co-workers own their internal context behavior

Codex, Claude Code, OpenClaw, ChatGPT, Claude chat, và các co-workers khác có cách quản lý context nội bộ riêng của chúng.

AICOS:

- không nên can thiệp sâu vào memory internals của chúng
- không nên giả định có thể kiểm soát context window nội bộ của chúng
- không nên ép chúng dùng cùng một cơ chế context persistence

### Rule

AICOS chỉ chịu trách nhiệm về:

- what to provide
- when to provide
- where to provide it from
- how to label it
- how to let agents ask for more when needed

---

## 3.2. Principle 2 — AICOS serves context, not total memory control

AICOS nên được hiểu là:

- context source
- rules source
- truth source
- retrieval/source-of-access layer
- state writeback destination

AICOS không phải là:

- manager of Codex internal memory
- manager of Claude Code internal context window
- manager of OpenClaw internal chat history

---

## 3.3. Principle 3 — Co-workers should receive onboarding-like packets

Mỗi co-worker khi vào task/project nên được cấp kiểu:

- role card
- current state
- current direction
- task packet
- rules to load
- access paths for deeper lookup

Đây giống onboarding/context handoff, không phải raw dump toàn bộ docs.

---

## 4. Context Loading Model: Packet-First, Not Document-First

AICOS nên chuyển từ:

- document-first loading

sang:

- packet-first loading

### 4.1. Document-first loading là gì

- đọc hàng loạt docs dài
- đọc nhiều policy/rule files
- đọc raw repo rộng
- tự cố reconstruct mental model từ quá nhiều nguồn

### 4.2. Packet-first loading là gì

Co-worker bắt đầu bằng một số packet ngắn:

- role card
- current state
- current direction
- task packet
- rule cards liên quan
- access paths

Rồi chỉ khi có trigger mới load sâu thêm.

### Câu chốt

AICOS không nên bắt agent “đọc cả thư viện trước khi làm việc”.  
AICOS nên cho agent một “packet vào việc” trước.

---

## 5. Bốn tầng context nên dùng

## 5.1. Hot Context

Đây là context luôn cần để bắt đầu task.

### Ví dụ

- role identity
- lane hiện tại
- current state tóm tắt
- current direction
- active task packet

### Properties

- rất ngắn
- startup-critical
- phải load nhanh
- phải dễ scan

---

## 5.2. Warm Context

Đây là context chỉ load khi task thật sự liên quan.

### Ví dụ

- writeback policy
- idea capture policy
- option choose flow
- sync brain flow
- migration status
- active risks chi tiết hơn

### Properties

- không cần load mọi lúc
- load theo task trigger
- có giá trị thực dụng ngay cho task

---

## 5.3. Cold Context

Đây là context chỉ load khi cần đào sâu.

### Ví dụ

- architecture docs dài
- review packs
- implementation notes chi tiết
- evidence docs
- source references

### Properties

- không startup-load
- chỉ load on-demand
- thường là provenance/reference

---

## 5.4. Frozen Context

Đây là context không load mặc định.

### Ví dụ

- legacy backup
- superseded docs
- old branches
- old imports
- old logs

### Properties

- chỉ đọc khi task migration/provenance/comparison cần
- không được override active direction

---

## 6. Ba lớp rule loading

AICOS không nên để agent load toàn bộ policy pack cùng lúc.

## 6.1. Identity Rules

Trả lời:

- tôi là A1 hay A2?
- A2-Core hay A2-Serve?
- lane của tôi là gì?
- tôi đang sửa AICOS hay đang làm project work?

### Startup relevance

Đây là lớp phải load đầu tiên.

---

## 6.2. Mode Rules

Trả lời:

- tôi đang ở interactive hay async?
- khi nào ghi state?
- khi nào chỉ ghi session/runtime?
- khi nào sync?
- khi nào route thành open question / backlog / risk?

### Startup relevance

Chỉ load khi bắt đầu thực thi thật.

---

## 6.3. Domain / Task Rules

Trả lời:

- task này liên quan option choose?
- task này liên quan sync brain?
- task này liên quan self-brain update?
- task này liên quan migration?
- task này liên quan service skill hay kernel?

### Startup relevance

Chỉ load theo task trigger.

---

## 7. AICOS Must Provide, Not Force

AICOS nên cung cấp các thứ sau cho co-worker.

## 7.1. Role Card

Một bản cực ngắn nói:

- actor là ai
- lane nào
- doing what
- not doing what

### Example

- A2-Core-C
- đang sửa AICOS itself
- không làm A1 project delivery
- phải đọc self-brain trước raw repo

---

## 7.2. Current State Packet

Một packet ngắn nói:

- project/system đang ở trạng thái nào
- active root gồm gì
- flow đã chứng minh được gì
- selected direction hiện tại là gì
- phần nào chưa active

---

## 7.3. Current Direction Packet

Một packet ngắn nói:

- đang ưu tiên cái gì
- cố tình chưa làm cái gì
- next execution nên đi hướng nào

---

## 7.4. Task Packet

Task packet nên có ít nhất:

- objective
- actor
- scope
- task type
- likely touched lanes/files
- required_context
- rules_to_load
- expected writeback lanes
- success condition

### Important field

`rules_to_load` là field rất quan trọng.  
Nếu không có field này, agent dễ đi load quá nhiều.

---

## 7.5. Rule Cards

Thay vì chỉ có full specs dài, AICOS nên cung cấp rule cards ngắn cho:

- role clarity
- writeback
- idea capture
- option choose
- sync brain

---

## 7.6. Access Paths

AICOS cũng phải nói rõ:

- nếu thiếu context thì query ở đâu
- nếu cần đào sâu thì đọc file nào tiếp
- nếu cần evidence thì vào lane nào
- nếu cần backup reference thì vào đâu

---

## 8. What AICOS Must Not Do

AICOS must not attempt to:

- control Codex internal context window
- control Claude Code internal memory strategy
- control OpenClaw internal chat memory
- assume every co-worker loads docs the same way
- require every co-worker to preload all project rules

### Instead

AICOS should:

- provide the right starting packet
- provide the right on-demand lookup path
- provide the right rules when the task triggers them

---

## 9. Required Loading Flow For A2-Core

Given the current repo state, A2-Core should use this loading model.

## 9.1. Step 1 — Load hot context only

Load:

- role card
- current state
- current direction
- current task packet

### In repo terms

This should come from a very small number of startup-critical files, not the full docs library.

## 9.2. Step 2 — Decide task type

Before loading more, determine:

- is this a writeback task?
- is this an option choose task?
- is this a sync task?
- is this a migration task?
- is this a kernel task?
- is this a self-brain summary task?

## 9.3. Step 3 — Load only triggered rule cards

Examples:

- if task is writeback-related -> load writeback rule card
- if task is option selection related -> load option choose rule card
- if task is sync-related -> load sync brain rule card
- if task concerns new ideas -> load idea-capture rule card

## 9.4. Step 4 — Load deep references only if needed

Only then inspect:

- architecture working summary
- review packs
- implementation details
- legacy backup references

---

## 10. Proposed AICOS Artifacts For Context Delivery

Codex should implement or normalize the following artifacts.

### 10.1. Startup cards

Very short files or generated packets for:

- A2-Core startup
- future A2-Serve startup
- future A1 startup

### 10.2. Rule cards

Very short files or generated packets for:

- writeback
- idea capture
- option choose
- sync brain

### 10.3. Task packet contract

A small schema or template that includes:

- actor
- scope
- task_type
- required_context
- rules_to_load
- allowed_write_lanes
- success_condition

### 10.4. Optional resolver helpers

Over time, AICOS may provide helpers like:

- `aicos context start <actor> <scope>`
- `aicos context task <task-id>`
- `aicos rules resolve <actor> <task-type>`

### Important note

Do not overbuild these as a large system immediately.  
Phase them in only as thin helpers or minimal packet generators.

---

## 11. Relationship With Current Repo State

The current repo already contains relevant structure to support this model.

### Already present

- self-brain under `brain/projects/aicos/`
- canonical role definitions
- project working rules
- current state
- current direction
- active risks
- open questions
- architecture working summary
- implementation status
- migration status
- A2 rules and backlog lanes
- option choose and sync brain MVP command surface
- AGENTS.md with incremental reading and self-brain-first direction

### What is still missing or not yet explicit enough

- explicit startup cards
- explicit rule cards
- explicit task packet contract
- explicit “rules_to_load” behavior
- explicit statement that AICOS serves context but does not own external runtime memory behavior

---

## 12. Key clarification to add to repo policies

Codex should add or normalize a clear statement like this into the appropriate repo lane:

> AICOS does not manage the internal memory or context mechanism of Codex, Claude Code, OpenClaw, or other co-workers.
>
> AICOS provides the correct role, rules, state summaries, task packets, and lookup paths for the current project/task.
>
> Co-workers remain free to manage their own internal context according to their own runtime/tool behavior.
>
> The contract is:
> - AICOS provides what should be known
> - AICOS labels what is authoritative
> - AICOS provides how to look up more
> - AICOS records meaningful state transitions
> - Co-workers decide how to hold that information internally

This point is essential and should be visible in a startup-critical or architecture-critical lane.

---

## 13. Concrete implementation tasks for Codex

### Checklist Code: CTX-26154

- [ ] review current startup-critical files and identify what is already acting as hot context
- [ ] define a minimal A2-Core startup card
- [ ] define minimal rule cards for writeback / idea capture / option choose / sync brain
- [ ] define a minimal task packet template including `rules_to_load`
- [ ] add a clear policy statement that AICOS serves context but does not control external runtime memory internals
- [ ] update startup-critical files to keep them concise and role-safe
- [ ] avoid pushing long policy prose into startup files
- [ ] ensure cold/frozen context remains reference-only unless explicitly needed

---

## 14. Things Codex must not do in this step

### Checklist Code: CTX-26155

- [ ] do not attempt to redesign Codex, Claude Code, or OpenClaw internal context systems
- [ ] do not build a giant context orchestration engine right now
- [ ] do not require loading all policy docs at startup
- [ ] do not turn current-state or current-direction into giant omnibus docs
- [ ] do not overbuild resolver APIs before packets/cards are proven useful
- [ ] do not collapse hot/warm/cold/frozen context into one loading behavior

---

## 15. Definition of Done

This model is implemented well only when:

- [ ] a co-worker can start with a very small context packet
- [ ] task-relevant rules are loaded only when needed
- [ ] long docs remain reference material, not startup burden
- [ ] AICOS clearly states that it provides context without claiming control over external runtime memory behavior
- [ ] startup context becomes lighter, not heavier
- [ ] the repo becomes easier for A2-Core to use incrementally

---

## 16. Final Reminder To Codex

Do not try to solve context loading by forcing every co-worker to read everything.

Solve it by:

- packaging the right minimum
- labelling the right authority
- giving the right lookup path
- loading more only on task trigger

AICOS should behave like a disciplined project environment, not like a giant mandatory reading list.

---
