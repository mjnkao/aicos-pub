# CHK-26216 Real Project Readiness Implementation Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Phase A — Core Discipline Hardening

### What Was Added

- Shared checkpoint/writeback policy:
  `brain/shared/policies/checkpoint-writeback-policy.md`
- Shared task-state template:
  `brain/shared/templates/task-state-template.md`
- `./aicos context start` now supports:
  - `A2-Core-C projects/aicos`
  - `A1 projects/<project-id>`

### Shared Reusable Foundation

Checkpoint triggers, writeback lanes, task-state fields, and context-start
orientation behavior are project-neutral.

### First Concrete Example

`projects/sample-project` can now be started by A1 once its bootstrap files
exist.

### Left For Later Automation

- scaffold generation helper
- missing bootstrap file generator
- richer packet selection metadata

## Phase B — Minimum Viable A1 Branch

### What Was Added

- A1 startup card:
  `agent-repo/classes/a1-work-agents/startup-cards/a1.md`
- A1 rule cards:
  `agent-repo/classes/a1-work-agents/rule-cards/`
- A1 task-state convention:
  `agent-repo/classes/a1-work-agents/tasks/README.md`
- A1 task packet index:
  `agent-repo/classes/a1-work-agents/task-packets/README.md`

### Shared Reusable Foundation

A1 rules are written for `projects/<project-id>`, not Crypto Trading.

### First Concrete Example

Crypto Trading is the first target project for A1 readiness testing, but no
Crypto-specific behavior is baked into A1 rules.

### Left For Later Automation

- A1 task packet generator
- A1 project-specific rule overlay if real usage proves it is needed

## Phase C — Real Project Onboarding Standard

### What Was Added

Reusable onboarding kit:

```text
brain/shared/templates/project-onboarding/
```

Crypto Trading bootstrap placeholder:

```text
brain/projects/sample-project/
```

### Shared Reusable Foundation

The onboarding checklist, lane mapping, bootstrap-state template, and source
inventory pattern are reusable for the next project with minimal edits.

### First Concrete Example

Crypto Trading has identity/bootstrap files marked clearly as not-yet-imported
truth. The first slice remains TBD.

### Left For Later Automation

- project bootstrap CLI
- import-plan renderer
- checklist completion validator

## Phase D — Real Usage Test Readiness

### What Was Added

Reusable test templates:

- startup/token test
- rule compliance test
- continuity/interruption test
- real task quality test
- evaluation scorecard

### Shared Reusable Foundation

Tests are project-neutral and can be applied to any future real project.

### First Concrete Example

Crypto Trading will use these tests after a bounded slice is selected.

### Left For Later Automation

- automated test run packet generation
- scorecard rendering
- friction capture helper

## Guardrails Preserved

- no transfer/takeover engine
- no full A2-Serve runtime
- no UI/API
- no DB-first ownership system
- no one-off Crypto-only onboarding flow
