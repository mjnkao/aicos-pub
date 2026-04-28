# AICOS Local MCP Agent Install Packet

Status: operator-copy install packet

Use this file when a new agent, IDE, or assistant needs a compact install
packet for connecting to AICOS.

This packet is self-contained. The agent should not need to inspect the AICOS
repo before installing the MCP server.

## What This Installs

This packet covers both:

- local stdio MCP through `aicos_mcp_stdio.py`
- host/LAN HTTP MCP through `aicos_mcp_daemon.py`

The local stdio server is:

```text
<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

The server exposes AICOS context/control-plane tools:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_packet_index`
- `aicos_get_task_packet`
- `aicos_get_status_items`
- `aicos_get_workstream_index`
- `aicos_get_context_registry`
- `aicos_get_project_registry`
- `aicos_get_feedback_digest`
- `aicos_get_project_health`
- `aicos_query_project_context`
- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`
- `aicos_update_status_item`
- `aicos_register_artifact_ref`
- `aicos_record_feedback`

Authority model:

- AICOS is the context/control-plane authority.
- The project checkout is the code/runtime authority.
- Existing project docs or context folders are source evidence/reference unless
  AICOS explicitly promotes them into current project context.

## Requirements

- Local machine has an AICOS repo checkout.
- `python3` is available.
- The client supports local stdio MCP servers.
- The client is allowed to run local commands.

Before writing MCP config, determine the local AICOS repo path and replace
`<AICOS_REPO_PATH>` everywhere in this packet.

If this file is being read from inside the repo, the AICOS repo path is the
directory that contains:

```text
AGENTS.md
integrations/local-mcp-bridge/aicos_mcp_stdio.py
packages/aicos-kernel/
brain/projects/aicos/
```

If the client asks for permission, allow running:

```text
python3 <AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

## Choose The Right Client Path

Use the smallest correct path for the client:

- `Claude Desktop`
  - use local `stdio`
- `Claude Code`
  - local machine: prefer `HTTP-first` wrapper with stdio fallback
  - LAN/VM: direct HTTP if headers work
- `Codex Desktop`
  - prefer direct HTTP / Streamable HTTP
- `Antigravity / Gemini IDE`
  - local machine: `stdio`
  - LAN/VM: HTTP/SSE config using `serverUrl` + `headers`
- generic MCP clients
  - local machine: `stdio`
  - LAN/VM: direct HTTP if custom headers are supported

## Generic Local Stdio MCP Config

Add this server as `aicos` in the client's MCP configuration:

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ],
      "cwd": "<AICOS_REPO_PATH>",
      "env": {}
    }
  }
}
```

If the client does not support `cwd`, omit it. The server resolves the AICOS
repo from the script path.

## Generic Team / LAN HTTP Mode

Use stdio for the default single-machine setup. Use HTTP mode only when a
single AICOS machine should serve multiple agents or people on a trusted LAN.

On the AICOS machine:

```bash
cd <AICOS_REPO_PATH>
cd integrations/mcp-daemon && docker compose up -d && cd ../..
export OPENAI_API_KEY="<optional-for-embedding-search>"
export AICOS_DAEMON_TOKEN="<shared-secret>"
python3 integrations/mcp-daemon/aicos_mcp_daemon.py --host 0.0.0.0 --port 8000
```

Default daemon bind is `127.0.0.1`. Passing `--host 0.0.0.0` intentionally
opens it to the LAN. Keep `AICOS_DAEMON_TOKEN` set for LAN mode. Current daemon
build refuses non-loopback bind without token unless explicitly started with
`--allow-unauthenticated-lan` on an isolated trusted network.

Search preference in HTTP mode is PostgreSQL hybrid search with pgvector
embeddings when PostgreSQL, pgvector, and `OPENAI_API_KEY` are available. If
embedding is unavailable, the daemon falls back to PostgreSQL FTS; if
PostgreSQL is unavailable, it falls back to markdown-direct search.

Health check from another machine:

```bash
curl -H "Authorization: Bearer <shared-secret>" http://<AICOS_HOST_OR_IP>:8000/health
```

If the client supports HTTP MCP:

```bash
claude mcp add --transport http aicos http://<AICOS_HOST_OR_IP>:8000/mcp
```

If the client does not support HTTP MCP yet, keep using local stdio on the same
machine as the AICOS checkout.

## Optional CLI Symlink

If the agent or operator needs `aicos ...` to work outside the repo root, run:

```bash
cd <AICOS_REPO_PATH>
./aicos install cli --bin-dir ~/.local/bin
```

Ensure `~/.local/bin` or the chosen bin directory is on `PATH`. The symlink
points to `<AICOS_REPO_PATH>/aicos`, which resolves the repo root from the
wrapper location.

## Claude Desktop Setup

Use local stdio. This is the stable path for Claude Desktop.

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ]
    }
  }
}
```

If Claude Desktop supports only its custom remote connector UI, do not try to
force LAN bearer-header auth through OAuth fields. Use the host-local HTTPS
adapter only when that path has been configured intentionally on the AICOS
machine.

## Claude Code Setup

### Claude Code local machine: HTTP-first with stdio fallback

Preferred:

```bash
claude mcp add aicos -- python3 <AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_http_first.py
```

This path:

- tries the local daemon first
- falls back to stdio if the daemon is down

### Claude Code LAN / VM direct HTTP

If Claude Code is running on another machine or VM and can attach headers:

```bash
claude mcp add --transport http aicos http://<AICOS_HOST_OR_IP>:8000/mcp -s user
```

It must send:

```text
Authorization: Bearer <AICOS_DAEMON_TOKEN>
```

## Codex Setup

### Codex Desktop direct HTTP

Preferred:

```text
Name: aicos_http
Transport: Streamable HTTP
URL: http://<AICOS_HOST_OR_IP>:8000/mcp
Headers:
  Authorization: Bearer <AICOS_DAEMON_TOKEN>
```

For localhost setups where loopback auth is disabled, the header may be omitted.

### Codex stdio fallback

If the Codex client cannot use HTTP, use:

```bash
codex mcp add aicos -- python3 <AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

## Antigravity / Gemini IDE Setup

Antigravity supports two useful AICOS paths:

1. local stdio, when the IDE runs on the same machine as the AICOS checkout
2. remote HTTP/SSE, when the IDE runs in a VM or on another machine and talks
   to the host AICOS daemon

### Antigravity local stdio

If Antigravity can run a local MCP command, use the same stdio server as other
local clients:

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ],
      "cwd": "<AICOS_REPO_PATH>",
      "env": {}
    }
  }
}
```

### Antigravity LAN HTTP/SSE

If Antigravity is connecting to the AICOS host daemon over VM/LAN, use the
HTTP/SSE connector shape that Antigravity expects.

Important:

- use `serverUrl`, not `url`
- pass bearer auth through `headers`
- do not put the token in the URL
- do not use `?token=...`

Example:

```json
{
  "mcpServers": {
    "aicos": {
      "serverUrl": "http://<AICOS_HOST_OR_IP>:8000/mcp",
      "headers": {
        "Authorization": "Bearer <AICOS_DAEMON_TOKEN>"
      }
    }
  }
}
```

If Antigravity is running in the common macOS VM-bridge setup used in this
repo, the host URL is usually:

```text
http://192.168.64.1:8000/mcp
```

Use the client UI if available:

1. Open the Agent panel.
2. Open MCP Servers / Manage MCP Servers.
3. Open the raw MCP config.
4. Add either the local stdio config or the HTTP/SSE config above.
5. Save and enable the server.

Then ask the agent to list MCP tools. It should see the `aicos_*` tools.

If Antigravity silently loads no tools:

- check that the config uses `serverUrl` and not `url`
- check that `headers.Authorization` includes the `Bearer ` prefix
- run the health check first:

```bash
curl -H "Authorization: Bearer <AICOS_DAEMON_TOKEN>" http://<AICOS_HOST_OR_IP>:8000/health
```

- then restart or refresh the Antigravity MCP runtime

## Gemini CLI Setup

Add the same `mcpServers.aicos` entry to one of these files:

- Project-level: `<client-settings>/settings.json`
- User-level: `~/<client-settings>/settings.json`

Project-level example:

```json
{
  "mcpServers": {
    "aicos": {
      "command": "python3",
      "args": [
        "<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py"
      ],
      "cwd": "<AICOS_REPO_PATH>",
      "env": {}
    }
  }
}
```

If Gemini has an allow-list for MCP servers, include `aicos`.

## Local Stdio Smoke Test

If the agent has terminal access, it may run this from `<AICOS_REPO_PATH>`:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"aicos_get_startup_bundle","arguments":{"actor":"A1","scope":"projects/sample-project"}}}' \
  | python3 integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

Expected result:

- the tools list includes `aicos_get_startup_bundle`;
- the startup bundle returns sample project project context;
- the startup bundle includes `mcp_contract_status`;
- the sample project project mode says AICOS-managed or equivalent current context.

## Doctor

From `<AICOS_REPO_PATH>`:

```bash
./aicos mcp doctor
./aicos mcp doctor --mode daemon --daemon-url http://127.0.0.1:8000
./aicos mcp doctor --mode daemon --daemon-url http://<AICOS_HOST_OR_IP>:8000 --token <shared-secret>
```

Use doctor before asking an agent to write if the MCP install was just changed,
the daemon was restarted, or the agent may have cached an old tool schema.

## Required First AICOS Read

After installing, the agent must read AICOS before doing project work.

For sample project:

```json
{
  "tool": "aicos_get_startup_bundle",
  "arguments": {
    "actor": "A1",
    "scope": "projects/sample-project"
  }
}
```

Then:

```json
{
  "tool": "aicos_get_packet_index",
  "arguments": {
    "actor": "A1",
    "scope": "projects/sample-project"
  }
}
```

If a selected task packet exists:

```json
{
  "tool": "aicos_get_task_packet",
  "arguments": {
    "actor": "A1",
    "scope": "projects/sample-project",
    "packet_id": "<packet-id>"
  }
}
```

## Prompt To Give The Agent After Install

Copy this prompt to the new agent after the `aicos` MCP server is installed:

```text
You are an A1 worker connected to AICOS through the local MCP server named
`aicos`.

Before doing project work, call:

1. `aicos_get_startup_bundle`
   actor: `A1`
   scope: `projects/sample-project`

2. `aicos_get_packet_index`
   actor: `A1`
   scope: `projects/sample-project`

Summarize the returned project mode, authority boundaries, current direction,
and available task packets.

Read `mcp_contract_status` from the startup bundle. If it says
`write_schema_refresh_required: true` and your client cached tools before this
session or before a known AICOS update, refresh/list MCP tools again or
restart/re-enable the `aicos` MCP server before writing. Do not add a heavy
preflight before every write during a normal short session.

Current write contract acknowledgment:

```yaml
mcp_contract_ack: "mcp-v0.5-write-contract-ack"
```

Every MCP write must include this field. If a write fails with
`write_contract_ack_required`, your client is using a stale write schema:
refresh/list tools or restart/re-enable the `aicos` MCP server, then retry.
Do not fall back to older write patterns.

Use AICOS/MCP as the project context/control-plane authority.
Use the project checkout only as the code/runtime authority.
Do not write new AICOS-facing continuity into the project repo by habit.

When you finish meaningful work, write continuity back through AICOS MCP using:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update` only for compact current-continuity handoff
  updates
- `aicos_update_status_item` when changing the status of an open item, open
  question, tech debt item, or decision follow-up
- `aicos_register_artifact_ref` when the durable artifact lives outside AICOS
  and AICOS only needs a compact ref plus relevance summary
- `aicos_record_feedback` when context serving, routing, policy, role fit, or
  query behavior was confusing or insufficient

Do not use `aicos_write_handoff_update` as a fallback for open items, open
questions, tech debt, decision follow-ups, or backlog-like status lists. If
`aicos_update_status_item` is missing from your available tools, your MCP
client is stale or incomplete: refresh/list tools or restart/re-enable the
AICOS MCP server before writing. If it is still missing, report the blocker
instead of normalizing status-item writes into handoff.

Do not use feedback writes as a substitute for task state, handoff, status-item
lifecycle, or canonical policy changes. Feedback is a learning signal for AICOS
improvement.

Every read/write must include agent identity. For external agents, AICOS treats
the service actor as `A1` by default.

- Read tool `actor` is optional. If present, it is the AICOS service actor, not
  the client name. External clients may omit it or send their client name;
  AICOS normalizes non-explicit A2 values to `A1`.
- Use `agent_family` for the client/product family, for example
  `antigravity`, `claude-code`, `codex`, or `openclaw`.
- External/A1 client tokens must not write protected AICOS service scopes such
  as `projects/aicos`. The daemon enforces this by token label. Only labels in
  `AICOS_DAEMON_INTERNAL_TOKEN_LABELS` or labels explicitly granted through
  `AICOS_DAEMON_TOKEN_SCOPE_POLICY` may write those scopes.
- Token labels are access subjects, not product families. Do not treat
  `codex`, `claude-code`, `antigravity`, or `openclaw` as internal authority
  by default. Use a dedicated role/access label such as `a2-core-c` for
  AICOS-maintainer write authority.

Every write must include actor identity:

- `mcp_contract_ack`: current write-contract value from
  `mcp_contract_status.write_contract_ack_value`
- `actor_role`: role lane, for example `A1` or `A2-Core-C`
- `agent_family`: client/agent family, for example `codex`,
  `claude-code`, `gemini-antigravity`, or `openclaw`
- `agent_instance_id`: unique session/instance id for this agent run
- `work_type`: one of `code`, `content`, `design`, `research`, `ops`,
  `review`, `planning`, `data`, `mixed`, or `orientation`
- `work_lane`: generic coordination lane. For code, this may match a git
  branch. For non-code, use a doc/design/research/campaign/review lane.
- `coordination_status`: `active`, `paused`, `blocked`, `handoff_ready`, or
  `completed`; default to `active` while work is ongoing
- `artifact_scope`: short human-readable artifact or sub-scope being worked on
- `artifact_refs`: relevant repo, Figma, Drive, Notion, data, or output refs
- `work_branch`: git branch when applicable to code work
- `worktree_path`: local checkout/worktree path; required for `work_type:
  "code"` so other agents can see which checkout/worktree is in use

Full coordination policy:

```text
brain/shared/policies/agent-coordination-policy.md
```

Do not confuse role labels with agent family:

- Correct: `actor_role: "A1"`, `agent_family: "claude-code"`
- Correct: `actor_role: "A1"`, `agent_family: "gemini-antigravity"`
- Correct: `actor_role: "A2-Core-C"`, `agent_family: "codex"`
- Wrong: `agent_family: "A1"`
- Wrong: `agent_family: "a1-work"`

Do not send `actor_family` or `logical_role` unless explicitly asked. Those are
legacy optional compatibility fields; AICOS derives them from `agent_family` and
`actor_role` when absent.

Before starting code work, read `active_task_state` from
`aicos_get_startup_bundle`. Do not reuse another active agent's `worktree_path`
or `work_lane` unless the human explicitly asks for a handoff, review, or
pair-work on the same checkout.

For code work, treat `worktree_path` as an active checkout occupancy signal, not
permanent ownership. Reuse an existing worktree only for explicit continuation,
handoff, review, takeover, or pair-work. Create/use a separate worktree for
parallel implementation, a different `work_lane`, a different branch, unclear
dirty state, or likely overlapping file edits.

If MCP is unavailable, say so explicitly and ask whether to proceed with an
exceptional fallback. Do not silently normalize raw cross-folder continuity
writes.

If a write fails with `details.mcp_contract_status`, follow its
`refresh_instruction`, then retry with the current required fields.
```

## New Project Or Existing Project Import

If the project is not already known to AICOS, do not invent raw AICOS folders.
Report which branch applies:

- `new_project`: no existing repo/context or only a fresh skeleton exists.
- `existing_project_import`: an existing repo/docs/context system should be
  imported into AICOS.

For a new project, collect a short human text summary:

- project name;
- project slug;
- 2-5 sentence project summary;
- current stage;
- expected work type;
- first desired task;
- known constraints;
- source location if one already exists.

For an existing project import, collect:

- project name;
- project slug;
- source path or Git URL;
- branch/ref;
- short project summary;
- existing context/docs locations;
- known current task or active workstream;
- known risks or ambiguity;
- requested import depth.

Then ask AICOS/A2-Core to create the appropriate project shell or import kit.
Do not create broad project context by raw file writes unless explicitly
authorized.

## Troubleshooting

If no tools appear:

- verify `python3` works;
- verify `<AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py`
  exists;
- restart or re-enable the MCP server in the client;
- run the Local Stdio Smoke Test from `<AICOS_REPO_PATH>`;
- check whether the client requires an allow-list entry for `aicos`.

If tool calls fail with project not found:

- check the requested scope, for example `projects/sample-project`;
- ask AICOS/A2-Core whether the project is known, new, or requires import.
