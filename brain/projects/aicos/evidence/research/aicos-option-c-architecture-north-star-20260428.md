# AICOS Option C Architecture North Star

Status: architecture north-star  
Date: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Define the target architecture for AICOS if it continues on the "Option C"
direction:

> AICOS as a semantic/control-plane layer on top of interchangeable substrate
> providers, so it can serve different companies, different scales, and future
> shared human+AI operational dashboards without turning into a PM tool or a
> generic memory product.

This note is not an implementation plan for one sprint. It is the direction
that future architecture and migration passes should protect.

## Product Position

AICOS is a **multi-agent project context control-plane**.

It is not defined by:

- one memory engine;
- one search engine;
- one graph engine;
- one MCP runtime;
- one UI;
- one PM tool.

AICOS is defined by:

- authority boundaries;
- continuity and handoff semantics;
- startup/read/write contracts;
- multi-agent ownership and coordination rules;
- project/workspace/company context semantics.

## Key Product Requirement

The architecture must support all of the following:

1. humans and AI agents working across multiple projects;
2. multiple agent families (`codex`, `claude-code`, `antigravity`, others);
3. coding and non-code projects;
4. long-lived context that survives agent, machine, and thread changes;
5. human-facing collaboration through shared dashboard/task tools such as
   Plane/ClickUp-like systems;
6. substrate variation depending on company size and needs.

## Architectural Principle

### AICOS core owns semantics

AICOS itself should own:

- context authority model;
- object taxonomy;
- read/write contracts;
- continuity semantics;
- coordination semantics;
- startup and handoff logic.

### Providers own implementation of replaceable substrate concerns

External or pluggable providers should be allowed to own:

- retrieval/search runtime;
- memory store implementation;
- graph/relation engine;
- jobs/maintenance execution;
- auth/audit sinks;
- connectors and ingestion paths.

## North-Star Layer Model

## Layer 1 — Semantic Core

This is the hardest boundary and should remain the most stable part of AICOS.

### Responsibilities

1. **Authority model**
   - truth / working / evidence / history
   - project/runtime authority split
   - source precedence

2. **Object model**
   - company
   - workspace
   - project
   - workstream
   - task packet
   - status item
   - checkpoint
   - handoff
   - feedback
   - artifact ref
   - project health
   - startup bundle

3. **Coordination semantics**
   - actor classification boundary
   - actor role
   - functional role
   - service role
   - agent family
   - agent instance id
   - work type
   - work lane
   - execution context
   - worktree/branch occupancy semantics

### Actor-model rule

AICOS should distinguish clearly between:

- **AICOS-internal actor classes** used only for maintaining AICOS itself
  (for example `A2-Core-R`, `A2-Core-C`, and AICOS-facing `A1`);
- **project-facing functional roles** that may vary by company, workspace, or
  project (for example CTO, coder, marketer, reviewer, researcher);
- **service roles** that describe the operational relationship to AICOS (for
  example internal actor vs external actor).

Design rule:

- `A1` / `A2` is not the universal role model for every project using AICOS.
- For projects other than AICOS itself, outside agents should normally be
  treated by AICOS as external work actors using AICOS as a context/control
  layer, while their local project-specific role taxonomy stays project-owned.
- Only agents working *inside* the AICOS project itself should need to reason
  explicitly about `A1` / `A2` as part of the product's own maintenance model.

4. **Contract semantics**
   - semantic reads
   - semantic writes
   - validation invariants
   - continuity/closure rules

### Design rule

This layer must not depend on a specific substrate like GBrain, PG, Graphiti,
Mem0, or Onyx.

## Layer 2 — AICOS Runtime Services

This is the assembly/orchestration layer that turns semantic core rules into
operational behavior.

### Responsibilities

- startup bundle assembly
- handoff serving
- status serving
- project health serving
- semantic write serving
- audit correlation
- feedback loop logic
- coordination policy enforcement

### Design rule

This layer may depend on provider interfaces, but should not hard-code one
substrate as product identity.

## Layer 3 — Provider Layer

This layer makes AICOS adaptable across company sizes and implementation
choices.

### Provider classes

1. **Retrieval Provider**
   - markdown-direct
   - GBrain
   - PG hybrid
   - enterprise search systems

2. **Memory / Context Store Provider**
   - file-backed markdown
   - GBrain pages/store
   - external memory layers

3. **Relation / Graph Provider**
   - none / Trace Refs only
   - derived relation index
   - graph memory system

4. **Jobs / Maintenance Provider**
   - shell/cron
   - GBrain-style maintenance jobs
   - cloud scheduler

5. **Auth / Audit Provider**
   - local token auth
   - labeled tokens
   - SSO / RBAC / enterprise audit sink

6. **Connector / Ingestion Provider**
   - repos
   - PM tools
   - docs/chat systems
   - enterprise apps

### Design rule

Providers are replaceable implementation paths, not product identity.

## Layer 4 — Deployment Profiles

AICOS should support clearly-defined profiles rather than one implicit stack.

### Profile A — solo

For one person or very small personal use:

- markdown truth
- local MCP
- bounded query
- minimal auth
- no heavy graph

### Profile B — small-team (5-20)

For a small technical team with shared AICOS usage:

- shared context/control-plane
- HTTP MCP
- stronger audit than solo mode
- long-lived context across many agent families
- lightweight shared human+AI coordination

Typical substrate choice today:

- markdown truth
- GBrain sync/import
- PG hybrid retrieval
- HTTP MCP
- token auth
- background embeddings / freshness checks

### Profile C — company-100

Target for a growing company where many humans and AI agents work across
multiple projects:

- shared daemon/service
- stronger auth/audit
- profile-specific provider stack
- structured task/worker coordination
- PM/dashboard integration path
- long-term context shared across humans and many agent families

### Profile D — enterprise

Future:

- permission-aware org memory
- enterprise connectors
- stronger governance/audit
- larger-scale deployment and compliance posture

### Design rule

AICOS core stays stable; profiles swap provider bundles and operational policy.
Substrate choices such as `gbrain-substrate` are implementation bundles inside
profiles, not the profile names themselves.

## Layer 5 — Company / Workspace / Project Packs

AICOS should eventually support pack-like adaptation without product forks.

### Company pack

- company policy
- approved systems
- naming and governance rules
- security/compliance constraints

### Workspace pack

- team conventions
- context precedence tweaks
- connector scope
- operational defaults

### Project pack

- startup ladder
- project workstreams
- project artifact model
- import/onboarding specifics

### Design rule

Use packs to adapt AICOS to real environments without changing core semantics.

## Human + AI Shared Dashboard Direction

AICOS should support future human-facing shared work surfaces, but should not
become a PM tool clone.

### Principle

- AICOS = context/control-plane and AI-native operational semantics
- Dashboard / PM tool = visible work surface for humans and agents

### Meaning

AICOS should integrate well with tools like Plane or ClickUp, but those tools
should be treated as collaboration windows, not as the full source of AICOS
truth.

### What AICOS must provide first

Before a serious dashboard integration, AICOS needs:

1. clearer coworker/task semantics;
2. operational read surfaces for active work and ownership;
3. explicit sync/authority rules between AICOS and PM tools.

## Near-Term Direction

The next architecture passes should **not** jump directly to building a
dashboard.

They should:

1. preserve and sharpen semantic core boundaries;
2. inventory current implementation into core vs runtime vs providers;
3. reduce custom substrate growth;
4. define the first provider boundaries cleanly;
5. formalize the current stack as the first real substrate bundle for the
   `small-team` profile (currently GBrain + PG hybrid + HTTP MCP + team auth);
6. define the future `company-100` profile deliberately.

## What This Changes Relative To Today

### Today

AICOS already behaves partially like a concrete substrate bundle inside the
`small-team` profile (currently GBrain + PG hybrid + HTTP MCP + team auth), but
its semantic core, runtime serving, provider concerns, and deployment
assumptions are still mixed together in places.

### Target

AICOS should become easier to reason about as:

- semantic core
- runtime services
- providers
- profiles
- packs

instead of one growing implementation stack.

## Main Risks

1. **Over-abstraction too early**
   - building generic provider frameworks before enough real variation exists

2. **Semantic drift**
   - weakening AICOS authority/continuity model while modularizing

3. **Product drift**
   - becoming a PM tool clone or a generic memory platform

4. **Migration drag**
   - destabilizing the currently-usable stack with a large rewrite

## Anti-Drift Rules

When evaluating any future feature, ask:

1. does this strengthen AICOS as a context control-plane?
2. is this semantic core or replaceable substrate?
3. should AICOS own this directly, or only integrate it?
4. does this make future human+AI shared work easier without turning AICOS into
   a generic task tracker?

## Final Judgment

The right long-term architecture for AICOS is:

> a stable semantic/control-plane core, served by runtime services, backed by
> interchangeable provider layers, deployed through clear profiles, and adapted
> through company/workspace/project packs.

This direction preserves what is unique about AICOS while keeping the path open
to reuse strong substrates such as GBrain and future organizational-memory
systems.
