# MCP Phase 2 Write Tools Implementation Note

Date: 2026-04-19
Actor: A2-Core Codex
Scope: `projects/aicos`

## What Phase 2 Now Includes

Phase 2 adds three semantic MCP write tools:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

These tools let A1 send small structured continuity intent to AICOS. AICOS MCP
validates, maps, formats, and records the update into approved lanes.

## Contracts

Updated:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`

The contract now defines tool purpose, inputs, validation rules, lane mapping,
output shape, and failure behavior for the three Phase 2 write tools.

## Implementation / Scaffolding

Added transport-independent write operations:

- `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`

Updated local surfaces:

- `packages/aicos-kernel/aicos_kernel/kernel.py`
- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`
- `integrations/local-mcp-bridge/README.md`

## Lane Mapping

- `aicos_record_checkpoint` writes checkpoint notes under:
  `brain/projects/<project-id>/evidence/checkpoints/`
- `aicos_write_task_update` writes project task continuity under:
  `brain/projects/<project-id>/working/task-state/`
- `aicos_write_handoff_update` upserts one compact continuity section in:
  `brain/projects/<project-id>/working/handoff/current.md`

## Why Raw File Tools Were Not Added

Generic tools such as `aicos_write_file`, `aicos_append_text`, or
`aicos_edit_any_path` would bypass AICOS lane semantics and recreate the
cross-folder ambiguity MCP is meant to reduce. Phase 2 intentionally implements
semantic continuity writes only.

## Still Deferred

- remote/online transport
- auth/session system
- family-specific wrappers
- broad workflow automation
- large cache/observability layer
- extra write tools beyond the initial three
- generic raw file mutation tools

## Next Likely Usage-Test Step

Run a bounded local MCP read/write usage test from an external checkout. The
test should call the Phase 1 read tools, then one or more Phase 2 write tools,
and verify the generated checkpoint/task-state/handoff outputs.
