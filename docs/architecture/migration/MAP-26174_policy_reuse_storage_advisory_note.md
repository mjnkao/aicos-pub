# MAP-26174 Policy Reuse And Storage Advisory Note

Date: 2026-04-18
Status: saved-as-advisory-source
Scope: `projects/aicos`
Actor lane: `A2-Core-C`

## What Was Saved

Source file:

```text
docs/New design/MAP-26174_A1_Reusable_Policies_And_AICOS_Markdown_vs_Database_Storage_Recommendation.md
```

## Normalized Takeaways

- Many operating policies can be reused for future A1: lane boundaries,
  canonical/working/evidence/branch boundaries, W1/W2/W3/W4 writeback levels,
  state-transition writeback, packet-first loading, and chat decision ->
  structured state.
- A1 needs its own role/startup/rule/task packets and lane mapping.
- A2-Core taxonomy, Codex-as-A2-Core-C identity, and A2 service backlog lanes
  should not be copied into A1.
- Markdown/text remains the authority surface for narrative, reviewed,
  human+AI-readable truth in the current phase.
- GBrain/PGLite/Postgres should be used as retrieval/runtime/index substrate and
  future registry support, not default authority for all self-brain/working
  truth.

## Updated Repo Truth

- `brain/projects/aicos/working/architecture-working-summary.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/evidence/policy-sources/policy-source-index.md`
- `agent-repo/classes/a2-service-agents/tasks/backlog/policy-followups.md`
- `brain/projects/aicos/working/handoff/current.md`

## Not Implemented Now

- No A1 startup card was created.
- No shared policy extraction was implemented yet.
- No DB-backed registry was added.
- No authority moved from Markdown to database.
