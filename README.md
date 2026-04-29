# AICOS

Status: public staging snapshot, synced from private AICOS on 2026-04-29.

AICOS is a local-first, online-ready context/control-plane for multi-agent
project work. It gives humans and agents a shared project reality without
turning every repository into one huge prompt, one chat log, or one private
memory dump.

This repository is the public continuation package for AICOS. It is generated
from a private source checkout through the public-export pipeline, then curated
so external agents and humans can understand the current architecture,
unfinished work, and next direction.

## Current Direction

AICOS is moving toward **Option C**:

```text
stable semantic core
  -> runtime services
  -> provider/profile/pack layers
  -> project, workspace, and company deployments
```

The core idea is deliberately narrow: AICOS should remain the semantic
coordination layer for agent work, not become a PM tool, a generic memory app,
or a replacement for source repositories.

Near-term deployment profiles are:

- `solo`: local-first project context and MCP access.
- `small-team`: HTTP MCP daemon, token auth, PostgreSQL hybrid search,
  pgvector embeddings, and shared project packs.
- `company-100`: stronger workspace/company packs, governance, audit, and
  service boundaries.
- `enterprise`: future profile, not the current build target.

The current public Railway runtime is the `small-team` implementation bundle:
HTTP MCP daemon + PostgreSQL hybrid search + pgvector + token-scoped write
access + Markdown authority.

## What AICOS Is

AICOS is a multi-human, multi-agent, multi-project work-brain.

It stores compact project context that agents and humans need in order to work
coherently:

- stable truth, decisions, rules, and architecture;
- current state, handoffs, open items, open questions, risks, and next tasks;
- evidence, research, import notes, and candidate updates;
- bounded read/write surfaces through MCP.

Your project repo remains the authority for code, tests, scripts, schemas,
generated artifacts, and runtime behavior. AICOS stores the control-plane
context around that work.

## What AICOS Is Not

AICOS is not:

- a PM product competing with Plane, Linear, ClickUp, or Jira;
- a personal memory app;
- a vector database wrapper;
- a raw cross-repo file editor;
- a replacement for Git, tests, CI, docs, or source repositories.

The Work State Ledger direction may project tasks/open items/questions/tech
debt into dashboard views later, but the authority remains AICOS semantic state
and the relevant project repositories.

## Start Here

Read these first if you are a new agent or human contributor:

- [Continuation guide](docs/aicos-continuation-guide.md)
- [Current architecture index](docs/architecture/README.md)
- [Current state](brain/projects/aicos/working/current-state.md)
- [Current direction](brain/projects/aicos/working/current-direction.md)
- [Current handoff](brain/projects/aicos/working/handoff/current.md)
- [Structured status items](brain/projects/aicos/working/status-items/)
- [Project registry](brain/shared/project-registry.md)

Key architecture anchors:

- [Option C architecture north star](brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md)
- [Option C transition checklist](brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md)
- [Work State Ledger vocabulary](brain/projects/aicos/evidence/research/aicos-work-state-ledger-vocabulary-spec-20260429.md)
- [Work State Ledger minimal schema proposal](brain/projects/aicos/evidence/research/aicos-work-state-ledger-minimal-schema-proposal-20260429.md)
- [Project intake productization options](brain/projects/aicos/evidence/research/aicos-project-intake-productization-options-20260429.md)

MCP/operator guides:

- [Query/search guide](docs/install/AICOS_QUERY_SEARCH_GUIDE.md)
- [MCP write cookbook](docs/install/AICOS_MCP_WRITE_COOKBOOK.md)
- [Railway agent connection guide](docs/install/AICOS_PUB_RAILWAY_AGENT_CONNECT.md)
- [Railway setup runbook](docs/install/AICOS_PUB_RAILWAY_SETUP_RUNBOOK.md)

## Repository Shape

- `brain/`: durable project truth and working state.
- `agent-repo/`: actor rules, startup cards, rule cards, and task packets.
- `packages/aicos-kernel/`: deterministic schemas, contracts, validators, CLI,
  read/write serving, and search integration.
- `integrations/`: MCP daemon and local MCP bridge.
- `templates/`: reusable project brain packs and onboarding templates.
- `serving/`: generated context surfaces, option packets, branch comparisons,
  and promotion review packets.
- `backend/`: local substrate and indexing support, not the truth store.
- `docs/`: current architecture index, install, MCP, and deployment guides.

## Authority Model

AICOS organizes project knowledge by state:

- `canonical`: approved or stable truth, such as project profile,
  architecture, requirements, decisions, and working rules.
- `working`: current reality, such as current state, direction, risks, open
  questions, open items, status items, and handoff.
- `evidence`: raw or reviewed inputs, such as research, source inventories,
  import notes, test evidence, and candidate updates.

The usual promotion path is:

```text
evidence -> working -> canonical
```

ADR-001 is the current truth-store rule: Markdown/agent-repo is authority;
PostgreSQL, FTS, vector indexes, cache, and daemon responses are serving/index
layers until a deliberate migration trigger changes that.

## Public Railway Runtime

The public MCP runtime is named:

```text
aicos_railway_public
```

Current endpoint:

```text
https://aicos-pub-production.up.railway.app/mcp
```

Use runtime-relative identity:

- Public/external work agents are `A1` relative to `aicos_railway_public`.
- Internal maintainers of the public Railway AICOS runtime are `A2-Core-C` or
  `A2-Core-R` relative to `aicos_railway_public`.
- The same Codex/Claude/OpenClaw client may have a different A1/A2 role in a
  different AICOS runtime.

Current public scopes:

- `projects/aicos`: core AICOS context, protected for internal maintainers.
- `projects/templates`: public templates/examples.
- `projects/agents-dashboard`: public AI Agent PM dashboard project context.

Do not use these removed/obsolete public scopes:

- `projects/aicos-pub`
- `projects/agents-pm-dashboard`

The repository/service can still be called `aicos-pub`; that is not the same
thing as an AICOS project scope.

## What Works Today

You can currently:

- run `./aicos --help`;
- inspect and extend AICOS kernel contracts and schemas;
- run the HTTP MCP daemon locally or on Railway;
- use PostgreSQL hybrid search with pgvector embeddings when configured;
- connect agents through Streamable HTTP MCP with bearer token auth;
- read project health, handoff, status items, feedback digest, and bounded
  project context;
- write semantic checkpoints, task updates, handoffs, status items, artifact
  refs, and feedback through MCP;
- bootstrap new projects from templates and project brain packs.

## Still Early

This is not a polished release.

Known active areas:

- Work State Ledger vocabulary and schema need implementation hardening.
- Project intake/import needs more MCP-native tooling.
- Runtime services need stronger retry, audit, auth, and operator ergonomics.
- Dashboard/PM projections should remain projections, not core authority.
- Public examples and templates should be expanded through real agent use.

## Safety

Do not commit secrets, `.env` files, bearer tokens, private project context,
local runtime homes, private logs, or generated output bulk.

If an example is derived from a real project, rewrite it into a synthetic sample
with fake names, fake paths, fake source inputs, and no operational history.

## License

Apache License 2.0 for now. The project may reconsider MIT later.
