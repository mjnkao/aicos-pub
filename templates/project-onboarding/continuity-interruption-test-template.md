# Continuity / Interruption Test Template

Status: shared reusable foundation

## Goal

Check whether another actor can continue a paused task cheaply.

## Scenario

1. Actor A starts a bounded real task.
2. Actor A reaches a meaningful midpoint and checkpoints.
3. Actor B starts from startup card, task packet, task state, and handoff refs.
4. Actor B continues without reading the full previous chat.

## Pass Criteria

- task state says what is done, blocked, and next
- handoff refs are small and useful
- project working state is current enough
- Actor B does not reconstruct from raw history
