# Task Packet: Review Default Digest Slice

Status: public sample

```yaml
schema_version: "0.1"
kind: "aicos.task_packet"
task_id: "sample-review-digest-slice"
project_id: "sample-project"
project_role: "reviewer"
mode: "review"
workstream: "default-digest-slice"
objective: "Review the default digest slice and identify the smallest useful improvement to the sample project."
required_context:
  - "examples/sample-project/README.md"
  - "examples/sample-project/brain/project/canonical/project-profile.md"
  - "examples/sample-project/brain/project/working/context-ladder.md"
  - "examples/sample-project/workstreams/default-digest-slice.md"
  - "examples/sample-project/delivery-surfaces/daily-digest-surface.md"
allowed_write_lanes:
  - "examples/sample-project/brain/project/working/open-items.md"
  - "examples/sample-project/brain/project/working/open-questions.md"
  - "examples/sample-project/brain/project/working/active-risks.md"
success_condition: "The reviewer can explain the digest slice, identify one next improvement, and avoid reading unrelated source or generated output."
```

## Review Focus

- Is the authority split clear?
- Is the role-aware context path clear?
- Is the workstream small enough?
- Are source/runtime artifacts separated from AICOS context?
- Are private data and generated bulk excluded?
