# POL-26150 — AICOS Policy Pack Consolidated Guide

**Status:** consolidated-policy-pack-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** tổng hợp các file policy/rules gần đây thành một guide ngắn để dễ đọc, dễ map vào repo, và dễ dùng làm reading order cho Codex A2-Core.

---

## 1. Mục tiêu của policy pack này

Policy pack này gom các file policy/rules quan trọng đã tạo gần đây để:

- tránh đọc quá nhiều file rời mà bị lạc
- xác định file nào đóng vai trò gì
- xác định file nào nên được normalize vào self-brain / working state / rules lane
- xác định reading order ngắn cho Codex

---

## 2. Danh sách các file policy/rules chính

### 2.1. RUL-26088
**Tên:** `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`

**Vai trò:**
- file role clarity ngắn
- định nghĩa A1 là gì
- định nghĩa A2 là gì
- nói rõ Codex hiện tại mặc định đang ở A2-C lane khi build AICOS
- cho startup reading order cơ bản

**Nên dùng để:**
- làm role/startup gate
- làm nguồn cho `role-definitions.md`
- làm nguồn cho startup reading order ngắn

---

### 2.2. A2S-26102
**Tên:** `A2S-26102_AICOS_A2_Taxonomy_A2_Rules_and_AICOS_Self_Brain_Working_Spec.md`

**Vai trò:**
- làm rõ taxonomy của A2
- tách A2-Core và A2-Serve
- tách A2-Core-R và A2-Core-C
- làm rõ self-brain của AICOS là gì
- nói file nào nên ở canonical / working / evidence

**Nên dùng để:**
- làm nguồn cho role-definitions
- làm nguồn cho architecture-working-summary
- làm nguồn cho project-working-rules
- làm nguồn cho startup reading order của A2

---

### 2.3. FLW-26124
**Tên:** `FLW-26124_Codex_A2_Core_Guide_For_Human_Chat_Decision_Flow_Option_Choose_And_Sync_Brain.md`

**Vai trò:**
- giải thích flow human chat ↔ agent ↔ AICOS
- định nghĩa vai trò của:
  - chat channel
  - `aicos option choose`
  - `aicos sync brain`
- làm rõ interactive mode và async mode
- giải thích agent commit decision vào AICOS state như thế nào

**Nên dùng để:**
- làm nguồn cho working/current-direction
- làm nguồn cho project-working-rules
- làm nguồn cho implementation plan cụ thể cho A2-Core

---

### 2.4. POL-26140
**Tên:** `POL-26140_AICOS_Policy_For_Capturing_New_Ideas_Open_Questions_TODOs_TechDebt_And_Candidate_Branch_Ideas.md`

**Vai trò:**
- policy cho new ideas
- phân biệt:
  - open questions
  - todo/backlog
  - candidate branch ideas
  - tech debt
  - active risks

**Nên dùng để:**
- làm nguồn cho `open-questions.md`
- làm nguồn cho `active-risks.md`
- làm nguồn cho A2 backlog handling
- làm nguồn cho candidate-decisions lane

---

### 2.5. POL-26145
**Tên:** `POL-26145_AICOS_State_Writeback_And_Sync_Policy.md`

**Vai trò:**
- master writeback policy
- phân biệt:
  - W1 no write
  - W2 session/runtime write
  - W3 working state write
  - W4 canonical promotion
- định nghĩa commit point
- policy riêng cho interactive mode
- policy riêng cho async mode
- khi nào gọi `aicos option choose`
- khi nào gọi `aicos sync brain`

**Nên dùng để:**
- làm policy gốc cho writeback behavior
- làm nguồn cho project-working-rules
- làm nguồn cho A2 operational rules
- làm nguồn cho startup docs liên quan đến writeback

---

## 3. Reading order ngắn cho Codex A2-Core

Nếu cần reading order ngắn nhất, hãy dùng:

1. `RUL-26088_*`
2. `A2S-26102_*`
3. `POL-26145_*`
4. `POL-26140_*`
5. `FLW-26124_*`

### Vì sao theo thứ tự này

- đọc role trước
- rồi taxonomy A2
- rồi writeback master policy
- rồi idea-capture policy
- rồi flow của chat decision / option choose / sync brain

---

## 4. Mapping các file này vào repo AICOS

Các file artifact ngoài chat không nên chỉ nằm rời mãi bên ngoài repo.  
Cần normalize nội dung của chúng vào các lane phù hợp bên trong repo.

### Table Code: POL-26152

| File nguồn | Nên map vào repo như thế nào |
|---|---|
| `RUL-26088_*` | normalize vào `brain/projects/aicos/canonical/role-definitions.md` và startup order ngắn |
| `A2S-26102_*` | normalize vào `brain/projects/aicos/canonical/role-definitions.md`, `brain/projects/aicos/working/architecture-working-summary.md`, `brain/projects/aicos/canonical/project-working-rules.md` |
| `FLW-26124_*` | normalize vào `brain/projects/aicos/canonical/project-working-rules.md`, `brain/projects/aicos/working/current-direction.md`, và implementation notes nếu cần |
| `POL-26140_*` | normalize vào `brain/projects/aicos/working/open-questions.md`, `brain/projects/aicos/working/active-risks.md`, A2 backlog handling conventions, và `evidence/candidate-decisions/README.md` |
| `POL-26145_*` | normalize vào `brain/projects/aicos/canonical/project-working-rules.md`, A2 operational rules, startup rule summaries, và implementation notes cho `option choose` / `sync brain` |

---

## 5. Nguyên tắc map vào repo

### Rule 1

Không cần copy nguyên từng file dài vào repo nếu không cần.

### Rule 2

Ưu tiên:
- trích xuất
- chuẩn hóa
- rút gọn
- đưa vào đúng lane

### Rule 3

Giữ source file gốc như evidence/reference nếu cần provenance.

### Rule 4

Self-brain phải ngắn gọn hơn source docs.

---

## 6. Những lane trong repo nên được update sau khi ingest policy pack

### 6.1. Canonical

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`

### 6.2. Working

- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/architecture-working-summary.md`

### 6.3. Evidence / policy references

- `brain/projects/aicos/evidence/candidate-decisions/README.md`
- `brain/projects/aicos/evidence/review-packs/` hoặc `brain/projects/aicos/evidence/source-references/`

### 6.4. Agent operational lanes

- `agent-repo/classes/a2-service-agents/rules/`
- `agent-repo/classes/a2-service-agents/tasks/backlog/`

---

## 7. Điều không nên làm

- không biến policy pack thành thêm một lớp docs dài khó đọc
- không copy nguyên toàn bộ artifact vào canonical
- không nhét hết policy vào `current-state.md`
- không để startup order phải đọc 8–10 file dài mới làm việc được

---

## 8. Kết luận ngắn

Policy pack này nên được coi là:

- **source material để normalize vào repo**
- không nhất thiết là hình thức cuối cùng bên trong repo

Mục tiêu cuối cùng là để AICOS có:

- role clarity ngắn gọn
- A2 taxonomy rõ
- writeback/sync policy rõ
- new-idea capture policy rõ
- startup reading order ngắn và dùng được thật

---
