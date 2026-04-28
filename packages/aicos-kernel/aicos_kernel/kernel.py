from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .context_registry import registry_payload, render_registry_markdown
from .mcp_read_serving import AicosMcpReadError, dispatch_read_surface
from .mcp_write_serving import AicosMcpWriteError, dispatch_write_tool
from .relations.trace_refs import parse_trace_refs, repo_path_exists


REPO_ROOT = Path(__file__).resolve().parents[3]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def write_json(path: Path, data: dict[str, Any]) -> Path:
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def markdown_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


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


def markdown_field(body: str, field: str) -> str:
    prefix = f"{field}:"
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip().strip("`").strip()
    return ""


def compact_text(body: str, limit: int = 360) -> str:
    text = re.sub(r"\s+", " ", body).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def first_paragraph(section: str) -> str:
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("- ") or (stripped.split(" ", 1)[0].endswith(".") and stripped.split(" ", 1)[0][:-1].isdigit()):
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


def upsert_markdown_section(path: Path, heading: str, body: str) -> Path:
    existing = read_text(path).rstrip()
    marker = f"## {heading}"
    section = f"{marker}\n\n{body.strip()}\n"
    if not existing:
        return write_text(path, section)
    start = existing.find(marker)
    if start == -1:
        return write_text(path, f"{existing}\n\n{section}")
    next_start = existing.find("\n## ", start + len(marker))
    if next_start == -1:
        updated = f"{existing[:start].rstrip()}\n\n{section}"
    else:
        updated = f"{existing[:start].rstrip()}\n\n{section}\n{existing[next_start:].lstrip()}"
    return write_text(path, updated)


def replace_status_line(path: Path, status: str) -> Path:
    body = read_text(path)
    if not body:
        return path
    lines = body.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("Status:"):
            lines[index] = f"Status: {status}"
            replaced = True
            break
    if not replaced:
        insert_at = 1 if lines and lines[0].startswith("# ") else 0
        lines.insert(insert_at, f"Status: {status}")
    return write_text(path, "\n".join(lines).rstrip() + "\n")


def collect_markdown(scope_root: Path, limit: int = 10) -> list[Path]:
    if not scope_root.exists():
        return []
    ignored = {".git", ".runtime-home", "node_modules"}
    files: list[Path] = []
    for path in sorted(scope_root.rglob("*.md")):
        if ignored.intersection(path.parts):
            continue
        files.append(path)
        if len(files) >= limit:
            break
    return files


@dataclass(frozen=True)
class CapsuleTarget:
    capsule_type: str
    identifier: str
    source_root: Path
    output_root: Path


def capsule_target(args: argparse.Namespace) -> CapsuleTarget:
    capsule_type = args.capsule_type
    if capsule_type == "company":
        identifier = args.values[0]
        return CapsuleTarget("company", identifier, REPO_ROOT / "brain/companies" / identifier, REPO_ROOT / "serving/capsules/company")
    if capsule_type == "workspace":
        identifier = args.values[0]
        return CapsuleTarget("workspace", identifier, REPO_ROOT / "brain/workspaces" / identifier, REPO_ROOT / "serving/capsules/workspace")
    if capsule_type == "project":
        identifier = args.values[0]
        return CapsuleTarget("project", identifier, REPO_ROOT / "brain/projects" / identifier, REPO_ROOT / "serving/capsules/project")
    if capsule_type == "branch":
        project_id, branch_id = args.values
        identifier = f"{project_id}__{branch_id}"
        return CapsuleTarget("branch", identifier, REPO_ROOT / "brain/projects" / project_id / "branches" / branch_id, REPO_ROOT / "serving/capsules/branch")
    if capsule_type == "actor":
        actor_class, scope = args.values
        identifier = f"{actor_class}__{scope.replace('/', '__')}"
        return CapsuleTarget("actor", identifier, REPO_ROOT / "agent-repo/classes" / actor_class, REPO_ROOT / "serving/capsules/a1")
    raise ValueError(f"Unsupported capsule type: {capsule_type}")


def render_capsule_markdown(capsule: dict[str, Any]) -> str:
    sections = []
    for item in capsule["items"]:
        sections.append(
            "\n".join(
                [
                    f"## {item['title']}",
                    "",
                    f"Source: `{item['source']}`",
                    "",
                    item["excerpt"],
                ]
            )
        )
    return "\n\n".join(
        [
            f"# AICOS {capsule['capsule_type'].title()} Capsule: {capsule['identifier']}",
            "",
            f"Generated: `{capsule['generated_at']}`",
            "",
            "This capsule is a deterministic MVP packet. Capsule assembly policy remains in A2 service skills.",
            "",
            *sections,
            "",
        ]
    )


def build_capsule(args: argparse.Namespace) -> int:
    target = capsule_target(args)
    source_files = collect_markdown(target.source_root)
    items = []
    for path in source_files:
        body = read_text(path).strip()
        items.append(
            {
                "source": rel(path),
                "title": markdown_title(body, path.stem),
                "excerpt": body[:1800] if body else "",
            }
        )
    capsule = {
        "schema_version": "0.1",
        "kind": "aicos.capsule",
        "capsule_type": target.capsule_type,
        "identifier": target.identifier,
        "generated_at": now_iso(),
        "source_root": rel(target.source_root),
        "items": items,
        "warnings": [] if source_files else [f"No markdown files found under {rel(target.source_root)}"],
    }
    json_path = target.output_root / f"{target.identifier}.json"
    md_path = target.output_root / f"{target.identifier}.md"
    write_json(json_path, capsule)
    write_text(md_path, render_capsule_markdown(capsule))
    print(rel(md_path))
    print(rel(json_path))
    return 0


def branch_compare(args: argparse.Namespace) -> int:
    project_id, branch_a, branch_b = args.project_id, args.branch_a, args.branch_b
    root = REPO_ROOT / "brain/projects" / project_id / "branches"
    a_root = root / branch_a
    b_root = root / branch_b
    packet = {
        "schema_version": "0.1",
        "kind": "aicos.branch_compare",
        "project_id": project_id,
        "branch_a": branch_a,
        "branch_b": branch_b,
        "generated_at": now_iso(),
        "inputs": [rel(a_root), rel(b_root)],
        "summary": "Thin deterministic comparison packet. Comparison policy remains in A2 service skills.",
        "exists": {"branch_a": a_root.exists(), "branch_b": b_root.exists()},
    }
    out = REPO_ROOT / "serving/branching/branch-compare" / f"{project_id}__{branch_a}__{branch_b}.json"
    write_json(out, packet)
    print(rel(out))
    return 0


def option_generate(args: argparse.Namespace) -> int:
    project_id, blocker_id = args.project_id, args.blocker_id
    blocker_paths = [
        REPO_ROOT / "agent-repo/classes/a1-work-agents/tasks/blocked" / f"{blocker_id}.md",
        REPO_ROOT / "brain/projects" / project_id / "working/blockers" / f"{blocker_id}.md",
    ]
    blocker_path = next((path for path in blocker_paths if path.exists()), blocker_paths[0])
    blocker_body = read_text(blocker_path).strip()
    title = markdown_title(blocker_body, blocker_id)
    options = [
        {
            "id": "option-a",
            "label": "Minimal branch scaffold",
            "branch_id": f"{blocker_id}-option-a",
            "recommendation": "Recommended for MVP because it proves the flow with the smallest reversible change.",
        },
        {
            "id": "option-b",
            "label": "Broader integration pass",
            "branch_id": f"{blocker_id}-option-b",
            "recommendation": "Use later if the reviewer wants deeper migration before proving the local flow.",
        },
    ]
    for option in options:
        branch_root = REPO_ROOT / "brain/projects" / project_id / "branches" / option["branch_id"]
        write_text(branch_root / "branch-profile.md", f"# {option['label']}\n\nProject: `{project_id}`\n\nBlocker: `{blocker_id}`\n")
        write_text(branch_root / "inherited-context.md", f"# Inherited Context\n\nDerived from blocker `{blocker_id}` and project `{project_id}`.\n")
        write_text(branch_root / "assumptions.md", "# Assumptions\n\n- This branch is an MVP option, not approved canonical truth.\n")
        write_text(branch_root / "recommendation.md", f"# Recommendation\n\n{option['recommendation']}\n")
    packet = {
        "schema_version": "0.1",
        "kind": "aicos.option_packet",
        "project_id": project_id,
        "blocker_id": blocker_id,
        "blocker_source": rel(blocker_path),
        "title": title,
        "generated_at": now_iso(),
        "options": options,
        "recommended_option_id": "option-a",
        "policy_source": "agent-repo/classes/a2-service-agents/skills/generate-mvp-options/SKILL.md",
    }
    out_root = REPO_ROOT / "serving/branching/option-packets"
    json_path = out_root / f"{project_id}__{blocker_id}.json"
    md_path = out_root / f"{project_id}__{blocker_id}.md"
    write_json(json_path, packet)
    write_text(
        md_path,
        "\n".join(
            [
                f"# Option Packet: {project_id} / {blocker_id}",
                "",
                f"Generated: `{packet['generated_at']}`",
                f"Blocker source: `{packet['blocker_source']}`",
                "",
                "## Recommendation",
                "",
                "Choose `option-a` for the MVP proof unless the reviewer asks for a broader migration first.",
                "",
                "## Options",
                "",
                *[f"- `{item['id']}` -> branch `{item['branch_id']}`: {item['label']}" for item in options],
                "",
            ]
        ),
    )
    print(rel(md_path))
    print(rel(json_path))
    return 0


def option_choose(args: argparse.Namespace) -> int:
    project_id = args.project_id
    blocker_id = args.blocker_id
    option_id = args.option_id
    packet_path = REPO_ROOT / "serving/branching/option-packets" / f"{project_id}__{blocker_id}.json"
    if not packet_path.exists():
        print(f"Missing option packet: {rel(packet_path)}")
        return 2

    packet = load_json(packet_path)
    options = packet.get("options", [])
    selected = next((item for item in options if item.get("id") == option_id), None)
    if not selected:
        available = ", ".join(str(item.get("id")) for item in options)
        print(f"Unknown option: {option_id}")
        print(f"Available options: {available}")
        return 2

    branch_id = str(selected["branch_id"])
    branch_root = REPO_ROOT / "brain/projects" / project_id / "branches" / branch_id
    if not branch_root.exists():
        print(f"Missing selected branch: {rel(branch_root)}")
        return 2

    now = now_iso()
    actor = args.actor
    reason = args.reason or str(selected.get("recommendation", "Manager selected this option in chat."))
    updated: list[Path] = []

    approval_path = REPO_ROOT / "agent-repo/classes/humans/approvals" / f"manager-choice-{blocker_id}.md"
    approval_body = "\n".join(
        [
            f"# Manager Choice: {blocker_id}",
            "",
            "Status: committed-to-aicos-state",
            f"Project: `{project_id}`",
            f"Blocker: `{blocker_id}`",
            f"Option packet: `{rel(packet_path.with_suffix('.md'))}`",
            f"Selected option: `{option_id}`",
            f"Selected branch: `{rel(branch_root)}/`",
            f"Decision actor: `{actor}`",
            f"Decision recorded at: `{now}`",
            "",
            "## Decision",
            "",
            f"Proceed with `{option_id}` via branch `{branch_id}`.",
            "",
            "## Rationale",
            "",
            reason,
            "",
            "## Boundary Notes",
            "",
            "- This records a manager decision from chat into AICOS state.",
            "- This does not promote working state to canonical truth.",
            "- Other option branches remain available for review.",
            "- Backend/runtime state is not treated as authority.",
            "",
        ]
    )
    updated.append(write_text(approval_path, approval_body))

    selected_state_path = branch_root / "selection-state.md"
    selected_state_body = "\n".join(
        [
            f"# Selection State: {branch_id}",
            "",
            "Status: selected",
            f"Project: `{project_id}`",
            f"Blocker: `{blocker_id}`",
            f"Selected option: `{option_id}`",
            f"Decision actor: `{actor}`",
            f"Decision recorded at: `{now}`",
            "",
            "## Source",
            "",
            f"- Option packet: `{rel(packet_path)}`",
            f"- Manager choice: `{rel(approval_path)}`",
            "",
            "## Boundary",
            "",
            "This branch is selected working direction, not canonical architecture truth.",
            "",
        ]
    )
    updated.append(write_text(selected_state_path, selected_state_body))

    current_state_path = REPO_ROOT / "brain/projects" / project_id / "working/current-state.md"
    state_section = "\n".join(
        [
            f"Recorded at: `{now}`",
            "",
            f"- Blocker: `{blocker_id}`",
            f"- Selected option: `{option_id}`",
            f"- Selected branch: `{branch_id}`",
            f"- Manager choice packet: `{rel(approval_path)}`",
            f"- Branch state: `{rel(selected_state_path)}`",
            "",
            "The project has a committed working direction for this blocker. Canonical truth remains unchanged until a separate promotion/review step.",
        ]
    )
    updated.append(upsert_markdown_section(current_state_path, f"Manager Decision: {blocker_id}", state_section))

    current_direction_path = REPO_ROOT / "brain/projects" / project_id / "working/current-direction.md"
    direction_section = "\n".join(
        [
            f"Active branch: `{branch_id}`",
            f"Chosen option: `{option_id}`",
            f"Reason: {reason}",
            "",
            "Next execution should follow the selected branch and keep broader alternatives as reviewable branches, not delete them.",
        ]
    )
    updated.append(upsert_markdown_section(current_direction_path, f"Selected Direction: {blocker_id}", direction_section))

    open_questions_path = REPO_ROOT / "brain/projects" / project_id / "working/open-questions.md"
    if open_questions_path.exists():
        questions_section = "\n".join(
            [
                f"Closed by manager decision at `{now}`.",
                "",
                f"- Blocker: `{blocker_id}`",
                f"- Selected option: `{option_id}`",
                f"- Selected branch: `{branch_id}`",
            ]
        )
        updated.append(upsert_markdown_section(open_questions_path, f"Closed Question: {blocker_id} option choice", questions_section))

    blocker_paths = [
        REPO_ROOT / "agent-repo/classes/a1-work-agents/tasks/blocked" / f"{blocker_id}.md",
        REPO_ROOT / "brain/projects" / project_id / "working/blockers" / f"{blocker_id}.md",
    ]
    for blocker_path in blocker_paths:
        if blocker_path.exists():
            replace_status_line(blocker_path, f"decision-selected ({option_id})")
            follow_up = "\n".join(
                [
                    f"Decision recorded at: `{now}`",
                    "",
                    f"- Selected option: `{option_id}`",
                    f"- Selected branch: `{branch_id}`",
                    f"- Manager choice: `{rel(approval_path)}`",
                ]
            )
            upsert_markdown_section(blocker_path, "Decision State", follow_up)
            updated.append(blocker_path)

    print(f"Chosen option: {option_id}")
    print(f"Project: {project_id}")
    print(f"Blocker: {blocker_id}")
    print(f"Selected branch: {branch_id}")
    print("")
    print("Updated:")
    for path in updated:
        print(f"- {rel(path)}")
    print("")
    print("Not changed:")
    print("- brain/projects/*/canonical/*")
    print("- other option branches")
    print("- backend truth")
    print("- GBrain/PGLite index (run `aicos sync brain` when retrieval refresh is needed)")
    return 0


def promote(args: argparse.Namespace) -> int:
    source = (REPO_ROOT / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path)
    if not source.exists():
        print(f"Missing promotion source: {source}")
        return 2
    lane = args.promotion_lane
    target_root = REPO_ROOT / "serving/promotion/review-packets" / lane
    target = target_root / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    review = target.with_suffix(target.suffix + ".review.md")
    write_text(
        review,
        f"# Promotion Review Packet\n\nLane: `{lane}`\n\nSource: `{rel(source)}`\n\nCopied to: `{rel(target)}`\n\nStatus: pending human review.\n",
    )
    print(rel(review))
    return 0


def validate_capsule(args: argparse.Namespace) -> int:
    path = Path(args.path)
    full_path = path if path.is_absolute() else REPO_ROOT / path
    try:
        data = json.loads(read_text(full_path))
    except json.JSONDecodeError as exc:
        print(f"invalid capsule: malformed JSON ({exc})")
        return 1
    required = {"schema_version", "kind", "capsule_type", "identifier", "items"}
    missing = sorted(required - set(data))
    if missing:
        print(f"invalid capsule: missing {', '.join(missing)}")
        return 1
    print("valid capsule")
    return 0


def validate_branch(args: argparse.Namespace) -> int:
    path = Path(args.path)
    full_path = path if path.is_absolute() else REPO_ROOT / path
    required = ["branch-profile.md", "inherited-context.md", "assumptions.md", "recommendation.md"]
    missing = [name for name in required if not (full_path / name).exists()]
    if missing:
        print(f"invalid branch: missing {', '.join(missing)}")
        return 1
    print("valid branch")
    return 0


def normalize_actor(actor: str) -> str:
    normalized = actor.strip().lower().replace("_", "-")
    aliases = {
        "a1": "a1-work",
        "a1-work": "a1-work",
        "a1-work-agent": "a1-work",
        "a1-work-agents": "a1-work",
        "a2-core": "a2-core",
        "a2-core-c": "a2-core",
        "a2-core-r": "a2-core",
    }
    return aliases.get(normalized, normalized)


def collect_task_packets(actor_key: str, scope: str) -> list[Path]:
    if actor_key == "a2-core" and scope == "projects/aicos":
        packet_root = REPO_ROOT / "agent-repo/classes/a2-service-agents/task-packets"
    elif actor_key == "a1-work" and scope.startswith("projects/"):
        project_id = scope.split("/", 1)[1]
        scoped_packet_root = REPO_ROOT / "agent-repo/classes/a1-work-agents/task-packets" / project_id
        packet_root = scoped_packet_root if scoped_packet_root.exists() else REPO_ROOT / "agent-repo/classes/a1-work-agents/task-packets"
    else:
        return []
    if not packet_root.exists():
        return []
    return sorted(path for path in packet_root.glob("*.md") if path.name != "README.md")


def task_packet_summary(path: Path) -> str:
    body = read_text(path)
    for field in ["summary", "objective"]:
        prefix = f"{field}:"
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith(prefix):
                return stripped[len(prefix):].strip().strip('"')
    return markdown_title(body, path.stem)


def context_start(args: argparse.Namespace) -> int:
    actor_key = normalize_actor(args.actor)
    scope = args.scope
    if actor_key not in {"a2-core", "a1-work"}:
        print(f"Unsupported actor for MVP context start: {args.actor}")
        print("Supported actors: A2-Core, A1")
        return 2
    if actor_key == "a2-core" and scope != "projects/aicos":
        print(f"Unsupported scope for MVP context start: {scope}")
        print("Supported scope: projects/aicos")
        return 2
    if actor_key == "a1-work" and not scope.startswith("projects/"):
        print(f"Unsupported scope for A1 context start: {scope}")
        print("Supported scope shape: projects/<project-id>")
        return 2

    project_id = scope.split("/", 1)[1]
    project_root = REPO_ROOT / "brain/projects" / project_id
    if actor_key == "a2-core":
        actor_lane = "A2-Core"
        startup_card = REPO_ROOT / "agent-repo/classes/a2-service-agents/startup-cards/a2-core.md"
        context_ladder = REPO_ROOT / "agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md"
        role_definitions = REPO_ROOT / "brain/projects/aicos/canonical/role-definitions.md"
        working_rules = REPO_ROOT / "brain/projects/aicos/canonical/project-working-rules.md"
        packet_index = REPO_ROOT / "agent-repo/classes/a2-service-agents/task-packets/README.md"
        rule_cards = [
            "agent-repo/classes/a2-service-agents/rule-cards/writeback.md",
            "agent-repo/classes/a2-service-agents/rule-cards/idea-capture.md",
            "agent-repo/classes/a2-service-agents/rule-cards/option-choose.md",
            "agent-repo/classes/a2-service-agents/rule-cards/sync-brain.md",
            "agent-repo/classes/a2-service-agents/rule-cards/handoff.md",
        ]
    else:
        actor_lane = "A1"
        startup_card = REPO_ROOT / "agent-repo/classes/a1-work-agents/startup-cards/a1.md"
        context_ladder = REPO_ROOT / "agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md"
        role_definitions = project_root / "canonical/project-profile.md"
        working_rules = REPO_ROOT / "brain/shared/policies/checkpoint-writeback-policy.md"
        packet_index = REPO_ROOT / "agent-repo/classes/a1-work-agents/task-packets/README.md"
        rule_cards = [
            "agent-repo/classes/a1-work-agents/rule-cards/writeback-checkpoint.md",
            "agent-repo/classes/a1-work-agents/rule-cards/handoff-continuation.md",
            "agent-repo/classes/a1-work-agents/rule-cards/task-packet-loading.md",
            "agent-repo/classes/a1-work-agents/rule-cards/project-state-routing.md",
            "agent-repo/classes/a1-work-agents/rule-cards/layered-rules.md",
            "agent-repo/classes/a1-work-agents/rule-cards/escalation-to-a2.md",
        ]
    current_state = project_root / "working/current-state.md"
    current_direction = project_root / "working/current-direction.md"
    current_handoff = project_root / "working/handoff/current.md"
    project_context_ladder = project_root / "working/context-ladder.md"
    packet_template = REPO_ROOT / "packages/aicos-kernel/contracts/task-packet-template.md"

    startup_body = read_text(startup_card)
    state_body = read_text(current_state)
    direction_body = read_text(current_direction)
    state_overview = first_paragraph(markdown_section(state_body, "Tóm Tắt") or markdown_section(state_body, "Summary"))
    existing_summary = summarize_bullets(markdown_section(state_body, "Đã Có") or markdown_section(state_body, "Known"), limit=4)
    direction_summary = summarize_bullets(markdown_section(direction_body, "Ưu Tiên Hiện Nay") or markdown_section(direction_body, "Current Direction"), limit=4)
    task_packets = collect_task_packets(actor_key, scope)

    print("# AICOS Context Start")
    print("")
    print(f"Actor: `{args.actor}`")
    print(f"Resolved actor lane: `{actor_lane}`")
    print(f"Scope: `{scope}`")
    print("Mode: packet-first startup bundle")
    print("Read-only: yes")
    print("")
    print("## Boundary")
    print("")
    print("AICOS serves context, rules, state summaries, task packets, and lookup paths.")
    print("AICOS does not control the internal memory/context behavior of external co-workers.")
    print("")
    print("## Startup Card")
    print("")
    print(f"Path: `{rel(startup_card)}`")
    if startup_body.strip():
        you_are = summarize_bullets(markdown_section(startup_body, "You Are"), limit=3)
        doing = summarize_bullets(markdown_section(startup_body, "You Are Doing"), limit=3)
        for bullet in [*you_are, *doing]:
            print(bullet)
    print("")
    print("## Context Ladder")
    print("")
    print("Use the ladder as the lightweight map before reading deeper.")
    print(f"- Actor ladder: `{rel(context_ladder)}`")
    if project_context_ladder.exists():
        print(f"- Project ladder: `{rel(project_context_ladder)}`")
    print("")
    print("## Current State")
    print("")
    print(f"Path: `{rel(current_state)}`")
    if state_overview:
        print(state_overview)
    for bullet in existing_summary:
        print(bullet)
    print("")
    print("## Current Direction")
    print("")
    print(f"Path: `{rel(current_direction)}`")
    for bullet in direction_summary:
        print(bullet)
    print("")
    print("## Suggested Next Reads")
    print("")
    next_reads = [context_ladder]
    if project_context_ladder.exists():
        next_reads.append(project_context_ladder)
    next_reads.extend([role_definitions, working_rules, current_state, current_direction])
    for path in next_reads:
        status = "" if path.exists() else " (missing)"
        print(f"- `{rel(path)}`{status}")
    print("")
    print("## Conditional Handoff")
    print("")
    print("Load the sole H1 current handoff index only for continuation, migration/state alignment, repo-wide architecture, or newest-vs-stale checks:")
    print(f"- `{rel(current_handoff)}`")
    print("")
    print("## Task Packet Index")
    print("")
    if packet_index.exists():
        print(f"Path: `{rel(packet_index)}`")
    print("Load one full task packet only after the task is chosen or strongly implied.")
    print("If no task is chosen, ask the human which task to continue.")
    print("")
    if task_packets:
        for path in task_packets:
            print(f"- `{rel(path)}` — {task_packet_summary(path)}")
    else:
        print(f"- Template only: `{rel(packet_template)}`")
    print("")
    print("## Rule Cards")
    print("")
    print("Load only when the task triggers them:")
    for path in rule_cards:
        print(f"- `{path}`")
    print("")
    print("## Not Loaded")
    print("")
    print("- long design docs under `docs/New design/`")
    print("- old handoff provenance under `backup/handoff-provenance-20260418/`")
    print("- backup/import/runtime/cache material")
    print("- network, API, UI, or external memory state")
    return 0


def brain_lane(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT / "brain")
    parts = relative.parts
    if len(parts) < 3:
        return "root"
    top = parts[0]
    if top in {"companies", "workspaces"} and len(parts) >= 3:
        return f"{top}/{parts[2]}"
    if top == "projects" and len(parts) >= 3:
        return f"projects/{parts[2]}"
    if top == "service-knowledge" and len(parts) >= 2:
        return f"service-knowledge/{parts[1]}"
    if top == "shared" and len(parts) >= 2:
        return f"shared/{parts[1]}"
    return top


def collect_brain_sync_files() -> tuple[list[Path], dict[str, int]]:
    brain_root = REPO_ROOT / "brain"
    files: list[Path] = []
    lane_counts: dict[str, int] = {}
    if not brain_root.exists():
        return files, lane_counts
    for path in sorted(brain_root.rglob("*.md")):
        if not path.is_file() or path.is_symlink():
            continue
        files.append(path)
        lane = brain_lane(path)
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
    return files, lane_counts


def latest_mtime(paths: list[Path]) -> datetime | None:
    if not paths:
        return None
    newest = max(path.stat().st_mtime for path in paths if path.exists())
    return datetime.fromtimestamp(newest, timezone.utc).replace(microsecond=0)


def runtime_state_path() -> Path:
    return REPO_ROOT / ".runtime-home/aicos/brain-sync-status.json"


def daemon_env_file() -> Path:
    return Path(os.environ.get("AICOS_DAEMON_ENV_FILE", str(REPO_ROOT / ".runtime-home/aicos-daemon.env")))


def load_daemon_env_file() -> dict[str, str]:
    path = daemon_env_file()
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key:
            values[key] = value.strip().strip("'").strip('"')
    return values


def write_daemon_env_file(values: dict[str, str]) -> Path:
    path = daemon_env_file()
    existing_order: list[str] = []
    passthrough: list[str] = []
    if path.exists():
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            if raw_line.strip() and not raw_line.lstrip().startswith("#") and "=" in raw_line:
                key = raw_line.split("=", 1)[0].strip()
                if key and key not in existing_order:
                    existing_order.append(key)
            else:
                passthrough.append(raw_line)
    default_order = [
        "AICOS_MCP_DAEMON_URL",
        "AICOS_DAEMON_HOST",
        "AICOS_DAEMON_PORT",
        "AICOS_DAEMON_CACHE_TTL",
        "AICOS_DAEMON_TOKEN",
        "AICOS_DAEMON_EXTRA_TOKENS",
        "AICOS_DAEMON_ALLOWLIST",
        "AICOS_DAEMON_INTERNAL_TOKEN_LABELS",
        "AICOS_DAEMON_TOKEN_SCOPE_POLICY",
        "AICOS_DAEMON_PRIMARY_TOKEN_LABEL",
    ]
    order = []
    for key in [*existing_order, *default_order, *sorted(values)]:
        if key in values and key not in order:
            order.append(key)
    body = "\n".join(f"{key}={values.get(key, '')}" for key in order).rstrip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def parse_extra_tokens(raw: str) -> dict[str, str]:
    tokens: dict[str, str] = {}
    for item in raw.split(","):
        entry = item.strip()
        if not entry or ":" not in entry:
            continue
        label, token = entry.split(":", 1)
        label = label.strip()
        token = token.strip()
        if label and token:
            tokens[label] = token
    return tokens


def render_extra_tokens(tokens: dict[str, str]) -> str:
    return ",".join(f"{label}:{token}" for label, token in tokens.items())


def csv_set(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def render_csv(values: set[str]) -> str:
    return ",".join(sorted(values))


def token_registry_path() -> Path:
    return REPO_ROOT / ".runtime-home/aicos-daemon-token-registry.json"


def load_token_registry() -> dict[str, Any]:
    path = token_registry_path()
    if not path.exists():
        return {"updated_at": "", "entries": []}
    try:
        data = load_json(path)
    except json.JSONDecodeError:
        data = {"updated_at": "", "entries": []}
    if not isinstance(data.get("entries"), list):
        data["entries"] = []
    return data


def write_token_registry(data: dict[str, Any]) -> Path:
    data["updated_at"] = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return write_json(token_registry_path(), data)


def masked_token(token: str) -> str:
    if len(token) <= 12:
        return token[:2] + "..."
    return token[:6] + "..." + token[-6:]


def write_runtime_state(payload: dict[str, Any]) -> None:
    write_json(runtime_state_path(), payload)


def load_runtime_state() -> dict[str, Any]:
    path = runtime_state_path()
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError:
        return {"error": "invalid runtime state json", "path": rel(path)}


def run_gbrain(args: list[str]) -> subprocess.CompletedProcess[str]:
    wrapper = REPO_ROOT / "scripts/gbrain_local.sh"
    return subprocess.run(
        [str(wrapper), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def parse_last_json_line(output: str) -> dict[str, Any] | None:
    for line in reversed(output.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return None


def daemon_reindex_url() -> str:
    env_values = load_daemon_env_file()
    daemon_url = os.environ.get("AICOS_MCP_DAEMON_URL", env_values.get("AICOS_MCP_DAEMON_URL", "http://127.0.0.1:8000/mcp")).rstrip("/")
    if daemon_url.endswith("/mcp"):
        daemon_url = daemon_url[:-4]
    return f"{daemon_url}/reindex?wait=1"


def request_daemon_reindex() -> tuple[bool, str]:
    env_values = load_daemon_env_file()
    request = urllib.request.Request(daemon_reindex_url())
    token = os.environ.get("AICOS_DAEMON_TOKEN", env_values.get("AICOS_DAEMON_TOKEN", ""))
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
        parsed = json.loads(body)
        status = str(parsed.get("status", "unknown"))
        return status == "reindex_completed", body
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return False, str(exc)


def sync_brain(args: argparse.Namespace) -> int:
    wrapper = REPO_ROOT / "scripts/gbrain_local.sh"
    if not wrapper.exists():
        print("missing scripts/gbrain_local.sh")
        return 2

    files, lane_counts = collect_brain_sync_files()
    if not files:
        print("Sync target: brain/")
        print("No markdown files found under brain/.")
        return 1

    runtime_home = REPO_ROOT / ".runtime-home"
    config_path = runtime_home / ".gbrain/config.json"
    db_path = runtime_home / ".gbrain/aicos-brain.pglite"
    initialized = config_path.exists()

    if not initialized:
        init_result = run_gbrain(["init", "--pglite", "--path", str(db_path), "--json"])
        if init_result.returncode != 0:
            print("Sync target: brain/")
            print("Engine: GBrain + PGLite")
            print("Result: init failed")
            print(init_result.stdout.strip())
            print(init_result.stderr.strip())
            return init_result.returncode

    mode = "text_only" if getattr(args, "text_only", False) else "full"
    import_args = ["import", str(REPO_ROOT / "brain"), "--fresh", "--json"]
    if mode == "text_only":
        import_args.insert(2, "--no-embed")
    import_result = run_gbrain(import_args)
    import_summary = parse_last_json_line(import_result.stdout)
    latest = latest_mtime(files)

    print("Sync target: brain/")
    print("Engine: GBrain + PGLite")
    print("")
    print("Scanned:")
    for lane, count in sorted(lane_counts.items()):
        print(f"- {lane}: {count} files")
    print("")
    print("Import/update:")
    if import_summary:
        print(f"- total files: {import_summary.get('total_files', len(files))}")
        print(f"- imported/updated: {import_summary.get('imported', 'unknown')}")
        print(f"- skipped/unchanged: {import_summary.get('skipped', 'unknown')}")
        print(f"- errors: {import_summary.get('errors', 'unknown')}")
        print(f"- chunks created: {import_summary.get('chunks', 'unknown')}")
    else:
        print(f"- scanned files passed to GBrain import: {len(files)}")
    print("")
    print("Skipped by policy:")
    print("- agent-repo/")
    print("- backend/")
    print("- backup/")
    print("- imports/")
    print("- scripts/")
    print("- integrations/")
    print("")
    print("Not changed:")
    print("- brain/* truth files")
    print("- promotion state")
    print("- manager choice state")
    print("")
    if not initialized:
        print(f"Initialized local PGLite config: {rel(config_path)}")
    if mode == "text_only":
        print("Embedding/vector refresh: skipped (`--text-only`).")
    else:
        print("Embedding/vector refresh: requested through GBrain import (`--full` / default).")

    if import_result.returncode != 0:
        print("")
        print("Result: sync failed during GBrain import")
        print(import_result.stdout.strip())
        print(import_result.stderr.strip())
        write_runtime_state(
            {
                "last_sync_at": now_iso(),
                "last_sync_mode": mode,
                "last_sync_status": "failed",
                "latest_brain_mtime": latest.isoformat() if latest else None,
                "gbrain_import_summary": import_summary or {},
            }
        )
        return import_result.returncode

    write_runtime_state(
        {
            "last_sync_at": now_iso(),
            "last_sync_mode": mode,
            "last_sync_status": "success",
            "latest_brain_mtime": latest.isoformat() if latest else None,
            "gbrain_import_summary": import_summary or {},
        }
    )
    print("")
    refresh_ok, refresh_detail = request_daemon_reindex()
    if refresh_ok:
        print("Daemon PostgreSQL reindex: completed")
    else:
        print(f"Daemon PostgreSQL reindex: skipped/failed ({refresh_detail})")
    print("")
    print("Result: sync success")
    return 0


def pg_index_status() -> dict[str, Any]:
    try:
        from .pg_search import PgSearchEngine, try_connect
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "reason": str(exc)}
    conn, err = try_connect()
    if err:
        return {"available": False, "reason": err}
    try:
        engine = PgSearchEngine(conn, REPO_ROOT)
        return {"available": True, **engine.index_stats()}
    finally:
        conn.close()


def brain_status(args: argparse.Namespace) -> int:
    files, lane_counts = collect_brain_sync_files()
    latest = latest_mtime(files)
    runtime_state = load_runtime_state()
    pg_status = pg_index_status()
    last_sync_at = runtime_state.get("last_sync_at")
    pg_latest_indexed = pg_status.get("latest_indexed_at") if pg_status.get("available") else None
    pg_latest_embedded = pg_status.get("latest_embedded_at") if pg_status.get("available") else None

    def stale(compared_at: str | None) -> str:
        if not latest:
            return "unknown"
        if not compared_at:
            return "unknown"
        try:
            current = datetime.fromisoformat(compared_at.replace("Z", "+00:00"))
        except ValueError:
            return "unknown"
        return "fresh" if current >= latest else "stale"

    payload = {
        "schema_version": "0.1",
        "kind": "aicos.brain_status",
        "checked_at": now_iso(),
        "brain_file_count": len(files),
        "latest_brain_mtime": latest.isoformat() if latest else None,
        "lane_counts": lane_counts,
        "gbrain_sync": {
            "last_sync_at": last_sync_at,
            "last_sync_mode": runtime_state.get("last_sync_mode", "unknown"),
            "last_sync_status": runtime_state.get("last_sync_status", "unknown"),
            "freshness": stale(last_sync_at),
        },
        "postgresql_index": {
            "available": bool(pg_status.get("available")),
            "reason": pg_status.get("reason", ""),
            "latest_indexed_at": pg_latest_indexed,
            "index_freshness": stale(pg_latest_indexed),
            "latest_embedded_at": pg_latest_embedded,
            "embedding_freshness": stale(pg_latest_embedded),
            "embedding_coverage": pg_status.get("embedding_coverage"),
            "missing_or_stale_embeddings": pg_status.get("missing_or_stale_embeddings"),
            "stale_docs": pg_status.get("stale_docs"),
            "total_docs": pg_status.get("total_docs"),
        },
        "boundary": "brain/ remains truth. This status reports serving/index freshness only.",
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    print("AICOS brain status")
    print(f"- brain files: {payload['brain_file_count']}")
    print(f"- latest brain mtime: {payload['latest_brain_mtime']}")
    print(f"- GBrain sync: {payload['gbrain_sync']['last_sync_status']} / {payload['gbrain_sync']['freshness']} ({payload['gbrain_sync']['last_sync_mode']})")
    print(f"- PG index: {'available' if payload['postgresql_index']['available'] else 'unavailable'} / {payload['postgresql_index']['index_freshness']}")
    if payload["postgresql_index"]["reason"]:
        print(f"  reason: {payload['postgresql_index']['reason']}")
    print(f"- embedding freshness: {payload['postgresql_index']['embedding_freshness']}")
    print(f"- embedding coverage: {payload['postgresql_index']['embedding_coverage']}")
    print(f"- missing/stale embeddings: {payload['postgresql_index']['missing_or_stale_embeddings']}")
    return 0


def mcp_read(args: argparse.Namespace) -> int:
    surface_map = {
        "startup-bundle": "aicos_get_startup_bundle",
        "handoff-current": "aicos_get_handoff_current",
        "packet-index": "aicos_get_packet_index",
        "task-packet": "aicos_get_task_packet",
        "status-items": "aicos_get_status_items",
        "workstream-index": "aicos_get_workstream_index",
        "context-registry": "aicos_get_context_registry",
        "project-registry": "aicos_get_project_registry",
        "feedback-digest": "aicos_get_feedback_digest",
        "project-health": "aicos_get_project_health",
        "query-project-context": "aicos_query_project_context",
    }
    arguments: dict[str, Any] = {"actor": args.actor, "scope": args.scope}
    if args.packet_id:
        arguments["packet_id"] = args.packet_id
    if getattr(args, "query", ""):
        arguments["query"] = args.query
    if getattr(args, "context_kind", None):
        arguments["context_kinds"] = args.context_kind
    if getattr(args, "project_role", ""):
        arguments["project_role"] = args.project_role
    if getattr(args, "max_results", 0):
        arguments["max_results"] = args.max_results
    if getattr(args, "include_candidate", False):
        arguments["include_candidate"] = True
    if getattr(args, "include_stale", False):
        arguments["include_stale"] = True
    try:
        payload = dispatch_read_surface(surface_map[args.read_surface], arguments)
    except AicosMcpReadError as exc:
        print(json.dumps({"error": {"code": exc.code, "message": exc.message, "details": exc.details}}, indent=2, ensure_ascii=False))
        return 2
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def split_handoff_sections(body: str) -> tuple[str, list[tuple[str, str]], str]:
    pattern = re.compile(r"^## MCP Continuity Update:\s*(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    if not matches:
        return body.rstrip(), [], ""
    prefix = body[: matches[0].start()].rstrip()
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections.append((match.group(1).strip(), body[match.start() : end].strip()))
    return prefix, sections, ""


def block_field(block: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:\s*`?([^`\n]+)`?\s*$", block, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def block_section(block: str, heading: str) -> str:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$", block, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^###\s+", block[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(block)
    return block[start:end].strip()


def compact_handoff(args: argparse.Namespace) -> int:
    scope = args.scope
    if not scope.startswith("projects/") or scope.count("/") != 1:
        print("Scope must use projects/<project-id>.")
        return 2
    project_id = scope.split("/", 1)[1]
    handoff = REPO_ROOT / "brain/projects" / project_id / "working/handoff/current.md"
    if not handoff.exists():
        print(f"Missing handoff: {rel(handoff)}")
        return 2
    body = read_text(handoff)
    prefix, sections, _suffix = split_handoff_sections(body)
    if len(sections) <= args.keep_latest:
        print(f"No compaction needed: {len(sections)} MCP continuity update section(s).")
        return 0
    old_sections = sections[: -args.keep_latest] if args.keep_latest else sections
    kept_sections = sections[-args.keep_latest :] if args.keep_latest else []
    digest_lines = [
        "## MCP Continuity Digest",
        "",
        f"Compacted at: `{now_iso()}`",
        f"Compacted sections: `{len(old_sections)}`",
        "",
        "This digest summarizes older MCP continuity update blocks. Detailed old",
        "blocks were removed from the hot handoff path to keep startup context",
        "bounded. Current project state remains in working/status-items,",
        "working/task-state, current-state, and current-direction.",
        "",
        "### Entries",
        "",
    ]
    for update_id, block in old_sections[-args.digest_limit :]:
        summary = first_paragraph(block_section(block, "Summary")) or block_field(block, "Summary")
        next_step = first_paragraph(block_section(block, "Next Step")) or block_field(block, "Next Step")
        work_lane = block_field(block, "Work lane") or "unknown"
        written_at = block_field(block, "Written at") or "unknown"
        actor = block_field(block, "Agent family") or block_field(block, "Actor role") or "unknown"
        digest_lines.extend(
            [
                f"- `{update_id}` at `{written_at}` by `{actor}` lane `{work_lane}`:",
                f"  {summary[:260] if summary else 'No summary captured.'}",
            ]
        )
        if next_step:
            digest_lines.append(f"  Next: {next_step[:220]}")
    if len(old_sections) > args.digest_limit:
        digest_lines.extend(["", f"Older omitted entries: `{len(old_sections) - args.digest_limit}`"])
    digest = "\n".join(digest_lines).rstrip()
    new_body_parts = [prefix, digest, *[block for _id, block in kept_sections]]
    new_body = "\n\n".join(part.strip() for part in new_body_parts if part.strip()) + "\n"
    if args.dry_run:
        print(json.dumps({"path": rel(handoff), "would_compact": len(old_sections), "would_keep": len(kept_sections)}, indent=2))
        return 0
    write_text(handoff, new_body)
    print(json.dumps({"path": rel(handoff), "compacted": len(old_sections), "kept_latest": len(kept_sections)}, indent=2))
    return 0


def mcp_write(args: argparse.Namespace) -> int:
    tool_map = {
        "record-checkpoint": "aicos_record_checkpoint",
        "task-update": "aicos_write_task_update",
        "handoff-update": "aicos_write_handoff_update",
        "status-item": "aicos_update_status_item",
        "artifact-ref": "aicos_register_artifact_ref",
        "feedback": "aicos_record_feedback",
    }
    try:
        arguments = json.loads(args.payload)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": {"code": "invalid_json", "message": str(exc)}}, indent=2, ensure_ascii=False))
        return 2
    if not isinstance(arguments, dict):
        print(json.dumps({"error": {"code": "invalid_payload", "message": "payload must be a JSON object"}}, indent=2, ensure_ascii=False))
        return 2
    try:
        payload = dispatch_write_tool(tool_map[args.write_tool], arguments)
    except AicosMcpWriteError as exc:
        print(json.dumps({"error": {"code": exc.code, "message": exc.message, "details": exc.details}}, indent=2, ensure_ascii=False))
        return 2
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def mcp_template(args: argparse.Namespace) -> int:
    work_type = args.work_type
    work_lane = args.work_lane
    execution_context = args.execution_context
    payload: dict[str, Any] = {
        "mcp_contract_ack": "mcp-v0.6-write-contract-ack",
        "scope": args.scope,
        "actor_role": args.actor_role,
        "agent_family": args.agent_family,
        "agent_instance_id": args.agent_instance_id,
        "work_type": work_type,
        "work_lane": work_lane,
        "execution_context": execution_context,
        "runtime_context": {
            "runtime": args.runtime,
            "mcp_name": args.mcp_name,
            "agent_position": args.agent_position,
            "functional_role": args.functional_role,
        },
    }
    if args.actor_role.startswith("A2-"):
        payload["runtime_identity_map"] = {
            "identity_current": {
                "runtime": args.runtime,
                "mcp_name": args.mcp_name,
                "project_scope": args.scope,
                "agent_position": args.agent_position,
                "actor_role": args.actor_role,
                "functional_role": args.functional_role or "AICOS runtime maintainer",
            }
        }
    if work_type == "code":
        payload["worktree_path"] = args.worktree_path or "/absolute/path/to/worktree"
        payload["work_branch"] = args.work_branch or "branch-name"

    if args.template_kind == "checkpoint":
        payload.update(
            {
                "checkpoint_type": "artifact",
                "summary": "Short checkpoint summary.",
                "status": "completed",
                "notes": "Optional short note.",
            }
        )
    elif args.template_kind == "task-update":
        payload.update(
            {
                "task_ref": "task-or-packet-id",
                "task_status": "in_progress",
                "what_is_done": "Short progress summary.",
                "next_step": "Immediate next step.",
            }
        )
    elif args.template_kind == "handoff-update":
        payload.update(
            {
                "summary": "Compact continuity summary for the next actor.",
                "status": "ready_for_next",
                "next_step": "Immediate continuation step.",
            }
        )
    elif args.template_kind == "status-item":
        payload.update(
            {
                "item_id": "ITEM-ID",
                "item_type": "open_item",
                "item_status": "open",
                "title": "Short status item title.",
                "summary": "Current state of the item.",
                "next_step": "Remaining action or none.",
            }
        )
    elif args.template_kind == "artifact-ref":
        payload.update(
            {
                "artifact_kind": "note",
                "title": "Artifact title",
                "artifact_ref": "/path/or/url/to/artifact",
                "summary": "Why this artifact matters.",
            }
        )
    elif args.template_kind == "feedback":
        payload.update(
            {
                "feedback_type": "other",
                "severity": "low",
                "title": "Feedback title",
                "summary": "What failed or should improve.",
                "recommendation": "Optional suggested improvement.",
            }
        )
    else:
        print(json.dumps({"error": {"code": "unknown_template_kind", "message": args.template_kind}}, indent=2, ensure_ascii=False))
        return 2

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def mcp_doctor(args: argparse.Namespace) -> int:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    stdio_script = REPO_ROOT / "integrations/local-mcp-bridge/aicos_mcp_stdio.py"
    add("repo_root", (REPO_ROOT / "AGENTS.md").exists(), str(REPO_ROOT))
    add("stdio_script", stdio_script.exists(), rel(stdio_script) if stdio_script.exists() else str(stdio_script))
    add("python", bool(sys.executable), sys.executable)

    if args.mode in {"all", "stdio"} and stdio_script.exists():
        try:
            probe = subprocess.run(
                [sys.executable, str(stdio_script)],
                input='{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}\n',
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
            )
            ok = probe.returncode == 0 and "aicos_get_startup_bundle" in probe.stdout and "aicos_update_status_item" in probe.stdout
            detail = "tools/list ok" if ok else (probe.stderr.strip() or probe.stdout[:500] or f"returncode={probe.returncode}")
        except subprocess.TimeoutExpired as exc:
            ok = False
            detail = f"timeout: {exc}"
        add("stdio_tools_list", ok, detail)

    if args.mode in {"all", "daemon"}:
        request = urllib.request.Request(args.daemon_url.rstrip("/") + "/health")
        if args.token:
            request.add_header("Authorization", f"Bearer {args.token}")
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                body = response.read().decode("utf-8")
            parsed = json.loads(body)
            add("daemon_health", parsed.get("status") == "ok", body)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            add("daemon_health", False, str(exc))

    result = {
        "schema_version": "0.1",
        "kind": "aicos.mcp_doctor",
        "repo_root": str(REPO_ROOT),
        "mode": args.mode,
        "daemon_url": args.daemon_url,
        "checks": checks,
        "ok": all(item["ok"] for item in checks),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


def mcp_token_list(args: argparse.Namespace) -> int:
    env_values = load_daemon_env_file()
    primary_label = env_values.get("AICOS_DAEMON_PRIMARY_TOKEN_LABEL", "default") or "default"
    tokens: list[dict[str, str]] = []
    primary = env_values.get("AICOS_DAEMON_TOKEN", "")
    if primary:
        tokens.append({"label": primary_label, "token": primary, "source": "primary"})
    for label, token in parse_extra_tokens(env_values.get("AICOS_DAEMON_EXTRA_TOKENS", "")).items():
        tokens.append({"label": label, "token": token, "source": "extra"})

    internal_labels = csv_set(env_values.get("AICOS_DAEMON_INTERNAL_TOKEN_LABELS", ""))
    policy_raw = env_values.get("AICOS_DAEMON_TOKEN_SCOPE_POLICY", "")
    try:
        scope_policy = json.loads(policy_raw) if policy_raw else {}
    except json.JSONDecodeError:
        scope_policy = {"_parse_error": policy_raw}
    registry = load_token_registry()
    registry_by_label = {str(item.get("label")): item for item in registry.get("entries", []) if isinstance(item, dict)}

    rows: list[dict[str, Any]] = []
    for item in tokens:
        label = item["label"]
        explicit_policy = scope_policy.get(label) if isinstance(scope_policy, dict) else None
        if explicit_policy:
            rights = f"policy={json.dumps(explicit_policy, ensure_ascii=False)}"
        elif label in internal_labels:
            rights = "read=all; write=all including protected projects/aicos"
        else:
            rights = "read=all; write=normal project scopes; denied protected projects/aicos"
        reg = registry_by_label.get(label, {})
        rows.append({
            "label": label,
            "token": item["token"] if args.show_tokens else masked_token(item["token"]),
            "source": item["source"],
            "assigned_to": reg.get("assigned_to"),
            "rights": rights,
            "notes": reg.get("notes", ""),
        })

    if args.format == "json":
        print(json.dumps({
            "env_file": str(daemon_env_file()),
            "registry": str(token_registry_path()),
            "internal_token_labels": sorted(internal_labels),
            "scope_policy": scope_policy,
            "tokens": rows,
        }, indent=2, ensure_ascii=False))
        return 0

    print("AICOS MCP tokens")
    print(f"- env: {daemon_env_file()}")
    print(f"- registry: {token_registry_path()}")
    print(f"- internal labels: {', '.join(sorted(internal_labels)) or '(none)'}")
    for row in rows:
        print(f"- {row['label']} | {row['token']} | {row['source']} | assigned_to={row['assigned_to'] or '-'}")
        print(f"  rights: {row['rights']}")
        if row["notes"]:
            print(f"  notes: {row['notes']}")
    return 0


def mcp_token_create(args: argparse.Namespace) -> int:
    label = args.label.strip()
    if not label or not re.fullmatch(r"[A-Za-z0-9_.-]+", label):
        print("label must contain only letters, numbers, underscore, dot, or hyphen")
        return 2
    token = args.token.strip() if args.token else secrets.token_urlsafe(32)
    env_values = load_daemon_env_file()
    primary_label = env_values.get("AICOS_DAEMON_PRIMARY_TOKEN_LABEL", "default") or "default"
    if label == primary_label and env_values.get("AICOS_DAEMON_TOKEN") and not args.force:
        print(f"token label already exists as primary: {label}; choose another label or use --force")
        return 2
    extra_tokens = parse_extra_tokens(env_values.get("AICOS_DAEMON_EXTRA_TOKENS", ""))
    if label in extra_tokens and not args.force:
        print(f"token label already exists: {label}; use --force to replace")
        return 2
    extra_tokens[label] = token
    env_values["AICOS_DAEMON_EXTRA_TOKENS"] = render_extra_tokens(extra_tokens)

    internal_labels = csv_set(env_values.get("AICOS_DAEMON_INTERNAL_TOKEN_LABELS", ""))
    if args.internal:
        internal_labels.add(label)
    if args.external:
        internal_labels.discard(label)
    env_values["AICOS_DAEMON_INTERNAL_TOKEN_LABELS"] = render_csv(internal_labels)

    if args.read_scope or args.write_scope:
        policy_raw = env_values.get("AICOS_DAEMON_TOKEN_SCOPE_POLICY", "")
        try:
            policy = json.loads(policy_raw) if policy_raw else {}
        except json.JSONDecodeError:
            print("AICOS_DAEMON_TOKEN_SCOPE_POLICY is invalid JSON; fix it before adding scoped grants")
            return 2
        label_policy = dict(policy.get(label, {}))
        if args.read_scope:
            label_policy["read"] = args.read_scope
        if args.write_scope:
            label_policy["write"] = args.write_scope
        policy[label] = label_policy
        env_values["AICOS_DAEMON_TOKEN_SCOPE_POLICY"] = json.dumps(policy, ensure_ascii=False, separators=(",", ":"))

    env_path = write_daemon_env_file(env_values)
    registry = load_token_registry()
    entries = [item for item in registry.get("entries", []) if isinstance(item, dict) and item.get("label") != label]
    notes = args.notes.strip()
    if not notes:
        notes = "AICOS maintainer access token. Access role label, not an agent family." if args.internal else "External/client access token. Not protected AICOS maintainer authority by default."
    entries.append({
        "label": label,
        "token": token,
        "assigned_to": args.assigned_to.strip() or None,
        "notes": notes,
    })
    registry["entries"] = entries
    registry_path = write_token_registry(registry)

    print("Created AICOS MCP token")
    print(f"- label: {label}")
    print(f"- token: {token}")
    print(f"- env: {env_path}")
    print(f"- registry: {registry_path}")
    print(f"- internal: {'yes' if label in internal_labels else 'no'}")
    if args.read_scope or args.write_scope:
        print(f"- read_scope: {args.read_scope or 'default'}")
        print(f"- write_scope: {args.write_scope or 'default'}")
    print("")
    print("Restart daemon to activate:")
    print("launchctl kickstart -k gui/$(id -u)/ai.aicos.mcp-daemon")
    return 0


def context_registry(args: argparse.Namespace) -> int:
    payload = registry_payload(scope=args.scope, limit=args.max_results, project_role=args.project_role)
    if args.write:
        scope_slug = (args.scope or "all").replace("/", "__")
        out_root = REPO_ROOT / "serving/context-registry"
        json_path = out_root / f"{scope_slug}.json"
        md_path = out_root / f"{scope_slug}.md"
        write_json(json_path, payload)
        write_text(md_path, render_registry_markdown(payload))
        print(rel(md_path))
        print(rel(json_path))
        return 0
    if args.format == "markdown":
        print(render_registry_markdown(payload), end="")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def install_cli(args: argparse.Namespace) -> int:
    bin_dir = Path(args.bin_dir).expanduser()
    target = bin_dir / args.name
    source = REPO_ROOT / "aicos"
    if not source.exists():
        print(f"missing CLI wrapper: {source}")
        return 2
    if args.dry_run:
        print("Install target:")
        print(f"- source: {source}")
        print(f"- symlink: {target}")
        print("")
        print("This creates a symlink so `aicos ...` works outside the repo.")
        print(f"Ensure {bin_dir} is on PATH.")
        return 0
    bin_dir.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if not args.force:
            print(f"target already exists: {target}")
            print("Use --force to replace it.")
            return 1
        target.unlink()
    target.symlink_to(source)
    print(f"Installed: {target} -> {source}")
    print(f"Ensure {bin_dir} is on PATH.")
    return 0


def audit_log_path() -> Path:
    return Path(os.environ.get("AICOS_DAEMON_AUDIT_LOG", str(Path.home() / "Library/Logs/aicos/mcp-audit.jsonl"))).expanduser()


def audit_recent(args: argparse.Namespace) -> int:
    path = audit_log_path()
    if not path.exists():
        print(f"missing audit log: {path}")
        return 1
    try:
        limit = max(1, min(int(args.limit), 200))
    except ValueError:
        print("limit must be an integer")
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    events: list[dict[str, Any]] = []
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if args.token_label and event.get("token_label") != args.token_label:
            continue
        if args.agent_family and event.get("agent_family") != args.agent_family:
            continue
        if args.agent_instance_id and event.get("agent_instance_id") != args.agent_instance_id:
            continue
        if args.scope and event.get("scope") != args.scope:
            continue
        if args.work_lane and event.get("work_lane") != args.work_lane:
            continue
        if args.status and event.get("status") != args.status:
            continue
        if args.error_contains and args.error_contains.lower() not in str(event.get("error", "")).lower():
            continue
        events.append(event)
        if len(events) >= limit:
            break
    events.reverse()
    if args.format == "json":
        print(json.dumps({"path": str(path), "count": len(events), "events": events}, indent=2, ensure_ascii=False))
        return 0
    print(f"AICOS audit recent")
    print(f"- path: {path}")
    print(f"- matched: {len(events)}")
    for event in events:
        summary = [
            event.get("ts", ""),
            event.get("token_label", "none"),
            event.get("http_method", ""),
            event.get("path", ""),
            event.get("status", ""),
        ]
        tool = event.get("tool_name")
        if tool:
            summary.append(str(tool))
        scope = event.get("scope")
        if scope:
            summary.append(str(scope))
        agent_family = event.get("agent_family")
        if agent_family:
            summary.append(str(agent_family))
        agent_instance_id = event.get("agent_instance_id")
        if agent_instance_id:
            summary.append(str(agent_instance_id))
        error = event.get("error")
        print("- " + " | ".join(part for part in summary if part))
        if error:
            print(f"  error: {error}")
    return 0


def audit_summary(args: argparse.Namespace) -> int:
    path = audit_log_path()
    if not path.exists():
        print(f"missing audit log: {path}")
        return 1
    try:
        limit = max(1, min(int(args.limit), 5000))
    except ValueError:
        print("limit must be an integer")
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    recent_lines = lines[-limit:]
    events: list[dict[str, Any]] = []
    for line in recent_lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        events.append(event)

    def tally(field: str) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for event in events:
            key = str(event.get(field) or "none")
            counts[key] = counts.get(key, 0) + 1
        return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    error_counts: dict[str, int] = {}
    for event in events:
        error = str(event.get("error") or "").strip()
        if not error:
            continue
        error_counts[error] = error_counts.get(error, 0) + 1

    payload = {
        "path": str(path),
        "sample_size": len(events),
        "status_counts": tally("status"),
        "token_label_counts": tally("token_label"),
        "tool_name_counts": tally("tool_name"),
        "scope_counts": tally("scope"),
        "error_counts": sorted(error_counts.items(), key=lambda item: (-item[1], item[0])),
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    print("AICOS audit summary")
    print(f"- path: {path}")
    print(f"- sampled events: {len(events)}")
    for label, rows in (
        ("status", payload["status_counts"]),
        ("token_label", payload["token_label_counts"]),
        ("tool_name", payload["tool_name_counts"]),
        ("scope", payload["scope_counts"]),
        ("error", payload["error_counts"]),
    ):
        print(f"- {label}:")
        if not rows:
            print("  - none")
            continue
        for key, count in rows[:10]:
            print(f"  - {key}: {count}")
    return 0


def audit_relations(args: argparse.Namespace) -> int:
    """Audit Trace Refs relation hygiene for markdown truth under brain/."""
    files, lane_counts = collect_brain_sync_files()
    repo_root = REPO_ROOT
    scope_filter = (args.scope or "").strip()

    def in_scope(path: Path) -> bool:
        if not scope_filter:
            return True
        if scope_filter == "shared":
            rel_str = str(path.relative_to(repo_root))
            return rel_str.startswith("brain/shared/")
        if scope_filter.startswith("projects/"):
            project_id = scope_filter.split("/", 1)[1]
            rel_str = str(path.relative_to(repo_root))
            return rel_str.startswith(f"brain/projects/{project_id}/")
        return False

    files = [p for p in files if in_scope(p)]

    with_trace = 0
    source_ref_total = 0
    artifact_ref_total = 0
    broken_source_refs: list[dict[str, str]] = []
    absolute_or_url_source_refs: list[dict[str, str]] = []
    nodes: list[dict[str, Any]] = []

    for path in files:
        rel_path = str(path.relative_to(repo_root))
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        trace = parse_trace_refs(text)
        if not trace.source_refs and not trace.artifact_refs:
            continue
        with_trace += 1
        source_ref_total += len(trace.source_refs)
        artifact_ref_total += len(trace.artifact_refs)

        outgoing: list[dict[str, str]] = []
        for ref in trace.source_refs:
            ref_str = ref.strip()
            if not ref_str:
                continue
            if ref_str.startswith(("http://", "https://", "/", "~/")):
                absolute_or_url_source_refs.append({"from_ref": rel_path, "to_ref": ref_str})
            else:
                if not repo_path_exists(repo_root, ref_str):
                    broken_source_refs.append({"from_ref": rel_path, "to_ref": ref_str})
            outgoing.append({"relation_type": "evidenced_by", "to_ref": ref_str})
        for ref in trace.artifact_refs:
            ref_str = ref.strip()
            if not ref_str:
                continue
            outgoing.append({"relation_type": "artifact_ref", "to_ref": ref_str})

        nodes.append({"source_ref": rel_path, "outgoing": outgoing})

    payload: dict[str, Any] = {
        "schema_version": "0.1",
        "kind": "aicos.audit.relations",
        "scope": scope_filter or "all",
        "checked_at": now_iso(),
        "stats": {
            "files_scanned": len(files),
            "files_with_trace_refs": with_trace,
            "source_refs_total": source_ref_total,
            "artifact_refs_total": artifact_ref_total,
            "broken_source_refs": len(broken_source_refs),
            "absolute_or_url_source_refs": len(absolute_or_url_source_refs),
            "lane_counts": lane_counts,
        },
        "broken_source_refs": broken_source_refs[:50],
        "absolute_or_url_source_refs": absolute_or_url_source_refs[:50],
        "derived_index": {"nodes": nodes},
        "boundary": "Derived adjacency from explicit Trace Refs only. Markdown remains truth.",
    }

    if args.write:
        runtime_dir = REPO_ROOT / ".runtime-home/aicos"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        suffix = scope_filter.replace("/", "__") if scope_filter else "all"
        out_path = runtime_dir / f"relations-index__{suffix}.json"
        write_json(out_path, payload)
        payload["written_to"] = rel(out_path)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1 if broken_source_refs else 0

    print("AICOS relation hygiene (Trace Refs)")
    print(f"- scope: {payload['scope']}")
    print(f"- files scanned: {payload['stats']['files_scanned']}")
    print(f"- files w/ Trace Refs: {payload['stats']['files_with_trace_refs']}")
    print(f"- source refs: {payload['stats']['source_refs_total']} (broken: {payload['stats']['broken_source_refs']})")
    print(f"- artifact refs: {payload['stats']['artifact_refs_total']}")
    if payload.get("written_to"):
        print(f"- wrote derived index: {payload['written_to']}")
    if broken_source_refs:
        print("")
        print("Broken source_ref examples:")
        for item in broken_source_refs[:10]:
            print(f"- {item['from_ref']} -> {item['to_ref']}")
    if absolute_or_url_source_refs:
        print("")
        print("Absolute/URL source_ref examples (prefer repo-relative):")
        for item in absolute_or_url_source_refs[:10]:
            print(f"- {item['from_ref']} -> {item['to_ref']}")
    return 1 if broken_source_refs else 0


def feedback_summary(args: argparse.Namespace) -> int:
    root = REPO_ROOT / "brain/projects"
    entries: list[dict[str, str]] = []
    for path in sorted(root.glob("*/working/feedback/*.md")):
        body = read_text(path)
        project_id = path.parts[-4]
        entry = {
            "project_id": project_id,
            "path": rel(path),
            "title": markdown_title(body, path.stem),
            "feedback_type": markdown_field(body, "Feedback type"),
            "severity": markdown_field(body, "Severity"),
            "status": markdown_field(body, "Status"),
            "agent_family": markdown_field(body, "Agent family"),
            "work_lane": markdown_field(body, "Work lane"),
            "summary": compact_text(markdown_section(body, "Summary"), limit=220),
            "last_updated_at": markdown_field(body, "Last updated at") or markdown_field(body, "Written at"),
        }
        if args.scope and f"projects/{project_id}" != args.scope:
            continue
        entries.append(entry)

    def tally(field: str) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for entry in entries:
            key = str(entry.get(field) or "none")
            counts[key] = counts.get(key, 0) + 1
        return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    payload = {
        "count": len(entries),
        "scope_filter": args.scope,
        "feedback_type_counts": tally("feedback_type"),
        "severity_counts": tally("severity"),
        "project_counts": tally("project_id"),
        "agent_family_counts": tally("agent_family"),
        "recent_entries": sorted(entries, key=lambda item: item.get("last_updated_at", ""), reverse=True)[: min(max(int(args.limit), 1), 20)],
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    print("AICOS feedback summary")
    print(f"- matched feedback items: {payload['count']}")
    if args.scope:
        print(f"- scope filter: {args.scope}")
    for label, rows in (
        ("feedback_type", payload["feedback_type_counts"]),
        ("severity", payload["severity_counts"]),
        ("project", payload["project_counts"]),
        ("agent_family", payload["agent_family_counts"]),
    ):
        print(f"- {label}:")
        if not rows:
            print("  - none")
            continue
        for key, count in rows[:10]:
            print(f"  - {key}: {count}")
    print("- recent:")
    if not payload["recent_entries"]:
        print("  - none")
    for entry in payload["recent_entries"]:
        print(f"  - {entry['last_updated_at']} | {entry['project_id']} | {entry['feedback_type'] or 'none'} | {entry['severity'] or 'none'} | {entry['title']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aicos")
    sub = parser.add_subparsers(dest="command", required=True)

    capsule = sub.add_parser("capsule")
    capsule_sub = capsule.add_subparsers(dest="capsule_command", required=True)
    capsule_build = capsule_sub.add_parser("build")
    capsule_build.add_argument("capsule_type", choices=["company", "workspace", "project", "branch", "actor"])
    capsule_build.add_argument("values", nargs="+")
    capsule_build.set_defaults(func=build_capsule)

    branch = sub.add_parser("branch")
    branch_sub = branch.add_subparsers(dest="branch_command", required=True)
    branch_compare_parser = branch_sub.add_parser("compare")
    branch_compare_parser.add_argument("project_id")
    branch_compare_parser.add_argument("branch_a")
    branch_compare_parser.add_argument("branch_b")
    branch_compare_parser.set_defaults(func=branch_compare)

    option = sub.add_parser("option")
    option_sub = option.add_subparsers(dest="option_command", required=True)
    option_generate_parser = option_sub.add_parser("generate")
    option_generate_parser.add_argument("project_id")
    option_generate_parser.add_argument("blocker_id")
    option_generate_parser.set_defaults(func=option_generate)
    option_choose_parser = option_sub.add_parser("choose")
    option_choose_parser.add_argument("project_id")
    option_choose_parser.add_argument("blocker_id")
    option_choose_parser.add_argument("option_id")
    option_choose_parser.add_argument("--actor", default="manager")
    option_choose_parser.add_argument("--reason", default="")
    option_choose_parser.set_defaults(func=option_choose)

    promote_parser = sub.add_parser("promote")
    promote_sub = promote_parser.add_subparsers(dest="promotion_lane", required=True)
    for lane in ["evidence-to-working", "working-to-canonical"]:
        lane_parser = promote_sub.add_parser(lane)
        lane_parser.add_argument("path")
        lane_parser.set_defaults(func=promote)

    validate = sub.add_parser("validate")
    validate_sub = validate.add_subparsers(dest="validate_target", required=True)
    validate_capsule_parser = validate_sub.add_parser("capsule")
    validate_capsule_parser.add_argument("path")
    validate_capsule_parser.set_defaults(func=validate_capsule)
    validate_branch_parser = validate_sub.add_parser("branch")
    validate_branch_parser.add_argument("path")
    validate_branch_parser.set_defaults(func=validate_branch)

    context = sub.add_parser("context")
    context_sub = context.add_subparsers(dest="context_command", required=True)
    context_start_parser = context_sub.add_parser("start")
    context_start_parser.add_argument("actor")
    context_start_parser.add_argument("scope", nargs="?", default="projects/aicos")
    context_start_parser.set_defaults(func=context_start)
    context_registry_parser = context_sub.add_parser("registry")
    context_registry_parser.add_argument("--scope", default="")
    context_registry_parser.add_argument("--max-results", type=int, default=200)
    context_registry_parser.add_argument("--project-role", default="")
    context_registry_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    context_registry_parser.add_argument("--write", action="store_true")
    context_registry_parser.set_defaults(func=context_registry)

    sync = sub.add_parser("sync")
    sync_sub = sync.add_subparsers(dest="sync_target", required=True)
    sync_brain_parser = sync_sub.add_parser("brain")
    sync_mode = sync_brain_parser.add_mutually_exclusive_group()
    sync_mode.add_argument("--text-only", action="store_true", help="Import text only; skip embeddings")
    sync_mode.add_argument("--full", action="store_true", help="Request full GBrain import including embeddings")
    sync_brain_parser.set_defaults(func=sync_brain)

    brain = sub.add_parser("brain")
    brain_sub = brain.add_subparsers(dest="brain_command", required=True)
    brain_status_parser = brain_sub.add_parser("status")
    brain_status_parser.add_argument("--format", choices=["text", "json"], default="text")
    brain_status_parser.set_defaults(func=brain_status)

    audit = sub.add_parser("audit")
    audit_sub = audit.add_subparsers(dest="audit_command", required=True)
    audit_recent_parser = audit_sub.add_parser("recent")
    audit_recent_parser.add_argument("--token-label", default="")
    audit_recent_parser.add_argument("--agent-family", default="")
    audit_recent_parser.add_argument("--agent-instance-id", default="")
    audit_recent_parser.add_argument("--scope", default="")
    audit_recent_parser.add_argument("--work-lane", default="")
    audit_recent_parser.add_argument("--status", default="")
    audit_recent_parser.add_argument("--error-contains", default="")
    audit_recent_parser.add_argument("--limit", default="20")
    audit_recent_parser.add_argument("--format", choices=["text", "json"], default="text")
    audit_recent_parser.set_defaults(func=audit_recent)
    audit_summary_parser = audit_sub.add_parser("summary")
    audit_summary_parser.add_argument("--limit", default="200")
    audit_summary_parser.add_argument("--format", choices=["text", "json"], default="text")
    audit_summary_parser.set_defaults(func=audit_summary)
    audit_relations_parser = audit_sub.add_parser("relations")
    audit_relations_parser.add_argument("--scope", default="", help="Limit to a scope like projects/aicos or shared.")
    audit_relations_parser.add_argument("--write", action="store_true", help="Write derived relation index under .runtime-home/aicos/.")
    audit_relations_parser.add_argument("--format", choices=["text", "json"], default="text")
    audit_relations_parser.set_defaults(func=audit_relations)

    feedback = sub.add_parser("feedback")
    feedback_sub = feedback.add_subparsers(dest="feedback_command", required=True)
    feedback_summary_parser = feedback_sub.add_parser("summary")
    feedback_summary_parser.add_argument("--scope", default="")
    feedback_summary_parser.add_argument("--limit", default="10")
    feedback_summary_parser.add_argument("--format", choices=["text", "json"], default="text")
    feedback_summary_parser.set_defaults(func=feedback_summary)

    install = sub.add_parser("install")
    install_sub = install.add_subparsers(dest="install_target", required=True)
    install_cli_parser = install_sub.add_parser("cli")
    install_cli_parser.add_argument("--bin-dir", default="~/.local/bin")
    install_cli_parser.add_argument("--name", default="aicos")
    install_cli_parser.add_argument("--force", action="store_true")
    install_cli_parser.add_argument("--dry-run", action="store_true")
    install_cli_parser.set_defaults(func=install_cli)

    mcp = sub.add_parser("mcp")
    mcp_sub = mcp.add_subparsers(dest="mcp_command", required=True)
    mcp_read_parser = mcp_sub.add_parser("read")
    mcp_read_parser.add_argument("read_surface", choices=["startup-bundle", "handoff-current", "packet-index", "task-packet", "status-items", "workstream-index", "context-registry", "project-registry", "feedback-digest", "project-health", "query-project-context"])
    mcp_read_parser.add_argument("--actor", default="A1")
    mcp_read_parser.add_argument("--scope", default="projects/aicos")
    mcp_read_parser.add_argument("--packet-id", default="")
    mcp_read_parser.add_argument("--query", default="")
    mcp_read_parser.add_argument("--context-kind", action="append", default=[])
    mcp_read_parser.add_argument("--project-role", default="")
    mcp_read_parser.add_argument("--max-results", type=int, default=0)
    mcp_read_parser.add_argument("--include-candidate", action="store_true")
    mcp_read_parser.add_argument("--include-stale", action="store_true")
    mcp_read_parser.set_defaults(func=mcp_read)
    mcp_write_parser = mcp_sub.add_parser("write")
    mcp_write_parser.add_argument("write_tool", choices=["record-checkpoint", "task-update", "handoff-update", "status-item", "artifact-ref", "feedback"])
    mcp_write_parser.add_argument("payload", help="JSON object payload for the semantic write tool")
    mcp_write_parser.set_defaults(func=mcp_write)
    mcp_template_parser = mcp_sub.add_parser("template")
    mcp_template_parser.add_argument("template_kind", choices=["checkpoint", "task-update", "handoff-update", "status-item", "artifact-ref", "feedback"])
    mcp_template_parser.add_argument("--scope", default="projects/aicos")
    mcp_template_parser.add_argument("--actor-role", default="A1")
    mcp_template_parser.add_argument("--agent-family", default="openclaw")
    mcp_template_parser.add_argument("--agent-instance-id", default="agent-session-01")
    mcp_template_parser.add_argument("--work-type", default="ops")
    mcp_template_parser.add_argument("--work-lane", default="intake")
    mcp_template_parser.add_argument("--execution-context", default="cli")
    mcp_template_parser.add_argument("--runtime", default="private-local-aicos")
    mcp_template_parser.add_argument("--mcp-name", default="aicos_local_private")
    mcp_template_parser.add_argument("--agent-position", choices=["external_agent", "internal_agent", "human_operator", "system"], default="external_agent")
    mcp_template_parser.add_argument("--functional-role", default="")
    mcp_template_parser.add_argument("--worktree-path", default="")
    mcp_template_parser.add_argument("--work-branch", default="")
    mcp_template_parser.set_defaults(func=mcp_template)
    mcp_doctor_parser = mcp_sub.add_parser("doctor")
    mcp_doctor_parser.add_argument("--mode", choices=["stdio", "daemon", "all"], default="stdio")
    mcp_doctor_parser.add_argument("--daemon-url", default="http://127.0.0.1:8000")
    mcp_doctor_parser.add_argument("--token", default="")
    mcp_doctor_parser.set_defaults(func=mcp_doctor)
    mcp_token_parser = mcp_sub.add_parser("token")
    mcp_token_sub = mcp_token_parser.add_subparsers(dest="mcp_token_command", required=True)
    mcp_token_create_parser = mcp_token_sub.add_parser("create")
    mcp_token_create_parser.add_argument("label", help="Access label, e.g. antigravity-2 or a2-core-c-2.")
    mcp_token_create_parser.add_argument("--assigned-to", default="", help="Human-readable assignment note.")
    mcp_token_create_parser.add_argument("--notes", default="", help="Registry note.")
    mcp_token_create_parser.add_argument("--internal", action="store_true", help="Grant protected AICOS maintainer write authority.")
    mcp_token_create_parser.add_argument("--external", action="store_true", help="Ensure the label is not in internal maintainer labels.")
    mcp_token_create_parser.add_argument("--read-scope", action="append", default=[], help="Explicit read scope pattern; repeatable.")
    mcp_token_create_parser.add_argument("--write-scope", action="append", default=[], help="Explicit write scope pattern; repeatable.")
    mcp_token_create_parser.add_argument("--token", default="", help="Use a provided token instead of generating one.")
    mcp_token_create_parser.add_argument("--force", action="store_true", help="Replace an existing extra token label.")
    mcp_token_create_parser.set_defaults(func=mcp_token_create)
    mcp_token_list_parser = mcp_token_sub.add_parser("list")
    mcp_token_list_parser.add_argument("--show-tokens", action="store_true", help="Print full tokens. Avoid sharing output.")
    mcp_token_list_parser.add_argument("--format", choices=["text", "json"], default="text")
    mcp_token_list_parser.set_defaults(func=mcp_token_list)

    compact = sub.add_parser("compact")
    compact_sub = compact.add_subparsers(dest="compact_target", required=True)
    compact_handoff_parser = compact_sub.add_parser("handoff")
    compact_handoff_parser.add_argument("scope")
    compact_handoff_parser.add_argument("--keep-latest", type=int, default=1)
    compact_handoff_parser.add_argument("--digest-limit", type=int, default=20)
    compact_handoff_parser.add_argument("--dry-run", action="store_true")
    compact_handoff_parser.set_defaults(func=compact_handoff)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "capsule" and args.capsule_command == "build":
        expected = {"company": 1, "workspace": 1, "project": 1, "branch": 2, "actor": 2}[args.capsule_type]
        if len(args.values) != expected:
            parser.error(f"capsule build {args.capsule_type} expects {expected} value(s)")
    return args.func(args)
