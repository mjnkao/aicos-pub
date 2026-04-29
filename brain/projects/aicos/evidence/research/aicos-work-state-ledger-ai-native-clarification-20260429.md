# AICOS Work State Ledger AI-Native Clarification

Status: architecture clarification
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Clarify how AICOS should apply the Work State Ledger idea without becoming a PM
tool, and whether the current direction is genuinely AI-native.

This note builds on:

- `aicos-work-state-ledger-pm-tool-taxonomy-review-20260429.md`
- `aicos-work-state-ledger-minimal-schema-proposal-20260429.md`

## Short Answer

The current direction is promising, but it is only AI-native if AICOS treats
the ledger as an **agent coordination and context continuity layer**, not as a
human project-management product.

That means AICOS owns:

- work-state identity;
- source/context refs;
- agent ownership and handoff semantics;
- blocker/dependency semantics;
- reconciliation/drift detection;
- MCP read/write behavior for agents;
- mappings to external PM tools.

AICOS does **not** own:

- board UI;
- comments product;
- notification system;
- sprint planner;
- Gantt/timeline UX;
- broad custom-field engine;
- full PM workflow automation;
- bidirectional PM sync as default.

## What Problem AICOS Solves Here

The real problem is not "AICOS needs tasks."

The real problem is:

```text
AI agents need a stable, portable way to know:
- what work exists;
- what is active;
- what is blocked;
- what was completed;
- what depends on what;
- what source/context proves it;
- who/which agent touched it;
- what can safely be continued next.
```

PM tools solve human planning and visual coordination. AICOS solves **AI-agent
continuity and context correctness** across tools, projects, machines, and
agent families.

## Neutral Layer, Not PM Tool

AICOS should define a neutral internal model and map it to external tools.

```text
AICOS Work State Ledger
  -> Plane work item / module / cycle
  -> ClickUp task / subtask / checklist / relationship
  -> Asana task / subtask / project / dependency
  -> Trello card / checklist item / list
  -> Notion page / database relation / status
  -> Airtable record / linked record / select status
```

The ledger should be smaller than all of these tools.

If a field only helps a human board, it does not belong in AICOS core. If a
field helps an agent avoid stale context, unsafe takeover, duplicated work, or
wrong authority, it belongs in AICOS.

## Core Schema Shape

The core should stay close to this:

```yaml
work_item:
  id: "WI-AICOS-..."
  scope: "projects/<id>"
  kind: "task|checklist_item|open_question|tech_debt|decision_followup|risk|proposal|phase|milestone"
  title: "<short>"
  status: "open|planned|in_progress|blocked|waiting|handoff_ready|resolved|closed|deferred|stale"
  authority:
    source_ref: "<where this item is defined or justified>"
    state_ref: "<where current state is recorded>"
    derived_refs: []
  relations:
    parent_id: "<optional hierarchical parent>"
    links:
      - type: "blocks|blocked_by|relates_to|duplicates|derived_from|supersedes|evidence_for"
        target: "<work_item_id|source_ref|external_ref>"
  agent_context:
    actor_role: "A1|A2-Core-C|A2-Core-R|Human|system"
    agent_family: "<codex|claude|antigravity|openclaw|...>"
    agent_instance_id: "<session/worker id>"
    functional_role: "<CTO|coder|researcher|designer|manager|...>"
    work_lane: "<coordination lane>"
    work_type: "<code|content|design|research|ops|planning|mixed>"
  handoff:
    handoff_status: "none|needed|ready|taken_over"
    latest_checkpoint_ref: "<optional>"
    takeover_constraints: []
  pm_projection:
    external_tool: "plane|clickup|asana|trello|notion|airtable|none"
    external_ref: "<optional>"
    sync_mode: "none|export_only|evidence_import|reviewed_bidirectional"
```

This schema is not meant to be implemented as a database immediately. It is the
semantic shape that markdown, MCP tools, generated indexes, and future PM
adapters should converge toward.

## What Makes It AI-Native

### 1. Agent-Readable State Before Human UI

A PM tool usually optimizes for a board, list, timeline, or notification.

AICOS should optimize for questions like:

- "What should I read before continuing this work?"
- "Is another agent already working on this lane?"
- "What changed since the last checkpoint?"
- "What source proves this item is resolved?"
- "Can I safely take over?"
- "Which blocker is preventing progress?"
- "Is this checklist stale compared with status items?"

If these are first-class read surfaces, the design is AI-native.

### 2. Context Refs Are Mandatory

Human PM tasks can survive with vague descriptions. Agent tasks cannot.

Every meaningful item needs refs:

- `source_ref`: why this exists;
- `state_ref`: where current state lives;
- `artifact_refs`: files/docs/designs/repos involved;
- `checkpoint_ref`: what the last agent did;
- `handoff_ref`: what the next agent needs.

This is a stronger requirement than most PM tools impose.

### 3. Status Is Not Just Progress

For AI agents, status must include coordination meaning:

- `in_progress`: an actor may be occupying a lane/worktree/context.
- `blocked`: the next useful action is not more execution but blocker
  resolution.
- `handoff_ready`: another agent can continue safely.
- `stale`: this surface may be misleading.
- `resolved`: fulfilled, but still useful as evidence.

This is different from a simple Kanban column.

### 4. Reconciliation Is A Core Feature

AICOS should actively detect mismatches:

- checklist says unchecked, status item says resolved;
- handoff says ready, task says in progress;
- item says blocked, but no blocker link exists;
- open item duplicates another decision follow-up;
- PM task moved to done, but AICOS source refs do not support closure.

This is AI-native because it protects agents from stale or contradictory
context.

### 5. PM Tools Are Projections

Plane/ClickUp/Asana may display AICOS work, but should not automatically become
AICOS truth.

Recommended sync modes:

| Mode | Meaning |
| --- | --- |
| `none` | no external PM link |
| `export_only` | AICOS exports state to PM tool for humans |
| `evidence_import` | PM events become evidence/status candidates, not truth |
| `reviewed_bidirectional` | selected fields sync after explicit mapping/review |

Default should be `export_only` or `evidence_import`, not full bidirectional
sync.

## Neutral Mapping Rules

### To Plane

- `work_item.kind=task/open_item/bug` -> Plane work item
- `phase/milestone` -> module or cycle only if the project actually uses those
- `blocks/blocked_by` -> Plane relation
- `source_ref/artifact_refs` -> links/description

Do not force all AICOS work into Plane cycles.

### To ClickUp

- `work_item` -> task
- `checklist_item` -> checklist item if lightweight, subtask if owned/handoff
  needed
- `blocks/blocked_by` -> dependency
- `relates_to` -> relationship

Do not copy ClickUp's full Space/Folder/List hierarchy into AICOS.

### To Asana

- `work_item` -> task
- `phase/milestone` -> project section/milestone-like task or portfolio mapping
  later
- `parent_id` -> subtask only when shallow
- same `work_item_id` can appear in many derived views, but AICOS truth remains
  one item.

Do not make multi-homing default for AICOS truth.

### To Trello

- `work_item` -> card
- `checklist_item` -> card checklist item when lightweight
- status view -> list only as projection

Do not treat Trello list position as AICOS authority.

### To Notion/Airtable

- `work_item` -> page/record
- `kind/status/work_lane` -> properties/fields
- links -> relation fields
- source refs -> URL/text/file refs

Do not let arbitrary database schemas redefine AICOS semantics.

## What Is Missing From The Current Proposal

The current schema proposal is directionally right but needs three refinements
before implementation:

1. **Separate semantic state from PM projection**
   - Add an explicit `pm_projection` section.

2. **Make handoff/takeover fields first-class**
   - `handoff_status`, `latest_checkpoint_ref`, `takeover_constraints`.

3. **Make reconciliation a first-class read/check operation**
   - The first implementation should be report-only and should not mutate
     truth.

## Recommended Next Build Step

Do not build a database yet.

Do this first:

1. Create a Work State Ledger contract/ADR with:
   - schema shape;
   - mapping rules;
   - anti-PM boundaries;
   - reconciliation rules.
2. Build a report-only reconciliation command:
   - scans status items and known checklist anchors;
   - finds stale/contradictory states;
   - outputs warnings only.
3. Run it on AICOS itself.
4. Only after repeated useful warnings, decide whether to add:
   - ledger index files;
   - MCP work-item read tool;
   - MCP work-item update tool.

## CTO Judgment

The Work State Ledger is worth doing because it solves an AICOS-native problem:
agents need consistent, source-linked, handoff-aware work state.

It becomes non-AI-native if it drifts into:

- human board management;
- PM custom-field sprawl;
- sprint planning;
- notification UX;
- generic task app behavior;
- syncing every field with external PM tools.

The right version is small, neutral, source-linked, reconciliation-focused, and
designed for agents to continue work safely.
