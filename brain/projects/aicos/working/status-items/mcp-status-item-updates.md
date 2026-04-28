# Status Item: mcp-status-item-updates

Status: resolved
Item type: `open_item`
Project: `aicos`
Scope: `projects/aicos`
Item id: `mcp-status-item-updates`
Title: MCP structured status updates for open items/questions/tech debt
Last write id: `mcp-status-item-updates-resolved`
Last updated at: `2026-04-21T08:56:27+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-a2-core-20260421-status-items`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-mcp-status-items`
Coordination status: `completed`
Artifact scope: `AICOS MCP status item write surface`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added lightweight MCP status-item upsert surface so agents can mark open items, open questions, tech debt, and decision follow-ups by stable item_id instead of appending noisy handoff sections.

## Reason

Claude A2-Core-R reported that agents could only append handoff notes when closing items, which made current handoff noisy and left source items unclear.

## Next Step

Use aicos_update_status_item for future item status changes; do not migrate all legacy lists until a concrete cleanup pass is selected.

## Trace Refs

- source_ref: `brain/projects/aicos/working/handoff/current.md#MCP Continuity Update 20260421T085151Z-67445fd0ec`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
