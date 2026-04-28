# AICOS Problem Framing And Build-vs-Buy Memo

Status: research / co-founder framing  
Date: 2026-04-28  
Scope: `projects/aicos`

## Why this note exists

Before making more architecture decisions, AICOS needs a stable answer to:

1. what painpoints AICOS is actually solving;
2. who AICOS serves directly and indirectly;
3. what level of help AICOS is supposed to provide;
4. whether AICOS should keep building large parts of the stack itself or reuse
   existing products/substrates more aggressively.

This note is meant to become a decision anchor for later architecture passes.

## Core Product Judgment

AICOS is **not** primarily a generic memory product.

AICOS is **not** primarily a search engine.

AICOS is **not** primarily a universal company wiki.

AICOS is a **multi-agent project context control-plane**.

Its core job is to stop context, continuity, authority, and coordination from
breaking down when many agents and humans work across multiple projects.

## The Actual Painpoints

The core problem is not "we lack knowledge storage".

The core problem is **operational context breakdown** in multi-agent work.

That breakdown appears in six recurring ways:

### 1. Current truth ambiguity

Teams and agents cannot reliably tell:

- what the current truth is;
- which note is active vs historical;
- which file is authority vs evidence;
- which context belongs to current work vs archived reference.

### 2. Ownership ambiguity

The team cannot reliably tell:

- which agent is working on what;
- which lane is active;
- which worktree or branch is occupied;
- whether a task or lane has a live owner;
- whether a handoff is real or implied.

### 3. Startup/read overload

New agents or threads often:

- read too much;
- read the wrong things;
- miss the critical rule or current state;
- fail to distinguish overview from authority.

### 4. Writeback ambiguity

Agents often do not know:

- what should be written back;
- where it should be written;
- whether the update is handoff, status, checkpoint, feedback, evidence, or
  artifact reference;
- whether it belongs in AICOS or the external project repo.

### 5. Continuity breakdown across agents and threads

When work moves from one agent or thread to another, the team often loses:

- why the current state exists;
- who changed what;
- what the next agent should trust;
- what the current active lane actually is.

### 6. Search without authority is insufficient

Search can return documents, but that alone does not answer:

- which result is authoritative;
- which result is current;
- which result is only evidence/history;
- which adjacent objects matter for the active lane.

## Who AICOS Serves

### Direct users

1. **A1 agents**
   - coding, content, design, research, ops, review workers
2. **A2 agents**
   - system maintainers, architecture/policy/runtime maintainers
3. **Human operators**
   - founders, leads, managers, coordinators, project owners

### Indirect beneficiaries

1. **Projects**
   - better continuity, clearer ownership, cleaner startup/handoff
2. **Company / team**
   - lower coordination cost across many projects and agent families
3. **End users / customers**
   - delivery quality improves because fewer things are lost in coordination

## What AICOS Helps With

### Directly, for A1/A2

AICOS helps agents:

- know what to read first;
- know what is authoritative;
- know where to write updates;
- know who is doing what;
- avoid stepping on each other;
- preserve continuity cleanly.

### Indirectly, for the human/team/business

AICOS helps by:

- lowering coordination cost;
- reducing context loss;
- reducing onboarding time for new agents;
- making many concurrent lanes more manageable;
- making organizational memory operational rather than decorative.

## What Level Of Help AICOS Should Provide

### Level 1 — context control-plane

Must have:

- startup/orientation;
- current state and handoff;
- status and open-item surfaces;
- authority boundaries;
- query/search;
- structured writeback.

### Level 2 — coordination operating system

Important medium-term:

- active lanes and worktree occupancy;
- agent identity and ownership;
- feedback and closure discipline;
- project health;
- import/intake behavior.

### Level 3 — organization intelligence layer

Future, but not the immediate center:

- cross-project intelligence;
- company/workspace memory;
- pattern learning;
- policy promotion;
- architecture review loops.

## Important Future Expansion To Keep In View

Short term, AICOS does **not** need to manage all company knowledge.

Long term, however, a stronger statement is likely true:

> If company knowledge is required for AI agents to work correctly and safely,
> AICOS or its substrate boundary must eventually be able to manage
> company knowledge for AI agents.

This does **not** mean AICOS should immediately become a universal company
knowledge product.

It means the architecture should not block the future path where
company/workspace-level agent-relevant knowledge is treated as first-class
context.

## Landscape Review: Nearby Products And What They Solve

This section is based on currently-visible official material.

### GBrain

Official source:
- [GBrain GitHub](https://github.com/garrytan/gbrain)
- [GBRAIN_V0](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_V0.md)

What GBrain solves well:

- persistent AI-agent memory;
- strong retrieval substrate;
- direct / keyword / hybrid query discipline;
- MCP access;
- skills as retrieval/operating behavior;
- maintenance loops and recurring jobs;
- page/link oriented knowledge organization.

Why it matters to AICOS:

- GBrain is strong exactly where AICOS is currently at risk of rebuilding too
  much substrate.

Where it is weaker relative to AICOS needs:

- project control-plane semantics;
- authority distinction between truth/working/evidence/history;
- multi-agent lane/worktree coordination;
- project intake/import discipline.

### Memobase

Official source:
- [Memobase](https://memobase.ai/)

What it solves well:

- persistent long-term memory for agents;
- MCP-native access;
- semantic vector search;
- per-user isolation;
- audit-ready, timestamped structured metadata;
- shared memory for multiple MCP-compatible agents.

Why it matters to AICOS:

- shows that "shared agent memory via MCP" is already a real category.

Why it is not enough for AICOS:

- it is a memory product first;
- it does not naturally give AICOS project-control semantics, lane/worktree
  contracts, or authority modeling.

### Membase

Official source:
- [Membase](https://membase.so/)

What it solves well:

- memory hub for agents;
- many tool/app integrations;
- context sync across agents and apps;
- "second brain" positioning.

Why it matters to AICOS:

- validates demand for cross-agent memory and context sync.

Why it is not enough for AICOS:

- product emphasis is broad memory aggregation and personal/team context sync;
- AICOS still needs stronger project/control-plane semantics and explicit
  authority boundaries.

### GitAgent

Official source:
- [GitAgent GitHub](https://github.com/open-gitagent/gitagent)

What it solves well:

- git-native agent identity, rules, memory, tools, and skills;
- compliance and audit logging;
- versionable agent framework conventions.

Why it matters to AICOS:

- validates the importance of auditability, identity, and versioned agent
  operating surfaces.

Why it is not enough for AICOS:

- it is closer to an agent framework and git-native operating standard than to
  a multi-project context control-plane;
- it does not directly answer AICOS's project authority / working-state /
  handoff/control-plane problem.

### Other nearby patterns

There are also adjacent categories, such as:

- file-based agent context systems;
- research systems for git-like context control;
- hierarchical memory for multi-agent systems.

These validate the problem space, but they do not obviously remove the need for
AICOS's project-control semantics.

## Co-Founder Critique: Why Build AICOS At All?

The hard critique is valid:

If GBrain, Memobase, Membase, GitAgent, and similar products already provide
memory, MCP, search, jobs, and audit surfaces, why keep building AICOS?

The answer is:

Because those products are strongest at **memory, retrieval, and agent
substrate**, while AICOS is strongest where the others are not yet opinionated
enough:

- project authority boundaries;
- working/evidence/history separation;
- lane/worktree/ownership semantics;
- startup/handoff/checkpoint/status/feedback discipline;
- project intake/import flows;
- multi-agent control-plane behavior.

## Build-Only-What-We-Must Principle

As a co-founder, the principle should be:

1. build only what is actually part of AICOS differentiation;
2. reuse substrate aggressively where third parties are already better;
3. keep long-term independence in the parts that define product identity and
   control-plane power.

Translated into practice:

### AICOS should own

- authority model;
- object semantics;
- MCP read/write contracts;
- startup/handoff/status/checkpoint/feedback model;
- actor/lane/worktree coordination semantics;
- project/company/workspace control-plane shape;
- intake/import/governance behavior.

### AICOS should strongly consider reusing / wrapping / forking from partners

- retrieval/search substrate;
- chunking;
- direct/keyword/hybrid mode system;
- doctor/verify/health loops;
- maintenance jobs;
- some MCP serving/runtime helpers.

## Should We Abandon Most Of AICOS And Just Use GBrain?

Current judgment: **no**.

That would likely collapse AICOS into a memory/retrieval product shape and lose
too much of its real product identity.

## Should We Keep Building AICOS Exactly As We Are Now?

Current judgment: **also no**.

That risks rebuilding too much substrate and creates a custom platform burden
that is not where AICOS is most differentiated.

## Recommended Direction

The recommended strategy is:

> AICOS should remain the semantic and control-plane layer, while more of the
> retrieval/runtime substrate should be reduced, reused, wrapped, or migrated
> toward a more GBrain-derived path where that increases leverage without
> weakening authority.

This is not a complete product pivot.

It is a strategic narrowing of what AICOS should own directly.

## What This Means For Future Architecture Decisions

Before approving new AICOS runtime/search/substrate work, ask:

1. is this part of AICOS differentiation?
2. is this already solved better by GBrain or a similar substrate?
3. if we build it ourselves, are we gaining long-term control or just adding
   maintenance burden?
4. does this strengthen AICOS as a control-plane, or drift it toward a generic
   knowledge/memory product?

## Final Judgment

The strongest product framing is:

> AICOS is a multi-agent project context control-plane that preserves truth,
> continuity, authority, and coordination across human and AI work.

That framing justifies why AICOS should exist.

It also justifies why AICOS should **not** insist on owning every layer of
memory, search, or runtime implementation.
