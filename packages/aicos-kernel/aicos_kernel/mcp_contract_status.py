from __future__ import annotations

from copy import deepcopy
from typing import Any


MCP_CONTRACT_STATUS: dict[str, Any] = {
    "schema_version": "0.6",
    "minimum_write_contract": "mcp-v0.6-write-contract-ack",
    "coordination_policy_version": "2026-04-21.agent-coordination-v1",
    "write_schema_refresh_required": True,
    "write_schema_refresh_recommended": False,
    "write_contract_ack_required": True,
    "write_contract_ack_field": "mcp_contract_ack",
    "write_contract_ack_value": "mcp-v0.6-write-contract-ack",
    "required_write_fields": [
        "mcp_contract_ack",
        "actor_role",
        "agent_family",
        "agent_instance_id",
        "work_type",
        "work_lane",
        "runtime_context",
    ],
    "conditional_required_fields": {
        "worktree_path": "required when work_type is code",
        "runtime_identity_map": "required when actor_role begins with A2-",
    },
    "semantic_write_tools": [
        "aicos_record_checkpoint",
        "aicos_write_task_update",
        "aicos_write_handoff_update",
        "aicos_update_status_item",
        "aicos_register_artifact_ref",
        "aicos_record_feedback",
    ],
    "semantic_read_tools": [
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
    ],
    "policy_ref": "brain/shared/policies/agent-coordination-policy.md",
    "contract_ref": "packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md",
    "refresh_instruction": (
        "If your client cached MCP tool schemas, call tools/list again or "
        "restart/re-enable the AICOS MCP server before writing."
    ),
}


def contract_status_payload() -> dict[str, Any]:
    return deepcopy(MCP_CONTRACT_STATUS)


def contract_error_details(details: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = dict(details or {})
    merged["mcp_contract_status"] = contract_status_payload()
    return merged
