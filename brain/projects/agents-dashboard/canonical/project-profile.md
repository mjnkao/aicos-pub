# Agents Dashboard Project Profile

Scope: `projects/agents-dashboard`

`agents-dashboard` is the AICOS-managed project for the AI Agent PM Dashboard:
a project-management dashboard for AI agents working through AICOS public MCP.

## Runtime And Repository

- AICOS runtime: `public-railway-aicos`
- AICOS MCP endpoint: `https://aicos-pub-production.up.railway.app/mcp`
- AICOS scope: `projects/agents-dashboard`
- Local code path: `<USER_HOME>/Projects/agents-pm-dashboard`
- Git repository: `git@github.com:mjnkao/ai-agent-pm-dashboard.git`
- GitHub URL: `https://github.com/mjnkao/ai-agent-pm-dashboard`

## Purpose

- Show project status, handoff, open items, tasks, feedback, and agent activity
  from AICOS.
- Help human operators and agents understand what to do next.
- Provide a public example app that consumes AICOS MCP context.

## Current Boundary

The app repository remains the code/runtime authority for the dashboard UI.
AICOS is the context and project-management authority for coordination,
handoff, tasks, and agent feedback.

## Write Boundary

External agent tokens may write to `projects/agents-dashboard` for project
coordination. They must not write to protected core scope `projects/aicos`.
