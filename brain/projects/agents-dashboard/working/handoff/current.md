# Agents Dashboard Current Handoff

Scope: `projects/agents-dashboard`
Status: active starter project

## Current State

The local dashboard repo exists at `<USER_HOME>/Projects/agents-pm-dashboard`
and is connected to `git@github.com:mjnkao/ai-agent-pm-dashboard.git`.

The AICOS public project scope now exists so Railway MCP clients can read and
write project-management context for this dashboard.

## Next Work

- Replace any remaining mock dashboard data with AICOS MCP reads.
- Add views for current handoff, status items, feedback, and project health.
- Add a safe write flow for external agent feedback to
  `projects/agents-dashboard`.
- Add setup docs showing how Codex, Claude Code, and other agents connect with
  scoped Railway tokens.

## Guardrails

- Do not expose bearer tokens in the dashboard UI or committed docs.
- Keep token-bearing setup files local-only under ignored runtime folders.
- Treat `<USER_HOME>/Projects/agents-pm-dashboard` as the code authority.
- Treat this AICOS project as the coordination/context authority.
