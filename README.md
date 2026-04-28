# AICOS

Status: public staging preview

AICOS is a local-first context and coordination layer for AI agents working
across real projects. It helps humans and agents share the same project reality
without turning every project repository into one large prompt, one chat log, or
one private memory dump.

This repository is a public staging package. It is generated and curated from a
private AICOS source checkout through an allowlist export and synthetic public
examples. It is not yet a final release.

## Why AICOS Exists

Modern AI coding and work agents are capable, but they still struggle with the
same operating problems:

- they start from incomplete or stale context;
- each new thread has to rediscover project reality;
- handoffs become long chat histories instead of compact state;
- agents read too much raw history or too little current truth;
- private project context is hard to separate from reusable system structure;
- multiple humans and agents need the same working reality without sharing one
  fragile prompt.

AICOS exists to provide a durable context/control-plane for that work.

It separates:

- stable project truth from daily working state;
- evidence from promoted knowledge;
- agent rules from project truth;
- source/runtime repositories from context/control-plane records;
- project-facing roles from internal AICOS actor classes.

## What AICOS Is

AICOS is a multi-human, multi-agent, multi-project work-brain.

It is not a personal memory app and it is not a replacement for your project
repo. Your project repo remains the authority for code, tests, scripts,
schemas, generated artifacts, and runtime behavior. AICOS stores the compact
context that agents and humans need in order to work on that repo coherently.

At the current stage, AICOS is Markdown-first with deterministic contracts and a
thin local CLI. A local MCP bridge provides bounded context access and semantic
writeback for agents.

## The Core Model

AICOS organizes project knowledge by state:

- `canonical`: approved or stable truth, such as project profile,
  architecture, requirements, decisions, and working rules.
- `working`: current reality, such as current state, direction, risks, open
  questions, open items, and current handoff.
- `evidence`: raw or reviewed inputs, such as source inventories, research,
  import notes, test evidence, and candidate updates.

The usual promotion path is:

```text
evidence -> working -> canonical
```

AICOS also separates operating surfaces:

- `brain/`: durable knowledge and project reality.
- `agent-repo/`: actor rules, startup cards, rule cards, task packets, and
  operational lanes.
- `packages/aicos-kernel/`: deterministic schemas, contracts, validators, and
  CLI behavior.
- `integrations/`: runtime bindings such as the local MCP bridge.
- `serving/`: generated or served context surfaces such as capsules, query,
  branch, feedback, and promotion review overviews.
- `backend/`: local substrate and indexing support, not the authority for truth.

## What Problem It Solves

AICOS is designed for teams that want AI agents to work across real projects
without losing context or crossing boundaries.

It helps answer:

- What is the current truth of this project?
- What is stable, what is working, and what is only evidence?
- Which context should a new CEO, product owner, CTO, dev, reviewer, or worker
  agent read first?
- What task is selected, and what files or artifacts are actually relevant?
- Where should agents write checkpoints, handoffs, risks, or open questions?
- How can a project be imported into an agent-readable context layer without
  copying the entire source repo?

## Current Public Surface

This staging repo currently includes:

- `packages/aicos-kernel/`: schemas, contracts, validators, and thin CLI code.
- `integrations/local-mcp-bridge/`: local MCP stdio bridge scaffold.
- `integrations/mcp-daemon/`: optional HTTP daemon, env example, LAN helper,
  and local health monitor for staging review.
- `agent-repo/`: internal actor rules and onboarding model for review.
- `templates/`: reusable project onboarding and import templates.
- `serving/`: public overviews of serving surfaces.
- `backend/`: local substrate scaffold.
- `examples/sample-project/`: a synthetic project template rewritten from a
  private real-project pattern.
- `docs/guides/`: public setup and role-aware onboarding guides.
- `docs/concepts/`: conceptual docs for authority split and task packets.

## What Works Today

You can currently:

- run the local CLI help with `./aicos --help`;
- inspect the AICOS kernel contracts and schemas;
- inspect local MCP bridge code and install notes;
- copy the sample project structure to start your own AICOS-managed project;
- use the sample project to understand canonical, working, import-kit,
  workstream, delivery-surface, and task-packet lanes;
- use the public docs to understand role-aware onboarding and project authority
  boundaries.

## What Is Still Early

AICOS is not yet a polished product.

Current limitations:

- no packaged installer yet;
- no public release tag yet;
- local MCP setup still expects manual client configuration;
- role-aware query tools are still design-stage;
- A2-Serve is not active as a full service runtime;
- retrieval/index freshness is still a future hardening area;
- public examples are synthetic and intentionally small.

## Direction

AICOS is moving toward:

- a repeatable project import flow;
- role-aware context/query surfaces;
- cleaner public examples;
- better MCP read/write tools;
- stronger status-item, handoff, and task-packet workflows;
- optional retrieval/index backends;
- future service agents that improve context quality, promotion decisions,
  branch comparisons, and project health signals.

The long-term direction is a local-first operating layer where humans and many
agents can work across many projects while preserving shared reality and clear
authority boundaries.

## Start Here

- [Install AICOS](INSTALL.md)
- [Getting Started](GETTING_STARTED.md)
- [MCP Daemon Local Setup](docs/guides/mcp-daemon-local-setup.md)
- [Create Your Own AICOS Project](docs/guides/create-your-project.md)
- [Sample Research Digest](examples/sample-project/README.md)
- [Role-Aware Project Onboarding](docs/guides/role-aware-project-onboarding.md)

## Role Terminology

AICOS-internal actor classes such as A1 and A2 are not the same as external
project roles such as CEO, product owner, CTO, fullstack dev, reviewer, or
worker.

Use internal actor classes for AICOS access/writeback rules. Use project-facing
roles to decide which project context an agent should read.

## Safety

Do not put private project context, handoffs, logs, secrets, `.env` files, local
tool residue, or generated output bulk in this public repo.

If an example is derived from a real project, rewrite it into a synthetic sample
with fake names, fake paths, fake source inputs, and no operational history.

## License

Apache License 2.0 for now. The project may reconsider MIT later.

## Current Status

This is still a staging repo. Before public release, the project needs clean
install verification, maintainer review, and a final pass over public-facing
terminology.
