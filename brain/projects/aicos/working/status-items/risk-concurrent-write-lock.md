# Status Item: RISK-CONCURRENT-WRITE-LOCK

Status: resolved
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `RISK-CONCURRENT-WRITE-LOCK`
Title: Concurrent write safety: file lock + cache invalidation implemented
Last write id: `20260423T064653Z-aca0dcfa96`
Last updated at: `2026-04-23T06:46:53+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-embedding-pass`
Agent display name: `unknown`
Work type: `code`
Work lane: `concurrency-safety`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Implemented scope-level write locking in mcp_write_serving.py using fcntl.flock under .runtime-home/aicos-write-locks, and improved ResponseCache invalidation to track scope per cached read. HTTP daemon write path invalidates scope cache immediately after semantic writes. This resolves the immediate silent overwrite/stale read risk for file-backed AICOS write tools while preserving markdown as truth store.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

Implemented by Codex during AICOS HTTP/embedding hardening pass on 2026-04-23.

## Next Step

Keep RISK-CONCURRENT-WRITE-QUEUE open as the medium-term scalability follow-up; file locking is the minimum correctness layer, not the final high-throughput design.

## Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `packages/aicos-kernel/aicos_kernel/mcp_cache.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
