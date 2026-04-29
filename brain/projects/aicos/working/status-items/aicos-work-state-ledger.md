# Status Item: AICOS-WORK-STATE-LEDGER

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-WORK-STATE-LEDGER`
Title: Design minimal Work State Ledger without becoming a PM tool
Last write id: `20260429T034430Z-936229090b`
Last updated at: `2026-04-29T03:44:30+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260429-work-state-reconciler`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-work-state-ledger`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``
Runtime: `private-local-aicos`
MCP name: `aicos_http`
Agent position: `internal_agent`
Functional role: `CTO/fullstack dev of AICOS`
Runtime identity map:
```json
{
  "identity_private": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "CTO/fullstack dev of AICOS",
    "mcp_name": "aicos_http",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

## Summary

Implemented the first report-only Work State Ledger reconciliation slice. New CLI command `./aicos work-state reconcile --scope projects/<project-id>` reads existing status-items, maps legacy item type/status into the proposed work_item kind/status vocabulary, extracts Trace Ref relations, checks checkbox/status drift, duplicate-looking titles, and kind/status ambiguity, and emits text or JSON without mutating truth. Added work-state feedback labels so A1/A2 can report missing, ambiguous, stale, conflicting, or ownership-unclear work state directly through `aicos_record_feedback`.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

This validates the vocabulary on real AICOS/sample project data before adding a durable ledger database or new work-item write tools, while creating a lightweight learning loop for work-state friction.

## Next Step

Review reconciliation warnings and tune heuristics only where warnings are actionable. If the report remains useful across AICOS and sample project, define the minimal Work State Ledger contract and only then add write/read MCP tools for work_item.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-work-state-ledger-vocabulary-spec-20260429.md`
  - `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
  - `docs/install/AICOS_MCP_WRITE_COOKBOOK.md`
- source_ref: `packages/aicos-kernel/aicos_kernel/kernel.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
