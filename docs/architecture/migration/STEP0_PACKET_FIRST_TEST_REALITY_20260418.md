# Step 0 Packet-First Test Reality Note

Date: 2026-04-18
Status: repo-truth-refresh

## Verified Local Reality

- `./aicos context start A2-Core-C projects/aicos` is implemented and usable in
  MVP form.
- Bare `aicos context start A2-Core-C projects/aicos` fails in the current shell
  when the repo wrapper is not on PATH.
- A2-Core task packets exist in
  `agent-repo/classes/a2-service-agents/task-packets/`.
- Implementation note exists at
  `docs/migration/A2_CORE_TASK_PACKETS_20260418.md`.
- Rule cards exist in `agent-repo/classes/a2-service-agents/rule-cards/`.

## Repo-Visible Truth Updated

- Handoff now says `context start` exists in narrow MVP form.
- Handoff now lists `./aicos context start A2-Core-C projects/aicos` in the CLI
  surface.
- Open questions no longer ask when to add `context start`; they now ask when to
  extend it beyond MVP and improve packet selection/PATH consistency.
- Backlog records the fresh-thread frictions as actionable follow-ups.

## Intentionally Left For Future Work

- No resolver/orchestration system was added.
- `context start` was not expanded beyond `A2-Core-C` and `projects/aicos`.
- Packet one-line summaries were recorded as a follow-up, not implemented.
- Suggested Next Reads were recorded as slightly broad, not redesigned.

## Frictions Recorded, Not Fully Fixed

- PATH inconsistency: `aicos ...` vs `./aicos ...`.
- Task packet list lacks one-line summaries.
- Suggested Next Reads may still be broader than ideal.

Tiny wording fix completed:

- rule cards now use repo-local `./aicos ...` command examples for option
  choose and sync brain.
