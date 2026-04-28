# Import Master Checklist Template

Status: shared reusable template

Purpose: coordinate one bounded external project import pass without becoming
the project truth itself.

## A. Import Overview

- source repo:
- source branch:
- target AICOS project id:
- import actor:
- import date:
- current status:

## B. Import Mode

- mode: full active context / slice-first / other
- first slice name:
- reason for current mode:
- explicit out-of-scope areas:

## C. Isolated Checkout Gate

- isolated checkout path:
- source branch confirmed in isolated checkout: yes/no/TBD
- checkout independent from current working folder: yes/no/TBD
- current folder must not be mutated: yes/no/TBD

## D. Required Companion Files

- identity file:
- source inventory:
- authority and lane mapping:
- slice definition:
- active context include/exclude checklist:
- bootstrap output checklist:
- A1 import startup:
- import validation:

## E. Worker Separation

- kit maintainer:
- independent import executor:
- optional later A1 importer:
- old thread context allowed: no

## F. Current Pass Status

- [ ] not started
- [ ] in source inventory
- [ ] in digestion
- [ ] in startup validation
- [ ] validated for A1
- [ ] paused / blocked

## G. Completion Gate

- [ ] isolated checkout confirmed
- [ ] full active context include set selected
- [ ] excluded historical/reference set selected
- [ ] canonical digest done
- [ ] working digest done
- [ ] delivery/runtime surface digest done
- [ ] evidence/reference recorded
- [ ] A1 packet/startup ready
- [ ] validation recorded
- [ ] independent worker can start without old-thread context

## Rule

This checklist is the first import-status surface for a project-specific import
cluster. It is evidence/control, not canonical truth.
