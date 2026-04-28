# AICOS Phase 0.5 Learning Loop Check

Status: completed
Date: 2026-04-28
Actor: A2-Core-C
Scope: projects/aicos

## Purpose

Before moving to Phase 1 module inventory, verify that A1 agents can send
learning-loop feedback through AICOS MCP when context serving, onboarding,
query, routing, or write-schema behavior is confusing.

## Findings

- AICOS already exposes `aicos_record_feedback` and `aicos_get_feedback_digest`.
- Startup bundle and project health expose a `feedback_loop` object.
- Session-close write gates require one feedback closure for the same
  `scope + agent_family + agent_instance_id + work_lane`.
- HTTP daemon schema already advertised `work_type=orientation`, but the kernel
  write validator rejected it. This made first-contact feedback examples brittle.
- The local stdio adapter had stale feedback schema:
  - missing `no_issue`
  - missing tool/setup friction feedback types such as `tool_missing`,
    `bootstrap_confusing`, `write_schema_confusing`, and `interop_problem`
  - missing `orientation` in write `work_type` enums
  - read schemas did not surface the audit identity fields that let
    `feedback_loop` detect first-contact usage.

## Changes

- Added `orientation` to kernel write `ALLOWED_WORK_TYPES`.
- Updated local stdio write schemas to include `orientation`.
- Updated local stdio feedback schema to match the HTTP daemon feedback types.
- Added read identity fields to local stdio read tool schemas so stdio-only A1
  clients are nudged toward `agent_family`, `agent_instance_id`, `work_type`,
  `work_lane`, and `execution_context`.

## Verification

- `python3 -m py_compile` passed for:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `integrations/local-mcp-bridge/aicos_mcp_stdio.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
- CLI feedback smoke succeeded with `work_type=orientation`,
  `work_lane=intake`, `feedback_type=no_issue`.
- HTTP daemon was restarted through `scripts/aicos-install-launchagents`.
- HTTP `/health` returned `status=ok` and `search_engine=postgresql_hybrid`.
- HTTP startup bundle for an A1 orientation read returned
  `feedback_loop.ask_now=true`, `trigger=first_contact`.
- HTTP feedback smoke succeeded with `work_type=orientation`,
  `work_lane=intake`, `feedback_type=no_issue`.
- Local stdio `tools/list` now exposes read identity fields, `orientation`, and
  the full feedback type enum including `no_issue`.

## Judgment

The learning loop is now good enough to move into Phase 1 while real A1 usage
continues. The loop is intentionally lightweight: AICOS nudges at first contact,
after repeated friction, and at session-close boundaries, without adding a
separate survey or heavy workflow.

Remaining improvement should be driven by actual A1 feedback rather than more
Phase 0.5 hardening.
