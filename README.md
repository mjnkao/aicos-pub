# AICOS

Status: public staging snapshot, synced from private AICOS on 2026-04-29.

AICOS is a local-first, team-ready context/control-plane for multi-agent
project work. It gives humans and agents a shared project reality without
turning every repository into one huge prompt, one chat log, or one private
memory dump.

Local-first does not mean local-only. AICOS now has a working small-team path:
run it locally for one operator, expose it on a trusted LAN for a small team, or
deploy it to Railway as an HTTP MCP service with token auth, PostgreSQL hybrid
search, pgvector embeddings, and scoped agent access.

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
  pgvector embeddings, LAN/Railway deployment, and shared project packs.
- `company-100`: stronger workspace/company packs, governance, audit, and
  service boundaries.
- `enterprise`: future profile, not the current build target.

The current public Railway runtime is the `small-team` implementation bundle.
It proves that AICOS can run beyond a single local checkout while still keeping
Markdown authority, scoped token access, PostgreSQL hybrid search, and pgvector
as serving/index layers.

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

## Related Work And Influences

AICOS is not built in a vacuum. It explicitly learns from nearby open-source
projects, memory products, orchestration frameworks, and PM tools. The goal is
to acknowledge those influences while keeping AICOS' own boundary clear.

- [GBrain](https://github.com/garrytan/gbrain): the strongest current
  influence on retrieval/search substrate, MCP-native memory/search, freshness
  discipline, skills, jobs, and page/link organization. AICOS should reuse or
  wrap GBrain-like substrate patterns where they fit, but should not copy
  GBrain's product identity or make a GBrain database the AICOS truth store.
- [Memobase](https://memobase.ai/) and [Membase](https://membase.so/): validate
  the need for persistent memory shared across agents and MCP-compatible tools.
  AICOS learns from that memory-layer direction, but narrows its own scope to
  project authority, handoff, status, and control-plane semantics.
- [GitAgent](https://github.com/open-gitagent/gitagent): validates
  git-native, reviewable agent configuration, identity, and audit surfaces.
  AICOS shares the preference for file-backed, inspectable operating state, but
  adds its own project truth/working/evidence model.
- [LangGraph](https://docs.langchain.com/oss/javascript/langgraph/persistence),
  [LangMem](https://langchain-ai.github.io/langmem/), CrewAI, and Mem0:
  validate persistence, checkpoints, orchestration, and memory as mainstream
  agent-runtime concerns. AICOS treats these as runtime/substrate ideas, not as
  replacements for AICOS' semantic control-plane.
- Plane, ClickUp, Linear, Jira, and similar PM systems: validate the need for
  dashboard views, work items, relations, ownership, comments, notifications,
  and human workflow. AICOS may integrate with these tools, but should not
  become a PM clone or let external board fields overwrite AICOS semantic
  authority.

The current architecture direction is therefore reuse-first at the substrate
layer and AICOS-owned at the semantic/control-plane layer. See the market and
substrate review in
[AICOS Market Landscape And Substrate Comparison](brain/projects/aicos/evidence/research/aicos-market-landscape-and-substrate-comparison-20260428.md)
and the
[AICOS On Top Of GBrain decision memo](brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md).

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

## Deployment Profiles

AICOS currently supports three practical operating modes:

- Local solo: one human or agent runs AICOS from a checkout and uses the CLI,
  local MCP bridge, or local HTTP daemon.
- Trusted LAN: a small team runs the HTTP MCP daemon on a reachable machine
  with bearer token auth. Non-loopback/LAN mode should not run without auth.
- Railway small-team: a hosted HTTP MCP service with token-scoped access,
  PostgreSQL hybrid retrieval, pgvector embeddings, health checks, and external
  agent connection guides.

The product direction is local-first and team-ready: local files remain the
human-readable authority, while LAN/Railway runtimes provide shared read/write
serving for multiple agents and humans.

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
- run the HTTP MCP daemon locally, on a trusted LAN, or on Railway;
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
