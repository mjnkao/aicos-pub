# Agents Dashboard Current Direction

Scope: `projects/agents-dashboard`
Status: active

## Direction

Build the AI Agent PM Dashboard as a public example and real operating surface
for AICOS-managed AI agent projects.

## Near-Term Work

- Replace mock dashboard data with AICOS MCP reads.
- Show current handoff, current state, status items, feedback, and project
  health.
- Add safe write flows for external agent feedback.
- Document setup for Codex, Claude Code, and other MCP-capable agents.

## Product Boundary

- Dashboard repo is code/runtime authority.
- AICOS is context, project-management, and continuity authority.
- Tokens must never be committed or exposed in frontend code.
