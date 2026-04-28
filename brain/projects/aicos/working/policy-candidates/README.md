# AICOS Policy Candidates

Status: active MVP lane
Updated: 2026-04-23

## Purpose

Hold proposed rule, policy, framework, or operating-model changes before they
are promoted into active policy/canonical surfaces.

This lane prevents feedback or suggestions from being written into handoff,
task-state, or canonical files by habit.

## Candidate Lifecycle

Use this lightweight lifecycle until AICOS has dedicated MCP tools:

- `proposed`: captured suggestion; not active policy.
- `reviewing`: A2/human is evaluating fit and blast radius.
- `accepted`: approved for implementation or promotion.
- `rejected`: intentionally not adopted.
- `superseded`: replaced by another candidate or implementation.

## Write Rule

Agents may register a compact policy candidate through:

- `aicos_update_status_item` with `item_type=decision_followup` or
  `open_item`; and/or
- `aicos_register_artifact_ref` pointing to a longer proposal artifact.

Do not edit canonical policy files from a candidate unless the human or A2-Core
explicitly approves promotion.

## Minimum Candidate Fields

- candidate id
- source or proposer
- affected scope
- proposed change
- reason
- expected benefit
- risk or compatibility concern
- review status
- artifact refs, if any

## Promotion Boundary

Promotion means a separate edit to the target active policy/canonical file plus
a status-item update explaining why the candidate was accepted. Candidate text
itself is not active policy.
