# Project To AICOS Lane Mapping Template

Status: shared reusable foundation

## Mapping Rules

- Stable reviewed project truth -> `brain/projects/<project-id>/canonical/`
- Current best understanding -> `brain/projects/<project-id>/working/`
- Raw/reference/source material -> `brain/projects/<project-id>/evidence/`
- Experiments/alternatives -> `brain/projects/<project-id>/branches/`
- Actor-owned execution tasks -> `agent-repo/classes/<actor-class>/tasks/`
- Generated serving artifacts -> `serving/`

## Source Type Mapping

| Source type | Default lane | Notes |
| --- | --- | --- |
| project profile / mission | canonical or working | canonical only after review |
| current priorities | working | keep concise |
| unresolved question | working/open-questions | do not turn into task unless owner/action exists |
| open item | working/open-items | project-level unresolved item |
| risk | working/active-risks or potential-risks | active only when evidence/impact is clear |
| raw docs / logs / outputs | evidence | not startup by default |
| implementation task | agent-repo tasks | actor-owned state |
| candidate experiment | evidence/candidate-decisions or branches | branch only after explicit selection |

## Shared vs Project-Specific

Reusable policy belongs in `brain/shared/`.
Project reality belongs in `brain/projects/<project-id>/`.
Actor execution belongs in `agent-repo/`.
