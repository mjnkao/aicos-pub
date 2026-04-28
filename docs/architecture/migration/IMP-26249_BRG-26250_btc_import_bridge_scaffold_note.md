# IMP-26249 / BRG-26250 sample project Import And Bridge Scaffold Note

Date: 2026-04-19
Actor: A2-Core-C
Scope: `projects/aicos`

## Import Scaffolding Added

Created AICOS project scaffold:

```text
brain/projects/sample-project/
```

Normalized import identity:

- source project: `sample project-Trading-Framework`
- source branch: `main`
- AICOS project id: `sample-project`
- first slice: `default sample_workstream delivery slice`

Added first-slice planning lanes:

- `brain/projects/sample-project/evidence/source-inventory/import-plan.md`
- `brain/projects/sample-project/evidence/workstreams/default-sample-workstream-delivery-slice.md`
- `brain/projects/sample-project/evidence/import-notes/authority-and-mapping.md`
- `brain/projects/sample-project/evidence/delivery-surfaces/sample-workstream-surface.md`

Added A1 packet scaffold:

```text
agent-repo/classes/a1-work-agents/task-packets/sample-project/
```

## MCP Bridge Contract Normalized

Added contract-only local MCP bridge scaffold:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- `integrations/local-mcp-bridge/README.md`

The contract is local-first, stdio-oriented, and intentionally thin. It defines
read tools, writeback tools, and checkpoint payload shape but does not implement
a server or remote platform.

## Authority Boundary

- AICOS remains context/control-plane authority.
- sample project repo remains code/runtime authority.
- Optional `.aicos/` cache in external repos is future convenience only, not
  truth.

## Intentionally Left For Later

- no full sample project repo import
- no canonical sample project truth digestion yet
- no MCP server implementation yet
- no remote infrastructure
- no broad automation or registry-heavy workflow

## Next Concrete Step

Confirm the local sample project repo path and inspect branch `main` to complete the
source inventory for the `default sample_workstream delivery slice`. Only after that
should AICOS digest selected canonical/working context from sample project.
