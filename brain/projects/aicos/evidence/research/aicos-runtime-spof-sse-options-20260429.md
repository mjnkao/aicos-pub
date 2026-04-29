# AICOS Runtime SPOF / SSE / LAN Reliability Options

Status: options memo, no implementation
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Summarize practical options for AICOS runtime reliability and client
interoperability without implementing infrastructure changes yet.

Related status items:

- `ARCH-SINGLE-MACHINE-SPOF`
- `RISK-LAN-AGENT-FALLBACK`
- `AICOS-LAN-SECURITY-HARDENING`
- `AICOS-MCP-SSE-AUTH-INTEROP`

## Current State

Current small-team bundle:

- one local Mac host;
- HTTP MCP daemon;
- Postgres.app / PG hybrid search;
- token-based auth;
- local stdio/proxy paths for some clients;
- HTTPS proxy special case for local clients that need it.

This is acceptable for solo/small-team MVP, but fragile for wider team use.

## Options

| Option | Description | Pros | Cons | Fit |
| --- | --- | --- | --- | --- |
| A. Accept/document current SPOF | Keep one host, rely on git push discipline and restart docs | Lowest cost, no architecture churn | Host sleep/crash breaks LAN agents; no SLA | Solo/small-team now |
| B. Add operational discipline only | Keep one host, add clearer runbook, push reminders, health checks, manual restart path | Low risk, helps current users | Still SPOF | Best immediate option |
| C. Secondary read-only daemon/replica | Another machine can serve read-only context/search from pushed brain | Better fallback for reads | More sync complexity, write conflicts still unsolved | Later small team |
| D. VPS/cloud daemon | Always-on daemon with managed runtime and network access | Better availability, easier remote team access | Security, secrets, deployment, cost, ops | Company-100 direction |
| E. Full HA/provider runtime | Multi-node, queues, DB replication, auth provider | Strong reliability | Too heavy now | Future only |

## SSE/Auth Interop Options

| Option | Description | Pros | Cons | Recommendation |
| --- | --- | --- | --- | --- |
| Keep localhost HTTPS proxy special case | Same-machine clients use local proxy where headers are hard | Works now, contained | Does not solve non-local headerless clients | Keep short-term |
| Streamable HTTP/session bootstrap | First request exchanges token/capability for session-compatible transport | Cleaner for clients that cannot set headers | Needs design and security review | Research later |
| Query-param token fallback | Put token in URL for headerless clients | Easy | Leaks secrets in logs/history; bad security | Avoid except temporary local-only |
| Per-client stdio wrapper | Use local wrapper/proxy where possible | Preserves auth boundary | Client-specific install burden | Accept for desktop clients |

## Recommendation

Near term:

1. Choose Option B:
   - document current SPOF explicitly;
   - maintain push discipline;
   - keep daemon health checks;
   - keep local HTTPS/stdout adapters for compatibility.

2. Do not build secondary daemon or VPS deployment until:
   - more than one human/operator depends on AICOS concurrently;
   - remote agents need reliable always-on MCP;
   - or daemon downtime blocks real A1 work repeatedly.

3. Treat SSE/auth interop as a design follow-up, not an urgent runtime change.

## Trigger To Reopen

Reopen for implementation when any of these happen:

- remote A1 agents repeatedly fail because host is asleep/offline;
- a company/team pilot needs non-local access;
- one-machine downtime causes lost work, not just temporary inconvenience;
- a client cannot work through header auth/proxy/stdio options.
