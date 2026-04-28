# Sample Project Task Packet Index

Status: public sample
Scope: `projects/sample-project`

Do not load every task packet at startup. Read the project context ladder first,
then select one task packet after the role and work item are clear.

## Authority Rule

For `projects/sample-project`:

- AICOS is the context/control-plane authority.
- The sample project checkout is the code/runtime/artifact authority.
- Raw source notes and generated digest outputs are evidence, not default
  working continuity.

## Role-Aware Startup

An agent should declare:

- project id
- project-facing role
- workstream
- mode: onboarding, continuation, execution, review, or decision
- selected task packet if known

Example:

```text
project_id: sample-project
project_role: fullstack-dev
mode: execution
workstream: default-digest-slice
task_packet: sample-review-digest-slice
```

## Current Sample Packets

Suggested packet to create next:

- `sample-review-digest-slice.md` - review the default digest slice and identify
  the smallest safe implementation or documentation improvement.

## Writeback Rule

Write project continuity through AICOS semantic write surfaces when available:

- checkpoint
- task update
- handoff update
- status item update
- artifact reference registration

Do not write continuity into the external project repo unless the selected task
explicitly changes runtime documentation or source artifacts.
