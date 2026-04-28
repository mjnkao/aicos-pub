# PLN-26072 — Codex Implementation Plan & Checklist For The Current `aicos` Repo

**Status:** draft-v1  
**Project:** AICOS  
**Date:** 2026-04-17  
**Purpose:** kế hoạch và checklist chi tiết để Codex triển khai kiến trúc mới của AICOS trên repo `aicos` hiện tại, theo hướng local-first MVP, dùng GBrain + PGLite, chưa cần Manager UI / Project UI / API riêng.

---

## 1. Executive Summary

Plan này được viết để Codex có thể triển khai cụ thể trên repo `aicos` hiện tại mà không phá vỡ toàn bộ cấu trúc cũ ngay lập tức.

### Key implementation constraints

- local MVP only
- use GBrain
- use PGLite first
- no dedicated Manager UI yet
- no dedicated Project/task UI yet
- no public API required in MVP
- use MCP stdio and CLI for local co-worker integration
- support:
  - Codex
  - Claude Code
  - OpenClaw
- ChatGPT and Claude chat remain manager-facing layers with manual sync for now

### Implementation philosophy

- keep current repo usable
- add new architecture incrementally
- avoid breaking all existing paths at once
- build kernel first
- treat service logic as skills/policies, not hardcoded too early
- prepare for A2-R and A2-C split even if A2-C is not fully activated on day 1

---

## 2. Immediate Objectives

Codex should make the current repo capable of:

1. holding the new folder structure
2. representing canonical / working / evidence / branch states
3. representing A1 / A2 / human agent classes cleanly
4. generating capsules via local commands
5. generating blocked -> option packets
6. storing service-knowledge
7. using GBrain locally with PGLite
8. preserving current repo materials as migration reference where needed

---

## 3. Current Repo Baseline

The current repo already contains active or semi-active lanes such as:

- `canonical/`
- `brains/`
- `gateway/`
- `bridges/`
- `reports/`
- `backup/`
- `scripts/`

Codex must assume that some of these are useful migration sources.

### Rule

Do not delete old structures first.  
Create the new structure, map old structure into it, and preserve migration notes.

---

## 4. Phase Plan

Implementation should be done in phases.

## Phase 1 — Create New Target Structure Without Breaking Current Structure
## Phase 2 — Add AICOS Kernel
## Phase 3 — Add Brain Reality Structure
## Phase 4 — Add AgentRepo Class Structure
## Phase 5 — Add Capsule / Branch / Promotion Commands
## Phase 6 — Wire GBrain With PGLite
## Phase 7 — Wire local runtime integrations
## Phase 8 — Validate MVP workflows
## Phase 9 — Write migration notes and stop for review

---

## 5. Phase 1 — Create New Target Structure

Codex should create the following top-level folders if missing.

### Checklist Code: PLN-26073

- [ ] create `packages/`
- [ ] create `brain/`
- [ ] create `agent-repo/`
- [ ] create `serving/`
- [ ] create `backend/`
- [ ] create `integrations/`
- [ ] keep existing `scripts/`
- [ ] keep existing `docs/`
- [ ] keep existing `archive/` or reuse `backup/`
- [ ] do **not** delete `canonical/`, `brains/`, `gateway/`, `bridges/`, `reports/` yet

### Required target shape

```text
AICOS/
├── packages/
├── brain/
├── agent-repo/
├── serving/
├── backend/
├── integrations/
├── scripts/
├── docs/
└── archive/ or backup/
```

### Deliverable

- folder scaffold committed
- no destructive moves yet

---

## 6. Phase 2 — Add AICOS Kernel

Codex should create a minimal deterministic kernel.

### Required package

```text
packages/aicos-kernel/
  contracts/
  schemas/
  validators/
  packet-renderers/
  promotion-primitives/
  write-lanes/
  gbrain-adapter/
```

### Checklist Code: PLN-26074

- [ ] create `packages/aicos-kernel/contracts/`
- [ ] create `packages/aicos-kernel/schemas/`
- [ ] create `packages/aicos-kernel/validators/`
- [ ] create `packages/aicos-kernel/packet-renderers/`
- [ ] create `packages/aicos-kernel/promotion-primitives/`
- [ ] create `packages/aicos-kernel/write-lanes/`
- [ ] create `packages/aicos-kernel/gbrain-adapter/`

### Minimal schema files to create

- [ ] `capsule.schema.json`
- [ ] `option-packet.schema.json`
- [ ] `promotion-packet.schema.json`
- [ ] `branch-state.schema.json`
- [ ] `project-reality.schema.json`
- [ ] `service-feedback.schema.json`

### Minimal contract files to create

- [ ] `actor-classes.md`
- [ ] `read-write-lanes.md`
- [ ] `promotion-flow.md`
- [ ] `branching-contract.md`

### Minimal renderers to create

- [ ] capsule markdown renderer
- [ ] capsule json renderer
- [ ] option packet markdown renderer
- [ ] promotion packet markdown renderer

### Minimal validators to create

- [ ] capsule validator
- [ ] option packet validator
- [ ] promotion packet validator
- [ ] branch state validator

---

## 7. Phase 3 — Add Brain Reality Structure

Codex should create the new `brain/` structure.

### Required target shape

```text
brain/
  companies/
  workspaces/
  projects/
  shared/
  service-knowledge/
```

### Checklist Code: PLN-26075

- [ ] create `brain/companies/`
- [ ] create `brain/workspaces/`
- [ ] create `brain/projects/`
- [ ] create `brain/shared/`
- [ ] create `brain/service-knowledge/`

### For company scope

- [ ] create `<company-id>/canonical/`
- [ ] create `<company-id>/working/`
- [ ] create `<company-id>/evidence/`

### For workspace scope

- [ ] create `<workspace-id>/canonical/`
- [ ] create `<workspace-id>/working/`
- [ ] create `<workspace-id>/evidence/`

### For project scope

- [ ] create `<project-id>/canonical/`
- [ ] create `<project-id>/working/`
- [ ] create `<project-id>/evidence/`
- [ ] create `<project-id>/branches/`

### For service knowledge

- [ ] create `service-knowledge/canonical/`
- [ ] create `service-knowledge/working/`
- [ ] create `service-knowledge/evidence/`

### Seed files to create for first project

For one test project (e.g. `aicos`):

- [ ] `brain/projects/aicos/canonical/project-profile.md`
- [ ] `brain/projects/aicos/canonical/requirements.md`
- [ ] `brain/projects/aicos/canonical/architecture.md`
- [ ] `brain/projects/aicos/canonical/decisions.md`
- [ ] `brain/projects/aicos/canonical/source-manifest.md`
- [ ] `brain/projects/aicos/canonical/project-working-rules.md`
- [ ] `brain/projects/aicos/working/current-state.md`
- [ ] `brain/projects/aicos/working/current-direction.md`
- [ ] `brain/projects/aicos/working/active-risks.md`
- [ ] `brain/projects/aicos/working/open-questions.md`
- [ ] `brain/projects/aicos/working/handoff-summary.md`
- [ ] `brain/projects/aicos/evidence/README.md`
- [ ] `brain/projects/aicos/branches/README.md`

---

## 8. Phase 4 — Add AgentRepo Class Structure

Codex should create class-based operational structure.

### Required target shape

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

### Checklist Code: PLN-26076

- [ ] create `agent-repo/shared/`
- [ ] create `agent-repo/classes/a1-work-agents/`
- [ ] create `agent-repo/classes/a2-service-agents/`
- [ ] create `agent-repo/classes/humans/`
- [ ] create `agent-repo/classes/a3-template/`
- [ ] create `agent-repo/instances/`

### Shared policies

- [ ] `agent-repo/shared/shared-access-rules/source-of-truth-access.md`
- [ ] `agent-repo/shared/shared-access-rules/write-lane-policy.md`
- [ ] `agent-repo/shared/shared-access-rules/scope-resolution-policy.md`
- [ ] `agent-repo/shared/shared-promotion-rules/evidence-to-working-policy.md`
- [ ] `agent-repo/shared/shared-promotion-rules/working-to-canonical-policy.md`
- [ ] `agent-repo/shared/shared-promotion-rules/review-required-cases.md`
- [ ] `agent-repo/shared/shared-tool-policies/tool-usage-policy.md`
- [ ] `agent-repo/shared/shared-tool-policies/query-policy.md`
- [ ] `agent-repo/shared/shared-tool-policies/safety-boundaries.md`
- [ ] `agent-repo/shared/capsule-policies/capsule-schema.md`
- [ ] `agent-repo/shared/capsule-policies/capsule-freshness-policy.md`
- [ ] `agent-repo/shared/capsule-policies/capsule-priority-policy.md`

### A1 structure

- [ ] create `rules/`
- [ ] create `tasks/current/`
- [ ] create `tasks/backlog/`
- [ ] create `tasks/blocked/`
- [ ] create `tasks/completed/`
- [ ] create `queues/assignment-queue/`
- [ ] create `queues/retry-queue/`
- [ ] create `queues/proposal-queue/`
- [ ] create `queues/branch-option-queue/`
- [ ] create `session-logs/`
- [ ] create `heartbeat/`
- [ ] create `mcp/`
- [ ] create `runtime/`
- [ ] create `memory/`
- [ ] create `capsules/company/`
- [ ] create `capsules/workspace/`
- [ ] create `capsules/project/`
- [ ] create `capsules/branch/`
- [ ] create `capsules/task/`

### A1 seed rule files

- [ ] `startup-rules.md`
- [ ] `autonomy-contract.md`
- [ ] `blocker-response-policy.md`
- [ ] `option-generation-policy.md`
- [ ] `writeback-rules.md`
- [ ] `escalation-rules.md`

### A2 structure

- [ ] create `rules/`
- [ ] create `tasks/current/`
- [ ] create `tasks/backlog/`
- [ ] create `tasks/blocked/`
- [ ] create `tasks/completed/`
- [ ] create `queues/feedback-intake-queue/`
- [ ] create `queues/retrieval-review-queue/`
- [ ] create `queues/source-classification-queue/`
- [ ] create `queues/promotion-candidate-queue/`
- [ ] create `queues/capsule-quality-queue/`
- [ ] create `session-logs/`
- [ ] create `heartbeat/`
- [ ] create `mcp/`
- [ ] create `runtime/`
- [ ] create `memory/`
- [ ] create `skills/`
- [ ] create `evaluations/`
- [ ] create `capsules/service/`
- [ ] create `capsules/company/`
- [ ] create `capsules/workspace/`
- [ ] create `capsules/project/`

### A2 seed rule files

- [ ] `startup-rules.md`
- [ ] `service-boundaries.md`
- [ ] `improvement-policy.md`
- [ ] `no-silent-promotion-policy.md`
- [ ] `service-writeback-rules.md`
- [ ] `escalation-rules.md`

### Human structure

- [ ] create `role-policies/`
- [ ] create `review-queues/`
- [ ] create `approvals/`
- [ ] create `dashboards/`
- [ ] create `capsules/company/`
- [ ] create `capsules/workspace/`
- [ ] create `capsules/project/`
- [ ] create `capsules/branch/`

---

## 9. Phase 5 — Add Service Skills Structure For A2

Codex should add service skill lanes, but keep them content-driven first.

### Checklist Code: PLN-26077

- [ ] create `agent-repo/classes/a2-service-agents/skills/resolve-scope/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/build-project-capsule/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/build-branch-capsule/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/generate-mvp-options/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/compare-branches/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/recommend-promotion/`
- [ ] create `agent-repo/classes/a2-service-agents/skills/improve-query-patterns/`

### Skill contents should emphasize

- role
- input expectations
- output packet shape
- evaluation criteria
- known failure modes
- escalation conditions
- writeback lanes

### Important implementation rule

Do not hardcode these policies deeply into TS logic yet.  
Represent them as service skills / markdown contracts first.

---

## 10. Phase 6 — Add Serving Structure

Codex should create the serving layer folders and initial commands.

### Required target shape

```text
serving/
  query/
  capsules/
  promotion/
  branching/
  truth/
  feedback/
```

### Checklist Code: PLN-26078

- [ ] create `serving/query/project-query/`
- [ ] create `serving/query/workspace-query/`
- [ ] create `serving/query/company-query/`
- [ ] create `serving/query/service-query/`

- [ ] create `serving/capsules/company/`
- [ ] create `serving/capsules/workspace/`
- [ ] create `serving/capsules/project/`
- [ ] create `serving/capsules/branch/`
- [ ] create `serving/capsules/task/`
- [ ] create `serving/capsules/manager/`
- [ ] create `serving/capsules/a1/`
- [ ] create `serving/capsules/a2/`

- [ ] create `serving/promotion/evidence-to-working/`
- [ ] create `serving/promotion/working-to-canonical/`
- [ ] create `serving/promotion/review-packets/`

- [ ] create `serving/branching/branch-create/`
- [ ] create `serving/branching/branch-compare/`
- [ ] create `serving/branching/branch-summary/`
- [ ] create `serving/branching/option-packets/`

- [ ] create `serving/truth/source-resolution/`
- [ ] create `serving/truth/conflict-check/`
- [ ] create `serving/truth/precedence/`
- [ ] create `serving/truth/lineage/`

- [ ] create `serving/feedback/a1-feedback/`
- [ ] create `serving/feedback/a2-feedback/`
- [ ] create `serving/feedback/manager-feedback/`
- [ ] create `serving/feedback/synthesis/`

---

## 11. Phase 7 — Add Backend Structure And GBrain PGLite Path

Codex should keep backend local-first and lightweight.

### Required target shape

```text
backend/
  engine/
  indexes/
  sync/
  embeddings/
  health/
  migrations/
```

### Checklist Code: PLN-26079

- [ ] create `backend/engine/pglite/`
- [ ] optionally create `backend/engine/postgres/` as future placeholder
- [ ] create `backend/indexes/keyword/`
- [ ] create `backend/indexes/vector/`
- [ ] create `backend/indexes/graph/`
- [ ] create `backend/indexes/hybrid/`
- [ ] create `backend/sync/brain-sync/`
- [ ] create `backend/sync/service-knowledge-sync/`
- [ ] create `backend/sync/branch-sync/`
- [ ] create `backend/embeddings/models/`
- [ ] create `backend/embeddings/jobs/`
- [ ] create `backend/embeddings/quality-checks/`
- [ ] create `backend/health/engine-health/`
- [ ] create `backend/health/sync-health/`
- [ ] create `backend/health/index-health/`
- [ ] create `backend/health/retrieval-health/`
- [ ] create `backend/migrations/`

### GBrain integration tasks

- [ ] keep or adapt current local gbrain wrapper scripts
- [ ] verify PGLite-based local brain still works
- [ ] create or adapt an AICOS-specific sync command
- [ ] ensure `brain/` becomes the primary sync target
- [ ] avoid indexing `agent-repo/` as work truth

---

## 12. Phase 8 — Add Local CLI Commands

Codex should implement a small CLI surface for AICOS.

### Required commands

### Checklist Code: PLN-26080

- [ ] `aicos capsule build company <id>`
- [ ] `aicos capsule build workspace <id>`
- [ ] `aicos capsule build project <id>`
- [ ] `aicos capsule build branch <project-id> <branch-id>`
- [ ] `aicos capsule build actor <actor-class> <scope>`
- [ ] `aicos branch compare <project-id> <branch-a> <branch-b>`
- [ ] `aicos option generate <project-id> <task-or-blocker-id>`
- [ ] `aicos promote evidence-to-working <path>`
- [ ] `aicos promote working-to-canonical <path>`
- [ ] `aicos validate capsule <path>`
- [ ] `aicos validate branch <path>`
- [ ] `aicos sync brain`

### Implementation note

These commands should use:

- kernel contracts
- renderers
- validators
- GBrain adapter
- skill content from A2 when appropriate

---

## 13. Phase 9 — Add Runtime Integrations

Codex should create a stable local integration structure.

### Required target shape

```text
integrations/
  codex/
  claude-code/
  openclaw/
  chatgpt-sync/
  claude-chat-sync/
```

### Checklist Code: PLN-26081

- [ ] create `integrations/codex/README.md`
- [ ] create `integrations/codex/mcp/`
- [ ] create `integrations/codex/startup/`
- [ ] create `integrations/codex/sync/`

- [ ] create `integrations/claude-code/README.md`
- [ ] create `integrations/claude-code/mcp/`
- [ ] create `integrations/claude-code/startup/`
- [ ] create `integrations/claude-code/sync/`

- [ ] create `integrations/openclaw/README.md`
- [ ] create `integrations/openclaw/mcp/`
- [ ] create `integrations/openclaw/startup/`
- [ ] create `integrations/openclaw/sync/`

- [ ] create `integrations/chatgpt-sync/README.md`
- [ ] create `integrations/chatgpt-sync/manual-sync.md`

- [ ] create `integrations/claude-chat-sync/README.md`
- [ ] create `integrations/claude-chat-sync/manual-sync.md`

### Rule

ChatGPT and Claude chat remain manual-sync actors for now.

---

## 14. Phase 10 — Add MVP Example Flow

Codex should ensure the repo can demonstrate one full example.

### Example flow

Project: `aicos`  
Task: blocked implementation task  
Branching: generate 2 options  
Manager: chooses 1  
Promotion: update working state

### Checklist Code: PLN-26082

- [ ] create one sample blocker input
- [ ] generate one project capsule
- [ ] generate one branch capsule
- [ ] generate at least 2 option packets
- [ ] generate one manager decision packet
- [ ] record selection result
- [ ] update project working state
- [ ] write one service feedback entry if process quality issue found

### Definition of done for example flow

A human reviewer can inspect:

- the project truth
- the current working state
- the blocker
- the options
- the recommendation
- the selected branch
- the resulting update

without needing to read the whole raw repo.

---

## 15. Migration Of Existing Folders

Codex must not destroy old material first.

### Checklist Code: PLN-26083

- [ ] map `canonical/` into new `brain/` lanes
- [ ] map `brains/` to current GBrain-facing references or intermediate migration notes
- [ ] map `gateway/` to `packages/aicos-kernel/` and/or `serving/`
- [ ] map `bridges/` into `integrations/` and `agent-repo/.../mcp`
- [ ] map `reports/` into:
  - `brain/.../evidence`
  - `agent-repo/.../queues`
  - `serving/feedback`
- [ ] keep `backup/` or rename to `archive/` only if safe and documented

### Required migration notes

- [ ] `docs/migration/PLN-26072_old-to-new-structure-map.md`
- [ ] `docs/migration/PLN-26072_status.md`
- [ ] `docs/migration/PLN-26072_unresolved-items.md`

---

## 16. Explicit Non-Goals For MVP

Codex should not overbuild the following yet.

### Checklist Code: PLN-26084

- [ ] do not add a full public API layer
- [ ] do not add Manager UI yet
- [ ] do not add Project/task UI yet
- [ ] do not migrate to Postgres yet unless explicitly requested
- [ ] do not force direct ChatGPT / Claude chat integration yet
- [ ] do not make GStack mandatory in the MVP
- [ ] do not hardcode too much A2 policy logic into TS too early
- [ ] do not turn backend into canonical truth
- [ ] do not treat `agent-repo/` as work truth

---

## 17. Acceptance Criteria

### Checklist Code: PLN-26085

- [ ] repo has the new target structure
- [ ] old structure is preserved or mapped safely
- [ ] GBrain local path still works with PGLite
- [ ] `brain/` is primary knowledge lane
- [ ] `agent-repo/` cleanly separates A1, A2, humans
- [ ] capsule schemas and renderers exist
- [ ] branch packet and option packet schemas exist
- [ ] local CLI commands exist for capsule / option / promotion / sync
- [ ] one full blocked -> options -> manager selection example works
- [ ] migration notes explain the new structure clearly

---

## 18. Final Instruction To Codex

Implement the new AICOS architecture on the current repo by:

1. preserving old structure first  
2. adding the new structure alongside it  
3. building the kernel before hardcoding intelligence  
4. representing evolving service logic as A2 skills and service knowledge  
5. keeping GBrain as substrate  
6. keeping GStack optional and only for future code-change workflows  
7. proving the architecture with one full local blocked -> options -> manager-choice flow

---
