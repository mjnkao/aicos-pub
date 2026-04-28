# Agent Onboarding Front Door Refresh

Date: 2026-04-19
Actor: A2-Core-C
Status: implemented

## Purpose

Make the repo clearer for future agents entering AICOS without inherited chat
context. This pass updates the front-door reading paths so a new A1, A2-Core,
or future A2-Serve candidate can understand where to start, where to read
deeper, and when to use MCP instead of raw AICOS file access.

## What Changed

- Root `AGENTS.md` now points new agents to actor-specific context ladders
  before deeper reading.
- A2-Core onboarding now includes an MCP context/control-plane layer for Phase 1
  reads and Phase 2 semantic writes.
- A1 onboarding now states the MCP-first rule for AICOS-facing context/control
  plane reads/writes, while preserving direct artifact/repo access for actual
  project work.
- A1 writeback/handoff rule cards now point to MCP semantic write/read surfaces
  before direct-file fallback.
- AICOS and sample project project context ladders now summarize where MCP contract,
  integration, and operations surfaces fit.
- Root `README.md` now points GitHub/readme-first readers to the same actor
  ladders.
- AICOS current state and handoff now record that agent onboarding/front-door
  surfaces have been refreshed.

## Updated Files

- `AGENTS.md`
- `README.md`
- `agent-repo/classes/a2-service-agents/onboarding/README.md`
- `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
- `agent-repo/classes/a2-service-agents/onboarding/a2-core-new-agent-prompt-template.md`
- `agent-repo/classes/a2-service-agents/onboarding/a2-serve-context-ladder.md`
- `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
- `agent-repo/classes/a1-work-agents/onboarding/README.md`
- `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`
- `agent-repo/classes/a1-work-agents/onboarding/a1-new-agent-prompt-template.md`
- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`
- `agent-repo/classes/a1-work-agents/rule-cards/writeback-checkpoint.md`
- `agent-repo/classes/a1-work-agents/rule-cards/handoff-continuation.md`
- `brain/projects/aicos/working/context-ladder.md`
- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/handoff/current.md`
- `brain/projects/sample-project/working/context-ladder.md`
- `brain/shared/templates/project-onboarding/project-context-ladder-template.md`

## What Was Intentionally Not Built

- No new onboarding engine.
- No new MCP runtime or daemon.
- No company/workspace governance tree.
- No duplicated long summaries of volatile project state.
- No broad rewrite of task packets or project truths.

## Current Reading Model

New agents should:

1. Read root `AGENTS.md`.
2. Open the actor ladder for A1, A2-Core, or future A2-Serve.
3. Open the project context ladder when the project provides one.
4. Use packet index/summary before loading one selected task packet.
5. Use MCP-first access for A1 AICOS-facing context/control-plane operations
   when MCP is available.
6. Read deeper contracts, rules, source code, evidence, or migration notes only
   when the task requires them.

## Remaining Future Work

- Run a clean new-agent startup test with A2-Core Claude/OpenClaw, not only
  Codex.
- Run an A1 startup/writeback test through the local MCP bridge from an isolated
  external checkout.
- Decide later whether A2-Serve needs a detailed ladder once it becomes active.
