# AICOS Architecture Overview

Status: latest working overview
Updated: 2026-04-21
Scope: AICOS as a workspace/project context intelligence layer

## Executive Summary

AICOS is a workspace/project context intelligence layer for humans, work
agents, and service agents.

Its job is not only to store project truth. Its job is to help agents know:

- what context to read;
- where to find it;
- which source is authoritative;
- which state, service class, project role, project, workstream, or task the
  context belongs to;
- how much context is enough for the current work;
- how to write back meaningful state so the next agent starts smarter.

AICOS should make a project easier to re-enter over time. Each checkpoint,
handoff, decision, feedback item, status update, and context query should help
future agents load less irrelevant material and find the right context faster.

The current implementation has established the first foundation: repo
restructuring, AICOS self-brain, A1/A2 service-boundary separation,
packet-first onboarding, local MCP read/write surfaces, handoff/status lanes,
and markdown-direct bounded context query. The next architectural step is to
make context intelligence itself first-class: context indexing, routing, query
quality, freshness, and learning loops for the human-like roles that use AICOS
inside each project.

## Why This Matters

Agent work fails less often because the model is weak and more often because the
agent receives the wrong project reality.

Common failure modes:

- the agent reads stale docs and treats them as current;
- the agent misses an active workstream because startup context is too narrow;
- the agent reads too much and loses the actual task;
- task status, handoff, open questions, risks, and decisions are scattered;
- search returns text matches without authority, freshness, or role relevance;
- useful lessons remain buried in prose instead of improving future context
  serving.

AICOS exists to solve these problems as an operating layer around project work.
It should let humans and agents share a current project reality without forcing
every agent to reread the whole repository at every startup.

## Product Definition

AICOS should be understood as:

> A workspace/project context intelligence layer that provides authoritative
> project reality, project-role-aware context serving, semantic writeback, and
> learning loops for multi-agent work.

AICOS is not:

- a replacement for a project code/runtime repository;
- a generic task tracker;
- a full agent orchestration runtime;
- the internal memory manager for Codex, Claude Code, OpenClaw, or future
  external co-workers;
- a vector search product by itself;
- a personal-brain clone.

AICOS provides what should be known, where it comes from, how current it is, how
to load more, and where meaningful updates should be written. External agents
remain responsible for their own internal context window and execution behavior.

## Design Sources Consolidated

This overview consolidates the current direction from:

- `DSC-26040` — AI-native co-worker architecture;
- `DSC-26038` — company/team-native AICOS architecture leveraging GBrain;
- `ARC-26071` — AICOS Kernel, Service Skills, GBrain, and GStack split;
- `CTX-26153` — context loading, access, and rule delivery model;
- `ARC-26291` — MCP expansion for scalable multi-project work;
- `ARC-26301` — workstream index surface;
- `FRM-26308` — structured feedback framework;
- `GOV-26311` — rule and policy promotion candidate mechanism;
- current AICOS self-brain under `brain/projects/aicos/working/`;
- current MCP bridge contract and implementation status.

The older design docs already point in the right direction: AICOS as a
company/workspace intelligence layer with canonical, working, evidence,
execution, branch, capsule, and serving layers. The current update sharpens one
point: search and context serving are not optional backend details. They are
core product capability.

## Role Model

AICOS needs two role dimensions, and they must not be collapsed.

### 1. Service Boundary Class

`A1` and `A2` describe the actor's relationship to AICOS as a service.

- `A1`: actors using AICOS to do company/workspace/project work.
- `A2`: actors maintaining, operating, or improving AICOS itself.

This boundary answers: is the actor using AICOS, or changing AICOS?

### 2. Project Or Company Role

Project/company roles describe what human-like responsibility the actor has in
the current project.

Examples for coding projects:

- Product Owner;
- CTO;
- Tech Lead;
- Architect;
- Fullstack Developer;
- Backend Developer;
- QA;
- Designer;
- Reviewer.

Examples for non-code or mixed projects:

- Content Writer;
- Editor;
- Researcher;
- Analyst;
- Operations Manager;
- Strategy Lead;
- Brand Designer;
- Project Manager.

These roles can be held by humans or agents. An A1 agent on one project may act
as a QA, while another A1 acts as a content writer or product analyst. An A2
agent maintaining AICOS may act as an AICOS architect, kernel engineer,
retrieval engineer, service designer, or documentation architect.

The search and context-serving layer primarily exists to serve these
project/company roles well. It should answer different context needs for a QA,
Product Owner, Designer, CTO, or Writer instead of treating every A1 as the same
generic "work agent".

This is the main product reason for search/context serving: AICOS should help
each human-like project role get the context it needs quickly enough to work
well.

## Core Goals

### 1. Shared Reality

Humans and A1 work agents should see the same current project reality. A2
service agents should see the current AICOS service reality plus the project
friction that explains why AICOS needs to improve.

For A1-facing work, shared reality includes current state, current direction,
active workstreams, decisions, handoff, open questions, risks, status items,
task packets, and relevant artifact references.

For A2-facing work, shared reality includes AICOS architecture, contracts,
kernel/MCP state, service policies, retrieval/capsule quality, repeated A1
friction, and improvement candidates.

### 2. Role-Aware Context Loading

AICOS should serve context by both service boundary class and project/company
role.

- An A1 Product Owner needs goals, requirements, decisions, tradeoffs, and
  customer/business context.
- An A1 Tech Lead or Architect needs system boundaries, contracts, risks,
  dependencies, and implementation direction.
- An A1 Fullstack Developer needs task packet, acceptance criteria, code/runtime
  authority, current blockers, and relevant implementation context.
- An A1 QA needs expected behavior, risk areas, test targets, known issues, and
  artifact refs.
- An A1 Designer or Content Writer needs design/content brief, audience,
  constraints, examples, approvals, and review criteria.
- A2-Core needs AICOS architecture, contracts, implementation state, and service
  maintenance context.
- Future A2-Serve needs repeated friction, query quality, capsule quality, and
  context improvement signals.
- Humans need concise project reality, options, tradeoffs, and decision points.

### 3. State-Aware Context Retrieval

Context must be organized by state, not only by folder or topic.

Primary states:

- canonical: accepted truth, rules, contracts, decisions;
- working: current reality, direction, handoff, status, risks, open questions;
- evidence: source docs, research, raw inputs, historical notes;
- execution: task state, checkpoints, active work, occupancy;
- branch/experiment: reversible options and alternative project realities;
- reference/frozen: legacy material and provenance that must not override
  active direction.

### 4. Fast Context Discovery

AICOS must help agents find the right context quickly.

The search problem is not only text search. It is scoped, role-aware,
state-aware, freshness-aware, authority-aware context discovery.

The first good search system can be simple:

- structured context registry;
- markdown-direct parsing;
- lexical or FTS search;
- rule-based ranking;
- bounded results;
- explicit freshness and authority labels.

Vector search, graph traversal, GBrain, Knowledge Plane, or other retrieval
systems can be added behind adapters later. They should not become silent
authority before freshness and lineage are observable.

### 5. Semantic Writeback

Agents should not write arbitrary prose into random files.

Important updates should land in semantic lanes:

- checkpoint;
- task update;
- handoff update;
- status item update;
- artifact reference registration;
- open item/open question/risk/decision follow-up;
- future feedback records;
- future promotion candidates.

This makes future reads cheaper and future search more reliable.

### 6. Learning Loop

AICOS should become more useful for each project over time.

It should learn from:

- repeated agent confusion;
- missing context;
- context overload;
- stale search hits;
- bad routing;
- ambiguous rules;
- duplicate or conflicting docs;
- human corrections;
- task outcomes;
- repeated useful summaries or capsules.

Learning should not mean silently rewriting authority. It should mean capturing
structured signals, creating reviewable improvement candidates, and promoting
better rules, context maps, packets, or summaries after review.

## Target Architecture

## 1. Brain Layer

`brain/` holds durable project knowledge and working reality.

Primary responsibilities:

- canonical truth;
- current working state;
- evidence and provenance;
- handoff and continuity;
- status items;
- project-specific context ladders;
- service knowledge and improvement signals.

Markdown remains appropriate for this phase because it is readable,
reviewable, and easy for humans and agents to inspect. It should remain the
source of truth until a separate truth-store ADR defines when structured storage
becomes authoritative.

## 2. Agent Repo Layer

`agent-repo/` holds actor-facing operational material.

Primary responsibilities:

- A1/A2/human service-boundary cards;
- project/company role guidance and task-role metadata;
- onboarding ladders;
- rule cards;
- startup cards;
- task packets;
- task templates and backlog lanes.

It is not project truth by itself. It routes agents into the right project
context and work packet.

## 3. AICOS Kernel

`packages/aicos-kernel/` should stay deterministic and small.

Primary responsibilities:

- schemas and contracts;
- validators;
- packet rendering;
- read/write serving operations;
- safe lane mapping;
- compact mechanical operations;
- CLI adapters.

The kernel should not hardcode evolving intelligence too early. Heuristics for
retrieval quality, promotion, option generation, and service improvement should
mature first as service knowledge and reviewed policies.

## 4. MCP Context/Control Plane

MCP is the active interface for AICOS-facing context and writeback.

Current read surfaces include:

- startup bundle;
- current handoff;
- packet index;
- selected task packet;
- status items;
- workstream index;
- bounded project context query.

Current write surfaces include:

- checkpoint;
- task update;
- handoff update;
- status item update;
- artifact reference registration.

The MCP layer must remain semantic. It should not become raw file RPC. Its role
is to validate intent, map updates to lanes, and serve bounded context.

## 5. Context Intelligence Layer

This is the part that must now become more explicit.

Responsibilities:

- context registry by scope, service class, project role, state, kind,
  authority, and freshness;
- context ladders for human-readable routing;
- query surfaces that return ranked, bounded, answer-bearing results;
- workstream index for project lane routing;
- capsule/packet assembly by service class, project role, actor, and task;
- freshness checks and stale warnings;
- feedback capture when context serving fails;
- promotion candidates when repeated patterns should become rules or summaries.

This layer is the real differentiator of AICOS. It is what turns a document
repository into an agent-usable project intelligence system.

## 6. Serving / Retrieval Substrate

`serving/`, `backend/`, GBrain/PGLite, and future retrieval systems are serving
substrates, not primary truth.

Recommended approach:

1. Start with markdown-direct and structured metadata.
2. Add lexical/FTS search for local project context.
3. Add retrieval adapters for GBrain, Postgres, Knowledge Plane, vector search,
   or graph search when needed.
4. Require freshness, lineage, source refs, and authority labels before any
   retrieval backend is used as a correctness path.

Search engine complexity should be outsourced or kept simple. AICOS should own
the context policy, ranking constraints, and result packaging.

## 7. Service Intelligence

A2 service intelligence should improve AICOS itself.

Examples:

- improve query behavior;
- improve retrieval quality;
- improve capsule quality;
- detect stale or duplicate docs;
- suggest rule or policy updates;
- recommend promotions;
- compare branches or options;
- synthesize repeated friction.

This intelligence should remain reviewable. The system can suggest, summarize,
rank, and prepare candidates, but major authority changes should stay explicit.

## What Has Been Built

The current repo has working foundations:

- active root restructuring;
- AICOS self-brain under `brain/projects/aicos/`;
- A1/A2/human service-boundary separation;
- A2-Core and A1 onboarding ladders;
- packet-first startup model;
- A2 startup cards, rule cards, and task packet conventions;
- current state/current direction/implementation status;
- local MCP Phase 1 read-serving;
- local MCP Phase 2 semantic write tools;
- MCP contract `0.5`;
- status items as structured working-status lane;
- compact handoff direction and handoff compaction command;
- startup bundle with active task state, status items, and continuity signal;
- bounded markdown-direct project context query;
- workstream index read surface;
- artifact reference registration;
- Sample Project as first active external project proving the split
  between AICOS context/control authority and external code/runtime authority.

This is enough to prove the direction. It is not yet enough to support many
projects and many agents without more context intelligence.

## What Is Not Yet Complete

The following areas are not yet mature:

- full context registry with role/state/freshness metadata;
- project/company role taxonomy and metadata in task packets/context registry;
- query quality evaluation;
- retrieval freshness observability;
- structured feedback capture through MCP;
- project health digest;
- A2-Serve activation criteria;
- cross-project context propagation policy;
- formal ADR truth-store decision;
- project intake/import flow for multiple external projects;
- first-class capsule generation and quality measurement;
- broader query coverage over canonical/policy/contract/design docs.

## Search Strategy

Search is core, but AICOS should not build a complex search engine too early.

The hard part is not raw retrieval. The hard part is knowing what result is
right for the current actor, scope, state, and task.

Recommended phased strategy:

### Phase 1 — Context Registry And Lexical Search

Build or normalize a lightweight registry with:

- `scope`;
- `context_kind`;
- `state`;
- `service_class`;
- `project_role_relevance`;
- `workstream_id`;
- `authority_level`;
- `freshness`;
- `source_ref`;
- `summary`.

Use markdown-direct parsing and lexical search first. Return bounded results
with `why_matched`, authority, freshness, and source references.

### Phase 2 — FTS Or Backend Adapter

Add SQLite/Postgres FTS or a GBrain-backed adapter when local markdown-direct
search becomes too weak.

Do not expose the backend directly to agents as truth. Route it through AICOS
context policy.

### Phase 3 — Semantic/Graph Retrieval

Add vector or graph retrieval only when:

- index freshness is observable;
- source lineage is explicit;
- stale results are detectable;
- result ranking can be evaluated;
- agents can see when retrieval is uncertain.

## Learning Strategy

AICOS should learn through structured signals, not accidental prose.

Initial learning signals should include:

- query failed;
- query returned stale result;
- agent loaded too much;
- agent missed required context;
- context was correct for a generic A1 but wrong for the actor's project role;
- context ladder was ambiguous;
- task packet lacked required refs;
- handoff was too long or too thin;
- workstream routing was unclear;
- rule caused repeated confusion;
- capsule helped or failed.

These signals should feed:

- feedback digest;
- project health digest;
- context registry improvements;
- context ladder updates;
- task packet template improvements;
- rule/policy promotion candidates;
- stale/duplicate/conflict cleanup.

Learning should be explicit and reviewable. AICOS should get smarter, but it
should not silently rewrite project truth.

## Near-Term Roadmap

### Phase 1 — Stabilize Current Context Intelligence

- Make this architecture overview the current high-level entry point.
- Add or normalize a context registry for AICOS project docs.
- Ensure `aicos_query_project_context` covers current working, handoff, status,
  packets, policy, and contract docs with clear freshness labels.
- Keep startup bundles small and route deeper lookup through query/workstream
  surfaces.

### Phase 2 — Improve Search Quality Without Heavy Infrastructure

- Add lexical/FTS-backed context query.
- Add query evaluation examples for common A1/A2 startup and continuation
  questions, plus role-specific questions for Product Owner, Tech Lead,
  Developer, QA, Designer, Writer, Manager, and other common project roles.
- Track stale/closed filtering and freshness metadata consistently.
- Add structured feedback records for query failures and context overload.

### Phase 3 — Make Learning Operational

- Add `aicos_record_framework_feedback` or equivalent structured write surface.
- Add `aicos_get_feedback_digest`.
- Add `aicos_get_project_health`.
- Use repeated signals to propose context ladder, packet, and rule improvements.

### Phase 4 — Scale Across Projects

- Define project registry and cross-project context propagation policy.
- Standardize project intake/import flows.
- Require accepted workstream index for active projects with multiple lanes.
- Define A2-Serve graduation criteria.

### Phase 5 — Add Advanced Retrieval Backends

- Evaluate GBrain, Postgres/pgvector, Knowledge Plane, or other retrieval
  substrates behind an AICOS adapter.
- Require freshness and lineage before using semantic retrieval as a correctness
  path.
- Keep markdown/ADR authority explicit unless a truth-store ADR changes that.

## CTO Position

AICOS should not become a giant product that solves task management, agent
orchestration, vector search, graph memory, UI, and project governance all at
once.

The focused product is:

> context intelligence for multi-agent project work.

That means AICOS must own:

- authority and state boundaries;
- context routing;
- project-role/state-aware context serving;
- semantic writeback;
- freshness and lineage;
- learning from repeated context failures;
- reviewable promotion of better rules and summaries.

It should reuse or adapt external systems for:

- vector search;
- graph memory;
- orchestration runtime;
- project issue tracking;
- UI-heavy collaboration.

The long-term advantage is not that AICOS has the most advanced search engine.
The advantage is that AICOS knows what context is supposed to mean for a
specific project, human-like role, state, and task, and improves that mapping
over time.
