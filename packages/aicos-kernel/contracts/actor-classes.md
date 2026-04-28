# Actor Classes Contract

Status: initial MVP contract

## Classes

- `humans`: manager, reviewer, approver, team lead.
- `a1-work-agents`: agents that perform project or business work.
- `a2-service-agents`: agents that improve AICOS service quality.
- `a3-template`: reserved for future classes.

## Boundary

A1 agents may create working updates, blockers, findings, proposals, and branch
option packets. They must not silently promote business truth to canonical.

A2 agents may create service feedback, retrieval notes, capsule quality notes,
source classification proposals, and service improvements. They must not act as
final business authority.

Humans approve promotions and decide between material options.

