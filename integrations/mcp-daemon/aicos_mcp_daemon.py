#!/usr/bin/env python3
"""AICOS MCP HTTP Daemon — with PostgreSQL search engine.

Serves the full AICOS MCP surface over HTTP (Streamable HTTP / JSON-RPC).
On startup:
  1. Connects to PostgreSQL (AICOS_PG_DSN or defaults).
  2. Applies schema (idempotent).
  3. Runs full brain/ reindex.
  4. Starts HTTP server.

aicos_query_project_context uses PostgreSQL FTS when pg is available.
All other tools fall back to the original markdown-direct dispatch.

Usage:
    python aicos_mcp_daemon.py [--host 127.0.0.1] [--port 8000] [--cache-ttl 30]

Setup PostgreSQL (quickest):
    docker compose up -d           # from integrations/mcp-daemon/

Agent config (Claude Code):
    claude mcp add --transport http aicos http://localhost:8000/mcp
    AICOS_DAEMON_TOKEN=secret python aicos_mcp_daemon.py --host 0.0.0.0  # LAN
    claude mcp add --transport http aicos http://192.168.1.100:8000/mcp
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import logging
import os
import queue
import socketserver
import sys
import threading
import time
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages/aicos-kernel"))

from aicos_kernel.mcp_cache import ResponseCache  # noqa: E402
from aicos_kernel.mcp_read_serving import AicosMcpReadError, dispatch_read_surface  # noqa: E402
from aicos_kernel.mcp_tool_definitions import build_tools  # noqa: E402
from aicos_kernel.mcp_tool_schema import READ_IDENTITY_REQUIRED, READ_TOOL_NAMES, WORK_TYPE_ENUM, WRITE_TOOL_NAMES, apply_aicos_tool_schema_extensions  # noqa: E402
from aicos_kernel.mcp_write_serving import AicosMcpWriteError, dispatch_write_tool  # noqa: E402

logger = logging.getLogger("aicos-daemon")

# ---------------------------------------------------------------------------
# PostgreSQL search engine (optional — degrades gracefully when unavailable)
# ---------------------------------------------------------------------------

_pg_search_engine = None   # PgSearchEngine | None
_pg_indexer       = None   # BrainIndexer   | None
_pg_status        = {
    "engine": "markdown_direct",
    "postgresql": "not_initialized",
    "vector": "not_initialized",
    "embeddings": "not_initialized",
    "embedding_index": "not_started",
}
_pg_lock          = threading.Lock()
_reindex_lock     = threading.Lock()
_reindex_state: dict[str, dict[str, Any]] = {}
_sse_lock         = threading.Lock()
_sse_sessions: dict[str, "queue.Queue[dict[str, Any]]"] = {}
_audit_lock       = threading.Lock()


DEFAULT_INTERNAL_TOKEN_LABELS: set[str] = set()
PROTECTED_WRITE_SCOPES = {"projects/aicos"}


def _parse_token_set(primary_token: str) -> dict[str, str]:
    tokens: dict[str, str] = {}
    if primary_token:
        primary_label = os.environ.get("AICOS_DAEMON_PRIMARY_TOKEN_LABEL", "default").strip() or "default"
        tokens[primary_label] = primary_token
    raw = os.environ.get("AICOS_DAEMON_EXTRA_TOKENS", "").strip()
    if not raw:
        return tokens
    for item in raw.split(","):
        entry = item.strip()
        if not entry:
            continue
        if ":" in entry:
            name, token = entry.split(":", 1)
            name = name.strip() or "unnamed"
            token = token.strip()
            if token:
                tokens[name] = token
        else:
            tokens[f"extra_{len(tokens)}"] = entry
    return tokens


def _parse_allowlist() -> list[ipaddress._BaseNetwork]:
    raw = os.environ.get("AICOS_DAEMON_ALLOWLIST", "").strip()
    networks: list[ipaddress._BaseNetwork] = []
    if not raw:
        return networks
    for item in raw.split(","):
        entry = item.strip()
        if not entry:
            continue
        try:
            if "/" in entry:
                networks.append(ipaddress.ip_network(entry, strict=False))
            else:
                addr = ipaddress.ip_address(entry)
                suffix = "/32" if addr.version == 4 else "/128"
                networks.append(ipaddress.ip_network(f"{entry}{suffix}", strict=False))
        except ValueError:
            logger.warning("Ignoring invalid AICOS_DAEMON_ALLOWLIST entry: %s", entry)
    return networks


def _parse_csv_set(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def _parse_token_scope_policy() -> dict[str, dict[str, list[str]]]:
    """Parse optional token scope policy from JSON env.

    Shape:
      {
        "antigravity": {"read": ["projects/sample-*"], "write": ["projects/sample-project"]},
        "codex": {"read": ["projects/*"], "write": ["projects/*"]}
      }

    Missing labels/operations fall back to the daemon's default policy.
    """
    raw = os.environ.get("AICOS_DAEMON_TOKEN_SCOPE_POLICY", "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.warning("Ignoring invalid AICOS_DAEMON_TOKEN_SCOPE_POLICY JSON: %s", exc)
        return {}
    if not isinstance(parsed, dict):
        logger.warning("Ignoring AICOS_DAEMON_TOKEN_SCOPE_POLICY: top-level value must be an object")
        return {}
    policy: dict[str, dict[str, list[str]]] = {}
    for label, rules in parsed.items():
        if not isinstance(label, str) or not isinstance(rules, dict):
            continue
        clean_rules: dict[str, list[str]] = {}
        for op in ("read", "write"):
            values = rules.get(op)
            if isinstance(values, str):
                clean_rules[op] = [values]
            elif isinstance(values, list):
                clean_rules[op] = [item for item in values if isinstance(item, str) and item.strip()]
        if clean_rules:
            policy[label] = clean_rules
    return policy


def _scope_pattern_matches(pattern: str, scope: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith("/*"):
        return scope.startswith(pattern[:-1])
    if pattern.endswith("*"):
        return scope.startswith(pattern[:-1])
    return pattern == scope


def _operation_authorized(token_label: str, operation: str, scope: str, policy: dict[str, dict[str, list[str]]], internal_labels: set[str]) -> tuple[bool, str, dict[str, Any]]:
    label = token_label or "none"
    rules = policy.get(label)
    if rules and operation in rules:
        patterns = rules[operation]
        allowed = any(_scope_pattern_matches(pattern, scope) for pattern in patterns)
        return allowed, "token_scope_policy", {
            "token_label": label,
            "operation": operation,
            "scope": scope,
            "allowed_patterns": patterns,
        }

    if operation == "read":
        return True, "default_read_allowed", {"token_label": label, "operation": operation, "scope": scope}

    if scope in PROTECTED_WRITE_SCOPES and label not in internal_labels:
        return False, "protected_scope_write_denied", {
            "token_label": label,
            "operation": operation,
            "scope": scope,
            "protected_write_scopes": sorted(PROTECTED_WRITE_SCOPES),
            "internal_token_labels": sorted(internal_labels),
            "hint": "Use a dedicated AICOS-maintainer access label such as a2-core-c, or configure AICOS_DAEMON_TOKEN_SCOPE_POLICY explicitly.",
        }

    return True, "default_write_allowed", {"token_label": label, "operation": operation, "scope": scope}


def _audit_log_path() -> Path:
    raw = os.environ.get("AICOS_DAEMON_AUDIT_LOG", "").strip()
    if raw:
        return Path(raw).expanduser()
    return Path.home() / "Library/Logs/aicos/mcp-audit.jsonl"


def _write_audit_event(payload: dict[str, Any]) -> None:
    path = _audit_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, ensure_ascii=False) + "\n"
    with _audit_lock:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)


def _tool_call_summary(message: dict[str, Any]) -> dict[str, Any]:
    params = message.get("params") or {}
    if not isinstance(params, dict):
        return {}
    arguments = params.get("arguments") or {}
    if not isinstance(arguments, dict):
        arguments = {}
    return {
        "tool_name": params.get("name"),
        "scope": arguments.get("scope"),
        "actor_role": arguments.get("actor_role") or arguments.get("actor"),
        "agent_family": arguments.get("agent_family"),
        "agent_instance_id": arguments.get("agent_instance_id"),
        "work_type": arguments.get("work_type"),
        "work_lane": arguments.get("work_lane"),
        "worktree_path": arguments.get("worktree_path"),
        "work_branch": arguments.get("work_branch"),
    }


def _result_status(result: dict[str, Any] | None) -> tuple[str, str | None]:
    if result is None:
        return "ok", None
    if "error" in result:
        error = result.get("error") or {}
        return "rpc_error", str(error.get("message") or error.get("code") or "unknown")
    payload = result.get("result")
    if not isinstance(payload, dict):
        return "ok", None
    if payload.get("isError"):
        content = payload.get("content") or []
        if content and isinstance(content, list):
            first = content[0]
            if isinstance(first, dict):
                text = first.get("text")
                if isinstance(text, str):
                    try:
                        parsed = json.loads(text)
                        error = parsed.get("error") or {}
                        return "tool_error", str(error.get("code") or error.get("message") or "unknown")
                    except json.JSONDecodeError:
                        return "tool_error", text[:200]
        return "tool_error", "unknown"
    return "ok", None


READ_IDENTITY_FIELD_HELP = {
    "agent_family": "Family/tool name of the reader, e.g. codex, claude-code, openclaw.",
    "agent_instance_id": "Stable id for this thread/worker/session, e.g. vm-alpha-01 or codex-thread-20260423-01.",
    "work_type": "Current work type: code, content, design, research, ops, review, planning, data, mixed, or orientation for first-contact/bootstrap reads.",
    "work_lane": "Current lane/task stream, e.g. telegram-pipeline, aicos-core, content-brief. Use intake for first-contact/bootstrap reads when the real lane is not known yet.",
    "execution_context": "Where this reader runs, e.g. codex-desktop, claude-desktop, openclaw-vm, cli.",
    "worktree_path": "Required when work_type=code. Absolute path of the checkout/worktree being used.",
    "work_branch": "Recommended when work_type=code. Branch name for the current worktree.",
}


def _validate_read_identity(arguments: dict[str, Any]) -> None:
    missing: list[str] = []
    for field in READ_IDENTITY_REQUIRED:
        value = arguments.get(field)
        if not isinstance(value, str) or not value.strip():
            missing.append(field)
    if missing:
        raise AicosMcpReadError(
            "missing_read_identity",
            "Read requests must include the minimum audit identity fields.",
            {
                "required": READ_IDENTITY_REQUIRED,
                "missing": missing,
                "field_help": {field: READ_IDENTITY_FIELD_HELP[field] for field in missing if field in READ_IDENTITY_FIELD_HELP},
                "example": {
                    "agent_family": "openclaw",
                    "agent_instance_id": "vm-alpha-01",
                    "work_type": "orientation",
                    "work_lane": "intake",
                    "execution_context": "openclaw-vm",
                },
            },
        )
    if str(arguments.get("work_type", "")).strip() == "code":
        worktree_path = arguments.get("worktree_path")
        if not isinstance(worktree_path, str) or not worktree_path.strip():
            raise AicosMcpReadError(
                "missing_read_identity",
                "Code read requests must include worktree_path.",
                {
                    "required_when": {"work_type": "code"},
                    "missing": ["worktree_path"],
                    "field_help": {"worktree_path": READ_IDENTITY_FIELD_HELP["worktree_path"]},
                    "recommended": {"work_branch": READ_IDENTITY_FIELD_HELP["work_branch"]},
                    "example": {
                        "work_type": "code",
                        "worktree_path": "/workspace/sample-workspace",
                        "work_branch": "feature/openclaw",
                    },
                },
            )


def _init_pg(repo_root: Path) -> str | None:
    """Try to connect to PG, apply schema, run full reindex.
    Returns None on success, error string on failure."""
    global _pg_search_engine, _pg_indexer
    try:
        from aicos_kernel.pg_search import (
            BrainIndexer, EmbeddingClient, PgSearchEngine, apply_schema,
            apply_vector_schema, embedding_config, try_connect,
        )
    except ImportError as exc:
        _pg_status.update({"postgresql": "unavailable", "engine": "markdown_direct", "embeddings": str(exc)})
        return f"pg_search module unavailable: {exc}"

    conn, err = try_connect()
    if err:
        _pg_status.update({"postgresql": err, "engine": "markdown_direct"})
        return err

    try:
        apply_schema(conn)
    except Exception as exc:
        _pg_status.update({"postgresql": f"schema failed: {exc}", "engine": "markdown_direct"})
        return f"Schema apply failed: {exc}"

    config = embedding_config()
    vector_enabled, vector_reason = apply_vector_schema(conn, config.dimensions)
    embedding_client = EmbeddingClient(config) if config.enabled else None
    if not vector_enabled:
        embedding_client = None

    indexer = BrainIndexer(
        repo_root,
        conn,
        embedding_client=embedding_client,
        embedding_config=config,
        vector_enabled=vector_enabled,
    )
    stats = indexer.full_reindex(with_embeddings=False)
    logger.info("PG index ready: %s", stats)
    logger.info("Embedding search: %s; %s", config.reason, vector_reason)

    with _pg_lock:
        _pg_search_engine = PgSearchEngine(
            conn,
            repo_root,
            embedding_client=embedding_client,
            embedding_config=config,
            vector_enabled=vector_enabled,
        )
        _pg_indexer = indexer
        _pg_status.update(
            {
                "engine": "postgresql_hybrid" if vector_enabled and config.enabled else "postgresql_fts",
                "postgresql": "active",
                "vector": vector_reason,
                "embeddings": config.reason,
                "embedding_model": config.model,
                "embedding_dimensions": config.dimensions,
                "index": stats,
                "embedding_index": "pending" if vector_enabled and config.enabled else "disabled",
            }
        )

    if vector_enabled and config.enabled:
        _schedule_embedding_reindex()

    return None


def _schedule_embedding_reindex(scope: str = "") -> None:
    if _pg_indexer is None:
        return

    def _run() -> None:
        with _pg_lock:
            _pg_status["embedding_index"] = "running"
        try:
            stats = _pg_indexer.full_embed_stale(scope=scope or "")
            logger.info("Embedding reindex%s: %s", f" scope={scope}" if scope else "", stats)
            with _pg_lock:
                _pg_status["embedding_index"] = "completed"
                _pg_status["last_embedding_reindex"] = stats
        except Exception as exc:  # noqa: BLE001 - background index must not kill daemon
            logger.warning("Embedding reindex failed%s: %s", f" scope={scope}" if scope else "", exc)
            with _pg_lock:
                _pg_status["embedding_index"] = f"failed: {exc}"

    threading.Thread(target=_run, daemon=True).start()


def _scope_reindex_root(scope: str) -> Path | None:
    if not scope.startswith("projects/") or scope.count("/") != 1:
        return None
    project_id = scope.removeprefix("projects/")
    root = REPO_ROOT / "brain" / "projects" / project_id
    return root if root.exists() else None


def _pg_query(arguments: dict[str, Any]) -> dict[str, Any] | None:
    """Run query via pg_search engine. Returns None if engine not available."""
    with _pg_lock:
        engine = _pg_search_engine
    if engine is None:
        return None
    scope   = arguments.get("scope", "")
    query   = arguments.get("query", "")
    actor   = arguments.get("actor", "A1")
    kinds   = arguments.get("context_kinds") or []
    maxr    = arguments.get("max_results", 5)
    stale   = bool(arguments.get("include_stale", False))
    project_role = str(arguments.get("project_role", "") or "")
    if not scope or not query:
        return None
    return engine.search(
        query=query, scope=scope, actor=actor,
        context_kinds=kinds, max_results=maxr, include_stale=stale,
        project_role=project_role,
    )


# ---------------------------------------------------------------------------
# Contract
# ---------------------------------------------------------------------------

 # Contract ack and read identity schema extensions are injected via
 # aicos_kernel.mcp_tool_schema.apply_aicos_tool_schema_extensions.

# ---------------------------------------------------------------------------
# Tool definitions (mirrors integrations/local-mcp-bridge/aicos_mcp_stdio.py)
# ---------------------------------------------------------------------------

TOOLS: list[dict[str, Any]] = [
    {
        "name": "aicos_get_startup_bundle",
        "description": "Return a compact AICOS startup bundle for one actor and project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string", "description": "Actor family/role, e.g. A1 or A2-Core-C."},
                "scope": {"type": "string", "description": "Project scope, e.g. projects/sample-project."},
            },
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_handoff_current",
        "description": "Return the H1 current handoff bundle for one project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {"actor": {"type": "string"}, "scope": {"type": "string"}},
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_packet_index",
        "description": "Return compact task packet index for one actor and project scope.",
        "inputSchema": {
            "type": "object",
            "properties": {"actor": {"type": "string"}, "scope": {"type": "string"}},
            "required": ["actor", "scope"],
        },
    },
    {
        "name": "aicos_get_task_packet",
        "description": "Return one selected task packet bundle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor": {"type": "string"}, "scope": {"type": "string"},
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
                "actor": {"type": "string"}, "scope": {"type": "string"},
                "status_filter":   {"type": "array", "items": {"type": "string"}},
                "item_type_filter":{"type": "array", "items": {"type": "string"}},
                "status_work_lane_filter":       {"type": "string", "description": "Optional filter for status item work_lane. Do not use read identity work_lane as a filter."},
                "status_agent_family_filter":    {"type": "string", "description": "Optional filter for status item agent_family. Do not use read identity agent_family as a filter."},
                "max_results":     {"type": "integer"},
                "include_stale":   {"type": "boolean"},
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
                "actor": {"type": "string"}, "scope": {"type": "string"},
                "include_candidate": {"type": "boolean"},
                "status_filter":     {"type": "array", "items": {"type": "string"}},
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
        "description": (
            "Bounded context search over AICOS project docs. "
            "Backed by PostgreSQL FTS (authority + freshness ranked) when available; "
            "falls back to markdown-direct keyword search otherwise."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor":  {"type": "string"},
                "scope":  {"type": "string"},
                "query":  {"type": "string"},
                "project_role": {"type": "string"},
                "context_kinds": {
                    "type": "array", "items": {"type": "string"},
                    "description": (
                        "Optional filter: current_state, current_direction, handoff, "
                        "packets, status_items, task_state, workstreams, artifacts, "
                        "open_items, open_questions, canonical, policy, contract, project_registry. "
                        "Leave empty to let intent detection choose."
                    ),
                },
                "max_results":  {"type": "integer"},
                "include_stale":{"type": "boolean"},
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
                "scope": {"type": "string"}, "actor_role": {"type": "string"},
                "agent_family": {"type": "string"}, "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "checkpoint_type": {"type": "string", "enum": ["review","validation","artifact","blocked","continuation"]},
                "summary": {"type": "string"}, "status": {"type": "string", "enum": ["completed","blocked","partial"]},
                "client_request_id": {"type": "string"}, "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"}, "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}}, "notes": {"type": "string"},
            },
            "required": ["scope","actor_role","agent_family","agent_instance_id","work_type","work_lane","checkpoint_type","summary","status"],
        },
    },
    {
        "name": "aicos_write_task_update",
        "description": "Write bounded project task continuity state.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"}, "task_ref": {"type": "string"},
                "actor_role": {"type": "string"}, "agent_family": {"type": "string"},
                "agent_instance_id": {"type": "string"}, "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "task_status": {"type": "string", "enum": ["planned","in_progress","completed","blocked","waiting"]},
                "what_is_done": {"type": "string"}, "what_is_blocked": {"type": "string"}, "next_step": {"type": "string"},
                "client_request_id": {"type": "string"}, "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"}, "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope","task_ref","actor_role","agent_family","agent_instance_id","work_type","work_lane","task_status","what_is_done"],
        },
    },
    {
        "name": "aicos_write_handoff_update",
        "description": "Add or replace one compact current-continuity section in project handoff/current.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"}, "actor_role": {"type": "string"},
                "agent_family": {"type": "string"}, "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "summary": {"type": "string"}, "status": {"type": "string", "enum": ["completed","blocked","partial","ready_for_next"]},
                "next_step": {"type": "string"}, "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"}, "packet_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}}, "notes": {"type": "string"},
            },
            "required": ["scope","actor_role","agent_family","agent_instance_id","work_type","work_lane","summary","status","next_step"],
        },
    },
    {
        "name": "aicos_update_status_item",
        "description": "Upsert a structured project status item.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"}, "actor_role": {"type": "string"},
                "agent_family": {"type": "string"}, "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "item_id": {"type": "string"}, "item_type": {"type": "string", "enum": ["open_item","open_question","tech_debt","decision_followup"]},
                "item_status": {"type": "string", "enum": ["open","resolved","closed","stale","deferred","blocked"]},
                "title": {"type": "string"}, "summary": {"type": "string"}, "reason": {"type": "string"},
                "next_step": {"type": "string"}, "source_ref": {"type": "string"},
                "client_request_id": {"type": "string"}, "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"}, "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope","actor_role","agent_family","agent_instance_id","work_type","work_lane","item_id","item_type","item_status","title","summary"],
        },
    },
    {
        "name": "aicos_register_artifact_ref",
        "description": "Register a compact artifact reference without copying artifact body into AICOS.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"}, "actor_role": {"type": "string"},
                "agent_family": {"type": "string"}, "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "artifact_kind": {"type": "string", "enum": ["note","report","diff","output","analysis","contract_check","dataset","design","content","other"]},
                "title": {"type": "string"}, "artifact_ref": {"type": "string"}, "summary": {"type": "string"},
                "source_ref": {"type": "string"}, "client_request_id": {"type": "string"},
                "startup_bundle_ref": {"type": "string"}, "packet_ref": {"type": "string"},
                "handoff_ref": {"type": "string"}, "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope","actor_role","agent_family","agent_instance_id","work_type","work_lane","artifact_kind","title","artifact_ref","summary"],
        },
    },
    {
        "name": "aicos_record_feedback",
        "description": "Record a structured AICOS/project context-serving feedback signal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string"}, "actor_role": {"type": "string"},
                "agent_family": {"type": "string"}, "agent_instance_id": {"type": "string"},
                "agent_display_name": {"type": "string"},
                "work_type": {"type": "string", "enum": WORK_TYPE_ENUM},
                "work_lane": {"type": "string"}, "coordination_status": {"type": "string", "enum": ["active","paused","blocked","handoff_ready","completed"]},
                "artifact_scope": {"type": "string"}, "work_branch": {"type": "string"}, "worktree_path": {"type": "string"},
                "execution_context": {"type": "string"}, "actor_family": {"type": "string"}, "logical_role": {"type": "string"}, "work_context": {"type": "string"},
                "feedback_type": {"type": "string", "enum": ["no_issue","query_failed","stale_result","context_missing","context_overload","rule_confusing","tool_missing","tool_shape_confusing","tool_too_heavy","bootstrap_confusing","write_schema_confusing","interop_problem","packet_missing_ref","handoff_too_long","role_context_wrong","routing_confusing","other"]},
                "severity": {"type": "string", "enum": ["low","medium","high","critical"]},
                "title": {"type": "string"}, "summary": {"type": "string"}, "observed_in": {"type": "string"},
                "recommendation": {"type": "string"}, "source_ref": {"type": "string"},
                "client_request_id": {"type": "string"}, "startup_bundle_ref": {"type": "string"},
                "packet_ref": {"type": "string"}, "handoff_ref": {"type": "string"},
                "artifact_refs": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["scope","actor_role","agent_family","agent_instance_id","work_type","work_lane","feedback_type","severity","title","summary"],
        },
    },
]

TOOLS = build_tools()
apply_aicos_tool_schema_extensions(TOOLS)

# ---------------------------------------------------------------------------
# JSON-RPC helpers
# ---------------------------------------------------------------------------

def _response(msg_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}

def _error_response(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}

def _tool_result(payload: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}], "isError": False}

def _tool_error(exc) -> dict[str, Any]:
    body = {"error": {"code": exc.code, "message": exc.message, "details": exc.details}}
    return {"content": [{"type": "text", "text": json.dumps(body, indent=2, ensure_ascii=False)}], "isError": True}


def _authorization_tool_error(code: str, message: str, details: dict[str, Any]) -> dict[str, Any]:
    body = {"error": {"code": code, "message": message, "details": details}}
    return {"content": [{"type": "text", "text": json.dumps(body, indent=2, ensure_ascii=False)}], "isError": True}

# ---------------------------------------------------------------------------
# Core MCP handler (cache + pg_search aware)
# ---------------------------------------------------------------------------

def handle(message: dict[str, Any], cache: ResponseCache | None = None, *, token_label: str = "", scope_policy: dict[str, dict[str, list[str]]] | None = None, internal_token_labels: set[str] | None = None) -> dict[str, Any] | None:
    method  = message.get("method")
    msg_id  = message.get("id")
    params  = message.get("params") or {}

    if method == "initialize":
        with _pg_lock:
            pg_status = str(_pg_status.get("engine", "markdown_direct"))
        return _response(msg_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {"subscribe": False, "listChanged": False},
                "prompts": {"listChanged": False},
            },
            "serverInfo": {"name": "aicos-mcp-daemon", "version": "0.7.0", "search_engine": pg_status},
        })

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return _response(msg_id, {})

    if method == "tools/list":
        return _response(msg_id, {"tools": TOOLS})

    if method == "resources/list":
        return _response(msg_id, {"resources": []})

    if method == "resources/templates/list":
        return _response(msg_id, {"resourceTemplates": []})

    if method == "prompts/list":
        return _response(msg_id, {"prompts": []})

    if method == "tools/call":
        name      = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(name, str):
            return _error_response(msg_id, -32602, "Missing tool name")
        if not isinstance(arguments, dict):
            return _error_response(msg_id, -32602, "Tool arguments must be an object")

        try:
            if name in READ_TOOL_NAMES:
                authorized, reason, details = _operation_authorized(
                    token_label,
                    "read",
                    str(arguments.get("scope", "")),
                    scope_policy or {},
                    internal_token_labels or DEFAULT_INTERNAL_TOKEN_LABELS,
                )
                if not authorized:
                    return _response(msg_id, _authorization_tool_error("scope_read_denied", "This token is not allowed to read this AICOS scope.", {**details, "reason": reason}))
                _validate_read_identity(arguments)
                # Check response cache first
                cached = cache.get(name, arguments) if cache else None
                if cached is not None:
                    logger.debug("cache hit: %s", name)
                    return _response(msg_id, _tool_result(cached))

                # PostgreSQL search for query tool
                if name == "aicos_query_project_context":
                    pg_result = _pg_query(arguments)
                    if pg_result is not None:
                        if cache:
                            cache.set(name, arguments, pg_result)
                        return _response(msg_id, _tool_result(pg_result))
                    # Fall through to markdown-direct fallback

                payload = dispatch_read_surface(name, arguments)
                if cache:
                    cache.set(name, arguments, payload)

            elif name in WRITE_TOOL_NAMES:
                authorized, reason, details = _operation_authorized(
                    token_label,
                    "write",
                    str(arguments.get("scope", "")),
                    scope_policy or {},
                    internal_token_labels or DEFAULT_INTERNAL_TOKEN_LABELS,
                )
                if not authorized:
                    return _response(msg_id, _authorization_tool_error("scope_write_denied", "This token is not allowed to write this AICOS scope.", {**details, "reason": reason}))
                payload = dispatch_write_tool(name, arguments)
                if cache:
                    cache.invalidate_scope(arguments.get("scope", ""))
                # Trigger pg reindex for the written scope (best-effort, background)
                _schedule_reindex(arguments.get("scope", ""))

            else:
                return _error_response(msg_id, -32601, f"Unknown tool: {name}")

        except (AicosMcpReadError, AicosMcpWriteError) as exc:
            return _response(msg_id, _tool_error(exc))

        return _response(msg_id, _tool_result(payload))

    return _error_response(msg_id, -32601, f"Unsupported method: {method}")


def _schedule_reindex(scope: str) -> None:
    """Debounced best-effort reindex for one scope after semantic writes."""
    if not scope or _pg_indexer is None:
        return
    try:
        delay = max(0.0, float(os.environ.get("AICOS_REINDEX_DEBOUNCE_SECONDS", "3")))
    except ValueError:
        delay = 3.0
    with _reindex_lock:
        state = _reindex_state.setdefault(scope, {"running": False, "pending": False, "timer": None})
        if state.get("running"):
            state["pending"] = True
            with _pg_lock:
                _pg_status["reindex"] = {"scope": scope, "status": "pending"}
            return
        timer = state.get("timer")
        if timer is not None:
            timer.cancel()
        state["timer"] = threading.Timer(delay, _run_reindex, args=(scope,))
        state["timer"].daemon = True
        state["timer"].start()
        with _pg_lock:
            _pg_status["reindex"] = {"scope": scope, "status": "scheduled", "debounce_seconds": delay}


def _run_reindex(scope: str) -> None:
    with _reindex_lock:
        state = _reindex_state.setdefault(scope, {"running": False, "pending": False, "timer": None})
        state["timer"] = None
        if state.get("running"):
            state["pending"] = True
            return
        state["running"] = True
        state["pending"] = False
    stats = {"indexed": 0, "skipped": 0, "embedded": 0, "embedding_errors": 0, "errors": 0}
    try:
        root = _scope_reindex_root(scope)
        if root is None:
            return
        for path in root.rglob("*.md"):
            result = _pg_indexer.reindex_file(path, with_embeddings=False)
            if result:
                stats["indexed"] += 1
            else:
                stats["skipped"] += 1
        logger.info("Background reindex scope=%s: %s", scope, stats)
        with _pg_lock:
            _pg_status["reindex"] = {"scope": scope, "status": "completed", "stats": stats}
        _schedule_embedding_reindex(scope)
    except Exception as exc:
        logger.warning("Background reindex failed for scope=%s: %s", scope, exc)
        with _pg_lock:
            _pg_status["reindex"] = {"scope": scope, "status": f"failed: {exc}", "stats": stats}
    finally:
        rerun = False
        with _reindex_lock:
            state = _reindex_state.setdefault(scope, {"running": False, "pending": False, "timer": None})
            rerun = bool(state.get("pending"))
            state["running"] = False
            state["pending"] = False
        if rerun:
            _schedule_reindex(scope)

# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class _ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class _MCPHandler(BaseHTTPRequestHandler):
    cache: ResponseCache
    token: str = ""
    accepted_tokens: dict[str, str] = {}
    allowlist: list[ipaddress._BaseNetwork] = []
    scope_policy: dict[str, dict[str, list[str]]] = {}
    internal_token_labels: set[str] = DEFAULT_INTERNAL_TOKEN_LABELS

    def _token_candidate_and_label(self) -> tuple[str, str]:
        bearer = self.headers.get("Authorization", "")
        api_token = self.headers.get("X-AICOS-Token", "")
        candidate = api_token
        if bearer.startswith("Bearer "):
            candidate = bearer.removeprefix("Bearer ")
        label = ""
        if candidate:
            for name, token in self.accepted_tokens.items():
                if token == candidate:
                    label = name
                    break
            if not label and self.token and candidate == self.token:
                label = "default"
        return candidate, label

    def _authorized(self) -> tuple[bool, str]:
        if self.allowlist:
            try:
                remote = ipaddress.ip_address(self.client_address[0])
            except ValueError:
                return False, ""
            if not any(remote in network for network in self.allowlist):
                return False, "ip_blocked"
        if not self.accepted_tokens and not self.token:
            return True, "unauthenticated"
        candidate, label = self._token_candidate_and_label()
        if not candidate:
            return False, ""
        return candidate in self.accepted_tokens.values() or candidate == self.token, label

    def _auth_capabilities(self) -> dict[str, Any]:
        accepted_labels = sorted(self.accepted_tokens.keys())
        allowlist_networks = [str(network) for network in self.allowlist]
        return {
            "mode": "token_required" if (self.accepted_tokens or self.token) else "none",
            "accepted_token_labels": accepted_labels,
            "allowlist_enabled": bool(self.allowlist),
            "allowlist_networks": allowlist_networks,
            "scope_authorization": {
                "policy_env": "AICOS_DAEMON_TOKEN_SCOPE_POLICY",
                "internal_token_labels": sorted(self.internal_token_labels),
                "protected_write_scopes": sorted(PROTECTED_WRITE_SCOPES),
                "configured_policy_labels": sorted(self.scope_policy.keys()),
                "default": "read allowed for authenticated tokens; write allowed except protected scopes for non-internal token labels",
            },
            "oauth_supported": False,
            "query_token_supported": False,
            "supported_client_profiles": [
                {
                    "id": "codex-http",
                    "transport": "streamable_http",
                    "auth": "bearer_header",
                    "url": "/mcp",
                    "notes": "Use daemon bearer token in Authorization header.",
                },
                {
                    "id": "openclaw-vm",
                    "transport": "streamable_http",
                    "auth": "bearer_header",
                    "url": "/mcp",
                    "notes": "Use a labeled client token for VM/LAN access.",
                },
                {
                    "id": "claude-desktop-local",
                    "transport": "https_proxy_localhost",
                    "auth": "local_proxy_injects_upstream_bearer",
                    "url": "https://localhost:8443/mcp",
                    "notes": "Claude Desktop connector beta does not expose custom bearer headers in the current UI. Use the local HTTPS proxy on the same machine.",
                },
            ],
        }

    def _audit(self, *, status: str, path: str, duration_ms: int | None = None, message: dict[str, Any] | None = None, error: str | None = None, token_label: str = "", http_status: int | None = None) -> None:
        summary = _tool_call_summary(message or {})
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "remote_ip": self.client_address[0] if self.client_address else "",
            "http_method": self.command,
            "path": path,
            "http_status": http_status,
            "status": status,
            "duration_ms": duration_ms,
            "token_label": token_label or "none",
            "rpc_method": (message or {}).get("method"),
            "rpc_id": (message or {}).get("id"),
            **summary,
        }
        if error:
            payload["error"] = error
        _write_audit_event(payload)

    def do_POST(self) -> None:
        start = time.time()
        parsed = urllib.parse.urlparse(self.path)
        authorized, token_label = self._authorized()
        if not authorized:
            self._audit(status="unauthorized", path=parsed.path.rstrip("/"), duration_ms=round((time.time() - start) * 1000), error="Unauthorized", token_label=token_label, http_status=401)
            self._reply_error(401, "Unauthorized"); return
        if not parsed.path.rstrip("/").endswith("/mcp"):
            self._audit(status="not_found", path=parsed.path.rstrip("/"), duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=404)
            self._reply_error(404, "Not found"); return
        raw_len = self.headers.get("Content-Length", "")
        if not raw_len.isdigit():
            self._audit(status="invalid_request", path=parsed.path.rstrip("/"), duration_ms=round((time.time() - start) * 1000), error="Content-Length required", token_label=token_label, http_status=411)
            self._reply_error(411, "Content-Length required"); return
        length = int(raw_len)
        if length > 2_000_000:
            self._audit(status="too_large", path=parsed.path.rstrip("/"), duration_ms=round((time.time() - start) * 1000), error="Too large", token_label=token_label, http_status=413)
            self._reply_error(413, "Too large"); return
        body = self.rfile.read(length) if length else b""
        try:
            message = json.loads(body)
        except json.JSONDecodeError as exc:
            self._audit(status="parse_error", path=parsed.path.rstrip("/"), duration_ms=round((time.time() - start) * 1000), error=str(exc), token_label=token_label, http_status=200)
            self._reply_json(_error_response(None, -32700, f"Parse error: {exc}")); return
        result = handle(message, self.cache, token_label=token_label, scope_policy=self.scope_policy, internal_token_labels=self.internal_token_labels)
        status, error = _result_status(result)
        duration_ms = round((time.time() - start) * 1000)
        query = urllib.parse.parse_qs(parsed.query)
        session_id = (query.get("session_id") or [""])[0]
        if session_id:
            with _sse_lock:
                session_queue = _sse_sessions.get(session_id)
            if session_queue is None:
                self._audit(status="sse_session_missing", path=parsed.path.rstrip("/"), duration_ms=duration_ms, message=message, error="SSE session not found", token_label=token_label, http_status=404)
                self._reply_error(404, "SSE session not found"); return
            if result is not None:
                session_queue.put(result)
            self._audit(status=status, path=parsed.path.rstrip("/"), duration_ms=duration_ms, message=message, error=error, token_label=token_label, http_status=202)
            self.send_response(202)
            self.end_headers()
            return
        if result is None:
            self._audit(status=status, path=parsed.path.rstrip("/"), duration_ms=duration_ms, message=message, error=error, token_label=token_label, http_status=204)
            self.send_response(204); self.end_headers()
        else:
            self._audit(status=status, path=parsed.path.rstrip("/"), duration_ms=duration_ms, message=message, error=error, token_label=token_label, http_status=200)
            self._reply_json(result)

    def do_GET(self) -> None:
        start = time.time()
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        authorized, token_label = self._authorized()
        if not authorized:
            self._audit(status="unauthorized", path=path, duration_ms=round((time.time() - start) * 1000), error="Unauthorized", token_label=token_label, http_status=401)
            self._reply_error(401, "Unauthorized"); return
        if path.endswith("/health"):
            with _pg_lock:
                engine = _pg_search_engine
                status = dict(_pg_status)
            index_stats = {}
            index_error = None
            if engine is not None:
                try:
                    index_stats = engine.index_stats()
                except Exception as exc:  # noqa: BLE001 - health must degrade, not crash
                    index_error = str(exc)
                    logger.warning("Health index_stats failed: %s", exc)
            self._audit(status="ok", path=path, duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=200)
            self._reply_json({
                "status": "ok",
                "search_engine": status.get("engine", "markdown_direct"),
                "cache_entries": self.cache.size(),
                "auth": "token_required" if self.token else "none",
                "auth_capabilities": self._auth_capabilities(),
                "index": index_stats,
                "index_error": index_error,
                "search_status": status,
            })
        elif path.endswith("/reindex") and _pg_indexer is not None:
            query = urllib.parse.parse_qs(parsed.query)
            wait = (query.get("wait") or ["0"])[0] in {"1", "true", "yes"}
            if wait:
                stats = _pg_indexer.full_reindex(with_embeddings=False)
                logger.info("Manual reindex (wait=1): %s", stats)
                _schedule_embedding_reindex()
                self._audit(status="ok", path=path, duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=200)
                self._reply_json({"status": "reindex_completed", "stats": stats})
            else:
                def _full():
                    stats = _pg_indexer.full_reindex(with_embeddings=False)
                    logger.info("Manual reindex: %s", stats)
                    _schedule_embedding_reindex()
                self._audit(status="ok", path=path, duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=200)
                threading.Thread(target=_full, daemon=True).start()
                self._reply_json({"status": "reindex_started"})
        elif path.endswith("/mcp"):
            self._audit(status="sse_open", path=path, duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=200)
            self._serve_sse()
        else:
            self._audit(status="not_found", path=path, duration_ms=round((time.time() - start) * 1000), token_label=token_label, http_status=404)
            self._reply_error(404, "Not found")

    def _serve_sse(self) -> None:
        session_id = uuid.uuid4().hex
        session_queue: "queue.Queue[dict[str, Any]]" = queue.Queue()
        with _sse_lock:
            _sse_sessions[session_id] = session_queue
        endpoint = f"/mcp?session_id={session_id}"
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        try:
            self._sse_event("endpoint", endpoint)
            keepalive_seconds = max(1, int(os.environ.get("AICOS_SSE_KEEPALIVE_SECONDS", "5")))
            while True:
                try:
                    message = session_queue.get(timeout=keepalive_seconds)
                except queue.Empty:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
                    continue
                self._sse_event("message", json.dumps(message, ensure_ascii=False))
        except (BrokenPipeError, ConnectionResetError):
            logger.info("SSE client disconnected: %s", session_id)
        finally:
            self.close_connection = True
            with _sse_lock:
                _sse_sessions.pop(session_id, None)

    def _sse_event(self, event: str, data: str) -> None:
        payload = f"event: {event}\ndata: {data}\n\n".encode("utf-8")
        self.wfile.write(payload)
        self.wfile.flush()

    def _reply_json(self, data: Any) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _reply_error(self, code: int, text: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(text.encode())

    def log_message(self, fmt: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="AICOS MCP HTTP Daemon")
    parser.add_argument("--host",      default="127.0.0.1")
    parser.add_argument("--port",      type=int, default=8000)
    parser.add_argument("--cache-ttl", type=int, default=30, metavar="SECONDS")
    parser.add_argument("--no-pg",     action="store_true", help="Disable PostgreSQL, use markdown-direct only")
    parser.add_argument("--token",     default="", help="Require this bearer/X-AICOS-Token for HTTP requests")
    parser.add_argument("--allow-unauthenticated-lan", action="store_true", help="Allow non-loopback bind without a token")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG","INFO","WARNING","ERROR"])
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Try PostgreSQL
    if not args.no_pg:
        logger.info("Connecting to PostgreSQL…")
        err = _init_pg(REPO_ROOT)
        if err:
            logger.warning("PostgreSQL unavailable (%s) — falling back to markdown-direct search", err)
        else:
            logger.info("PostgreSQL search engine active")
    else:
        logger.info("PostgreSQL disabled via --no-pg flag")

    ttl   = max(0, args.cache_ttl)
    cache = ResponseCache(ttl=ttl) if ttl > 0 else ResponseCache(ttl=0)
    token = args.token or os.environ.get("AICOS_DAEMON_TOKEN", "")
    accepted_tokens = _parse_token_set(token)
    allowlist = _parse_allowlist()
    internal_token_labels = DEFAULT_INTERNAL_TOKEN_LABELS | _parse_csv_set(os.environ.get("AICOS_DAEMON_INTERNAL_TOKEN_LABELS", ""))
    scope_policy = _parse_token_scope_policy()
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not token and not args.allow_unauthenticated_lan:
        logger.error("Refusing LAN/non-loopback bind without AICOS_DAEMON_TOKEN/--token.")
        logger.error("Set a token, or pass --allow-unauthenticated-lan only on an isolated trusted network.")
        return 2
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not token:
        logger.warning("LAN/non-loopback bind without auth is explicitly allowed. Use only on an isolated trusted network.")

    class _Handler(_MCPHandler):
        pass
    _Handler.cache = cache
    _Handler.token = token
    _Handler.accepted_tokens = accepted_tokens
    _Handler.allowlist = allowlist
    _Handler.scope_policy = scope_policy
    _Handler.internal_token_labels = internal_token_labels

    server = _ThreadingHTTPServer((args.host, args.port), _Handler)

    logger.info("AICOS MCP daemon started")
    logger.info("  endpoint : http://%s:%d/mcp",    args.host, args.port)
    logger.info("  health   : http://%s:%d/health", args.host, args.port)
    logger.info("  reindex  : GET http://%s:%d/reindex", args.host, args.port)
    logger.info("  cache TTL: %ds", ttl)
    logger.info("  auth     : %s", "token required" if token else "none")
    if accepted_tokens:
        logger.info("  accepted tokens: %s", ", ".join(sorted(accepted_tokens.keys())))
    if allowlist:
        logger.info("  allowlist: %s", ", ".join(str(item) for item in allowlist))
    logger.info("  internal token labels: %s", ", ".join(sorted(internal_token_labels)) or "(none)")
    if scope_policy:
        logger.info("  token scope policy labels: %s", ", ".join(sorted(scope_policy.keys())))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
