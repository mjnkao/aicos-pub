from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TraceRefs:
    source_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    scope_refs: tuple[str, ...] = ()
    session_refs: tuple[str, ...] = ()


_TRACE_HEADER_RE = re.compile(r"^(#{2,3})\s+Trace Refs\s*$", re.IGNORECASE)
_HEADER_RE = re.compile(r"^#{1,6}\s+")

# bullets:
# - source_ref: `path`
# - source_refs:
#   - `path`
# - artifact_refs:
#   - `figma:file/...`
# - scope_refs:
#   - `projects/aicos`
# - session_refs:
#   - `codex-thread-...`
_KEY_BULLET_RE = re.compile(r"^\s*-\s*([a-zA-Z_]+)\s*:\s*(.*)\s*$")
_SUB_BULLET_RE = re.compile(r"^\s{2,}-\s*(.+?)\s*$")
_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _extract_backticked(value: str) -> list[str]:
    hits = [m.group(1).strip() for m in _BACKTICK_RE.finditer(value)]
    if hits:
        return [h for h in hits if h]
    # fallback: allow plain value without backticks
    cleaned = value.strip()
    if not cleaned:
        return []
    # strip common wrappers
    cleaned = cleaned.strip("[]()")
    return [cleaned] if cleaned else []


def parse_trace_refs(markdown_text: str) -> TraceRefs:
    """Parse a `## Trace Refs` block into structured refs.

    This intentionally only reads explicit, human-curated refs.
    """
    lines = markdown_text.splitlines()
    start_idx: int | None = None
    for idx, line in enumerate(lines):
        if _TRACE_HEADER_RE.match(line.strip()):
            start_idx = idx + 1
            break
    if start_idx is None:
        return TraceRefs()

    source_refs: list[str] = []
    artifact_refs: list[str] = []
    scope_refs: list[str] = []
    session_refs: list[str] = []

    current_key: str | None = None
    for raw in lines[start_idx:]:
        line = raw.rstrip("\n")
        stripped = line.strip()

        if not stripped:
            continue
        if _HEADER_RE.match(stripped):
            break

        key_match = _KEY_BULLET_RE.match(line)
        if key_match:
            current_key = key_match.group(1).strip().lower()
            value = key_match.group(2).strip()
            if value:
                items = _extract_backticked(value)
                if current_key in {"source_ref", "source_refs"}:
                    source_refs.extend(items)
                elif current_key in {"artifact_ref", "artifact_refs"}:
                    artifact_refs.extend(items)
                elif current_key in {"scope_ref", "scope_refs"}:
                    scope_refs.extend(items)
                elif current_key in {"session_ref", "session_refs", "thread_ref", "thread_refs"}:
                    session_refs.extend(items)
            continue

        sub_match = _SUB_BULLET_RE.match(line)
        if sub_match and current_key:
            value = sub_match.group(1).strip()
            items = _extract_backticked(value)
            if current_key in {"source_ref", "source_refs"}:
                source_refs.extend(items)
            elif current_key in {"artifact_ref", "artifact_refs"}:
                artifact_refs.extend(items)
            elif current_key in {"scope_ref", "scope_refs"}:
                scope_refs.extend(items)
            elif current_key in {"session_ref", "session_refs", "thread_ref", "thread_refs"}:
                session_refs.extend(items)
            continue

    # preserve order, drop empties, de-dupe
    def dedupe(items: list[str]) -> tuple[str, ...]:
        seen: set[str] = set()
        out: list[str] = []
        for item in items:
            item = item.strip()
            if not item or item in seen:
                continue
            seen.add(item)
            out.append(item)
        return tuple(out)

    return TraceRefs(
        source_refs=dedupe(source_refs),
        artifact_refs=dedupe(artifact_refs),
        scope_refs=dedupe(scope_refs),
        session_refs=dedupe(session_refs),
    )


def repo_path_exists(repo_root: Path, ref: str) -> bool:
    """Return True if ref resolves to a path inside repo_root and exists."""
    ref = ref.strip()
    if not ref or ref.startswith("http://") or ref.startswith("https://"):
        return False
    # Allow file anchors like path.md#heading or path.md#L10
    if "#" in ref:
        ref = ref.split("#", 1)[0].strip()
    if ref.startswith("~/") or ref.startswith("/"):
        return False
    try:
        candidate = (repo_root / ref).resolve()
    except OSError:
        return False
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return False
    return candidate.exists()
