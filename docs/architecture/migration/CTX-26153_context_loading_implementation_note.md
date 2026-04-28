# CTX-26153 Context Loading Implementation Note

Date: 2026-04-18
Status: implemented-small-step

## Files Updated

- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/implementation-status.md`
- `brain/projects/aicos/canonical/project-working-rules.md`
- `brain/projects/aicos/evidence/policy-sources/policy-source-index.md`

## Startup Card

Placed here:

```text
agent-repo/classes/a2-service-agents/startup-cards/a2-core.md
```

Purpose: give A2-Core a small hot-context card that states actor, lane, current
mode, what it does, what it does not do, and what to read first.

## Rule Cards

Placed here:

```text
agent-repo/classes/a2-service-agents/rule-cards/
```

Cards:

- `writeback.md`
- `idea-capture.md`
- `option-choose.md`
- `sync-brain.md`

These are short warm-context cards loaded only when task triggers need them.

## Task Packet Template

Placed here:

```text
packages/aicos-kernel/contracts/task-packet-template.md
```

It includes:

- actor
- scope
- task_type
- required_context
- rules_to_load
- allowed_write_lanes
- success_condition

No resolver API was added.

## Context Boundary Added

`brain/projects/aicos/canonical/project-working-rules.md` now states that AICOS
serves context, rules, state summaries, task packets, and lookup paths, but does
not own or control the internal memory/context behavior of Codex, Claude Code,
OpenClaw, ChatGPT, Claude chat, or other external co-workers.

## Unresolved Questions

- When should AICOS add thin helpers like `aicos context start`?
- Should task packets become JSON Schema after a few real examples?
- Where should A1 and A2-Serve startup cards live when those lanes become active?
