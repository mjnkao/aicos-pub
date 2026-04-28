# Source Inventory Template

Status: shared reusable template

Purpose: record source materials considered for import and their intended AICOS
handling.

## Inventory Table

| source_path | source_group | source_type | authority_level | import_action | target_lane | target_file | slice_relevance | pass_phase | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | project / impl / state / startup / evidence / code / output | canonical / working / evidence / excluded | authoritative / reference / historical / excluded | digest / summary-only / reference-only / skip | canonical / working / evidence / a1-support |  | required / optional / later / out-of-scope | pass 1 / later |  |

## Selected Canonical Sources

- TBD

## Selected Working Sources

- TBD

## Selected Active Delivery / Runtime Surface Sources

- TBD

## Selected Startup / Routing Sources

- TBD

## Selected Evidence / Reference Sources

- TBD

## Excluded Sources

- TBD

## Open Questions In Inventory

1. TBD

## Rule

Every real import must instantiate source inventory before digesting project
truth. Do not import from memory or inherited chat context.
