# CHK-26216 Real Project Readiness Classification

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Classification

| CHK item | Classification | Implementation direction |
| --- | --- | --- |
| A1 mandatory checkpoint/writeback policy | Shared reusable foundation | Shared policy usable by A1, A2-Core, and future actor classes |
| A2 task-state convention hardening | Shared reusable foundation | Shared task-state template plus actor-lane convention notes |
| A3 `context start` hardening | Shared reusable foundation / future automation candidate | MVP support for A2-Core and generic A1 project scopes; no resolver engine |
| B1 A1 startup card | Shared reusable foundation | Generic A1 startup card with project-specific scope binding |
| B2 A1 rule cards | Shared reusable foundation | Minimal reusable rule cards, not Crypto-specific |
| B3 A1 task/startup conventions | Shared reusable foundation | A1 task-state and task-packet conventions |
| C1 project import/onboarding checklist | Shared reusable foundation | Template under shared onboarding kit |
| C2 project-to-AICOS lane mapping spec | Shared reusable foundation | Template under shared onboarding kit |
| C3 imported project bootstrap state | Shared reusable foundation + project-specific instantiation | Reusable template plus Crypto Trading placeholder bootstrap |
| D1 startup/token test plan | Shared reusable foundation | Reusable test template |
| D2 rule compliance test plan | Shared reusable foundation | Reusable test template |
| D3 continuity/interruption test plan | Shared reusable foundation | Reusable test template |
| D4 real task quality test plan | Shared reusable foundation + project-specific instantiation | Reusable template; Crypto slice remains TBD |
| CHK-26230 Crypto Trading slice recommendation | Project-specific instantiation | Record as first target only; do not hardcode into shared rules |
| scaffold/import/checklist generation helpers | Future automation candidate | Leave as future; templates are automation-ready inputs |

## Execution Rule

Build the shared reusable foundation first. Use Crypto Trading only as the first
placeholder/onboarding target, with all project-specific details isolated under
`brain/projects/sample-project/`.
