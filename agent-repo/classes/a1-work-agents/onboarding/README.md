# A1 Work Agent Onboarding

Status: shared A1 onboarding index

This folder is the front door for A1 work agents joining a company, workspace,
project, workstream, or task scope.

## Start Here

- `a1-context-ladder.md`: generic A1 reading ladder.
- `a1-new-agent-prompt-template.md`: prompt template for starting a fresh A1
  worker.

## Rule

A1 must identify scope before reading deeply. Project context belongs in
`brain/projects/<project-id>/`, while actor operation belongs in
`agent-repo/classes/a1-work-agents/`.

A1 should use the local MCP read/write surfaces first for AICOS-facing
context/control-plane operations when available:

- read startup bundle / packet index / selected task packet through MCP
- write checkpoint / task update / handoff update through semantic MCP tools

Direct local repo or artifact access is still correct for the actual scoped
project work, such as code, design, content, research, runtime, or external
source artifacts.
