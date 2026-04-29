# Status Item: AICOS-LEARNING-LOOP-EFFECTIVENESS-20260429

Status: open
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-LEARNING-LOOP-EFFECTIVENESS-20260429`
Title: Review AICOS learning-loop effectiveness after real A1 usage
Last write id: `20260429T024710Z-08e4186ecb`
Last updated at: `2026-04-29T02:47:10+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260429-major-work-plan-pass`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-learning-loop`
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
Functional role: `CTO/AICOS maintainer`
Runtime identity map:
```json
{
  "identity_current": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "CTO/AICOS maintainer",
    "mcp_name": "aicos_http",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

## Summary

Reviewed current learning loop. Mechanically it works: feedback writes, feedback digest, feedback indexing, and eval coverage exist. Latest digest scanned 15 feedback records, found 4 actionable records, and found 0 new eval candidates. The gap is not mechanics but evidence: most feedback still comes from A2 maintenance, so AICOS has not yet proven real external A1 agents reliably submit useful non-no_issue feedback.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

AICOS search/tool quality should improve from real A1 friction rather than manual one-off fixes, but the feedback loop must show it collects useful signals.

## Next Step

Keep current feedback loop. Add A1 feedback examples in a later docs pass and review non-no_issue rate after more real A1 sessions before adding new nudge boundaries.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-feedback-to-eval-digest-20260428.md`
  - `brain/projects/aicos/evidence/research/aicos-checklist-cto-review-and-execution-plan-20260428.md`
- source_ref: `brain/projects/aicos/evidence/research/aicos-learning-loop-effectiveness-review-20260429.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
