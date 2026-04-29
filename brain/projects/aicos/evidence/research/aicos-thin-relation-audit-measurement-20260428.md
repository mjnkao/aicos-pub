# AICOS Thin Relation Audit Measurement

Status: measurement note
Date: 2026-04-28

## Purpose

Measure whether the current audit-only relation layer is useful enough to
justify a future bounded read surface such as `aicos_get_related_context`.

This pass does not add a graph truth store and does not promote derived
relations into canonical truth.

## Commands

```bash
./aicos audit relations --scope projects/aicos --write --format json
./aicos audit relations --scope projects/sample-project --write --format json
```

## Results

### Initial Measurement

| Scope | Files scanned | Files with Trace Refs | Source refs | Artifact refs | Derived edges | Broken source refs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `projects/aicos` | 201 | 94 | 49 | 153 | 202 | 2 |
| `projects/sample-project` | 97 | 35 | 1 | 109 | 110 | 1 |

### After Trace Ref Hygiene

| Scope | Files scanned | Files with Trace Refs | Source refs | Artifact refs | Scope refs | Session refs | Broken source refs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `projects/aicos` | 202 | 94 | 49 | 139 | 0 | 2 | 0 |
| `projects/sample-project` | 97 | 35 | 0 | 109 | 1 | 0 | 0 |

Written runtime indexes:

- `.runtime-home/aicos/relations-index__projects__aicos.json`
- `.runtime-home/aicos/relations-index__projects__sample-project.json`

## Observations

The audit-only relation layer is already useful for hygiene and provenance:

- AICOS has enough explicit Trace Refs to make derived adjacency measurable.
- sample project has many artifact refs but almost no source refs, which means current
  adjacency is mostly "this status/checkpoint points to an artifact" rather
  than "this item is evidenced by this internal context source."
- The current audit catches malformed or non-path `source_ref` values.
- A small Trace Ref hygiene pass added `scope_refs` and `session_refs`, moved
  known symbolic refs out of `source_ref`, and brought broken source refs to
  zero for both AICOS and sample project.

Broken source-ref samples:

- `brain/projects/aicos/working/status-items/aicos-mcp-actor-normalization-and-sse-keepalive-20260428.md`
  -> `codex-thread-20260428-actor-sse-fix`
- `brain/projects/aicos/working/status-items/aicos-mcp-token-scope-authorization-20260428.md`
  -> `codex-thread-20260428-token-scope-authz`
- `brain/projects/sample-project/working/feedback/74b2664e-c457-4ead-8a30-011b110d2408.md`
  -> `projects/sample-project`

These were not missing files. They were symbolic refs written into a field
treated as a repo path. The current write/audit vocabulary now distinguishes
path refs, scope refs, session refs, and artifacts.

## CTO Judgment

Do not add `aicos_get_related_context` yet.

The audit-only relation pass has value, and the first ref hygiene pass is now
clean enough to keep measuring. However, there is still no repeated A1 feedback
showing adjacency misses that justify an A1-facing read tool.

The right next step is to keep this audit as a regression check and watch real
A1 feedback/eval misses. Consider `aicos_get_related_context` only if agents
repeatedly miss adjacent evidence/status/task context that is visible in the
derived relation index.

## Boundary

This note is evidence for the current relation/read-surface decision. Runtime
relation JSON files remain derived cache material under `.runtime-home/aicos/`;
markdown brain remains source truth.
