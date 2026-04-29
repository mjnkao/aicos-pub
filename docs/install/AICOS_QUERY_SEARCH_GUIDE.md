# AICOS Query And Search Guide

Status: operator-facing quick guide  
Last updated: 2026-04-24

Use this guide when an agent already has AICOS access and needs to query
project context efficiently without over-reading.

For external agents, `actor` is an AICOS service actor, not the client name.
External clients may omit it or send their client name; AICOS normalizes
non-explicit A2 values to `A1`. Put the client/product name in
`agent_family`, for example `antigravity`, `claude-code`, `codex`, or
`openclaw`.

This guide is inspired by good GBrain patterns, but adapted to AICOS:

- use the smallest search mode that fits
- snippets first, full context second
- treat search output as evidence pointers, not truth by itself
- debug freshness before blaming ranking

## 1. Use The Smallest Correct Path

### Mode A — direct structured read

Use direct read tools when you already know the surface you need:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_status_items`
- `aicos_get_workstream_index`
- `aicos_get_project_health`
- `aicos_get_project_registry`

Use this first when the task is obviously about:

- startup/orientation
- current continuity
- active status items
- accepted workstreams
- project health/authority boundaries

### Mode B — bounded query

Use:

```text
aicos_query_project_context
```

when you do not know the exact file/surface, but the question is still bounded.

Good examples:

- "What in AICOS mentions feedback closure?"
- "Which docs define MCP write identity requirements?"
- "Where is the current guidance for LAN client auth?"

### Mode C — exact file/path read

Use direct file reads only when:

- MCP is unavailable
- the query result already points to a specific file
- you are doing deep implementation work and need the raw source

Do not start with broad raw repo reads when the MCP surface already gives a
bounded answer.

## 2. Query Like This

Prefer short, concrete queries:

- good: `feedback closure`
- good: `LAN auth token policy`
- good: `Claude Desktop MCP`
- good: `worktree occupancy rule`

Avoid vague prompts:

- bad: `tell me everything about search`
- bad: `what is happening in this project`

If needed, constrain with `context_kinds`.

Useful kinds:

- `current_state`
- `current_direction`
- `handoff`
- `status_items`
- `workstreams`
- `canonical`
- `policy`
- `contract`

## 3. Read Snippets First

`aicos_query_project_context` returns ranked refs and compact snippets.

Use that to decide what to read next.

Pattern:

1. run a bounded query
2. inspect the top snippets and refs
3. only open the 1-3 sources that clearly matter
4. avoid loading every matched file

This keeps context smaller and usually produces better work.

## 4. Source Precedence

When sources conflict, prefer:

1. explicit user instruction in the current thread
2. current project working/canonical surfaces in `brain/projects/<id>/`
3. current contracts/policies relevant to the task
4. older evidence or historical handoff
5. design docs / backup material

Search results do not override truth. They point to likely sources.

## 5. Search Quality Debugging

If query results look wrong, check freshness before changing ranking logic.

Run:

```bash
./aicos brain status
```

Things to inspect:

- GBrain sync fresh/stale
- PG index fresh/stale
- embedding freshness
- embedding coverage
- missing/stale embedding count

If freshness is stale, fix that first.

Useful checks:

```bash
./aicos sync brain
./aicos audit summary --limit 20
```

If the daemon is involved:

```bash
curl http://127.0.0.1:8000/health
```

or token-protected equivalent.

If freshness is healthy but the expected context is still missing:

1. retry with tighter `context_kinds`
2. try the relevant direct read surface if one exists
3. include the expected missing ref, query text, and top wrong refs in
   `aicos_record_feedback`
4. do not patch raw markdown from an A1 agent just to hide the retrieval gap

Useful feedback labels:

- `tool_missing`
- `tool_shape_confusing`
- `tool_too_heavy`
- `bootstrap_confusing`
- `write_schema_confusing`
- `interop_problem`
- `work_state_missing`
- `work_state_ambiguous`
- `work_state_stale`
- `work_state_conflict`
- `ownership_unclear`

## 6. When To Use Which Surface

- "What should I read first for this project?"
  - `aicos_get_startup_bundle`

- "What is the current continuity?"
  - `aicos_get_handoff_current`

- "What open items / tech debt / open questions matter?"
  - `aicos_get_status_items`

- "Which lane should I work in?"
  - `aicos_get_workstream_index`
  - then `aicos_get_packet_index` / `aicos_get_task_packet` if applicable

- "Where is the rule/contract/doc for X?"
  - `aicos_query_project_context`

- "Is this retrieval issue a ranking problem or stale index problem?"
  - `./aicos brain status`

## 7. Human Manager Startup Question

When a human manager asks an A1:

```text
kiểm tra xem dự án đang làm đến đâu rồi, có những việc gì đang làm,
ai đang làm, chúng ta nên làm việc gì tiếp?
```

The A1 should not start with a broad repo read. Use this AICOS-first sequence:

1. `aicos_get_startup_bundle` for the actor/project orientation
2. `aicos_get_handoff_current` for current continuity and takeover context
3. `aicos_get_status_items` for open work, blockers, tech debt, and follow-ups
4. `aicos_get_project_health` for authority/coordination health
5. `aicos_query_project_context` only for missing details, with
   `context_kinds` such as `handoff`, `status_items`, `task_state`,
   `current_state`, `current_direction`, and `policy`

The answer should include:

- project progress/state
- active work lanes and visible agents
- current blockers/risks
- overlap/takeover notes
- recommended next work
- refs used

## 8. A1-Oriented Query Examples

For A1 agents, prefer task-shaped but still concrete queries:

- `what should I read first before starting this project`
- `what is ready for takeover`
- `canonical repo URL and branch`
- `how do I report MCP feedback`
- `why does brain status say stale`
- `how does OpenClaw connect to AICOS MCP`
- `what is the current handoff for this lane`

When the question is about known operational state, use direct reads before
general query:

- startup/orientation -> `aicos_get_startup_bundle`
- current continuity -> `aicos_get_handoff_current`
- open items / tech debt -> `aicos_get_status_items`
- work routing -> `aicos_get_workstream_index`
- feedback patterns -> `aicos_get_feedback_digest`

If query results are too broad, retry with `context_kinds`:

- setup/startup: `current_state`, `current_direction`, `handoff`, `task_state`
- rules/contracts: `canonical`, `policy`, `contract`
- current work: `status_items`, `task_state`, `handoff`
- source/repo identity: `canonical`, `current_state`, `project_registry`

## 9. CTO / CEO Review Questions

When a human asks:

```text
hãy đóng vai trò CTO/CEO, đọc tổng quan dự án, thiết kế kiến trúc
và đánh giá
```

The A1 should treat this as a strategic review, not a single broad search.

Use this read path:

1. `aicos_get_startup_bundle`
2. `aicos_get_handoff_current`
3. `aicos_get_status_items`
4. `aicos_get_project_health`
5. targeted `aicos_query_project_context`

Useful CTO context kinds:

- `current_state`
- `current_direction`
- `handoff`
- `status_items`
- `canonical`
- `policy`
- `contract`
- `evidence`

Useful CTO queries:

- `CTO architecture review current direction risks scalability`
- `architecture north star semantic core provider boundary deployment profile`
- `technical risks build vs buy provider boundary search retrieval`

Useful CEO context kinds:

- `current_state`
- `current_direction`
- `handoff`
- `status_items`
- `canonical`
- `evidence`

Useful CEO queries:

- `CEO strategic review product direction business value risks`
- `market landscape build vs buy product positioning company workspace context`
- `what should leadership decide next`

The answer should separate:

- current state
- strategic direction
- what is sound
- what is weak or misaligned
- missing decisions
- recommended next actions
- source refs

## 10. Common Mistakes

1. Using query when a direct read tool already exists
2. Loading every matched file instead of reading snippets first
3. Treating search results as truth instead of source pointers
4. Debugging ranking before checking freshness/coverage
5. Querying without `context_kinds` when the question is clearly about policy,
   contract, or handoff only
6. Treating derived projections as truth. PostgreSQL index metadata (and any
   future link-graph edges) are derived views. They are helpful for retrieval
   and navigation, but the durable source of truth remains the underlying
   markdown + MCP semantic writes.
