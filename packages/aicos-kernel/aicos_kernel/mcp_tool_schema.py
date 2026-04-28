from __future__ import annotations

from typing import Any

from .mcp_contract_status import contract_status_payload


WORK_TYPE_ENUM = ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]

READ_TOOL_NAMES: set[str] = {
    "aicos_get_startup_bundle",
    "aicos_get_handoff_current",
    "aicos_get_packet_index",
    "aicos_get_task_packet",
    "aicos_get_status_items",
    "aicos_get_workstream_index",
    "aicos_get_context_registry",
    "aicos_get_project_registry",
    "aicos_get_feedback_digest",
    "aicos_get_project_health",
    "aicos_query_project_context",
}

WRITE_TOOL_NAMES: set[str] = {
    "aicos_record_checkpoint",
    "aicos_write_task_update",
    "aicos_write_handoff_update",
    "aicos_update_status_item",
    "aicos_register_artifact_ref",
    "aicos_record_feedback",
}

READ_IDENTITY_REQUIRED = ["agent_family", "agent_instance_id", "work_type", "work_lane", "execution_context"]

RUNTIME_CONTEXT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "Required lightweight runtime identity for this MCP call. A1 agents normally only need this object.",
    "properties": {
        "runtime": {
            "type": "string",
            "description": "AICOS runtime receiving this MCP call, e.g. private-local-aicos or public-railway-aicos.",
        },
        "mcp_name": {
            "type": "string",
            "description": "Client-side MCP server alias, e.g. aicos_local_private or aicos_railway_public.",
        },
        "agent_position": {
            "type": "string",
            "enum": ["external_agent", "internal_agent", "human_operator", "system"],
            "description": "Position relative to the runtime receiving this call.",
        },
        "functional_role": {
            "type": "string",
            "description": "Task/business role for this write, e.g. reviewer, CTO/fullstack dev, runtime maintainer.",
        },
    },
    "required": ["runtime", "mcp_name", "agent_position"],
    "additionalProperties": False,
}

RUNTIME_IDENTITY_ENTRY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "One runtime-relative identity entry for A2/cross-runtime work.",
    "properties": {
        "runtime": {"type": "string"},
        "mcp_name": {"type": "string"},
        "project_scope": {"type": "string"},
        "agent_position": {"type": "string", "enum": ["external_agent", "internal_agent", "human_operator", "system"]},
        "actor_role": {"type": "string"},
        "functional_role": {"type": "string"},
    },
    "required": ["runtime", "mcp_name", "project_scope", "agent_position", "actor_role", "functional_role"],
    "additionalProperties": False,
}

RUNTIME_IDENTITY_MAP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "Required for A2 writes. Map each relevant runtime label to its runtime-relative identity, e.g. identity_private and identity_public.",
    "additionalProperties": RUNTIME_IDENTITY_ENTRY_SCHEMA,
}

READ_IDENTITY_PROPERTIES: dict[str, dict[str, Any]] = {
    "actor": {
        "type": "string",
        "description": "Optional AICOS service actor. External clients may omit this or send their client name; AICOS normalizes non-explicit A2 values to A1. Use A2-Core-C/R only when maintaining AICOS itself.",
    },
    "agent_family": {
        "type": "string",
        "description": "Required client/agent family for audit correlation, e.g. codex, claude-code, openclaw.",
    },
    "agent_instance_id": {
        "type": "string",
        "description": "Required per-agent/per-thread/per-worker instance id for audit correlation.",
    },
    "work_type": {
        "type": "string",
        "enum": WORK_TYPE_ENUM,
        "description": "Required current work type for read-side audit context. Use orientation for first-contact/bootstrap reads.",
    },
    "work_lane": {
        "type": "string",
        "description": "Required current work lane for read-side audit context. Use intake for first-contact/bootstrap reads when the real lane is not known yet.",
    },
    "worktree_path": {
        "type": "string",
        "description": "Required when the reader is a code worker. Absolute path of the worktree/checkout.",
    },
    "work_branch": {
        "type": "string",
        "description": "Recommended branch name when the reader is a code worker.",
    },
    "execution_context": {
        "type": "string",
        "description": "Required execution context such as codex-desktop, claude-desktop, openclaw-vm, cli.",
    },
}


def write_contract_ack_value() -> str:
    return str(contract_status_payload()["write_contract_ack_value"])


def apply_aicos_tool_schema_extensions(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply shared AICOS read identity and write-contract schema extensions.

    This keeps HTTP daemon and stdio bridge behavior aligned while the base tool
    definitions are still declared close to each transport.
    """
    ack = write_contract_ack_value()
    for tool in tools:
        schema = tool.get("inputSchema") or {}
        properties = schema.setdefault("properties", {})
        required = schema.setdefault("required", [])
        name = str(tool.get("name") or "")

        if name in READ_TOOL_NAMES:
            properties.update(READ_IDENTITY_PROPERTIES)
            if "actor" in required:
                required.remove("actor")
            for field in READ_IDENTITY_REQUIRED:
                if field not in required:
                    required.append(field)

        if name in WRITE_TOOL_NAMES:
            properties["runtime_context"] = RUNTIME_CONTEXT_SCHEMA
            properties["runtime_identity_map"] = RUNTIME_IDENTITY_MAP_SCHEMA
            properties["mcp_contract_ack"] = {
                "type": "string",
                "const": ack,
                "description": "Required write-contract acknowledgment. If missing, refresh tools/list or restart/re-enable the AICOS MCP server before writing.",
            }
            if "mcp_contract_ack" not in required:
                schema["required"] = ["mcp_contract_ack", *required]
            if "runtime_context" not in schema["required"]:
                schema["required"].append("runtime_context")
    return tools
