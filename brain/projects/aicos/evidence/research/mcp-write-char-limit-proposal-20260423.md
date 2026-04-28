# Đề Xuất: Điều Chỉnh Giới Hạn Ký Tự Trong MCP Write Tools

**Loại:** Research / Design Proposal  
**Ngày:** 2026-04-23  
**Tác giả:** A2-Core-C (claude-code, session claude-code-ops-20260423-infra)  
**Liên quan:**
- `brain/projects/aicos/working/status-items/ux-mcp-summary-char-limit.md`
- `brain/projects/aicos/working/status-items/oq-mcp-detail-field.md`
- `brain/projects/aicos/evidence/candidate-decisions/decision-candidate-index.md`

---

## 1. Bối Cảnh

AICOS MCP write tools hiện tại áp đặt giới hạn ký tự cứng trên các field
chính. Giới hạn này được validate tại server và trả về lỗi nếu vượt quá:

| Field | Tool | Giới hạn hiện tại |
|-------|------|-------------------|
| `summary` | `aicos_update_status_item` | **700 chars** |
| `summary` | `aicos_write_handoff_update` | **600 chars** |
| `next_step` | cả hai | ~400 chars (ước tính) |
| `title` | cả hai | ~120 chars |

Giới hạn này được thiết kế với mục đích rõ ràng: giữ status items và handoff
compact, tránh agent dump toàn bộ document vào một field.

---

## 2. Vấn Đề Thực Tế Quan Sát Được

### 2.1 Ví Dụ Cụ Thể — Session 2026-04-23

Trong session phân tích rủi ro concurrency cho 10-agent LAN, tôi cần ghi item
`RISK-CONCURRENT-WRITE-LOCK`. Item này mô tả **2 bugs riêng biệt** cùng nằm
trong một vấn đề logic:

**Nội dung cần truyền đạt:**

```
Bug 1 — FILE RACE:
  - Cơ chế: read-then-rewrite không có file lock
  - File bị ảnh hưởng: brain/projects/*/working/handoff/current.md
  - Hệ quả: last writer silently overwrites first, không có error
  - Trigger condition: 2+ agents ghi đồng thời trong vài milliseconds

Bug 2 — STALE CACHE SPLIT-BRAIN:
  - Cơ chế: 30s TTL cache, agents đọc worktree state stale
  - Scenario: A đọc xyz=free → B đọc xyz=free (cache hit) → cả 2 claim xyz
  - Hệ quả: coordination policy bị vô hiệu hóa trong 30s window
  - Trigger condition: 2+ agents startup trong cùng 30s window

Files cần fix: aicos_mcp_daemon.py, mcp_write_serving.py
Severity: HIGH — data loss hôm nay, không cần scale
```

**Kết quả khi fit vào 700 chars:**

Tôi phải chọn một trong hai:
- Mô tả đủ Bug 1, bỏ gần hết Bug 2 → Codex chỉ fix một trong hai
- Mô tả cả hai quá sơ sài → Codex thiếu context để implement đúng
- Tách thành 2 items riêng → mất liên kết logic, 2 tasks không natural

Đây không phải trường hợp ngoại lệ. Technical items về bugs, risks, và
architectural decisions thường có cấu trúc này: **nhiều facts liên quan cần
được đặt cùng nhau** để agent đọc hiểu đúng.

### 2.2 Pattern Tổng Quát

Giới hạn 700 chars (~100 từ) đủ cho:
- ✅ Thông báo status change đơn giản ("đã merge branch X vào main")
- ✅ Open question ngắn ("nên dùng approach A hay B?")
- ✅ Decision followup ("đã quyết định dùng PostgreSQL, cần track migration")
- ❌ Mô tả bug kỹ thuật với đủ context để reproduce và fix
- ❌ Risk analysis với scenario cụ thể và điều kiện trigger
- ❌ Architectural trade-off với đủ evidence để quyết định

---

## 3. Mục Đích Thiết Kế Ban Đầu Của Giới Hạn

Giới hạn ký tự phục vụ 3 mục đích quan trọng, tất cả đều valid:

### 3.1 Giữ Handoff/Digest Scannable

`brain/projects/*/working/handoff/current.md` là file được đọc ở startup.
Nếu mỗi section dài 2000+ chars, file trở nên không scannable. Agent mới sẽ
phải đọc toàn bộ để tìm thông tin cần thiết.

### 3.2 Ngăn Document Dumping

Không có giới hạn → agent sẽ paste toàn bộ analysis, code snippet, log output
vào summary field. Status items không phải nơi lưu tài liệu đầy đủ. AICOS đã
có `brain/evidence/research/` cho việc này.

### 3.3 Khuyến Khích Tư Duy Ngắn Gọn

Giới hạn ép agent phải suy nghĩ về điều quan trọng nhất trước khi ghi. Đây là
hành vi mong muốn cho công cụ coordination, không phải storage.

**→ Cả 3 mục đích đều đúng và cần giữ lại.**

---

## 4. Tại Sao Calibration Hiện Tại Quá Chặt

### 4.1 Mismatch giữa item_type và giới hạn đồng nhất

AICOS có 4 `item_type` với nhu cầu ký tự rất khác nhau:

| item_type | Nội dung điển hình | Chars cần |
|-----------|-------------------|-----------|
| `open_question` | Câu hỏi ngắn + 2-3 options | 300–500 |
| `decision_followup` | Ghi nhận decision + tracking note | 300–600 |
| `tech_debt` | Mô tả friction + file + impact | 500–900 |
| `open_item` (technical) | Bug / risk: cơ chế + scenario + file + severity | 800–1500 |

Giới hạn 700 áp dụng đồng nhất cho tất cả → quá chặt với `open_item` kỹ thuật,
quá rộng với `open_question`.

### 4.2 Sự Khác Biệt Giữa "Ngắn Gọn" Và "Không Đủ Thông Tin"

Ngắn gọn tốt: bỏ đi những gì không cần thiết để người đọc ra quyết định.  
Ngắn gọn xấu: bỏ đi thông tin cần thiết để người đọc ra quyết định đúng.

700 chars với một technical bug thường rơi vào "ngắn gọn xấu": Codex đọc item
xong nhưng thiếu context để implement fix đúng, phải tự suy đoán hoặc hỏi lại.

### 4.3 So Sánh Thực Tế

```
700 chars  ≈ 100 từ  ≈ 3-4 câu mô tả + 1 file ref
1200 chars ≈ 170 từ  ≈ mô tả đủ 1 bug hoặc 2 bugs ngắn + file refs
1500 chars ≈ 220 từ  ≈ mô tả đủ 2 bugs với context + implementation hint
3000 chars ≈ 430 từ  ≈ bắt đầu thành document, nên để ở evidence/research
```

Vùng **1200–1500 chars** là điểm cân bằng: đủ context để Codex act mà không
khuyến khích document dumping.

---

## 5. Đề Xuất

### Option A — Tăng Giới Hạn (Ngắn Hạn, Low Risk) ✅ Recommended First

Thay đổi validation trong `mcp_write_serving.py`:

```python
# Trước
SUMMARY_MAX_LEN = {
    "update_status_item":    700,
    "write_handoff_update":  600,
}

# Sau
SUMMARY_MAX_LEN = {
    "update_status_item":    1500,
    "write_handoff_update":  1200,
}
```

Thêm **soft warning** (không reject) khi summary > 1200 chars để nhắc agent
cân nhắc dùng artifact_refs:

```python
if len(summary) > 1200:
    warnings.append({
        "code": "summary_approaching_document",
        "message": (
            "Summary is long. If this is a full document or analysis, "
            "consider writing it to brain/projects/<scope>/evidence/research/ "
            "and referencing it via artifact_refs instead."
        )
    })
```

**Lợi ích:**
- Không thay đổi schema, không migration
- Backward compatible hoàn toàn
- Fix ngay friction agents đang gặp
- Soft warning duy trì hướng đúng

**Rủi ro:**
- Một số agents có thể viết dài hơn → digest ít compact hơn
- Chấp nhận được: summary vẫn bị giới hạn, không phải không giới hạn

**Files cần sửa:**
- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py` (hoặc validators/)
- Không cần thay đổi schema, contract, hay client code

---

### Option B — Thêm Field `detail` (Dài Hạn, Candidate Decision)

Thêm optional field `detail` (3000 chars) vào write tools:

```json
{
  "summary": "compact, luôn hiển thị trong digest (1500 chars max)",
  "detail":  "kỹ thuật, chỉ load khi cần, optional (3000 chars max)"
}
```

**Đọc:**
- `aicos_get_status_items` trả về `summary` mặc định
- Có thể thêm `include_detail=true` param để load full khi cần

**Lợi ích:**
- Digest vẫn compact với `summary`
- Codex có thể đọc `detail` khi cần implement một item cụ thể
- Phân tách rõ "signal" vs "context"

**Rủi ro:**
- Schema change → cần update write tools, read tools, file format
- Phức tạp hơn Option A đáng kể
- Có thể không cần nếu `artifact_refs` đủ dùng

**→ Xem thêm:** `OQ-MCP-DETAIL-FIELD` trong status items.  
**→ Quyết định gate:** Thử `artifact_refs` trên 2-3 items thực. Nếu vẫn còn
friction, mới promote Option B thành open_item.

---

## 6. So Sánh Hai Options

| Tiêu chí | Option A (tăng limit) | Option B (thêm field) |
|----------|----------------------|----------------------|
| Effort | **Thấp** — 1 ngày | **Cao** — schema + migration |
| Risk | **Thấp** — backward compatible | **Trung** — breaking change nhỏ |
| Fixes ngay friction? | **Có** | Có, nhưng overkill nếu A đủ |
| Giữ digest compact? | **Vẫn ổn** — 1500 vẫn compact | Tốt hơn |
| Schema change? | **Không** | Có |
| Cần human decision? | **Không** | Có |

---

## 7. Recommendation

1. **Làm ngay — Option A**: tăng limit, thêm soft warning. Codex có thể làm
   trong 1 task, không cần discussion. Track qua `UX-MCP-SUMMARY-CHAR-LIMIT`.

2. **Observe 4–6 tuần**: sau khi Option A live, xem agents có viết summary
   quá dài không, digest có còn scannable không.

3. **Quyết định Option B** dựa trên observation thực tế. Nếu agents vẫn cần
   nhiều hơn 1500 chars thường xuyên → promote Option B. Nếu không → close
   `OQ-MCP-DETAIL-FIELD`.

---

## 8. Điều Không Thay Đổi

Các giới hạn sau **giữ nguyên hoàn toàn** — calibration hiện tại là đúng:

| Field | Giới hạn | Lý do giữ |
|-------|---------|-----------|
| `title` | ~120 chars | Title phải scannable, không bao giờ cần dài hơn |
| `next_step` | ~400 chars | Instruction cụ thể, actionable — ngắn gọn là đức tính |
| `reason` | ~400 chars | Context tại sao, không phải how-to |

Giới hạn tổng thể của design vẫn đúng: **status items là coordination signals,
không phải documents.** Proposal này chỉ điều chỉnh calibration của một field
(`summary`) đang quá chặt, không thay đổi triết lý thiết kế.
