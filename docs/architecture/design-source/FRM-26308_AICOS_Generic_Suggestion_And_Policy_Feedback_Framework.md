# FRM-26308 — AICOS Generic Suggestion And Policy Feedback Framework

**Status:** framework-brief-v1  
**Project:** AICOS  
**Date:** 2026-04-19  
**Primary scope:** generic cross-project feedback capture  
**Purpose:** định nghĩa một framework feedback chung để AICOS có thể:
- học từ việc các project dùng suggestion frameworks
- đánh giá chất lượng của project/workspace/company rules và policies
- gom feedback có cấu trúc để về sau tổng hợp thành manager digest và policy candidates
- tránh việc feedback chỉ tồn tại trong prose rải rác khó học ngược

---

## 1. Core Principle

AICOS không nên học chủ yếu từ:
- prose handoff dài
- ghi chú rải rác
- phản hồi mơ hồ kiểu “cái này hơi rối”
- cảm nhận ngầm mà không có structure

AICOS nên học chủ yếu từ:
- **structured feedback**
- theo **scope**
- theo **framework/policy reference**
- theo **outcome**
- theo **quality signal**
- theo **reason summary**
- theo **evidence refs**

### Final rule
Nếu feedback không có structure tối thiểu, nó rất khó trở thành nguồn để cải tiến rules/policies về sau.

---

## 2. What This Framework Covers

Framework này dùng cho feedback liên quan tới:

- suggestion frameworks
- project rules
- workspace rules
- company policies
- shared cross-company governance patterns

Ví dụ:
- workstream suggestion framework
- packet suggestion framework
- canonical promotion suggestion framework
- context routing rules
- MCP-first context discipline
- project-specific language/output visibility rules
- future workspace/company governance rules

---

## 3. What This Framework Does Not Cover

Framework này không nhằm thay thế:
- task status update
- checkpoint write
- handoff continuity write
- artifact registry

Nó không ghi lại:
- “đã làm task gì”
- “task đang blocked hay completed”
- “handoff bây giờ là gì”

Nó ghi lại:
- **chất lượng và hiệu quả của framework/rule/policy**
- **feedback về cách rule/suggestion đang vận hành**
- **evidence để cải tiến governance layer**

---

## 4. Feedback Capture Goals

### 4.1. Learn what actually helps
Framework nào thật sự giúp actor:
- bớt lẫn
- route đúng
- write đúng lane
- giảm broad reading
- hiểu project nhanh hơn

### 4.2. Learn what causes friction
Framework/rule nào đang:
- quá mơ hồ
- quá rộng
- quá hẹp
- bị overlap
- gây duplication
- bị actor hiểu sai lặp lại

### 4.3. Learn what should be promoted
Pattern nào lặp lại qua nhiều project/workspace và đủ tốt để:
- trở thành candidate
- rồi có thể được nâng lên tầng cao hơn

---

## 5. Minimal Feedback Model

### Report Code: FRM-26309

Mọi feedback nên có tối thiểu các trường sau:

```yaml
scope: "projects/<project-id>"                         # required
feedback_type: "framework|rule|policy"                # required
subject_ref: "<framework-id | rule-id | policy-id>"   # required
subject_layer: "project|workspace|company|shared"     # required

outcome: "accepted|merged|rejected|deferred|overridden|partially_used"  # required

quality_signal:                                       # required, 1 or more
  - helpful
  - ambiguous
  - too_broad
  - too_narrow
  - caused_overlap
  - reduced_confusion
  - improved_routing
  - improved_writeback_discipline
  - not_used
  - repeatedly_triggered
  - repeatedly_ignored

reason_summary: "<short bounded explanation>"         # required

workstream_id: "<optional>"
task_ref: "<optional>"
packet_ref: "<optional>"
artifact_refs: ["<optional>"]
handoff_ref: "<optional>"]

feedback_actor_family: "a1-work-agents|a2-service-agents|other"  # optional
feedback_actor_role: "<logical role>"                             # optional
confidence: "low|medium|high"                                     # optional
client_request_id: "<optional>"
```

### Rule
Feedback must stay:
- small
- structured
- comparable
- project-neutral

---

## 6. Feedback Outcome Semantics

To keep feedback comparable, outcomes should be interpreted consistently.

### `accepted`
The suggestion/rule/policy was used substantially and judged appropriate.

### `merged`
The suggestion was not adopted as-is, but merged into an existing lane/rule.

### `rejected`
The suggestion/rule was actively not adopted.

### `deferred`
Not enough evidence yet; revisit later.

### `overridden`
A higher-scope rule or local project rule replaced it.

### `partially_used`
Only part of the suggestion/rule was useful.

---

## 7. Quality Signal Semantics

Quality signals are the most important learning surface.

### Helpful signals
- `helpful`
- `reduced_confusion`
- `improved_routing`
- `improved_writeback_discipline`

### Friction signals
- `ambiguous`
- `too_broad`
- `too_narrow`
- `caused_overlap`

### Adoption signals
- `not_used`
- `repeatedly_triggered`
- `repeatedly_ignored`

### Rule
Use short enumerated signals instead of long qualitative paragraphs whenever possible.

---

## 8. Suggested MCP Relationship

Long-term, AICOS should support structured feedback through a semantic write surface such as:

### Possible future tool
- `aicos_record_framework_feedback`

This tool would:
- write structured framework/rule/policy feedback
- map it into approved feedback lanes
- preserve refs and traceability
- feed later digest/promotion mechanisms

### Important
This framework does not require that tool immediately, but it defines the target shape for future implementation.

---

## 9. Storage / Lane Principles

Feedback should not be mixed randomly into:
- handoff/current
- task update
- long evidence prose

Instead, feedback should land in a lane that is:
- structured
- project-scoped at minimum
- easy to query later
- distinguishable from normal task continuity

### Guiding principle
Task continuity tells us what happened.
Framework feedback tells us what the system learned from what happened.

---

## 10. How Managers Should Use This Framework

### Project manager use
At project level, use feedback to answer:
- which suggestion frameworks help this project most?
- which rules are causing friction?
- which patterns are repeatedly proposed?
- what should be refined locally first?

### Workspace/company manager use
At higher levels, use feedback to answer:
- which project-level patterns keep repeating?
- which rules should be considered as candidate higher-scope policy?
- what should remain project-specific?
- which shared patterns are broadly useful?

---

## 11. Relationship To Feedback Digest

This framework is the raw signal layer.

`aicos_get_feedback_digest` should later summarize:
- repeated feedback patterns
- high-signal subjects
- likely rule refinements
- likely promotion candidates

### Rule
Do not skip structured feedback and jump directly to digest.
Digest quality depends on capture quality.

---

## 12. Relationship To Project Health

This framework is not the same as project health.

### Feedback framework answers:
- what did actors learn about the rule/framework/policy?

### Project health answers:
- how healthy is the project’s context/control-plane operation?

Both are useful, but they serve different questions.

---

## 13. Suggested Review Questions

### Checklist Code: FRM-26310

- [ ] Is the feedback about a framework/rule/policy rather than a task event?
- [ ] Is the subject clearly referenced?
- [ ] Is the outcome one of the normalized outcomes?
- [ ] Are quality signals explicit?
- [ ] Is the reason summary short and meaningful?
- [ ] Are refs attached where helpful?
- [ ] Is this feedback useful for later digest or promotion decisions?

---

## 14. Final Recommendation

### Final recommendation

AICOS should standardize suggestion/rule/policy feedback around:
- a referenced subject
- a normalized outcome
- explicit quality signals
- a short reason summary
- optional task/packet/artifact refs

### Final rule
If AICOS wants to improve rules and suggestion frameworks over time, it must treat feedback as a first-class structured object, not as accidental prose hidden inside task notes.

---
