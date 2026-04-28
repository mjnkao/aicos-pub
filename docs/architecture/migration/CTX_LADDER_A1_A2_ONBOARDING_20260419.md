# CTX Ladder A1/A2 Onboarding Note

Date: 2026-04-19
Actor: A2-Core-C
Scope: `projects/aicos`

## What Was Added

Added lightweight context ladders for new external co-workers:

- `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
- `agent-repo/classes/a2-service-agents/onboarding/a2-serve-context-ladder.md`
- `agent-repo/classes/a2-service-agents/onboarding/a2-core-new-agent-prompt-template.md`
- `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`
- `agent-repo/classes/a1-work-agents/onboarding/a1-new-agent-prompt-template.md`

Added project-level ladder support:

- `brain/shared/templates/project-onboarding/project-context-ladder-template.md`
- `brain/projects/aicos/working/context-ladder.md`
- `brain/projects/sample-project/working/context-ladder.md`

## Design Choice

Each ladder entry gives a short stable summary of what a file or file group is
for. It does not copy volatile project state. The referenced files remain
authoritative, so future edits should not require updating many duplicated
summaries.

## Actor Coverage

- A2-Core: active, detailed ladder for improving AICOS itself.
- A2-Serve: placeholder ladder only; runtime lane is not active yet.
- A1: active generic ladder that starts with actor identity, then scope binding,
  then project/task context.

## What Was Not Built

- no new runtime resolver
- no UI/API
- no automation/generator
- no A2-Serve runtime implementation
- no company/workspace governance tree

## Next Possible Step

Extend `./aicos context start` output to mention the matching context ladder
when startup bundles are generated for A1 or A2-Core.
