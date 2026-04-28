# KIT-26261 — AICOS Import Kit Template System For Cross-Repo Project Onboarding

**Status:** reusable-import-kit-v2
**Project:** AICOS
**Date:** 2026-04-19
**Purpose:** định nghĩa bộ **Import Kit templates** chuẩn để Codex có thể triển khai theo cho:
- `sample-project` ngay bây giờ
- và các external projects khác trong tương lai

Bộ kit này được viết theo các nguyên tắc:

- template-first
- project-instantiation-second
- packet-first
- startup-light
- authority-separated
- cross-repo friendly
- không overbuild

---

## 1. Executive Summary

AICOS đang đi vào phase **real cross-repo project onboarding**.

Ở phase này, cần một **Import Kit** đủ chuẩn để Codex không phải “nghĩ lại từ đầu” mỗi lần onboard một external project repo mới vào AICOS.

Import Kit này phải giúp Codex làm được 5 việc:

1. xác định **import identity** rõ ràng
2. xác định **authority boundary** rõ ràng
3. tạo **source inventory + lane mapping** rõ ràng
4. bootstrap đúng các **canonical / working / evidence / A1 startup** surfaces
5. validate rằng imported project đã đủ để A1 bắt đầu làm việc thật

### Core principle

Import Kit phải gồm **2 tầng**:

### Tầng A — Shared reusable kit
- templates dùng lại cho mọi project

### Tầng B — Project-specific instantiation
- checklist/files được instantiate riêng cho từng project, ví dụ:
  - `sample-project`
  - hoặc project khác sau này

### Rule
Shared kit không được viết theo logic riêng của sample project.

---

## 2. What This Kit Is For

Import Kit này **không** phải là:
- MCP implementation spec
- orchestration engine
- repo mirror plan
- code import automation framework lớn

Import Kit này **là**:
- một bộ file template và checklist rõ ràng
- để điều phối import pass đầu tiên một cách lặp lại được
- và để Codex biết chính xác:
  - cần tạo file nào
  - cần điền thông tin gì
  - cần validate cái gì
  - khi nào import được coi là đủ dùng

---

## 3. Current Operating Rule

### Rule 1
**Import first, bridge second.**

- First import digestion = A2-Core direct pass
- Local MCP = contract/runtime dùng cho cross-repo ongoing work về sau

### Rule 2
Không merge external repo vào AICOS.

### Rule 3
Không import full repo ở pass 1 nếu slice-first là đủ.

### Rule 4
External repo giữ:
- code/runtime authority

AICOS giữ:
- context/control-plane authority

### Rule 5
Imported project phải trở thành:
- startup-usable
- packet-usable
- continuity-usable

---

## 4. Recommended Shared Template Set

### Report Code: KIT-26262

Shared template set khuyến nghị gồm **8 file**:

1. `import-master-checklist-template.md`
2. `import-identity-template.md`
3. `source-inventory-template.md`
4. `authority-and-lane-mapping-template.md`
5. `slice-definition-template.md`
6. `bootstrap-output-checklist-template.md`
7. `a1-import-startup-template.md`
8. `import-validation-template.md`

### Suggested home

```text
brain/shared/templates/project-import-kit/
```

### Why 8 files instead of 6
File kit cũ khá đúng hướng nhưng còn gộp một số phần quá rộng.
Phiên bản này tách rõ hơn:
- import identity
- source inventory
- authority/lane mapping
- A1 startup readiness
- validation

để Codex làm theo từng bước nhỏ, ít nhầm hơn.

---

## 5. Shared Template 1 — Import Master Checklist

### File
`brain/shared/templates/project-import-kit/import-master-checklist-template.md`

### Purpose
Đây là file điều phối tổng thể cho một import pass.

Nó không chứa toàn bộ chi tiết, nhưng phải trỏ tới:
- identity
- inventory
- lane mapping
- slice
- bootstrap outputs
- A1 startup surfaces
- validation

### Required sections

#### A. Import overview
- source repo
- source branch
- target AICOS project id
- import actor
- import date
- current status

#### B. Import mode
- full import hay slice-first
- first slice name
- reason for current mode

#### C. Required companion files
- identity file
- source inventory
- lane mapping
- slice definition
- bootstrap checklist
- A1 startup readiness
- validation checklist

#### D. Current pass status
- not started
- in source inventory
- in digestion
- in startup validation
- validated for A1
- paused / blocked

#### E. Completion gate
- canonical digest done?
- working digest done?
- evidence/reference done?
- A1 packet/startup ready?
- validation recorded?

### Rule
Master checklist là file đầu tiên để xem trạng thái import của một project.

---

## 6. Shared Template 2 — Import Identity Template

### File
`brain/shared/templates/project-import-kit/import-identity-template.md`

### Purpose
Chuẩn hóa identity của một project import.

### Required sections

#### A. Source identity
- external repo name
- external repo URL
- source branch
- local source path
- current source authority statement

#### B. AICOS identity
- target AICOS project id
- target lane root
- import owner / actor lane
- current import status

#### C. First-slice decision
- slice name
- slice reason
- pass phase
- excluded broad scope

#### D. Authority split
- external repo keeps
- AICOS imports/digests
- future MCP role
- whether optional `.aicos/` cache is expected later

### Rule
Identity file phải đủ để một agent mới hiểu “đang import cái gì, từ đâu, vào đâu”.

---

## 7. Shared Template 3 — Source Inventory Template

### File
`brain/shared/templates/project-import-kit/source-inventory-template.md`

### Purpose
Ghi lại source materials được xét cho import.

### Inventory table

### Table Code: KIT-26263

| Field | Meaning |
|---|---|
| `source_path` | path trong external repo |
| `source_group` | project / impl / state / startup / evidence / code / output |
| `source_type` | canonical / working / evidence / excluded |
| `authority_level` | authoritative / reference / historical / excluded |
| `import_action` | digest / summary-only / reference-only / skip |
| `target_lane` | canonical / working / evidence / a1-support |
| `target_file` | file đích trong AICOS |
| `slice_relevance` | required / optional / later / out-of-scope |
| `pass_phase` | pass 1 / later |
| `notes` | rationale, caveat, dependency |

### Required sections
- selected canonical sources
- selected working sources
- selected evidence/reference sources
- excluded sources
- open questions in inventory

### Rule
Mọi real import đều phải có source inventory instantiated.

---

## 8. Shared Template 4 — Authority And Lane Mapping Template

### File
`brain/shared/templates/project-import-kit/authority-and-lane-mapping-template.md`

### Purpose
Chuẩn hóa cách map source materials vào lanes của AICOS mà không mirror repo nguồn quá literally.

### Required sections

#### A. Authority boundary
- code/runtime authority
- context/control-plane authority
- imported canonical truth boundary
- imported working truth boundary
- excluded/not-owned surfaces

#### B. Canonical mapping
- source file nào feed canonical summaries nào
- file canonical nào cần tạo
- file canonical nào deferred

#### C. Working mapping
- source nào feed:
  - `current-state.md`
  - `current-direction.md`
  - `handoff/current.md`
  - `open-questions.md`
  - `open-items.md`
  - `active-risks.md`

#### D. Evidence mapping
- source nào giữ lại làm provenance/reference
- source nào chỉ cần startup/reference note
- source nào chỉ ghi inventory mà chưa digest

#### E. A1 support mapping
- packet index nào cần có
- first packets nào cần có
- startup guidance nào cần có
- continuation surfaces nào cần có

### Rule
Lane mapping phải là **AICOS-native normalization**, không phải external-repo mirroring.

---

## 9. Shared Template 5 — Slice Definition Template

### File
`brain/shared/templates/project-import-kit/slice-definition-template.md`

### Purpose
Định nghĩa rõ slice đầu tiên được import/test.

### Required sections

#### A. Slice identity
- project id
- slice name
- source branch
- actor lane

#### B. Slice objective
- slice này nhằm test/enable cái gì

#### C. Included scope
- mặt nào được lấy vào
- docs/surfaces nào cần đọc/digest
- task/startup surfaces nào cần có

#### D. Excluded scope
- archive/history
- generated outputs
- deep internals
- variants chưa cần
- broader code map nếu chưa cần

#### E. Why this slice is right
- đủ thật
- đủ nhỏ
- đủ testable
- phù hợp startup-light

#### F. Expected outputs
- note nào cần tạo
- packet nào cần tạo
- validation nào phải chạy

### Rule
Slice phải bounded, explicit, testable, và explainable.

---

## 10. Shared Template 6 — Bootstrap Output Checklist Template

### File
`brain/shared/templates/project-import-kit/bootstrap-output-checklist-template.md`

### Purpose
Định nghĩa “minimum imported project outputs” để project được coi là startup-usable trong AICOS.

### Checklist blocks

### Checklist Code: KIT-26264

#### A. Canonical minimum
- [ ] `project-brief.md`
- [ ] `product-goals.md`
- [ ] `architecture-baseline.md`
- [ ] `source-limits.md` *(nếu thực sự cần)*
- [ ] `data-scope.md` *(nếu thực sự cần)*
- [ ] `pipeline-baseline.md` *(nếu thực sự cần)*

#### B. Working minimum
- [ ] `current-state.md`
- [ ] `current-direction.md`
- [ ] `handoff/current.md`
- [ ] `open-questions.md`
- [ ] `open-items.md`
- [ ] `active-risks.md`

#### C. Evidence minimum
- [ ] source inventory file
- [ ] import note
- [ ] slice note
- [ ] delivery/reference surface note

#### D. A1 minimum
- [ ] project packet index
- [ ] first review/import packet
- [ ] startup/context validation packet
- [ ] optional continuation packet if needed

### Rule
Nếu bootstrap outputs chưa đủ thì imported project chưa được coi là “usable enough”.

---

## 11. Shared Template 7 — A1 Import Startup Template

### File
`brain/shared/templates/project-import-kit/a1-import-startup-template.md`

### Purpose
Định nghĩa A1 startup surfaces tối thiểu cho một imported project.

### Required sections

#### A. Startup entry
- expected `./aicos context start ...`
- scope
- role
- project id

#### B. Startup reading boundary
- what is read by default
- what is not read by default
- packet-first condition
- when handoff/current is required

#### C. First packet surfaces
- first review/import packet
- startup validation packet
- optional continuation packet
- packet index path

#### D. Continuity expectation
- working files to trust
- handoff file to trust
- when second A1 can continue
- what must exist before continuation is considered cheap

### Rule
Imported project chỉ thực sự usable cho A1 khi startup path được viết rõ.

---

## 12. Shared Template 8 — Import Validation Template

### File
`brain/shared/templates/project-import-kit/import-validation-template.md`

### Purpose
Checklist để xác nhận import đã usable hay chưa.

### Validation categories

#### A. Startup sufficiency
- [ ] A1 mới có hiểu project là gì không?
- [ ] A1 mới có nhận ra first slice không?
- [ ] A1 mới có tìm được packet đúng mà không broad-load không?

#### B. Startup efficiency
- [ ] startup có còn light không?
- [ ] archive/history có nằm ngoài hot path không?
- [ ] packet-first có còn đúng không?

#### C. Rule compatibility
- [ ] A1 có biết rule layers nào apply không?
- [ ] project / work_context / task có tách bạch không?

#### D. Continuity quality
- [ ] A1 thứ hai có tiếp tục rẻ không?
- [ ] `handoff/current.md` có đủ không?
- [ ] task continuity metadata có đủ không?

#### E. Authority integrity
- [ ] external repo vẫn giữ code/runtime authority không?
- [ ] AICOS có giữ context/control-plane authority không?
- [ ] imported truth có bị lẫn với raw reference docs không?

#### F. Import discipline
- [ ] có import quá nhiều không?
- [ ] có mirror external repo structure quá literally không?
- [ ] có kéo broad code internals quá sớm không?

### Rule
Import không nên được coi là complete nếu validation chưa được ghi lại.

---

## 13. Recommended Project Instantiation Pattern

Sau khi shared kit tồn tại, mỗi project cụ thể sẽ instantiate thành một cụm file riêng.

### Suggested project-specific home

```text
brain/projects/<project-id>/evidence/import-kit/
```

### Suggested instantiated files

For any project:

- `import-master-checklist.md`
- `import-identity.md`
- `source-inventory.md`
- `authority-and-lane-mapping.md`
- `slice-definition.md`
- `bootstrap-output-checklist.md`
- `a1-import-startup.md`
- `import-validation.md`

### Why use one dedicated folder
File kit cũ dùng nhiều locations gần đúng, nhưng với import-kit instantiated thì nên có **một cụm rõ ràng** để:
- agent mới tìm dễ hơn
- Codex update có thứ tự hơn
- tránh rải rác import files vào quá nhiều folders

### Rule
Đây là **evidence/import execution cluster**, không phải authority replacement.
Canonical/working truth sau khi digest vẫn sống ở lanes chuẩn của project.

---

## 14. Recommended Minimal Deliverable For `sample-project`

Khi Codex áp dụng kit này cho sample project, bộ instantiated files nên tối thiểu gồm:

```text
brain/projects/sample-project/evidence/import-kit/
  import-master-checklist.md
  import-identity.md
  source-inventory.md
  authority-and-lane-mapping.md
  slice-definition.md
  bootstrap-output-checklist.md
  a1-import-startup.md
  import-validation.md
```

### Notes
- các file đã có như `evidence/source-inventory/import-plan.md` hoặc
  `evidence/workstreams/default-sample-workstream-delivery-slice.md` có thể được:
  - giữ lại
  - hoặc được absorb/reference bởi import-kit cluster mới
- không cần xóa vội nếu chúng vẫn hữu ích
- nhưng import execution cluster nên là cụm theo dõi chính cho pass thực thi

---

## 15. Recommended Codex Implementation Order

### Phase 1 — Create shared kit
Codex tạo đủ 8 shared templates ở:

```text
brain/shared/templates/project-import-kit/
```

### Phase 2 — Do not automate yet
Không build generator/script/MCP automation ở pass này.

### Phase 3 — Instantiate for sample project
Dùng kit để tạo import-kit cluster cho:

```text
projects/sample-project
```

### Phase 4 — Execute real import pass
Sau khi instantiated kit rõ ràng:
- complete source inventory
- digest selected truth
- refine A1 startup
- validate import quality

### Rule
Shared template first, project instantiation second, real import execution third.

---

## 16. What Codex Should Avoid

### Checklist Code: KIT-26265

- [ ] không làm templates sample project-specific
- [ ] không giả định mọi project đều là code-first
- [ ] không giả định mọi project đều có same startup surfaces
- [ ] không nhét MCP server implementation vào import kit
- [ ] không tạo huge empty folder tree
- [ ] không mirror external repo path structure quá literally
- [ ] không biến import kit thành workflow engine lớn
- [ ] không cố auto-generate mọi thứ trước khi first real import được validate

---

## 17. What Codex Should Preserve

### Checklist Code: KIT-26266

- [ ] preserve packet-first discipline
- [ ] preserve startup-light discipline
- [ ] preserve authority separation
- [ ] preserve AICOS lane semantics
- [ ] preserve artifact-neutral wording
- [ ] preserve future reusability for company/workspace expansion
- [ ] preserve the option to later semi-automate once the kit proves useful

---

## 18. Definition Of Done

Import Kit template pass chỉ được coi là complete khi:

- [ ] shared template set exists in a coherent shared lane
- [ ] each template has one clear purpose
- [ ] template wording is project-neutral
- [ ] kit is immediately usable for `sample-project`
- [ ] kit is reusable for a different future project
- [ ] instantiated project import cluster becomes obvious
- [ ] no MCP runtime or large automation leaked into this pass

---

## 19. Final Operating Rule

Import Kit phải làm cho project import trở nên:

- repeatable
- bounded
- explainable
- startup-usable
- continuity-friendly
- future semi-automatable

mà **không** biến AICOS thành một import framework quá lớn trước khi first real project test chứng minh cái gì thực sự cần.

---
