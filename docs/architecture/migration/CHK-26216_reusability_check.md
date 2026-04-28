# CHK-26216 Reusability Check

Date: 2026-04-18
Actor: A2-Core-C

## Shared Reusable Foundation

- `brain/shared/policies/checkpoint-writeback-policy.md`
- `brain/shared/templates/task-state-template.md`
- `brain/shared/templates/project-onboarding/`
- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`
- `agent-repo/classes/a1-work-agents/rule-cards/`
- `agent-repo/classes/a1-work-agents/tasks/README.md`
- `agent-repo/classes/a1-work-agents/task-packets/README.md`
- `./aicos context start A1 projects/<project-id>`

These artifacts are project-neutral and should be reused for future projects.

## Crypto-Specific

- `brain/projects/sample-project/`

This is only the first concrete onboarding target. Its files are bootstrap
placeholders and do not contain reviewed project truth yet.

## Future Semi-Automation Candidates

- generate project bootstrap folders from templates
- render onboarding checklist for a project id
- generate initial A1 task packet after slice selection
- validate required bootstrap files
- render real-project scorecards
- index task packet summaries

## Reusability Verdict

A second real project can follow the same onboarding kit by changing only
project-specific identity, source inventory, slice choice, and bootstrap state.
No large subsystem is required.
