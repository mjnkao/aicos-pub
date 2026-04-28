# AICOS Phase 7 Plane / ClickUp Integration Contract

Status: phase-7 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Define how AICOS should integrate with Plane, ClickUp, or similar PM/dashboard
tools without surrendering AICOS context/control-plane identity.

This note is a contract direction only. It does not build a connector or sync
engine.

## Authority Model

Recommended model: hybrid with AICOS semantic authority.

AICOS owns:

- actor identity and work lane continuity;
- handoff/takeover semantics;
- context source refs;
- semantic status item lifecycle;
- feedback/tool/search friction;
- authority/freshness metadata.

PM tool owns:

- human-friendly board layout;
- task display;
- comments and lightweight collaboration;
- due dates/reminders where the team already uses them;
- notification UX;
- optional human assignment view.

Shared:

- task title;
- task status;
- owner/assignee;
- priority;
- blocker flag;
- links/source refs;
- activity events.

## Field Mapping

| Concept | AICOS field/object | PM tool field | Authority |
| --- | --- | --- | --- |
| project | `scope` | project/space | shared, mapped |
| lane | `work_lane` | label/component/list | AICOS |
| task/status item | `task_ref` / `item_id` | issue/task id | shared |
| semantic status | `task_status` / `item_status` / handoff status | column/status | shared with mapping |
| actor identity | `actor_role`, `agent_family`, `agent_instance_id` | assignee/custom fields/comment actor | AICOS |
| functional role | `logical_role` / project role | role label/custom field | project-owned |
| source refs | `source_ref`, `artifact_refs`, `trace refs` | links/description | AICOS |
| human comments | evidence or external refs | comments | PM tool first, AICOS refs only |
| priority | status item/task metadata | priority | shared |
| canonical truth | `brain/.../canonical` | not PM canonical | AICOS |

## Sync Direction

Near-term:

- AICOS -> PM for display of active work, blockers, handoff-ready state.
- PM -> AICOS only through reviewed/semantic connector events, not raw comment
  scraping into truth.

Later:

- bidirectional sync for selected fields after conflict rules are explicit.

Do not begin with full bidirectional sync. It is high-friction and can corrupt
authority boundaries.

## Conflict Rules

If AICOS and PM disagree:

1. canonical AICOS truth wins for context/decision facts;
2. AICOS working state wins for handoff/agent continuity;
3. PM tool may win for visual status if humans intentionally move the board;
4. connector should write a status item or evidence note when conflict matters;
5. never silently overwrite canonical truth from PM comments or task text.

## AI Coworker Activity Model

PM/dashboard should show AI agents as coworkers, but not flatten identity.

Minimum display:

- display name;
- client family;
- functional role;
- work lane;
- current state;
- last update time;
- next step;
- handoff/takeover readiness;
- source refs.

Behind the display, AICOS preserves:

- `actor_role`;
- `agent_family`;
- `agent_instance_id`;
- `work_type`;
- `work_lane`;
- `execution_context`.

## Connector Minimal Contract

Future connector should support:

```yaml
export_to_pm:
  scope: "projects/<project-id>"
  objects:
    - status_items
    - active_task_state
    - handoff_ready
    - human_attention_queue

import_from_pm:
  source_event:
    pm_tool: "plane|clickup|..."
    event_type: "status_changed|comment_added|assignee_changed|..."
    external_ref: "<url/id>"
  mapping_policy: "evidence_only|working_update_candidate|ignored"
```

Default import policy should be `evidence_only` until stronger governance is
implemented.

## What Not To Build Now

- no full Plane connector;
- no ClickUp connector;
- no bidirectional sync engine;
- no task database replacement;
- no custom dashboard;
- no PM-tool-first authority migration.

## Implementation Sequence Later

1. Define dashboard read surfaces in AICOS.
2. Export read-only board summary to one PM/dashboard target.
3. Add human attention queue.
4. Add reviewed import of selected PM events as evidence.
5. Only then consider bidirectional field sync.

## CTO Judgment

PM integration is important for company-100, but it should sit above AICOS
semantics. The correct near-term work is to make AICOS state/search/handoff
strong enough that a dashboard can trust it.

Search quality is a prerequisite: if A1 agents cannot reliably find the right
context, a dashboard will only make confusion more visible.
