# AICOS Status Item Type Policy

Status: active
Updated: 2026-04-21

## Purpose

Keep project status items filterable across coding, content, design, research,
ops, and mixed work.

## Type Guide

- `open_item`: new actionable work that is not primarily an existing
  defect/debt, unresolved question, or decision follow-up.
- `open_question`: unresolved question needing human, architecture, product, or
  project decision before the next clear action.
- `tech_debt`: known existing issue, friction, missing validation, missing
  coverage, missing docs, stale behavior, cleanup, or quality gap.
- `decision_followup`: a decision already made that needs tracking through
  implementation, rollout, verification, or cleanup.

## Examples

- Coding: "missing test coverage for import validation" is `tech_debt`.
- Coding: "add query support for canonical docs" is `open_item` when it is a
  new planned capability, and `tech_debt` if it records an existing gap that is
  already causing incorrect agent behavior.
- Content: "missing brand voice guide" is `tech_debt` if work is already
  blocked or inconsistent because the guide does not exist.
- Content: "decide launch narrative for campaign" is `open_question`.
- Design: "follow up on approved navigation direction" is
  `decision_followup`.

## Write Behavior

`aicos_update_status_item` owns status-item writes. It returns soft warnings
when an item type looks suspicious, but it does not reject otherwise valid enum
values. Agents should correct obviously wrong types before relying on filters.
