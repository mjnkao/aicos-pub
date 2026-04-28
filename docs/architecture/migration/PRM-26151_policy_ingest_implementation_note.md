# PRM-26151 Policy Ingest Implementation Note

Date: 2026-04-18
Status: implemented-mvp

## Updated Files

Canonical:

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`

Working:

- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/architecture-working-summary.md`

Evidence:

- `brain/projects/aicos/evidence/candidate-decisions/README.md`
- `brain/projects/aicos/evidence/candidate-decisions/decision-candidate-index.md`
- `brain/projects/aicos/evidence/policy-sources/policy-source-index.md`

A2 operational lanes:

- `agent-repo/classes/a2-service-agents/rules/startup-rules.md`
- `agent-repo/classes/a2-service-agents/rules/service-boundaries.md`
- `agent-repo/classes/a2-service-agents/rules/service-writeback-rules.md`
- `agent-repo/classes/a2-service-agents/rules/idea-capture-rules.md`
- `agent-repo/classes/a2-service-agents/tasks/backlog/README.md`
- `agent-repo/classes/a2-service-agents/tasks/backlog/policy-followups.md`

## Normalized From Source Files

- `RUL-26088`: role clarity for humans, A1, A2, and Codex as A2-Core-C.
- `A2S-26102`: A2-Core vs A2-Serve, A2-Core-R vs A2-Core-C, and current A2-Core focus.
- `FLW-26124`: chat decision flow, `aicos option choose`, and `aicos sync brain` boundaries.
- `POL-26140`: routing for open questions, backlog, candidate branch ideas, tech debt, and active risks.
- `POL-26145`: W1/W2/W3/W4 writeback levels, commit points, debounce rule, and sync-as-serving-refresh.
- `POL-26150`: mapping guidance and short reading order intent.

## Intentionally Left As Source/Reference

The long source files remain in `docs/New design/` and are referenced from
`brain/projects/aicos/evidence/policy-sources/policy-source-index.md`.

They were not copied verbatim into canonical or working because self-brain must
stay concise and startup-friendly.

## Unresolved Questions

- When should `aicos sync brain` run embedding/vector refresh by default?
- When does `aicos option choose` need actor registry, review signature, or reason taxonomy?
- When should temporary role rules be split into permanent class-specific files?
- What threshold turns a candidate branch idea into official branch reality?
