# Status Item: AICOS-THIN-RELATION-MODEL

Status: `in_progress`
Item type: `open_item`
Priority: `medium`
Opened at: `2026-04-24T00:00:00+07:00`
Last updated at: `2026-04-24T09:55:00+07:00`
Owner: `A2-Core`
Work lane: `aicos-search-query-architecture`

## Summary

AICOS should strengthen explicit adjacency between project/workstream/task
packet/status item/checkpoint/handoff/artifact surfaces without introducing a
heavy graph truth store. The current pass now has a proposal, a brain-level
resolver, and an audit-only derived relation index built from explicit Trace
Refs. The next decision is whether to keep relations as audit/maintenance only
or expose a bounded read surface later.

## Why It Matters

Large projects need better answers to:

- what is related to this active item?
- what evidence supports this state?
- what should an agent read next after this result?

Current search/query surfaces can find relevant documents, but adjacency is
still mostly implicit.

## Next Step

Use the current audit-only relation pass on AICOS and one active project to
measure value. Only if it proves useful should AICOS consider a bounded read
surface such as `aicos_get_related_context`.

## Trace Refs

- source_ref: `brain/projects/aicos/evidence/research/aicos-thin-relation-model-proposal-20260424.md`
- artifact_refs:
  - `brain/RESOLVER.md`
  - `packages/aicos-kernel/aicos_kernel/relations/trace_refs.py`
  - `packages/aicos-kernel/aicos_kernel/kernel.py`
  - `integrations/nightly-maintenance/README.md`
  - `.runtime-home/aicos/relations-index__projects__aicos.json`

## Notes

Learn from GBrain's primary-home and adjacency model, but do not import the
full personal-brain schema or a heavy graph subsystem.

Current low-risk progress already landed:

- `brain/RESOLVER.md` for primary-home routing + Trace Refs discipline
- `./aicos audit relations --scope <scope> --write` for derived relation audit
- optional nightly maintenance script to refresh context registry, relation
  audit, and brain status snapshots
