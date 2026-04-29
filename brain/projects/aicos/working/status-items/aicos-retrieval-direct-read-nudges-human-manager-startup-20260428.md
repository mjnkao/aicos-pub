# Status Item: aicos-retrieval-direct-read-nudges-human-manager-startup-20260428

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-retrieval-direct-read-nudges-human-manager-startup-20260428`
Title: Direct-read nudges and human-manager startup retrieval pass
Last write id: `20260428T153325Z-12f4f0721f`
Last updated at: `2026-04-28T15:33:25+00:00`

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

Direct-read nudges and answer playbook are now part of query responses for common manager/A1 intents. They guide agents toward startup bundle, status items, handoff/current, project health, feedback digest, and bounded search instead of relying on broad search alone.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

The old next step was answer synthesis/playbook; that baseline has now landed. Ongoing improvements should be feedback/eval-driven.

## Next Step

Keep resolved. If A1 answers remain poor despite correct refs, add feedback-to-eval cases before adding heavier retrieval infrastructure.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/pg_search/engine.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
