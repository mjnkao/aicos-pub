# AIC-26185 — Codex Implementation Brief  
## Startup Truth Surface Normalization for AICOS

**Status:** proposed implementation brief  
**Lane mặc định:** `A2-Core-C`  
**Reasoning mode trước thay đổi kiến trúc/ownership lớn:** `A2-Core-R` ngắn  
**Primary project:** `projects/aicos`

---

## 1) Objective

Thực hiện một **small normalization pass** để làm sạch **startup truth surface** của repo AICOS, sao cho một fresh agent hoặc Codex mới vào có thể:

- đọc đúng **current repo truth**
- không bị kéo về startup docs/path đã stale hoặc missing
- không phải tự đoán file nào mới là authority
- không phải bulk-load `docs/New design/` hoặc `docs/migration/` để bắt đầu

Mục tiêu của pass này là **alignment**, không phải build subsystem mới.

---

## 2) Current Reality To Respect

Codex phải giữ đúng các boundary hiện tại của repo:

- `brain/` = durable knowledge, canonical truth, working reality, evidence, branch reality
- `agent-repo/` = actor operations, startup cards, rule cards, tasks, packets
- `backend/` = substrate / index / runtime support, **không phải authority**
- `serving/` = generated artifacts / packets / compare outputs, **không phải authority**
- `docs/migration/` = migration / implementation / provenance notes, **không phải startup truth mặc định**
- `docs/New design/` = design/reference/source docs, **không phải startup truth mặc định**

Ngoài ra, lane active hiện tại là:

- `A2-Core` = active lane để sửa chính AICOS
- `A2-Serve` = target/future lane, **chưa build đầy đủ trong pass này**

---

## 3) Problem This Pass Is Solving

Hiện tại startup surface có dấu hiệu chưa khép hoàn toàn:

1. Có startup doc/path cũ được kỳ vọng nhưng không còn xuất hiện ở đúng path trên `main`.
2. Có khả năng overlap vai trò giữa:
   - `brain/projects/aicos/working/current-state.md`
   - `brain/projects/aicos/working/handoff/current.md`
   - `brain/projects/aicos/working/handoff-summary.md`
3. Fresh agent có thể vẫn phải suy đoán:
   - đâu là **sole H1 current handoff index**
   - đâu là digest/reference
   - đâu là startup-authoritative file
4. Startup philosophy đã đúng theo hướng packet-first / index-first, nhưng entry surface cần **deterministic** hơn.

---

## 4) Non-Goals

**Không làm** các việc sau trong pass này:

- không tạo folder tree mới chỉ để đẹp
- không build transfer / takeover subsystem
- không build registry lớn cho handoff hoặc task ownership
- không build UI
- không build public API
- không mở full A2-Serve runtime lane
- không migrate toàn bộ legacy docs
- không rewrite lớn `docs/New design/`
- không expand packet system beyond current MVP need

Nếu có ý tưởng vượt scope ở trên, chỉ ghi vào `open-items.md` hoặc `open-questions.md` đúng lane, không nhét vào implementation này.

---

## 5) Target Outcome

Sau pass này, startup story phải rõ ràng như sau:

### 5.1 Sole H1 Current Handoff Index
File authority cho current handoff của project AICOS là:

```text
brain/projects/aicos/working/handoff/current.md
```

Đây là **sole H1 current handoff index**.

### 5.2 Handoff Summary Status
`brain/projects/aicos/working/handoff-summary.md` nếu được giữ lại thì chỉ là:

- digest/reference ngắn
- optional helper
- **không** là startup authority ngang hàng với H1 current index
- **không** là file mà fresh agent phải đọc mặc định nếu startup card không yêu cầu

### 5.3 Current State Role
`brain/projects/aicos/working/current-state.md` phải là:

- current repo/system state summary
- implementation reality summary
- scope/status summary

File này **không nên** lặp lại quá nhiều nội dung “handoff ownership model” nếu phần đó đã authoritative hơn ở `working/handoff/current.md`.

### 5.4 Migration Doc Status
Nếu startup doc cũ ở `docs/migration/...` đang missing hoặc stale, thì phải có **redirect / superseded note rõ ràng** để agent không phải tự suy đoán.

---

## 6) Files Likely To Touch

### 6.1 Startup-critical files
Ưu tiên các file sau:

1. `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
2. `brain/projects/aicos/working/current-state.md`
3. `brain/projects/aicos/working/current-direction.md` *(chỉ nếu wording hiện tại cần minor alignment; không sửa nếu không cần)*
4. `brain/projects/aicos/working/handoff/current.md`
5. `brain/projects/aicos/working/handoff-summary.md`

### 6.2 Migration/provenance file
Chỉ chạm khi cần:

6. `docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md`

### 6.3 Optional consistency targets
Chỉ update nếu tìm thấy reference conflict rõ ràng:

7. `agent-repo/classes/a2-service-agents/rule-cards/handoff.md`
8. `agent-repo/classes/a2-service-agents/rules/handoff-policy.md`
9. `agent-repo/classes/a2-service-agents/task-packets/README.md`

---

## 7) Implementation Strategy

Thực hiện theo thứ tự nhỏ, reversible, repo-coherent.

---

## 8) Step Plan

## AIC-26186 — Verify Actual Repo Reality First

### Goal
Xác minh repo reality trước khi sửa wording.

### What To Do
Chạy targeted inspection, không bulk-load repo:

- kiểm tra file/path nào thực sự tồn tại
- kiểm tra path nào stale/missing
- kiểm tra reference nào đang chỉ tới startup doc cũ
- kiểm tra file nào đang nói cùng một câu chuyện startup/handoff

### Suggested search
Dùng search/grep có chọn lọc, ví dụ:

```bash
rg -n "AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418|handoff-summary|working/handoff/current\.md|current-state\.md|startup-cards/a2-core\.md" .
```

### Acceptance
- biết rõ doc cũ còn tồn tại hay không
- biết file nào đang đóng vai authority
- biết có reference conflict hay không

### Important
Không suy đoán chỉ từ memory. Tin repo reality.

---

## AIC-26187 — Normalize Sole Startup Authority Story

### Goal
Làm rõ **một startup truth surface chính**, không để 2–3 file ngang quyền.

### Required outcome
Sau bước này, story phải rõ:

- startup card chỉ đúng startup path
- `handoff/current.md` là sole H1
- `handoff-summary.md` chỉ là digest/reference nếu còn giữ
- `current-state.md` không tranh vai H1

### What To Edit

#### 1. `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
Kiểm tra và nếu cần thì làm rõ thêm:

- startup read order ngắn
- chỉ đọc `working/handoff/current.md` khi continuation / migration-state-alignment / repo-wide architecture / newest-vs-stale
- không để `handoff-summary.md` thành implied startup-authority
- nhấn mạnh packet-first / stop-at-orientation nếu chưa có task

**Do not** biến startup card thành doc dài hơn nhiều.

#### 2. `brain/projects/aicos/working/handoff/current.md`
File này phải nói rất rõ:

- đây là **sole H1 current handoff index**
- H2/H3 là gì
- file nào chỉ là digest/reference
- `docs/migration/` không còn là default active handoff home
- startup mới không cần đọc docs cũ mặc định

Nếu cần, thêm một dòng explicit như:

> `brain/projects/aicos/working/handoff/current.md` is the sole current handoff index for `projects/aicos`.

#### 3. `brain/projects/aicos/working/handoff-summary.md`
Khuyến nghị **giữ file này nhưng demote rõ** thay vì xóa ngay.

Biến nó thành một trong hai kiểu sau:

**Option recommended:** digest/reference only  
- ngắn hơn
- explicit rằng không phải startup authority
- không thay thế current handoff index
- chỉ useful nếu cần summary ngắn hoặc pointer

**Không nên** giữ wording mơ hồ kiểu “summary nhưng có vẻ cũng là current startup doc”.

#### 4. `brain/projects/aicos/working/current-state.md`
Giảm overlap nếu cần:

- giữ phần current repo reality
- giữ phần active root / current CLI surface / current A2 status
- giữ phần “đã có / chưa active đầy đủ / flow đã chứng minh”
- **giảm lặp** chi tiết handoff model nếu `handoff/current.md` đã authoritative hơn
- nếu cần, chỉ để pointer ngắn sang `working/handoff/current.md`

### Acceptance
Một fresh agent đọc các file startup chính sẽ không bị hiểu rằng:
- `current-state.md`
- `handoff-summary.md`
- `handoff/current.md`

đều là startup authority ngang nhau.

---

## AIC-26188 — Fix Or Redirect Stale Startup Migration Path

### Goal
Giải quyết startup path cũ để không còn ambiguity.

### Decision rule
Nếu file sau **không tồn tại** hoặc rõ ràng đã stale:

```text
docs/migration/AICOS_CURRENT_STATE_AND_ARCHITECTURE_HANDOFF_20260418.md
```

thì làm **một redirect note hoặc superseded note tối thiểu**.

### Recommended action
Tạo hoặc cập nhật file này thành một note cực ngắn, ví dụ theo tinh thần:

- doc này không còn là active startup truth
- current startup authority đã chuyển sang:
  - `brain/projects/aicos/working/current-state.md`
  - `brain/projects/aicos/working/current-direction.md`
  - `brain/projects/aicos/working/handoff/current.md`
  - `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
- `docs/migration/` hiện giữ migration/provenance/implementation notes

### Important
Không viết lại file này thành “new big startup doc”.
Chỉ dùng nó như:
- redirect
- superseded marker
- provenance bridge

### Acceptance
Người đọc path cũ sẽ được redirect rõ ràng sang path đúng hiện tại.

---

## AIC-26189 — Consistency Sweep For Reference Conflicts

### Goal
Đảm bảo rule cards và packet index không vô tình tạo startup story khác.

### Files to inspect
- `agent-repo/classes/a2-service-agents/rule-cards/handoff.md`
- `agent-repo/classes/a2-service-agents/rules/handoff-policy.md`
- `agent-repo/classes/a2-service-agents/task-packets/README.md`

### What To Check
- có nói đúng H1/H2/H3 không
- có vô tình nói `docs/migration/` như active handoff home không
- có imply `handoff-summary.md` là authority không
- có mâu thuẫn với startup card không
- có nhắc đúng packet-first / on-demand episodic handoff loading không

### Acceptance
Không còn contradiction đáng kể giữa:
- startup card
- handoff current index
- handoff summary
- handoff rule/policy
- packet index

---

## AIC-26190 — Validate The Result

### Goal
Xác minh pass này thực sự giảm ambiguity.

### Validation questions
Codex phải tự kiểm tra được rằng:

1. Nếu là fresh A2-Core agent, file nào đọc trước?
2. Nếu cần continuation, file handoff authority là file nào?
3. Nếu thấy `handoff-summary.md`, có hiểu nhầm nó là H1 không?
4. Nếu có ai giữ startup link cũ vào `docs/migration/...`, họ có được redirect rõ không?
5. Nếu chưa có concrete task, agent có bị kéo vào full packets / old migration docs không?

### Suggested checks
- đọc lại startup card sau khi sửa
- đọc lại `working/handoff/current.md`
- đọc lại `working/current-state.md`
- grep lại các reference chính
- xác nhận story nhất quán trong 3–5 phút review cuối

### Optional runtime follow-up
Nếu pass này làm thay đổi meaningful state trong `brain/`, có thể chạy:

```bash
./aicos sync brain
```

sau khi sửa xong, **chỉ để refresh serving/retrieval substrate từ `brain/`**.

### Important
Không được diễn giải `./aicos sync brain` như:
- promote canonical truth
- mutate truth
- full orchestration step
- proof rằng mọi external co-worker memory đã đồng bộ

---

## 9) File-By-File Guidance

## AIC-26191 — `a2-core.md`
### Keep
- read-first list ngắn
- packet-first behavior
- “stop at orientation if no concrete task”
- handoff read only when triggered

### Improve if needed
- wording để authority story rõ hơn
- nhấn mạnh `working/handoff/current.md` là continuation entry
- không ám chỉ startup authority khác ngoài path đã chốt

### Avoid
- thêm quá nhiều prose
- thêm design rationale dài
- thêm references vượt scope

---

## AIC-26192 — `working/handoff/current.md`
### Keep
- H1/H2/H3 model
- current CLI surface ngắn
- newest/current vs stale guidance
- open follow-ups

### Improve if needed
- explicit “sole H1 current handoff index”
- explicit demotion của stale migration startup path
- explicit demotion của `handoff-summary.md` nếu giữ file đó

### Avoid
- biến nó thành lịch sử đầy đủ
- append mọi thay đổi nhỏ
- copy quá nhiều từ migration docs

---

## AIC-26193 — `working/handoff-summary.md`
### Recommended direction
Giữ làm **digest/reference only**.

### It should say clearly
- đây không phải startup authority chính
- authority hiện tại là `working/handoff/current.md`
- summary này chỉ hỗ trợ đọc nhanh / reference

### Avoid
- wording kiểu “summary nhưng cũng current index”
- duplicate quá nhiều từ `current.md`

Nếu sau review thấy file này hoàn toàn không còn giá trị, có thể đề xuất xóa ở pass sau, nhưng **không bắt buộc trong pass này**.

---

## AIC-26194 — `working/current-state.md`
### Keep
- active root
- đã có / chưa active
- current CLI surface / status
- flow đã chứng minh
- manager decision / selected direction reality nếu còn current

### Reduce
- overlap nặng với handoff model
- overlap nặng với startup policy language
- overlap khiến fresh agent không biết file nào authority

### Recommended pattern
Nếu cần nói về handoff, dùng pointer ngắn kiểu:
- continuity authority: see `brain/projects/aicos/working/handoff/current.md`

---

## AIC-26195 — stale migration startup doc
### If missing
Tạo redirect note ngắn.

### If exists but stale
Demote rõ bằng:
- `Status: superseded / redirect-only`
- pointer sang current startup truth surface

### Avoid
- biến thành doc mới quá dài
- duplicate toàn bộ startup state vào docs/migration

---

## 10) Expected Deliverables

Sau khi hoàn tất, Codex nên để lại:

1. các file đã chỉnh sửa
2. một summary ngắn nói:
   - file nào đã đổi
   - authority story sau cùng là gì
   - file nào là startup-authoritative
   - file nào chỉ còn reference/digest
3. nếu có file cũ/path cũ được demote, nói rõ:
   - vì sao
   - path thay thế là gì
4. nếu có chỗ còn intentionally unresolved, ghi đúng lane:
   - `open-items.md`
   - `open-questions.md`

---

## 11) Success Criteria

Pass này được coi là thành công khi:

- một fresh A2-Core agent có thể startup nhẹ, đúng scope
- repo authority story không còn mơ hồ
- `working/handoff/current.md` là sole H1 current index
- `handoff-summary.md` không còn gây hiểu nhầm là authority ngang H1
- startup migration path cũ không còn làm người đọc lệch hướng
- không có subsystem mới nào bị build thêm
- không có folder tree mới chỉ để đẹp
- không có overbuild

---

## 12) Escalation Rule

Nếu trong lúc làm Codex phát hiện rằng repo reality đã khác đáng kể so với assumptions ở brief này, thì:

1. **tin repo reality**
2. không cố ép repo theo brief này một cách máy móc
3. ghi lại divergence ngắn gọn
4. chọn phương án nhỏ nhất, reversible nhất
5. tránh architecture expansion

---

## 13) Suggested Working Mode For Codex

Trình tự làm việc nên là:

1. đọc targeted files
2. verify repo reality bằng search ngắn
3. chốt ownership story
4. sửa các file startup/handoff bị overlap
5. tạo redirect/superseded marker cho path cũ nếu cần
6. chạy consistency sweep
7. chỉ sau đó mới refresh `brain/` serving substrate nếu phù hợp

---

## 14) Final Instruction To Codex

Hãy xử lý pass này như một **repo hygiene + startup determinism task**, không phải một architecture rewrite.

Ưu tiên:
- nhỏ
- rõ
- reversible
- repo-coherent
- authority-first
- packet-first
- startup-light

Không overbuild.
