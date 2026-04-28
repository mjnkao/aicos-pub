# A2 Service Agent Onboarding

Status: shared A2 onboarding index

This folder is the front door for new A2 service agents entering AICOS from
Codex, Claude Code, OpenClaw, ChatGPT, or another external co-worker runtime.

## Start Here

- `a2-core-context-ladder.md`: use when the agent will improve AICOS itself.
- `a2-serve-context-ladder.md`: placeholder for future A2-Serve agents.
- `a2-core-new-agent-prompt-template.md`: prompt template for starting a fresh
  A2-Core thread.

## Rule

Read ladders as routing surfaces, not as replacement truth. The short summaries
explain why a file matters; the referenced files remain authoritative.

For MCP-related maintenance, use the contract and integration docs as the
current source of truth:

- `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- `integrations/local-mcp-bridge/README.md`

A2-Core can still read and edit the repo directly while maintaining AICOS. The
MCP-first rule is aimed at A1-facing context/control-plane access.
