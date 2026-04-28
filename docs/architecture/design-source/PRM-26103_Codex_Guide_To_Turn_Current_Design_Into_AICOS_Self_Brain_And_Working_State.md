# PRM-26103 — Codex Guide To Turn The Current Design Into AICOS Self-Brain And Working State

**Status:** active-build-guide-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** hướng dẫn Codex biến các tài liệu thiết kế hiện có thành **self-brain** và **working state** của chính AICOS, thay vì để chúng chỉ nằm rải rác ở `docs/` hoặc các file thiết kế rời.

---

## 1. Mục tiêu của công việc này

Codex phải thực hiện một việc rất cụ thể:

> Biến các tài liệu thiết kế, rules, review pack, implementation plan, và kiến trúc hiện có thành **brain** và **working state** của chính AICOS.

Điều này có nghĩa là:

- AICOS phải có **self-brain** cho chính nó
- self-brain đó phải phản ánh:
  - AICOS là gì
  - current architecture là gì
  - current implementation status là gì
  - current risks là gì
  - current open questions là gì
  - current migration state là gì
  - role definitions hiện tại là gì
- các tài liệu dài ở `docs/` không phải là nơi đọc mặc định đầu tiên nữa
- thay vào đó, Codex và các A2 agents phải đọc **self-brain của AICOS** trước, rồi mới đọc raw docs khi cần

---

## 2. Nguyên tắc quan trọng nhất

### 2.1. Brain phải ngắn gọn

Các file trong self-brain của AICOS phải:

- ngắn gọn
- súc tích
- dễ đọc
- dễ dùng làm startup context
- dễ review
- không copy nguyên quá nhiều từ tài liệu dài

### 2.2. Brain không phải là nơi nhồi toàn bộ docs gốc

Không copy nguyên xi toàn bộ:

- architecture docs dài
- review packs dài
- implementation plans dài
- raw design notes dài

vào `brain/`.

Thay vào đó:

- giữ source docs ở chỗ cũ
- tạo **bản tóm tắt chuẩn hóa, ngắn gọn** vào self-brain
- nếu cần, dẫn chiếu tới source file gốc

### 2.3. Working state phải phản ánh trạng thái hiện tại thật

Các file working state không được viết kiểu trừu tượng chung chung.

Chúng phải phản ánh đúng:

- repo hiện ở trạng thái nào
- Codex đã làm gì
- cái gì đang active
- cái gì chưa active
- risk hiện tại là gì
- next step hiện tại là gì

---

## 3. Quy tắc ngôn ngữ bắt buộc

### 3.1. Trong self-brain và working state của AICOS

Các file dưới các lane sau phải **ưu tiên dùng tiếng Việt có dấu**:

- `brain/projects/aicos/canonical/`
- `brain/projects/aicos/working/`
- `brain/projects/aicos/evidence/` (nếu là file tóm tắt do Codex viết mới)
- các file summary hoặc working notes mới tạo cho self-brain của AICOS

### 3.2. Các phần khác có thể dùng English

Các phần sau có thể dùng English bình thường:

- code
- JSON schema
- CLI help text nếu cần
- script names
- file names
- command names
- package names
- low-level technical docs
- integration configs

### 3.3. Nếu có vấn đề kỹ thuật với tiếng Việt có dấu

Nếu có lý do kỹ thuật thật sự khiến tiếng Việt có dấu không dùng được an toàn ở một chỗ nào đó:

- dùng **English**
- **không** dùng tiếng Việt không dấu

### 3.4. Cho phép mixed language khi cần

Nếu có thuật ngữ:

- khó dịch
- không nên dịch
- dịch ra sẽ kém chính xác

thì được phép dùng tiếng Anh lẫn tiếng Việt, ví dụ:

- working state
- capsule
- branch
- option packet
- promotion
- self-brain
- service skill
- deterministic kernel

---

## 4. Phạm vi công việc hiện tại

Công việc này chỉ tập trung vào:

- self-brain của **AICOS**
- working state của **AICOS**
- canonical identity/rules tối thiểu của **AICOS**
- evidence lane cho các tài liệu thiết kế và review pack của **AICOS**

### Không làm trong bước này

- chưa tối ưu phần A1 business/project khác
- chưa migrate hàng loạt old backup
- chưa làm UI
- chưa làm public API
- chưa làm deep MCP server riêng cho AICOS
- chưa canonicalize quá nhiều

---

## 5. File nguồn mà Codex phải dùng làm đầu vào

Codex phải đọc và dùng các file này làm source đầu vào để tạo self-brain của AICOS:

### Nhóm thiết kế / kiến trúc

- `ARC-26071_AICOS_Kernel_ServiceSkills_GBrain_GStack_Architecture.md`
- `DSC-26040_AICOS_AI_Native_CoWorker_Architecture_Detail_Spec.md`
- `MAP-26031_AICOS_Brain_vs_AgentRepo_vs_Backend_ReadWrite_Boundary.md`
- `DSC-26038_AICOS_Company_Team_Native_Architecture_Leveraging_GBrain.md`
- `AGT-26016_AICOS_Agent_Classes_Knowledge_Boundaries_and_Rules_Matrix.md`

### Nhóm implementation / migration

- `PLN-26072_Codex_Implementation_Plan_Checklist_For_AICOS_Current_Repo.md`
- `AICOS_RESTRUCTURE_BUILD_REVIEW_PACK_20260418.md`

### Nhóm rules / role clarity

- `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`
- `A2S-26102_AICOS_A2_Taxonomy_A2_Rules_and_AICOS_Self_Brain_Working_Spec.md`

---

## 6. Mục tiêu self-brain của AICOS sau bước này

Sau khi hoàn thành bước này, AICOS phải có ít nhất các file sau trong self-brain.

### 6.1. Canonical tối thiểu

```text
brain/projects/aicos/canonical/
  project-profile.md
  role-definitions.md
  project-working-rules.md
  source-manifest.md
```

### 6.2. Working state tối thiểu

```text
brain/projects/aicos/working/
  current-state.md
  current-direction.md
  active-risks.md
  open-questions.md
  architecture-working-summary.md
  implementation-status.md
  migration-status.md
```

### 6.3. Evidence tối thiểu

```text
brain/projects/aicos/evidence/
  review-packs/
  codex-reports/
  candidate-rules/
  candidate-decisions/
  friction/
```

### 6.4. Optional but useful if already available

```text
brain/projects/aicos/working/
  handoff-summary.md
  service-skills-working-summary.md
```

---

## 7. Nội dung từng file nên viết như thế nào

## 7.1. `canonical/project-profile.md`

File này phải ngắn gọn và trả lời:

- AICOS là gì
- AICOS phục vụ ai
- AICOS không phải là gì
- mục tiêu hiện tại của MVP là gì

### Độ dài khuyến nghị

- ngắn
- khoảng 10–30 dòng là đủ

---

## 7.2. `canonical/role-definitions.md`

File này phải chốt ngắn gọn:

- A1 là gì
- A2 là gì
- humans là gì
- Codex hiện tại mặc định đang ở lane nào
- A2-Core là gì
- A2-Serve là gì
- nhánh nào đang active hiện nay

### Độ dài khuyến nghị

- khoảng 20–50 dòng
- không lan man

---

## 7.3. `canonical/project-working-rules.md`

File này phải chốt những working rules tối thiểu của AICOS hiện tại.

Ít nhất phải có:

- brain vs agent-repo vs backend boundary
- canonical vs working vs evidence boundary
- A1 không sửa system
- A2 sửa AICOS, không làm thay project business
- startup reading order phải ưu tiên self-brain trước raw repo
- không hardcode service intelligence quá sớm

### Độ dài khuyến nghị

- khoảng 20–60 dòng
- bullet / section ngắn, dễ scan

---

## 7.4. `canonical/source-manifest.md`

File này phải nói rõ:

- đâu là source docs chính cho AICOS hiện tại
- file nào là design source
- file nào là implementation/review source
- source nào đang authoritative hơn source nào

Không cần dài.  
Mục tiêu chỉ là để Codex biết nên đọc đâu trước.

---

## 7.5. `working/current-state.md`

File này phải phản ánh đúng trạng thái hiện tại của AICOS.

Ví dụ nên có:

- repo đã restructure tới đâu
- active root hiện tại gồm các lane nào
- GBrain đang ở trạng thái nào
- CLI `./aicos` đang làm được gì
- blocked→options flow đã được chứng minh ở mức nào
- phần nào mới là scaffold
- phần nào còn chưa active

Đây là file quan trọng nhất cho startup context.

---

## 7.6. `working/current-direction.md`

File này phải trả lời:

- hướng triển khai hiện tại đang ưu tiên gì
- thứ tự ưu tiên hiện nay là gì
- bước nào đang làm trước
- bước nào cố tình chưa làm

Ví dụ hiện tại nên phản ánh:

- ưu tiên A2 + AICOS self-brain trước
- chưa làm sâu phần A1
- chưa làm UI
- chưa làm API
- chưa ép GStack thành core

---

## 7.7. `working/active-risks.md`

File này phải ghi rõ các risk đang còn.

Ví dụ:

- A1/A2 role confusion
- A2-Core vs A2-Serve confusion
- self-brain chưa đủ mạnh
- brain docs có nguy cơ quá dài
- service logic có nguy cơ hardcode sớm
- old backup material có nguy cơ leak lại vào startup context
- GBrain sync chưa fully active

Mỗi risk nên rất ngắn:
- risk
- impact
- mitigation hiện tại

---

## 7.8. `working/open-questions.md`

File này phải ghi các câu hỏi kiến trúc / implementation còn mở.

Ví dụ:

- khi nào activate A2-Serve?
- khi nào canonicalize architecture.md?
- khi nào thêm `aicos option choose`?
- khi nào bật real GBrain import/index?
- MCP wrapper riêng của AICOS nên làm ở phase nào?

---

## 7.9. `working/architecture-working-summary.md`

File này phải là **bản tóm tắt rất gọn** từ các tài liệu kiến trúc dài.

Không copy nguyên xi.

Nội dung nên có:

- AICOS = company/workspace intelligence layer
- layers chính
- AICOS Kernel vs A2 Service Skills
- GBrain là substrate
- GStack optional khi cần code work
- self-brain model của AICOS
- A2 taxonomy summary

### Rule

Nếu file này quá dài, Codex phải rút gọn lại.

---

## 7.10. `working/implementation-status.md`

File này phải trả lời:

- Codex đã làm gì rồi
- phần nào đã scaffold
- phần nào mới là seed
- commands nào đang chạy
- phần nào mới là preflight
- part nào chưa phải runtime thật

Có thể lấy từ review pack hiện có, nhưng phải viết lại gọn.

---

## 7.11. `working/migration-status.md`

File này phải tóm tắt:

- old root đã được move đi đâu
- active root hiện còn gì
- folder nào đã migrate
- folder nào chưa migrate
- nguyên tắc dùng backup hiện nay là gì

---

## 8. Evidence lane nên dùng thế nào

Các tài liệu dài, raw, hoặc review-heavy nên vào `evidence/` theo 2 cách:

### Cách 1 — giữ source file ở nơi cũ, tạo file index/tóm tắt trong evidence
Khuyến nghị ưu tiên cách này.

Ví dụ tạo:

```text
brain/projects/aicos/evidence/review-packs/review-pack-index.md
brain/projects/aicos/evidence/candidate-rules/rules-candidate-index.md
```

Các file này chỉ cần:
- nêu file nguồn
- nêu nội dung chính
- nêu vì sao liên quan

### Cách 2 — copy chọn lọc một phần ngắn đã review
Chỉ dùng khi thật cần.

### Rule

Không dump nguyên nhiều file dài vào evidence lane nếu chưa cần.

---

## 9. Quy tắc độ dài cho self-brain

Đây là rule rất quan trọng.

### 9.1. Canonical files
Nên:
- ngắn
- rõ
- ít noise
- dễ dùng làm startup context

### 9.2. Working files
Cho phép dài hơn canonical một chút, nhưng vẫn phải:
- tóm tắt trước
- liệt kê ngắn
- dễ scan

### 9.3. Không tạo các file “essay”
Không viết self-brain theo kiểu bài luận dài.

Mỗi file nên ưu tiên:

- mục đích rõ
- bullets ngắn
- sections ngắn
- decision / status / risk / next step rõ

---

## 10. Rule ngôn ngữ cho Codex khi viết self-brain

### Bắt buộc

Trong các file dưới:

- `brain/projects/aicos/canonical/`
- `brain/projects/aicos/working/`

Codex phải ưu tiên:

- **tiếng Việt có dấu**

### Cho phép

- mixed Vietnamese + English cho technical terms
- English cho code / command / filenames / package names

### Không được

- không dùng tiếng Việt không dấu
- không trộn văn phong nửa Việt không dấu nửa English lộn xộn

### Fallback

Nếu gặp lý do kỹ thuật khiến không dùng tiếng Việt có dấu an toàn:

- dùng **English**
- không được dùng tiếng Việt không dấu

---

## 11. Startup reading order mới mà Codex phải áp dụng

Sau khi tạo self-brain của AICOS, Codex phải áp dụng startup reading order mới như sau:

### Step 1
Read:

- `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`

### Step 2
Read:

- `A2S-26102_AICOS_A2_Taxonomy_A2_Rules_and_AICOS_Self_Brain_Working_Spec.md`

### Step 3
Read self-brain working state first:

- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/architecture-working-summary.md`
- `brain/projects/aicos/working/implementation-status.md`
- `brain/projects/aicos/working/migration-status.md`

### Step 4
Only then inspect:

- raw repo structure
- scripts
- package code
- integrations
- evidence docs if needed

### Rule

Raw repo should no longer be the first place to reconstruct AICOS mental model.

---

## 12. Công việc Codex phải làm cụ thể

### Checklist Code: PRM-26104

- [ ] create/update `brain/projects/aicos/canonical/project-profile.md`
- [ ] create/update `brain/projects/aicos/canonical/role-definitions.md`
- [ ] create/update `brain/projects/aicos/canonical/project-working-rules.md`
- [ ] create/update `brain/projects/aicos/canonical/source-manifest.md`

- [ ] create/update `brain/projects/aicos/working/current-state.md`
- [ ] create/update `brain/projects/aicos/working/current-direction.md`
- [ ] create/update `brain/projects/aicos/working/active-risks.md`
- [ ] create/update `brain/projects/aicos/working/open-questions.md`
- [ ] create/update `brain/projects/aicos/working/architecture-working-summary.md`
- [ ] create/update `brain/projects/aicos/working/implementation-status.md`
- [ ] create/update `brain/projects/aicos/working/migration-status.md`

- [ ] create/update `brain/projects/aicos/evidence/review-packs/`
- [ ] create/update `brain/projects/aicos/evidence/candidate-rules/`
- [ ] create/update `brain/projects/aicos/evidence/candidate-decisions/`
- [ ] create/update `brain/projects/aicos/evidence/friction/`

- [ ] ensure these self-brain files are concise and reviewable
- [ ] ensure language rule is respected
- [ ] ensure startup reading order is updated in relevant startup docs or AGENTS path if appropriate

---

## 13. Không được làm gì trong bước này

### Checklist Code: PRM-26105

- [ ] do not over-canonicalize too many files
- [ ] do not copy all long docs into brain verbatim
- [ ] do not rewrite all A1 logic yet
- [ ] do not build UI yet
- [ ] do not build public API yet
- [ ] do not activate full A2-Serve runtime lane yet
- [ ] do not force all policies into code
- [ ] do not use tiếng Việt không dấu in self-brain

---

## 14. Định nghĩa done cho bước này

Bước này chỉ được coi là done khi:

1. AICOS có self-brain tối thiểu ở `brain/projects/aicos/`
2. các file canonical tối thiểu đã tồn tại
3. các file working tối thiểu đã tồn tại
4. review pack hiện có đã được map vào evidence lane hoặc có index/tóm tắt tương ứng
5. startup reading order mới cho A2 đã rõ
6. Codex có thể đọc self-brain trước rồi mới đọc repo raw
7. các file self-brain ngắn gọn, dễ scan, dùng tiếng Việt có dấu

---

## 15. Final Reminder To Codex

Your goal in this step is **not** to add more architecture.

Your goal is to turn the current architecture and implementation knowledge into a **usable self-brain and working state for AICOS itself**.

Do this in a way that:

- is concise
- is reviewable
- is role-safe
- is future-friendly
- reduces context loss
- makes startup reading easier
- avoids long noisy brain docs

If there is a conflict between:

- copying full source material
- and creating concise self-brain files

always prefer:

- concise self-brain files
- with references back to source docs

---
