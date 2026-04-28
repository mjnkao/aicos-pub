# AICOS Market Landscape And Substrate Comparison

Status: research / co-founder landscape memo  
Date: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Preserve the strategic critique around:

- what AICOS is actually solving;
- which nearby products solve adjacent painpoints;
- why AICOS should continue to exist;
- where AICOS should build, buy, reuse, wrap, or fork.

This note extends the product framing and build-vs-buy memo with a more
explicit market/substrate comparison.

## Core Reminder

AICOS is best framed as a **multi-agent project context control-plane**.

It is not primarily:

- a generic memory product;
- a generic search engine;
- a universal company wiki;
- or a raw agent orchestration framework.

Its core job is to stop **operational context breakdown** in multi-agent project
work.

## Market Observation

The market is **not empty**.

There are already multiple products and frameworks solving meaningful parts of
the broader problem:

- memory for AI agents;
- long-term context persistence;
- shared context via MCP;
- retrieval and search substrate;
- audit and agent identity;
- orchestration and persistence;
- domain-specific context governance.

What is still relatively under-solved is the **combined package** AICOS cares
about:

- project control-plane semantics;
- truth / working / evidence / history separation;
- startup/handoff/checkpoint/status discipline;
- multi-agent lane/worktree ownership;
- project/runtime authority boundaries.

## Reference Systems Reviewed

### 1. GBrain

Sources:

- [GBrain GitHub](https://github.com/garrytan/gbrain)
- [GBRAIN_V0](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_V0.md)

Strongest at:

- agent memory and retrieval substrate;
- direct / keyword / hybrid query discipline;
- MCP serving;
- skills as operational behavior;
- maintenance jobs;
- page/link knowledge organization.

What it validates:

- the need for a powerful shared retrieval substrate;
- the usefulness of MCP-native memory/search;
- the value of skills/jobs over ad hoc prompting.

What it does not fully solve for AICOS:

- project control-plane semantics;
- authority separation between truth/working/evidence/history;
- multi-agent lane/worktree coordination;
- project intake/import workflow.

### 2. Memobase

Source:

- [Memobase](https://memobase.ai/)

Strongest at:

- persistent long-term memory for AI agents;
- MCP-native access;
- semantic retrieval;
- per-user isolation;
- audit-ready structured memory records.

What it validates:

- a real demand for production-grade shared memory for agents;
- memory plus traceability as an actual product category.

What it does not fully solve for AICOS:

- project-specific authority model;
- control-plane semantics for ongoing multi-agent project execution;
- startup/handoff/lane/worktree coordination.

### 3. Membase

Source:

- [Membase](https://membase.so/)
- [Membase docs](https://docs.membase.so/)

Strongest at:

- cross-agent memory hub;
- broad context ingestion from tools/apps;
- "second brain" positioning for many agents.

What it validates:

- cross-agent memory sync is valuable;
- users want one context layer across tools and agents.

What it does not fully solve for AICOS:

- authoritative project operating surfaces;
- explicit working/evidence/history boundaries;
- strong control-plane write semantics.

### 4. GitAgent

Source:

- [GitAgent GitHub](https://github.com/open-gitagent/gitagent)

Strongest at:

- git-native agent identity/rules/memory;
- compliance and audit logging;
- versioned agent framework structure.

What it validates:

- identity, audit, and versioned operating surfaces matter;
- agent systems benefit from file-backed, reviewable structure.

What it does not fully solve for AICOS:

- multi-project context control-plane;
- project authority semantics;
- structured status/handoff/checkpoint model;
- retrieval/search substrate quality by itself.

### 5. LangGraph / LangMem

Sources:

- [LangGraph persistence docs](https://docs.langchain.com/oss/javascript/langgraph/persistence)
- [LangGraph memory overview](https://docs.langchain.com/oss/javascript/langgraph/memory)
- [LangMem docs](https://langchain-ai.github.io/langmem/)

Strongest at:

- long-running agent orchestration;
- checkpointed graph state;
- human-in-the-loop flow control;
- long-term memory tools and storage interfaces;
- custom stateful agent runtime patterns.

What it validates:

- persistence, threads, checkpoints, and memory are mainstream agent concerns;
- state and memory are central to production agent workflows.

What it does not fully solve for AICOS:

- AICOS-style project/control-plane semantics;
- strong truth vs evidence vs history boundaries for project context;
- cross-agent project operating rules as a product layer.

### 6. CrewAI

Source:

- [CrewAI memory docs](https://docs.crewai.com/en/concepts/memory)

Strongest at:

- multi-agent workflow framework;
- unified memory abstraction;
- orchestration-oriented agent building blocks.

What it validates:

- memory is integral to multi-agent execution;
- orchestration frameworks are converging on built-in memory as a baseline.

What it does not fully solve for AICOS:

- AICOS-specific project authority and working-state semantics;
- organization/project control-plane boundaries;
- cross-project truth/working/evidence separation.

### 7. Mem0

Source:

- [Mem0 docs](https://docs.mem0.ai/) (or official product/docs surface)

Strongest at:

- agent memory productization;
- relevance-driven memory retrieval;
- personalization and long-term memory reuse across sessions and tasks.

What it validates:

- memory as a dedicated product category is real;
- teams are willing to adopt external memory systems rather than build them all
  themselves.

What it does not fully solve for AICOS:

- project control-plane semantics;
- structured multi-agent continuity surfaces;
- project/runtime authority distinctions.

### 8. Atlan

Sources:

- [Atlan Context Agents Studio](https://docs.atlan.com/product/capabilities/governance/context-agents-studio)
- [Atlan AI Governance](https://docs.atlan.com/product/capabilities/governance/ai-governance)

Strongest at:

- context/governance layer for AI over enterprise data;
- metadata-driven context;
- domain-specific active context for agents;
- governance and traceability over AI usage.

What it validates:

- "context layer for AI" is a serious category;
- governance + context can be a product moat;
- context is not only memory, but also trusted metadata and current usage
  signals.

What it does not fully solve for AICOS:

- it is much more data-platform-centric;
- it does not directly target multi-agent project execution control-plane for
  arbitrary engineering/content/design/research work.

## Comparative Table

| System | What it solves best | What it proves | Where it falls short for AICOS | Implication for AICOS |
| --- | --- | --- | --- | --- |
| GBrain | Retrieval substrate, MCP memory/search, jobs, skills, page/link memory | Shared agent brain with strong search discipline is valuable | Lacks AICOS-specific control-plane semantics and authority model | Strong substrate candidate; not enough as the whole product |
| Memobase | Production memory + MCP + audit-ready memory | Shared memory + traceability is a real product need | Does not provide project operating semantics | Memory layer candidate, not control-plane replacement |
| Membase | Cross-agent memory hub and broad integrations | Users want one context hub across tools and agents | Strong memory product shape, weak project-control semantics | Good signal for demand; not enough as AICOS itself |
| GitAgent | Git-native agent identity, rules, audit | Identity/audit/versioned agent ops matter | Not a complete multi-project context control-plane | Useful pattern source for identity/audit discipline |
| LangGraph/LangMem | Stateful orchestration, persistence, memory tools | Threads/checkpoints/memory are foundational | Not opinionated enough about AICOS project/control semantics | Good runtime substrate ideas; not product replacement |
| CrewAI | Multi-agent workflow + unified memory | Orchestration frameworks now assume memory | Memory/orchestration != context control-plane | Supports AICOS thesis, but doesn't replace it |
| Mem0 | Long-term memory productization | Teams will adopt external memory systems | Memory product alone does not solve authority/continuity semantics | Good buy/reuse signal for memory substrate |
| Atlan | Context/governance layer over enterprise data | Context + governance can be a product moat | Domain focus is data/metadata, not general project operations | Strong validation for context/governance thinking |

## Synthesis

### The market does have real solutions

So AICOS is **not** solving a fake problem.

The market clearly validates demand for:

- persistent agent memory;
- MCP-native context systems;
- governance and auditability;
- stateful long-running agent workflows;
- context layers with operational value.

### But AICOS still has a real wedge

The wedge is not "memory exists".

The wedge is:

- context with authority;
- continuity with operating semantics;
- coordination with ownership and lane boundaries;
- project-aware control-plane behavior.

That is still not a solved commodity in the general case.

## Build vs Buy vs Reuse

### Build

AICOS should build and own:

- project/company/workspace control-plane semantics;
- authority boundaries;
- startup/handoff/checkpoint/status/feedback structure;
- agent identity + lane/worktree rules;
- intake/import/governance model.

### Buy / reuse / wrap / fork

AICOS should strongly consider buying, reusing, wrapping, or forking for:

- retrieval/search substrate;
- chunking;
- memory storage/retrieval plumbing;
- health/doctor/verify loops;
- maintenance jobs;
- some MCP/search serving behavior.

### Do not build if it is only substrate duplication

If a new AICOS component is mainly:

- memory plumbing;
- generic retrieval;
- generic embedding/index lifecycle;
- generic orchestration persistence;
- generic MCP substrate behavior,

then the default question should be:

> why are we building this instead of reusing a proven substrate?

## Why AICOS Should Still Exist

AICOS should continue to exist because it is solving the product layer above
memory/search:

- how project context is organized;
- how authority is defined;
- how continuity survives across agents;
- how updates are structured and governed;
- how context becomes operational rather than just searchable.

## Why AICOS Should Not Keep Owning Every Layer

If AICOS keeps building every layer itself, it risks:

- becoming a custom memory/search/orchestration platform by accident;
- increasing maintenance burden;
- slowing down work on the true differentiated layer;
- losing strategic focus.

## Long-Term Note: Company Knowledge For AI Agents

This is worth preserving explicitly:

- short term, AICOS should not overexpand into "all company knowledge";
- long term, if AI agents need company/workspace knowledge to work correctly,
  the AICOS architecture should leave room to support that in a bounded,
  control-plane-aware way.

This future path should remain open without forcing AICOS to become a universal
knowledge platform immediately.

## Final Judgment

The market does solve adjacent pieces.

That is exactly why AICOS should be disciplined:

- build the control-plane layer that others do not solve well;
- reuse the substrate layers that others already solve well;
- keep enough ownership to remain strategically independent where it matters.

The right question for future decisions is no longer:

- "can AICOS build this?"

It is:

- "is this where AICOS must own the stack, or is this substrate we should stop
  rebuilding?"
