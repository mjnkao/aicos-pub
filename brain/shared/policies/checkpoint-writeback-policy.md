# Checkpoint And Writeback Policy

Status: shared reusable foundation

This policy applies to A1 project work, A2 system work, and future actor classes
unless a stricter local rule exists.

For actor identity, work lane, artifact scope, and code worktree coordination,
use:

```text
brain/shared/policies/agent-coordination-policy.md
```

## Mandatory Checkpoint Triggers

An actor must checkpoint before continuing far ahead when any of these happen:

- meaningful milestone completed
- scope, work context, project, or actor role changes
- blocked or waiting state appears
- a handoff to another actor is likely
- artifact delta becomes meaningful enough that another actor would need an
  update
- pause before a long interruption
- human decision or approval changes the current direction

More than one meaningful uncheckpointed milestone is not acceptable.

## What To Update

Update the smallest correct lanes:

- project working state: when shared project reality changes
- actor task state: when owner/status/next step/blocker changes
- handoff current: when continuation story, newest-vs-stale status, or startup
  guidance changes
- canonical: only after explicit review/promotion
- artifact checkpoint: when primary artifact(s) reach a coherent saved or
  reviewable state
- remote continuity checkpoint: when the human asks, when collaboration depends
  on a remote/shared surface, or when handoff needs remote preservation

For coding tasks, an artifact checkpoint may be a git commit and a remote
continuity checkpoint may be a push. For design, content, research, or hybrid
work, use the equivalent saved concept, draft, evidence packet, reviewable
version, or shared artifact state.

## What Not To Do

- do not write every chat turn
- do not checkpoint every shell command
- do not use vague context-length feelings as the primary trigger
- do not hide meaningful work deltas inside one actor session
- do not promote working state to canonical without review

## Minimum Checkpoint Content

At minimum, record:

- what changed
- actor identity and current owner/lane
- work type, work lane, and artifact scope
- task status
- primary artifact(s)
- meaningful work delta
- what is done
- what is blocked, if anything
- immediate next step
- artifacts or lanes touched
- whether another actor can continue cheaply
