# Status Item: AICOS-RUNTIME-SPOF-SSE-OPTIONS-20260429

Status: open
Item type: `open_question`
Type guidance: Unresolved question needing human, architecture, product, or project decision before the next clear action.
Project: `aicos`
Scope: `projects/aicos`
Item id: `AICOS-RUNTIME-SPOF-SSE-OPTIONS-20260429`
Title: Choose near-term runtime reliability model for small-team AICOS
Last write id: `20260429T024710Z-274865598c`
Last updated at: `2026-04-29T02:47:10+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260429-major-work-plan-pass`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-runtime-hardening`
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

Created an options memo for single-machine SPOF, LAN fallback, LAN security, and SSE/auth interop. Recommended near-term option is to accept/document the current single-host small-team model with stronger push/runbook/health discipline, while deferring secondary daemon, VPS/cloud host, or first-class streamable HTTP/session bootstrap until real team/remote usage demands it.

## Item Type Guidance

Unresolved question needing human, architecture, product, or project decision before the next clear action.

## Reason

AICOS should not overbuild infrastructure before real usage requires it, but should make the current reliability boundary explicit.

## Next Step

Human/CTO should decide whether to accept the recommended near-term model. Do not implement secondary daemon, cloud host, or auth transport changes until the decision changes.

## Trace Refs

- artifact_refs:
  - `brain/projects/aicos/working/status-items/arch-single-machine-spof.md`
  - `brain/projects/aicos/working/status-items/risk-lan-agent-fallback.md`
  - `brain/projects/aicos/working/status-items/aicos-lan-security-hardening.md`
  - `brain/projects/aicos/working/status-items/aicos-mcp-sse-auth-interop.md`
- source_ref: `brain/projects/aicos/evidence/research/aicos-runtime-spof-sse-options-20260429.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
