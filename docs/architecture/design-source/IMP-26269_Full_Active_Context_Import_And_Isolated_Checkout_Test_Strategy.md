# IMP-26269 — Full Active Context Import And Isolated Checkout Test Strategy For Sample Project

**Status:** execution-brief-v1
**Project:** AICOS
**Date:** 2026-04-19
**Primary scope:** `projects/aicos`
**Target external project:** `sample project-Trading-Framework`
**Purpose:** định nghĩa strategy chi tiết để Codex triển khai theo hướng:

- không chỉ import một slice quá mỏng để “demo”
- mà import **full active context** đủ để làm việc thật
- trong khi vẫn giữ:
  - external repo checkout mới = code/runtime authority
  - AICOS = context/control-plane authority
- và đảm bảo việc test diễn ra trên **isolated checkout mới**, không ảnh hưởng folder hiện tại đang dùng

Tài liệu này cũng phân biệt rõ 3 vai trò triển khai có thể có:

1. **A2-Core Codex 1**
   Agent A2-Core hiện tại đang làm việc cùng human để:
   - cập nhật AICOS
   - tạo Import Kit
   - chuẩn hóa checklist/template/rules
   - không trực tiếp làm import test thật trong external repo checkout

2. **A2-Core Codex 2**
   Một agent A2-Core Codex khác, chạy ở thread độc lập, dùng kit đã chuẩn hóa để:
   - thực thi import riêng
   - không thừa hưởng context từ A2-Core Codex 1
   - giúp kiểm tra kit có đủ tốt thật không

3. **A1 Importer (optional alternative)**
   Có thể thay vì dùng A2-Core Codex 2 để import, tạo một A1 mới làm import operator theo packet/rules của AICOS.
   Mục đích:
   - test xem A1 có đủ khả năng startup/import/continuation không
   - nhưng chỉ nên dùng khi kit đã đủ rõ để A1 không bị underpowered

---

## 1. Executive Summary

### New strategic direction

Thay vì tiếp tục đi theo hướng:

- import slice rất mỏng
- rồi mới dần nới context

ta chuyển sang hướng:

### **Full active context import + isolated external checkout test**

Nghĩa là:

#### A. AICOS sẽ import
- toàn bộ **current active context** cần thiết để một worker mới có thể làm việc thật
- nhưng **không** import:
  - archive/history
  - stale handoffs
  - generated output bulk
  - full repo/code mirror
  - broad historical proposal/review trails

#### B. External repo checkout mới sẽ giữ
- codebase
- scripts
- tests
- runtime
- environment/bootstrap
- generated runtime artifacts

#### C. Worker mới trong test
- lấy context từ AICOS
- làm việc trong isolated checkout mới
- không động vào folder hiện tại
- writeback/continuity về AICOS

### Main principle

**Import first, bridge later.**

- First import digestion = direct import execution pass
- MCP/runtime bridge chỉ nên được implement sau khi test thực chiến cho thấy nó thật sự cần

---

## 2. Why This Direction Is Better For Testing

### 2.1. Test independence
External checkout mới giúp:
- không ảnh hưởng folder hiện tại
- dễ rollback
- dễ so sánh workflow cũ và workflow mới

### 2.2. Better realism
A1 hoặc Codex worker sẽ làm việc trên:
- repo thật
- codebase thật
- scripts/tests/runtime thật

thay vì một môi trường “chỉ có context mỏng”.

### 2.3. Better proof of kit quality
Nếu một agent mới, chạy thread mới, vẫn import và làm việc được:
- đó là bằng chứng kit/checklist đủ tốt thật
- không phải vì nó thừa hưởng context chat cũ

### 2.4. Safer migration path
Cho tới khi phương pháp mới ổn định:
- team vẫn giữ workflow hiện tại
- test path mới tồn tại độc lập
- chỉ khi đủ chắc mới chuyển hẳn

---

## 3. Definitions

## 3.1. “Full active context” means what

**Full active context** = toàn bộ **context đang active và hữu ích cho real work**, gồm:

- current project truth
- current product/runtime baseline
- current startup/routing truth
- current handoff/current continuity
- current active working state
- current active open items / open questions / active risks
- current delivery surfaces cần thiết
- current A1 startup/task packet surfaces cần thiết

### It does NOT mean
- archive/history
- superseded handoffs
- generated bundle bulk
- historical review trails không cần cho current work
- raw codebase mirror
- broad code internals không cần thiết cho startup/use path

---

## 3.2. “Isolated checkout” means what

Một local folder mới, độc lập với folder đang dùng hiện tại, chứa:

- full checkout hoặc working checkout của external repo
- branch cần test
- runtime/scripts/tests/env trong chính folder đó

A1/Codex test worker sẽ làm việc trong folder này.

### Rule
Không dùng folder hiện tại làm nơi test phương pháp mới.

---

## 4. Authority Model

## 4.1. AICOS authority
AICOS là authority cho:

- imported project truth
- imported working truth
- startup bundles
- task packets
- handoff/current continuity
- writeback expectations
- open questions / open items / active risks
- context/control-plane coordination

## 4.2. External checkout authority
External isolated checkout là authority cho:

- code
- runtime
- scripts
- tests
- env/bootstrap
- execution artifacts
- repo-local operational behavior

## 4.3. Worker session authority
Worker session chỉ giữ:

- current in-memory state
- local task execution state
- ephemeral tool outputs

### Rule
Worker session không phải durable truth.
Durable continuity phải quay về AICOS.

---

## 5. Role Separation

## 5.1. A2-Core Codex 1

### Identity
Agent đang làm việc ở thread hiện tại cùng human để cải tiến AICOS.

### Scope
- update AICOS
- normalize handoff model
- normalize A1/A2 rules
- create Import Kit
- create templates/checklists
- create scaffolding notes/contracts
- define process and evaluation model

### Must not be used as proof of import success
Vì agent này đã tích lũy nhiều context về:
- AICOS
- sample project target
- import strategy
- bridge strategy

Nếu chính agent này tự import thành công, ta chưa chứng minh được kit đủ tốt.

### Rule
A2-Core Codex 1 là **kit builder / system shaper**, không phải “clean test operator”.

---

## 5.2. A2-Core Codex 2

### Identity
Một agent A2-Core Codex khác, chạy ở:
- thread mới
- startup mới
- context mới

### Scope
- đọc current handoff và kit đã chuẩn hóa
- instantiate/execute import theo kit
- không dựa vào memory/context của thread cũ
- làm import test một cách gần-independent

### Why use this
Đây là cách tốt nhất để test:
- kit đủ rõ hay không
- startup/handoff/packet/import surfaces đủ tốt hay không
- import process có repeatable hay không

### Rule
A2-Core Codex 2 là **independent import operator**.

---

## 5.3. A1 Importer (optional alternative)

### Identity
Một A1 mới, dùng startup/rules/packet của AICOS để làm import operator.

### Why this may be useful
Nếu muốn test sâu hơn rằng:
- A1 startup đã đủ rõ
- A1 rules đủ mạnh
- A1 task packet đủ để làm import-like work

thì có thể dùng A1 importer.

### Why this may be too early
Import pass đầu tiên vẫn có tính:
- boundary-sensitive
- lane-mapping-sensitive
- truth-digestion-sensitive

Nếu A1 model chưa được validate đủ, dùng A1 quá sớm có thể gây nhiễu:
- fail vì A1 còn non
- chứ không hẳn fail vì Import Kit

### Recommendation
- **Preferred for first real import test:** A2-Core Codex 2
- **Optional later experiment:** A1 importer

---

## 6. Recommended Operating Decision

### Primary recommendation
Dùng:

- **A2-Core Codex 1** = tiếp tục làm system shaper / kit maintainer
- **A2-Core Codex 2** = independent import executor trong thread khác

### Optional later
Sau khi import pass bằng A2-Core Codex 2 thành công và được validate:
- tạo thêm một A1 importer thử nghiệm

### Why this is best
Cách này tách được:
- “người xây kit”
- và “người dùng kit”

nên kết quả test đáng tin cậy hơn.

---

## 7. What The Import Pass Should Actually Do

Import pass mới **không** nên là “read a tiny slice only”.

Nó nên làm:

## Phase A — confirm isolated checkout target
- local source path
- source repo identity
- source branch
- checkout status
- whether the checkout is safe/independent from the current working folder

## Phase B — full active context import
Digest into AICOS all **current active context** needed for real work, such as:

### Canonical-active
- project brief
- product goals
- architecture baseline
- source/data/pipeline baseline if needed

### Working-active
- current state
- current handoff
- current active direction / readiness / work posture
- open items / open questions / active risks relevant to current project work

### Delivery-active
- current default delivery surface
- relevant command/runtime surface
- current default startup/use surfaces

### A1-active
- startup/use packet surfaces needed for future A1 work

## Phase C — validate imported project startup
Confirm that a fresh worker can:
- startup from AICOS lightly
- understand current project truth
- understand current working truth
- identify the isolated checkout as code/runtime authority

## Phase D — run independent work test
A new worker operates in the isolated checkout using AICOS as context authority.

---

## 8. What Must Not Be Imported By Default

Do **not** import broadly:

- archive/history
- historical handoff logs
- generated dist/runtime artifact bulk
- stale review/proposal trails
- raw full code tree mirror into AICOS
- full module map unless required
- broad older tactical variants unless currently active and needed

### Rule
Import “full active context”, not “everything”.

---

## 9. Recommended Deliverable Structure For This Strategy

## 9.1. Shared layer (already being built by A2-Core Codex 1)
Shared templates and process rules live in AICOS shared lanes.

## 9.2. Project-specific import execution cluster
For sample project:

```text
brain/projects/sample-project/evidence/import-kit/
```

This cluster should track:
- import execution state
- import identity
- source inventory
- lane mapping
- active context import checklist
- validation

## 9.3. Project truth lanes
Imported truth still lives in:
- `canonical/`
- `working/`

not inside the import-kit folder.

---

## 10. Revised Import Checklist Model

Import checklist for this new strategy must explicitly separate:

### A. Full active context include set
What active context will be digested.

### B. Excluded historical/reference set
What will remain excluded.

### C. External isolated checkout facts
Where the new checkout lives and which branch it uses.

### D. Worker separation
Which agent is:
- kit builder
- import executor
- optional A1 importer

### E. Validation target
How we know the new method is really usable.

---

## 11. Required New Checklist Items

The existing Import Kit should be extended/instantiated to include these explicit checks.

### Checklist Code: IMP-26270

- [ ] confirmed isolated external checkout path
- [ ] confirmed source branch in isolated checkout
- [ ] confirmed checkout is independent from the current working folder
- [ ] selected full active context include set
- [ ] selected explicit excluded historical/reference set
- [ ] canonical active context digested into AICOS
- [ ] working active context digested into AICOS
- [ ] delivery surface digested into AICOS
- [ ] A1 startup/use surfaces updated accordingly
- [ ] independent worker can startup from AICOS
- [ ] independent worker can work in isolated checkout
- [ ] no dependency on old thread memory/context
- [ ] no mutation of current working folder required

---

## 12. Recommended Validation Model

Validation should happen in 3 layers.

## 12.1. Import quality validation
Did AICOS capture the right active context without over-importing?

## 12.2. Startup validation
Can a fresh agent understand the project from AICOS without broad reading?

## 12.3. Independent execution validation
Can a separate agent operate in the isolated checkout and continue work correctly?

### Rule
Only layer 3 proves the method actually works.

---

## 13. Proposed Next Concrete Sequence

### Step 1
A2-Core Codex 1 finalizes:
- shared Import Kit
- project-specific instantiation guidance
- revised strategy note for full active context import

### Step 2
A2-Core Codex 2, in a new thread:
- reads AICOS current handoff
- reads sample project import kit instantiation
- confirms isolated checkout path
- performs full active context import
- does not rely on thread-old memory

### Step 3
After import succeeds:
- startup validation for new worker
- optional real task test in isolated checkout

### Step 4
Only after that:
- decide whether MCP runtime is still needed immediately
- or whether direct AICOS + isolated checkout is already sufficient enough for now

---

## 14. Decision On Whether To Use A1 For Import

### Default answer
Not for the first main import test.

### Why
Because the first main import test should primarily test:
- import kit quality
- context authority quality
- lane mapping quality
- startup quality

Using A1 too early may confound:
- A1 capability gaps
- with import strategy quality

### Better timing for A1 importer
After:
- A2-Core Codex 2 proves the import path works
- imported project truth is stable enough
- startup/use packets are refined enough

Then A1 importer becomes a good second-stage validation.

---

## 15. Final Recommendation

### Recommended model to adopt now

- **A2-Core Codex 1**
  - continues shaping AICOS
  - continues improving kits/templates/checklists/rules
  - does not serve as the clean import operator

- **A2-Core Codex 2**
  - runs independently in a new thread
  - performs the actual sample project import via the prepared kit
  - uses an isolated external checkout
  - proves the kit is good enough without inherited context

- **A1 importer**
  - optional later-stage test
  - not the preferred first main import operator

### Strategic rule
**Use full active context import, not ultra-thin slice import, for the first real isolated checkout test.**
But still do **not** import archives/history/full raw code mirror.

---

## 16. Definition Of Done For This Strategy

This strategic preparation is complete only when:

- [ ] A2-Core Codex 1 and A2-Core Codex 2 roles are explicitly separated
- [ ] the import test is planned against an isolated external checkout
- [ ] the import target is “full active context”, not “everything”
- [ ] excluded surfaces are explicit
- [ ] the project-specific import kit can guide an independent operator
- [ ] the next thread can run import without relying on current-thread context
- [ ] MCP runtime is explicitly deferred until after real isolated test validation

---

## 17. Final Operating Rule

For the first real cross-repo proof:

- do not test by relying on inherited thread context
- do not test by touching the current working folder
- do not test by importing only a toy-thin slice
- do not test by building MCP runtime too early

Instead:

- build/normalize the kit in one thread
- run the import in another thread
- use an isolated external checkout
- import full active context
- prove the method works independently

before deciding whether the new method should become the primary way of working.

---
