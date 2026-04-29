# Status Item: aicos-retrieval-eval-expanded-a1-manager-corpus-20260428

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-eval-expanded-a1-manager-corpus-20260428`
Title: Expanded A1/human-manager retrieval eval corpus and HTTP runner
Last write id: `20260428T153324Z-685e9af510`
Last updated at: `2026-04-28T15:33:24+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-checklist-relation-audit`
Agent display name: `Codex Desktop`
Work type: `planning`
Work lane: `checklist-reconciliation`
Coordination status: `completed`
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
Functional role: `AICOS maintainer`
Runtime identity map:
```json
{
  "identity_private": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "AICOS maintainer",
    "mcp_name": "aicos_http",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

## Summary

The expanded retrieval eval runner/corpus is now baseline infrastructure. Current corpus has 59 items across projects/aicos, projects/sample-project, and mjnclaw smoke; latest gate passes top3 57/59, top5 59/59, errors 0.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

The old next step referenced three early top3 misses. Those were addressed by later direct-read nudges, answer playbook, corpus expansion, and gate tuning.

## Next Step

Keep resolved. Continue running scripts/aicos-retrieval-eval --max-results 5 --gate before search changes.

## Trace Refs

- source_ref: `scripts/aicos-retrieval-eval`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
