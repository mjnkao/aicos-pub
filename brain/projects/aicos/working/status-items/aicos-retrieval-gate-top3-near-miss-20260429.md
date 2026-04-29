# Status Item: aicos-retrieval-gate-top3-near-miss-20260429

Status: open
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-gate-top3-near-miss-20260429`
Title: Retrieval eval gate has a small top3 near-miss after adding new ledger vocabulary context
Last write id: `20260429T033435Z-12e0afacb4`
Last updated at: `2026-04-29T03:34:35+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260429-work-ledger-vocabulary`
Agent display name: `unknown`
Work type: `review`
Work lane: `aicos-search-regression-watch`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
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

After adding the Work State Ledger vocabulary spec and syncing text index, retrieval eval still returned top5 59/59 and errors 0, but top3 dropped to 56/59, just below the 0.95 gate. Misses were rank 5 for manager-next-work, rank 4 for sample-operator-test-smoke-commands, and rank 4 for aicos-field-open-search-status-items. This looks like ranking sensitivity from new status/research context, not lost recall.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

AICOS needs to preserve search quality as new planning docs are added. Top5 recall is intact, but top3 ranking is the practical A1 usability target.

## Next Step

Do not tune blindly. In the next search pass, inspect whether status/open-item filtering and resolved/closed handling should be stronger before changing ranking weights.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-work-state-ledger-vocabulary-spec-20260429.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
