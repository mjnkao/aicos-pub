# Daily Digest Delivery Surface

Status: public sample

## Purpose

`daily_digest` is the default assistant-ready package for the sample project.

It demonstrates how an AICOS-managed project can describe a runtime output
surface without copying generated output into AICOS.

## Runtime Surface

Example command:

```bash
python -m sample_research_digest build-daily-digest
```

Example output:

```text
outputs/assistant/daily-digest-package.json
```

## Package Boundary

Top-level sections:

- `package_meta`
- `requested_context`
- `source_status`
- `data_reliability`
- `research_topics`
- `open_questions`
- `recommended_next_reads`
- `output_hints`

## Source References

Use source repo files as runtime authority when deeper review is needed. Do not
mirror generated output into AICOS unless a task specifically requires a small
fixture.
