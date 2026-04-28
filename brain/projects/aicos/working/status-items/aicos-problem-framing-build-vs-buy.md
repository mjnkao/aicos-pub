# Status Item: AICOS-PROBLEM-FRAMING-BUILD-VS-BUY

Status: `open`
Item type: `open_item`
Priority: `high`
Opened at: `2026-04-28T00:00:00+07:00`
Last updated at: `2026-04-28T10:15:00+07:00`
Owner: `A2-Core`
Work lane: `aicos-product-architecture`

## Summary

AICOS now has a clearer co-founder-level framing: it is a multi-agent project
context control-plane, not merely a memory or search product. The next
architecture decisions should preserve AICOS-owned semantics while reducing
custom substrate work where GBrain or similar systems already offer stronger
retrieval/runtime leverage.

## Why It Matters

Without a clear product framing, AICOS risks:

- overbuilding generic memory/search/runtime layers;
- under-investing in true control-plane differentiation;
- drifting toward a product shape that does not match its actual value.

## Next Step

Use the product framing and build-vs-buy memo to:

1. validate which AICOS components are true differentiation;
2. decide which substrate areas should be kept, migrated, wrapped, or retired;
3. leave room for a future path where company/workspace knowledge for AI agents
   can become first-class without forcing that scope immediately.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
- artifact_refs:
  - `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`
  - `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`

## Notes

Important nuance:

- short term, AICOS does not need to become a universal company knowledge
  product;
- long term, if company knowledge is required for AI agents to operate
  correctly, AICOS or its substrate boundary must be able to support it.
