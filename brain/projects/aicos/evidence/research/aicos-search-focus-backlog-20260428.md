# AICOS Search Focus Backlog

Status: active follow-up
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Capture the concrete next work after Phases 4-7: improve A1 context search.

User signal:

> Search context của các A1 hiện nay chưa hiệu quả.

## Search Problem Statement

A1 agents need to answer these questions cheaply:

- What should I read first?
- What is the current state?
- What is ready for takeover?
- What task/lane should I work on?
- What rule applies?
- Where is the canonical source/ref?
- Why did MCP/search fail?
- What feedback should I report?

Current search can find documents, but it does not yet reliably guide A1 from
intent to the right surface/ref with low context load.

## Immediate Work Order

### Pass S1 — Eval Corpus

Create a checked-in eval corpus with 15-30 real A1/A2 retrieval questions.

Include:

- expected refs;
- expected answer shape;
- work role/lane;
- failure mode;
- priority.

### Pass S2 — Baseline Current Search

Run corpus against:

- direct read where applicable;
- markdown-direct;
- PG FTS;
- PG hybrid;
- explicit context_kinds.

Record:

- top 3 hit/miss;
- top 5 hit/miss;
- snippet usefulness;
- stale/noisy result cases;
- direct-read better cases.

### Pass S3 — Low-Risk Improvements

Only after S2:

- add query-time direct-read suggestions;
- improve intent-to-context-kind routing;
- tune source authority/freshness for A1 queries;
- improve snippets for status/handoff/task refs;
- fix false freshness/stale status signal;
- update query guide with examples from corpus.

### Pass S4 — Decide Bigger Moves

Only if eval still fails:

- relation-assisted retrieval from trace refs;
- lightweight link graph;
- GBrain page/link reuse;
- external search provider;
- LLM reranker.

Do not start here.

## High-Priority Eval Seeds

| Priority | Query | Scope | Expected target |
| --- | --- | --- | --- |
| high | "what should I do next on AICOS?" | projects/aicos | transition checklist/current status/handoff |
| high | "how do I connect as OpenClaw?" | projects/mjnclaw | project current state/install docs |
| high | "where is sample project repo source and branch?" | projects/sample-project | project profile/registry/current state |
| high | "how do I report AICOS feedback?" | projects/aicos | feedback write docs/contract |
| high | "what is A1 vs A2?" | projects/aicos | actor model/role definitions |
| high | "why does brain status say stale?" | projects/aicos | false stale status item |
| medium | "what status items are open for phase 2?" | projects/aicos | status items |
| medium | "what is current deployment profile?" | projects/aicos | Phase 4 profiles |
| medium | "what provider should search use?" | projects/aicos | Phase 3 provider sketch/Phase 5 retrieval |
| medium | "what should dashboard show?" | projects/aicos | Phase 6 coworker model |

## Guardrails

- Do not add graph/page schema before eval.
- Do not replace PG/GBrain before benchmark.
- Do not make LLM reranking required.
- Do not require agents to read more context to compensate for weak search.
- Do not let generated `serving/` become truth.

## Definition Of Better

A1 search is improving when:

- expected ref appears in top 3 for high-priority evals;
- snippets are enough to choose the next read;
- search suggests direct read surfaces when query is really about
  startup/handoff/status;
- stale/closed/noisy items do not dominate;
- A1 agents record fewer `context_missing`, `query_failed`, and
  `context_overload` feedback items.
