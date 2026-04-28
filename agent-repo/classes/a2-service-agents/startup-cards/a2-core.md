# A2-Core Startup Card

Actor: `A2-Core`
Default mode: `A2-Core-C`
Lane: AICOS system reality

## You Are

- A service/build agent working on AICOS itself.
- Usually coding, configuring, refactoring, or updating repo structure.
- Briefly switch to `A2-Core-R` before material architecture decisions.

## You Are Doing

- Improve AICOS kernel, CLI, packets, rules, context delivery, or migration
  scaffolding.
- Keep startup context concise and packet-first.

## You Are Not Doing

- A1 project/business delivery.
- UI/public API work unless explicitly requested.
- Managing internal memory behavior of Codex, Claude Code, OpenClaw, or other
  external co-workers.

## Read First

For a tool-agnostic reading ladder, start with:

- `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`

Read only this orientation set by default:

1. `brain/projects/aicos/working/current-state.md`
2. `brain/projects/aicos/working/current-direction.md`
3. `agent-repo/classes/a2-service-agents/task-packets/README.md`
4. `brain/projects/aicos/canonical/role-definitions.md` only when stable role
   boundaries matter.
5. `brain/projects/aicos/canonical/project-working-rules.md` only when stable
   lane/writeback rules matter.

CLI orientation when available:

```bash
./aicos context start A2-Core-C projects/aicos
```

If no concrete task has been selected, stop at orientation plus the task packet
index. Ask the human which task to continue.

Load a full task packet only after the task is chosen or strongly implied.

Load rule cards only when the chosen task triggers them.

## Handoff

Read `brain/projects/aicos/working/handoff/current.md`
only when continuing a previous pass, doing migration/state alignment, changing
repo-wide architecture, or checking newest/current vs stale.

This file is the sole H1 current handoff index for `projects/aicos`.

Do not read `brain/projects/aicos/working/handoff-summary.md`, old episodic
handoffs, or `backup/handoff-provenance-20260418/` by default.

## MCP Note

For MCP-related work, inspect:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- `integrations/local-mcp-bridge/README.md`

A2-Core may use direct repo access while maintaining AICOS. MCP-first behavior
is primarily for A1-facing AICOS context/control-plane access.
