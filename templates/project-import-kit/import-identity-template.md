# Import Identity Template

Status: shared reusable template

Purpose: identify what is being imported, from where, into which AICOS project,
and under which authority boundary.

## A. Source Identity

- external repo name:
- external repo URL:
- source branch:
- isolated local checkout path:
- path independence from existing working folder:
- current source authority statement:

## B. AICOS Identity

- target AICOS project id:
- target lane root: `brain/projects/<project-id>/`
- import owner / actor lane:
- current import status:

## C. First-Slice Decision

- slice name:
- slice reason:
- pass phase:
- excluded broad scope:

## D. Import Scope Mode

- mode: full active context / slice-first / other
- active context means:
- excluded history/reference means:
- why this mode is appropriate:

## E. Worker Separation

- kit maintainer:
- independent import executor:
- optional later A1 importer:
- old thread context allowed: no

## F. Authority Split

External repo keeps authority for:

- code/runtime:
- scripts/tests:
- environment/bootstrap:
- generated runtime artifacts:
- repo-local implementation files:

AICOS imports/digests authority for:

- project truth:
- working state:
- handoff/current:
- open questions/items/risks:
- A1 packets/continuity:

Future bridge role:

- local MCP expected later: yes/no/TBD
- optional `.aicos/` cache expected later: yes/no/TBD

## Rule

This file must let a new agent answer: what is being imported, from where, into
where, and what remains outside AICOS authority.
