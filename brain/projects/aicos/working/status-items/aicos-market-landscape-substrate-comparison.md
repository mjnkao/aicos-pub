# Status Item: AICOS-MARKET-LANDSCAPE-SUBSTRATE-COMPARISON

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-MARKET-LANDSCAPE-SUBSTRATE-COMPARISON`
Title: Use market landscape comparison to guide future build-vs-buy decisions
Last write id: `20260428T032854Z-7674144a6c`
Last updated at: `2026-04-28T03:28:54+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-2026-04-28-market-landscape`
Agent display name: `unknown`
Work type: `research`
Work lane: `aicos-product-architecture`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

AICOS now has a comparative note covering GBrain, Memobase, Membase, GitAgent, LangGraph/LangMem, CrewAI, Mem0, and Atlan. The working judgment is that the market clearly validates agent memory, context, governance, and stateful runtime needs, but AICOS still has a real wedge in project control-plane semantics. Future decisions should build AICOS-owned semantics while reusing substrate layers more aggressively.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Preserve the broader market/context analysis so architecture passes do not drift into rebuilding every substrate layer by default.

## Next Step

Use the comparison note together with the product framing and substrate decision memos when producing the keep/migrate/retire inventory for AICOS modules.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-market-landscape-and-substrate-comparison-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
