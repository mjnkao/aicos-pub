# Status Item: aicos-public-code-brain-package-boundary

Status: deferred
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-public-code-brain-package-boundary`
Title: Defer public export manifest refactor until public repo matters
Last write id: `codex-defer-public-package-boundary-20260428`
Last updated at: `2026-04-28T11:43:44+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-brain-modularity-tasking-20260428`
Agent display name: `unknown`
Work type: `planning`
Work lane: `brain-modularity`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `main`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `codex-desktop via aicos_local_private`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``
Runtime: `private-local-aicos`
MCP name: `aicos_local_private`
Agent position: `internal_agent`
Functional role: `CTO / AICOS maintainer`
Runtime identity map:
```json
{
  "identity_private": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "CTO / AICOS maintainer",
    "mcp_name": "aicos_local_private",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

## Summary

The public repo sync/export boundary is a real packaging smell, but public publishing is not currently important enough to justify manifest/export refactor work. Do not prioritize public-specific package manifest or sync-script redesign now.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

The useful near-term subset is not public export itself; it is the general AICOS modularity behind it: configurable brain root and reusable template/sample brain packs.

## Next Step

Track the core modularity work in dedicated items: aicos-brain-root-config-boundary and aicos-template-project-brain-pack. Revisit public export manifest only before a real public release.

## Trace Refs

- source_ref: `public-export/sync-aicos-pub.sh`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
