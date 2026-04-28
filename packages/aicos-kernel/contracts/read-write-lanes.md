# Read And Write Lanes Contract

Status: initial MVP contract

## Brain

`brain/` holds durable work reality and service knowledge:

- `canonical/` for approved truth.
- `working/` for current best working reality.
- `evidence/` for intake, raw input, and candidate updates.
- `branches/` for project experiment reality.

## Agent Repo

`agent-repo/` holds operational state and actor behavior. It is not project
truth by default.

## Backend

`backend/` holds serving substrate, indexes, sync state, and engine config. It
is not the authority layer.

## Serving

`serving/` holds generated query, capsule, promotion, branch, truth, and
feedback packets.

