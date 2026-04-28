# Sample Research Digest Architecture Baseline

Status: public sample

## Pipeline

1. source collection
2. normalization
3. enrichment
4. digest assembly
5. validation
6. assistant handoff

## Module Boundaries

- `collectors/`: fetch or read approved public source notes.
- `normalization/`: convert source notes into stable records.
- `enrichment/`: add tags, source links, and topic descriptors.
- `digest_builder/`: assemble a compact package for the selected mode.
- `validation/`: check freshness, missingness, schema shape, and attribution.
- `handoff/`: write assistant-ready digest artifacts.

## Architecture Rules

- Keep deterministic package construction separate from assistant reasoning.
- Do not hide final conclusions in pipeline code.
- Keep source attribution visible.
- Let unavailable sources degrade explicitly.
- Avoid expanding source scope without a clear user-facing reason.
