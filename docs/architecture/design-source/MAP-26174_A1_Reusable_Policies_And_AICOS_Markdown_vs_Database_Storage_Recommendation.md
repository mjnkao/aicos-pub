# MAP-26174 — A1 Reusable Policies Matrix And AICOS Markdown-vs-Database Storage Recommendation

**Status:** advisory-note-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** ghi lại rõ:
1. policy/rules nào hiện tại chỉ dành cho A2, policy nào có thể tái sử dụng cho A1, policy nào cần tách thành shared policy để sau này không phải làm lại từ đầu  
2. vì sao AICOS hiện đang thiên về Markdown/text files cho self-brain và working state, và boundary hợp lý giữa Markdown authority với DB substrate như PGLite/Postgres

---

## 1. Executive Summary

### 1.1. Về policy reuse cho A1

Các policy vừa làm **không chỉ dùng cho A2**.

Có thể chia thành 3 nhóm:

- **Nhóm A — Shared policies dùng lại được cho cả A1 và A2**
- **Nhóm B — Shared core nhưng hiện đang viết theo wording A2, cần normalize để A1 tái sử dụng**
- **Nhóm C — A2-only, không nên áp nguyên cho A1**

### 1.2. Về storage model

AICOS hiện đang dùng nhiều Markdown/text files vì:

- dễ review
- dễ diff
- dễ branch
- dễ canonicalize
- dễ human + AI cùng đọc
- phù hợp với self-brain, handoff, rules, current state

Điều này hiện **không phải sai**, mà còn khá khớp với boundary hiện tại của repo:

- `brain/` là durable knowledge/truth/state lane
- `backend/` là substrate/index/runtime support, không phải authority
- `aicos sync brain` sync `brain/` vào GBrain/PGLite như serving refresh, không mutate truth

### 1.3. Kết luận tổng quát

AICOS nên đi theo hướng:

- **Markdown-first for authority / review / human-readable truth**
- **DB-assisted for query / serving / registries / queues / indexes / runtime support**

Không nên chuyển sang DB-first authority quá sớm cho self-brain và working state.

---

## 2. Current Repo Facts This Note Uses

The current repo state already defines:

- `brain/` as durable knowledge, canonical truth, working reality, evidence, branch reality, and service knowledge
- `agent-repo/` as operational rules/state, not project truth
- `backend/` as substrate/index/runtime support, not authority
- A1 as project-reality actor
- A2 as system-reality actor
- writeback levels W1/W2/W3/W4
- chat decision / option choose / sync brain boundaries
- packet-first startup direction

These boundaries are already visible in current canonical repo rules and role definitions.

---

## 3. Policy Reuse Matrix For A1

### Table Code: MAP-26175

| Policy area | Reuse for A1? | Status |
|---|---|---|
| role clarity model | yes | shared with A1-specific wording |
| brain / agent-repo / backend boundary | yes | shared |
| canonical / working / evidence / branches boundary | yes | shared |
| writeback levels W1/W2/W3/W4 | yes | shared |
| “write by state transition, not every chat turn” | yes | shared |
| idea capture classification | yes | shared core, lane mapping differs |
| packet-first loading principle | yes | shared |
| startup cards concept | yes | shared concept, A1-specific implementation missing |
| task packets concept | yes | shared concept, current examples are A2-Core-only |
| option choose boundary | mostly yes | shared flow, exact touched lanes differ |
| sync brain boundary | mostly yes | shared concept, A1 usually triggers it indirectly or after meaningful state changes |
| A2-Core taxonomy | no | A2-only |
| A2-Serve taxonomy | no | A2-only |
| “Codex is A2-Core-C” | no | A2-only |
| A2 service backlog lane | no | A2-only lane |
| AICOS self-brain specific working files | no | A2/AICOS-specific |

---

## 4. Shared Policies That Can Reuse Directly For A1

These can largely be reused as-is, with minimal wording changes.

## 4.1. Boundary policy

The repo already states:

- `brain/` is durable knowledge and structured reality
- `agent-repo/` is operational actor state/rules, not project truth
- `backend/` is substrate/index/runtime support, not authority

This boundary is not A2-specific.  
It is equally valuable for A1.

### Why A1 also needs this

Without this boundary, A1 could easily:

- treat operational queue state as project truth
- treat backend/index state as authoritative
- mix runtime scratch with durable project reality

So this boundary should be treated as **shared policy**.

---

## 4.2. State-layer policy

The repo already defines:

- `canonical/`
- `working/`
- `evidence/`
- `branches/`

This layering is also **shared**, not A2-only.

### For A1

A1 also needs to know:

- canonical project truth
- current working state
- evidence/review material
- branch experiment reality

So this policy is reusable directly.

---

## 4.3. Writeback policy

The current repo already says:

- do not write every chat turn
- only write meaningful state transitions
- W1 No Write
- W2 Session/Runtime Write
- W3 Working State Write
- W4 Canonical Promotion

This is one of the most reusable policies for A1.

### For A1

This prevents A1 from:

- writing every interaction into project state
- turning working files into chat logs
- promoting unstable project changes too early

This should definitely become a **shared operating rule** later.

---

## 4.4. Packet-first loading

The packet-first principle is also reusable for A1.

A1 should not startup by reading:

- all long docs
- all project rules
- all old handoffs
- all branches

Instead A1 should get:

- role/startup card
- current project state
- current direction
- task packet
- rule cards triggered by the task

This is almost exactly the same pattern that A2-Core is now testing.

---

## 4.5. Chat is interface, AICOS is structured state

Current repo rules already clarify:

- chat is where human and agent exchange and decide
- AICOS keeps structured state
- decision from chat must be committed into state appropriately

This also applies strongly to A1.

For A1 project work, this is probably even more important.

---

## 5. Shared Policies That Need A1-Specific Lane Mapping

These are reusable in principle, but cannot simply be copied verbatim.

## 5.1. Idea capture policy

The core classification is reusable:

- open question
- todo/backlog
- candidate branch idea
- tech debt
- active risk
- real decision

But current lane examples are A2-heavy, e.g.:

- A2 backlog lane
- A2 service agent paths
- AICOS self-brain specific files

### For A1, this must be remapped

Example future A1 mapping may look like:

- project open questions -> project working/open-questions
- project backlog/todo -> A1 project task lanes
- project candidate branch ideas -> project evidence/candidate-decisions
- project tech debt -> project backlog or project active-risks
- project committed decision -> project working / approval / branch lanes

### Conclusion

The classification is reusable.  
The exact lane mapping is not yet reusable as-is.

---

## 5.2. Option choose flow

The concept is reusable:

- human decides in chat
- agent commits selected option into structured state
- selected branch / current direction / blocker status become coherent

But the current examples and touched files are AICOS/A2-Core specific.

### For A1

A1 will need the same flow, but touching:

- project-specific blockers
- project-specific branch lanes
- project-specific approvals
- project-specific working state

So this is a **shared flow pattern**, not a shared exact file map.

---

## 5.3. Sync brain flow

The concept is reusable:

- meaningful changes in `brain/` can be refreshed into GBrain/PGLite

But how and when A1 triggers sync may differ.

### For A1

A1 probably does not need to think about sync in every task.
Often sync can be:

- automatic after meaningful project working changes
- delegated to A2-Serve or system helper
- triggered by workflow policy

### Conclusion

The boundary/rule is reusable, but the operating mode may differ.

---

## 6. Policies That Are A2-Only

These should not simply be reused for A1.

## 6.1. A2-Core / A2-Serve taxonomy

This is specific to the A2 system-serving side.

A1 should not inherit:

- A2-Core-R
- A2-Core-C
- A2-Serve-R
- A2-Serve-O

These are not A1 concepts.

---

## 6.2. Codex identity as A2-Core-C

This is explicitly A2-only and should not leak into A1 role cards.

---

## 6.3. AICOS self-brain specific operational lanes

Current files and lanes such as:

- AICOS self-brain working files
- A2 service backlog lane
- A2 startup cards
- A2 rule cards

are not directly reusable for A1.
Only the **pattern** is reusable.

---

## 7. Recommendation: What To Reuse For A1 Later

### Table Code: MAP-26176

| Reuse target for future A1 | Recommendation |
|---|---|
| state-layer model | reuse directly |
| writeback W1/W2/W3/W4 | reuse directly |
| “state transition, not every chat turn” | reuse directly |
| packet-first loading | reuse directly |
| chat decision -> structured state principle | reuse directly |
| idea classification taxonomy | reuse concept, remap lanes |
| option choose flow | reuse flow, remap files/paths |
| sync brain boundary | reuse boundary, simplify A1 operating mode |
| startup cards | reuse concept, create A1-specific card |
| rule cards | reuse concept, create A1-specific cards |
| task packets | reuse template, create A1 project packets |

---

## 8. Conclusion On Policy Reuse

### Short answer

Most of the **core operational policies** just created are **not only for A2**.

They can be split into:

- **shared core**
- **A2-specific implementation**
- **future A1 remapping**

### Best practice

Do not rewrite everything for A1 later.

Instead:

- keep shared policy concepts stable
- create A1-specific role/startup/rule/task packets
- remap lanes to project reality

---

## 9. Why Is AICOS Using Mostly Markdown/Text Now?

This is a good question, and the answer is architectural, not accidental.

## 9.1. Markdown is good for authority and review

Markdown/text files are excellent for:

- human readability
- AI readability
- git diff/review
- branching and merge visibility
- explicit canonical promotion
- handoff notes
- startup summaries
- rule documents
- current-state summaries

For things like:

- role definitions
- working rules
- current state
- current direction
- open questions
- active risks
- handoff notes

Markdown is often better than DB rows as the first authority surface.

---

## 9.2. The current repo already encodes this boundary

The repo already says:

- `brain/` is durable knowledge/truth/state
- `backend/` is support substrate, not authority
- `aicos sync brain` refreshes retrieval from `brain/`
- backend/GBrain/PGLite should not become truth authority

This means the current design is intentionally **Markdown-first for authority**.

---

## 9.3. Why not DB-first immediately for working state?

If you put all working state straight into DB first, you gain:

- fast query
- structured filters
- easier indexes
- easier aggregation
- simpler queue joins

But you also lose or weaken:

- git-native diff/review for meaning-rich state
- easy human inspection
- explicit branchable text reality
- transparent canonical promotion review
- low-friction manual editing
- “what changed in words” visibility

### Especially for AICOS today

AICOS is still in a highly evolving architecture phase.

Many of its most important artifacts are still:

- conceptual
- qualitative
- summary-heavy
- review-heavy
- human+AI co-edited

These are still better served by text/Markdown as the authority layer.

---

## 10. Where DB Is Actually Better

DB is excellent for:

- search indexes
- retrieval substrate
- packet registries
- queue state
- trigger state
- sync ledger
- change/event journal
- materialized summaries
- actor/task registries
- operational metrics
- maybe branch metadata
- runtime bookkeeping

### This means

DB should be heavily used — but not necessarily as the first authority for all brain/working truth.

---

## 11. Recommended Hybrid Model

### 11.1. Markdown/Text should remain authority for

- canonical truth summaries
- working state summaries
- current direction
- open questions
- active risks
- handoff notes
- role definitions
- project working rules
- evidence references
- branch narrative state
- reviewable packets that humans/agents need to inspect directly

### 11.2. DB should be used for

- retrieval/index state
- sync/import registry
- packet registry and packet metadata
- queues and waiting states
- candidate decision registry
- change journal / event ledger
- path resolution caches
- query acceleration
- task/run metadata
- future handoff registry metadata

### 11.3. Important boundary

DB should usually be:

- **derived**
- **indexed**
- **operational**
- **accelerating**

not automatically:

- the final truth authority for everything

---

## 12. What About Working State Specifically?

This is the subtle part.

### Short answer

Not all working state should stay only in Markdown forever.  
But not all working state should move into DB authority either.

### Split working state into two classes

#### Class W-A — Narrative working state
Better in Markdown:

- current-state summary
- current-direction
- open questions
- active risks
- implementation-status
- migration-status
- handoff digest

These are meaning-rich and review-heavy.

#### Class W-B — Operational working state
Better in DB or registry-like storage:

- queue state
- retry counters
- waiting status
- task run metadata
- sync-needed marker
- freshness timestamps
- registry of packets
- registry of branches
- event history

These are structured and machine-friendly.

### Conclusion

“Working state” is not one thing.  
Some working state should stay text-first; some should become DB-backed.

---

## 13. Why PGLite / Postgres Still Matters

PGLite or Postgres can be very useful now, but in the right role.

### Good immediate roles

- GBrain substrate/index store
- packet registry metadata
- sync ledger
- queue state
- candidate decision registry
- event journal
- search helper tables
- future handoff registry metadata

### Not ideal immediate role

Using PGLite/Postgres as the sole authority for:

- current-state meaning
- role definitions
- working rules
- handoff summaries
- direction summaries

at this phase would likely make the system harder to review and evolve.

---

## 14. Recommendation For Next Phases

### Phase now

Keep:

- Markdown-first authority
- DB-assisted serving/runtime/index

### Phase next

Add thin DB-backed registries for:

- task packets
- handoffs
- queues
- candidate decisions
- sync/import state

### Phase later

Only after patterns stabilize, evaluate whether some working-state subsets should become DB-authoritative.

---

## 15. Final Recommendation

### For policy reuse

Do not redo everything for A1 later.

Instead:

- extract shared core policies
- remap lanes for A1
- create A1 startup/rule/task artifacts on top of the same core principles

### For storage

Do not rush to replace Markdown with DB for all state.

Use:

- **Markdown as authority for reviewed, narrative, human+AI readable state**
- **PGLite/Postgres as accelerator and operational substrate**

This is the best fit for the current AICOS phase.

---
