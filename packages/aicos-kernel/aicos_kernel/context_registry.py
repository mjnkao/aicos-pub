from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import REPO_ROOT, brain_root, repo_rel
from .pg_search.indexer import path_metadata


def rel(path: Path) -> str:
    return repo_rel(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def markdown_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def compact_text(body: str, limit: int = 320) -> str:
    text = re.sub(r"\s+", " ", body).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def first_summary(body: str) -> str:
    lines: list[str] = []
    seen_title = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            seen_title = True
            continue
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("#") or stripped.startswith("|"):
            if seen_title:
                continue
        if stripped.startswith("- ") and not lines:
            return compact_text(stripped)
        lines.append(stripped)
        if len(" ".join(lines)) >= 320:
            break
    return compact_text(" ".join(lines))


def registry_roots() -> list[Path]:
    return [
        brain_root(),
        REPO_ROOT / "agent-repo",
        REPO_ROOT / "packages/aicos-kernel/contracts",
    ]


def collect_context_registry(scope: str = "", limit: int = 500, project_role: str = "") -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for root in registry_roots():
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if path in seen:
                continue
            seen.add(path)
            meta = path_metadata(path, REPO_ROOT)
            if meta is None:
                continue
            if scope and meta["scope"] not in {scope, "shared"}:
                continue
            role_tags = list(meta["role_tags"])
            if project_role and "all" not in role_tags and project_role not in role_tags:
                continue
            body = read_text(path)
            stat = path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat()
            entries.append(
                {
                    "scope": meta["scope"],
                    "context_kind": meta["context_kind"],
                    "state": meta["state_tag"],
                    "authority": meta["authority_level"],
                    "authority_mult": meta["authority_mult"],
                    "role_tags": role_tags,
                    "source_ref": meta["source_ref"],
                    "title": markdown_title(body, path.stem),
                    "summary": first_summary(body),
                    "mtime": mtime,
                }
            )
            if len(entries) >= limit:
                return entries
    return entries


def registry_payload(scope: str = "", limit: int = 500, project_role: str = "") -> dict[str, Any]:
    entries = collect_context_registry(scope=scope, limit=limit, project_role=project_role)
    counts: dict[str, int] = {}
    for entry in entries:
        key = f"{entry['scope']}::{entry['context_kind']}"
        counts[key] = counts.get(key, 0) + 1
    return {
        "schema_version": "0.1",
        "kind": "aicos.context_registry",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope_filter": scope or "all",
        "project_role_filter": project_role or "any",
        "entry_count": len(entries),
        "counts": counts,
        "entries": entries,
        "boundary": "Registry metadata is an index over AICOS source files. It is not a replacement truth store.",
    }


def render_registry_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# AICOS Context Registry",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Scope filter: `{payload['scope_filter']}`",
        f"Entry count: `{payload['entry_count']}`",
        "",
        "This registry is metadata over context sources. It helps query/routing;",
        "it does not promote or replace source truth.",
        "",
        "## Entries",
        "",
    ]
    for entry in payload["entries"]:
        lines.extend(
            [
                f"### {entry['source_ref']}",
                "",
                f"- scope: `{entry['scope']}`",
                f"- context_kind: `{entry['context_kind']}`",
                f"- state: `{entry['state']}`",
                f"- authority: `{entry['authority']}`",
                f"- role_tags: `{', '.join(entry['role_tags'])}`",
                f"- title: {entry['title']}",
                f"- mtime: `{entry['mtime']}`",
                f"- summary: {entry['summary'] or 'none'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
