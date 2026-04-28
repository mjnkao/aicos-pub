# STR-26185 — AICOS Storage Structure For Handoff, Open Items, Open Questions, Risks, Research, And Agent Tasks

**Status:** working-structure-guide-v1  
**Project:** AICOS  
**Date:** 2026-04-18  
**Purpose:** chuẩn hóa rõ:
- handoff nên lưu ở đâu và theo cấu trúc nào
- open items / open questions / candidate branch ideas / tech debt / research / risks nên lưu ở đâu
- quy tắc phân biệt rõ khi nào lưu vào:
  - `brain/projects/<project_id>/...`
  - `brain/shared/...`
  - `agent-repo/.../tasks/...`

---

## 1. Executive Summary

AICOS cần phân biệt rõ 3 lớp dữ liệu:

### 1.1. Shared project/system understanding
Đây là tri thức, trạng thái, câu hỏi, risk, direction, và handoff mà nhiều actors cần nhìn chung khi bước vào một project.

### 1.2. Actor execution state
Đây là task queue, backlog, blocked, waiting, current execution, session scratch của từng actor hoặc class actors.

### 1.3. Reference / evidence / provenance
Đây là các note, evidence, research material, migration notes, implementation notes, review packs.

### Kết luận

Không nên trộn các lớp này vào cùng một lane.

---

## 2. Core Principle

### Principle A

`brain/projects/<project_id>/...` giữ **project reality**.

### Principle B

`brain/shared/...` giữ **cross-project / reusable / system-wide shared knowledge**.

### Principle C

`agent-repo/.../tasks/...` giữ **actor execution tasks**, không phải project truth.

### Principle D

`docs/...` giữ **design notes, migration notes, review notes, reference material**, không phải active working truth mặc định.

---

## 3. Recommended Project Structure

### Tree Code: STR-26186

```text
brain/
  shared/
    glossary/
    policies/
    service-knowledge/
    templates/
    handoffs/                # only for true cross-project/system-wide handoffs
  projects/
    <project_id>/
      canonical/
      working/
        current-state.md
        current-direction.md
        open-questions.md
        open-items.md
        active-risks.md
        potential-risks.md
        tech-debt.md
        implementation-status.md
        migration-status.md
        handoff/
          current.md
          episodes/
            YYYY-MM-DD_<actor-lane>_<topic>.md
      evidence/
        candidate-decisions/
        research/
        review-packs/
        source-references/
      branches/
        <branch-id>/
```

### Rule

This is the preferred structural direction for project-level truth and unresolved project knowledge.

---

## 4. Handoff Structure

## 4.1. Default rule

Handoff should be **project-scoped by default**.

If the scope is:

- `projects/aicos`

then the handoff should live under:

- `brain/projects/aicos/working/handoff/`

### Important

Do not use `docs/migration/` as the permanent home of active handoff.  
`docs/migration/` may temporarily contain migration/refinement notes, but active handoff should be normalized into project working lanes.

---

## 4.2. Three-layer handoff model

### H1 — Current handoff index

Location:

- `brain/projects/<project_id>/working/handoff/current.md`

Purpose:

- current continuity summary
- newest/current
- stale/reference-only
- what changed
- what did not change
- what next actor should know

### H2 — Episodic handoff notes

Location:

- `brain/projects/<project_id>/working/handoff/episodes/`

Purpose:

- bounded pass/test/refinement handoffs
- not startup-default
- on-demand provenance

### H3 — Self-brain digest

Location:

- `brain/projects/<project_id>/working/`

Purpose:

- stable/current facts digested from handoffs into:
  - current-state
  - current-direction
  - open-questions
  - active-risks
  - implementation-status
  - migration-status

---

## 4.3. When handoff should be shared

Only use:

- `brain/shared/handoffs/`

when the handoff is truly:

- cross-project
- cross-workspace
- system-wide
- actor-family-wide
- not tied to one project’s working reality

### Examples

- global serving outage affecting many projects
- cross-project policy migration
- system-wide actor/rule model change that multiple projects must know

### Rule

Do not use `brain/shared/handoffs/` as the default handoff lane.

---

## 4.4. Handoff naming rule

### For current index

Use a stable name:

- `current.md`

inside the project handoff folder.

### For episodes

Use bounded dated names:

- `YYYY-MM-DD_<actor-lane>_<topic>.md`

Examples:

- `2026-04-18_a2-core_context-loading.md`
- `2026-04-18_a2-core_packet-tests.md`
- `2026-04-18_a2-core_handoff-refinement.md`

### Metadata/header should include

- date
- status
- scope
- actor lane
- handoff layer
- purpose

---

## 5. Open Questions, Open Items, Tech Debt, Research, Risks

## 5.1. Open Questions

Location:

- `brain/projects/<project_id>/working/open-questions.md`

Use for:

- unresolved project questions
- architecture questions
- sequencing questions
- review questions
- research questions not yet assigned as an execution task

### Example

- Should A2-Serve become active now or later?
- Should task packets gain richer metadata?

---

## 5.2. Open Items

Location:

- `brain/projects/<project_id>/working/open-items.md`

Use for:

- unresolved project-level items
- things the project must not forget
- items that matter to current direction but are not yet actor-assigned tasks
- “needs follow-up” items that are broader than one actor task

### Example

- clarify handoff normalization path
- decide storage split between Markdown and DB-backed registries
- verify future A1 startup card location

### Rule

Open items are not the same as actor tasks.

---

## 5.3. Candidate Branch Ideas

Location:

- `brain/projects/<project_id>/evidence/candidate-decisions/`

Use for:

- branch ideas not yet approved
- alternate implementation directions
- candidate architectural routes
- option ideas not yet selected

### Rule

Do not create official branch reality in `branches/` until the candidate is chosen or clearly activated.

---

## 5.4. Tech Debt

### Tech debt note at project level

Location:

- `brain/projects/<project_id>/working/tech-debt.md`

Use for:

- debt acknowledged at project level
- debt not yet assigned as execution work
- debt affecting project planning or current direction

### Tech debt as actionable work

Location:

- `agent-repo/.../tasks/backlog/`

Use when:

- a tech debt item has become a concrete actor task
- it now has a likely owner or execution lane
- it belongs in backlog/current/blocked/waiting flow

---

## 5.5. Research Directions And Research Material

### Research question/direction

Location:

- `brain/projects/<project_id>/working/open-questions.md`

Use for:

- what still needs deeper investigation
- what the project wants to understand better

### Research material / exploration notes

Location:

- `brain/projects/<project_id>/evidence/research/`

Use for:

- collected research notes
- comparative analysis
- raw exploration
- source-backed materials
- notes that are not startup-default truth

### Assigned research task

Location:

- `agent-repo/.../tasks/...`

Use when:

- research is now a concrete assigned execution task

---

## 5.6. Risks

### Active risks

Location:

- `brain/projects/<project_id>/working/active-risks.md`

Use for:

- risks with enough evidence/impact to actively track

### Potential risks

Location:

- `brain/projects/<project_id>/working/potential-risks.md`

Use for:

- risk suspicions
- concerns not yet verified
- possible failure modes that need checking later
- “not enough time to verify yet” items

### Rule

Do not put every suspicion directly into `active-risks.md`.

---

## 6. Agent Task Structure

## 6.1. Where execution tasks belong

Actor execution tasks belong in:

- `agent-repo/.../tasks/...`

### Typical task lanes

- backlog
- current
- blocked
- waiting
- done/archive
- task-packets
- session or scratch if needed

### Why

These tasks are:

- actor-owned
- execution-oriented
- status-driven
- queue-driven
- not project truth themselves

---

## 6.2. Important distinction

A task in `agent-repo/.../tasks/...` can still be “about the project”.

But it is:

- an actor’s execution object
- not the project’s shared truth object

### Short rule

`brain/projects/<id>/working/` answers:

- what the project currently is / knows / needs to think about

`agent-repo/.../tasks/` answers:

- what a specific actor is doing / waiting on / blocked on

---

## 7. Decision Rules: What Goes Where

### Table Code: STR-26187

| Information type | Correct lane |
|---|---|
| current shared project state | `brain/projects/<id>/working/current-state.md` |
| current shared project direction | `brain/projects/<id>/working/current-direction.md` |
| startup continuity summary | `brain/projects/<id>/working/handoff/current.md` |
| bounded pass/test handoff | `brain/projects/<id>/working/handoff/episodes/` |
| unresolved project question | `brain/projects/<id>/working/open-questions.md` |
| unresolved project item | `brain/projects/<id>/working/open-items.md` |
| unapproved branch/option idea | `brain/projects/<id>/evidence/candidate-decisions/` |
| project-level tech debt note | `brain/projects/<id>/working/tech-debt.md` |
| research material | `brain/projects/<id>/evidence/research/` |
| potential risk not yet verified | `brain/projects/<id>/working/potential-risks.md` |
| active risk | `brain/projects/<id>/working/active-risks.md` |
| actor backlog/current/blocked/waiting task | `agent-repo/.../tasks/...` |
| actor task packet | `agent-repo/.../tasks/...` or task-packets lane |
| cross-project reusable knowledge | `brain/shared/...` |
| cross-project/system-wide handoff | `brain/shared/handoffs/` only if truly shared |
| migration/refinement note | `docs/migration/` or evidence/reference lane |

---

## 8. When To Store In `brain/projects/.../working/`

Store in project working lane when the information is:

- project-shared
- relevant to multiple actors
- needed for orientation or continuation
- not yet a concrete actor task
- part of current best understanding
- part of project continuity

### Examples

- current direction
- open questions
- open items
- tech debt notes
- potential risks
- active risks
- handoff current index

---

## 9. When To Store In `agent-repo/.../tasks/...`

Store in agent task lane when the information is:

- actionable
- actor-owned
- has execution status
- belongs in queue/backlog/current/blocked/waiting
- concrete enough to be worked on by an actor
- not just shared project understanding

### Examples

- implement handoff normalization
- verify packet summary rendering
- research DB registry options
- update startup card wording
- investigate PATH consistency issue

---

## 10. When To Store In `brain/shared/...`

Store in `brain/shared/...` only when the information is:

- reusable across projects
- not tied to one project’s working reality
- shared policy/reference/glossary/service knowledge
- system-wide

### Examples

- glossary
- shared policy references
- shared templates
- shared service knowledge
- true system-wide handoffs

### Do not store here by default

- project handoffs
- project open questions
- project tech debt
- actor tasks
- project candidate branch ideas

---

## 11. Suggested Shared Structure

### Tree Code: STR-26188

```text
brain/shared/
  glossary/
  policies/
  templates/
  service-knowledge/
  handoffs/          # use only for true cross-project/system-wide handoffs
```

---

## 12. Notes vs Tasks vs Handoffs

## 12.1. Notes

Notes are:

- reference
- explanation
- provenance
- research material
- migration note
- review note

Likely lanes:

- `docs/migration/`
- `brain/.../evidence/...`

## 12.2. Tasks

Tasks are:

- actor-owned execution units
- status-driven
- queue-based
- actionable

Likely lanes:

- `agent-repo/.../tasks/...`

## 12.3. Handoffs

Handoffs are:

- continuity objects
- session/pass transition summaries
- newest/current/stale guidance
- next-agent guidance

Likely lanes:

- `brain/projects/<id>/working/handoff/...`
- `brain/shared/handoffs/` only when genuinely shared

---

## 13. Immediate Normalization Recommendation

### Recommendation A

Move active project handoff out of `docs/migration/` over time and normalize into:

- `brain/projects/aicos/working/handoff/current.md`

### Recommendation B

Move project episodic handoffs into:

- `brain/projects/aicos/working/handoff/episodes/`

### Recommendation C

Keep `docs/migration/` for:

- migration notes
- implementation notes
- review packs
- reference-only design or refinement notes

### Recommendation D

If `brain/shared/handoffs/` already exists but is not truly active for shared/system-wide handoffs:
- mark it reserved/not-active
- or remove/deprecate it
- do not let it remain ambiguous

---

## 14. Final Rule Set

### Rule 1

Project continuity belongs with the project.

### Rule 2

Shared knowledge belongs in shared only if it is truly shared.

### Rule 3

Actor execution belongs in agent-repo tasks.

### Rule 4

Unresolved project knowledge is not automatically an actor task.

### Rule 5

Do not use `current-state.md` as a dump for all unresolved information.

### Rule 6

Do not use `docs/migration/` as the permanent home of active project handoff.

---

## 15. Final Reminder To Codex

When deciding where to store something, ask:

1. Is this shared project understanding?
2. Is this a concrete actor execution task?
3. Is this just reference/provenance?
4. Is this project-scoped or truly shared across projects?
5. Is this continuity/handoff or is it just a note?

Then place it in the smallest correct lane.

AICOS should be structured so that:

- project truth stays with the project
- shared knowledge stays shared
- actor work stays with the actor
- continuity is easy to follow
- startup stays light

---
