# Sample Research Digest Delivery Baseline

Status: public sample

## Default Delivery Surface

Default mode:

```text
daily_digest
```

Example generated artifact:

```text
outputs/digests/daily-digest-current.json
```

Example assistant package:

```text
outputs/assistant/daily-digest-package.json
```

## Package Sections

- `package_meta`
- `requested_context`
- `source_status`
- `data_reliability`
- `research_topics`
- `open_questions`
- `recommended_next_reads`
- `output_hints`

## Expected Assistant Output

The assistant should produce a concise research brief with:

- current topic map;
- high-confidence findings;
- source coverage gaps;
- unresolved questions;
- recommended next reads;
- caveats.
