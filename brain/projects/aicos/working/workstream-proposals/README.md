# AICOS Workstream Proposals

Status: active MVP lane
Updated: 2026-04-23

## Purpose

Hold proposed workstreams before they become accepted project workstream
surfaces.

`aicos_get_workstream_index` should expose accepted/materialized workstreams,
not infer new lanes from suggestions or agent notes.

## Proposal Lifecycle

- `proposed`: suggestion captured for review.
- `reviewing`: A2/human is checking scope and overlap.
- `accepted`: approved to materialize into project workstream context.
- `rejected`: intentionally not adopted.
- `superseded`: replaced by another proposal.

## Write Rule

Agents should use `aicos_update_status_item` for proposal lifecycle and
`aicos_register_artifact_ref` for longer supporting notes.

Do not create a new accepted workstream, packet lane, or context index entry
from a proposal unless the human or A2-Core explicitly accepts it.

## Minimum Proposal Fields

- proposed workstream id
- project scope
- intended owner/actor role
- problem or opportunity
- expected outputs
- affected artifacts/repos/tools
- overlap with existing workstreams
- acceptance condition

## Materialization Boundary

Accepted proposals may be materialized into project-specific workstream files
or task packets. Until then, this lane is proposal/reference only.
