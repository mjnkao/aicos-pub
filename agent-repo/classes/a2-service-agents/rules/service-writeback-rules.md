# A2 Service Writeback Rules

Status: reference/deep policy, not startup-default

A2 writes durable service knowledge to `brain/service-knowledge/` and
operational maintenance state to `agent-repo/classes/a2-service-agents/`.

## Write Only At Commit Points

A2 should not write every chat message into AICOS. Writeback should happen when
there is a meaningful state transition:

- decision made
- blocker confirmed
- option packet ready
- selected branch or direction changed
- milestone completed
- risk confirmed
- open question worth preserving
- backlog item clear enough to schedule later

## Lane Routing

- Working reality: `brain/projects/aicos/working/`
- Candidate decisions or branch ideas: `brain/projects/aicos/evidence/candidate-decisions/`
- A2 backlog or tech debt: `agent-repo/classes/a2-service-agents/tasks/backlog/`
- Service knowledge: `brain/service-knowledge/`
- Canonical truth: only after explicit review/promotion

## Sync

Run `aicos sync brain` after meaningful brain updates when retrieval should see
the new state. Sync is serving refresh, not authority mutation.
