# Startup And Token Test Template

Status: shared reusable foundation

## Goal

Check whether a fresh actor can orient without loading too much.

## Test

1. Run or simulate `./aicos context start <actor> projects/<project-id>`.
2. Record what was loaded.
3. Confirm long design docs, raw evidence, old handoffs, and all packets were
   not loaded by default.
4. Load one task packet only after task selection.

## Pass Criteria

- orientation is enough to choose next read
- no bulk-load behavior
- missing context is explicit
- agent can name the next task or ask the human cleanly
