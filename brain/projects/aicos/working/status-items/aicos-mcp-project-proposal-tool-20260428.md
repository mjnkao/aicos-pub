# Status Item: aicos-mcp-project-proposal-tool-20260428

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-project-proposal-tool-20260428`
Title: Add MCP tool for missing-project proposals
Last write id: `20260428T152055Z-2d5f1f7c03`
Last updated at: `2026-04-28T15:20:55+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-project-proposal-tool`
Agent display name: `Codex Desktop`
Work type: `code`
Work lane: `mcp-project-intake`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
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

Added aicos_propose_project as a bounded semantic write tool for agents to propose a new projects/<id> scope when it does not exist yet. The tool writes intake proposals to brain/workspaces/main/working/project-proposals and does not create project brain state or canonical truth.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Agents previously had to route missing-project intent through feedback or handoff, which mixed project-intake with continuity and learning signals.

## Next Step

Use this tool for missing-project intake; review proposals manually before creating project brains or changing token scope policy.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
