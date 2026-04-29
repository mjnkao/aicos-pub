# AICOS Work State Ledger Minimal Schema Proposal

Status: schema proposal, no implementation
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Propose the smallest Work State Ledger model AICOS needs to prevent
task/checklist/open-item drift without becoming a PM tool.

This proposal follows the PM taxonomy review:

`brain/projects/aicos/evidence/research/aicos-work-state-ledger-pm-tool-taxonomy-review-20260429.md`

## Design Rule

AICOS should normalize work-state identity and relationships.

AICOS should not build a PM product.

## Core Object

Use one normalized object:

```yaml
work_item:
  id: "WI-AICOS-YYYYMMDD-NNN"
  scope: "projects/<project-id>|workspaces/<id>|companies/<id>|shared"
  kind: "task|checklist|checklist_item|open_item|open_question|tech_debt|decision_followup|phase|milestone|risk|bug|proposal"
  title: "<short title>"
  status: "open|planned|in_progress|blocked|waiting|handoff_ready|resolved|closed|deferred|stale"
  source_ref: "<authoritative markdown/source artifact>"
  state_ref: "<where current state is recorded>"
  derived_refs:
    - "<checklist/report/dashboard/query/status surfaces derived from this>"
  parent_id: "<optional parent work item id>"
  links:
    - type: "blocks|blocked_by|relates_to|duplicates|duplicated_by|derived_from|supersedes|superseded_by|evidence_for"
      target: "<work item id or source ref>"
  owner:
    actor_role: "A1|A2-Core-C|A2-Core-R|Human|system"
    agent_family: "<optional>"
    agent_instance_id: "<optional>"
    functional_role: "<optional>"
  work:
    work_type: "<planning|code|research|ops|content|design|mixed|...>"
    work_lane: "<coordination lane>"
  trace:
    source_refs: []
    artifact_refs: []
    scope_refs: []
    session_refs: []
  timestamps:
    created_at: "<iso timestamp>"
    updated_at: "<iso timestamp>"
    resolved_at: "<optional iso timestamp>"
```

## Kinds

| Kind | Meaning | Parent rules |
| --- | --- | --- |
| `task` | concrete work to execute | may have checklist/checklist_item/task children |
| `checklist` | ordered list of child work/check items | parent should be task/phase/milestone/decision_followup |
| `checklist_item` | lightweight child completion item | must have one parent checklist or task |
| `open_item` | actionable work not yet assigned to a concrete task | may become task or decision_followup |
| `open_question` | unresolved decision question | can block task/phase |
| `tech_debt` | known quality/reliability gap | may become task |
| `decision_followup` | follow-up after a decision exists | may have task/checklist children |
| `phase` | large execution slice | may have tasks/checklists/milestones |
| `milestone` | outcome marker, not necessarily work itself | may group tasks/phases |
| `risk` | risk to monitor or mitigate | may block work |
| `bug` | defect requiring fix or workaround | may become task |
| `proposal` | suggested work needing review | may become open_item/task/decision_followup |

## Lifecycle

Use one lifecycle vocabulary across kinds:

| Status | Meaning |
| --- | --- |
| `open` | known and valid, not currently active |
| `planned` | accepted for upcoming work |
| `in_progress` | actively worked by an owner/agent/lane |
| `blocked` | cannot proceed without blocker resolution |
| `waiting` | waiting on external input/time/tool |
| `handoff_ready` | ready for another actor to continue |
| `resolved` | fulfilled for current purpose, can remain visible |
| `closed` | finished and no longer active |
| `deferred` | intentionally postponed |
| `stale` | likely outdated and needs review |

Avoid separate checkbox-only truth. A checkbox in a markdown checklist is a
projection of this lifecycle, not the only state.

## Parent-Child Rules

1. A child has at most one hierarchical `parent_id`.
2. Use links for non-hierarchical relationships.
3. Avoid deep nesting by default:
   - phase -> task/checklist is okay;
   - task -> checklist/checklist_item is okay;
   - checklist_item -> child item should be avoided.
4. A checklist item can be promoted to task if it needs:
   - owner;
   - handoff;
   - source refs;
   - blocker/dependency;
   - multi-session execution.

## Link Types

| Link type | Direction | Meaning |
| --- | --- | --- |
| `blocks` / `blocked_by` | directional | one item prevents another from progressing |
| `relates_to` | symmetric | useful contextual relation, not dependency |
| `duplicates` / `duplicated_by` | directional | one item is duplicate of another |
| `derived_from` | directional | item was created from another artifact/item |
| `supersedes` / `superseded_by` | directional | newer item replaces older one |
| `evidence_for` | directional | artifact/status supports an item |

## Source Of Truth Rules

Every ledger item must include:

- `source_ref`: the authoritative artifact or original source;
- `state_ref`: the current state record;
- `derived_refs`: optional views/checklists/reports that mirror it.

Examples:

- A checklist row in `aicos-option-c-transition-checklist-20260428.md` may be
  a derived view of `WI-AICOS-...`.
- A status item file may be `state_ref`.
- An evidence memo may be `source_ref`.

## Reconciliation Rules

AICOS should add audit/reconcile tooling before database migration:

1. checklist unchecked but linked work item resolved -> warn;
2. status item open but title/summary says completed -> warn;
3. two work items with same title/source_ref/kind -> possible duplicate;
4. item deferred but referenced as active next work -> warn;
5. item blocked without `blocked_by` link or blocker text -> warn;
6. item in_progress with stale owner/session -> warn;
7. derived view points to missing source/state ref -> warn.

First implementation should be report-only.

## Storage Recommendation

Phase 1 should stay markdown-first:

- keep current status item files;
- optionally add ledger YAML blocks or generated ledger index under
  `brain/projects/<project>/working/work-ledger/`;
- do not introduce a database truth store;
- generate views from markdown/ledger into query/search indexes.

## MCP Surface Recommendation

Do not add a broad PM API.

If needed, add narrow semantic tools later:

- `aicos_get_work_items`
- `aicos_update_work_item_status`
- `aicos_link_work_items`
- `aicos_reconcile_work_state`

But first, implement a CLI/report-only reconciliation pass and observe results.

## Anti-PM Boundaries

AICOS should not implement:

- kanban board UI;
- sprint planner;
- Gantt/timeline UI;
- notification/reminder system;
- comment-thread product;
- broad assignee management UX;
- full Plane/ClickUp bidirectional sync;
- arbitrary PM custom-field engine.

AICOS owns coordination truth for agents. PM tools can display or sync a
projection later.

## Recommended Next Implementation Pass

1. Add a report-only `work-state-ledger` ADR or contract note.
2. Add a simple reconciliation script that scans:
   - status items;
   - known checklist anchors;
   - source refs;
   - summaries/next steps.
3. Produce a drift report only.
4. After two or three real drift cases, decide whether to add ledger index
   files or MCP work-item tools.
