# Status Item: aicos-mcp-schema-constants-dedupe-next

Status: open
Item type: `open_item`
Type guidance: New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-mcp-schema-constants-dedupe-next`
Title: Centralize MCP tool schemas and shared constants before adding more tools
Last write id: `20260428T075745Z-89eba3c1a7`
Last updated at: `2026-04-28T07:57:45+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-checklist-5-step`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-checklist-5-step`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Phase 1/3 review confirms the next low-risk modularization step should be schema/constants dedupe for MCP tools. HTTP daemon and stdio adapter currently duplicate tool schemas and can drift; the status-items identity/filter bug was one symptom. This should be a focused refactor, not a provider framework.

## Item Type Guidance

New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.

## Reason

This strengthens the current small-team operating surface and reduces future drift without adding runtime weight or new dependencies.

## Next Step

Create a shared schema/constants module for MCP tool definitions or generate daemon/stdio schemas from one source, then verify tools/list parity for HTTP and stdio.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-phase-3-provider-interface-sketch-20260428.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
