# Rule Card: A1 Writeback And Checkpoint

Load when project work changes state, reaches a milestone, creates a meaningful
artifact delta, becomes blocked/reviewable, or may be continued by another
actor.

## Rule

- Prefer Phase 2 semantic MCP write tools for AICOS-facing continuity:
  `aicos_record_checkpoint`, `aicos_write_task_update`, and
  `aicos_write_handoff_update`.
- Update project working state only when shared project reality changes.
- Update actor task state when owner/status/blocked reason/next step changes.
- Update project handoff only when continuation or newest-vs-stale story
  changes.
- Keep project state, workstream/task state, and actor execution state separate.
- Create an artifact checkpoint appropriate to the task: commit for code,
  saved draft for writing, named route for design, evidence digest for research,
  or another reviewable saved artifact state.
- Do not write every chat turn.
- Do not promote canonical truth without review.
- Do not use raw AICOS file edits as the default A1 writeback interface when
  MCP is available.

Direct local repo/artifact writes remain valid for the actual assigned work
artifact, such as code, design files, content drafts, or research evidence.

Shared policy:

```text
brain/shared/policies/checkpoint-writeback-policy.md
```
