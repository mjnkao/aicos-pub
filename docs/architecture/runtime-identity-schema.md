# Runtime Identity Schema

Status: active contract

## Purpose

AICOS can run as more than one runtime: private/local, public Railway,
company-hosted, or future team deployments. `A1` and `A2` are not global
identities. They are actor roles relative to the AICOS runtime receiving a
read/write call.

This schema keeps that boundary explicit without making normal A1 writes heavy.

## Required For Every MCP Write

Every semantic write must include `runtime_context`.

```yaml
runtime_context:
  runtime: private-local-aicos       # runtime receiving this MCP call
  mcp_name: aicos_local_private      # client-side MCP server alias
  agent_position: external_agent     # external_agent | internal_agent | human_operator | system
  functional_role: reviewer          # optional task/business role
```

For A1 agents, this lightweight object is enough.

## Required For Every A2 MCP Write

Every write with `actor_role` beginning with `A2-` must also include
`runtime_identity_map`.

```yaml
runtime_identity_map:
  identity_private:
    runtime: private-local-aicos
    mcp_name: aicos_local_private
    project_scope: projects/aicos-pub
    agent_position: external_agent
    actor_role: A1
    functional_role: CTO/fullstack dev of aicos-pub
  identity_public:
    runtime: public-railway-aicos
    mcp_name: aicos_railway_public
    project_scope: projects/aicos
    agent_position: internal_agent
    actor_role: A2-Core-C
    functional_role: CTO/fullstack dev of public AICOS
```

Use map keys that are meaningful in the handoff, such as
`identity_private`, `identity_public`, `identity_company`, or
`identity_current`.

## Field Meanings

| Field | Required | Meaning |
|---|---:|---|
| `runtime` | yes | Stable runtime name, not necessarily a hostname |
| `mcp_name` | yes | Client-side MCP server alias |
| `project_scope` | A2 map only | Scope where this identity applies |
| `agent_position` | yes | Relation to that runtime |
| `actor_role` | A2 map only | Runtime-relative AICOS actor role |
| `functional_role` | A2 map yes, context optional | Business/task role |

Allowed `agent_position` values:

```text
external_agent
internal_agent
human_operator
system
```

## Why This Is Structured

Free-form `work_context` was not enough. Agents could write:

```text
Codex / A2 / aicos-pub
```

and later readers could not tell whether that meant:

- Codex as external A1 relative to private/local AICOS, working on public
  export; or
- Codex as internal A2 relative to public Railway AICOS, maintaining that
  runtime.

`runtime_context` and `runtime_identity_map` make that distinction machine
readable and visible in status, handoff, feedback, and checkpoint records.

## Compatibility

`work_context`, `execution_context`, `actor_family`, and `logical_role` remain
accepted as legacy/compact context fields. They do not replace the structured
runtime identity fields.

