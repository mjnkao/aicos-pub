# AICOS Learning Loop Effectiveness Review

Status: review memo
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Review whether the current learning loop is actively collecting useful A1/A2
feedback and whether the feedback should change retrieval eval, search routing,
or MCP/tool UX.

## Current Mechanisms

AICOS currently has:

- first-contact/startup feedback nudges;
- session-close feedback closure or `feedback_type=no_issue`;
- `aicos_record_feedback`;
- `aicos_get_feedback_digest`;
- `scripts/aicos-feedback-to-eval-digest`;
- feedback records indexed as context;
- retrieval eval cases that already cover several feedback-derived issues.

## Current Digest Snapshot

Command:

```bash
scripts/aicos-feedback-to-eval-digest --project aicos --format text
```

Latest observed result:

- feedback scanned: `15`
- actionable feedback: `4`
- new eval candidates: `0`
- area counts:
  - `auth`: `1`
  - `general`: `2`
  - `tool_schema`: `1`

## Interpretation

The loop is working mechanically:

- feedback can be written;
- feedback can be digested;
- the digest can identify whether eval coverage already exists;
- current actionable feedback does not require new retrieval eval cases.

But the loop has not yet proven that external A1 agents reliably produce
non-`no_issue` feedback in normal work. Much of the current feedback is from
A2/Codex maintenance passes.

## Useful Signals Found

| Signal | Meaning | Current action |
| --- | --- | --- |
| Auth/token health feedback already covered | A1/A2 can confuse health/eval failures with search quality | Keep eval coverage; no new case now |
| Tool schema/read shape confusion already covered | Agent may send wrong identity/query fields | Keep examples explicit; no new case now |
| Checklist state drift feedback | Agent can be misrouted by stale checklist state | Work State Ledger task now tracks root cause |
| Automation no durable output | Recurring automation is not yet reliable | Do not rely on automation; run key reviews manually |

## Current Gaps

1. **A1-specific feedback volume is still low**
   - Need more real A1 sessions before judging loop quality.

2. **Feedback prompt quality is not yet role-specific**
   - A1 manager, worker, CTO, content, design, and research roles may need
     different examples.

3. **Feedback-to-eval is manual by design**
   - This is correct for now, but A2 must actually run the digest before search
     changes.

4. **No effectiveness dashboard/read view**
   - AICOS can produce digest text, but there is no compact read surface for
     "what feedback should A2 act on next?"

## Recommendation

Do not add a heavy survey or autonomous ranking mutation.

Do add better examples and operating discipline:

1. Add A1 feedback examples for:
   - expected context missing;
   - results too broad;
   - stale result;
   - confusing schema/tool shape;
   - missing project/tool;
   - direct read vs search uncertainty.

2. Before every retrieval/search change:
   - run feedback digest;
   - run retrieval eval gate;
   - add eval cases only when feedback is repeatable or high-risk.

3. After more real A1 sessions:
   - calculate non-`no_issue` rate by `agent_family`;
   - identify whether some clients never submit feedback;
   - decide whether one additional nudge boundary is needed.

## Next Step

Keep the loop as-is for now, but add a small A1 feedback examples section to
the write cookbook or A1 onboarding docs in a later doc pass.
