# AICOS Feedback To Eval Digest

Generated at: `2026-04-28T14:55:21+00:00`
Project: `aicos-pub`

## Summary

- Feedback records scanned: `16`
- Actionable feedback records: `2`
- Eval candidate records: `2`
- New eval candidates: `0`

## Area Counts

- `auth`: `2`

## Candidate Eval Cases

### Clarify Antigravity MCP Config for Stdio vs HTTP SSE

- Source: `brain/projects/aicos-pub/working/feedback/20260423t171257z-f082f2d2be.md`
- Area: `auth`
- Feedback type: `bootstrap_confusing`
- Severity: `medium`
- Already covered by eval: `true`
- Should add eval case: `false`
- Candidate question: how should an A1 or A2 check AICOS MCP auth/token setup when a health or eval command fails?
- Expected answer shape: Please update AICOS_MCP_AGENT_INSTALL.md under 'Antigravity / Gemini IDE Setup'. It should explicitly show both configurations: 1. Local Stdio: using 'command' and 'args'. 2. LAN HTTP/SSE: using 'serverUrl' (instead o...

### Proposal for A2: clarify runtime-relative agent identity

- Source: `brain/projects/aicos-pub/working/feedback/20260428t104022z-d695d970c9.md`
- Area: `auth`
- Feedback type: `other`
- Severity: `medium`
- Already covered by eval: `true`
- Should add eval case: `false`
- Candidate question: how should an A1 or A2 check AICOS MCP auth/token setup when a health or eval command fails?
- Expected answer shape: Do not rename public projects/aicos. Instead implement runtime identity boundary: rename MCP configs to aicos_local_private and aicos_railway_public, document actor_role as runtime-relative, require runtime_context/wo...

## Boundary

Digest only. It proposes eval additions; it does not mutate the retrieval corpus automatically.
