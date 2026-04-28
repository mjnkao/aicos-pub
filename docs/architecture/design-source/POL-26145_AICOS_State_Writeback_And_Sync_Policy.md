# POL-26145 — AICOS State Writeback and Sync Policy

**Status:** master-operational-policy-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** policy tổng để quy định **khi nào thì ghi thông tin vào state của AICOS, ghi vào đâu, ghi ở mức nào, khi nào không nên ghi, và khi nào cần sync** trong cả interactive mode và async mode.

---

## 1. Mục tiêu của policy này

AICOS cần một policy rõ ràng để tránh hai lỗi lớn:

### Lỗi A — ghi quá nhiều

- ghi mọi chat turn
- ghi mọi ý nghĩ giữa chừng
- ghi mọi clarification nhỏ vào working state
- biến self-brain thành log rác

### Lỗi B — ghi quá ít

- decision xảy ra trong chat nhưng không writeback
- blocker có thật nhưng không được phản ánh
- branch đã được chọn nhưng state không đổi
- idea quan trọng bị mất
- retrieval layer không thấy state mới

### Kết luận

AICOS phải đi theo nguyên tắc:

> **Không ghi theo từng message. Ghi theo state transition có ý nghĩa.**

---

## 2. Scope của policy này

Policy này áp dụng cho:

- A2-Core
- A2-Serve trong tương lai
- A1 khi làm việc với project reality
- human ↔ agent interactive flow
- async waiting/review flow
- self-brain của AICOS
- working state của AICOS
- writeback từ chat decision sang state
- `aicos option choose`
- `aicos sync brain`

Policy này không thay thế:

- code/schema contracts
- promotion policy chi tiết
- branch contract chi tiết
- packet schema chi tiết

Nó là **operational decision policy** cho việc writeback.

---

## 3. Nguyên tắc nền tảng

## 3.1. Principle 1 — Chat không phải source of truth duy nhất

Chat là nơi:

- hỏi đáp
- clarify
- đề xuất
- lựa chọn
- review

Nhưng chat transcript không nên là nơi duy nhất giữ state.

## 3.2. Principle 2 — Brain phải ít noise

Self-brain và working state phải:

- ngắn gọn
- dễ scan
- dùng được làm startup context
- không biến thành full conversation log

## 3.3. Principle 3 — Ghi theo state transition, không ghi theo từng chat turn

Chỉ ghi khi có:

- decision
- blocker confirmed
- option packet ready
- selected branch
- changed direction
- meaningful risk
- milestone completed
- question đủ quan trọng để review sau
- actionable deferred work

## 3.4. Principle 4 — Không phải mọi thông tin đều vào brain

Thông tin phải được phân loại trước khi ghi:

- no write
- session/runtime write
- working write
- canonical promotion

## 3.5. Principle 5 — Sync chỉ là serving refresh, không phải authority mutation

`aicos sync brain` chỉ dùng để:

- đồng bộ `brain/` sang GBrain/PGLite

Nó không được:

- quyết định truth
- promote state
- rewrite authority

---

## 4. Bốn mức write action

### Table Code: POL-26146

| Mức | Tên | Ý nghĩa |
|---|---|---|
| W1 | No Write | không ghi vào AICOS |
| W2 | Session / Runtime Write | ghi tạm vào session/runtime/queue lane, chưa vào brain truth |
| W3 | Working State Write | ghi vào `brain/.../working` hoặc lane working tương đương |
| W4 | Canonical Promotion | promote lên `brain/.../canonical` sau review/chấp thuận |

---

## 5. W1 — No Write

## 5.1. Khi nào dùng W1

Dùng khi nội dung chỉ là:

- clarifying question nhỏ
- wording adjustment nhỏ
- micro feedback
- thought chưa ổn định
- back-and-forth ngắn
- tentative idea rất sơ khai
- câu trả lời “ok”, “tiếp tục”, “chưa chắc”, “để nghĩ thêm”
- message không tạo state transition

## 5.2. Ví dụ

- “ý tôi là command kia thôi”
- “phần này nghe ổn”
- “thử phân tích thêm chút”
- “để tôi xem lại”
- “ok tiếp tục”

## 5.3. Rule

Không ghi vào:

- `brain/.../working`
- `brain/.../canonical`
- `active-risks`
- `open-questions`

trừ khi sau đó nó trở thành một state transition rõ ràng hơn.

---

## 6. W2 — Session / Runtime Write

## 6.1. Khi nào dùng W2

Dùng khi có nội dung tạm thời, in-progress, nhưng chưa đủ ổn định để vào brain.

### Examples

- session scratch
- in-progress hypothesis
- tóm tắt tạm lúc agent đang suy nghĩ
- intermediate compare note
- nhánh suy nghĩ đang cân
- tentative branch idea rất sớm
- runtime-local warnings
- temporary status

## 6.2. Nên ghi ở đâu

Thường nên vào:

- `agent-repo/.../session-logs/`
- `agent-repo/.../tasks/current/`
- `agent-repo/.../queues/...`
- runtime scratch phù hợp

## 6.3. Rule

W2 là nơi giữ **noise hữu ích tạm thời**, không phải nơi giữ truth dài hạn.

Nếu nội dung ở W2 trở nên đủ rõ và có giá trị lâu hơn, nó phải được nâng lên W3 hoặc chuyển sang lane phù hợp khác.

---

## 7. W3 — Working State Write

## 7.1. Khi nào dùng W3

Dùng khi đã có **state transition đủ rõ** để ảnh hưởng tới current reality.

### Các trường hợp chính

- blocker được xác nhận là có thật
- option packet đã đủ rõ để review
- human/manager đã chọn một option
- branch mới được activate
- working direction thay đổi
- active risk mới đủ nghiêm trọng
- open question mới đủ quan trọng để giữ lại
- implementation milestone hoàn thành
- migration status đổi đáng kể
- service state đổi đáng kể
- current status đủ ổn định để summarize

## 7.2. Nên ghi ở đâu

Tùy loại thông tin:

### Working state tổng quát
- `brain/projects/<id>/working/current-state.md`

### Hướng làm hiện tại
- `brain/projects/<id>/working/current-direction.md`

### Risk đang active
- `brain/projects/<id>/working/active-risks.md`

### Câu hỏi còn mở
- `brain/projects/<id>/working/open-questions.md`

### Implementation status
- `brain/projects/<id>/working/implementation-status.md`

### Migration status
- `brain/projects/<id>/working/migration-status.md`

### Branch đã active
- `brain/projects/<id>/branches/<branch-id>/...`

## 7.3. Rule

W3 chỉ dành cho nội dung:

- đủ ổn định
- đủ ngắn gọn để summarize
- đủ quan trọng để agent khác quay lại vẫn cần biết

Không dùng W3 như inbox cho mọi idea hoặc mọi đoạn chat.

---

## 8. W4 — Canonical Promotion

## 8.1. Khi nào dùng W4

Chỉ dùng khi:

- nội dung đã được review
- đủ ổn định
- đủ authoritative
- được human hoặc policy chấp thuận để trở thành canonical truth

## 8.2. Ví dụ

- role-definitions chính thức
- project-working-rules chính thức
- source-manifest chính thức
- architecture decision đã chốt
- promotion-policy đã chốt

## 8.3. Rule

Interactive chat flow hằng ngày hiếm khi đi thẳng tới W4.

Thông thường:
- W1 hoặc W2 diễn ra trước
- sau đó W3
- rồi mới cân nhắc W4 nếu thực sự cần

---

## 9. Commit Point là gì?

Commit point là thời điểm mà thông tin đủ “chín” để writeback.

### Một số commit point chuẩn

#### C1 — Decision point
Human đã chọn rõ:
- option nào
- branch nào
- direction nào

#### C2 — Stable blocker point
Sau trao đổi, blocker đã đủ rõ và thực sự block flow.

#### C3 — Stable summary point
Sau một đoạn làm việc, agent có thể tóm tắt ngắn gọn current state mà không đổi nhiều sau 1–2 phút nữa.

#### C4 — Milestone point
Một mốc có ý nghĩa đã hoàn thành:
- scaffold xong
- command chạy được
- migration xong pha 1
- compare packet xong

#### C5 — Risk confirmation point
Một risk đã đủ rõ để cần tracking chứ không chỉ là lo ngại mơ hồ.

---

## 10. Interactive Mode Policy

Interactive mode = human đang online và đang chat trực tiếp với agent.

## 10.1. Default rule

Không ghi vào brain sau mỗi chat turn.

## 10.2. Phải làm gì thay vì ghi liên tục

Agent nên:

- giữ context trong chat
- dùng W2 nếu cần scratch/in-progress note
- đợi tới commit point rồi mới W3

## 10.3. Khi nào nên write trong interactive mode

### Write W3 khi có:
- blocker confirmed
- option packet ready
- human selected option
- direction changed materially
- risk materially changed
- milestone completed
- câu hỏi mới đủ đáng để review sau
- task mới đủ rõ để backlog

## 10.4. Khi nào chưa nên write

### Stay W1 or W2 khi:
- chỉ đang clarify
- đang tranh luận nhỏ
- đang brainstorm chưa chín
- mới có idea sơ khai
- human chưa chọn gì rõ
- chưa có state transition

## 10.5. Debounce rule

Nếu chat đang nhanh và liên tục:

- không update file sau mỗi lượt
- chờ đến khi có summary đủ rõ
- hoặc decision đủ rõ
- hoặc milestone đủ rõ

Nói ngắn:

> interactive mode phải **debounce** writeback.

---

## 11. Async Mode Policy

Async mode = agent làm việc khi human không online trực tiếp hoặc không đang chat ngay.

## 11.1. Default rule

Async mode cho phép writeback chủ động hơn, vì state transition thường rõ hơn.

## 11.2. Nên write khi

- blocker confirmed
- waiting for human decision
- option packet ready
- recommendation ready
- candidate branch ideas đã đủ rõ để review
- branch reached review point
- milestone completed
- risk confirmed
- actionable deferred work identified

## 11.3. Không nên write khi

- intermediate scratch chưa ổn định
- every micro-attempt
- mọi nhánh suy nghĩ chưa chín
- logs kỹ thuật nhỏ không có giá trị review sau

## 11.4. Rule

Async mode rõ ràng hơn interactive mode, nhưng vẫn phải phân loại trước khi ghi.

---

## 12. Policy riêng cho new ideas

New ideas không phải lúc nào cũng vào `current-state`.

### Rule tổng quát

Nếu idea mới phát sinh, phân loại trước thành một trong các nhóm:

- open question
- todo/backlog
- candidate branch idea
- tech debt
- active risk
- real decision

### Mapping nhanh

#### Open question
Ghi vào:
- `brain/projects/aicos/working/open-questions.md`

#### TODO / backlog
Ghi vào:
- `agent-repo/classes/a2-service-agents/tasks/backlog/`

#### Candidate branch idea chưa activate
Ghi vào:
- `brain/projects/aicos/evidence/candidate-decisions/`
hoặc
- `open-questions.md` nếu còn rất chiến lược

#### Tech debt nhỏ
Ghi vào:
- backlog

#### Tech debt có impact/risk rõ
Ghi vào:
- `active-risks.md`

#### Real committed decision
Ghi vào:
- working lane hoặc branch lane tương ứng

---

## 13. `aicos option choose` Policy

## 13.1. Mục đích

`aicos option choose` dùng để:

- commit lựa chọn của human/manager vào AICOS state
- biến “đã chọn trong chat” thành “selected direction trong hệ”

## 13.2. Khi nào gọi

Chỉ gọi khi đã có **decision đủ rõ để commit**.

### Gọi khi:
- human nói rõ “chọn option A”
- human chốt “đi branch fast-mvp”
- human bác B, chọn C
- human xác nhận direction thực thi rõ ràng

### Chưa gọi khi:
- human chỉ bảo “nghe ổn”
- human bảo “phân tích thêm”
- human còn đang cân A/B
- chat chưa chốt execution direction

## 13.3. Nó nên update gì

Ít nhất phải update:

- selected option
- selected branch
- approval/choice lane
- working/current-state nếu cần
- working/current-direction nếu cần
- open questions nếu có câu hỏi đã được resolve
- blocker state nếu cần

## 13.4. Nó không được làm gì

- không tự promote canonical
- không rewrite architecture truth
- không chạm backend truth
- không auto-xóa options khác
- không thay human decision bằng recommendation của agent

---

## 14. `aicos sync brain` Policy

## 14.1. Mục đích

`aicos sync brain` dùng để:

- sync `brain/` sang GBrain/PGLite
- refresh retrieval/query substrate

## 14.2. Khi nào gọi

Gọi sau một **meaningful refresh point**.

### Nên gọi khi:
- vừa có working state update quan trọng
- vừa có manager choice đáng kể
- vừa activate branch mới
- vừa hoàn thành milestone lớn
- sắp có agent khác cần query state mới

### Chưa cần gọi ngay khi:
- chỉ đổi wording nhỏ
- mới thêm note nhỏ
- chỉ có session scratch
- chat còn đang diễn ra nhanh, chưa ổn định

## 14.3. Nó nên sync gì

Mặc định sync:

- `brain/companies/`
- `brain/workspaces/`
- `brain/projects/`
- `brain/shared/`
- `brain/service-knowledge/`

### Không sync mặc định
- `agent-repo/`
- `backend/`
- `scripts/`
- `integrations/`
- `backup/`

## 14.4. Nó không được làm gì

- không mutate truth
- không promote state
- không treat backend as authority
- không index legacy backup mặc định

---

## 15. Lane Selection Policy

### Table Code: POL-26147

| Nội dung phát sinh | Lane đúng |
|---|---|
| clarify nhỏ | W1 — không ghi |
| scratch tạm | W2 — session/runtime |
| blocker confirmed | W3 — working/current-state + blocker lane |
| option packet ready | W3 — serving/option-packets + working nếu cần |
| human selected option | `aicos option choose` -> W3 updates |
| changed direction | W3 — current-direction |
| new open question | W3 — open-questions |
| deferred actionable work | backlog/todo lane |
| candidate branch idea chưa activate | evidence/candidate-decisions hoặc open-questions |
| tech debt nhỏ | backlog |
| tech debt có impact | active-risks |
| canonicalized policy/rule | W4 — canonical |

---

## 16. Self-Brain phải giữ ngắn như thế nào

### Rule A

`current-state.md` chỉ ghi:
- current truth about state
- không ghi full chat transcript
- không ghi mọi thought

### Rule B

`current-direction.md` chỉ ghi:
- direction hiện hành
- không ghi tất cả alternatives chưa chọn

### Rule C

`open-questions.md` chỉ ghi:
- câu hỏi đủ quan trọng để review sau
- không ghi mọi thought ngắn

### Rule D

`active-risks.md` chỉ ghi:
- risk thật có impact
- không ghi mọi annoyance nhỏ

### Rule E

Nếu một thứ chỉ đáng để “không quên”, nhưng chưa là current state:
- ưu tiên backlog / candidate-decisions / session notes
- không nhồi vào current-state

---

## 17. Policy cho Human ↔ Agent chat flow

### Flow A — Interactive chat

1. human và agent trao đổi trong chat
2. agent có thể hỏi, clarify, trình options
3. chỉ khi có commit point mới writeback
4. nếu human chọn rõ một option:
   - agent chạy `aicos option choose`
5. nếu state thay đổi đủ ý nghĩa và cần query:
   - agent chạy `aicos sync brain` sau đó hoặc theo policy refresh phù hợp

### Flow B — Async waiting

1. agent tự làm việc
2. gặp blocker
3. ghi blocker + options + recommendation + waiting status
4. human quay lại review trong chat
5. human chọn
6. agent chạy `aicos option choose`
7. nếu cần, sync brain

---

## 18. Checklist thực thi cho Codex

### Checklist Code: POL-26148

- [ ] implement or refine lane-based writeback behavior
- [ ] ensure no-write / session-write / working-write / canonical-promotion are conceptually separated
- [ ] ensure interactive mode does not write every chat turn
- [ ] ensure async mode writes only meaningful states
- [ ] ensure idea capture follows lane classification
- [ ] ensure `aicos option choose` is called only on real committed choices
- [ ] ensure `aicos sync brain` is called only on meaningful refresh points
- [ ] ensure self-brain files remain concise
- [ ] document the touched lanes clearly
- [ ] update relevant working docs if behavior changes

---

## 19. Những điều Codex không được làm

### Checklist Code: POL-26149

- [ ] do not store every chat message into brain
- [ ] do not use `current-state.md` as a general inbox
- [ ] do not create real branches for every branch idea
- [ ] do not put every tech debt into active-risks
- [ ] do not sync non-brain lanes by default
- [ ] do not promote working state to canonical automatically
- [ ] do not use tiếng Việt không dấu in self-brain and working files

---

## 20. Definition of Done

Policy này được coi là implemented tốt khi:

- [ ] agent biết khi nào không ghi gì
- [ ] agent biết khi nào chỉ ghi session/runtime
- [ ] agent biết khi nào ghi working state
- [ ] agent biết khi nào cần canonical promotion
- [ ] interactive chat không làm loạn self-brain
- [ ] async flow không làm mất blocker/options/decisions
- [ ] new ideas không bị mất nhưng cũng không làm bẩn current-state
- [ ] `aicos option choose` có vị trí rõ trong flow
- [ ] `aicos sync brain` có vị trí rõ trong flow
- [ ] self-brain vẫn ngắn gọn, dễ scan, dùng tốt làm startup context

---

## 21. Final Reminder To Codex

Do not optimize for maximum logging.

Optimize for:

- correct state capture
- low noise
- good retrieval later
- clear reviewability
- stable startup context

The system should remember what matters, not everything that was said.

---
