# FRM-26298 — AICOS Workstream Suggestion Framework

**Status:** framework-brief-v1  
**Project:** AICOS  
**Date:** 2026-04-19  
**Primary scope:** generic project-facing framework  
**Purpose:** cung cấp một framework gợi ý chung để các project sử dụng AICOS có thể:
- đề xuất tạo workstream mới khi thật sự cần
- giữ `workstream_index` chất lượng cao
- tránh lẫn lộn giữa workstream, task, packet, phase, và note ngắn
- gửi proposal về AICOS theo format thống nhất

---

## 1. Core Principle

AICOS **không tạo workstream thay cho project**.

AICOS chỉ:
- cung cấp **framework gợi ý**
- cung cấp **format proposal**
- cung cấp **tool đọc/ghi** phù hợp nếu project chọn sử dụng
- giúp project giữ routing/context discipline tốt hơn

### Decision ownership
Việc:
- có tạo workstream mới hay không
- gộp vào workstream cũ
- chỉ giữ ở mức task

là quyết định của **project scope**.

A1 có thể:
- đọc workstream hiện có
- nhận thấy lane hiện tại không đủ
- gửi proposal về AICOS theo đúng format

AICOS không tự áp đặt.

---

## 2. What A Workstream Is

Workstream là một **lane làm việc có thể quản lý độc lập**, không phải:
- một task ngắn
- một packet
- một file
- một phase nhỏ một lần

Một workstream tốt thường có:
- mục tiêu riêng
- entry path riêng
- input/source riêng
- output/artifact riêng
- rule/authority emphasis riêng
- khả năng lặp lại hoặc kéo dài theo thời gian

---

## 3. What A Workstream Is Not

Không nên coi là workstream nếu đó chỉ là:
- một lần check ngắn
- một bounded validation task
- một fix nhỏ
- một note mới
- một packet mới nhưng vẫn nằm trong cùng lane
- một bước con tạm thời của workstream hiện có

---

## 4. When A1 Should Suggest A New Workstream

A1 chỉ nên đề xuất workstream mới khi thỏa cả 3 điều kiện bắt buộc dưới đây.

### 4.1. Distinct purpose
Lane mới có mục tiêu khác bản chất so với lane hiện tại.

### 4.2. Distinct entry path
Lane mới cần entry path/hot path khác đáng kể:
- file/surface khác
- context khác
- packet nhóm khác
- artifact nhóm khác

### 4.3. Expected recurrence or persistence
Lane mới không phải việc một lần.
Nó có khả năng:
- lặp lại
- kéo dài
- hoặc trở thành một lane ổn định của project

---

## 5. Strengthening Signals

Nếu đã thỏa 3 điều kiện bắt buộc ở trên, proposal sẽ mạnh hơn nếu có thêm từ 2 dấu hiệu trở lên:

- output/artifact khác rõ
- cadence khác rõ
- rule/authority emphasis khác
- handoff riêng giữa actors có ích rõ ràng
- packet hiện tại không route đủ tốt
- agent đã bị lẫn lane từ 2 lần trở lên
- đã có ít nhất 2 task liên tiếp thực chất cùng xoay quanh lane mới này

---

## 6. When A1 Should Not Suggest A New Workstream

A1 không nên đề xuất nếu:
- việc đó vẫn xử lý tốt trong workstream hiện tại
- chỉ là task con
- chưa có bằng chứng lặp lại
- output không khác rõ
- chỉ vì packet hiện tại viết chưa rõ
- chỉ vì actor chưa đọc kỹ routing hiện tại

Trong các trường hợp này:
- ưu tiên refine packet
- refine handoff
- refine current direction
- hoặc chỉ giữ ở mức task

---

## 7. Minimal Proposal Format

### Report Code: FRM-26299

Nếu A1 thấy cần đề xuất workstream mới, proposal nên theo format tối thiểu sau:

```yaml
scope: "projects/<project-id>"
proposed_workstream_id: "<short-stable-id>"
title: "<short human-readable title>"

distinct_purpose: "<one sentence>"
distinct_entry_path: "<main files/surfaces/routes>"
expected_recurrence: "<why this will recur or persist>"

why_not_current_lane:
  - "<reason 1>"
  - "<reason 2>"

inputs:
  - "<source/input 1>"
  - "<source/input 2>"

expected_outputs:
  - "<artifact/output 1>"
  - "<artifact/output 2>"

authority_emphasis:
  context_control_plane: "AICOS | mixed | project-specific"
  code_runtime: "<repo/runtime authority if relevant>"

routing_hints:
  likely_packets:
    - "<packet-id>"
  likely_writeback:
    - "<lane or working surface>"
  likely_artifacts:
    - "<artifact kind>"

confidence: "low|medium|high"
```

### Rule
Proposal phải ngắn, rõ, và thực dụng.
Không cần prose dài.

---

## 8. Review Outcomes

Mọi workstream proposal nên dẫn đến một trong 4 kết quả rõ ràng.

### A. Accept as new workstream
Tạo workstream mới là hợp lý.

### B. Merge into existing workstream
Không cần lane mới; chỉ cần route đúng vào lane đang có.

### C. Keep as task only
Chưa đủ để tách workstream.

### D. Defer
Có thể đúng, nhưng chưa đủ evidence.

---

## 9. Minimum Quality For A Workstream Index Entry

Nếu project chấp nhận tạo workstream mới, index của nó nên có tối thiểu:

### Checklist Code: FRM-26300

- `workstream_id`
- `title`
- `purpose`
- `when_to_use`
- `when_not_to_use`
- `main_entry_surfaces`
- `typical_packets`
- `typical_outputs`
- `default_writeback_lanes`
- `status: candidate|active|paused|deprecated`

---

## 10. Relationship To Packet Index

`packet_index` và `workstream_index` không giống nhau.

### `packet_index`
- execution-facing
- nói: có packet nào để chạy

### `workstream_index`
- routing/context-facing
- nói: có lane nào để đi, lane đó dùng khi nào

Một workstream có thể có:
- nhiều packet
- nhiều artifacts
- nhiều actors chạm vào

Vì vậy packet index không thay thế workstream index.

---

## 11. Relationship To Current Direction

`current_direction` và `workstream_index` cũng không giống nhau.

### `current_direction`
Trả lời:
- nên ưu tiên lane/hướng nào bây giờ

### `workstream_index`
Trả lời:
- project có những lane nào tất cả
- mỗi lane là gì
- lane nào dùng khi nào

Direction là ưu tiên hiện tại.
Workstream index là bản đồ lanes.

---

## 12. AICOS Responsibility Boundary

AICOS nên làm:
- đưa ra framework gợi ý
- đưa ra format proposal
- cung cấp MCP read/write surfaces khi project dùng
- giúp route và giữ context discipline

AICOS không nên:
- tự đứng ra tạo workstream thay project
- tự suy luận lane mới rồi promote thành active lane mà không có project-level decision
- biến mình thành manager trung tâm cứng cho tất cả project

---

## 13. Suggested MCP Relationship

Về lâu dài, project có thể dùng MCP theo mô hình sau:

### Read side
- `aicos_get_workstream_index` để đọc lane map
- `aicos_query_project_context` để hỏi lane/context phù hợp
- các tool packet/startup/handoff hiện có để thực thi

### Write side
Workstream proposal không cần generic raw file write.
Project có thể gửi proposal như:
- working item
- artifact ref
- hoặc proposal note structured

AICOS chỉ cần đảm bảo proposal vào đúng lane và đúng format.

---

## 14. Future Extension Principle

Framework này là **generic base framework**.

Các loại suggestion framework khác về sau có thể mở rộng theo cùng pattern, ví dụ:
- packet suggestion framework
- canonical promotion suggestion framework
- artifact classification suggestion framework

### Important
AICOS không cần build tất cả ngay.
Nên bổ sung dần theo thời gian khi project needs đủ rõ.

---

## 15. Final Rule

### Final rule

A1 chỉ nên đề xuất workstream mới khi:
- có mục tiêu riêng
- có entry path riêng
- có tính lặp lại hoặc kéo dài
- và đã có đủ evidence rằng nếu không tách lane thì routing sẽ tiếp tục rối

AICOS cung cấp framework và tool support.
Project giữ quyền quyết định có tách workstream hay không.

---
