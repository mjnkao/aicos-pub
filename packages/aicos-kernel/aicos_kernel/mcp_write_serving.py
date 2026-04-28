from __future__ import annotations

import hashlib
import fcntl
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .mcp_contract_status import contract_error_details, contract_status_payload


REPO_ROOT = Path(__file__).resolve().parents[3]
LOCK_ROOT = REPO_ROOT / ".runtime-home/aicos-write-locks"


class AicosMcpWriteError(ValueError):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = contract_error_details(details)


ALLOWED_CHECKPOINT_TYPES = {"review", "validation", "artifact", "blocked", "continuation"}
ALLOWED_CHECKPOINT_STATUSES = {"completed", "blocked", "partial"}
ALLOWED_TASK_STATUSES = {"planned", "in_progress", "completed", "blocked", "waiting"}
ALLOWED_HANDOFF_STATUSES = {"completed", "blocked", "partial", "ready_for_next"}
ALLOWED_WORK_TYPES = {"code", "content", "design", "research", "ops", "review", "planning", "data", "mixed", "orientation"}
ALLOWED_COORDINATION_STATUSES = {"active", "paused", "blocked", "handoff_ready", "completed"}
ALLOWED_STATUS_ITEM_TYPES = {"open_item", "open_question", "tech_debt", "decision_followup"}
ALLOWED_STATUS_ITEM_STATUSES = {"open", "resolved", "closed", "stale", "deferred", "blocked"}
ALLOWED_ARTIFACT_KINDS = {"note", "report", "diff", "output", "analysis", "contract_check", "dataset", "design", "content", "other"}
ALLOWED_FEEDBACK_TYPES = {
    "no_issue",
    "query_failed",
    "stale_result",
    "context_missing",
    "context_overload",
    "rule_confusing",
    "tool_missing",
    "tool_shape_confusing",
    "tool_too_heavy",
    "bootstrap_confusing",
    "write_schema_confusing",
    "interop_problem",
    "packet_missing_ref",
    "handoff_too_long",
    "role_context_wrong",
    "routing_confusing",
    "other",
}
ALLOWED_FEEDBACK_SEVERITIES = {"low", "medium", "high", "critical"}
FORBIDDEN_RAW_WRITE_KEYS = {"path", "target_path", "file_path", "content", "markdown", "raw_text", "append_text"}
SUMMARY_MAX_LEN = 1500
HANDOFF_SUMMARY_MAX_LEN = 1200
STATUS_ITEM_TYPE_GUIDANCE = {
    "open_item": "New actionable work that is not primarily an existing defect/debt, unresolved question, or decision follow-up.",
    "open_question": "Unresolved question needing human, architecture, product, or project decision before the next clear action.",
    "tech_debt": "Known existing issue, friction, missing validation/coverage/docs, stale behavior, cleanup, or quality gap.",
    "decision_followup": "A decision already made that needs tracking through implementation, rollout, verification, or cleanup.",
}


def normalize_actor_role(actor_role: str) -> str:
    normalized = actor_role.strip().lower().replace("_", "-")
    aliases = {
        "a2": "A2-Core-C",
        "a2-core": "A2-Core-C",
        "a2-core-c": "A2-Core-C",
        "a2-core-r": "A2-Core-R",
        "a1": "A1",
        "a1-work": "A1",
        "a1-work-agent": "A1",
        "external": "A1",
        "external-agent": "A1",
    }
    # For AICOS, client names such as Antigravity, Claude, Codex, and OpenClaw
    # are external A1 actors unless the request explicitly says A2.
    return aliases.get(normalized, "A1")


def feedback_nudge(trigger: str, reason: str) -> dict[str, Any]:
    return {
        "ask_now": True,
        "trigger": trigger,
        "reason": reason,
        "preferred_action": "aicos_record_feedback",
        "prompt": [
            "Bạn có gặp khó khăn gì khi dùng AICOS trong pass vừa rồi không?",
            "Có tool nào còn thiếu hoặc đang gây chậm/nhầm không?",
            "Nếu chỉ sửa một thứ để tiết kiệm thời gian nhất, đó là gì?",
        ],
        "closure_rule": "Before session-close writes, record either aicos_record_feedback with a real issue or feedback_type=no_issue.",
    }


def expected_contract_ack() -> str:
    status = contract_status_payload()
    return str(status["write_contract_ack_value"])


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")
    return path


def safe_slug(value: str, fallback: str = "item") -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-").lower()
    return slug[:80] or fallback


@contextmanager
def scope_write_lock(scope: str):
    """Serialize semantic writes for one project scope across MCP processes."""
    LOCK_ROOT.mkdir(parents=True, exist_ok=True)
    lock_name = safe_slug(scope, fallback="global") + ".lock"
    with (LOCK_ROOT / lock_name).open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def validate_scope(scope: str) -> tuple[str, Path]:
    if not scope.startswith("projects/") or scope.count("/") != 1:
        raise AicosMcpWriteError(
            "unsupported_scope",
            "Phase 2 write tools support project scopes only.",
            {"scope": scope, "supported_shape": "projects/<project-id>"},
        )
    project_id = scope.split("/", 1)[1]
    project_root = REPO_ROOT / "brain/projects" / project_id
    if not project_root.exists():
        raise AicosMcpWriteError("missing_project_scope", "Project scope does not exist.", {"scope": scope, "path": rel(project_root)})
    return project_id, project_root


def reject_raw_write_keys(payload: dict[str, Any]) -> None:
    found = sorted(FORBIDDEN_RAW_WRITE_KEYS.intersection(payload))
    if found:
        raise AicosMcpWriteError(
            "raw_write_semantics_rejected",
            "MCP write tools accept structured continuity intent, not raw file edit payloads.",
            {"forbidden_keys": found},
        )


def require_contract_ack(payload: dict[str, Any]) -> None:
    expected = expected_contract_ack()
    received = payload.get("mcp_contract_ack")
    if received != expected:
        raise AicosMcpWriteError(
            "write_contract_ack_required",
            "This AICOS MCP write schema changed. Refresh tools/list or restart/re-enable the AICOS MCP server before writing.",
            {
                "required_field": "mcp_contract_ack",
                "expected_value": expected,
                "received_value": received,
                "reason": "Prevents stale MCP clients from writing status/open-item content into old handoff or task-state lanes.",
            },
        )


def require_string(payload: dict[str, Any], field: str, max_len: int = 600) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AicosMcpWriteError("missing_required_field", f"{field} is required.", {"field": field})
    stripped = value.strip()
    if len(stripped) > max_len:
        raise AicosMcpWriteError("field_too_long", f"{field} is too long for a small structured write.", {"field": field, "max_len": max_len})
    return stripped


def optional_string(payload: dict[str, Any], field: str, max_len: int = 600) -> str:
    value = payload.get(field, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        raise AicosMcpWriteError("invalid_field_type", f"{field} must be a string.", {"field": field})
    stripped = value.strip()
    if len(stripped) > max_len:
        raise AicosMcpWriteError("field_too_long", f"{field} is too long for a small structured write.", {"field": field, "max_len": max_len})
    return stripped


def optional_refs(payload: dict[str, Any], field: str) -> list[str]:
    value = payload.get(field, [])
    if value in ("", None):
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise AicosMcpWriteError("invalid_refs", f"{field} must be a list of non-empty strings.", {"field": field})
    refs = [item.strip() for item in value]
    if len(refs) > 12:
        raise AicosMcpWriteError("too_many_refs", f"{field} has too many refs for one bounded write.", {"field": field, "max": 12})
    for item in refs:
        if len(item) > 240:
            raise AicosMcpWriteError("ref_too_long", f"{field} contains a ref that is too long.", {"field": field, "max_len": 240})
    return refs


def enum_value(payload: dict[str, Any], field: str, allowed: set[str]) -> str:
    value = require_string(payload, field, max_len=80)
    if value not in allowed:
        raise AicosMcpWriteError("invalid_enum", f"{field} is not allowed.", {"field": field, "allowed": sorted(allowed), "received": value})
    return value


def write_id(tool: str, payload: dict[str, Any], timestamp: str) -> str:
    request_id = optional_string(payload, "client_request_id", max_len=120)
    if request_id:
        return safe_slug(request_id, fallback="request")
    seed_fields = [
        tool,
        payload.get("scope", ""),
        payload.get("task_ref", ""),
        payload.get("work_context", ""),
        payload.get("summary", ""),
        payload.get("what_is_done", ""),
        timestamp,
    ]
    digest = hashlib.sha1("|".join(str(item) for item in seed_fields).encode("utf-8")).hexdigest()[:10]
    return f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{digest}"


def refs_block(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for field in ["startup_bundle_ref", "packet_ref", "handoff_ref"]:
        value = optional_string(payload, field, max_len=240)
        if value:
            lines.append(f"- {field}: `{value}`")
    artifact_refs = optional_refs(payload, "artifact_refs")
    if artifact_refs:
        lines.append("- artifact_refs:")
        lines.extend(f"  - `{item}`" for item in artifact_refs)
    return lines


def actor_identity_block(base: dict[str, str]) -> list[str]:
    lines = [
        f"Actor role: `{base['actor_role']}`",
        f"Agent family: `{base['agent_family']}`",
        f"Agent instance id: `{base['agent_instance_id']}`",
        f"Agent display name: `{base['agent_display_name']}`",
        f"Work type: `{base['work_type']}`",
        f"Work lane: `{base['work_lane']}`",
        f"Coordination status: `{base['coordination_status']}`",
        f"Artifact scope: `{base['artifact_scope']}`",
        f"Work branch: `{base['work_branch']}`",
        f"Worktree path: `{base['worktree_path']}`",
        f"Execution context: `{base['execution_context']}`",
        f"Legacy actor family: `{base['actor_family']}`",
        f"Legacy logical role: `{base['logical_role']}`",
        f"Work context: `{base['work_context']}`",
    ]
    if base.get("submitted_actor_role") and base.get("submitted_actor_role") != base.get("actor_role"):
        lines.insert(1, f"Submitted actor role: `{base['submitted_actor_role']}`")
    return lines


def trace_metadata(tool: str, payload: dict[str, Any], target_paths: list[Path], timestamp: str, write_id_value: str) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "kind": "aicos.mcp.write_result",
        "tool": tool,
        "write_id": write_id_value,
        "written_at": timestamp,
        "scope": payload.get("scope", ""),
        "actor_role": payload.get("actor_role", ""),
        "agent_family": payload.get("agent_family", ""),
        "agent_instance_id": payload.get("agent_instance_id", ""),
        "agent_display_name": payload.get("agent_display_name", ""),
        "work_type": payload.get("work_type", ""),
        "work_lane": payload.get("work_lane", ""),
        "coordination_status": payload.get("coordination_status", ""),
        "artifact_scope": payload.get("artifact_scope", ""),
        "work_branch": payload.get("work_branch", ""),
        "worktree_path": payload.get("worktree_path", ""),
        "execution_context": payload.get("execution_context", ""),
        "actor_family": payload.get("actor_family", ""),
        "logical_role": payload.get("logical_role", ""),
        "work_context": payload.get("work_context", ""),
        "task_ref": payload.get("task_ref", ""),
        "target_paths": [rel(path) for path in target_paths],
        "authority": "AICOS MCP validates, maps, formats, and records semantic continuity writes.",
    }


def markdown_list(items: list[str]) -> list[str]:
    return items if items else ["- none"]


def _feedback_match(path: Path, scope: str, agent_family: str, agent_instance_id: str, work_lane: str) -> bool:
    body = read_text(path)
    return all(
        needle in body
        for needle in [
            f"Scope: `{scope}`",
            f"Agent family: `{agent_family}`",
            f"Agent instance id: `{agent_instance_id}`",
            f"Work lane: `{work_lane}`",
        ]
    )


def find_feedback_closure(project_root: Path, scope: str, agent_family: str, agent_instance_id: str, work_lane: str) -> str:
    feedback_root = project_root / "working/feedback"
    if not feedback_root.exists():
        return ""
    matches = sorted(
        (
            path for path in feedback_root.glob("*.md")
            if _feedback_match(path, scope, agent_family, agent_instance_id, work_lane)
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        return ""
    return rel(matches[0])


def require_feedback_closure(base: dict[str, str], project_root: Path) -> str:
    closure_ref = find_feedback_closure(
        project_root,
        base["scope"],
        base["agent_family"],
        base["agent_instance_id"],
        base["work_lane"],
    )
    if closure_ref:
        return closure_ref
    raise AicosMcpWriteError(
        "feedback_closure_required",
        "Session-close writes require one feedback closure first: record either a real issue or feedback_type=no_issue.",
        {
            "required_before": [
                "aicos_record_checkpoint(status=completed|blocked)",
                "aicos_write_task_update(task_status=completed|blocked|waiting)",
                "aicos_write_handoff_update(status=completed|blocked|ready_for_next)",
            ],
            "closure_rule": "Use aicos_record_feedback once per agent_instance_id + scope + work_lane before session-close writes.",
            "matching_keys": ["scope", "agent_family", "agent_instance_id", "work_lane"],
            "quick_no_issue_example": {
                "scope": base["scope"],
                "actor_role": base["actor_role"],
                "agent_family": base["agent_family"],
                "agent_instance_id": base["agent_instance_id"],
                "work_type": base["work_type"],
                "work_lane": base["work_lane"],
                "execution_context": base["execution_context"],
                "feedback_type": "no_issue",
                "severity": "low",
                "title": "No significant friction",
                "summary": "Bootstrap/read/write flow was clear enough for this pass.",
            },
        },
    )


def status_item_type_warnings(item_type: str, title: str, summary: str, reason: str) -> list[dict[str, str]]:
    text = " ".join([title, summary, reason]).lower()
    warnings: list[dict[str, str]] = []
    debt_markers = [
        "tech debt",
        "debt",
        "bug",
        "friction",
        "missing",
        "cleanup",
        "stale",
        "coverage",
        "validation",
        "deprecated",
        "lỗi",
        "thiếu",
        "chưa có",
        "chưa được",
    ]
    question_markers = ["?", "question", "open question", "câu hỏi", "chưa rõ", "cần quyết định"]
    decision_markers = ["decision", "decided", "adr", "đã quyết định", "follow-up", "followup"]
    if item_type == "open_item" and any(marker in text for marker in debt_markers):
        warnings.append(
            {
                "code": "item_type_may_be_tech_debt",
                "message": "This looks like an existing issue, missing coverage/docs, stale behavior, cleanup, or quality gap. Consider item_type=tech_debt.",
            }
        )
    if item_type != "open_question" and any(marker in text for marker in question_markers):
        warnings.append(
            {
                "code": "item_type_may_be_open_question",
                "message": "This looks like an unresolved question. Consider item_type=open_question if a decision is needed before action.",
            }
        )
    if item_type not in {"decision_followup", "open_question"} and any(marker in text for marker in decision_markers):
        warnings.append(
            {
                "code": "item_type_may_be_decision_followup",
                "message": "This references a decision or ADR. Consider item_type=decision_followup if the decision is already made and needs tracking.",
            }
        )
    return warnings


def upsert_markdown_section(path: Path, heading: str, body: str) -> None:
    existing = read_text(path).rstrip()
    marker = f"## {heading}"
    section = f"{marker}\n\n{body.strip()}\n"
    if not existing:
        write_text(path, section)
        return
    start = existing.find(marker)
    if start == -1:
        write_text(path, f"{existing}\n\n{section}")
        return
    next_start = existing.find("\n## ", start + len(marker))
    if next_start == -1:
        updated = f"{existing[:start].rstrip()}\n\n{section}"
    else:
        updated = f"{existing[:start].rstrip()}\n\n{section}\n{existing[next_start:].lstrip()}"
    write_text(path, updated)


def base_payload(payload: dict[str, Any]) -> dict[str, Any]:
    reject_raw_write_keys(payload)
    require_contract_ack(payload)
    scope = require_string(payload, "scope", max_len=120)
    validate_scope(scope)
    submitted_actor_role = require_string(payload, "actor_role", max_len=80)
    actor_role = normalize_actor_role(submitted_actor_role)
    agent_family = require_string(payload, "agent_family", max_len=120)
    agent_instance_id = require_string(payload, "agent_instance_id", max_len=160)
    work_type = enum_value(payload, "work_type", ALLOWED_WORK_TYPES)
    work_lane = require_string(payload, "work_lane", max_len=200)
    coordination_status = optional_string(payload, "coordination_status", max_len=80) or "active"
    if coordination_status not in ALLOWED_COORDINATION_STATUSES:
        raise AicosMcpWriteError(
            "invalid_enum",
            "coordination_status is not allowed.",
            {"field": "coordination_status", "allowed": sorted(ALLOWED_COORDINATION_STATUSES), "received": coordination_status},
        )
    worktree_path = optional_string(payload, "worktree_path", max_len=240)
    if work_type == "code" and not worktree_path:
        raise AicosMcpWriteError(
            "missing_required_field",
            "worktree_path is required for code work so parallel agents can avoid overlapping checkouts.",
            {"field": "worktree_path", "work_type": work_type},
        )
    return {
        "scope": scope,
        "actor_role": actor_role,
        "submitted_actor_role": submitted_actor_role,
        "agent_family": agent_family,
        "agent_instance_id": agent_instance_id,
        "agent_display_name": optional_string(payload, "agent_display_name", max_len=160) or "unknown",
        "work_type": work_type,
        "work_lane": work_lane,
        "coordination_status": coordination_status,
        "artifact_scope": optional_string(payload, "artifact_scope", max_len=500) or "unspecified",
        "work_branch": optional_string(payload, "work_branch", max_len=200) or "unknown",
        "worktree_path": worktree_path or "unknown",
        "execution_context": optional_string(payload, "execution_context", max_len=160) or "unknown",
        "actor_family": optional_string(payload, "actor_family", max_len=120) or agent_family,
        "logical_role": optional_string(payload, "logical_role", max_len=120) or actor_role,
        "work_context": optional_string(payload, "work_context", max_len=160),
    }


def record_checkpoint(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    checkpoint_type = enum_value(payload, "checkpoint_type", ALLOWED_CHECKPOINT_TYPES)
    status = enum_value(payload, "status", ALLOWED_CHECKPOINT_STATUSES)
    feedback_closure_ref = require_feedback_closure(base, project_root) if status in {"completed", "blocked"} else ""
    summary = require_string(payload, "summary", max_len=SUMMARY_MAX_LEN)
    notes = optional_string(payload, "notes", max_len=1000)
    timestamp = now_iso()
    write_id_value = write_id("aicos_record_checkpoint", payload, timestamp)
    target = project_root / "evidence/checkpoints" / f"{safe_slug(write_id_value)}.md"
    ref_lines = refs_block(payload)
    body = "\n".join(
        [
            f"# MCP Checkpoint: {write_id_value}",
            "",
            f"Status: {status}",
            f"Project: `{project_id}`",
            f"Scope: `{base['scope']}`",
            f"Write id: `{write_id_value}`",
            f"Written at: `{timestamp}`",
            f"Checkpoint type: `{checkpoint_type}`",
            "",
            "## Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "## Notes",
            "",
            notes or "none",
            "",
            "## Boundary",
            "",
            "Recorded through MCP semantic checkpoint write. This is evidence/continuity, not canonical promotion.",
        ]
    )
    write_text(target, body)
    meta = trace_metadata("aicos_record_checkpoint", {**payload, **base}, [target], timestamp, write_id_value)
    result = {
        "metadata": meta,
        "status": "success",
        "normalized_summary": summary,
        "checkpoint_type": checkpoint_type,
    }
    if feedback_closure_ref:
        result["feedback_closure"] = {"status": "recorded", "ref": feedback_closure_ref}
    if status in {"completed", "blocked"}:
        result["feedback_nudge"] = feedback_nudge("session_close", "Checkpoint reached a boundary where capturing friction is low-cost.")
    return result


def write_task_update(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    task_ref = require_string(payload, "task_ref", max_len=200)
    task_status = enum_value(payload, "task_status", ALLOWED_TASK_STATUSES)
    feedback_closure_ref = require_feedback_closure(base, project_root) if task_status in {"completed", "blocked", "waiting"} else ""
    what_is_done = require_string(payload, "what_is_done", max_len=700)
    what_is_blocked = optional_string(payload, "what_is_blocked", max_len=700)
    next_step = optional_string(payload, "next_step", max_len=700)
    if task_status in {"blocked", "waiting"} and not (what_is_blocked or next_step):
        raise AicosMcpWriteError("missing_continuity_field", "blocked/waiting task updates require what_is_blocked or next_step.", {"task_status": task_status})
    if task_status in {"completed", "partial", "in_progress"} and not what_is_done:
        raise AicosMcpWriteError("missing_continuity_field", "task updates require what_is_done.", {"task_status": task_status})
    timestamp = now_iso()
    write_id_value = write_id("aicos_write_task_update", payload, timestamp)
    target = project_root / "working/task-state" / f"{safe_slug(task_ref, fallback='task')}.md"
    ref_lines = refs_block(payload)
    body = "\n".join(
        [
            f"# MCP Task State: {task_ref}",
            "",
            f"Status: {task_status}",
            f"Project: `{project_id}`",
            f"Scope: `{base['scope']}`",
            f"Task ref: `{task_ref}`",
            f"Last write id: `{write_id_value}`",
            f"Last updated at: `{timestamp}`",
            "",
            "## Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "## What Is Done",
            "",
            what_is_done,
            "",
            "## What Is Blocked",
            "",
            what_is_blocked or "none",
            "",
            "## Next Step",
            "",
            next_step or "none",
            "",
            "## Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "## Boundary",
            "",
            "Recorded through MCP semantic task update. This file is project working continuity, not raw task history.",
        ]
    )
    write_text(target, body)
    meta = trace_metadata("aicos_write_task_update", {**payload, **base, "task_ref": task_ref}, [target], timestamp, write_id_value)
    result = {"metadata": meta, "status": "success", "normalized_task_state": {"task_ref": task_ref, "task_status": task_status, "next_step": next_step}}
    if feedback_closure_ref:
        result["feedback_closure"] = {"status": "recorded", "ref": feedback_closure_ref}
    if task_status in {"completed", "blocked", "waiting"}:
        result["feedback_nudge"] = feedback_nudge("session_close", "Task update reached a boundary where feedback is cheap to capture.")
    return result


def write_handoff_update(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    summary = require_string(payload, "summary", max_len=HANDOFF_SUMMARY_MAX_LEN)
    status = enum_value(payload, "status", ALLOWED_HANDOFF_STATUSES)
    feedback_closure_ref = require_feedback_closure(base, project_root) if status in {"completed", "blocked", "ready_for_next"} else ""
    next_step = require_string(payload, "next_step", max_len=700)
    notes = optional_string(payload, "notes", max_len=1000)
    timestamp = now_iso()
    write_id_value = write_id("aicos_write_handoff_update", payload, timestamp)
    target = project_root / "working/handoff/current.md"
    ref_lines = refs_block(payload)
    section_body = "\n".join(
        [
            f"Status: `{status}`",
            f"Write id: `{write_id_value}`",
            f"Written at: `{timestamp}`",
            "",
            "### Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "### Summary",
            "",
            summary,
            "",
            "### Next Step",
            "",
            next_step,
            "",
            "### Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "### Notes",
            "",
            notes or "none",
            "",
            "Boundary: MCP semantic handoff update; compact current continuity only.",
        ]
    )
    upsert_markdown_section(target, f"MCP Continuity Update: {write_id_value}", section_body)
    meta = trace_metadata("aicos_write_handoff_update", {**payload, **base}, [target], timestamp, write_id_value)
    result = {
        "metadata": meta,
        "status": "success",
        "normalized_handoff_update": {"summary": summary, "next_step": next_step},
        "boundary": (
            "Handoff updates are compact current continuity only. Use "
            "aicos_update_status_item for open items, open questions, tech debt, "
            "decision follow-ups, or backlog-like status changes."
        ),
    }
    if feedback_closure_ref:
        result["feedback_closure"] = {"status": "recorded", "ref": feedback_closure_ref}
    if status in {"completed", "blocked", "ready_for_next"}:
        result["feedback_nudge"] = feedback_nudge("session_close", "A handoff boundary is a good moment to record friction or tool gaps.")
    return result


def update_status_item(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    item_id = require_string(payload, "item_id", max_len=160)
    item_type = enum_value(payload, "item_type", ALLOWED_STATUS_ITEM_TYPES)
    item_status = enum_value(payload, "item_status", ALLOWED_STATUS_ITEM_STATUSES)
    title = require_string(payload, "title", max_len=240)
    summary = require_string(payload, "summary", max_len=SUMMARY_MAX_LEN)
    reason = optional_string(payload, "reason", max_len=700)
    next_step = optional_string(payload, "next_step", max_len=700)
    source_ref = optional_string(payload, "source_ref", max_len=240)
    warnings = status_item_type_warnings(item_type, title, summary, reason)
    timestamp = now_iso()
    write_id_value = write_id("aicos_update_status_item", {**payload, "task_ref": item_id}, timestamp)
    target = project_root / "working/status-items" / f"{safe_slug(item_id, fallback='status-item')}.md"
    ref_lines = refs_block(payload)
    if source_ref:
        ref_lines.append(f"- source_ref: `{source_ref}`")
    body = "\n".join(
        [
            f"# Status Item: {item_id}",
            "",
            f"Status: {item_status}",
            f"Item type: `{item_type}`",
            f"Type guidance: {STATUS_ITEM_TYPE_GUIDANCE[item_type]}",
            f"Project: `{project_id}`",
            f"Scope: `{base['scope']}`",
            f"Item id: `{item_id}`",
            f"Title: {title}",
            f"Last write id: `{write_id_value}`",
            f"Last updated at: `{timestamp}`",
            "",
            "## Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Item Type Guidance",
            "",
            STATUS_ITEM_TYPE_GUIDANCE[item_type],
            "",
            "## Reason",
            "",
            reason or "none",
            "",
            "## Next Step",
            "",
            next_step or "none",
            "",
            "## Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "## Boundary",
            "",
            "Recorded through MCP semantic status-item update. This file tracks project working status for open items, open questions, tech debt, or decision follow-ups; it is not a raw handoff edit.",
        ]
    )
    write_text(target, body)
    meta = trace_metadata("aicos_update_status_item", {**payload, **base, "task_ref": item_id}, [target], timestamp, write_id_value)
    result = {
        "metadata": meta,
        "status": "success",
        "normalized_status_item": {
            "item_id": item_id,
            "item_type": item_type,
            "item_status": item_status,
            "type_guidance": STATUS_ITEM_TYPE_GUIDANCE[item_type],
            "title": title,
            "next_step": next_step,
        },
        "warnings": warnings,
        "item_type_guidance": STATUS_ITEM_TYPE_GUIDANCE,
    }
    if item_status in {"resolved", "blocked", "deferred"}:
        result["feedback_nudge"] = feedback_nudge("session_close", "This status change may reveal process or tool friction worth capturing.")
    return result


def register_artifact_ref(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    artifact_kind = enum_value(payload, "artifact_kind", ALLOWED_ARTIFACT_KINDS)
    title = require_string(payload, "title", max_len=240)
    artifact_ref = require_string(payload, "artifact_ref", max_len=300)
    summary = require_string(payload, "summary", max_len=SUMMARY_MAX_LEN)
    source_ref = optional_string(payload, "source_ref", max_len=240)
    timestamp = now_iso()
    write_id_value = write_id("aicos_register_artifact_ref", {**payload, "task_ref": title}, timestamp)
    target = project_root / "working/artifact-refs" / f"{safe_slug(write_id_value)}.md"
    ref_lines = refs_block(payload)
    if source_ref:
        ref_lines.append(f"- source_ref: `{source_ref}`")
    body = "\n".join(
        [
            f"# Artifact Ref: {title}",
            "",
            "Status: registered",
            f"Artifact kind: `{artifact_kind}`",
            f"Project: `{project_id}`",
            f"Scope: `{base['scope']}`",
            f"Artifact ref: `{artifact_ref}`",
            f"Write id: `{write_id_value}`",
            f"Written at: `{timestamp}`",
            "",
            "## Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "## Boundary",
            "",
            "Registered through MCP semantic artifact-ref write. The artifact body remains in its natural home; AICOS stores only a compact reference and relevance summary.",
        ]
    )
    write_text(target, body)
    meta = trace_metadata("aicos_register_artifact_ref", {**payload, **base}, [target], timestamp, write_id_value)
    result = {
        "metadata": meta,
        "status": "success",
        "normalized_artifact_ref": {
            "artifact_kind": artifact_kind,
            "title": title,
            "artifact_ref": artifact_ref,
            "summary": summary,
            "path": rel(target),
        },
    }
    result["feedback_nudge"] = feedback_nudge("session_close", "If artifact registration felt awkward, record a feedback item while context is fresh.")
    return result


def record_feedback(payload: dict[str, Any]) -> dict[str, Any]:
    base = base_payload(payload)
    project_id, project_root = validate_scope(base["scope"])
    feedback_type = enum_value(payload, "feedback_type", ALLOWED_FEEDBACK_TYPES)
    severity = enum_value(payload, "severity", ALLOWED_FEEDBACK_SEVERITIES)
    title = require_string(payload, "title", max_len=240)
    summary = require_string(payload, "summary", max_len=SUMMARY_MAX_LEN)
    recommendation = optional_string(payload, "recommendation", max_len=700)
    observed_in = optional_string(payload, "observed_in", max_len=240)
    source_ref = optional_string(payload, "source_ref", max_len=240)
    timestamp = now_iso()
    write_id_value = write_id("aicos_record_feedback", {**payload, "task_ref": title}, timestamp)
    target = project_root / "working/feedback" / f"{safe_slug(write_id_value)}.md"
    ref_lines = refs_block(payload)
    if source_ref:
        ref_lines.append(f"- source_ref: `{source_ref}`")
    body = "\n".join(
        [
            f"# Feedback: {title}",
            "",
            "Status: open",
            f"Feedback type: `{feedback_type}`",
            f"Severity: `{severity}`",
            f"Project: `{project_id}`",
            f"Scope: `{base['scope']}`",
            f"Write id: `{write_id_value}`",
            f"Written at: `{timestamp}`",
            f"Last updated at: `{timestamp}`",
            "",
            "## Actor Identity",
            "",
            *actor_identity_block(base),
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Observed In",
            "",
            observed_in or "unspecified",
            "",
            "## Recommendation",
            "",
            recommendation or "none",
            "",
            "## Trace Refs",
            "",
            *markdown_list(ref_lines),
            "",
            "## Boundary",
            "",
            "Recorded through MCP semantic feedback write. This is a service-improvement signal, not canonical truth or task continuity.",
        ]
    )
    write_text(target, body)
    meta = trace_metadata("aicos_record_feedback", {**payload, **base}, [target], timestamp, write_id_value)
    result = {
        "metadata": meta,
        "status": "success",
        "normalized_feedback": {
            "feedback_type": feedback_type,
            "severity": severity,
            "title": title,
            "path": rel(target),
        },
    }
    return result


def dispatch_write_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    scope = arguments.get("scope", "")
    if isinstance(scope, str) and scope:
        with scope_write_lock(scope):
            return _dispatch_write_tool_unlocked(name, arguments)
    return _dispatch_write_tool_unlocked(name, arguments)


def _dispatch_write_tool_unlocked(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "aicos_record_checkpoint":
        return record_checkpoint(arguments)
    if name == "aicos_write_task_update":
        return write_task_update(arguments)
    if name == "aicos_write_handoff_update":
        return write_handoff_update(arguments)
    if name == "aicos_update_status_item":
        return update_status_item(arguments)
    if name == "aicos_register_artifact_ref":
        return register_artifact_ref(arguments)
    if name == "aicos_record_feedback":
        return record_feedback(arguments)
    raise AicosMcpWriteError("unknown_write_tool", "Unknown Phase 2 MCP write tool.", {"tool": name})
