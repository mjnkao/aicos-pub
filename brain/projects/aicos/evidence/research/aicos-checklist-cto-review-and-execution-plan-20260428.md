# AICOS Checklist CTO Review And Execution Plan

Status: CTO review / execution plan
Date: 2026-04-28
Scope: `projects/aicos`
Actor: `A2-Core-C`

## Purpose

Review whether current AICOS checklists are still aligned with the Option C
direction, identify stale or misleading checklist state, and add the next
execution plan with explicit attention to the A1 learning loop.

## CTO Judgment

The current checklist direction is still correct.

AICOS should continue toward:

- semantic/control-plane core;
- small-team provider bundle as the current implementation;
- provider boundaries instead of substrate lock-in;
- retrieval quality measured by eval and A1 feedback;
- dashboard/PM integration only after coworker/job read semantics are stable.

The main issue was not a wrong architecture direction. The issue was checklist
state drift: many baseline phases were still unchecked even though the
corresponding notes and implementation passes already exist. That can mislead a
new A1/A2 into repeating Phase 0.5, redoing search baseline work, or starting
dashboard/graph work too early.

## Checklist Review

| Area | Current state | CTO decision |
| --- | --- | --- |
| Phase 0 direction lock | materially established | keep as active guardrail |
| Phase 0.5 operating surface | good enough for continued real A1 usage | do not block architecture work on more stabilization |
| Phase 1 module inventory | completed and upgraded with current decision inventory | use as implementation guardrail |
| Phase 2 semantic core | baseline note exists | continue reducing coupling only when touching relevant code |
| Phase 3 provider boundaries | sketch exists | do not build a provider framework yet |
| Phase 4 profiles | baseline exists | current stack remains `small-team` bundle |
| Phase 5 retrieval/runtime | eval loop exists, still active | keep improving only from eval/feedback evidence |
| Phase 5.5 learning loop | partially implemented | add operating discipline and effectiveness review |
| Phase 6 coworker/dashboard model | baseline semantics exist | no UI/backend implementation yet |
| Phase 7 PM integration | contract direction exists | no connector/sync engine yet |
| Phase 8 packs | project pack exists; company/workspace packs not mature | defer until more external project evidence |

## Learning Loop Review

Current proactive mechanisms:

- startup/first-contact can return `feedback_loop.ask_now=true`;
- session-close continuity writes require feedback closure or
  `feedback_type=no_issue`;
- A1/A2 can write structured feedback through `aicos_record_feedback`;
- agents can read feedback digest through `aicos_get_feedback_digest`;
- `scripts/aicos-feedback-to-eval-digest` turns feedback records into candidate
  eval items for A2 review;
- feedback files are searchable context;
- retrieval eval corpus already includes feedback/search/tool-shape cases.

This is enough for a lightweight loop, but not yet enough to prove that real A1
agents will reliably send useful feedback. The current loop asks and gates at
important boundaries, but the system still needs an effectiveness review after
more real A1 sessions.

The right next improvement is not a heavy survey or autonomous ranking update.
It is:

1. keep first-contact and session-close prompts;
2. run feedback digest before search/tooling changes;
3. promote repeated/high-risk A1 misses into eval cases;
4. review whether actual A1 sessions produce non-`no_issue` feedback;
5. add one additional nudge boundary only if feedback remains absent despite
   known friction.

## Execution Plan

### P0 — Keep Current Guardrails Fresh

- Keep Option C, module decision inventory, semantic boundary, and provider
  sketch as the architecture anchors.
- Keep relation graph, dashboard, PM connector, and PG-as-truth deferred unless
  new evidence changes the decision.
- Keep `aicos-current-module-decision-inventory-20260428.md` as the concrete
  implementation guardrail.

### P1 — Learning Loop Effectiveness Pass

- Run feedback digest before future retrieval/tooling changes.
- Check whether recent A1 sessions produce real friction feedback or only
  `no_issue`.
- Add eval cases only for repeated or high-risk misses.
- Add explicit A1 prompt examples for:
  - missing expected context;
  - overly broad results;
  - stale results;
  - confusing schema;
  - missing project/tool.

### P2 — Runtime/Security Readiness

- Review token scope clarity and protected write scopes.
- Decide practical next action for SSE/HTTPS auth interop.
- Decide whether single-machine SPOF is acceptable for the next small-team
  period or needs a fallback profile.
- Fix monitor noise only when it creates real false-alert friction.

### P3 — Project Intake Productization

- Keep the project proposal MCP tool.
- Add the minimum approval/import path:
  project proposal -> approval -> project brain pack creation/import ->
  registry entry -> token/access policy.
- Do not build company/workspace pack framework until at least two projects
  need the same abstraction.

### P4 — Coworker/Job Read Views

- Build only read-only views first:
  active workers, active lanes, takeover-ready items, human attention queue,
  project board summary.
- Derive from status/task/handoff/checkpoint/feedback.
- Do not create first-class job truth until repeated usage proves the view is
  the right abstraction.

### P5 — Dashboard / PM Integration Later

- Use Phase 6 and Phase 7 notes as contract anchors.
- Start with export/read-only integration before any bidirectional sync.
- Keep AICOS semantic authority over source refs, handoff, agent identity, and
  context truth.

## What Not To Do Next

- Do not restart Phase 0.5 unless a real client breaks.
- Do not add `aicos_get_related_context` until adjacency misses repeat.
- Do not build a graph/page schema engine now.
- Do not build dashboard/backend logic inside the MCP daemon.
- Do not convert PostgreSQL/GBrain into truth under the current direction.
- Do not create a generic provider plugin framework before current seams force
  it.

## References

- `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-current-module-decision-inventory-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-search-learning-loop-assessment-20260428.md`
- `brain/projects/aicos/evidence/research/aicos-phase-0-5-learning-loop-check-20260428.md`
- `brain/projects/aicos/working/status-items/aicos-feedback-closure-gate.md`
