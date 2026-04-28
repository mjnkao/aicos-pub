# PLN-26215 — AICOS Plan To Reach Real-Project Readiness Using A Crypto Trading Project

**Status:** working-plan-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** lưu lại đầy đủ phân tích và kế hoạch triển khai tiếp theo cho AICOS, trong bối cảnh mục tiêu không còn chỉ là hoàn thiện kiến trúc nội bộ, mà là **đưa một dự án thật vào AICOS** để kiểm tra xem hệ thống có thực sự dùng được hay không.

---

## 1. Bối cảnh và mục tiêu thực tế

Mục tiêu mới của phase này là:

- chọn một **dự án thật** đang tồn tại sẵn
- cụ thể trước mắt là **Crypto Trading project**
- đọc dự án đó từ nguồn hiện có
- chuyển toàn bộ context quan trọng của dự án đó vào AICOS theo tiêu chuẩn đã xây
- sau khi chuyển đổi xong, cho agents như **Codex** hoặc **Claude Code** vào làm việc trực tiếp trên dự án đó
- kiểm tra bằng usage thật:
  - có lấy đủ context không
  - có load nhanh không
  - có tốn token không
  - có làm theo các quy tắc đã xây không
  - continuity giữa actors có tốt không

### Kết luận

AICOS chỉ thật sự chứng minh được giá trị khi chạy trên **một dự án thật**, không phải chỉ trên chính AICOS.

---

## 2. Tại sao cần chuyển sang dự án thật ở thời điểm này

AICOS hiện đã đi khá xa ở mức hệ thống lõi:

- active root mới đã được ổn định ở mức nền
- self-brain cho chính AICOS đã có
- handoff model H1 / H2 / H3 đã có
- packet-first và index-first startup đã có
- `./aicos context start` đã có ở mức MVP
- `./aicos sync brain` và `./aicos option choose` đã có flow thật
- lane semantics giữa `brain/`, `agent-repo/`, `backend/`, `serving/` đã rõ hơn nhiều
- handoff-ready task metadata đang đi theo hướng mỏng, không tạo subsystem thừa

### Nhưng vẫn còn một khoảng trống lớn

AICOS mới chủ yếu được kiểm thử bằng:

- self-application trên chính repo AICOS
- local packet-first tests
- bounded flow tests

Điều này tốt, nhưng chưa đủ để trả lời các câu hỏi quan trọng nhất:

- A1 có thể dùng AICOS cho một project thật không?
- project lớn hơn có bị load chậm / nặng token không?
- rules có thực sự được agent tuân thủ khi làm việc thật không?
- continuity có còn tốt khi đổi actor không?
- lane semantics có đủ rõ dưới áp lực usage thật không?

### Vì vậy

Đưa **Crypto Trading project** vào AICOS là bước rất hợp lý để:

- kiểm tra thiết kế bằng usage thật
- phát hiện những chỗ còn mơ hồ
- ưu tiên nâng cấp AICOS dựa trên friction thật, không phải suy đoán

---

## 3. Điều kiện để có thể đưa dự án thật vào AICOS

Để đạt mức có thể onboard và chạy một project thật, AICOS cần đủ 4 lớp:

### 3.1. Lõi continuity và discipline đủ ổn
Bao gồm:

- checkpoint/writeback discipline
- handoff discipline
- task-state convention
- packet-first startup ổn định hơn
- actor/task continuity đủ dùng

### 3.2. Nhánh A1 tối thiểu nhưng dùng được
Vì khi chạy dự án thật, không thể chỉ có A2-Core.

Cần có tối thiểu:

- A1 role/startup card
- A1 rule cards cơ bản
- A1 task/startup conventions
- A1 task lanes đủ dùng

### 3.3. Chuẩn import/onboarding project vào AICOS
Phải có cách rõ ràng để:

- đọc dự án hiện có
- map tài liệu và context vào các lane của AICOS
- sinh current state / current direction / handoff bootstrap
- không biến import thành việc copy file rối loạn

### 3.4. Kế hoạch test usage thật
Phải biết trước sẽ đánh giá theo gì:

- context sufficiency
- context efficiency
- rule compliance
- continuity quality
- operational friction

---

## 4. Những việc quan trọng cần làm để đạt mức chạy dự án thật

## 4.1. Nhóm A — Chốt AICOS core discipline

Đây là nhóm phải làm trước tiên.

### A1. Mandatory checkpoint / writeback discipline

Phải chốt rõ:

- khi nào actor bắt buộc checkpoint
- khi nào phải update project working state
- khi nào phải update actor task state
- khi nào phải update handoff current
- khi nào nên commit
- khi nào phải push

### Vì sao đây là ưu tiên số 1

Nếu không có checkpoint discipline:

- actor sẽ làm quá xa trong session riêng
- continuity sẽ chỉ nằm trong chat/thread
- actor khác vào sẽ phải dựng lại context
- bài test trên dự án thật sẽ cho kết quả nhiễu

---

### A2. Task-state convention

Phải chuẩn hóa tối thiểu trong actor task lanes:

- current owner
- status
- blocked reason
- next step
- continuation mode
- handoff refs
- handoff readiness
- checkpoint markers nếu cần

### Vì sao cần

Task continuity hiện đã có nền, nhưng nếu task-state vẫn lỏng thì continuity giữa actors vẫn tốn công.

---

### A3. `context start` hardening

MVP `./aicos context start` đã có, nhưng trước khi sang dự án thật nên làm nó ổn hơn ở mức:

- output ngắn, nhất quán
- packet index / summaries rõ hơn
- guidance “nếu chưa có task thì chỉ ở mức orientation” rõ hơn
- không kéo agent load thừa

### Vì sao cần

Đây là cổng vào chính của bài test “load nhanh, đủ context, ít tốn token”.

---

## 4.2. Nhóm B — Mở nhánh A1 tối thiểu

Không cần full A1 ecosystem ngay, nhưng cần **minimum viable A1 branch**.

### B1. A1 role/startup card

Phải giúp A1 biết:

- mình là ai
- đang làm trên project reality nào
- phải đọc gì trước
- không được làm gì
- khi nào escalate sang A2

### B2. A1 rule cards cơ bản

Tối thiểu nên có:

- writeback / checkpoint rule
- handoff/continuation rule
- task packet loading rule
- project/open items/open questions/risk handling rule
- escalation-to-A2 rule

### B3. A1 task/startup conventions

Phải chốt:

- A1 task packets có theo template hiện có hay cần specialization nhẹ
- A1 startup có packet-first như A2 không
- A1 current/backlog/blocked/waiting lanes ở đâu
- A1 task continuity và project continuity tương tác ra sao

### Kết luận

Chưa có A1 artifacts tối thiểu thì chưa thể nói AICOS “sẵn sàng cho dự án thật”.

---

## 4.3. Nhóm C — Chuẩn import/onboarding project thật

### C1. Project import checklist

Phải có checklist trả lời:

- project id là gì
- scope là gì
- nguồn hiện có là gì
- canonical docs là gì
- working docs là gì
- current direction là gì
- open questions / open items / risks / research là gì
- branches / experiments hiện có là gì
- handoff bootstrap phải sinh ra là gì

### C2. Mapping spec từ dự án cũ → AICOS lanes

Dự án Crypto Trading hiện có thể nằm ở nhiều dạng:

- repo code
- markdown docs
- JSON packages
- trading memos
- prompt files
- scripts
- outputs
- analysis packages

Cần map vào:

- `brain/projects/<project_id>/canonical/`
- `brain/projects/<project_id>/working/`
- `brain/projects/<project_id>/evidence/`
- `brain/projects/<project_id>/branches/`
- `agent-repo/.../tasks/...`

### C3. Initial bootstrap state for the imported project

Sau import phải có ngay:

- `current-state.md`
- `current-direction.md`
- `handoff/current.md`
- `open-questions.md`
- `open-items.md`
- `active-risks.md`
- packet index / task packet bootstrap nếu cần

Nếu không có bước này, import chỉ là chép dữ liệu chứ chưa phải onboarding vào AICOS.

---

## 4.4. Nhóm D — Test usage thật

### D1. Startup speed and token discipline test

Mục tiêu:

- agent mới vào có load đủ nhanh không
- có load thừa không
- packet-first có giúp giảm startup burden thật không

### D2. Rule compliance test

Mục tiêu:

- agent có tuân thủ checkpoint/writeback/handoff/task rules không
- có update đúng lane không

### D3. Continuity under interruption test

Mục tiêu:

- Codex làm dở rồi dừng
- Claude Code vào tiếp
- continuity có còn rẻ không
- actor mới có phải rebuild quá nhiều không

### D4. Real task quality test

Mục tiêu:

- agent có hiểu đủ context của Crypto Trading project để làm task thật không
- có sai vì thiếu context không
- có phải hỏi lại quá nhiều không

---

## 5. Vì sao phải làm A1 trước khi onboard Crypto Trading

A2-Core chỉ sửa AICOS.  
Crypto Trading là **một project thật**, nên actor chính làm việc trên project đó phải là **A1**.

Nếu chưa có A1 artifacts:

- project import xong vẫn chưa có ai dùng đúng lane để làm việc
- Codex/Claude có thể vẫn làm như A2-Core, gây lẫn giữa “sửa AICOS” và “làm project work”
- bài test sẽ không phản ánh đúng intended usage của AICOS

### Kết luận

**A1 minimum viable branch là điều kiện bắt buộc trước khi test thật.**

---

## 6. Vì sao nên onboard theo “một slice” của Crypto Trading trước

Không nên import toàn bộ project thật ngay từ đầu.

### Nên làm:
- chọn một **slice đủ thật nhưng không quá rộng**
- import slice đó trước
- chạy agents trên slice đó
- đo friction và context quality
- rồi mới mở rộng

### Lợi ích
- dễ debug
- dễ biết lỗi ở đâu
- tránh scope quá lớn làm hỏng bài test

### Ví dụ slice phù hợp
Tùy dự án cụ thể, có thể chọn:

- một workflow memo cụ thể
- một analysis pipeline cụ thể
- một module ra quyết định cụ thể
- một subproject đã có docs tương đối rõ

---

## 7. Các tiêu chí đánh giá phải chốt trước

## 7.1. Context sufficiency
Agent có đủ context để làm đúng không?

## 7.2. Context efficiency
Agent có load quá nhiều / tốn token quá mức không?

## 7.3. Rule compliance
Agent có ghi đúng, đủ, đúng lane không?

## 7.4. Continuity quality
Actor khác có thể tiếp tục rẻ không?

## 7.5. Operational friction
Human có phải cứu tay quá nhiều không?

---

## 8. Thứ tự triển khai khuyến nghị

### Phase 1 — core discipline hardening
1. checkpoint/writeback policy
2. task-state convention
3. `context start` hardening

### Phase 2 — minimum viable A1
4. A1 startup card
5. A1 rule cards
6. A1 task/startup conventions

### Phase 3 — Crypto Trading onboarding standard
7. project import checklist
8. mapping spec from legacy/current project materials into AICOS lanes
9. bootstrap current-state/current-direction/handoff for imported project

### Phase 4 — real project test
10. startup/token test
11. rule compliance test
12. continuity under interruption test
13. real task quality test

### Phase 5 — improve AICOS from real usage
14. capture friction
15. refine lanes / packets / startup / policies
16. decide next A2-Serve or registry improvements only after real evidence

---

## 9. Những việc chưa nên làm ngay

Để tránh overbuild, chưa nên ưu tiên:

- full A2-Serve runtime
- UI
- public API
- large DB-first ownership model
- broad migration of all backups
- full takeover/transfer engine
- complex orchestration runtime

---

## 10. Kết luận cuối

AICOS đã đủ xa để chuyển từ “thiết kế cho chính nó” sang “kiểm chứng bằng dự án thật”.

Để làm được việc đó, ba trụ quan trọng nhất bây giờ là:

1. **checkpoint/writeback discipline**
2. **minimum viable A1 branch**
3. **project onboarding/import standard cho Crypto Trading**

Sau khi ba trụ này đủ ổn, việc đưa một **Crypto Trading project slice** vào AICOS và cho **Codex / Claude Code** làm thật sẽ là bước kiểm tra có giá trị nhất để nâng cấp AICOS tiếp theo.

---
