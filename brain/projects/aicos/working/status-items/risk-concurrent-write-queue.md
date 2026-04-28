# Status Item: RISK-CONCURRENT-WRITE-QUEUE

Status: open
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `RISK-CONCURRENT-WRITE-QUEUE`
Title: Medium-term concurrency: per-scope write queue + optimistic concurrency for current.md
Last write id: `20260423T042939Z-117eb4cac1`
Last updated at: `2026-04-23T04:29:39+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `claude-code-ops-20260423-infra`
Agent display name: `unknown`
Work type: `ops`
Work lane: `concurrency-safety`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

After RISK-CONCURRENT-WRITE-LOCK is fixed, two medium-term improvements remain. (1) PER-SCOPE WRITE QUEUE: writes to the same project scope are serialized via a FIFO queue in the daemon — reads stay parallel, only same-scope writes queue up. Eliminates file lock contention without blocking cross-scope throughput. (2) OPTIMISTIC CONCURRENCY: write_handoff_update accepts a last_write_id param; daemon rejects if file was modified since agent's last read, forcing retry. Prevents silent overwrite even if file lock is missed. Dependency: complete RISK-CONCURRENT-WRITE-LOCK first.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

File lock (RISK-CONCURRENT-WRITE-LOCK) prevents data loss but can serialize all writes globally. Scope queue + optimistic concurrency give better throughput and stronger correctness guarantee for 10+ concurrent agents.

## Next Step

Codex: implement after RISK-CONCURRENT-WRITE-LOCK is resolved. (1) Add per-scope asyncio.Lock or threading.Lock dict in daemon, keyed by scope string. (2) Add optional last_write_id field to write_handoff_update; return write_id on success; reject with 409 if mismatch. File: aicos_mcp_daemon.py, mcp_write_serving.py.

## Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
