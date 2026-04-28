# AICOS Phase 4 Deployment Profiles

Status: phase-4 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Formalize AICOS deployment profiles so the current small-team implementation
does not become an implicit one-size-fits-all stack.

This is a profile definition note only. It does not add runtime code, providers,
jobs, auth systems, dashboards, or hosted deployment.

## Profile Matrix

| Profile | Target | Required capabilities | Optional capabilities | Provider expectation |
| --- | --- | --- | --- | --- |
| `solo` | one person or one machine | markdown truth, local startup/handoff/status reads, bounded query, semantic writes, simple CLI, local MCP/stdio | local HTTP daemon, embeddings, PG hybrid | markdown context store, markdown-direct or local PG retrieval, no heavy auth |
| `small-team` | 5-20 people/agents | shared context/control-plane, HTTP MCP, token auth, audit log, PG hybrid search, feedback loop, freshness visibility, multi-agent handoff | GBrain sync, embeddings, health monitor, HTTPS proxy for Claude Desktop | current bundle: markdown truth + GBrain sync/import + PG hybrid + HTTP MCP + labeled tokens |
| `company-100` | growing company using many AI agents | stronger auth/audit, stable jobs provider, dashboard/PM integration, project/workspace/company context packs, permission-aware ingestion, reliable retrieval, human attention queue | graph provider, enterprise search integration, SSO/RBAC, hosted deployment | modular provider stack; current bundle may remain dev/local substrate but not enough alone |
| `enterprise` | future larger org | permission-aware org memory, enterprise audit, governance, advanced connectors, policy controls, data residency | custom provider mix | future target only; do not build now |

## Current Stack Classification

The current implementation is the first concrete `small-team` bundle:

- markdown truth under `brain/`;
- AICOS contracts/schemas under `packages/aicos-kernel/`;
- GBrain sync/import as local substrate;
- PG hybrid retrieval with optional embeddings;
- HTTP MCP daemon;
- local stdio bridge and HTTP-first stdio proxy;
- labeled bearer tokens;
- JSONL audit;
- lightweight feedback loop;
- optional launchagents/health monitor.

It should not be described as "the AICOS architecture." It is one provider
bundle under the AICOS semantic/control-plane architecture.

## Profile Boundaries

### Solo

Optimize for:

- inspectability;
- low setup cost;
- no always-on requirement;
- no heavy auth;
- local-only work.

Do not require:

- GBrain;
- PG;
- embeddings;
- background jobs;
- dashboard;
- PM sync.

### Small-team

Optimize for:

- many agent families;
- shared durable context;
- HTTP MCP access;
- audit and feedback;
- enough search quality for project handoff;
- no hosted dependency by default.

Required:

- stable MCP read/write path;
- token-separated clients;
- query/search freshness visibility;
- A1 feedback loop;
- compatibility docs by client family.

### Company-100

Optimize for:

- many humans and AI agents;
- many projects;
- dashboard/PM-tool coordination;
- permissions and accountability;
- reliable jobs/maintenance;
- stronger retrieval and ingestion.

Likely needs:

- Auth/Audit Provider beyond local tokens;
- Jobs Provider beyond desktop automation;
- Connector Provider for PM/docs/repos;
- Retrieval Provider that can scale beyond local markdown/PG;
- dashboard-facing read surfaces.

Do not jump here by making the current daemon bigger. Company-100 should be a
profile assembled from clearer provider boundaries.

## Required vs Optional Capability Table

| Capability | Solo | Small-team | Company-100 |
| --- | --- | --- | --- |
| Markdown truth | required | required/current | optional as source format |
| Semantic MCP reads/writes | required | required | required |
| HTTP MCP | optional | required | required or hosted equivalent |
| Token auth | optional | required | insufficient alone |
| Audit | basic | required | strong/centralized |
| PG hybrid search | optional | current required bundle | provider choice |
| Embeddings | optional | recommended | provider choice |
| Feedback loop | recommended | required | required |
| Jobs/maintenance | manual | lightweight | reliable provider |
| Dashboard/PM integration | not needed | optional | required |
| Enterprise SSO/RBAC | not needed | not needed | likely required |
| Graph/relation provider | not needed | trace refs only | optional if evals prove need |

## Scalability / Bloat Guardrail

When adding a feature, first ask:

1. Is this semantic core, runtime service, provider, or profile-specific?
2. Which profile actually needs it?
3. Can `solo` keep working without it?
4. Can `small-team` use it without extra operational burden?
5. Does this belong in the current daemon, or should it wait for a provider
   boundary?

Default answer:

- keep `solo` simple;
- keep `small-team` practical;
- design `company-100` without cramming it into the current daemon.

## Immediate Implication

The next implementation work should not be a hosted platform or dashboard.

Near-term useful work:

- reduce MCP schema duplication;
- improve A1 search quality;
- tighten freshness/status signals;
- keep feedback loop active;
- prepare dashboard read-surface contracts before building UI.
