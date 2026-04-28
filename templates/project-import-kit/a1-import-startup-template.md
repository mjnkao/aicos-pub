# A1 Import Startup Template

Status: shared reusable template

Purpose: define the minimum A1 startup surfaces for an imported project.

## A. Startup Entry

- expected command: `./aicos context start A1 projects/<project-id>`
- scope:
- role:
- project id:

## B. Startup Reading Boundary

Read by default:

- A1 startup card
- project profile
- project current state
- project current direction
- packet index

Not read by default:

- full external repo
- archives/history
- raw evidence bundles
- all task packets
- all handoffs
- MCP/runtime internals

Packet-first condition:

- load one task packet only after task selection or strong implication

Conditional handoff:

- read `working/handoff/current.md` only for continuation, interruption
  recovery, migration/state alignment, or newest-vs-stale checks

## C. First Packet Surfaces

- first review/import packet:
- startup validation packet:
- optional continuation packet:
- packet index path:

## D. External Work Context

- isolated checkout path:
- branch:
- checkout authority:
- AICOS authority:
- rule for current working folder:

## E. Continuity Expectation

- working files to trust:
- handoff file to trust:
- when second A1 can continue:
- metadata required for cheap continuation:

## Rule

The project is usable for A1 only when startup path is explicit and light.
