# AICOS Feedback To Eval Digest

Generated at: `2026-04-28T14:55:21+00:00`
Project: `aicos`

## Summary

- Feedback records scanned: `12`
- Actionable feedback records: `3`
- Eval candidate records: `3`
- New eval candidates: `0`

## Area Counts

- `auth`: `1`
- `general`: `1`
- `tool_schema`: `1`

## Candidate Eval Cases

### P0 health checks failed without exported daemon token

- Source: `brain/projects/aicos/working/feedback/20260428t112627z-886f23eabe.md`
- Area: `auth`
- Feedback type: `bootstrap_confusing`
- Severity: `low`
- Already covered by eval: `true`
- Should add eval case: `false`
- Candidate question: how should an A1 or A2 check AICOS MCP auth/token setup when a health or eval command fails?
- Expected answer shape: Default these health/eval tools to fall back to .runtime-home/aicos-daemon.env when env AICOS_DAEMON_TOKEN is not set.

### Retrieval eval runner initially missed required read-query shape

- Source: `brain/projects/aicos/working/feedback/aicos-retrieval-eval-read-shape-feedback-20260428.md`
- Area: `tool_schema`
- Feedback type: `tool_shape_confusing`
- Severity: `low`
- Already covered by eval: `true`
- Should add eval case: `false`
- Candidate question: what MCP read/write fields should an agent use when a tool schema or field name is confusing?
- Expected answer shape: Keep examples and eval tooling explicit about read identity fields and query-field naming. Consider friendlier aliases only if more A1 clients hit the same mismatch.

### Feedback surface smoke test

- Source: `brain/projects/aicos/working/feedback/feedback-surface-smoke-test-20260422.md`
- Area: `general`
- Feedback type: `other`
- Severity: `low`
- Already covered by eval: `true`
- Should add eval case: `false`
- Candidate question: what AICOS service friction should be recorded before the next handoff?
- Expected answer shape: Use feedback digest for future repeated context-serving issues.

## Boundary

Digest only. It proposes eval additions; it does not mutate the retrieval corpus automatically.
