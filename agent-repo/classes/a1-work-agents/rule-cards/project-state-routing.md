# Rule Card: A1 Project State Routing

Load when deciding where to write project information.

## Routing

- stable reviewed truth -> `brain/projects/<project-id>/canonical/`
- current shared state -> `brain/projects/<project-id>/working/`
- raw/source material -> `brain/projects/<project-id>/evidence/`
- branch/experiment/alternate route reality -> `brain/projects/<project-id>/branches/`
- actor execution state -> `agent-repo/classes/a1-work-agents/tasks/`
- generated option/review artifacts -> `serving/`

Do not use `current-state.md` as a general inbox.

Project artifacts may be code, docs, design assets, content drafts, research
outputs, operational plans, or hybrid sets. Route by authority/state, not by
artifact type alone.

Future company/workspace scoped rules may live above project rules, but they are
not implemented as startup-default layers in the current MVP.
