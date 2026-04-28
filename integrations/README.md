# AICOS Integrations

Status: active runtime binding lane

`integrations/` holds runtime bindings and manual sync lanes. These are not
project truth.

The most important active integration is the local MCP bridge:

- contract: `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- operations: `packages/aicos-kernel/aicos_kernel/mcp_read_serving.py` and
  `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
- stdio adapter: `integrations/local-mcp-bridge/aicos_mcp_stdio.py`

Local MCP is AICOS context/control-plane access. It serves bounded context and
records semantic continuity writes; it is not a generic raw-file edit API.

Remote/hosted MCP, auth/session, daemonization, and broad workflow automation
are deferred.
