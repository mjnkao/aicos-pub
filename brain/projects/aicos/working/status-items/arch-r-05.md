# Status Item: ARCH-R-05

Status: resolved
Item type: `tech_debt`
Type guidance: Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.
Project: `aicos`
Scope: `projects/aicos`
Item id: `ARCH-R-05`
Title: CLI PATH friction resolved with install cli
Last write id: `20260423T020421Z-3d3d15506e`
Last updated at: `2026-04-23T02:04:21+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-20260423-roadmap-reconcile`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-cli-lan-policy-minimum`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Added portable symlink install command `./aicos install cli`. Fixed the root wrapper to resolve symlink targets before setting PYTHONPATH, so `aicos ...` works from outside the repo after install.

## Item Type Guidance

Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.

## Reason

User approved fixing CLI install/path portability now.

## Next Step

Operators can install into a PATH directory such as ~/.local/bin; docs should still use ./aicos when no install is guaranteed.

## Trace Refs

- artifact_refs:
  - `aicos`
  - `packages/aicos-kernel/aicos_kernel/kernel.py`
  - `integrations/local-mcp-bridge/README.md`

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
