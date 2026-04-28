# Rule Compliance Test Template

Status: shared reusable foundation

## Goal

Check whether an actor follows project lane, checkpoint, and escalation rules.

## Observe

- writes project reality to `brain/projects/<project-id>/working/`
- writes actor execution state to `agent-repo/.../tasks/`
- avoids canonical promotion without review
- escalates AICOS/system friction to A2
- checkpoints meaningful milestones

## Distinguish

- actor-discipline issue: rule existed but actor ignored it
- architecture issue: rule was ambiguous or lane was missing
- tooling issue: command/helper made the correct path hard
