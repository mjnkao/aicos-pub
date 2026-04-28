# aicos-pub Current Handoff

Date: 2026-04-28
Scope: `projects/aicos-pub`

## Current State

`aicos-pub` is deployed on Railway and serves AICOS MCP over HTTPS with bearer
token auth. PostgreSQL, pgvector, and embeddings are enabled for the exported
public corpus.

## Current Runtime

- MCP URL: `https://aicos-pub-production.up.railway.app/mcp`
- Health URL: `https://aicos-pub-production.up.railway.app/health`
- Search mode: `postgresql_hybrid`
- Embedding coverage: expected `1.0` after deploy/restart stabilization

## Active Public Work

- Maintain public export safety boundaries.
- Document Railway install and MCP client setup.
- Support public agents through scoped bearer tokens.
- Build agent-facing project management surfaces for public workstreams.

## Next Steps

- Harden PostgreSQL schema apply retry/backoff to avoid manual restart after
  Railway redeploy lock timeouts.
- Continue moving public onboarding and agent setup docs into stable install
  guides.
- Replace mock dashboard data in the AI Agent PM Dashboard with read-only AICOS
  MCP calls, then add carefully scoped write flows.
