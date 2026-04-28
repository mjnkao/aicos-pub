# AICOS Phase 6 Human + AI Coworker Model

Status: phase-6 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Prepare AICOS for human + AI coworker coordination and future dashboard/PM-tool
integration without turning AICOS into a PM tool clone.

This note defines semantics only. It does not build a dashboard.

## Product Rule

AICOS is not the board. AICOS is the context/control-plane behind humans and AI
agents working together.

Dashboard/PM tools should show the shared working reality, but AICOS should
continue to own:

- context authority;
- handoff semantics;
- agent identity;
- work lane continuity;
- feedback and retrieval quality signals;
- source refs and traceability.

## Coworker Object Model

Minimum coworker state:

```yaml
coworker:
  actor_role: "A1|A2-Core-C|A2-Core-R|Human"
  agent_family: "codex|claude-code|gemini-antigravity|openclaw|human|..."
  agent_instance_id: "<session/worker id>"
  display_name: "<human-friendly name>"
  logical_role: "<functional role>"
  service_relationship: "external-work-actor|internal-aicos-maintainer|human-manager|human-reviewer|automation"
  execution_context: "<where work happens>"
```

Minimum work state:

```yaml
work_item:
  scope: "projects/<project-id>"
  work_lane: "<coordination lane>"
  work_type: "code|research|planning|ops|content|design|mixed"
  task_ref: "<task/packet/status item/ref>"
  status: "planned|in_progress|blocked|handoff_ready|waiting|completed"
  owner: "<coworker ref>"
  next_step: "<bounded next action>"
  source_refs: []
```

## State Semantics

| Status | Meaning | Dashboard implication |
| --- | --- | --- |
| `planned` | known work, not actively owned | can be picked up |
| `in_progress` | actor is actively working | show owner/lane |
| `blocked` | cannot proceed without blocker resolution | human/agent attention needed |
| `waiting` | waiting on external input or async result | show wait reason |
| `handoff_ready` | ready for another actor to continue | highlight takeover |
| `completed` | completed for this continuity slice | show done, preserve refs |

## Ownership Rules

- One work lane may have multiple related artifacts, but active ownership should
  be clear.
- A handoff-ready item must include enough context for takeover without broad
  rediscovery.
- Humans can override assignment/priority, but AICOS should preserve the prior
  actor/source refs.
- AI agents should not silently take over another dirty code worktree unless the
  handoff explicitly allows it.

## Blocker Semantics

| Blocker type | Meaning | Required output |
| --- | --- | --- |
| `blocked_by_human` | needs decision, review, approval, credentials, or priority | question + options/source refs |
| `blocked_by_agent` | another agent owns needed work or handoff missing | owner/lane/ref |
| `blocked_by_tool` | MCP/search/runtime/tool issue | feedback item + workaround |
| `blocked_by_context` | required context missing or contradictory | feedback/status item + expected source |
| `blocked_by_external_system` | external repo/API/service unavailable | evidence/ref + retry/owner |

## Dashboard-Facing Read Surfaces

Minimum future read surfaces:

1. `active_workers`
   - who is active by project/work_lane;
   - actor identity and functional role;
   - last seen/write time.

2. `active_lanes`
   - lanes with open/in-progress/blocked/handoff-ready state;
   - owner and next step.

3. `takeover_ready`
   - handoff-ready items;
   - task refs;
   - source refs;
   - constraints for safe continuation.

4. `human_attention_queue`
   - blockers needing human decision;
   - pending approvals;
   - questions/options.

5. `project_board_summary`
   - compact project state for a PM/dashboard view;
   - status item counts;
   - active handoffs;
   - recent feedback/tool friction.

6. `agent_feedback_digest`
   - repeated tool/search/context issues;
   - top failing clients;
   - suggested A2 follow-up.

## What Belongs In AICOS vs Dashboard

AICOS owns:

- semantic state;
- continuity and handoff;
- source refs;
- actor identity;
- feedback/retrieval signals;
- authority boundaries.

Dashboard owns:

- visual layout;
- board columns;
- comments;
- notifications;
- human-friendly labels;
- filtering/sorting preferences.

## Scalability / Bloat Guardrail

Do not build a custom PM tool inside AICOS.

Build only enough AICOS read/write semantics that a Plane/ClickUp-like tool can
display and coordinate human+AI work without losing AICOS authority.

Near-term implementation should be read-surface contracts, not UI.

## Immediate Implication

Before dashboard work, improve:

- status item quality;
- handoff/takeover semantics;
- search reliability for "what should I do next?";
- actor identity consistency;
- feedback loop visibility.
