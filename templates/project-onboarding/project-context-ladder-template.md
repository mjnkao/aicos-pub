# Project Context Ladder Template

Status: shared reusable template

Use this template to create:

```text
brain/projects/<project-id>/working/context-ladder.md
```

## Purpose

Give A1, A2, humans, and reviewers a light project-specific reading ladder.
Each entry should include:

- when to read
- path or group of paths
- what the reader learns
- what not to read by default

Do not duplicate volatile file contents. Summarize the stable purpose of each
file or group so future edits do not require many synchronized summaries.

## Layer 0 — Project Identity

Read:

- `brain/projects/<project-id>/canonical/project-profile.md`

What you learn:

- project identity
- authority boundaries
- current scope model

## Layer 1 — Current Working Reality

Read:

- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`

What you learn:

- current active reality
- current direction
- what is intentionally not active

## Layer 2 — Continuation

Read only when continuing or checking newest/current:

- `brain/projects/<project-id>/working/handoff/current.md`

What you learn:

- current handoff index
- recent meaningful changes
- which provenance files to open only on demand

## Layer 3 — Project Tasks

Read:

- `agent-repo/classes/a1-work-agents/task-packets/<project-id>/README.md`

What you learn:

- available project task packets
- which one to load after task selection

## Layer 4 — A1 MCP Context/Control Plane

Read when the project will be served to A1 workers through local MCP:

- `integrations/local-mcp-bridge/README.md`
- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`

What you learn:

- how A1 should retrieve startup bundle, handoff/current, packet index, and one
  selected task packet
- how A1 should write checkpoint, task update, and handoff update through
  semantic MCP write tools
- what remains direct project artifact access rather than AICOS
  context/control-plane access

## Layer 5 — Evidence And Source Inputs

Read only when the task points to it:

- `brain/projects/<project-id>/evidence/`
- project-specific source/import/workstream folders

What you learn:

- raw inputs, reference material, provenance, or import evidence

## Layer 6 — Deep Source Or External Runtime

Read only when the task requires direct source work:

- external repo/worktree/artifact paths
- code/runtime/design/content/research source surfaces

What you learn:

- artifact details required for the selected task

## Not Read By Default

- archives/history
- stale handoff trails
- generated output bulk
- all evidence folders
- all task packets
- long source docs not referenced by the selected task
