# AICOS Restructure Build Review Pack

Date: 2026-04-18
Status: review pack for ChatGPT / human architecture review

## Purpose

This document summarizes what was changed in the AICOS repository during the
restructuring pass and describes the current system architecture after building
the new MVP structure from the design documents in:

```text
docs/New design/
```

The goal is to make the current state reviewable without requiring ChatGPT or a
human reviewer to read the entire repository.

## Design Sources Used

The current build follows these design documents:

- `docs/New design/ARC-26071_AICOS_Kernel_ServiceSkills_GBrain_GStack_Architecture.md`
- `docs/New design/PLN-26072_Codex_Implementation_Plan_Checklist_For_AICOS_Current_Repo.md`
- `docs/New design/DSC-26040_AICOS_AI_Native_CoWorker_Architecture_Detail_Spec.md`
- `docs/New design/MAP-26031_AICOS_Brain_vs_AgentRepo_vs_Backend_ReadWrite_Boundary.md`
- `docs/New design/DSC-26038_AICOS_Company_Team_Native_Architecture_Leveraging_GBrain.md`
- `docs/New design/AGT-26016_AICOS_Agent_Classes_Knowledge_Boundaries_and_Rules_Matrix.md`

## High-Level Product Interpretation

AICOS is being rebuilt as a company/workspace intelligence layer, not as a
personal brain.

The target system supports:

- many humans;
- many AI agents;
- many projects;
- branch and experiment reality;
- shared project truth;
- controlled agent autonomy;
- blocked-to-options workflows;
- reviewable promotion from evidence to working reality and from working
  reality to canonical truth.

## Major Change: Old Data Moved To Backup

To avoid mixing the old architecture with the new one, legacy data and old
runtime/context material were moved out of the active root into:

```text
backup/pre-restructure-20260418/
```

The old main-branch state is also preserved in Git at:

```text
backup/pre-restructure-main
```

This was a move, not a deletion.

The active root should no longer use old folders as default context. If old data
is needed later, agents should inspect the backup selectively, cite the backup
source path, and copy only reviewed material into the new structure.

### Backup Contents

The backup contains:

- `root/`: old root-level context files, runtime/cache folders, old knowledge
  lanes, imports, reports, gateway, bridges, artifacts, data, and temp files.
- `docs/`: old documentation outside the new design and migration docs.
- `scripts/`: old scripts except the active MVP wrappers.
- `previous-backup/`: previous contents that had already existed under
  `backup/`.

### Active Root After Cleanup

The active root now contains:

```text
AGENTS.md
README.md
agent-repo/
aicos
backend/
backup/
brain/
docs/
integrations/
packages/
scripts/
serving/
tools/gbrain/
```

`tools/gbrain/` remains outside backup because it is the GBrain substrate needed
for the MVP. It is not treated as old truth data.

## Agent Rules Changed

`AGENTS.md` was rewritten for restructuring mode.

The previous mandatory startup rule that forced agents to load old canonical
scope context was suspended. Current rule:

- no mandatory startup context loading;
- follow the current user request first;
- read only files needed for the task;
- treat old backup material as reference only;
- do not read `backup/pre-restructure-20260418/` by default;
- when old material is reused, copy or summarize only the reviewed piece into
  the new structure and cite the backup path.

This change was necessary because the repository is being restructured and the
old context model could otherwise override the new architecture.

## Current Architecture

The current system is split into these active top-level lanes:

```text
brain/
agent-repo/
packages/aicos-kernel/
serving/
backend/
integrations/
docs/
scripts/
tools/gbrain/
backup/
```

Each lane has a distinct role.

## `brain/`: Durable Knowledge And Work Reality

`brain/` is the new durable knowledge and project reality lane.

It is organized by:

```text
brain/
  companies/
  workspaces/
  projects/
  shared/
  service-knowledge/
```

Important rule:

`brain/` is the only active root lane intended to hold durable work reality.
It is separate from agent operational state and backend/index state.

### State Separation In `brain/`

Important scopes use these state lanes:

```text
canonical/
working/
evidence/
```

Projects also support:

```text
branches/
```

Meaning:

- `canonical/`: approved or intended canonical truth.
- `working/`: current working reality and best current understanding.
- `evidence/`: raw or candidate input waiting for review.
- `branches/`: experiment or option-specific project reality.

### Seeded Project Scope

The first seeded project is:

```text
brain/projects/aicos/
```

It contains:

```text
canonical/
working/
evidence/
branches/
```

Key files:

- `brain/projects/aicos/canonical/project-profile.md`
- `brain/projects/aicos/canonical/requirements.md`
- `brain/projects/aicos/canonical/architecture.md`
- `brain/projects/aicos/canonical/decisions.md`
- `brain/projects/aicos/canonical/source-manifest.md`
- `brain/projects/aicos/canonical/project-working-rules.md`
- `brain/projects/aicos/working/current-state.md`
- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/handoff-summary.md`

## `agent-repo/`: Actor Operations And Runtime Lanes

`agent-repo/` is the operational layer for humans and agents.

It is not project truth.

Current structure:

```text
agent-repo/
  shared/
  classes/
    a1-work-agents/
    a2-service-agents/
    humans/
    a3-template/
  instances/
```

### A1 Work Agents

A1 agents do project or business work.

Current A1 lanes include:

```text
agent-repo/classes/a1-work-agents/
  rules/
  tasks/
  queues/
  session-logs/
  heartbeat/
  mcp/
  runtime/
  memory/
  capsules/
```

A1 writes blockers, tasks, queues, session state, and operational notes here.
Durable project reality should go to `brain/`, not `agent-repo/`.

### A2 Service Agents

A2 agents improve AICOS itself.

Current A2 lanes include:

```text
agent-repo/classes/a2-service-agents/
  rules/
  tasks/
  queues/
  session-logs/
  heartbeat/
  mcp/
  runtime/
  memory/
  skills/
  evaluations/
  capsules/
```

A2 service skills were created as markdown contracts, including:

- `resolve-scope`
- `build-project-capsule`
- `build-branch-capsule`
- `generate-mvp-options`
- `compare-branches`
- `recommend-promotion`
- `improve-query-patterns`

This keeps evolving policy in service skills instead of hardcoding it into the
kernel too early.

### Humans

Humans are first-class actors.

Current human lanes include:

```text
agent-repo/classes/humans/
  role-policies/
  review-queues/
  approvals/
  dashboards/
  capsules/
```

Roles seeded:

- manager;
- reviewer;
- approver.

## `packages/aicos-kernel/`: Deterministic Kernel

`packages/aicos-kernel/` is the deterministic structural code layer.

It owns:

- schemas;
- contracts;
- validators;
- packet renderers;
- promotion primitives;
- write lane helpers;
- GBrain adapter notes;
- local CLI behavior.

It does not own evolving service reasoning.

Current structure:

```text
packages/aicos-kernel/
  contracts/
  schemas/
  validators/
  packet-renderers/
  promotion-primitives/
  write-lanes/
  gbrain-adapter/
  aicos_kernel/
```

### Current Schemas

Schemas created:

- `capsule.schema.json`
- `option-packet.schema.json`
- `promotion-packet.schema.json`
- `branch-state.schema.json`
- `project-reality.schema.json`
- `service-feedback.schema.json`

### Current Contracts

Contracts created:

- `actor-classes.md`
- `read-write-lanes.md`
- `promotion-flow.md`
- `branching-contract.md`

### Local CLI

The active root CLI is:

```text
./aicos
```

There is also a wrapper:

```text
scripts/aicos
```

Current command surface:

```text
aicos capsule build company <id>
aicos capsule build workspace <id>
aicos capsule build project <id>
aicos capsule build branch <project-id> <branch-id>
aicos capsule build actor <actor-class> <scope>
aicos branch compare <project-id> <branch-a> <branch-b>
aicos option generate <project-id> <task-or-blocker-id>
aicos promote evidence-to-working <path>
aicos promote working-to-canonical <path>
aicos validate capsule <path>
aicos validate branch <path>
aicos sync brain
```

These are intentionally thin wrappers. They are not meant to encode full
service policy yet.

## `serving/`: Generated Review And Retrieval Surfaces

`serving/` is where generated packets and helper outputs live.

Current structure:

```text
serving/
  query/
  capsules/
  promotion/
  branching/
  truth/
  feedback/
```

This lane contains generated capsules, branch comparison packets, option
packets, promotion review packets, and feedback.

Important rule:

`serving/` helps humans and agents inspect work. It is not the final authority
layer.

## `backend/`: Serving Substrate Only

`backend/` exists for engine, index, sync, embedding, health, and migration
support.

Current structure:

```text
backend/
  engine/pglite/
  indexes/
  sync/
  embeddings/
  health/
  migrations/
```

Important rule:

`backend/` is not truth. It is serving substrate only.

The MVP is local-first and keeps PGLite first through the existing GBrain tool.

## `tools/gbrain/`: GBrain Substrate

`tools/gbrain/` remains active because the design says AICOS should use GBrain
as the substrate for:

- repo-as-truth conventions;
- retrieval;
- indexing;
- sync;
- MCP/CLI access;
- backend abstraction.

The current AICOS build does not reimplement a brain engine.

## `integrations/`: Runtime Integration Lanes

`integrations/` contains future and manual integration lanes:

```text
integrations/
  codex/
  claude-code/
  openclaw/
  chatgpt-sync/
  claude-chat-sync/
```

ChatGPT and Claude chat remain manual sync actors for now.

No dedicated Manager UI, Project UI, or public API was added.

## MVP Flow Proven

One local blocked-to-options-to-manager-choice flow was created.

### 1. Blocker

Blocker file:

```text
agent-repo/classes/a1-work-agents/tasks/blocked/blocker-001.md
```

Problem:

The migration could drift into a broad rewrite if all old structures were moved
or integrated immediately.

### 2. Project Capsule

Generated with:

```bash
./aicos capsule build project aicos
```

Output:

```text
serving/capsules/project/aicos.md
serving/capsules/project/aicos.json
```

### 3. Option Packet

Generated with:

```bash
./aicos option generate aicos blocker-001
```

Output:

```text
serving/branching/option-packets/aicos__blocker-001.md
serving/branching/option-packets/aicos__blocker-001.json
```

The packet generated two options:

- `option-a`: minimal reversible branch scaffold;
- `option-b`: broader integration pass.

The recommended option was `option-a`.

### 4. Branch Reality

Branches created:

```text
brain/projects/aicos/branches/blocker-001-option-a/
brain/projects/aicos/branches/blocker-001-option-b/
```

Branch capsules were generated for these branches.

### 5. Manager Choice

Manager decision packet:

```text
agent-repo/classes/humans/approvals/manager-choice-blocker-001.md
```

Selected option:

```text
option-a
```

Selected branch:

```text
brain/projects/aicos/branches/blocker-001-option-a/
```

### 6. Working State Updated

Project working state updated:

```text
brain/projects/aicos/working/current-state.md
```

The working state now records the selected option, selected branch, option
packet, and manager decision packet.

### 7. Promotion Review Packet

Created with:

```bash
./aicos promote evidence-to-working agent-repo/classes/a1-work-agents/tasks/blocked/blocker-001.md
```

Output:

```text
serving/promotion/review-packets/evidence-to-working/blocker-001.md
serving/promotion/review-packets/evidence-to-working/blocker-001.md.review.md
```

This proves review packet creation without silently promoting truth.

## Commands Verified

These commands were run successfully:

```bash
./aicos --help
./aicos capsule build project aicos
./aicos capsule build company main-company
./aicos capsule build workspace main
./aicos capsule build actor a1-work-agents project/aicos
./aicos option generate aicos blocker-001
./aicos capsule build branch aicos blocker-001-option-a
./aicos capsule build branch aicos blocker-001-option-b
./aicos branch compare aicos blocker-001-option-a blocker-001-option-b
./aicos validate capsule serving/capsules/project/aicos.json
./aicos validate branch brain/projects/aicos/branches/blocker-001-option-a
./aicos promote evidence-to-working agent-repo/classes/a1-work-agents/tasks/blocked/blocker-001.md
./aicos sync brain
python3 -m py_compile packages/aicos-kernel/aicos_kernel/*.py
```

`aicos sync brain` currently performs a safe preflight only. It confirms the
GBrain wrapper exists and does not force `init` or `import`.

This is deliberate: activating or initializing the runtime engine should be an
explicit decision, not a side effect of scaffolding.

## Important Architectural Guardrails Preserved

The current build preserves these boundaries:

- `brain/` is durable work and service knowledge.
- `agent-repo/` is operational actor state and rules.
- `backend/` is serving substrate, not truth.
- `serving/` is generated helper and review output, not final authority.
- `packages/aicos-kernel/` is deterministic structural code.
- A2 service intelligence remains in markdown skills and service knowledge.
- GBrain remains the substrate; AICOS does not reimplement a brain engine.
- GStack is not introduced as the core control plane.
- No UI or public API was added.
- Old data remains available in backup but is not read by default.

## Known Limitations

This is still an MVP scaffold, not a complete product.

Known limitations:

- JSON Schema files exist, but validation is currently a lightweight stdlib
  check rather than full JSON Schema validation.
- `aicos sync brain` is a preflight and does not import/index yet.
- `aicos option generate` uses a minimal deterministic option template. The
  richer option policy should evolve in A2 service skills.
- Manager choice is currently a markdown approval packet, not yet a first-class
  CLI command.
- Old data has not been migrated into the new structure except for minimal MVP
  seed material.
- No MCP stdio server has been created yet for AICOS-specific commands.

## Recommended Review Questions

Please review:

1. Does the new root structure correctly reflect the architecture in
   `docs/New design/`?
2. Is the backup isolation strict enough to prevent old-context confusion?
3. Are the boundaries between `brain/`, `agent-repo/`, `backend/`, and
   `serving/` clear enough?
4. Is the current `packages/aicos-kernel/` appropriately deterministic, or does
   it still encode too much service policy?
5. Should `aicos option choose` become the next CLI command to formalize manager
   selection?
6. Should full JSON Schema validation be added now, or after packet shapes
   stabilize?
7. When should `aicos sync brain` begin calling GBrain import/index commands
   instead of remaining a preflight?

## Suggested Next Implementation Steps

Recommended next steps:

1. Add `aicos option choose <project-id> <blocker-id> <option-id>` to formalize
   manager selection and working-state update.
2. Add full JSON Schema validation if packet shapes are accepted.
3. Add a GBrain import/index path that targets `brain/` only and excludes
   `agent-repo/`.
4. Define the AICOS MCP stdio wrapper after CLI behavior stabilizes.
5. Selectively migrate old material from
   `backup/pre-restructure-20260418/` only when needed.

## Final State Summary

The repository now has a clean active root for the new AICOS architecture.

Old data has been isolated into one backup folder.

The new architecture is visible and testable through:

- root docs;
- `brain/`;
- `agent-repo/`;
- `packages/aicos-kernel/`;
- generated `serving/` packets;
- local `./aicos` commands;
- one complete blocked-to-options-to-manager-choice MVP flow.
