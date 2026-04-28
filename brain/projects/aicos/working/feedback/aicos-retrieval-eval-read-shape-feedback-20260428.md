# Feedback: Retrieval eval runner initially missed required read-query shape

Status: open
Feedback type: `tool_shape_confusing`
Severity: `low`
Project: `aicos`
Scope: `projects/aicos`
Write id: `aicos-retrieval-eval-read-shape-feedback-20260428`
Written at: `2026-04-28T06:23:41+00:00`
Last updated at: `2026-04-28T06:23:41+00:00`

## Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-retrieval-eval`
Agent display name: `unknown`
Work type: `ops`
Work lane: `retrieval-eval`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

## Summary

While testing through HTTP MCP, the first runner calls failed because read calls require agent_family/agent_instance_id/execution_context and aicos_query_project_context expects query rather than question. Runner now maps these correctly. This is useful A1-facing friction evidence.

## Observed In

scripts/aicos-retrieval-eval HTTP MCP run

## Recommendation

Keep examples and eval tooling explicit about read identity fields and query-field naming. Consider friendlier aliases only if more A1 clients hit the same mismatch.

## Trace Refs

- artifact_refs:
  - `scripts/aicos-retrieval-eval`
  - `brain/projects/aicos/evidence/research/aicos-retrieval-eval-corpus-20260428.json`
- source_ref: `brain/projects/aicos/evidence/research/aicos-retrieval-eval-run-20260428.md`

## Boundary

Recorded through MCP semantic feedback write. This is a service-improvement signal, not canonical truth or task continuity.
