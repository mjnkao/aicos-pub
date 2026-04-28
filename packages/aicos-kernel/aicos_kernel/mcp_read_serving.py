from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .context_registry import registry_payload
from .mcp_contract_status import contract_status_payload


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_HIDDEN_STATUSES = {"closed", "stale"}
FEEDBACK_LOOP_PROMPTS = [
    "Bạn có gặp khó khăn gì khi đọc hoặc ghi AICOS không?",
    "Có tool nào còn thiếu hoặc shape của tool nào đang gây chậm/nhầm không?",
    "Nếu chỉ sửa một thứ để tiết kiệm thời gian nhất, đó là gì?",
]


class AicosMcpReadError(ValueError):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


@dataclass(frozen=True)
class SourceRef:
    path: Path
    role: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def optional_read_string(arguments: dict[str, Any], field: str, default: str = "", max_len: int = 500) -> str:
    value = arguments.get(field, default)
    if value is None:
        return default
    if not isinstance(value, str):
        raise AicosMcpReadError("invalid_argument_type", f"{field} must be a string.", {"field": field})
    stripped = value.strip()
    if len(stripped) > max_len:
        raise AicosMcpReadError("argument_too_long", f"{field} is too long.", {"field": field, "max_len": max_len})
    return stripped


def optional_read_list(arguments: dict[str, Any], field: str, allowed: set[str] | None = None, max_items: int = 12) -> list[str]:
    value = arguments.get(field, [])
    if value in ("", None):
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise AicosMcpReadError("invalid_argument_type", f"{field} must be a list of strings.", {"field": field})
    items = [item.strip() for item in value]
    if len(items) > max_items:
        raise AicosMcpReadError("too_many_items", f"{field} has too many items.", {"field": field, "max_items": max_items})
    if allowed:
        invalid = sorted(set(items) - allowed)
        if invalid:
            raise AicosMcpReadError("invalid_filter", f"{field} contains unsupported values.", {"field": field, "invalid": invalid, "allowed": sorted(allowed)})
    return items


def markdown_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def compact_text(body: str, limit: int = 360) -> str:
    text = re.sub(r"\s+", " ", body).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def markdown_section(body: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = body.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index + 1
            break
    if start is None:
        return ""
    selected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        selected.append(line)
    return "\n".join(selected).strip()


def markdown_section_any_level(body: str, heading: str) -> str:
    pattern = re.compile(rf"^(?P<level>#+)\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    level_len = len(match.group("level"))
    start = match.end()
    next_heading = re.search(rf"^#{{1,{level_len}}}\s+", body[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    return body[start:end].strip()


def first_paragraph(section: str) -> str:
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        prefix = stripped.split(" ", 1)[0]
        if stripped.startswith("- ") or (prefix.endswith(".") and prefix[:-1].isdigit()):
            break
        lines.append(stripped)
    return " ".join(lines)


def summarize_bullets(section: str, limit: int = 5) -> list[str]:
    bullets: list[str] = []
    current: str | None = None
    for line in section.splitlines():
        stripped = line.strip()
        prefix = stripped.split(" ", 1)[0]
        if stripped.startswith("- ") or (prefix.endswith(".") and prefix[:-1].isdigit()):
            if current is not None:
                bullets.append(current)
                if len(bullets) >= limit:
                    break
            current = stripped
            continue
        if current and stripped and not stripped.startswith("#"):
            current = f"{current} {stripped}"
    if current is not None and len(bullets) < limit:
        bullets.append(current)
    return bullets


def normalize_actor(actor: str) -> str:
    normalized = actor.strip().lower().replace("_", "-")
    aliases = {
        "": "a1-work",
        "a1": "a1-work",
        "a1-work": "a1-work",
        "a1-work-agent": "a1-work",
        "a1-work-agents": "a1-work",
        "external": "a1-work",
        "external-agent": "a1-work",
        "external-agents": "a1-work",
        "a2-core": "a2-core",
        "a2": "a2-core",
        "a2-core-c": "a2-core",
        "a2-core-r": "a2-core",
    }
    # External agents often send their client name here (Antigravity, Claude,
    # Codex, OpenClaw). For AICOS read-serving, any non-explicit A2 actor is an
    # A1 external work actor; client identity belongs in agent_family.
    return aliases.get(normalized, "a1-work")


def service_actor_label(actor: str) -> str:
    return "A2-Core" if normalize_actor(actor) == "a2-core" else "A1"


def validate_scope(scope: str) -> str:
    if not scope.startswith("projects/") or scope.count("/") != 1:
        raise AicosMcpReadError(
            "unsupported_scope",
            "Phase 1 read-serving supports project scopes only.",
            {"scope": scope, "supported_shape": "projects/<project-id>"},
        )
    return scope.split("/", 1)[1]


def actor_paths(actor: str, scope: str) -> dict[str, Any]:
    actor_key = normalize_actor(actor)
    project_id = validate_scope(scope)
    project_root = REPO_ROOT / "brain/projects" / project_id
    if actor_key == "a2-core":
        if scope != "projects/aicos":
            raise AicosMcpReadError(
                "unsupported_actor_scope",
                "A2-Core Phase 1 startup is currently scoped to projects/aicos.",
                {"actor": actor, "scope": scope},
            )
        packet_root = REPO_ROOT / "agent-repo/classes/a2-service-agents/task-packets"
        return {
            "actor_key": actor_key,
            "actor_lane": "A2-Core",
            "project_id": project_id,
            "project_root": project_root,
            "startup_card": REPO_ROOT / "agent-repo/classes/a2-service-agents/startup-cards/a2-core.md",
            "actor_ladder": REPO_ROOT / "agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md",
            "project_ladder": project_root / "working/context-ladder.md",
            "packet_index": packet_root / "README.md",
            "packet_root": packet_root,
            "role_or_profile": project_root / "canonical/role-definitions.md",
            "working_rules": project_root / "canonical/project-working-rules.md",
            "rule_cards": [
                "agent-repo/classes/a2-service-agents/rule-cards/writeback.md",
                "agent-repo/classes/a2-service-agents/rule-cards/idea-capture.md",
                "agent-repo/classes/a2-service-agents/rule-cards/option-choose.md",
                "agent-repo/classes/a2-service-agents/rule-cards/sync-brain.md",
                "agent-repo/classes/a2-service-agents/rule-cards/handoff.md",
            ],
        }
    if actor_key == "a1-work":
        scoped_packet_root = REPO_ROOT / "agent-repo/classes/a1-work-agents/task-packets" / project_id
        packet_root = scoped_packet_root if scoped_packet_root.exists() else REPO_ROOT / "agent-repo/classes/a1-work-agents/task-packets"
        return {
            "actor_key": actor_key,
            "actor_lane": "A1",
            "project_id": project_id,
            "project_root": project_root,
            "startup_card": REPO_ROOT / "agent-repo/classes/a1-work-agents/startup-cards/a1.md",
            "actor_ladder": REPO_ROOT / "agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md",
            "project_ladder": project_root / "working/context-ladder.md",
            "packet_index": packet_root / "README.md",
            "packet_root": packet_root,
            "role_or_profile": project_root / "canonical/project-profile.md",
            "working_rules": REPO_ROOT / "brain/shared/policies/checkpoint-writeback-policy.md",
            "rule_cards": [
                "agent-repo/classes/a1-work-agents/rule-cards/writeback-checkpoint.md",
                "agent-repo/classes/a1-work-agents/rule-cards/handoff-continuation.md",
                "agent-repo/classes/a1-work-agents/rule-cards/task-packet-loading.md",
                "agent-repo/classes/a1-work-agents/rule-cards/project-state-routing.md",
                "agent-repo/classes/a1-work-agents/rule-cards/layered-rules.md",
                "agent-repo/classes/a1-work-agents/rule-cards/escalation-to-a2.md",
            ],
        }
    raise AicosMcpReadError(
        "unsupported_actor",
        "Phase 1 read-serving supports A1 and A2-Core actors.",
        {"actor": actor, "normalized_actor": actor_key},
    )


def file_ref(path: Path, role: str) -> dict[str, Any]:
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        "path": rel(path),
        "role": role,
        "exists": exists,
        "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat() if stat else None,
    }


def metadata(surface: str, actor: str, scope: str, sources: list[SourceRef]) -> dict[str, Any]:
    served_at = now_iso()
    source_refs = [file_ref(item.path, item.role) for item in sources]
    seed = "|".join([surface, actor, scope, served_at, *[item["path"] for item in source_refs]])
    return {
        "schema_version": "0.1",
        "kind": "aicos.mcp.read_bundle",
        "surface": surface,
        "bundle_id": f"{surface}:{hashlib.sha1(seed.encode('utf-8')).hexdigest()[:12]}",
        "served_at": served_at,
        "actor": actor,
        "scope": scope,
        "source_refs": source_refs,
        "authority": "AICOS brain/agent-repo source files; MCP is access/control-plane, not truth store.",
        "staleness_hint": "Refresh before continuation-sensitive work or before using a copied local context.",
    }


def audit_log_path() -> Path:
    return Path(os.environ.get("AICOS_DAEMON_AUDIT_LOG", str(Path.home() / "Library/Logs/aicos/mcp-audit.jsonl"))).expanduser()


def recent_audit_events(scope: str, arguments: dict[str, Any], limit: int = 120) -> list[dict[str, Any]]:
    path = audit_log_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    agent_family = optional_read_string(arguments, "agent_family", max_len=120)
    agent_instance_id = optional_read_string(arguments, "agent_instance_id", max_len=160)
    events: list[dict[str, Any]] = []
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if scope and event.get("scope") not in {None, "", scope} and event.get("path") != "/health":
            continue
        if agent_family and event.get("agent_family") not in {None, "", agent_family}:
            continue
        if agent_instance_id and event.get("agent_instance_id") not in {None, "", agent_instance_id}:
            continue
        events.append(event)
        if len(events) >= limit:
            break
    events.reverse()
    return events


def feedback_loop_payload(scope: str, arguments: dict[str, Any], feedback_items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    work_type = optional_read_string(arguments, "work_type", max_len=80)
    work_lane = optional_read_string(arguments, "work_lane", max_len=160)
    events = recent_audit_events(scope, arguments, limit=120)
    friction_statuses = {"tool_error", "rpc_error", "unauthorized"}
    friction_events = [event for event in events if str(event.get("status")) in friction_statuses]
    repeated_errors: dict[str, int] = {}
    for event in friction_events:
        key = str(event.get("error") or event.get("status") or "unknown")
        repeated_errors[key] = repeated_errors.get(key, 0) + 1
    trigger = "none"
    ask_now = False
    reason = "No immediate feedback nudge."
    if work_type == "orientation" or work_lane == "intake":
        trigger = "first_contact"
        ask_now = True
        reason = "First-contact/bootstrap read; this is the best time to capture onboarding friction."
    elif any(count >= 2 for count in repeated_errors.values()):
        trigger = "repeated_friction"
        ask_now = True
        reason = "Recent repeated MCP friction detected for this agent/scope."
    elif feedback_items is not None and not feedback_items:
        trigger = "low_signal"
        ask_now = True
        reason = "No feedback has been recorded for this scope yet."
    top_errors = sorted(repeated_errors.items(), key=lambda item: (-item[1], item[0]))[:3]
    return {
        "ask_now": ask_now,
        "trigger": trigger,
        "reason": reason,
        "prompt": FEEDBACK_LOOP_PROMPTS,
        "preferred_action": "aicos_record_feedback",
        "template_hint": "./aicos mcp template feedback --scope " + scope,
        "recent_friction": [{"error": error, "count": count} for error, count in top_errors],
    }


def packet_summary(path: Path) -> str:
    body = read_text(path)
    for field in ["summary", "objective"]:
        prefix = f"{field}:"
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith(prefix):
                return stripped[len(prefix):].strip().strip('"')
    return markdown_title(body, path.stem)


def collect_packets(packet_root: Path) -> list[Path]:
    if not packet_root.exists():
        return []
    return sorted(path for path in packet_root.glob("*.md") if path.name != "README.md")


def markdown_field(body: str, field: str) -> str:
    prefix = f"{field}:"
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip().strip("`").strip()
    return ""


def markdown_heading_field(body: str, field: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}:\s*`?([^`\n]+)`?\s*$", re.MULTILINE)
    match = pattern.search(body)
    return match.group(1).strip() if match else ""


def project_root_for_scope(scope: str) -> tuple[str, Path]:
    project_id = validate_scope(scope)
    project_root = REPO_ROOT / "brain/projects" / project_id
    if not project_root.exists():
        raise AicosMcpReadError("missing_project_scope", "Project scope does not exist.", {"scope": scope, "path": rel(project_root)})
    return project_id, project_root


def collect_task_state(project_root: Path) -> dict[str, list[dict[str, Any]]]:
    task_state_root = project_root / "working/task-state"
    if not task_state_root.exists():
        return {"active": [], "recent_completed": []}
    states: list[dict[str, Any]] = []
    for path in sorted(task_state_root.glob("*.md")):
        body = read_text(path)
        status = markdown_field(body, "Status")
        states.append(
            {
                "task_ref": markdown_field(body, "Task ref") or path.stem,
                "status": status,
                "path": rel(path),
                "last_updated_at": markdown_field(body, "Last updated at"),
                "actor_role": markdown_field(body, "Actor role"),
                "agent_family": markdown_field(body, "Agent family"),
                "agent_instance_id": markdown_field(body, "Agent instance id"),
                "agent_display_name": markdown_field(body, "Agent display name"),
                "work_type": markdown_field(body, "Work type"),
                "work_lane": markdown_field(body, "Work lane"),
                "coordination_status": markdown_field(body, "Coordination status"),
                "artifact_scope": markdown_field(body, "Artifact scope"),
                "work_branch": markdown_field(body, "Work branch"),
                "worktree_path": markdown_field(body, "Worktree path"),
                "execution_context": markdown_field(body, "Execution context"),
                "work_context": markdown_field(body, "Work context"),
            }
        )
    active_statuses = {"planned", "in_progress", "blocked", "waiting"}
    active = [item for item in states if item["status"] in active_statuses]
    completed = [item for item in states if item["status"] not in active_statuses]
    completed.sort(key=lambda item: item.get("last_updated_at", ""), reverse=True)
    return {"active": active, "recent_completed": completed[:5]}


def collect_status_items(project_root: Path) -> dict[str, list[dict[str, Any]]]:
    status_root = project_root / "working/status-items"
    if not status_root.exists():
        return {"active": [], "recent": []}
    items: list[dict[str, Any]] = []
    for path in sorted(status_root.glob("*.md")):
        body = read_text(path)
        items.append(
            {
                "item_id": markdown_field(body, "Item id") or path.stem,
                "item_type": markdown_field(body, "Item type"),
                "status": markdown_field(body, "Status"),
                "title": markdown_field(body, "Title"),
                "path": rel(path),
                "last_updated_at": markdown_field(body, "Last updated at"),
                "actor_role": markdown_field(body, "Actor role"),
                "agent_family": markdown_field(body, "Agent family"),
                "agent_instance_id": markdown_field(body, "Agent instance id"),
                "work_type": markdown_field(body, "Work type"),
                "work_lane": markdown_field(body, "Work lane"),
            }
        )
    active_statuses = {"open", "blocked", "deferred"}
    active = [item for item in items if item["status"] in active_statuses]
    recent = [item for item in items if item["status"] not in active_statuses]
    active.sort(key=lambda item: item.get("last_updated_at", ""), reverse=True)
    recent.sort(key=lambda item: item.get("last_updated_at", ""), reverse=True)
    return {"active": active[:10], "recent": recent[:5]}


def all_status_items(project_root: Path) -> list[dict[str, Any]]:
    status_root = project_root / "working/status-items"
    if not status_root.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(status_root.glob("*.md")):
        body = read_text(path)
        items.append(
            {
                "item_id": markdown_field(body, "Item id") or path.stem,
                "item_type": markdown_field(body, "Item type"),
                "status": markdown_field(body, "Status"),
                "title": markdown_field(body, "Title"),
                "path": rel(path),
                "last_updated_at": markdown_field(body, "Last updated at"),
                "actor_role": markdown_field(body, "Actor role"),
                "agent_family": markdown_field(body, "Agent family"),
                "agent_instance_id": markdown_field(body, "Agent instance id"),
                "work_type": markdown_field(body, "Work type"),
                "work_lane": markdown_field(body, "Work lane"),
                "summary": compact_text(markdown_section(body, "Summary")),
                "reason": compact_text(markdown_section(body, "Reason")),
                "next_step": compact_text(markdown_section(body, "Next Step")),
            }
        )
    items.sort(key=lambda item: item.get("last_updated_at", ""), reverse=True)
    return items


def status_items_payload(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    _project_id, project_root = project_root_for_scope(scope)
    items = all_status_items(project_root)
    status_filter = set(optional_read_list(arguments, "status_filter", max_items=8))
    item_type_filter = set(optional_read_list(arguments, "item_type_filter", max_items=8))
    status_work_lane_filter = optional_read_string(arguments, "status_work_lane_filter", max_len=200)
    status_agent_family_filter = optional_read_string(arguments, "status_agent_family_filter", max_len=120)
    include_stale = bool(arguments.get("include_stale", False))
    max_results_raw = arguments.get("max_results", 20)
    if not isinstance(max_results_raw, int):
        raise AicosMcpReadError("invalid_argument_type", "max_results must be an integer.", {"field": "max_results"})
    max_results = max(1, min(max_results_raw, 50))
    filtered = [
        item
        for item in items
        if (status_filter or include_stale or item["status"] not in DEFAULT_HIDDEN_STATUSES)
        and (not status_filter or item["status"] in status_filter)
        and (not item_type_filter or item["item_type"] in item_type_filter)
        and (not status_work_lane_filter or item["work_lane"] == status_work_lane_filter)
        and (not status_agent_family_filter or item["agent_family"] == status_agent_family_filter)
    ]
    source = project_root / "working/status-items"
    return {
        "metadata": metadata("aicos_get_status_items", actor, scope, [SourceRef(source, "status_items")]),
        "items": filtered[:max_results],
        "filters": {
            "status_filter": sorted(status_filter),
            "item_type_filter": sorted(item_type_filter),
            "status_work_lane_filter": status_work_lane_filter,
            "status_agent_family_filter": status_agent_family_filter,
            "max_results": max_results,
            "include_stale": include_stale,
            "default_hidden_statuses": [] if status_filter or include_stale else sorted(DEFAULT_HIDDEN_STATUSES),
            "identity_fields_not_filters": ["work_lane", "agent_family"],
        },
        "boundary": "Structured status item index only; full evidence remains in referenced files.",
    }


def parse_workstream_doc(path: Path) -> dict[str, Any]:
    body = read_text(path)
    workstream_id = markdown_field(body, "Workstream id") or markdown_field(body, "workstream_id") or path.stem
    return {
        "workstream_id": workstream_id,
        "title": markdown_field(body, "Title") or markdown_title(body, workstream_id),
        "purpose": markdown_field(body, "Purpose") or compact_text(first_paragraph(markdown_section(body, "Purpose")) or markdown_section(body, "Purpose")),
        "when_to_use": markdown_field(body, "When to use") or compact_text(markdown_section(body, "When To Use")),
        "when_not_to_use": markdown_field(body, "When not to use") or compact_text(markdown_section(body, "When Not To Use")),
        "main_entry_surfaces": summarize_bullets(markdown_section(body, "Main Entry Surfaces"), limit=6),
        "typical_packets": summarize_bullets(markdown_section(body, "Typical Packets"), limit=6),
        "typical_outputs": summarize_bullets(markdown_section(body, "Typical Outputs"), limit=6),
        "default_writeback_lanes": summarize_bullets(markdown_section(body, "Default Writeback Lanes"), limit=6),
        "status": markdown_field(body, "Status") or "active",
        "path": rel(path),
    }


def workstream_index_payload(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    _project_id, project_root = project_root_for_scope(scope)
    include_candidate = bool(arguments.get("include_candidate", False))
    status_filter = set(optional_read_list(arguments, "status_filter", {"active", "paused", "deprecated", "candidate"}, max_items=8))
    workstream_root = project_root / "working/workstreams"
    candidate_paths: list[Path] = []
    if workstream_root.exists():
        candidate_paths.extend(sorted(path for path in workstream_root.glob("*.md") if path.name != "README.md"))
    workstreams = [parse_workstream_doc(path) for path in candidate_paths]
    if not include_candidate:
        workstreams = [item for item in workstreams if item["status"] != "candidate"]
    if status_filter:
        workstreams = [item for item in workstreams if item["status"] in status_filter]
    return {
        "metadata": metadata("aicos_get_workstream_index", actor, scope, [SourceRef(workstream_root, "workstream_index_source")]),
        "workstreams": workstreams[:30],
        "source_exists": workstream_root.exists(),
        "setup_hint": "" if workstream_root.exists() else "No project-declared workstream index exists yet. Do not infer active workstreams from handoff; create/accept a project workstream map first.",
        "boundary": "Serves project-declared or project-accepted workstream structure only; does not create or promote workstreams.",
    }


def context_registry_read_payload(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    _project_id, project_root = project_root_for_scope(scope)
    project_role = optional_read_string(arguments, "project_role", max_len=80)
    max_results_raw = arguments.get("max_results", 200)
    if not isinstance(max_results_raw, int):
        raise AicosMcpReadError("invalid_argument_type", "max_results must be an integer.", {"field": "max_results"})
    max_results = max(1, min(max_results_raw, 500))
    payload = registry_payload(scope=scope, limit=max_results, project_role=project_role)
    return {
        "metadata": metadata(
            "aicos_get_context_registry",
            actor,
            scope,
            [
                SourceRef(project_root, "project_context_registry_source"),
                SourceRef(REPO_ROOT / "brain/shared/policies", "shared_policy_registry_source"),
                SourceRef(REPO_ROOT / "packages/aicos-kernel/contracts", "contract_registry_source"),
            ],
        ),
        **payload,
    }


def project_registry_payload(actor: str, scope: str, _arguments: dict[str, Any]) -> dict[str, Any]:
    validate_scope(scope)
    registry = REPO_ROOT / "brain/shared/project-registry.md"
    body = read_text(registry)
    projects: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in body.splitlines():
        if line.startswith("### "):
            if current:
                projects.append(current)
            current = {"heading": line[4:].strip()}
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip().lower().replace(" ", "_")
        stripped = value.strip().strip("`")
        if normalized_key in {"project_id", "status", "project_type", "aicos_scope", "context_authority", "runtime_authority", "cross-project_exposure"}:
            current[normalized_key] = stripped
    if current:
        projects.append(current)
    return {
        "metadata": metadata("aicos_get_project_registry", actor, scope, [SourceRef(registry, "project_registry")]),
        "path": rel(registry),
        "projects": projects,
        "content": body,
        "boundary": "Shared project discovery only. Project current truth remains under brain/projects/<project-id>/.",
    }


def feedback_digest_payload(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    _project_id, project_root = project_root_for_scope(scope)
    feedback_root = project_root / "working/feedback"
    max_results_raw = arguments.get("max_results", 10)
    if not isinstance(max_results_raw, int):
        raise AicosMcpReadError("invalid_argument_type", "max_results must be an integer.", {"field": "max_results"})
    max_results = max(1, min(max_results_raw, 50))
    items: list[dict[str, str]] = []
    feedback_type_counts: dict[str, int] = {}
    severity_counts: dict[str, int] = {}
    if feedback_root.exists():
        for path in sorted(feedback_root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
            body = read_text(path)
            feedback_type = markdown_field(body, "Feedback type")
            severity = markdown_field(body, "Severity")
            if feedback_type:
                feedback_type_counts[feedback_type] = feedback_type_counts.get(feedback_type, 0) + 1
            if severity:
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            items.append(
                {
                    "path": rel(path),
                    "title": markdown_title(body, path.stem),
                    "feedback_type": feedback_type,
                    "severity": severity,
                    "status": markdown_field(body, "Status"),
                    "summary": compact_text(markdown_section(body, "Summary"), limit=320),
                    "recommendation": compact_text(markdown_section(body, "Recommendation"), limit=320),
                    "last_updated_at": markdown_field(body, "Last updated at") or markdown_field(body, "Written at"),
                }
            )
    return {
        "metadata": metadata("aicos_get_feedback_digest", actor, scope, [SourceRef(feedback_root, "feedback_digest_source")]),
        "items": items[:max_results],
        "summary": {
            "total_feedback_count": len(items),
            "feedback_type_counts": sorted(feedback_type_counts.items(), key=lambda item: (-item[1], item[0])),
            "severity_counts": sorted(severity_counts.items(), key=lambda item: (-item[1], item[0])),
        },
        "feedback_loop": feedback_loop_payload(scope, arguments, items),
        "boundary": "Feedback digest is service-improvement signal, not project truth promotion.",
    }


def project_health_payload(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    _project_id, project_root = project_root_for_scope(scope)
    status_items = all_status_items(project_root)
    active_status = [item for item in status_items if item["status"] in {"open", "blocked", "deferred"}]
    blocked_status = [item for item in active_status if item["status"] == "blocked"]
    task_state = collect_task_state(project_root)
    feedback = feedback_digest_payload(actor, scope, {"max_results": 5})
    return {
        "metadata": metadata(
            "aicos_get_project_health",
            actor,
            scope,
            [
                SourceRef(project_root / "working/status-items", "status_items"),
                SourceRef(project_root / "working/task-state", "task_state"),
                SourceRef(project_root / "working/feedback", "feedback"),
            ],
        ),
        "summary": {
            "active_status_item_count": len(active_status),
            "blocked_status_item_count": len(blocked_status),
            "active_task_count": len(task_state["active"]),
            "recent_feedback_count": len(feedback["items"]),
        },
        "blocked_status_items": blocked_status[:10],
        "active_task_state": task_state["active"],
        "recent_feedback": feedback["items"],
        "feedback_loop": feedback["feedback_loop"],
        "boundary": "Project health is a compact control-plane condition view, not a manager decision or canonical assessment.",
    }


def query_terms(query: str) -> list[str]:
    return [term for term in re.findall(r"[A-Za-z0-9_./:-]+", query.lower()) if len(term) >= 2]


def query_snippet(body: str, terms: list[str], fallback: str = "", limit: int = 420) -> str:
    compact = re.sub(r"\s+", " ", body).strip()
    lower = compact.lower()
    positions = [lower.find(term) for term in terms if lower.find(term) >= 0]
    if not positions:
        return compact_text(fallback or compact, limit=limit)
    start = max(0, min(positions) - 120)
    end = min(len(compact), start + limit)
    snippet = compact[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(compact):
        snippet += "..."
    return snippet


def markdown_files_under(root: Path, limit: int = 80) -> list[Path]:
    if not root.exists():
        return []
    excluded = {".git", "backup", "node_modules", "__pycache__"}
    paths: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if any(part in excluded for part in path.parts):
            continue
        paths.append(path)
        if len(paths) >= limit:
            break
    return paths


def query_candidate_sources(actor: str, scope: str, kinds: set[str], include_stale: bool = False) -> list[tuple[str, Path]]:
    paths = actor_paths(actor, scope)
    project_root = paths["project_root"]
    sources: list[tuple[str, Path]] = []
    def include(kind: str) -> bool:
        return not kinds or kind in kinds
    def include_selected(kind: str) -> bool:
        return kind in kinds
    if include("current_state"):
        sources.append(("current_state", project_root / "working/current-state.md"))
    if include("current_direction"):
        sources.append(("current_direction", project_root / "working/current-direction.md"))
    if include("handoff"):
        sources.append(("handoff", project_root / "working/handoff/current.md"))
    if include("open_items"):
        sources.append(("open_items", project_root / "working/open-items.md"))
    if include("open_questions"):
        sources.append(("open_questions", project_root / "working/open-questions.md"))
    if include_selected("project_registry"):
        sources.append(("project_registry", REPO_ROOT / "brain/shared/project-registry.md"))
    if include_selected("canonical"):
        sources.extend(("canonical", path) for path in markdown_files_under(project_root / "canonical"))
    if include_selected("policy"):
        sources.extend(("policy", path) for path in markdown_files_under(REPO_ROOT / "brain/shared/policies"))
    if include_selected("contract"):
        sources.extend(("contract", path) for path in markdown_files_under(REPO_ROOT / "packages/aicos-kernel/contracts"))
    if include("packets"):
        sources.append(("packet_index", paths["packet_index"]))
        sources.extend(("packet", path) for path in collect_packets(paths["packet_root"]))
    if include("status_items"):
        status_root = project_root / "working/status-items"
        if status_root.exists():
            for path in sorted(status_root.glob("*.md")):
                if not include_stale and markdown_field(read_text(path), "Status") in DEFAULT_HIDDEN_STATUSES:
                    continue
                sources.append(("status_item", path))
    if include("task_state"):
        task_root = project_root / "working/task-state"
        if task_root.exists():
            sources.extend(("task_state", path) for path in sorted(task_root.glob("*.md")))
    if include("workstreams"):
        workstream_root = project_root / "working/workstreams"
        if workstream_root.exists():
            sources.extend(("workstream", path) for path in sorted(workstream_root.glob("*.md")))
    if include("artifacts"):
        artifact_root = project_root / "working/artifact-refs"
        if artifact_root.exists():
            sources.extend(("artifact_ref", path) for path in sorted(artifact_root.glob("*.md")))
    return sources


def direct_read_nudges_for_query(query: str) -> list[dict[str, str]]:
    """Suggest structured reads when markdown-direct fallback handles query."""
    lowered = query.lower()
    nudges: list[dict[str, str]] = []

    def has_any(terms: list[str]) -> bool:
        return any(term in lowered for term in terms)

    def add(tool: str, reason: str) -> None:
        if not any(item["tool"] == tool for item in nudges):
            nudges.append({"tool": tool, "reason": reason})

    startup_or_role = has_any(["read first", "before starting", "before continuing", "what should", "manager read", "worker read", "bắt đầu", "đọc gì", "nên đọc"])
    current_and_next = has_any(["đang làm", "làm đến đâu", "where are we", "current progress", "what's happening", "what is happening"]) and has_any(["next work", "what should be done next", "việc gì tiếp", "làm gì tiếp"])
    strategic_review = has_any(["cto", "ceo", "strategic review", "architecture review", "technical review", "product review", "build-vs-buy", "build vs buy", "scalability", "đóng vai", "vai trò cto", "vai trò ceo", "đọc tổng quan", "thiết kế kiến trúc", "đánh giá", "phản biện", "rủi ro kiến trúc", "định hướng sản phẩm", "chiến lược"])
    if startup_or_role or strategic_review or current_and_next:
        add("aicos_get_startup_bundle", "Best first read for role/project orientation before broad search.")
    if has_any(["what projects", "list projects", "projects exist", "project registry", "có project", "dự án nào"]):
        add("aicos_get_project_registry", "Best direct read for discovering registered projects.")
    if strategic_review or has_any(["đang làm", "làm đến đâu", "where are we", "current progress", "what's happening", "what is happening", "next work", "what should be done next", "việc gì tiếp", "làm gì tiếp", "ai đang làm", "which agents", "avoid overlap", "stepping on", "chồng chéo", "dẫm chân"]):
        add("aicos_get_handoff_current", "Best direct read for current continuity and takeover context.")
        add("aicos_get_status_items", "Best direct read for open items, tech debt, blockers, and decision follow-ups.")
        add("aicos_get_project_health", "Best direct read for project health, authority, and coordination signals.")
    if has_any(["ai đang làm", "which agents", "avoid overlap", "stepping on", "chồng chéo", "dẫm chân"]):
        add("aicos_get_feedback_digest", "Useful secondary read for recent A1 friction and coordination signals.")
    return nudges


def query_project_context(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    query = optional_read_string(arguments, "query", max_len=300)
    if not query:
        raise AicosMcpReadError("missing_argument", "query is required.", {"required": ["query"]})
    allowed_kinds = {
        "current_state",
        "current_direction",
        "handoff",
        "packets",
        "status_items",
        "task_state",
        "workstreams",
        "artifacts",
        "open_items",
        "open_questions",
        "canonical",
        "policy",
        "contract",
        "project_registry",
    }
    kinds = set(optional_read_list(arguments, "context_kinds", allowed_kinds, max_items=10))
    max_results_raw = arguments.get("max_results", 5)
    if not isinstance(max_results_raw, int):
        raise AicosMcpReadError("invalid_argument_type", "max_results must be an integer.", {"field": "max_results"})
    max_results = max(1, min(max_results_raw, 10))
    include_stale = bool(arguments.get("include_stale", False))
    project_role = optional_read_string(arguments, "project_role", max_len=80)
    terms = query_terms(query)
    candidates = query_candidate_sources(actor, scope, kinds, include_stale=include_stale)
    scored: list[dict[str, Any]] = []
    for kind, path in candidates:
        if not path.exists() or not path.is_file():
            continue
        body = read_text(path)
        haystack = body.lower()
        score = sum(haystack.count(term) for term in terms)
        title = markdown_title(body, path.stem)
        if query.lower() in haystack:
            score += 5
        if any(term in title.lower() for term in terms):
            score += 3
        if score <= 0:
            continue
        section_summary = first_paragraph(markdown_section(body, "Summary")) or first_paragraph(markdown_section(body, "Tóm Tắt"))
        scored.append(
            {
                "score": score,
                "kind": kind,
                "ref": rel(path),
                "title": title,
                "summary": query_snippet(body, terms, fallback=section_summary, limit=420),
            }
        )
    scored.sort(key=lambda item: (-item["score"], item["ref"]))
    results = [
        {
            "rank": index + 1,
            "kind": item["kind"],
            "ref": item["ref"],
            "title": item["title"],
            "summary": item["summary"],
        }
        for index, item in enumerate(scored[:max_results])
    ]
    source_refs = [SourceRef(path, kind) for kind, path in candidates[:50]]
    return {
        "metadata": metadata("aicos_query_project_context", actor, scope, source_refs),
        "query": query,
        "project_role": project_role or "any",
        "context_kinds": sorted(kinds) if kinds else "default_hot_context",
        "include_stale": include_stale,
        "default_hidden_statuses": [] if include_stale else sorted(DEFAULT_HIDDEN_STATUSES),
        "direct_read_nudges": direct_read_nudges_for_query(query),
        "results": results,
        "boundary": "Bounded keyword/metadata search over AICOS hot context. Results are refs and compact summaries, not source-of-truth promotion and not full file dumps.",
    }


def coordination_rules_payload() -> dict[str, Any]:
    contract_status = contract_status_payload()
    return {
        "policy_ref": "brain/shared/policies/agent-coordination-policy.md",
        "required_write_identity": contract_status["required_write_fields"],
        "agent_family_rule": "Use the client/product family such as codex, claude-code, gemini-antigravity, or openclaw; do not use A1/A2 role labels.",
        "artifact_neutral_rule": "Use work_lane for all work types. For non-code work, use artifact_scope and artifact_refs instead of inventing code worktree requirements.",
        "code_worktree_rule": "For work_type=code, include worktree_path. Reuse a worktree only for explicit continuation, handoff, review, takeover, or pair-work; otherwise use a separate worktree for parallel/different lane/branch/dirty-overlap risk.",
    }


def packet_index_payload(actor: str, scope: str) -> dict[str, Any]:
    paths = actor_paths(actor, scope)
    packet_root = paths["packet_root"]
    packet_index = paths["packet_index"]
    packet_paths = collect_packets(packet_root)
    sources = [SourceRef(packet_index, "packet_index"), *[SourceRef(path, "task_packet") for path in packet_paths]]
    return {
        "metadata": metadata("aicos_get_packet_index", actor, scope, sources),
        "actor_lane": paths["actor_lane"],
        "packet_index_path": rel(packet_index),
        "packets": [
            {
                "packet_id": path.stem,
                "path": rel(path),
                "title": markdown_title(read_text(path), path.stem),
                "summary": packet_summary(path),
            }
            for path in packet_paths
        ],
        "loading_rule": "Load exactly one task packet only after task selection or strong implication.",
    }


def latest_handoff_signal(handoff: Path) -> dict[str, Any]:
    body = read_text(handoff)
    base = {
        "path": rel(handoff),
        "exists": handoff.exists(),
        "latest_update_id": "",
        "latest_written_at": "",
        "actor_role": "",
        "agent_family": "",
        "agent_instance_id": "",
        "work_type": "",
        "work_lane": "",
        "coordination_status": "",
        "artifact_scope": "",
        "work_branch": "",
        "worktree_path": "",
        "summary": "",
        "read_hint": "Empty active_task_state does not prove the project is idle. Check continuity_signal and load handoff-current when continuing or checking active workstreams.",
    }
    if not body:
        return base
    matches = list(re.finditer(r"^## MCP Continuity Update:\s*(.+?)\s*$", body, flags=re.MULTILINE))
    if not matches:
        base["summary"] = compact_text(first_paragraph(body), limit=260)
        return base
    match = matches[-1]
    next_match = next((item for item in matches if item.start() > match.start()), None)
    block = body[match.end() : next_match.start() if next_match else len(body)]
    base.update(
        {
            "latest_update_id": match.group(1).strip(),
            "latest_written_at": markdown_heading_field(block, "Written at"),
            "actor_role": markdown_heading_field(block, "Actor role"),
            "agent_family": markdown_heading_field(block, "Agent family"),
            "agent_instance_id": markdown_heading_field(block, "Agent instance id"),
            "work_type": markdown_heading_field(block, "Work type"),
            "work_lane": markdown_heading_field(block, "Work lane"),
            "coordination_status": markdown_heading_field(block, "Coordination status"),
            "artifact_scope": markdown_heading_field(block, "Artifact scope"),
            "work_branch": markdown_heading_field(block, "Work branch"),
            "worktree_path": markdown_heading_field(block, "Worktree path"),
            "summary": compact_text(first_paragraph(markdown_section_any_level(block, "Summary")), limit=300),
        }
    )
    return base


def startup_bundle(actor: str, scope: str, arguments: dict[str, Any]) -> dict[str, Any]:
    paths = actor_paths(actor, scope)
    project_root = paths["project_root"]
    current_state = project_root / "working/current-state.md"
    current_direction = project_root / "working/current-direction.md"
    current_handoff = project_root / "working/handoff/current.md"
    startup_card = paths["startup_card"]
    actor_ladder = paths["actor_ladder"]
    project_ladder = paths["project_ladder"]
    role_or_profile = paths["role_or_profile"]
    working_rules = paths["working_rules"]
    coordination_policy = REPO_ROOT / "brain/shared/policies/agent-coordination-policy.md"
    contract_doc = REPO_ROOT / "packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md"
    packet_index = packet_index_payload(actor, scope)

    state_body = read_text(current_state)
    direction_body = read_text(current_direction)
    startup_body = read_text(startup_card)
    sources = [
        SourceRef(startup_card, "startup_card"),
        SourceRef(actor_ladder, "actor_context_ladder"),
        SourceRef(project_ladder, "project_context_ladder"),
        SourceRef(current_state, "current_state"),
        SourceRef(current_direction, "current_direction"),
        SourceRef(current_handoff, "conditional_handoff"),
        SourceRef(role_or_profile, "role_or_project_profile"),
        SourceRef(working_rules, "working_rules"),
        SourceRef(coordination_policy, "coordination_policy"),
        SourceRef(contract_doc, "mcp_contract"),
        SourceRef(paths["packet_index"], "packet_index"),
    ]
    task_state = collect_task_state(project_root)
    status_items = collect_status_items(project_root)
    feedback = feedback_digest_payload(actor, scope, {"max_results": 5, **arguments})
    handoff_signal = latest_handoff_signal(current_handoff)
    return {
        "metadata": metadata("aicos_get_startup_bundle", actor, scope, sources),
        "actor_lane": paths["actor_lane"],
        "boundary": {
            "aicos": "context/control-plane authority",
            "external_checkout": "code/runtime authority when present",
            "mcp": "read-serving access surface, not truth store",
        },
        "startup_card": {
            "path": rel(startup_card),
            "you_are": summarize_bullets(markdown_section(startup_body, "You Are"), limit=4),
            "you_are_not_doing": summarize_bullets(markdown_section(startup_body, "You Are Not Doing"), limit=4),
        },
        "context_ladders": [
            {"path": rel(actor_ladder), "role": "actor ladder", "exists": actor_ladder.exists()},
            {"path": rel(project_ladder), "role": "project ladder", "exists": project_ladder.exists()},
        ],
        "current_state": {
            "path": rel(current_state),
            "overview": first_paragraph(markdown_section(state_body, "Tóm Tắt") or markdown_section(state_body, "Summary")),
            "known": summarize_bullets(markdown_section(state_body, "Đã Có") or markdown_section(state_body, "Known"), limit=5),
            "not_active": summarize_bullets(markdown_section(state_body, "Chưa Active Đầy Đủ") or markdown_section(state_body, "Not Yet Imported"), limit=5),
        },
        "current_direction": {
            "path": rel(current_direction),
            "bullets": summarize_bullets(markdown_section(direction_body, "Ưu Tiên Hiện Nay") or markdown_section(direction_body, "Current Direction"), limit=5),
        },
        "mcp_contract_status": contract_status_payload(),
        "suggested_next_reads": [
            {"path": rel(actor_ladder), "reason": "lightweight actor reading map"},
            *([{"path": rel(project_ladder), "reason": "project-specific reading map"}] if project_ladder.exists() else []),
            {"path": rel(role_or_profile), "reason": "stable role/project identity"},
            {"path": rel(working_rules), "reason": "stable working/checkpoint rules"},
            {"path": rel(coordination_policy), "reason": "agent identity, work lane, artifact scope, and code worktree coordination"},
            {"path": rel(contract_doc), "reason": "current MCP read/write schema and refresh rules"},
        ],
        "conditional_handoff": {
            "path": rel(current_handoff),
            "load_when": "continuation, migration/state alignment, repo-wide architecture, or newest-vs-stale checks",
            "empty_active_task_state_warning": "Empty active_task_state does not mean the project is idle. Check continuity_signal and active_status_items before concluding there is no active work.",
        },
        "continuity_signal": handoff_signal,
        "coordination_rules": coordination_rules_payload(),
        "active_task_state": task_state["active"],
        "recent_completed_task_state": task_state["recent_completed"],
        "active_status_items": status_items["active"],
        "recent_status_items": status_items["recent"],
        "feedback_loop": feedback["feedback_loop"],
        "recent_feedback": feedback["items"],
        "packet_index": packet_index["packets"],
        "rule_card_refs": paths["rule_cards"],
        "not_loaded": [
            "long design docs under docs/New design/",
            "old handoff provenance backup",
            "backup/import/runtime/cache material",
            "network, API, UI, or external memory state",
        ],
    }


def handoff_current(actor: str, scope: str) -> dict[str, Any]:
    paths = actor_paths(actor, scope)
    handoff = paths["project_root"] / "working/handoff/current.md"
    if not handoff.exists():
        raise AicosMcpReadError("missing_handoff", "Current handoff does not exist.", {"path": rel(handoff)})
    body = read_text(handoff)
    return {
        "metadata": metadata("aicos_get_handoff_current", actor, scope, [SourceRef(handoff, "handoff_current")]),
        "path": rel(handoff),
        "title": markdown_title(body, "Current Handoff"),
        "content": body,
        "boundary": "H1 current handoff only; old handoffs and backup are not loaded.",
    }


def task_packet(actor: str, scope: str, packet_id: str) -> dict[str, Any]:
    paths = actor_paths(actor, scope)
    packet_root = paths["packet_root"]
    candidate = packet_root / f"{packet_id}.md"
    if not candidate.exists():
        # Allow callers to pass a filename for convenience, but keep resolution
        # inside the authorized packet root.
        maybe_name = packet_id if packet_id.endswith(".md") else f"{packet_id}.md"
        candidate = packet_root / Path(maybe_name).name
    if not candidate.exists() or candidate.parent != packet_root:
        available = [path.stem for path in collect_packets(packet_root)]
        raise AicosMcpReadError(
            "missing_task_packet",
            "Task packet was not found in the allowed packet root.",
            {"packet_id": packet_id, "packet_root": rel(packet_root), "available": available},
        )
    body = read_text(candidate)
    return {
        "metadata": metadata("aicos_get_task_packet", actor, scope, [SourceRef(candidate, "task_packet")]),
        "packet_id": candidate.stem,
        "path": rel(candidate),
        "title": markdown_title(body, candidate.stem),
        "summary": packet_summary(candidate),
        "content": body,
        "loading_rule": "This is the selected packet. Do not load sibling packets unless the task changes.",
    }


def dispatch_read_surface(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    actor = service_actor_label(str(arguments.get("actor", "A1")))
    scope = str(arguments.get("scope", "projects/aicos"))
    if name == "aicos_get_startup_bundle":
        return startup_bundle(actor, scope, arguments)
    if name == "aicos_get_handoff_current":
        return handoff_current(actor, scope)
    if name == "aicos_get_packet_index":
        return packet_index_payload(actor, scope)
    if name == "aicos_get_task_packet":
        packet_id = arguments.get("packet_id")
        if not packet_id:
            raise AicosMcpReadError("missing_argument", "packet_id is required.", {"required": ["packet_id"]})
        return task_packet(actor, scope, str(packet_id))
    if name == "aicos_get_status_items":
        return status_items_payload(actor, scope, arguments)
    if name == "aicos_get_workstream_index":
        return workstream_index_payload(actor, scope, arguments)
    if name == "aicos_get_context_registry":
        return context_registry_read_payload(actor, scope, arguments)
    if name == "aicos_get_project_registry":
        return project_registry_payload(actor, scope, arguments)
    if name == "aicos_get_feedback_digest":
        return feedback_digest_payload(actor, scope, arguments)
    if name == "aicos_get_project_health":
        return project_health_payload(actor, scope, arguments)
    if name == "aicos_query_project_context":
        return query_project_context(actor, scope, arguments)
    raise AicosMcpReadError("unknown_surface", "Unknown Phase 1 MCP read surface.", {"surface": name})
