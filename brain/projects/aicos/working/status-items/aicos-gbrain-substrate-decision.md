# Status Item: AICOS-GBRAIN-SUBSTRATE-DECISION

Status: `open`
Item type: `open_item`
Priority: `high`
Opened at: `2026-04-24T00:00:00+07:00`
Last updated at: `2026-04-24T20:45:00+07:00`
Owner: `A2-Core`
Work lane: `aicos-architecture-substrate-strategy`

## Summary

AICOS should explicitly decide whether to continue as a mostly custom full
stack or evolve into a thinner semantic/control-plane layer on top of a more
GBrain-derived retrieval/runtime substrate. Current judgment is that AICOS
should keep semantics/authority/contracts in AICOS while reducing duplicate
custom substrate work where GBrain already has strong leverage.

## Why It Matters

AICOS is differentiated mainly in:

- authority model;
- multi-agent project semantics;
- control-plane write contracts;
- onboarding/import and continuity behavior.

AICOS is less differentiated in:

- retrieval substrate;
- health/verify/search operating discipline;
- chunking/query/runtime maintenance behavior.

Without an explicit decision, AICOS may continue to grow a custom substrate
surface that is expensive to maintain and overlaps too much with GBrain.

## Next Step

Build the concrete keep/migrate/retire inventory for current AICOS
retrieval/runtime components, then run a narrow substrate-reduction pass that
starts with retrieval eval and doctor/verify discipline rather than broad
schema migration.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`
- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`
  - `brain/projects/aicos/working/gbrain-search-reuse-review.md`

## Notes

Do not read this as "replace AICOS with GBrain". Read it as:

- keep AICOS product semantics;
- reduce custom substrate growth;
- use a phased, bounded migration strategy if the reuse path proves valuable.
