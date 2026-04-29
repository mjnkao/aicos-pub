# Status Item: aicos-brain-root-config-boundary

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-brain-root-config-boundary`
Title: Add configurable brain root boundary for AICOS runtime
Last write id: `20260428T141752Z-b2f3836243`
Last updated at: `2026-04-28T14:17:52+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-brain-root-boundary`
Agent display name: `Codex Desktop`
Work type: `code`
Work lane: `brain-modularity`
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

Implemented a small shared brain-root resolver in aicos_kernel.paths. Kernel sync/status, MCP read/write serving, context registry, PG indexer, and daemon scope reindex now use brain_path()/brain_root() for AICOS brain paths while default behavior remains <repo>/brain. AICOS_BRAIN_ROOT smoke with the current brain path works for brain status, status-items, and context registry. Retrieval gate still passes: 59 items, top3 57/59, top5 59/59, errors 0.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

This creates the first modularity boundary needed for future mounted/private brain packs without changing truth semantics or implementing public export now.

## Next Step

Use this resolver as the boundary for future template/sample project brain pack work. Do not assume arbitrary external brain roots are production-ready until write-path and packaging tests cover them.

## Trace Refs

- source_ref: `packages/aicos-kernel/aicos_kernel/paths.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
