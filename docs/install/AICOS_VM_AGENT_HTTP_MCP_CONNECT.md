# AICOS VM Agent HTTP MCP Connect Guide

Status: operator-facing quick connect guide  
Last updated: 2026-04-23

Use this file when a human wants an agent running inside a VM to connect to the
host machine's AICOS HTTP MCP daemon without reading the whole install runbook.

This guide assumes:

- the host machine already has AICOS cloned and configured
- the host daemon is running in LAN/VM mode
- the human can provide the shared bearer token

Client split for this guide:

- `Codex Desktop`
  - use direct HTTP / Streamable HTTP with bearer header
- `Claude Code`
  - use direct HTTP with bearer header when available
- `Antigravity / Gemini IDE`
  - use raw config with `serverUrl` + `headers`
- `Claude Desktop`
  - do not use this VM/LAN HTTP guide unless a dedicated remote-safe HTTPS
    adapter path has been set up for that machine

## 1. Values The Agent Needs From The Human

The human must provide or confirm:

1. `AICOS_MCP_URL`
2. `AICOS_DAEMON_TOKEN`

For the current macOS + VM bridge setup used in this repo, the default VM host
URL is:

```text
http://192.168.64.1:8000/mcp
```

Do not put the token in the URL.  
Do not use `?token=...`.  
Use a normal HTTP header:

```text
Authorization: Bearer <AICOS_DAEMON_TOKEN>
```

## 2. Quick Health Test From The VM

Before configuring MCP, test raw connectivity:

```bash
curl -H "Authorization: Bearer <AICOS_DAEMON_TOKEN>" \
  http://192.168.64.1:8000/health
```

Expected result: JSON with `"status": "ok"`.

The health payload may also include `auth_capabilities`, which tells the agent:

- OAuth is not supported by the daemon
- query-string token auth is not supported
- bearer-header HTTP is the expected VM/LAN path

If this fails:

- ask the human to restart the host daemon
- confirm the host is listening on LAN/VM bridge, not only `127.0.0.1`
- confirm the token matches the host's `.runtime-home/aicos-daemon.env`

## 3. Generic HTTP MCP Config

For any MCP client that supports a URL plus custom headers:

```text
URL: http://192.168.64.1:8000/mcp
Header:
  Key: Authorization
  Value: Bearer <AICOS_DAEMON_TOKEN>
```

If the client supports a bearer token env var instead of a direct header:

```bash
export AICOS_DAEMON_TOKEN=<AICOS_DAEMON_TOKEN>
```

Then set the MCP client bearer-token field to:

```text
AICOS_DAEMON_TOKEN
```

## 3b. Antigravity / Gemini IDE HTTP-SSE Config

Antigravity's raw MCP config is stricter than some other clients.

Use:

- `serverUrl`, not `url`
- `headers`, not a separate transport field

Example:

```json
{
  "mcpServers": {
    "aicos": {
      "serverUrl": "http://192.168.64.1:8000/mcp",
      "headers": {
        "Authorization": "Bearer <AICOS_DAEMON_TOKEN>"
      }
    }
  }
}
```

Do not use:

- `url`
- `transport`
- `?token=...`

If Antigravity connects but shows no tools, first verify the health endpoint,
then re-check that the config uses `serverUrl` and `headers` exactly.

## 4. Codex Desktop Form Values

When Codex Desktop asks for Streamable HTTP MCP fields:

```text
Name: aicos_http
Transport: Streamable HTTP
URL: http://192.168.64.1:8000/mcp
Bearer token env var: leave blank if entering a direct header
Headers:
  Key: Authorization
  Value: Bearer <AICOS_DAEMON_TOKEN>
```

Important:

- the value must include the `Bearer ` prefix
- if Save does not work, remove empty header-variable rows and retry
- after saving, restart or refresh Codex tools

## 5. Claude Code CLI Example

If the VM agent is Claude Code and supports direct HTTP MCP:

```bash
claude mcp add --transport http aicos http://192.168.64.1:8000/mcp -s user
```

If Claude Code needs the token in environment:

```bash
export AICOS_DAEMON_TOKEN=<AICOS_DAEMON_TOKEN>
```

Then configure the client to send:

```text
Authorization: Bearer $AICOS_DAEMON_TOKEN
```

If the client cannot attach auth headers reliably, do not weaken AICOS auth.
Use a local adapter/sidecar approach instead of URL tokens.

## 5b. Claude Desktop

Claude Desktop is not the normal VM/LAN client for this guide.

Preferred path:

- same machine as AICOS host: use the host-local Claude Desktop route
- if a remote Claude Desktop path is needed later, treat that as a separate
  HTTPS/interoperability setup, not as generic LAN bearer-header MCP

Do not tell Claude Desktop to use:

- raw VM HTTP bearer config from this file
- query-string token auth
- fake OAuth values

## 6. OpenClaw / Generic VM Agent Prompt

Send this exact instruction to a VM agent when you want it to self-configure:

```text
Connect this VM to the host AICOS HTTP MCP.

Use:
- MCP URL: http://192.168.64.1:8000/mcp
- Header: Authorization: Bearer <AICOS_DAEMON_TOKEN>

Steps:
1. Test the health endpoint first.
2. Configure the MCP client with the URL and Authorization bearer header.
3. Verify MCP tools load.
4. Read:
   - aicos_get_startup_bundle(actor=A2-Core-C, scope=projects/aicos)
5. Report success or the exact connection/auth error.

Do not put the token in the URL.
Do not use query-string auth.
```

For Antigravity, prefer telling it explicitly:

```text
Use raw MCP config with:
- serverUrl: http://192.168.64.1:8000/mcp
- headers.Authorization: Bearer <AICOS_DAEMON_TOKEN>

Do not use url, transport, or query-string token auth.
```

## 7. First Reads After MCP Connects

Read calls now require minimum identity fields for audit/correlation.

Minimum required on every read:

```text
agent_family
agent_instance_id
work_type
work_lane
execution_context
```

Additional required when `work_type=code`:

```text
worktree_path
```

Recommended when `work_type=code`:

```text
work_branch
```

Meaning of the fields:

```text
agent_family      = tool/family name, e.g. openclaw, codex, claude-code
agent_instance_id = this worker/thread/session id, e.g. vm-alpha-01
work_type         = code | content | design | research | ops | review | planning | data | mixed | orientation
work_lane         = current task lane, e.g. telegram-pipeline; use intake for first-contact/bootstrap reads
execution_context = where it runs, e.g. openclaw-vm, codex-desktop, claude-desktop, cli
worktree_path     = absolute checkout path when work_type=code
work_branch       = branch name when work_type=code
```

If the agent is connecting for the first time and does not yet know the real
lane, use this bootstrap pair:

```text
work_type=orientation
work_lane=intake
```

For AICOS maintenance work:

```text
aicos_get_startup_bundle(
  actor=A2-Core-C,
  scope=projects/aicos,
  agent_family=openclaw,
  agent_instance_id=vm-alpha-01,
  work_type=ops,
  work_lane=aicos-maintenance,
  execution_context=openclaw-vm
)
```

For first-contact orientation into any project:

```text
aicos_get_startup_bundle(
  actor=A1,
  scope=projects/<project-id>,
  agent_family=openclaw,
  agent_instance_id=vm-alpha-01,
  work_type=orientation,
  work_lane=intake,
  execution_context=openclaw-vm
)
```

For project work:

```text
aicos_get_startup_bundle(
  actor=A1,
  scope=projects/<project-id>,
  agent_family=openclaw,
  agent_instance_id=vm-alpha-01,
  work_type=code,
  work_lane=telegram-pipeline,
  worktree_path=/workspace/<project-worktree>,
  work_branch=feature/<branch>,
  execution_context=openclaw-vm
)
```

If the daemon rejects a read with `missing_read_identity`, fill the fields from
the error details and retry. The error now returns:

- `missing`: which fields are absent
- `field_help`: short explanation for each missing field
- `example`: a minimal example payload

## 8. Host-Side Reminder

If the VM cannot connect but the token is correct, the host likely needs a real
restart of the daemon in LAN mode.

On the host:

```bash
cd <AICOS_PRIVATE_REPO>
integrations/mcp-daemon/start-lan.sh
```

Or reload LaunchAgents:

```bash
cd <AICOS_PRIVATE_REPO>
scripts/aicos-install-launchagents
```

## 9. Security Boundary

Current LAN/VM HTTP MCP is acceptable for trusted same-host VM or small trusted
LAN use, but it is still MVP-level.

- shared bearer token
- no per-agent session model yet
- no query-string token auth
- prefer HTTPS proxy for broader LAN use when available

Related follow-up:

```text
brain/projects/aicos/working/status-items/aicos-lan-security-hardening.md
```
