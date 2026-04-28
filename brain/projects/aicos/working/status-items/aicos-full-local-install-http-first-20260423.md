# Status Item: aicos-full-local-install-http-first-20260423

Status: resolved
Item type: `decision_followup`
Type guidance: A decision already made that needs tracking through implementation, rollout, verification, or cleanup.
Project: `aicos`
Scope: `projects/aicos`
Item id: `aicos-full-local-install-http-first-20260423`
Title: AICOS HTTP daemon + PostgreSQL fully installed and running
Last write id: `20260423T035520Z-d8d2350547`
Last updated at: `2026-04-23T03:55:20+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `charming-nobel-eeb666`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-mcp-daemon-sse`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

Resolved: PostgreSQL 18 cài qua Postgres.app (không cần admin), pgvector 0.8.1 active, daemon chạy qua LaunchAgent tự động start khi Mac khởi động. Claude Code CLI dùng HTTP transport trực tiếp. Claude Desktop dùng stdio. HTTPS proxy chạy tại port 8443 cho LAN agents.

## Item Type Guidance

A decision already made that needs tracking through implementation, rollout, verification, or cleanup.

## Reason

Human tự cài Postgres.app, setup xong toàn bộ stack: PG18 + pgvector + daemon LaunchAgent + HTTPS proxy LaunchAgent. Blocked item về Homebrew permission không còn relevant vì đã dùng Postgres.app thay thế.

## Next Step

Implement SSE trong daemon (IMPL-MCP-DAEMON-SSE) để Claude Desktop connector hoạt động qua HTTPS.

## Trace Refs

- none

## Boundary

Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.
