# AIC-26185 Startup Truth Surface Normalization Note

Date: 2026-04-18
Actor: A2-Core-C
Scope: `projects/aicos`

## Source

Normalized from:

```text
docs/New design/AIC-26185_codex_startup_truth_surface_normalization.md
```

## What Changed

- Root `AGENTS.md` now uses the same packet-first A2 startup path as the repo
  self-brain.
- A2-Core startup card explicitly treats
  `brain/projects/aicos/working/handoff/current.md` as the sole H1 current
  handoff index for continuation-triggered reads.
- `brain/projects/aicos/working/handoff/current.md` now explicitly says it is
  the sole current handoff index and demotes `handoff-summary.md` to
  digest/reference only.
- `brain/projects/aicos/working/handoff-summary.md` now says it is not startup
  authority.
- `brain/projects/aicos/working/current-state.md` now points to the handoff
  authority instead of restating the handoff model.
- The old migration handoff path has a redirect-only file instead of the old
  large handoff content.

## Authority Story

- Startup orientation:
  `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
- Current repo/system state:
  `brain/projects/aicos/working/current-state.md`
- Current direction:
  `brain/projects/aicos/working/current-direction.md`
- Continuation handoff:
  `brain/projects/aicos/working/handoff/current.md`
- Handoff digest/reference only:
  `brain/projects/aicos/working/handoff-summary.md`
- Old handoff provenance backup:
  `backup/handoff-provenance-20260418/`

## Intentionally Not Built

- no new registry
- no transfer/takeover subsystem
- no broad A2-Serve runtime
- no migration of all old docs
- no UI/API
