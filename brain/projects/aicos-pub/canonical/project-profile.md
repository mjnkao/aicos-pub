# aicos-pub Project Profile

Scope: `projects/aicos-pub`

`aicos-pub` is the public distribution and community-facing deployment lane for
AICOS. It carries public-safe architecture, install, MCP, export, deployment,
and onboarding context derived from AICOS without exposing private project data.

## Current Public Runtime

- Railway MCP endpoint: `https://aicos-pub-production.up.railway.app/mcp`
- Retrieval: PostgreSQL hybrid search with pgvector and OpenAI embeddings
- Public write scope: `projects/aicos-pub`
- Protected private-source scope: `projects/aicos`

## Write Boundary

Public/community agents may write continuity, feedback, status, and handoff
updates only to `projects/aicos-pub` unless a maintainer explicitly grants a
broader scope. Do not write private-source continuity into `projects/aicos`.
