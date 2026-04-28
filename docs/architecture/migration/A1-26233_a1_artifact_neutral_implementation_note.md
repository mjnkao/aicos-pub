# A1-26233 A1 Artifact-Neutral Implementation Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Source

Normalized from:

```text
docs/New design/A1-26233_AICOS_A1_Artifact_Neutral_Model_For_Coding_And_Non_Coding_Workers.md
```

## What Was Refined From A1-26224

A1-26224 established identity, layered rules, packet-first startup, and
continuation metadata. This pass kept that model and made A1 core language
artifact-neutral.

## Coding-Biased Defaults Neutralized

- `branch` as universal continuation context -> `work_context`, route,
  workstream, scenario, concept, campaign angle, research path, or git branch
  when coding.
- `repo delta` -> `artifact delta` / meaningful work delta.
- `git commit` / `push` as universal checkpoint -> artifact checkpoint / remote
  continuity checkpoint.
- `files touched` as universal output -> artifacts or lanes touched.
- coding as implicit A1 default -> code is one supported artifact type.

## Artifact-Neutral Wording Introduced

- `primary_artifacts`
- `touched_artifacts`
- `artifact checkpoint`
- `meaningful work delta`
- `review / approval / validation`
- support for code, docs, design, content, research, operations, and hybrid
  artifact sets

## Where It Was Placed

- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`
- `agent-repo/classes/a1-work-agents/rules/layered-rules.md`
- `agent-repo/classes/a1-work-agents/rule-cards/`
- `agent-repo/classes/a1-work-agents/task-packets/README.md`
- `agent-repo/classes/a1-work-agents/tasks/README.md`
- `brain/shared/policies/checkpoint-writeback-policy.md`
- `brain/shared/templates/task-state-template.md`
- `packages/aicos-kernel/contracts/task-packet-template.md`

## Company / Workspace Compatibility

The existing A1 layered model is preserved:

- A1 core rules
- higher-scope rules later: shared/company/workspace
- project rules
- workstream/task rules

No company/workspace rule tree was added. Higher-scope layers remain optional
and not startup-default.

## Intentionally Left For Later

- artifact-type-specific rule packs
- project-specific design/content/research templates
- automated rule-stack resolution
- A1 registry or orchestration runtime

## Remaining Risk

A1 is now less coding-biased in core language, but real non-coding usage still
needs validation through actual design/content/research project slices.
