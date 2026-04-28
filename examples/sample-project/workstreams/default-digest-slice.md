# Default Digest Slice

Status: public sample workstream

## Intent

Use the daily digest as the first active workstream for the sample project.

The goal is to give agents enough current context to work on the digest flow
without reading every source note, generated output, or historical decision.

## Active Context

- Public research notes are collected from approved source folders.
- Notes are normalized into stable records.
- A digest package is assembled for assistant consumption.
- Validation checks freshness, missingness, and source attribution.
- The assistant produces a daily research brief from the digest package.

## Delivery Boundary

The digest package should be:

- compact
- source-attributed
- explicit about missing data
- useful for human review
- safe to regenerate

It should not become:

- a raw dump of all notes
- an unreviewed memory mirror
- a hidden scoring engine
- a substitute for source provenance

## Example Package Sections

- `package_meta`
- `requested_context`
- `source_status`
- `data_reliability`
- `research_topics`
- `open_questions`
- `recommended_next_reads`
- `output_hints`

## Runtime Authority

The external sample project checkout owns:

- collectors
- normalization scripts
- package builder
- validation tests
- generated digest artifacts

AICOS owns:

- current project context
- workstream routing
- task packets
- continuity
- risks and open questions

## Avoid In Hot Path

- historical source dumps
- generated output bulk
- stale notes
- private credentials
- unrelated project workstreams
