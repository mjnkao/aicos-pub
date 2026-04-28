#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages/aicos-kernel"))

from aicos_kernel.mcp_read_serving import AicosMcpReadError, dispatch_read_surface  # noqa: E402
from aicos_kernel.mcp_tool_definitions import build_tools  # noqa: E402
from aicos_kernel.mcp_tool_schema import READ_TOOL_NAMES, apply_aicos_tool_schema_extensions  # noqa: E402
from aicos_kernel.mcp_write_serving import AicosMcpWriteError, dispatch_write_tool  # noqa: E402


TOOLS = build_tools()
apply_aicos_tool_schema_extensions(TOOLS)


def response(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def error_response(message_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}
    if data is not None:
        payload["error"]["data"] = data
    return payload


def tool_result(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}],
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
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                {"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
                                indent=2,
                                ensure_ascii=False,
                            ),
                        }
                    ],
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

