#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages/aicos-kernel"))

from aicos_kernel.mcp_read_serving import AicosMcpReadError, dispatch_read_surface  # noqa: E402
from aicos_kernel.mcp_write_serving import AicosMcpWriteError, dispatch_write_tool  # noqa: E402
from aicos_kernel.mcp_contract_status import contract_status_payload  # noqa: E402


CONTRACT_STATUS = contract_status_payload()
WRITE_CONTRACT_ACK_VALUE = str(CONTRACT_STATUS["write_contract_ack_value"])


TOOLS: list[dict[str, Any]] = [
    {
        "name": "aicos_get_startup_bundle",
        "description": "Return a compact AICOS startup bundle for one actor and project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string", "description": "Actor family/role, for example A1 or A2-Core-C."},
                "scope": {"type": "string", "description": "Project scope, for example projects/sample-project."},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_handoff_current",
        "description": "Return the H1 current handoff bundle for one project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_packet_index",
        "description": "Return compact task packet index for one actor and project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_task_packet",
        "description": "Return one selected task packet bundle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
                "packet_id": {"type": "string"},
            },
            "required": ["actor", "scope", "packet_id"],
        },
    },
    {
        "name": "aicos_get_status_items",
        "description": "Return structured project status items with optional filters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
                "status_filter": {"type": "array", "items": {"type": "string"}},
                "item_type_filter": {"type": "array", "items": {"type": "string"}},
                "status_work_lane_filter": {"type": "string", "description": "Optional filter for status item work_lane. Do not use read identity work_lane as a filter."},
                "status_agent_family_filter": {"type": "string", "description": "Optional filter for status item agent_family. Do not use read identity agent_family as a filter."},
                "max_results": {"type": "integer"},
                "include_stale": {"type": "boolean", "description": "Include stale/closed items. Defaults to false."},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_workstream_index",
        "description": "Return project-declared workstream routing/context map when present.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
                "include_candidate": {"type": "boolean"},
                "status_filter": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_context_registry",
        "description": "Return metadata registry entries for project/shared context sources.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
                "max_results": {"type": "integer"},
                "project_role": {"type": "string"},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_project_registry",
        "description": "Return the shared AICOS project registry and parsed project entries.",
        "inputSchema": {
            "type": "object",
            "properties": {"actor": {"type": "string"}, "scope": {"type": "string"}},
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_feedback_digest",
        "description": "Return recent structured feedback signals for a project.",
        "inputSchema": {
            "type": "object",
            "properties": {"actor": {"type": "string"}, "scope": {"type": "string"}, "max_results": {"type": "integer"}},
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_project_health",
        "description": "Return a compact operational/control-plane health view for a project.",
        "inputSchema": {
            "type": "object",
            "properties": {"actor": {"type": "string"}, "scope": {"type": "string"}},
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_query_project_context",
        "description": "Bounded keyword/metadata query over AICOS project hot context plus selected canonical, policy, and contract surfaces.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"},
                "scope": {"type": "string"},
                "query": {"type": "string"},
                "project_role": {"type": "string"},
                "context_kinds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional filters: current_state, current_direction, handoff, packets, status_items, task_state, workstreams, artifacts, open_items, open_questions, canonical, policy, contract, project_registry.",
                },
                "max_results": {"type": "integer"},
                "include_stale": {"type": "boolean", "description": "Include stale/closed status item sources. Defaults to false."},
            },
            "required": ["actor", "scope", "query"],
        },
    },
    {
        "name": "aicos_record_checkpoint",
        "description": "Record a small semantic checkpoint into the project evidence checkpoint lane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "actor_role": {"type": "string", "description": "Role lane doing the work, for example A1, A2-Core-C, or A2-Core-R."},
                "agent_family": {"type": "string", "description": "Agent/client family, for example codex, claude-code, gemini-antigravity, or openclaw."},
                "agent_instance_id": {"type": "string", "description": "Unique session/instance id for this agent run."},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string", "description": "Generic coordination lane. For code this may match a branch; for non-code use a doc/design/research lane."},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string", "description": "Human-readable artifact or sub-scope being worked on."},
                "work_branch": {"type": "string", "description": "Git branch or work lane when applicable."},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "checkpoint_type": {"type": "string", "enum": ["review", "validation", "artifact", "blocked", "continuation"]},
                "summary": {"type": "string"},
                "status": {"type": "string", "enum": ["completed", "blocked", "partial"]},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
                "notes": {"type": "string"},
            },
            "required": ["scope", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "checkpoint_type", "summary", "status"],
        },
    },
    {
        "name": "aicos_write_task_update",
        "description": "Write bounded project task continuity state without exposing raw file writes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "task_ref": {"type": "string"},
                "actor_role": {"type": "string", "description": "Role lane doing the work, for example A1, A2-Core-C, or A2-Core-R."},
                "agent_family": {"type": "string", "description": "Agent/client family, for example codex, claude-code, gemini-antigravity, or openclaw."},
                "agent_instance_id": {"type": "string", "description": "Unique session/instance id for this agent run."},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string", "description": "Generic coordination lane. For code this may match a branch; for non-code use a doc/design/research lane."},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string", "description": "Human-readable artifact or sub-scope being worked on."},
                "work_branch": {"type": "string", "description": "Git branch or work lane when applicable."},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "task_status": {"type": "string", "enum": ["planned", "in_progress", "completed", "blocked", "waiting"]},
                "what_is_done": {"type": "string"},
                "what_is_blocked": {"type": "string"},
                "next_step": {"type": "string"},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope", "task_ref", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "task_status", "what_is_done"],
        },
    },
    {
        "name": "aicos_write_handoff_update",
        "description": "Add or replace one compact current-continuity section in project handoff/current. Do not use this to create or update open items, open questions, tech debt, or decision follow-ups; refresh/restart MCP and use aicos_update_status_item instead.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "actor_role": {"type": "string", "description": "Role lane doing the work, for example A1, A2-Core-C, or A2-Core-R."},
                "agent_family": {"type": "string", "description": "Agent/client family, for example codex, claude-code, gemini-antigravity, or openclaw."},
                "agent_instance_id": {"type": "string", "description": "Unique session/instance id for this agent run."},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string", "description": "Generic coordination lane. For code this may match a branch; for non-code use a doc/design/research lane."},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string", "description": "Human-readable artifact or sub-scope being worked on."},
                "work_branch": {"type": "string", "description": "Git branch or work lane when applicable."},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "summary": {"type": "string", "description": "Compact current handoff/continuity summary. Not a backlog, open-item list, open-question list, or tech-debt update."},
                "status": {"type": "string", "enum": ["completed", "blocked", "partial", "ready_for_next"]},
                "next_step": {"type": "string", "description": "Immediate continuation step for the handoff reader. Status item lifecycle changes belong in aicos_update_status_item."},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
                "notes": {"type": "string", "description": "Short handoff note only. Do not store detailed open-item/status-item bodies here."},
            },
            "required": ["scope", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "summary", "status", "next_step"],
        },
    },
    {
        "name": "aicos_update_status_item",
        "description": "Upsert a structured project status item for open items, open questions, tech debt, or decision follow-ups. Returns soft warnings when item_type appears suspicious.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "actor_role": {"type": "string", "description": "Role lane doing the work, for example A1, A2-Core-C, or A2-Core-R."},
                "agent_family": {"type": "string", "description": "Agent/client family, for example codex, claude-code, gemini-antigravity, or openclaw."},
                "agent_instance_id": {"type": "string", "description": "Unique session/instance id for this agent run."},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string", "description": "Generic coordination lane."},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string"},
                "work_branch": {"type": "string"},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "item_id": {"type": "string", "description": "Stable project-local id/key for the status item."},
                "item_type": {
                    "type": "string",
                    "enum": ["open_item", "open_question", "tech_debt", "decision_followup"],
                    "description": "open_item=new actionable work; open_question=unresolved decision/question; tech_debt=known existing issue, missing validation/coverage/docs, cleanup, quality gap; decision_followup=made decision needing tracking.",
                },
                "item_status": {"type": "string", "enum": ["open", "resolved", "closed", "stale", "deferred", "blocked"]},
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "reason": {"type": "string"},
                "next_step": {"type": "string"},
                "source_ref": {"type": "string"},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "item_id", "item_type", "item_status", "title", "summary"],
        },
    },
    {
        "name": "aicos_register_artifact_ref",
        "description": "Register a compact artifact reference without copying artifact body into AICOS.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "actor_role": {"type": "string", "description": "Role lane doing the work, for example A1, A2-Core-C, or A2-Core-R."},
                "agent_family": {"type": "string", "description": "Agent/client family, for example codex, claude-code, gemini-antigravity, or openclaw."},
                "agent_instance_id": {"type": "string", "description": "Unique session/instance id for this agent run."},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string"},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string"},
                "work_branch": {"type": "string"},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "artifact_kind": {"type": "string", "enum": ["note", "report", "diff", "output", "analysis", "contract_check", "dataset", "design", "content", "other"]},
                "title": {"type": "string"},
                "artifact_ref": {"type": "string"},
                "summary": {"type": "string"},
                "source_ref": {"type": "string"},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "artifact_kind", "title", "artifact_ref", "summary"],
        },
    },
    {
        "name": "aicos_record_feedback",
        "description": "Record a structured AICOS/project context-serving feedback signal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"},
                "actor_role": {"type": "string"},
                "agent_family": {"type": "string"},
                "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"]},
                "work_lane": {"type": "string"},
                "coordination_status": {"type": "string", "enum": ["active", "paused", "blocked", "handoff_ready", "completed"]},
                "artifact_scope": {"type": "string"},
                "work_branch": {"type": "string"},
                "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"},
                "actor_family": {"type": "string"},
                "logical_role": {"type": "string"},
                "work_context": {"type": "string"},
                "feedback_type": {"type": "string", "enum": ["no_issue", "query_failed", "stale_result", "context_missing", "context_overload", "rule_confusing", "tool_missing", "tool_shape_confusing", "tool_too_heavy", "bootstrap_confusing", "write_schema_confusing", "interop_problem", "packet_missing_ref", "handoff_too_long", "role_context_wrong", "routing_confusing", "other"]},
                "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "observed_in": {"type": "string"},
                "recommendation": {"type": "string"},
                "source_ref": {"type": "string"},
                "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope", "actor_role", "agent_family", "agent_instance_id", "work_type", "work_lane", "feedback_type", "severity", "title", "summary"],
        },
    },
]


WRITE_TOOL_NAMES = {
    "aicos_record_checkpoint",
    "aicos_write_task_update",
    "aicos_write_handoff_update",
    "aicos_update_status_item",
    "aicos_register_artifact_ref",
    "aicos_record_feedback",
}


for tool in TOOLS:
    if tool["name"] not in WRITE_TOOL_NAMES:
        continue
    schema = tool["inputSchema"]
    schema["properties"]["mcp_contract_ack"] = {
        "type": "string",
        "const": WRITE_CONTRACT_ACK_VALUE,
        "description": (
            "Required write-contract acknowledgment. If missing, refresh "
            "tools/list or restart/re-enable the AICOS MCP server before writing."
        ),
    }
    if "mcp_contract_ack" not in schema["required"]:
        schema["required"] = ["mcp_contract_ack", *schema["required"]]


READ_TOOL_NAMES = {
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

READ_IDENTITY_REQUIRED = ["agent_family", "agent_instance_id", "work_type", "work_lane", "execution_context"]
READ_IDENTITY_PROPERTIES: dict[str, dict[str, Any]] = {
    "actor": {"type": "string", "description": "Optional AICOS service actor. External clients may omit this or send their client name; AICOS normalizes non-explicit A2 values to A1. Use A2-Core-C/R only when maintaining AICOS itself."},
    "agent_family": {"type": "string", "description": "Required client/agent family for audit correlation, e.g. codex, claude-code, openclaw."},
    "agent_instance_id": {"type": "string", "description": "Required per-agent/per-thread/per-worker instance id for audit correlation."},
    "work_type": {"type": "string", "enum": ["code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"], "description": "Use orientation for first-contact/bootstrap reads."},
    "work_lane": {"type": "string", "description": "Use intake for first-contact/bootstrap reads when the real lane is not known yet."},
    "worktree_path": {"type": "string", "description": "Required when the reader is a code worker."},
    "work_branch": {"type": "string", "description": "Recommended branch name when the reader is a code worker."},
    "execution_context": {"type": "string", "description": "Execution context such as codex-desktop, claude-desktop, openclaw-vm, cli."},
}

for tool in TOOLS:
    if tool["name"] not in READ_TOOL_NAMES:
        continue
    schema = tool["inputSchema"]
    schema["properties"].update(READ_IDENTITY_PROPERTIES)
    if "actor" in schema.get("required", []):
        schema["required"].remove("actor")
    for field in READ_IDENTITY_REQUIRED:
        if field not in schema["required"]:
            schema["required"].append(field)


def response(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def error_response(message_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}
    if data is not None:
        payload["error"]["data"] = data
    return payload


def tool_result(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, indent=2, ensure_ascii=False),
            }
        ],
        "isError": False,
    }


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        return response(
            message_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False},
                },
                "serverInfo": {"name": "aicos-local-mcp-phase2", "version": "0.5.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return response(message_id, {})
    if method == "tools/list":
        return response(message_id, {"tools": TOOLS})
    if method == "resources/list":
        return response(message_id, {"resources": []})
    if method == "resources/templates/list":
        return response(message_id, {"resourceTemplates": []})
    if method == "prompts/list":
        return response(message_id, {"prompts": []})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(name, str):
            return error_response(message_id, -32602, "Missing tool name")
        if not isinstance(arguments, dict):
            return error_response(message_id, -32602, "Tool arguments must be an object")
        try:
            if name in READ_TOOL_NAMES:
                payload = dispatch_read_surface(name, arguments)
            else:
                payload = dispatch_write_tool(name, arguments)
        except (AicosMcpReadError, AicosMcpWriteError) as exc:
            return response(
                message_id,
                {
                    "content": [{"type": "text", "text": json.dumps({"error": {"code": exc.code, "message": exc.message, "details": exc.details}}, indent=2, ensure_ascii=False)}],
                    "isError": True,
                },
            )
        return response(message_id, tool_result(payload))
    return error_response(message_id, -32601, f"Unsupported Phase 1 method: {method}")


def main() -> int:
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped:
            continue
        try:
            message = json.loads(stripped)
        except json.JSONDecodeError as exc:
            print(json.dumps(error_response(None, -32700, f"Parse error: {exc}")), flush=True)
            continue
        result = handle(message)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
