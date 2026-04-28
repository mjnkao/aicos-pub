# Runtime Agent Identity Boundary

Status: active guidance

## Problem

The same agent family can connect to more than one AICOS runtime.

Example:

- `aicos_local_private`: private/local AICOS runtime used to manage the
  private AICOS work and the `projects/aicos-pub` export/deployment project.
- `aicos_railway_public`: public Railway AICOS runtime used by public agents
  to read public AICOS context and write public feedback/status.

If an agent writes only `A1`, `A2-Core`, or `Codex`, later readers cannot tell
which runtime the identity was relative to. This can make Codex look like both
an external A1 and an internal A2 in the same conversation.

## Rule

`actor_role` is runtime-relative.

It means:

```text
Who is this actor relative to the AICOS runtime receiving this MCP call?
```

It does not mean:

```text
What is this agent globally, forever, across all AICOS runtimes?
```

## Identity Dimensions

Keep these dimensions separate:

| Dimension | Field | Examples | Meaning |
|---|---|---|---|
| Runtime | `execution_context`, `work_context` | `aicos_railway_public`, `aicos_local_private` | Which AICOS runtime and client context received the call |
| AICOS actor role | `actor_role` | `A1`, `A2-Core-C`, `A2-Core-R` | Actor class relative to that runtime |
| Agent family | `agent_family` | `codex`, `claude-code`, `openclaw` | Product/client family; never use this for A1/A2 authority |
| Agent instance | `agent_instance_id` | `codex-runtime-identity-proposal-20260428` | Unique thread/session/worker id |
| Project functional role | `work_context` or task text | `CTO`, `fullstack dev`, `reviewer` | Business/task role for the current work |
| Token label | deployment config | `codex-agent-01`, `codex-a2-core-public-railway` | Access subject used by the runtime auth policy |

## Public Railway Examples

Public agent writing feedback to public-export operations:

```json
{
  "scope": "projects/aicos-pub",
  "actor_role": "A1",
  "agent_family": "codex",
  "agent_instance_id": "codex-public-export-review-001",
  "execution_context": "codex-desktop via aicos_railway_public",
  "work_context": "runtime=aicos_railway_public; agent_position=external_agent; functional_role=reviewer"
}
```

Codex maintaining the public Railway AICOS runtime itself:

```json
{
  "scope": "projects/aicos",
  "actor_role": "A2-Core-C",
  "agent_family": "codex",
  "agent_instance_id": "codex-public-core-maintainer-001",
  "execution_context": "codex-desktop via aicos_railway_public",
  "work_context": "runtime=aicos_railway_public; agent_position=internal_agent; functional_role=runtime maintainer"
}
```

Codex maintaining private/local AICOS:

```json
{
  "scope": "projects/aicos",
  "actor_role": "A2-Core-C",
  "agent_family": "codex",
  "agent_instance_id": "codex-private-core-maintainer-001",
  "execution_context": "codex-desktop via aicos_local_private",
  "work_context": "runtime=aicos_local_private; agent_position=internal_agent; functional_role=AICOS maintainer"
}
```

## Naming Guidance

Use explicit MCP server aliases:

```text
aicos_local_private   -> private/local AICOS runtime
aicos_railway_public  -> public Railway AICOS runtime
```

Avoid ambiguous aliases such as:

```text
aicos
aicos_pub
aicos_http
```

unless the surrounding config clearly states which runtime they point to.

## Scope Guidance

Do not rename the public Railway core scope from `projects/aicos` just to solve
identity confusion. Scope names identify project context. Runtime identity
should be carried by MCP server alias, execution context, work context, and
token label.

For the current public deployment:

| Scope | Use |
|---|---|
| `projects/aicos` | Public AICOS core context served by Railway |
| `projects/aicos-pub` | Public packaging/export/deployment coordination |

## Access Guidance

Runtime-relative actor role is an audit field, not the only authorization
source.

Protected write access should come from token policy:

- external public tokens may write `projects/aicos-pub`;
- public runtime maintainer tokens may write public runtime maintenance scopes;
- private/local maintainer tokens may write private AICOS maintenance scopes.

Do not infer internal authority from `agent_family=codex`.

