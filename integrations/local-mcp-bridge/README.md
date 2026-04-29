# Local MCP Bridge

Status: Phase 3 lightweight query/read/write scaffold

This lane contains the local-first stdio integration surface between AICOS and
external project repos.

## Authority Split

- AICOS: context/control-plane authority.
- External project repo: code/runtime authority.
- Worker session: immediate execution state only.

## Current Scope

Phase 1 implements the read-serving surface:

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

Phase 2 implements the semantic write surface:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update` for compact current-continuity handoff updates
  only
- `aicos_update_status_item`
- `aicos_register_artifact_ref`
- `aicos_record_feedback`
- `aicos_propose_project`

Contract:

```text
packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md
```

Do not use `aicos_write_handoff_update` as a substitute for
`aicos_update_status_item`. If a client only sees the older write tools, refresh
`tools/list` or restart/re-enable the AICOS MCP server before writing status,
open item, open question, tech debt, decision follow-up, or backlog updates.

Operations layer:

```text
packages/aicos-kernel/aicos_kernel/mcp_read_serving.py
packages/aicos-kernel/aicos_kernel/mcp_write_serving.py
```

Local stdio adapter:

```text
integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

HTTP-first stdio proxy for Codex and other stdio-only MCP clients:

```text
integrations/local-mcp-bridge/aicos_mcp_http_first.py
```

The proxy calls the HTTP daemon first and falls back to the local stdio adapter
if HTTP is unavailable.

Agent install packet:

```text
integrations/local-mcp-bridge/install/AICOS_MCP_AGENT_INSTALL.md
```

Give that file to a new local agent when it needs to install the AICOS MCP
server and then read AICOS context.

Default local mode remains stdio. For team/LAN use, run the optional HTTP
daemon in `integrations/mcp-daemon/`; do not expose it beyond a trusted network
without a token.

## CLI Convenience

From the repo root, install a portable `aicos` symlink into a user-writable bin
directory:

```bash
./aicos install cli --bin-dir ~/.local/bin
```

The symlink points to this checkout's `./aicos` wrapper, which discovers the
repo root from its own location. Ensure the chosen bin directory is on `PATH`.

## sample project First Test

The first intended cross-repo test target is:

```text
projects/sample-project
```

The bridge should eventually let a worker started inside the sample project repo request
AICOS startup context, task packets, and writeback operations without manually
browsing the AICOS repo broadly.

## Local Smoke Test

CLI debug surface:

```bash
./aicos mcp read startup-bundle --actor A1 --scope projects/sample-project
./aicos mcp read packet-index --actor A1 --scope projects/sample-project
./aicos mcp read task-packet --actor A1 --scope projects/sample-project --packet-id review-sample-workstream-import-slice
./aicos mcp read status-items --actor A1 --scope projects/sample-project
./aicos mcp read workstream-index --actor A1 --scope projects/sample-project
./aicos mcp read context-registry --actor A1 --scope projects/sample-project --max-results 20
./aicos mcp read project-registry --actor A1 --scope projects/sample-project
./aicos mcp read feedback-digest --actor A1 --scope projects/sample-project
./aicos mcp read project-health --actor A1 --scope projects/sample-project
./aicos mcp read query-project-context --actor A1 --scope projects/sample-project --query "openai pipeline handoff" --max-results 5
./aicos mcp doctor
```

Semantic write debug surface:

```bash
./aicos mcp template checkpoint --scope projects/sample-project --actor-role A1 --runtime private-local-aicos --mcp-name aicos_local_private --agent-position external_agent
./aicos mcp template status-item --scope projects/aicos --actor-role A2-Core-C --runtime private-local-aicos --mcp-name aicos_local_private --agent-position internal_agent --functional-role "AICOS maintainer"
```

Stdio JSON-RPC style smoke test:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"aicos_get_packet_index","arguments":{"actor":"A1","scope":"projects/sample-project"}}}' \
  | python3 integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

## Deferred

- production remote/online transport
- full auth/session system
- cache/observability beyond bundle trace metadata
- generic raw file write tools
- broader workflow write tools beyond the current bounded semantic surface
- dedicated MCP lifecycle tools for policy candidates and workstream proposals
