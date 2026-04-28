# POL-26277 — A1 MCP-First Context Policy For Local Cross-Repo Work

**Status:** policy-brief-v1
**Project:** AICOS
**Date:** 2026-04-19
**Primary scope:** A1 work agents
**Purpose:** định nghĩa rõ policy cho nhóm **A1** khi AICOS triển khai **local MCP** cho cross-repo local work.

Tài liệu này trả lời rõ các câu hỏi:

- A1 có nên dùng MCP hoàn toàn cho context hay không?
- A1 có được đọc/ghi context trực tiếp bằng raw file access không?
- A1 có được giữ local copied context trong worktree của nó không?
- Làm sao để tránh việc A1 “lười”, đọc context một lần rồi dùng local stale copy mãi?
- Authority boundary giữa:
  - AICOS
  - external checkout
  - local cache/scratch
  được hiểu như thế nào?
- Policy này sẽ sống ở layer nào bây giờ, và mở rộng thế nào về sau?

---

## 1. Executive Summary

### Core policy

Đối với **A1 work agents**, khi làm việc theo mô hình:

- `AICOS = context/control-plane authority`
- `external checkout = code/runtime authority`

thì policy chuẩn là:

### **A1 must be MCP-first for all AICOS-facing context/control-plane operations.**

Điều đó có nghĩa là:

#### A. A1 phải dùng MCP cho:
- startup context
- handoff/current retrieval
- packet index retrieval
- selected packet retrieval
- checkpoint writeback
- task update writeback
- handoff update writeback

#### B. A1 không cần dùng MCP cho:
- đọc code trong chính working checkout của nó
- sửa file local trong chính working checkout của nó
- chạy local scripts/tests trong chính working checkout của nó
- inspect local runtime outputs trong chính working checkout của nó

### Important clarification

Policy này **không** có nghĩa:
- “mọi thao tác của A1 đều phải đi qua MCP”

Policy này có nghĩa:
- **mọi thao tác liên quan tới AICOS context/control-plane phải đi qua MCP**
- còn **local work trong chính repo/checkout của A1 thì làm trực tiếp**

---

## 2. Why This Policy Exists

Policy này được đưa ra vì 4 lý do chính.

### 2.1. Permission-safe cross-folder operation
A1 không nên phụ thuộc vào broad/full filesystem access chỉ để:
- lấy startup context
- lấy packet
- lấy handoff
- ghi checkpoint
- ghi writeback sang AICOS

### 2.2. Multi-agent consistency
Nếu Codex, Claude, OpenClaw, hoặc các A1 clients khác cùng làm trong một project,
thì AICOS-facing context nên đi qua một contract chung thay vì mỗi tool tự mò file paths.

### 2.3. Continuity discipline
A1 không nên tự quyết định:
- file AICOS nào là authority
- handoff/current nào mới nhất
- packet nào đúng hot path

MCP giúp AICOS expose các surfaces này theo contract thống nhất.

### 2.4. Prevent stale-context drift
Nếu A1 chỉ copy context vào local notes/worktree rồi dùng mãi, rất dễ:
- dùng stale handoff
- dùng packet cũ
- bỏ qua current state mới
- tạo continuation không đáng tin cậy

MCP-first policy làm rõ rằng:
- local copied notes có thể tồn tại
- nhưng không phải authority

---

## 3. Scope Of This Policy

### Current layer
Hiện tại policy này được hiểu là:

- **A1-layer policy inside AICOS**
- áp dụng cho A1 actors khi tương tác với AICOS context/control-plane

### Future layering
Về sau, policy này phải mở rộng được theo logic rule stack:

- company/workspace layer
- project layer
- workstream/task layer
- prompt-local formatting layer

### Rule precedence principle
Khi có layering đầy đủ hơn trong tương lai, policy nên obey:

### **Higher-scope rules may override or extend lower-scope rules if explicitly defined.**

Ví dụ:
- company/workspace có thể đặt requirement mạnh hơn cho MCP
- project có thể đặt thêm context discipline riêng
- task/workstream có thể thu hẹp/điều chỉnh packet usage

### Important
Tài liệu này **không** đóng cứng rule stack tương lai.
Nó chỉ định nghĩa policy nền cho phase hiện tại.

---

## 4. Authority Boundary

## 4.1. AICOS authority
AICOS là authority cho:

- startup bundle
- project current state/current direction
- handoff/current
- packet index
- selected packet
- task continuity
- checkpoint continuity
- writeback/handoff updates
- context/control-plane truth

## 4.2. External checkout authority
External checkout là authority cho:

- source code
- local scripts
- local tests
- runtime execution
- runtime artifacts
- repo-local implementation files
- repo-local workflow behavior

## 4.3. Local copied context / scratch authority
Local copied context, scratch notes, or convenience cache are:

- allowed as working aids
- not authoritative
- not valid as durable continuity source
- not valid as startup authority
- not valid as handoff authority

### Rule
Local scratch is allowed.
Local scratch is not truth.

---

## 5. A1 MCP-Required Operations

The following operations are **MCP-required** for A1.

### Report Code: POL-26278

#### A. Startup read
A1 must retrieve startup context from MCP, not from manually assembled raw file reads across AICOS.

#### B. Current state / direction read
A1 must retrieve AICOS current project state/direction through MCP-exposed context surfaces.

#### C. Handoff/current read
A1 must retrieve handoff/current through MCP, not by treating arbitrary copied local notes as current authority.

#### D. Packet index read
A1 must retrieve packet index through MCP.

#### E. Selected packet read
A1 must retrieve the selected packet through MCP.

#### F. Checkpoint write
A1 must write meaningful checkpoint updates through MCP.

#### G. Task continuity write
A1 must write task update / continuation state through MCP.

#### H. Handoff update write
A1 must write handoff continuity updates through MCP.

---

## 6. A1 Non-MCP Operations

The following operations do **not** need MCP by default.

### Checklist Code: POL-26279

- [ ] reading code in the local working checkout
- [ ] editing code in the local working checkout
- [ ] running scripts/tests in the local working checkout
- [ ] inspecting local runtime outputs in the local working checkout
- [ ] creating local scratch notes that are explicitly non-authoritative

### Rule
A1 should not use MCP where direct local repo work is simpler and correct.

---

## 7. Policy On Local Cached / Copied Context

This is the most important behavioral rule.

### Rule 1 — local copies are allowed as convenience
A1 may keep:
- scratch notes
- temporary summaries
- copied excerpts
- local convenience references

### Rule 2 — local copies are never authoritative
A1 must not treat local copied context as:
- startup authority
- handoff authority
- packet authority
- current-state authority
- writeback authority

### Rule 3 — fresh continuation requires MCP refresh
Before a new bounded task or continuation-sensitive action, A1 must refresh relevant context through MCP.

### Rule 4 — stale local copy cannot justify action
If A1 acts on a stale copied note instead of current MCP state, that action is not valid continuation behavior.

### Rule 5 — local cache may exist later, but only as secondary surface
If `.aicos/` or another local cache is introduced later:
- it remains secondary
- it may speed up convenience
- it must not replace MCP as authoritative context surface

---

## 8. How To Prevent “Lazy Agent” Behavior

The solution is not just “tell the agent to behave.”

It must be enforced by design.

### 8.1. Do not rely on prompt-only discipline
Prompt-only rules are weak.
A1 may still:
- reuse stale notes
- skip refresh
- read direct files if accessible
- forget writeback discipline

### 8.2. Make MCP the only accepted authority path
Completion should only be accepted if:
- startup context came from MCP
- packet came from MCP
- handoff/current came from MCP when needed
- writeback went through MCP

### 8.3. Require MCP trace in final output
A1 final reports/checkpoints should include enough MCP trace to prove:
- which startup bundle was used
- which packet was used
- which handoff/current was used
- whether writeback/checkpoint succeeded

### 8.4. Treat local scratch as disposable
A1 can keep local scratch, but reviewers and system policy should ignore it as authority.

### 8.5. Hot path should not depend on mirrored AICOS files in worktree
Do not make AICOS truth live redundantly inside external checkout as a primary mechanism.
Otherwise A1 will naturally drift into using local copies.

---

## 9. Acceptance Rule For A1 Work

A1 work should not be considered complete unless the result is anchored to MCP-mediated context/control-plane surfaces.

### Minimum required evidence
At minimum, A1 completion should show:

- startup context source
- packet reference
- handoff/current reference if continuation-sensitive
- writeback/checkpoint result if meaningful work occurred

### If these are absent
Then the result is:
- incomplete
- weakly grounded
- or non-compliant with A1 MCP-first context policy

---

## 10. Recommended MCP Surface For A1

### Phase 1 — read-serving first
Start with the smallest useful read surfaces.

Recommended tools/resources:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_packet_index`
- `aicos_get_task_packet`

### Phase 2 — writeback next
Then add the minimum write surfaces.

Recommended tools:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

### Phase 3 — richer context later
Only after the first two phases are proven useful, consider:

- current-direction bundle
- open-items/questions surfaces
- workstream indexes
- lightweight secondary cache support

### Rule
Do not start with a giant MCP surface.

---

## 11. Performance And Token Considerations

### 11.1. Local MCP can be efficient
For local use, MCP over `stdio` is a good fit for low-overhead local tool access.

### 11.2. MCP does not automatically increase token cost
Token cost increases only if:
- the server returns bloated bundles
- agents call too many tiny tools
- context is mirrored as raw text instead of curated bundles

### 11.3. Bundle-first is preferred
A1 should prefer:
- compact startup bundle
- compact packet bundle
- compact handoff bundle

not:
- file-by-file MCP chatter

### Rule
Well-designed MCP should reduce context wandering, and may reduce token cost compared to broad raw repo reading.

---

## 12. Relationship To A2

This policy is specifically for **A1**.

### A2 behavior is different
A2 may:
- read AICOS directly
- edit AICOS directly
- do repo maintenance directly
- use MCP optionally where useful

### Rule
Do not apply A1 MCP-first context restrictions blindly to A2.

---

## 13. Project-Specific Policy Compatibility

A1 MCP-first context policy is separate from:
- language policy
- report style policy
- project-specific content rules

Those should live in:
- project layer
- or future workspace/company layers

### Example
A sample project project may require:
- user-facing communication in Vietnamese
- English technical terms as needed

That is a **project-layer policy**, not an A1-universal policy.

### Rule
A1 MCP-first context policy governs **how A1 obtains/updates context**, not the content policy of every project.

---

## 14. Minimum Review Questions

When reviewing an A1 result under this policy, ask:

### Checklist Code: POL-26280

- [ ] Did A1 obtain startup context through MCP?
- [ ] Did A1 obtain packet context through MCP?
- [ ] Did A1 obtain handoff/current through MCP when needed?
- [ ] Did A1 write checkpoint/task/handoff updates through MCP when required?
- [ ] Did A1 avoid treating local copied context as authority?
- [ ] Did A1 keep local repo work direct and bounded?
- [ ] Did A1 provide enough MCP trace in its output?

---

## 15. Definition Of Compliance

An A1 agent is compliant with this policy only if:

- AICOS-facing context is MCP-first
- AICOS-facing writeback is MCP-first
- local checkout work remains local
- local copied notes are not treated as authority
- final completion evidence shows MCP-mediated context/control-plane usage
- no broad raw cross-folder file dependency is required for normal A1 operation

---

## 16. Final Policy Statement

### Final rule

For A1 work agents in cross-repo local workflows:

- **Use MCP for all AICOS-facing context/control-plane operations**
- **Use direct local repo access for local code/runtime/artifact work**
- **Treat local copied context only as scratch, never as authority**
- **Do not accept A1 completion without MCP-mediated context/control-plane trace**

This is the preferred policy baseline for A1 as AICOS moves toward permission-safe local multi-agent work.

---
