# MCP Phase 1 Read-Serving Implementation Note

Date: 2026-04-19
Actor: A2-Core Codex 1
Scope: `projects/aicos`

## What Phase 1 Now Includes

Phase 1 adds a small local-first read-serving surface for A1-facing
AICOS context/control-plane access.

Implemented read surfaces:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_packet_index`
- `aicos_get_task_packet`

## Contracts

Updated:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`

The contract now records Phase 1 inputs, output shape, source mapping, trace
metadata expectations, and structured failure behavior.

## Implementation / Scaffolding

Added transport-independent operations layer:

- `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`

Updated CLI debug surface:

- `./aicos mcp read startup-bundle --actor A1 --scope projects/sample-project`
- `./aicos mcp read handoff-current --actor A1 --scope projects/sample-project`
- `./aicos mcp read packet-index --actor A1 --scope projects/sample-project`
- `./aicos mcp read task-packet --actor A1 --scope projects/sample-project --packet-id review-sample-workstream-import-slice`

Added local stdio adapter:

- `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

Updated integration README:

- `integrations/local-mcp-bridge/README.md`

## Why Writeback Is Deferred

Writeback tools need stricter validation and lane-mapping behavior. Phase 1 is
limited to compact read bundles so the repo can test MCP-first context serving
before accepting mutations through MCP.

Deferred tools:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

## Design Boundaries Preserved

- local-first, stdio-first
- bundle-first, not raw file RPC
- family-neutral for Codex, Claude, OpenClaw, and future clients
- A1 MCP-first for AICOS-facing context/control-plane reads
- A2 direct repo access remains allowed
- MCP is access/control-plane, not truth store
- no remote transport, auth/session system, daemon, cache, or writeback

## Next Likely Pass

Run a small local MCP usage test from an external checkout, then design Phase 2
writeback tools only after read-serving behavior is validated.
