# IMP-26249 — AICOS Import Strategy For Sample Project From `main`

**Status:** working-strategy-v1  
**Project:** AICOS  
**Target external project:** Sample Project  
**Date:** 2026-04-18  
**Purpose:** mô tả strategy import chi tiết để đưa dự án `sample project-Trading-Framework` từ nhánh `main` vào AICOS theo cách:
- không phá authority hiện có của repo sample project
- không merge codebase vào repo AICOS
- import đúng lớp context cần thiết
- tạo đủ bootstrap để A1 có thể làm việc thật sau import
- giữ startup light, packet-first, và token-efficient

---

## 1. Executive Summary

`sample project-Trading-Framework` hiện là một repo có cả:

- repo-local code/runtime structure
- `shared-context/` làm operational source of truth cho Codex, Claude, và ChatGPT
- startup routing theo task type
- compact `state/current.md` và `state/handoff.md`
- product baseline rõ
- kiến trúc pipeline đã có
- runnable MVP backbone cho `sample_workstream` và `tactical_update_4h`

Vì vậy, đây là ứng viên rất phù hợp để làm **first real-project import** vào AICOS.

### Import principle

AICOS không nên “nuốt” toàn bộ repo sample project vào cùng authority tree của AICOS.

Thay vào đó:

- sample project repo vẫn là **code/runtime authority**
- AICOS trở thành **context / coordination authority**
- AICOS import những lớp project truth và working truth cần thiết
- sau đó tạo đủ A1 startup/packet/handoff surfaces để worker có thể làm việc trên repo sample project nhưng vẫn follow AICOS

---

## 2. Why This Repo Is A Good First Real Project

Repo `sample project-Trading-Framework` có các đặc điểm khiến nó phù hợp làm real-project test đầu tiên:

### 2.1. Nó đã có context discipline riêng

Repo đã có:

- `AGENTS.md`
- `shared-context/README.md`
- startup paths theo loại task
- compact state/handoff model
- authority order
- scope discipline
- update discipline

Điều này có nghĩa là repo không phải một codebase “thô”, mà đã có operational context layer rõ ràng.

### 2.2. Nó đã có product truth tương đối rõ

Các file như:

- `shared-context/project/brief.md`
- `shared-context/project/product-goals.md`
- `shared-context/project/architecture.md`

đã mô tả rõ:

- project objectives
- product non-negotiables
- source stance
- timeframe stack
- mode baseline
- architecture backbone
- implementation direction

### 2.3. Nó đã có current coordination state tương đối ngắn gọn

Các file như:

- `shared-context/state/current.md`
- `shared-context/state/handoff.md`

đã được compact theo hướng token-aware, nên rất phù hợp để chuyển thành working bootstrap của AICOS.

### 2.4. Nó đã có một delivery surface “testable”

Repo đã có rõ:

- current GPT surface
- input JSON surface
- rolling bundle paths
- `sample_workstream`
- `tactical_update_4h`
- refresh/build commands

Điều này giúp ta chọn một **slice đầu tiên đủ thật** để test A1.

---

## 3. Import Scope Decision

## 3.1. Branch to import

- Source branch: `main`

### Why

`main` hiện được mô tả như portable-first baseline và active current branch cho repo.

---

## 3.2. AICOS project id

### Recommended project id

- `sample-project`

### Why not `sample-project` yet?

Vì scope hiện tại của repo đang là:

- sample project-first
- solo trader support product
- SCTR v3 baseline
- `sample_workstream` + `tactical_update_4h`

Nó hẹp hơn và cụ thể hơn một umbrella `sample-project`.

### Future note

Sau này có thể tạo higher scope như:

- workspace `sample-project`
- company/workspace layer containing multiple projects

Nhưng project import đầu tiên nên bám đúng repo reality hiện tại.

---

## 3.3. First slice to import

### Recommended first slice

- **default `sample_workstream` delivery slice**

### Meaning of this slice

Slice đầu tiên không phải toàn bộ pipeline/backbone của repo.
Nó là phần đủ để một A1 worker mới có thể:

- hiểu current project baseline
- hiểu current active product/runtime posture
- hiểu default delivery surface
- hiểu input/output path chính
- follow một task packet cụ thể liên quan đến `sample_workstream`
- test startup efficiency, rule compliance, và continuation quality

### Why this slice is best

Nó:

- đủ thật để test AICOS
- đủ gọn để debug
- gắn với current active delivery baseline
- không kéo full repo internals quá sớm
- phù hợp với mục tiêu test token/context efficiency

---

## 4. Authority Model During Import

### sample project repo remains authority for:

- source code
- scripts
- tests
- runtime execution
- environment/bootstrap
- generated runtime artifacts
- repo-local implementation files

### AICOS becomes authority for:

- imported project truth
- imported working truth
- normalized handoff/current state
- open questions / open items / active risks
- A1 startup / packets / continuation metadata
- cross-actor continuity
- future shared/company/workspace layering

### Rule

Import into AICOS does **not** mean moving code authority into AICOS.

---

## 5. Source Material Classification Before Import

Before importing, classify source material into 4 buckets.

## 5.1. Canonical project truth

Likely candidates:

- `shared-context/project/brief.md`
- `shared-context/project/product-goals.md`
- `shared-context/project/architecture.md`
- `shared-context/impl/source-limits.md`
- `shared-context/impl/data-scope.md`
- `shared-context/impl/pipeline.md`

These define what the project is, what it must deliver, and what constraints it must respect.

---

## 5.2. Current working/coordination state

Likely candidates:

- `shared-context/state/current.md`
- `shared-context/state/handoff.md`
- selected current items from:
  - `shared-context/state/todo.md`
  - `shared-context/state/review-queue.md`
  - `shared-context/state/decisions-open.md`
  only if needed for the chosen slice

These should not be copied blindly.
They should be **digested** into AICOS working files.

---

## 5.3. Coordination/reference surfaces

Likely candidates:

- `README.md`
- `AGENTS.md`
- `shared-context/README.md`
- startup entry files
- navigation/support files
- active command paths and output surfaces

These are useful but should usually become:

- evidence/reference
- implementation provenance
- onboarding reference

not startup authority inside AICOS by default.

---

## 5.4. Not-to-import-by-default surfaces

Do not import these by default in pass 1:

- `shared-context/archive/`
- `artifacts/history/`
- historical `dist/` outputs
- large sync bundles
- full historical handoff logs
- old review/proposal history
- broad code internals unless slice 1 requires them

### Reason

This project already has anti-bloat / anti-broad-loading rules.
AICOS should preserve that discipline, not undo it.

---

## 6. Recommended AICOS Mapping

## 6.1. Canonical lane mapping

Import/digest into:

- `brain/projects/sample-project/canonical/`

Recommended files to create or populate:

- `project-brief.md`
- `product-goals.md`
- `architecture-baseline.md`
- `source-limits.md`
- `data-scope.md`
- `pipeline-baseline.md`

### Rule

Do not mirror the external filenames blindly if AICOS naming conventions differ.
Normalize them into coherent AICOS canonical naming.

---

## 6.2. Working lane mapping

Create/bootstrap:

- `brain/projects/sample-project/working/current-state.md`
- `brain/projects/sample-project/working/current-direction.md`
- `brain/projects/sample-project/working/open-questions.md`
- `brain/projects/sample-project/working/open-items.md`
- `brain/projects/sample-project/working/active-risks.md`
- `brain/projects/sample-project/working/handoff/current.md`

These should be **short digests**, not raw copies of external files.

---

## 6.3. Evidence/reference mapping

Create evidence/reference for:

- external repo startup/authority overview
- imported source inventory
- original source file mapping
- command/output surfaces for the chosen slice
- provenance notes for import decisions

Suggested placement:

- `brain/projects/sample-project/evidence/source-inventory/`
- `brain/projects/sample-project/evidence/import-notes/`
- `brain/projects/sample-project/evidence/delivery-surfaces/`

---

## 6.4. Branch/workstream mapping

For pass 1, do not create many branch realities.

Instead, create a **slice/workstream note** for the chosen slice, such as:

- `brain/projects/sample-project/evidence/workstreams/default-sample-workstream-delivery-slice.md`

Later, if multiple alternate routes exist, they can become `branches/` entries.

---

## 6.5. A1 task-layer mapping

For pass 1, create only the smallest useful A1 artifacts:

- A1 packet index entry for the project
- one slice packet for onboarding/review
- one slice packet for first real task
- one continuation/handoff-oriented packet if needed

Suggested examples:

- `review-current-sample-workstream-slice`
- `validate-startup-and-context-sufficiency`
- `inspect-current-delivery-surface`
- `continue-prior-slice-review`

---

## 7. Bootstrap Requirements After Import

The import is not complete unless the imported project becomes startup-usable in AICOS.

## 7.1. Required working outputs

At minimum:

- `current-state.md`
- `current-direction.md`
- `handoff/current.md`
- `open-questions.md`
- `open-items.md`
- `active-risks.md`

## 7.2. Required A1 startup outputs

At minimum:

- project appears in A1 startup routing in a coherent way
- packet index exists for the chosen slice
- one packet is enough for a first A1 to begin work
- startup remains light and does not require broad loading

## 7.3. Required continuity outputs

At minimum:

- imported project has a current continuity point
- task packets refer to the right working context
- continuation is possible without reading the whole external repo context set

---

## 8. Proposed First-Slice Content

## 8.1. Slice name

- `default sample_workstream delivery slice`

## 8.2. Slice intent

Understand and work with the current active default delivery surface for the product, without importing the full code/runtime/internal history.

## 8.3. Slice components to capture

- current active product posture
- current default GPT surface
- root input-json surface
- rolling bundle surface
- refresh/build commands relevant to default delivery
- current operational baseline relevant to that delivery
- current open questions or risks relevant to the slice

## 8.4. Slice components to avoid in pass 1

- full pipeline internals
- all enrichment details
- all validation internals
- deep archive history
- full code module map
- all tactical/slower-view variants unless needed for the task

---

## 9. Recommended Import Procedure

### Step 1 — source inventory
Create a compact import inventory that records:
- source repo
- source branch
- selected files
- selected slice
- excluded surfaces
- rationale

### Step 2 — canonical digestion
Digest the selected project/impl truth into AICOS canonical files.

### Step 3 — working digestion
Digest current and handoff state into AICOS working files.

### Step 4 — delivery-surface note
Create one compact note describing the default `sample_workstream` delivery surface.

### Step 5 — A1 packet scaffolding
Create A1 task packet index and first packets for the chosen slice.

### Step 6 — startup check
Confirm a new A1 can enter the imported project with light startup.

### Step 7 — continuity check
Confirm a second A1 can continue without reconstructing the entire external repo manually.

---

## 10. What Should Be Measured After Import

After import, the first test should measure:

### 10.1. Context sufficiency
Can a new A1 understand the chosen slice without broad extra reading?

### 10.2. Context efficiency
Does startup stay compact and packet-first?

### 10.3. Rule compliance
Does A1 follow the imported project through AICOS lanes correctly?

### 10.4. Continuity quality
Can another A1 continue from task/handoff state cheaply?

### 10.5. Import quality
Did AICOS capture the right layers without bloating itself?

---

## 11. Risks To Watch During Import

### Risk 1 — importing too much
This will destroy the very token-efficiency AICOS is supposed to test.

### Risk 2 — mirroring external repo structure too literally
This will make AICOS a duplicate repo instead of a context authority.

### Risk 3 — promoting coordination docs into canonical truth blindly
This will confuse startup authority.

### Risk 4 — no real slice boundary
Then the import becomes “everything a little bit”, which is hard to validate.

### Risk 5 — no usable A1 packet after import
Then the imported project is not truly startup-usable.

---

## 12. Final Recommendation

### Project id
- `sample-project`

### Source branch
- `main`

### First slice
- `default sample_workstream delivery slice`

### Strategy
- import canonical truth first
- digest working state second
- create one slice delivery note
- create minimum viable A1 packets
- do not import archive/history/code internals broadly yet
- preserve repo sample project as code/runtime authority

This is the smallest import that is still useful enough to test AICOS on a real project.

---
