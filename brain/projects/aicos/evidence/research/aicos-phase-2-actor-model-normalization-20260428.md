# AICOS Phase 2 Actor Model Normalization

Status: phase-2 baseline
Date: 2026-04-28
Scope: projects/aicos
Actor: A2-Core-R/C

## Purpose

Normalize the AICOS actor model so `A1` / `A2` remains a service-boundary
taxonomy for AICOS, not a universal project role system imposed on every
company or project that uses AICOS.

## Core Rule

AICOS must separate four role/access dimensions:

1. **AICOS-internal actor class**
2. **Project-facing functional role**
3. **Service relationship role**
4. **Access subject / token label**

These dimensions may be held by the same human or agent at the same time, but
they must not be collapsed into one label.

## Dimension 1 — AICOS-Internal Actor Class

This answers:

> Is this actor using AICOS, or improving AICOS?

Current classes:

| Class | Meaning | Used by |
| --- | --- | --- |
| `A1` | External work actor using AICOS as context/control-plane service | Agents or humans doing company/workspace/project work |
| `A2-Core-R` | Internal AICOS reasoning/architecture actor | AICOS architecture, policy, tradeoff, review |
| `A2-Core-C` | Internal AICOS coding/build/config actor | AICOS code, repo, scripts, integration, runtime |
| `A2-Serve` | Future service-quality actor | Retrieval, capsule, feedback, option quality |
| `Human` | Human manager/reviewer/approver/operator | Decisions, review, approval, direction |

Rule:

- Only actors working on AICOS itself need to reason deeply about `A1`/`A2`.
- For other projects, AICOS can treat outside agents as `A1` for service
  boundary purposes, without forcing the project to adopt the A1/A2 taxonomy.

## Dimension 2 — Project-Facing Functional Role

This answers:

> What job is the actor doing inside the company/project/task?

Examples:

- CTO
- Architect
- Tech Lead
- Fullstack Developer
- QA
- Product Owner
- Researcher
- Designer
- Content Writer
- Marketer
- Operations Manager
- Reviewer
- Domain specialist

Rule:

- functional role belongs to the project/company context;
- it may change task by task;
- AICOS should store it as `logical_role`, `project_role`, task metadata, or
  a project-owned role field, not as `agent_family`;
- AICOS should not hardcode one global list of functional roles.

## Dimension 3 — Service Relationship Role

This answers:

> What is the actor's relationship to AICOS as a service?

Examples:

- internal AICOS maintainer;
- external work actor;
- human manager;
- human approver;
- read-only observer;
- automation/job actor;
- connector/import actor.

Rule:

- service relationship determines permissions, write surfaces, audit
  expectations, and fallback rules;
- it does not determine the professional/functional role of the actor.

## Dimension 4 — Access Subject / Token Label

This answers:

> Which credential is making this request, and what scopes may it read/write?

Examples:

- `antigravity`
- `openclaw-vm`
- `claude-code`
- `a2-core-c`
- `reserved-01`

Rule:

- token labels are access subjects, not product families and not professional
  roles;
- product/client names such as `codex`, `claude-code`, `antigravity`, or
  `openclaw` do not automatically mean internal authority;
- protected AICOS service scopes such as `projects/aicos` require an explicit
  maintainer access label such as `a2-core-c`, or an explicit
  `AICOS_DAEMON_TOKEN_SCOPE_POLICY` grant;
- clients may still send `agent_family=codex` while using an `a2-core-c`
  maintainer token, because `agent_family` describes the client/tool and token
  label describes access authority.

## Required Identity Fields

Current MCP identity fields should be interpreted as follows:

| Field | Meaning | Must not mean |
| --- | --- | --- |
| `actor_role` | AICOS service-boundary actor lane such as `A1`, `A2-Core-C`, `A2-Core-R` | client family or profession |
| `agent_family` | client/tool/product family such as `codex`, `claude-code`, `gemini-antigravity`, `openclaw` | A1/A2 role class |
| `agent_instance_id` | per-thread/per-worker/per-session id for audit/handoff correlation | human-friendly role title |
| `logical_role` | optional functional role in the task/project | AICOS permission class |
| `work_type` | kind of work being performed | actor class |
| `work_lane` | coordination lane shared across handoff/status/audit | project role |
| `execution_context` | where the agent is running | authority or permission class |

HTTP daemon token labels should be interpreted separately:

| Token label | Meaning | Must not mean |
| --- | --- | --- |
| `a2-core-c` | Maintainer access subject allowed to write protected AICOS service scopes | client family |
| `antigravity`, `openclaw-vm`, `claude-code` | External/client access subjects unless explicitly granted otherwise | AICOS internal authority |
| `reserved-*` | Unassigned access subject | project role |

## Examples

### sample project trading project

An OpenClaw agent implementing a Telegram pipeline feature:

```yaml
actor_role: A1
agent_family: openclaw
agent_instance_id: openclaw-vm-telegram-001
logical_role: backend engineer
work_type: code
work_lane: telegram-pipeline
execution_context: openclaw-vm
```

The project may call this actor a backend engineer, quant engineer, or infra
engineer. AICOS only needs `A1` to know it is an external work actor using the
context/control-plane.

### AICOS project

Codex editing the MCP daemon:

```yaml
actor_role: A2-Core-C
agent_family: codex
agent_instance_id: codex-thread-20260428-mcp-daemon
logical_role: MCP engineer
work_type: code
work_lane: aicos-mcp-daemon
execution_context: codex-desktop
```

Here `A2-Core-C` matters because the work target is AICOS itself.

### Product/architecture review

Codex acting as CTO/co-founder for AICOS architecture:

```yaml
actor_role: A2-Core-R
agent_family: codex
agent_instance_id: codex-thread-20260428-option-c
logical_role: CTO
work_type: planning
work_lane: aicos-architecture-option-c
execution_context: codex-desktop
```

`CTO` is the functional lens; `A2-Core-R` is the AICOS service boundary.

## Policy Consequences

1. A1 agents must use HTTP MCP for AICOS-facing reads/writes when available.
2. A1 agents must not directly write markdown continuity into AICOS by habit.
3. Only A2-Core-R/C may fallback to direct markdown/file writes, and only when
   HTTP MCP is blocked or the task is restructuring AICOS internals.
4. External projects do not need to teach their agents the full AICOS internal
   A1/A2 taxonomy; their setup docs should translate it into "use AICOS as
   context/control-plane service."
5. Dashboard/PM integrations should show human-readable functional roles, while
   preserving AICOS actor/service fields for audit and permissions.
6. Provider implementations must preserve these dimensions rather than
   flattening them into user name, bot name, or task assignee.
7. Protected write authorization must be enforced from token/access policy, not
   from untrusted request fields such as `actor_role` or `agent_family`.

## Anti-Patterns

Avoid:

- using `agent_family=A1`;
- using `actor_role=codex`;
- using `A1` as a project profession;
- making every external company adopt `A2-Core-C`;
- encoding permissions only through functional roles like "CTO";
- making a PM tool assignee field the only actor identity;
- treating a model family as authority or permission level.
- allowing `actor_role=A2-Core-C` to write protected scopes unless the token
  label is also authorized.

## Refactor Implications

Near-term:

- keep the current MCP fields;
- clarify docs and examples;
- avoid expanding the actor taxonomy until real projects need it.
- keep the small token-label scope authorization in the daemon for protected
  AICOS writes;
- do not introduce a full RBAC system until company/team requirements need it.

Later:

- introduce a formal `service_role` or equivalent if `actor_role` becomes too
  overloaded;
- allow project-specific role registries without putting them in core AICOS
  taxonomy;
- expose dashboard-friendly role labels separately from audit/permission
  fields.

## Scalability / Bloat Judgment

This normalization keeps AICOS scalable because it avoids forcing every
company/project into AICOS's internal maintenance taxonomy.

It also avoids overbuilding now:

- no new role registry is required yet;
- no RBAC framework is required yet;
- no dashboard model is required yet;
- no provider code is required yet.

The only near-term requirement is discipline in MCP payloads, docs, and future
schema examples.
