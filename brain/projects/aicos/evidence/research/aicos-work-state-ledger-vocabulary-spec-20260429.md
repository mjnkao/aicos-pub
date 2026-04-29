# AICOS Work State Ledger Vocabulary Spec

Status: vocabulary spec, no implementation
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Define the first Work State Ledger vocabulary for:

- `kind`
- `status`
- `relation`

The goal is to make `work_item` precise enough for AICOS agents while staying
neutral enough to map into Plane, ClickUp, Trello, Asana, Notion, Airtable, and
future PM/dashboard tools.

This is not a database schema migration and not a PM connector design.

## Design Principles

1. `work_item` is the center.
2. `kind` says what kind of work-state object this is.
3. `status` says the current lifecycle/coordination state.
4. `relations` say how this item connects to other work, sources, artifacts, or
   external PM records.
5. Visual PM concepts such as board columns, list positions, sprint boards, or
   timeline views are projections, not AICOS truth.
6. AICOS should keep vocabulary small and only add new values after real use.

## Kind Vocabulary

### Summary Table

| Kind | Definition | Use when | Do not use when | Common children | PM mapping |
| --- | --- | --- | --- | --- | --- |
| `task` | Concrete work someone/agent can execute | There is a clear action and expected output | It is only a question, risk, or grouping | checklist, checklist_item, task | Plane work item, ClickUp task/subtask, Trello card, Asana task |
| `checklist` | Ordered group of child items used to track completion | A parent work item needs multiple checkable steps | Each child is independent work needing ownership; use tasks instead | checklist_item, task | ClickUp checklist, Trello checklist, Notion/Airtable child table/view |
| `checklist_item` | Lightweight child step with minimal state | Step is small, usually no independent owner/handoff | It needs owner, blocker, handoff, source refs; promote to task | none by default | Trello check item, ClickUp checklist item, lightweight Asana subtask if needed |
| `open_item` | Actionable work not yet shaped as a task | Work is real but still broad or unassigned | It is a decision question; use open_question | task, checklist | PM backlog item/task |
| `open_question` | Unresolved decision or ambiguity blocking clarity | Human/A2/product decision is needed | It can be executed without decision; use task/open_item | task, decision_followup | Task with question label/status, Notion question record |
| `tech_debt` | Known quality, reliability, maintainability, or UX gap | Existing system has known debt/friction | It is a new feature idea; use open_item/proposal | task, risk | Bug/tech-debt task, Plane issue, ClickUp task |
| `decision_followup` | Work needed after a decision is accepted | Decision exists and rollout/verification/cleanup remains | Decision itself is unresolved; use open_question | task, checklist, risk | Task/issue linked to decision doc |
| `phase` | Large execution slice containing multiple items | Sequencing multi-step work over time | It is a human PM sprint by default; do not overload | milestone, task, checklist | Plane module/cycle only if project uses it; ClickUp folder/list optionally |
| `milestone` | Outcome marker or checkpoint | Need to mark an important target/result | It contains detailed execution; use phase/task | task, phase | Milestone, module goal, Trello/Notion marker |
| `risk` | Potential future problem to monitor/mitigate | Issue may happen and needs watch/mitigation | Problem already occurred; use bug/tech_debt/task | task, open_question | Risk task/record/custom field |
| `bug` | Observed defect or broken behavior | Something is currently wrong | It is a general reliability gap; use tech_debt | task, checklist_item | Bug issue/task/card |
| `proposal` | Suggested work not yet accepted | Someone/agent proposes new project/work/policy/tool | Accepted work exists; use open_item/task/decision_followup | open_question, open_item | Intake request, ClickUp task, Plane intake/work item |

### Detailed Definitions

#### `task`

Concrete executable work.

Use when:

- someone can start doing it;
- output can be checked;
- it may need owner, handoff, blocker, checkpoint, or artifact refs.

Do not use when:

- the next step is a decision, not execution;
- it is only a small checkbox step;
- it is a broad area with unclear output.

Example:

```yaml
kind: task
title: "Implement report-only checklist reconciliation command"
```

#### `checklist`

An ordered set of child items used to track completion under a parent.

Use when:

- a task/phase/decision follow-up needs a visible breakdown;
- children are mostly lightweight;
- order/progress matters.

Do not use when:

- the children are independent work streams with owners and handoffs;
- the checklist is being used as a project plan replacement.

Rule:

- checklist is a grouping object;
- child `checklist_item` state should reconcile against parent.

#### `checklist_item`

Small child step.

Use when:

- the step is simple;
- it usually does not need independent handoff;
- it belongs to one checklist/task.

Promote to `task` when:

- it needs owner/agent instance;
- it has blocker/dependency;
- it requires source refs beyond the parent;
- it spans sessions;
- another agent must continue it.

#### `open_item`

Actionable work that is not yet fully shaped.

Use when:

- something should be done eventually;
- no concrete task packet exists;
- it is not primarily an unresolved question.

Convert to:

- `task` when execution becomes clear;
- `decision_followup` if it follows an accepted decision;
- `tech_debt` if it is a known quality gap.

#### `open_question`

Unresolved decision or ambiguity.

Use when:

- progress depends on human/A2/product choice;
- there are multiple valid options;
- executing now risks wrong direction.

Do not use for ordinary unknowns an agent can resolve by reading/searching.

#### `tech_debt`

Known defect in system quality, clarity, maintainability, reliability, docs,
tests, or UX.

Use when:

- problem exists now;
- not necessarily user-visible;
- can be paid down later.

Do not use for:

- new strategic feature ideas;
- one-time failed task;
- unresolved product question.

#### `decision_followup`

Work required because a decision has already been made.

Use when:

- architecture/product/policy decision exists;
- rollout, docs, verification, cleanup, or implementation remains.

This is different from `open_question`: the question is closed; execution
remains.

#### `phase`

Large ordered execution slice.

Use when:

- work spans many tasks/checklists;
- ordering matters;
- completion means a capability level is reached.

Do not use as default PM sprint. AICOS phases are architecture/execution
sequencing, not necessarily time-boxed cycles.

#### `milestone`

Outcome marker.

Use when:

- a target/result matters;
- it may group tasks but is not itself the execution detail.

Example:

```yaml
kind: milestone
title: "A1 agents can reliably find current project state"
```

#### `risk`

Potential problem, not necessarily already happening.

Use when:

- probability/impact should be monitored;
- mitigation may be needed;
- it can block decisions if risk grows.

Convert to:

- `bug` if it manifests as broken behavior;
- `tech_debt` if it becomes a known quality gap;
- `task` if mitigation is selected.

#### `bug`

Observed broken behavior.

Use when:

- expected behavior is known;
- actual behavior violates it;
- fix or workaround is needed.

#### `proposal`

Suggested new work, project, policy, or tool.

Use when:

- A1/agent/human proposes something not yet accepted;
- project does not exist yet;
- tool/policy should be reviewed before becoming work.

Convert to:

- `open_item` when accepted but not shaped;
- `task` when executable;
- `open_question` when decision needed;
- `deferred`/`closed` when rejected or parked.

## Status Vocabulary

### Summary Table

| Status | Definition | Agent meaning | PM mapping |
| --- | --- | --- | --- |
| `open` | valid known item, not actively being executed | can be considered, not occupied | Backlog/Todo/card open |
| `planned` | accepted for upcoming work | chosen but not started | Planned/Scheduled |
| `in_progress` | actively owned/being worked | check owner/lane before takeover | In Progress/Doing |
| `blocked` | cannot progress until blocker resolved | read blocker relation/question | Blocked/Waiting on |
| `waiting` | waiting on external input/time/tool | do not assume failure; check wait reason | Waiting/Pending |
| `handoff_ready` | ready for another actor to continue | safe takeover if constraints met | Ready for pickup/custom |
| `resolved` | fulfilled for current purpose, still useful as evidence | do not redo; can cite evidence | Done/Resolved |
| `closed` | no longer active or relevant | do not surface as next work | Closed/Archived |
| `deferred` | intentionally postponed | do not act until reopened | Deferred/Later |
| `stale` | likely outdated/needs review | verify before using | Needs review/custom |

### Status Rules

#### `open`

Default valid state.

Use when:

- item is real;
- not accepted into near-term plan;
- no current owner.

#### `planned`

Accepted for upcoming work.

Use when:

- manager/A2 chose it;
- sequence is known;
- execution has not started.

#### `in_progress`

Active work.

Required fields:

- owner or observed actor;
- `work_lane`;
- latest checkpoint or state note when available.

Agent rule:

- another agent should not take over without handoff/review/pair-work signal.

#### `blocked`

Cannot proceed usefully.

Required:

- `blocked_by` relation, or blocker summary;
- owner of next decision/action if known.

Do not use for ordinary TODOs.

#### `waiting`

Waiting on something external or time-based.

Examples:

- waiting on human reply;
- waiting on API/rate limit;
- waiting on scheduled run;
- waiting on external system.

Difference from `blocked`:

- blocked usually needs resolution;
- waiting may simply need time/input.

#### `handoff_ready`

Ready for another actor to continue.

Required:

- latest checkpoint/handoff ref;
- source/artifact refs;
- takeover constraints if any.

This is AICOS-specific and AI-native. Most PM tools do not model this cleanly;
map to custom status/label.

#### `resolved`

Fulfilled for current purpose but remains part of evidence/history.

Use when:

- task/status item/checklist item is done;
- future agents may need to know it was done.

Difference from `closed`:

- resolved still useful in current context;
- closed is removed from active surfaces.

#### `closed`

No longer active/relevant.

Use when:

- completed and no longer useful as active context;
- duplicate is closed in favor of another item;
- proposal rejected.

#### `deferred`

Intentionally postponed.

Required:

- reason or reopening trigger.

#### `stale`

May be wrong or outdated.

Use when:

- checklist/status mismatch is detected;
- source refs point to old direction;
- next step no longer matches current plan.

## Relation Vocabulary

### Summary Table

| Relation | Direction | Definition | Use when | PM mapping |
| --- | --- | --- | --- | --- |
| `parent_of` / `child_of` | directional | hierarchical containment | one item owns another as breakdown | subtask/checklist hierarchy |
| `blocks` / `blocked_by` | directional | progress dependency | one item must resolve before another progresses | dependency/blocker |
| `relates_to` | symmetric | contextual link, no dependency | useful context but no ordering | related task/link |
| `duplicates` / `duplicated_by` | directional | same work represented twice | one item should be canonical | duplicate relation |
| `derived_from` | directional | created from source item/artifact | item came from feedback/proposal/memo | source/backlink |
| `supersedes` / `superseded_by` | directional | newer item replaces older | direction changed or stale item replaced | linked replacement |
| `evidence_for` | directional | artifact supports item state/claim | proof of completion/decision/status | attachment/link/reference |
| `external_ref` | directional | maps to external PM/repo/design/doc artifact | cross-system projection | URL/task ID/link |

### Relation Rules

#### Parent-child

Use only for hierarchy.

Rules:

- one hierarchical parent per child;
- shallow by default;
- use links for cross-cutting relationships.

Examples:

- phase parent_of task;
- task parent_of checklist;
- checklist parent_of checklist_item.

#### Blocks / Blocked By

Use only when progress order matters.

Examples:

- open question blocks implementation task;
- auth decision blocks LAN rollout;
- feedback missing context blocks A1 handoff.

Required for `blocked` status unless blocker is embedded in summary.

#### Relates To

Loose context link.

Use when:

- two items are connected but neither owns/blocks the other;
- agent should see both during review.

Do not overuse; too many `relates_to` links become graph noise.

#### Duplicates

Use when two items represent same work/question.

Canonical item should be explicit.

Status behavior:

- duplicate item should become `closed` or `resolved` with relation to
  canonical item.

#### Derived From

Use for provenance.

Examples:

- work item derived from A1 feedback;
- task derived from decision memo;
- open question derived from failed eval.

#### Supersedes

Use when new direction replaces old direction.

This is stronger than `relates_to`.

#### Evidence For

Use to connect proof to state.

Examples:

- commit evidence_for resolved task;
- eval report evidence_for retrieval quality;
- relation audit evidence_for trace hygiene.

#### External Ref

Use to map AICOS item to external systems.

This relation is part of projection, not authority.

Examples:

- ClickUp task URL;
- Plane work item ID;
- Trello card URL;
- Figma file;
- GitHub issue;
- external repo path.

## PM Tool Compatibility Review

### Plane

Fit: good.

- `task`, `bug`, `open_item` map to work items.
- `phase` can map to module or cycle only when useful.
- `blocks`, `blocked_by`, `relates_to`, `duplicates` map naturally to work-item
  relations.
- `handoff_ready` likely needs custom state/label.

Concern:

- Plane is still software/project-work biased. AICOS should not make cycles
  default.

### ClickUp

Fit: good.

- `work_item` maps to task.
- `checklist_item` can map to checklist item when lightweight.
- promoted child task maps to subtask.
- `blocks/blocked_by` maps to dependencies.
- `relates_to` maps to relationship.

Concern:

- ClickUp hierarchy is deep. AICOS should not copy Workspace/Space/Folder/List.

### Trello

Fit: moderate.

- `task/open_item/bug` map to card.
- `checklist` and `checklist_item` map well to card checklist/check item.
- board/list maps to view/status projection.

Concern:

- Trello has weak native dependency/relation semantics. AICOS must keep
  relations internally and export links/labels/comments as projection.

### Asana

Fit: good.

- `work_item` maps to task.
- `parent_id` maps to subtask only for shallow hierarchy.
- `blocks/blocked_by` maps to dependencies.
- derived views can map to multi-project membership.

Concern:

- multi-homing is powerful but can confuse AICOS authority. AICOS should keep
  one canonical item and many derived views.

### Notion / Airtable

Fit: good for research/content/design.

- `work_item` maps to page/record.
- kind/status/work_lane map to properties.
- relations map to relation fields.

Concern:

- arbitrary database schemas can drift. AICOS should own vocabulary and only
  project it into Notion/Airtable schemas.

## Vocabulary Review Risks

### Risk 1: Too Many Kinds

The proposed kind list is already near the upper limit.

Mitigation:

- do not add more kinds until real use proves need;
- prefer `kind + tags/metadata` over new kind.

### Risk 2: `resolved` vs `closed` Confusion

This distinction is useful for AICOS but may confuse humans.

Mitigation:

- resolved = done but still visible as evidence;
- closed = no longer active/relevant.

### Risk 3: `open_item` vs `task`

Agents may overuse `open_item`.

Mitigation:

- task requires executable output;
- open_item means actionable but not shaped.

### Risk 4: `phase` vs `milestone`

Agents may confuse work slice with outcome marker.

Mitigation:

- phase contains work;
- milestone marks outcome.

### Risk 5: Relation Graph Noise

`relates_to` can become dumping ground.

Mitigation:

- use `relates_to` only when it changes what an agent should read or do;
- otherwise use source refs or artifact refs.

### Risk 6: PM Mapping Pressure

ClickUp/Trello/Plane may push AICOS into their shape.

Mitigation:

- keep AICOS vocabulary as source;
- PM sync uses `pm_projection`;
- default sync modes remain `export_only` or `evidence_import`.

## Recommended Acceptance Criteria

Before implementation, the vocabulary is acceptable if:

1. every current AICOS status item can map to one `kind`;
2. every current status can map to one lifecycle value;
3. checklist drift can be represented without adding UI;
4. Plane/ClickUp/Trello can display a useful projection;
5. no field requires building PM-specific UX;
6. handoff/takeover remains first-class for AI agents.

## Recommended Next Step

Create a report-only reconciliation prototype that uses this vocabulary to
classify existing status items and checklist anchors. It should output warnings
only, not mutate truth.
