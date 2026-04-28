# Rule Card: Sync Brain

Load when retrieval/query needs current `brain/` state.

## Command

```text
./aicos sync brain
```

## Use After

- manager choice committed
- working state changed materially
- branch selected or updated
- milestone completed
- another agent needs fresh retrieval

## Sync Scope

Default source: `brain/`

Excluded by default:

- `agent-repo/`
- `backend/`
- `backup/`
- `imports/`
- `scripts/`
- `integrations/`

## Boundary

Sync is serving refresh into GBrain/PGLite. It does not mutate truth, promote
state, or manage external co-worker memory.
