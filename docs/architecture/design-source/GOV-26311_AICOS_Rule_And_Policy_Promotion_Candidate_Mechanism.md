# GOV-26311 — AICOS Rule And Policy Promotion Candidate Mechanism

**Status:** governance-brief-v1  
**Project:** AICOS  
**Date:** 2026-04-19  
**Primary scope:** suggestion-to-policy evolution  
**Purpose:** định nghĩa cơ chế để AICOS có thể:
- biến suggestion frameworks và lower-scope rules thành **promotion candidates**
- tổng hợp evidence từ project/workspace/company feedback
- gợi ý nâng cấp rule/policy ở tầng cao hơn
- nhưng không tự động áp đặt promotion khi chưa có human decision

---

## 1. Core Principle

AICOS không nên:
- tự động biến một suggestion thành company policy
- tự động promote rule chỉ vì một project thấy hữu ích
- trộn lẫn experimental suggestions với active policies

AICOS nên:
- theo dõi evidence
- tạo candidate
- tổng hợp confidence
- nêu trade-offs
- để human hoặc higher-scope maintainer quyết định

### Final rule
AICOS generates **promotion candidates**, not automatic promotions.

---

## 2. Why This Mechanism Exists

Suggestion frameworks và lower-scope rules sẽ dần được dùng ở:
- project layer
- workspace layer
- company layer
- shared cross-company layer

Nếu không có promotion mechanism, hệ thống sẽ rơi vào một trong hai trạng thái xấu:

### A. Stuck in endless suggestion mode
Nhiều pattern tốt nhưng không bao giờ được chuẩn hóa.

### B. Premature hardening
Một pattern vừa dùng được ở một project đã bị nâng thành policy chung quá sớm.

Promotion candidate mechanism giúp tránh cả hai.

---

## 3. Layer Model

### Layer 1 — Project
Project-specific suggestions, rules, and local policies.

### Layer 2 — Workspace
Patterns useful across several projects in one workspace.

### Layer 3 — Company
Patterns useful broadly across one company.

### Layer 4 — Shared
Patterns generic enough to be useful across many companies/domains.

### Rule
Higher layers should only be fed by repeated lower-layer evidence, not by one-off intuition alone.

---

## 4. Candidate Stages

### Report Code: GOV-26312

A rule/suggestion should move through these stages:

#### `experimental`
Being tried in one or a few scopes. No promotion claim yet.

#### `project_proven`
Repeatedly useful within one project. Stable enough for stronger local use.

#### `workspace_candidate`
Shows value across multiple contexts inside one workspace, or evidence suggests workspace relevance.

#### `company_candidate`
Shows value across multiple project/workspace contexts in one company.

#### `shared_candidate`
Looks generic enough for cross-company reuse.

#### `active_policy`
Human-accepted and officially active at the target layer.

### Important
`active_policy` is not just another candidate stage.
It requires explicit approval.

---

## 5. Evidence Inputs For Promotion

Promotion should be driven by evidence such as:

- repeated structured feedback
- consistent acceptance patterns
- reduced confusion signals
- improved routing/writeback discipline
- low override rate
- cross-project reuse
- stable purpose and low ambiguity
- low overlap with existing higher-scope policies

### Negative evidence should also matter
Do not promote when feedback repeatedly shows:
- ambiguous
- too broad
- too narrow
- caused overlap
- repeatedly ignored
- repeatedly overridden

---

## 6. Minimal Candidate Record

### Report Code: GOV-26313

A promotion candidate should have a compact canonical record such as:

```yaml
candidate_id: "<stable-id>"
subject_ref: "<framework-id | rule-id | policy-id>"
origin_layer: "project|workspace|company|shared"
target_layer: "workspace|company|shared"
candidate_stage: "experimental|project_proven|workspace_candidate|company_candidate|shared_candidate"

summary: "<short description of the pattern>"
why_promote: "<short rationale>"

evidence_snapshot:
  projects_observed: 0
  workspaces_observed: 0
  accepted_count: 0
  merged_count: 0
  deferred_count: 0
  rejected_count: 0

quality_signals_positive:
  - reduced_confusion
  - improved_routing

quality_signals_negative:
  - ambiguous

confidence: "low|medium|high"
human_review_required: true
status: "open|accepted|rejected|deferred"
```

### Rule
Candidate records should stay compact and comparative.

---

## 7. Promotion Decision Heuristics

AICOS should not use one hard formula, but it can use simple heuristics.

### Strong signs for promotion
- repeated `accepted`
- repeated `helpful`
- repeated `reduced_confusion`
- repeated `improved_routing`
- repeated `improved_writeback_discipline`
- low `caused_overlap`
- low `rejected`
- useful in more than one project/workspace

### Strong signs against promotion
- high ambiguity
- frequent overrides
- frequent merge-back into older patterns
- only one narrow project context
- high overlap with existing rules
- mainly useful due to one domain-specific quirk

---

## 8. Human Review Boundary

Promotion decisions should remain human-reviewed.

### AICOS may:
- create candidate records
- summarize evidence
- suggest target layer
- estimate confidence

### AICOS should not:
- silently activate higher-scope policy
- silently deprecate lower-scope rules
- auto-override workspace/company governance

### Rule
Promotion remains recommendation-driven, not automatic.

---

## 9. Relationship To Feedback Digest

`aicos_get_feedback_digest` should help identify:
- repeated patterns
- high-signal subjects
- possible promotion candidates

But digest is not candidate record.

### Digest answers:
- what signals are appearing?

### Candidate mechanism answers:
- which subject is mature enough to be reviewed for promotion?

---

## 10. Relationship To Project Health

Project health should not directly decide promotion.

A project may be healthy operationally while still using local-only rules that should not be promoted.
Conversely, a project may be somewhat messy operationally but still generate a good reusable governance pattern.

### Rule
Promotion should be based on repeated governance evidence, not only operational health.

---

## 11. Relationship To Suggestion Frameworks

Promotion candidate mechanism depends on suggestion frameworks having:
- clear ids
- clear purpose
- reusable structure
- structured feedback capture

Without those, promotion becomes too subjective.

### Rule
Good suggestion frameworks are promotable.
Messy informal patterns are not.

---

## 12. Suggested MCP Relationship

Later, AICOS may support manager-facing reads such as:
- `aicos_get_feedback_digest`
- `aicos_get_project_health`
- maybe eventually `aicos_get_policy_candidates`

And write surfaces such as:
- `aicos_record_framework_feedback`
- maybe later `aicos_upsert_policy_candidate`

### Important
This mechanism can be designed before all tools exist.
Do not wait for full tooling to define governance logic.

---

## 13. Suggested Review Questions

### Checklist Code: GOV-26314

- [ ] Has this subject shown value in more than one context?
- [ ] Are positive signals repeated and credible?
- [ ] Are negative signals still too high?
- [ ] Is the pattern truly higher-scope, or still mainly project-specific?
- [ ] Does it overlap confusingly with existing higher-scope rules?
- [ ] Is human review still required before activation?
- [ ] Is the candidate record compact and evidence-based?

---

## 14. Final Recommendation

### Final recommendation

AICOS should treat policy evolution as:

1. suggestion/framework usage
2. structured feedback capture
3. digest/signal synthesis
4. promotion candidate generation
5. human review
6. higher-scope activation if approved

### Final rule
AICOS should help rules and suggestion frameworks mature upward through evidence, but should not harden them automatically without explicit human decision.

---
