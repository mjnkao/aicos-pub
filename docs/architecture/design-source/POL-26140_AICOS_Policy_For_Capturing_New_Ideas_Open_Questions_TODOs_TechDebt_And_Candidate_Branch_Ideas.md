# POL-26140 — AICOS Policy For Capturing New Ideas, Open Questions, TODOs, Tech Debt, and Candidate Branch Ideas

**Status:** implementation-policy-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** hướng dẫn Codex tạo policy rõ ràng để xử lý các idea mới phát sinh từ human hoặc agents trong quá trình làm việc, sao cho:
- không bị mất idea
- không làm loạn self-brain của AICOS
- biết idea nào nên vào `open questions`
- biết idea nào nên vào `todo/backlog`
- biết idea nào là `candidate branch idea`
- biết khi nào cần ghi vào `active risks`

---

## 1. Mục tiêu của policy này

Trong quá trình làm việc trên AICOS, rất thường xuyên sẽ phát sinh:

- idea mới từ human
- idea mới từ A1
- idea mới từ A2
- ý tưởng rẽ nhánh mới nhưng chưa triển khai
- câu hỏi kiến trúc mới
- tech debt mới
- việc cần làm sau nhưng chưa làm ngay
- hướng cải tiến mới nhưng chưa đủ rõ để commit

Nếu không có policy rõ ràng, hệ sẽ bị một trong hai lỗi:

### Lỗi 1 — làm mất idea
- ý hay được nói ra trong chat nhưng không lưu
- sau đó quên mất
- phải nghĩ lại từ đầu

### Lỗi 2 — làm loạn working state
- mọi idea nhỏ đều bị nhét vào `current-state`
- file working trở thành nơi chứa mọi thứ
- startup context bị nặng và lẫn

### Kết luận

AICOS cần một policy đơn giản:

> Không để mất idea, nhưng cũng không ghi mọi idea vào working state.

---

## 2. Principle cốt lõi

### Principle 1

Không phải mọi idea mới đều là working state.

### Principle 2

Idea mới chỉ nên được ghi vào lane phù hợp với bản chất của nó.

### Principle 3

`working/current-state.md` không phải inbox cho mọi idea.

### Principle 4

Chỉ các ý tưởng đủ quan trọng, ổn định, hoặc liên quan tới hướng làm hiện tại mới được phản ánh vào working state chính.

### Principle 5

Idea nhỏ, idea chưa chín, hoặc idea để review sau phải đi vào lane nhẹ hơn:
- open questions
- backlog / todo
- candidate branch ideas
- active risks nếu thật sự là risk

---

## 3. Các loại idea mới cần phân biệt

## 3.1. Open Question

Đây là các idea có bản chất là **câu hỏi chưa chốt**.

### Ví dụ

- Có nên thêm command `aicos option choose` không?
- Có nên activate A2-Serve ở phase này không?
- Có nên canonicalize `architecture.md` chưa?
- Có nên dùng GStack cho A2-C ở bước tiếp theo không?

### Rule

Nếu một idea mới có bản chất là:

- vấn đề còn mở
- cần quyết định sau
- chưa đủ rõ để biến thành task cụ thể ngay
- cần review sau

thì nên ghi vào:

- `brain/projects/aicos/working/open-questions.md`

---

## 3.2. TODO / Backlog Item

Đây là các idea đã đủ rõ để trở thành **việc cần làm**, nhưng chưa làm ngay.

### Ví dụ

- thêm full JSON Schema validation
- thêm MCP stdio wrapper riêng cho AICOS
- dọn lại naming của packets
- viết helper command cho review packet
- làm cleanup lane cho migration notes

### Rule

Nếu một idea mới có bản chất là:

- việc rõ ràng
- có thể làm thành task
- không nhất thiết làm ngay
- phù hợp để review trong planning sau

thì nên ghi vào:

- `agent-repo/classes/a2-service-agents/tasks/backlog/`
hoặc
- queue/backlog lane tương ứng của A2

### Important note

TODO/backlog **không nên** đổ vào `working/current-state.md` trừ khi nó đang là active priority.

---

## 3.3. Candidate Branch Idea

Đây là các idea kiểu:

- có thể rẽ nhánh theo hướng này
- có thể thử một MVP option khác
- có thể có branch experiment mới
- có một hướng kiến trúc thay thế nhưng chưa quyết định triển khai

### Ví dụ

- có thể tạo branch “sync-brain-real-import” thay vì tiếp tục preflight
- có thể tạo branch “thin-mcp-wrapper-first”
- có thể thử một branch riêng cho A2-Serve skeleton
- có thể thử tách branch compare policy ra khỏi current package

### Rule

Nếu một idea mới có bản chất là:

- branch/experiment idea
- hướng thử nghiệm tiềm năng
- chưa được manager chọn
- chưa được activate

thì **không** ghi ngay thành active branch reality trong `brain/projects/aicos/branches/`.

Thay vào đó nên ghi vào một lane nhẹ hơn, ví dụ:

- `brain/projects/aicos/working/open-questions.md` nếu nó vẫn là câu hỏi chiến lược
- hoặc
- `brain/projects/aicos/evidence/candidate-decisions/`
- hoặc
- `brain/projects/aicos/evidence/friction/` nếu nó xuất phát từ một pain point rõ

### Rule đơn giản

Chỉ khi human/manager hoặc agent flow thực sự quyết định “hãy thử branch này” thì mới tạo branch reality chính thức.

---

## 3.4. Tech Debt Item

Tech debt là một loại đặc biệt.

### Ví dụ

- command hoạt động nhưng code đang rất tạm
- validator mới là check nhẹ
- sync brain mới là preflight
- naming/folder contract chưa sạch
- service logic đang bị hardcode quá mức tạm thời

### Rule

Nếu tech debt:

- chưa ảnh hưởng ngay tới current flow
- không block trực tiếp bước hiện tại

thì ghi vào:

- `agent-repo/classes/a2-service-agents/tasks/backlog/`
và nếu cần:
- thêm một dòng ngắn trong `brain/projects/aicos/working/open-questions.md`

Nếu tech debt:

- đang ảnh hưởng trực tiếp tới current flow
- có nguy cơ làm sai architecture
- có thể gây drift lớn

thì ghi vào:

- `brain/projects/aicos/working/active-risks.md`

### Câu chốt

Tech debt nhỏ -> backlog  
Tech debt có risk kiến trúc hoặc operational rõ -> active risks

---

## 3.5. Active Risk

Một idea mới chỉ nên vào `active-risks.md` nếu nó thật sự là risk.

### Ví dụ

- self-brain đang quá dài
- lẫn A1/A2 role
- sync brain chưa active nên retrieval bị lệch
- backend có nguy cơ bị hiểu thành truth
- service logic bị hardcode quá sớm

### Rule

Không phải mọi tech debt hay idea đều là risk.

Chỉ ghi vào:

- `brain/projects/aicos/working/active-risks.md`

nếu có đủ 3 yếu tố:

1. có khả năng gây hại thật
2. có impact rõ
3. cần được theo dõi trong current phase

---

## 4. Policy quyết định “ghi vào đâu”

### Table Code: POL-26141

| Loại phát sinh | Ghi vào đâu |
|---|---|
| câu hỏi còn mở, chưa chốt | `brain/projects/aicos/working/open-questions.md` |
| việc rõ ràng nhưng để làm sau | `agent-repo/classes/a2-service-agents/tasks/backlog/` |
| idea branch/experiment nhưng chưa được chọn | `brain/projects/aicos/evidence/candidate-decisions/` hoặc `open-questions.md` |
| tech debt nhỏ, chưa block hiện tại | `agent-repo/classes/a2-service-agents/tasks/backlog/` |
| tech debt có impact/risk rõ | `brain/projects/aicos/working/active-risks.md` |
| decision đã chốt | lane tương ứng trong `working/` hoặc approval/branch state |
| branch đã được chọn để thử thật | `brain/projects/aicos/branches/<branch-id>/` |

---

## 5. Policy theo mode làm việc

## 5.1. Interactive mode

Khi human đang online và chat liên tục với agent:

### Không nên làm

- không ghi mọi idea nhỏ ngay vào brain
- không update working file sau mỗi chat turn
- không biến brainstorming noise thành state thật

### Nên làm

Agent nên giữ idea tạm trong:

- session scratch
- runtime note
- local temporary note

Sau đó chỉ khi đến một **commit point** thì mới quyết định ghi vào lane phù hợp.

### Commit point examples

- câu hỏi mới đủ quan trọng để review sau
- tech debt mới được xác nhận là có thật
- một todo mới đã đủ rõ để cho vào backlog
- một candidate branch idea đã đủ rõ để note lại
- một risk mới đã đủ rõ để track

---

## 5.2. Async mode

Khi agent làm việc mà không có human online trực tiếp:

### Nên làm

Agent có thể ghi chủ động hơn, nhưng vẫn phải chọn đúng lane.

Ví dụ:

- blocker confirmed -> working state
- options ready -> option packet
- waiting for decision -> blocked/waiting lane
- new branch idea not yet selected -> candidate-decisions hoặc open-questions
- new tech debt found -> backlog hoặc active-risks

### Không nên làm

- tạo branch reality đầy đủ cho mọi branch idea mới nếu chưa có quyết định thử
- nhét mọi observation vào current-state

---

## 6. Policy “ghi ít nhưng không mất”

Đây là policy đơn giản nhất mà Codex phải áp dụng.

### Rule A

Nếu idea mới chỉ là thought nhỏ, chưa đủ ổn định:

- không ghi vào self-brain ngay

### Rule B

Nếu idea mới có giá trị review sau:

- ghi vào `open-questions.md` hoặc backlog tương ứng

### Rule C

Nếu idea mới là branch idea nhưng chưa activate:

- ghi là candidate branch idea
- chưa tạo branch reality chính thức

### Rule D

Nếu idea mới là task rõ ràng:

- ghi backlog / todo

### Rule E

Nếu idea mới là risk có impact rõ:

- ghi `active-risks.md`

---

## 7. Hướng dẫn viết ngắn gọn

Các file brain/working phải giữ ngắn.

### 7.1. Với open questions

Mỗi item nên viết ngắn:

- câu hỏi
- vì sao nó quan trọng
- trạng thái hiện tại (optional)

### 7.2. Với backlog/todo

Mỗi item nên viết ngắn:

- task title
- 1 dòng mô tả
- priority (optional)

### 7.3. Với candidate branch ideas

Mỗi item nên viết ngắn:

- idea branch là gì
- vì sao có idea này
- chưa active / chờ review

### 7.4. Với active risks

Mỗi item nên có:

- risk
- impact
- mitigation hiện tại

---

## 8. Yêu cầu cụ thể cho Codex

Codex phải biến policy này thành thực tế trong repo AICOS.

### Checklist Code: POL-26142

- [ ] review current self-brain files and avoid turning them into idea inboxes
- [ ] ensure new questions are routed to `brain/projects/aicos/working/open-questions.md`
- [ ] ensure actionable deferred work is routed to A2 backlog/task lane
- [ ] ensure candidate branch ideas are not auto-created as real branches
- [ ] ensure tech debt is split between backlog vs active-risks based on impact
- [ ] add or update lightweight files/folders if needed for candidate decisions
- [ ] update role/startup docs if the reading order or policy needs to mention these lanes
- [ ] keep all brain summaries concise and in Vietnamese with proper diacritics

---

## 9. Đề xuất nơi ghi cụ thể trong repo hiện tại

Codex nên dùng các nơi sau.

### 9.1. Open questions

- `brain/projects/aicos/working/open-questions.md`

### 9.2. Active risks

- `brain/projects/aicos/working/active-risks.md`

### 9.3. A2 backlog / todo

- `agent-repo/classes/a2-service-agents/tasks/backlog/`

### 9.4. Candidate decisions / candidate branch ideas

Nếu chưa có lane rõ, Codex nên tạo nhẹ:

- `brain/projects/aicos/evidence/candidate-decisions/`

Có thể bắt đầu bằng một file index ngắn, ví dụ:

- `brain/projects/aicos/evidence/candidate-decisions/README.md`
- hoặc `brain/projects/aicos/evidence/candidate-decisions/candidate-branch-ideas.md`

### Rule

Không overbuild nhiều file nhỏ ngay.  
Có thể bắt đầu bằng 1 file index gọn, sau đó tách dần nếu thực sự cần.

---

## 10. Những điều Codex không được làm

### Checklist Code: POL-26143

- [ ] do not write every new idea into `working/current-state.md`
- [ ] do not turn `open-questions.md` into a giant messy note dump
- [ ] do not create official branch realities for branch ideas that are not yet approved
- [ ] do not put every tech debt item into `active-risks.md`
- [ ] do not lose useful ideas that are likely to matter later
- [ ] do not use tiếng Việt không dấu in self-brain/working files

---

## 11. Definition of Done

This policy is implemented correctly only when:

- [ ] new ideas during work are not lost
- [ ] self-brain remains concise
- [ ] `open-questions.md` contains real open questions, not all random thoughts
- [ ] A2 backlog contains real deferred work items
- [ ] candidate branch ideas are tracked without being prematurely activated
- [ ] active risks track only meaningful risks
- [ ] Codex can follow the policy consistently in both interactive and async modes

---

## 12. Final Reminder To Codex

When new ideas appear during work, do **not** choose between only two bad extremes:

- write everything
- write nothing

Instead, classify the idea first:

- open question
- todo/backlog
- candidate branch idea
- tech debt
- active risk
- real committed decision

Then write it into the smallest correct lane.

Always prefer:

- concise writeback
- correct lane
- low noise
- future reviewability

---
