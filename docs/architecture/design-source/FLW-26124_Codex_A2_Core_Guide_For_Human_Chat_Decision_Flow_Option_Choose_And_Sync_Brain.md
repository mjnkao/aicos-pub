# FLW-26124 — Codex A2-Core Guide For Human-Chat Decision Flow, `aicos option choose`, and `aicos sync brain`

**Status:** implementation-guide-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** hướng dẫn Codex trong vai **A2-Core** triển khai đúng flow làm việc giữa human ↔ agent ↔ AICOS khi human ra quyết định qua chat channel, còn agent phải ghi lại quyết định đó vào state của AICOS và sync self-brain khi cần.

---

## 1. Mục tiêu của bước này

Mục tiêu của bước này là làm rõ và hiện thực hóa một flow rất cụ thể:

1. human giao tiếp với A1 hoặc A2 qua **chat channel phù hợp**
   - Telegram của OpenClaw
   - UI chat của Codex Desktop
   - UI/chat của Claude Code
   - các kênh tương tự khác về sau

2. khi agent bị blocker hoặc có nhiều hướng xử lý, agent:
   - hỏi user ngay trong chat nếu đang có phiên trực tiếp
   - hoặc ghi `blocked + options + waiting` vào AICOS nếu đang ở mode async

3. khi human chọn phương án trong chat, agent phải:
   - hiểu đây là một **manager decision**
   - ghi lại quyết định đó vào state chính thức của AICOS

4. sau khi state trong `brain/` đã đổi, nếu cần retrieval/query layer nhìn thấy cập nhật mới nhất, agent phải:
   - chạy sync sang GBrain/PGLite

### Kết luận ngắn

- **chat** là nơi trao đổi và ra quyết định
- **AICOS** là nơi lưu trạng thái có cấu trúc
- `aicos option choose` là bước commit manager decision vào system state
- `aicos sync brain` là bước đồng bộ `brain/` sang retrieval substrate

---

## 2. Vai trò của Codex trong bước này

Trong bước này, Codex phải hiểu rõ:

- Codex đang làm việc cho **AICOS itself**
- vì vậy Codex đang ở lane:
  - **A2-Core**
  - chủ yếu là **A2-Core-C**

Codex không được hiểu nhầm là đang build UI chat mới hay thay thế chat channel.  
Codex chỉ đang build **system behavior phía sau** để AICOS làm việc tốt với các chat channel hiện có.

---

## 3. Mental Model bắt buộc phải giữ

## 3.1. Chat channel không phải source of truth chính

Quyết định có thể được nói ra trong chat, nhưng chat transcript không nên là nơi duy nhất giữ quyết định đó.

### Vì sao

Nếu chỉ có chat mà không writeback vào AICOS:

- agent khác quay lại sẽ không chắc option nào đã được chọn
- working state sẽ lệch với chat history
- branch reality sẽ lệch với manager choice
- retrieval layer sẽ không thấy current decision

## 3.2. AICOS mới là nơi giữ structured state

AICOS phải giữ các thứ như:

- blocker
- option packet
- selected option
- selected branch
- working state update
- open question status
- approval state

## 3.3. `aicos option choose` không thay thế chat

Lệnh này không phải nơi human “chat”.

Nó là nơi system ghi lại:

- human đã chọn gì
- branch nào là selected
- blocker nào đã có execution direction
- working state nào phải đổi theo

## 3.4. `aicos sync brain` không tương tác với human

Lệnh này không dùng để hỏi user.

Lệnh này dùng để:

- đọc `brain/`
- import/update vào GBrain/PGLite
- làm retrieval/query substrate phản ánh brain state mới hơn

---

## 4. Hai mode làm việc phải hỗ trợ

AICOS phải hỗ trợ đồng thời 2 mode:

## 4.1. Sync / Interactive mode

Flow:

1. agent đang nói chuyện trực tiếp với human qua chat
2. agent trình bày blocker + options trong chat
3. human trả lời ngay trong chat
4. agent commit decision đó vào AICOS state
5. agent tiếp tục làm việc

### Ý nghĩa

Đây là mode “đang online, đang đối thoại”.

## 4.2. Async / Waiting mode

Flow:

1. agent đang làm việc nhưng không có human online trực tiếp
2. agent gặp blocker
3. agent tạo:
   - blocker state
   - option packet
   - recommendation
   - waiting status
4. human quay lại sau qua chat channel phù hợp
5. human review các options
6. human chọn một hướng
7. agent commit decision vào AICOS state

### Ý nghĩa

Đây là mode “ghi lại để chờ human review sau”.

---

## 5. Scope của công việc hiện tại

Trong bước này, Codex phải triển khai hoặc hoàn thiện:

- `aicos option choose`
- behavior map rõ giữa chat decision và AICOS state update
- behavior của `aicos sync brain` theo đúng boundary
- update docs / rules / self-brain nếu cần
- không build UI mới
- không build public API mới
- không thay thế chat channel hiện có

---

## 6. `aicos option choose` phải được hiểu như thế nào

## 6.1. Mục đích

`aicos option choose` dùng để:

- chốt option mà manager/human đã chọn
- ghi việc chọn đó vào AICOS state
- update selected branch
- update project working state
- update approval lane phù hợp
- đóng hoặc đổi trạng thái blocker/open question nếu cần

## 6.2. Nó không phải là chat interface

Human có thể chọn option qua:

- Telegram
- Codex Desktop UI
- Claude Code UI
- comment trong review flow
- các channel khác

Sau khi human chọn xong, agent phải gọi lệnh tương đương:

```text
aicos option choose <project-id> <blocker-id> <option-id>
```

Đây là bước **commit decision** chứ không phải bước đối thoại.

## 6.3. Input tối thiểu nên có

Codex nên triển khai command theo hướng tối thiểu như sau:

```text
aicos option choose <project-id> <blocker-id> <option-id>
```

Ví dụ:

```text
aicos option choose aicos blocker-001 option-a
```

### Optional future flags

Sau này có thể mở rộng:

```text
aicos option choose <project-id> <blocker-id> <option-id> \
  --actor manager-min \
  --reason "Ưu tiên nhanh, reversible, phù hợp MVP"
```

Nhưng ở phase đầu, không cần overbuild.

## 6.4. Input sources mà command này nên đọc

Tối thiểu nên đọc:

- option packet hiện tại của blocker
- project working state hiện tại
- branch candidates liên quan
- approval / manager-choice file nếu đã có

Có thể đọc thêm nếu cần:

- blocker source file
- branch compare packet
- recommendation note
- open questions liên quan

## 6.5. State updates mà command này phải tạo ra

Khi chọn option, command nên update rõ ràng các lane sau.

### Required updates

- selected option được ghi rõ
- selected branch được ghi rõ
- project working state được update
- approval/choice packet được update hoặc tạo mới
- blocker được chuyển trạng thái phù hợp
- open question hoặc next direction được update nếu liên quan

### Không được làm

- không tự promote sang canonical
- không tự đổi architecture truth
- không tự index backend như truth
- không tự xóa các option khác
- không tự làm manager review packet biến mất

## 6.6. Các file/lane mà command này nên chạm tới

### Bắt buộc nên xem xét

- `serving/branching/option-packets/...`
- `agent-repo/classes/humans/approvals/...`
- `brain/projects/<project-id>/branches/<selected-branch>/...`
- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`
- `brain/projects/<project-id>/working/open-questions.md`
- `agent-repo/classes/.../tasks/blocked/...` hoặc queue tương ứng

## 6.7. Output command nên rõ

Output tối thiểu nên trả lời:

- option nào đã được chọn
- branch nào thành selected
- file/lane nào đã update
- lane nào chưa bị chạm
- command có thành công hay không

Ví dụ output ngắn:

```text
Chosen option: option-a
Project: aicos
Blocker: blocker-001
Selected branch: blocker-001-option-a

Updated:
- human approval packet
- selected branch reality
- working/current-state.md
- working/current-direction.md

Not changed:
- canonical/*
- other option branches
- backend truth
```

---

## 7. `aicos sync brain` phải được hiểu như thế nào

## 7.1. Mục đích

`aicos sync brain` dùng để:

- đọc các file trong `brain/`
- import/update chúng vào GBrain/PGLite
- làm retrieval/query substrate phản ánh state mới hơn

## 7.2. Nó không phải truth engine

Lệnh này **không được**:

- rewrite truth trong `brain/`
- promote `working` sang `canonical`
- tự xử lý manager choice
- tự index `agent-repo/` như work truth
- load backup mặc định

### Câu chốt

`sync brain` là **serving sync**, không phải **authority mutation engine**.

## 7.3. Nó nên sync cái gì

Tối thiểu chỉ nên sync:

- `brain/companies/`
- `brain/workspaces/`
- `brain/projects/`
- `brain/shared/`
- `brain/service-knowledge/`

### Đặc biệt quan trọng

Với phase hiện tại, target quan trọng nhất là:

- `brain/projects/aicos/canonical/`
- `brain/projects/aicos/working/`
- `brain/projects/aicos/evidence/`
- `brain/projects/aicos/branches/`

## 7.4. Nó không nên sync cái gì mặc định

Không sync mặc định:

- `agent-repo/`
- `backend/`
- `scripts/`
- `integrations/`
- `backup/`
- legacy material
- runtime logs
- queue artifacts như truth

## 7.5. Các bước hành vi mà `sync brain` nên làm

Tối thiểu command nên có 4 phase:

### Phase 1 — scan

- scan các file hợp lệ trong `brain/`

### Phase 2 — validate

- validate lane hợp lệ
- skip lane không nên sync
- check encoding/metadata tối thiểu nếu cần

### Phase 3 — import/update

- import/update vào GBrain/PGLite
- refresh retrieval/index state

### Phase 4 — report

- báo số file scan
- số file import/update
- số file skipped
- lý do skip
- lane nào đã sync

## 7.6. Output command nên rõ

Ví dụ output ngắn:

```text
Sync target: brain/
Engine: GBrain + PGLite

Scanned:
- canonical: 4 files
- working: 7 files
- evidence: 5 files
- branches: 2 files

Imported/updated:
- 16 files

Skipped:
- 3 files
Reason:
- missing metadata
- unsupported lane
- excluded by policy

Not scanned:
- agent-repo/
- backend/
- backup/

Result:
- sync success
- retrieval index refreshed
```

---

## 8. Mối quan hệ giữa chat flow và 2 command này

## 8.1. Flow chuẩn ở interactive mode

1. agent trình blocker/options trong chat
2. human chọn trong chat
3. agent hiểu selection
4. agent gọi `aicos option choose ...`
5. AICOS state update
6. nếu policy hoặc workflow cần retrieval layer cập nhật ngay:
   - agent gọi `aicos sync brain`

## 8.2. Flow chuẩn ở async mode

1. agent ghi blocker + options + waiting
2. human quay lại sau và review qua chat
3. human chọn trong chat
4. agent gọi `aicos option choose ...`
5. AICOS state update
6. sau đó sync brain nếu cần

## 8.3. Rule quan trọng

Human không bắt buộc phải tự chạy command.

Thông thường, agent đang làm việc trong channel đó sẽ:

- hiểu choice của human
- tự gọi command phù hợp
- tự writeback vào AICOS

---

## 9. Những việc Codex phải làm cụ thể

### Checklist Code: FLW-26125

- [ ] review current CLI implementation of `./aicos`
- [ ] identify current placeholder/preflight behavior of `option`-related flows
- [ ] implement first-class `aicos option choose <project-id> <blocker-id> <option-id>`
- [ ] ensure command updates approval + branch + working lanes coherently
- [ ] document exact touched files/lane behavior
- [ ] review current `aicos sync brain` implementation
- [ ] convert `sync brain` from preflight-only toward real GBrain/PGLite import/update for `brain/` only
- [ ] ensure `agent-repo/`, `backend/`, `backup/` are excluded by default
- [ ] update self-brain working docs if command behavior changes materially
- [ ] keep all docs and self-brain summaries concise

---

## 10. Những việc Codex không được làm trong bước này

### Checklist Code: FLW-26126

- [ ] do not build new UI for manager choice
- [ ] do not replace Telegram/Codex/Claude chat with AICOS UI
- [ ] do not make backend the truth layer
- [ ] do not index `agent-repo/` as project work truth
- [ ] do not auto-promote `working` to `canonical`
- [ ] do not overbuild a full event system
- [ ] do not overcomplicate async message delivery
- [ ] do not hardcode too much future policy into the command

---

## 11. Acceptance Criteria

### Checklist Code: FLW-26127

This step is done only when:

- [ ] a human can choose an option in a normal chat channel
- [ ] the agent can commit that choice into AICOS with `aicos option choose`
- [ ] the selected branch and working state become clear and reviewable
- [ ] `aicos sync brain` can update GBrain/PGLite from `brain/`
- [ ] retrieval sync excludes non-brain lanes by default
- [ ] no new UI is required for the flow to work
- [ ] docs reflect the new behavior clearly and concisely

---

## 12. Final Reminder To Codex

Your job in this step is not to redesign the whole architecture again.

Your job is to make this human workflow real:

- human decides in chat
- agent commits decision into AICOS state
- AICOS state becomes coherent
- retrieval layer can be refreshed from `brain/`

Keep the implementation:

- local-first
- chat-compatible
- boundary-safe
- concise
- non-overbuilt

If there is a conflict between:

- elegant over-engineering
- and a simple robust local flow

choose:

- the simple robust local flow

---
