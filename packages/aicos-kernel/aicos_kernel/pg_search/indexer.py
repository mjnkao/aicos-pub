"""AICOS brain/ file indexer → PostgreSQL.

Scans all relevant markdown files under brain/, agent-repo/, and
packages/aicos-kernel/contracts/, maps each to structured metadata
(scope, context_kind, state_tag, authority_level, authority_mult,
role_tags, freshness_label), and upserts into aicos_context_docs.

Skips: backup/, docs/, serving/, node_modules/, .git/.

Usage:
    from aicos_kernel.pg_search.indexer import BrainIndexer
    idx = BrainIndexer(repo_root, conn)
    idx.full_reindex()          # full scan on startup
    idx.reindex_file(path)      # called by file watcher on change
    idx.remove_file(path)       # called by file watcher on delete
"""
from __future__ import annotations

import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .embedding import EmbeddingClient, EmbeddingConfig, approximate_tokens, vector_literal

# -----------------------------------------------------------------------
# Metadata mapping helpers
# -----------------------------------------------------------------------

_SKIP_DIRS = {"backup", "docs", "serving", "node_modules", ".git",
              "__pycache__", ".venv", "venv", "dist", "build"}

_AUTHORITY: dict[str, tuple[str, str, float, list[str]]] = {
    # (state_tag, authority_level, authority_mult, role_tags)
    "canonical":       ("canonical",  "high",   2.0,  ["all"]),
    "policy":          ("canonical",  "high",   2.0,  ["all"]),
    "contract":        ("canonical",  "high",   2.0,  ["all"]),
    "project_registry":("canonical",  "high",   1.9,  ["all", "manager", "architect", "operator"]),
    "current_state":   ("working",    "high",   1.8,  ["all"]),
    "current_direction":("working",   "high",   1.8,  ["all"]),
    "handoff":         ("working",    "high",   1.5,  ["all"]),
    "workstream":      ("working",    "medium", 1.2,  ["all"]),
    "open_items":      ("working",    "medium", 1.1,  ["all"]),
    "open_questions":  ("working",    "medium", 1.1,  ["all"]),
    "status_item":     ("working",    "medium", 1.0,  ["all"]),
    "working":         ("working",    "medium", 1.0,  ["all"]),
    "packet":          ("execution",  "medium", 1.0,  ["developer", "qa", "tech_lead"]),
    "task_state":      ("execution",  "medium", 0.9,  ["developer", "tech_lead"]),
    "artifact_ref":    ("working",    "low",    0.7,  ["all"]),
    "evidence":        ("evidence",   "low",    0.5,  ["researcher", "analyst"]),
}


def _authority(kind: str) -> tuple[str, str, float, list[str]]:
    return _AUTHORITY.get(kind, ("working", "medium", 1.0, ["all"]))


def _freshness(mtime: datetime, state_tag: str) -> str:
    if state_tag == "canonical":
        return "stable"  # canonical docs don't go stale
    now = datetime.now(timezone.utc)
    age_days = (now - mtime).days
    if age_days <= 7:
        return "fresh"
    if age_days <= 21:
        return "aging"
    return "stale"


# -----------------------------------------------------------------------
# Path → metadata mapping
# -----------------------------------------------------------------------

def path_metadata(path: Path, repo_root: Path) -> dict[str, Any] | None:
    """Return metadata dict for this path, or None if path should be skipped."""
    try:
        rel = path.relative_to(repo_root)
    except ValueError:
        return None

    parts = rel.parts
    if not parts:
        return None

    # Skip excluded dirs anywhere in path
    if any(p in _SKIP_DIRS for p in parts):
        return None

    # Skip non-markdown
    if path.suffix != ".md":
        return None

    scope: str | None = None
    kind: str | None = None

    top = parts[0]

    # ----------------------------------------------------------------
    # brain/projects/<project-id>/<layer>/...
    # ----------------------------------------------------------------
    if top == "brain" and len(parts) >= 4 and parts[1] == "projects":
        project_id = parts[2]
        scope = f"projects/{project_id}"
        layer = parts[3]
        fname = path.name

        if layer == "canonical":
            kind = "canonical"

        elif layer == "working":
            if fname == "current-state.md":
                kind = "current_state"
            elif fname in ("current-direction.md", "context-ladder.md",
                           "architecture-working-summary.md",
                           "aicos-architecture-overview.md"):
                kind = "current_direction"
            elif "handoff" in parts:
                kind = "handoff"
            elif "status-items" in parts:
                kind = "status_item"
            elif "task-state" in parts:
                kind = "task_state"
            elif "workstreams" in parts:
                kind = "workstream"
            elif "artifact-refs" in parts:
                kind = "artifact_ref"
            elif fname in ("open-items.md",):
                kind = "open_items"
            elif fname in ("open-questions.md",):
                kind = "open_questions"
            else:
                kind = "working"

        elif layer == "evidence":
            kind = "evidence"

        else:
            return None  # unknown layer — skip

    # ----------------------------------------------------------------
    # brain/shared/policies/...
    # ----------------------------------------------------------------
    elif top == "brain" and len(parts) >= 3 and parts[1] == "shared" and parts[2] == "policies":
        scope = "shared"
        kind = "policy"

    elif top == "brain" and len(parts) >= 3 and parts[1] == "shared" and path.name == "project-registry.md":
        scope = "shared"
        kind = "project_registry"

    # ----------------------------------------------------------------
    # packages/aicos-kernel/contracts/...
    # ----------------------------------------------------------------
    elif top == "packages" and "contracts" in parts:
        scope = "shared"
        kind = "contract"

    # ----------------------------------------------------------------
    # agent-repo/.../task-packets/...
    # ----------------------------------------------------------------
    elif top == "agent-repo" and "task-packets" in parts:
        # Try to extract scope from path like .../task-packets/<project-id>/...
        # parts[idx+1] must be a directory name (project-id), not a .md file
        idx = parts.index("task-packets")
        next_part = parts[idx + 1] if idx + 1 < len(parts) else None
        if next_part and not next_part.endswith(".md"):
            scope = f"projects/{next_part}"
        else:
            scope = "shared"
        kind = "packet"

    else:
        return None  # not a tracked path

    if scope is None or kind is None:
        return None

    state_tag, authority_level, authority_mult, role_tags = _authority(kind)
    return {
        "scope":          scope,
        "context_kind":   kind,
        "state_tag":      state_tag,
        "authority_level": authority_level,
        "authority_mult": authority_mult,
        "role_tags":      role_tags,
        "source_ref":     str(rel),
    }


# -----------------------------------------------------------------------
# Markdown parsing helpers
# -----------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_H1_RE          = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_BLANK_RE       = re.compile(r"\n{3,}")
_SUMMARY_H_RE   = re.compile(r"^##\s+(summary|tóm tắt)\s*$", re.IGNORECASE)
_META_LINE_RE   = re.compile(
    r"^(status|project|scope|write id|written at|last updated at|priority|owner|item type|work lane|task ref|last write id|checkpoint type|feedback type|severity|artifact kind|artifact ref|opened at)\s*:",
    re.IGNORECASE,
)


def _parse_markdown(text: str) -> tuple[str, str, str]:
    """Return (title, summary, body)."""
    body = _FRONTMATTER_RE.sub("", text).strip()
    body = _BLANK_RE.sub("\n\n", body)

    # Title: first H1
    m = _H1_RE.search(body)
    title = m.group(1).strip() if m else ""

    # Summary preference order:
    # 1) First paragraph under "## Summary" / "## Tóm tắt" (common AICOS templates)
    # 2) First non-heading paragraph after H1, skipping metadata key/value lines
    summary = ""
    body_lines = body.splitlines()

    def first_paragraph_from(start: int) -> str:
        collected: list[str] = []
        for raw in body_lines[start:]:
            stripped = raw.strip()
            if not stripped:
                if collected:
                    break
                continue
            if stripped.startswith("#"):
                if collected:
                    break
                continue
            if stripped.startswith("- "):
                if collected:
                    break
                continue
            if _META_LINE_RE.match(stripped):
                if collected:
                    break
                continue
            collected.append(stripped)
            if len(" ".join(collected)) > 400:
                break
        return " ".join(collected)[:400].strip()

    # 1) Summary heading block
    for idx, raw in enumerate(body_lines):
        if _SUMMARY_H_RE.match(raw.strip()):
            summary = first_paragraph_from(idx + 1)
            if summary:
                break

    # 2) Fallback: first paragraph after H1, skipping metadata
    if not summary:
        summary = first_paragraph_from(0)

    return title, summary, body


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _embedding_batch_size() -> int:
    try:
        return max(1, min(128, int(os.environ.get("AICOS_EMBEDDING_BATCH_SIZE", "32"))))
    except ValueError:
        return 32


def _embedding_text(title: str, summary: str, body: str) -> str:
    return "\n\n".join(part for part in [title, summary, body] if part)[:8000]


# -----------------------------------------------------------------------
# BrainIndexer
# -----------------------------------------------------------------------

class BrainIndexer:
    def __init__(
        self,
        repo_root: Path,
        conn,
        embedding_client: EmbeddingClient | None = None,
        embedding_config: EmbeddingConfig | None = None,
        vector_enabled: bool = False,
    ) -> None:
        self.repo_root = repo_root
        self.conn = conn
        self.embedding_client = embedding_client
        self.embedding_config = embedding_config
        self.vector_enabled = vector_enabled

    # -- Public API ------------------------------------------------------

    def full_reindex(self, *, with_embeddings: bool = True) -> dict[str, int]:
        """Scan all tracked files and upsert. Returns stats dict."""
        stats = {"indexed": 0, "skipped": 0, "embedded": 0, "embedding_errors": 0, "errors": 0}
        for path in self._scan_all():
            try:
                updated = self.reindex_file(path, with_embeddings=with_embeddings)
                if updated == "embedded":
                    stats["embedded"] += 1
                elif updated == "embedding_error":
                    stats["embedding_errors"] += 1
                elif updated:
                    stats["indexed"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as exc:
                stats["errors"] += 1
                import sys
                print(f"[indexer] ERROR {path}: {exc}", file=sys.stderr)
        return stats

    def full_embed_stale(self, *, scope: str = "", limit: int | None = None) -> dict[str, int]:
        stats = {
            "embedded": 0,
            "skipped": 0,
            "embedding_errors": 0,
            "docs_considered": 0,
            "docs_submitted": 0,
            "approx_input_chars": 0,
            "approx_input_tokens": 0,
            "batches": 0,
        }
        refs = self.stale_embedding_refs(scope=scope, limit=limit)
        stats["docs_considered"] = len(refs)
        if not refs:
            return stats
        batch_size = _embedding_batch_size()
        for i in range(0, len(refs), batch_size):
            batch = refs[i:i + batch_size]
            result = self._embed_batch(batch)
            for key, value in result.items():
                stats[key] += value
        return stats

    def stale_embedding_refs(self, *, scope: str = "", limit: int | None = None) -> list[tuple[str, str]]:
        if not self.vector_enabled or self.embedding_client is None or self.embedding_config is None:
            return []
        if not self.embedding_config.enabled:
            return []
        where = ["(embedding IS NULL OR embedding_content_hash IS DISTINCT FROM content_hash OR embedding_model IS DISTINCT FROM %s)"]
        params: list[Any] = [self.embedding_config.model]
        if scope:
            where.append("scope = %s")
            params.append(scope)
        sql = f"""
            SELECT source_ref, content_hash
            FROM aicos_context_docs
            WHERE {' AND '.join(where)}
            ORDER BY indexed_at DESC
        """
        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return [(str(row[0]), str(row[1])) for row in cur.fetchall()]

    def reindex_file(self, path: Path, *, with_embeddings: bool = True) -> bool | str:
        """Upsert one file. Returns True/embedded if changed, False if skipped."""
        meta = path_metadata(path, self.repo_root)
        if meta is None:
            return False
        if not path.exists():
            self.remove_file(path)
            return False

        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return False

        chash = _content_hash(text)

        # Skip if unchanged
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT content_hash FROM aicos_context_docs WHERE source_ref = %s",
                (meta["source_ref"],),
            )
            row = cur.fetchone()
            if row and row[0] == chash:
                if not with_embeddings:
                    return False
                return self._ensure_embedding(meta["source_ref"], chash)

        title, summary, body = _parse_markdown(text)
        mtime_ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        freshness = _freshness(mtime_ts, meta["state_tag"])

        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO aicos_context_docs
                  (scope, context_kind, state_tag, authority_level, authority_mult,
                   role_tags, source_ref, title, summary, body,
                   mtime, freshness_label, content_hash, indexed_at)
                VALUES
                  (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s, now())
                ON CONFLICT (source_ref) DO UPDATE SET
                  scope           = EXCLUDED.scope,
                  context_kind    = EXCLUDED.context_kind,
                  state_tag       = EXCLUDED.state_tag,
                  authority_level = EXCLUDED.authority_level,
                  authority_mult  = EXCLUDED.authority_mult,
                  role_tags       = EXCLUDED.role_tags,
                  title           = EXCLUDED.title,
                  summary         = EXCLUDED.summary,
                  body            = EXCLUDED.body,
                  mtime           = EXCLUDED.mtime,
                  freshness_label = EXCLUDED.freshness_label,
                  content_hash    = EXCLUDED.content_hash,
                  indexed_at      = now()
                """,
                (
                    meta["scope"], meta["context_kind"], meta["state_tag"],
                    meta["authority_level"], meta["authority_mult"],
                    meta["role_tags"], meta["source_ref"],
                    title, summary, body,
                    mtime_ts, freshness, chash,
                ),
            )
        self.conn.commit()
        if not with_embeddings:
            return True
        embedded = self._ensure_embedding(meta["source_ref"], chash)
        return embedded or True

    def _ensure_embedding(self, source_ref: str, content_hash: str) -> bool | str:
        if not self.vector_enabled or self.embedding_client is None or self.embedding_config is None:
            return False
        if not self.embedding_config.enabled:
            return False
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT title, summary, body, embedding_content_hash, embedding_model
                FROM aicos_context_docs
                WHERE source_ref = %s
                """,
                (source_ref,),
            )
            row = cur.fetchone()
        if not row:
            return False
        title, summary, body, existing_hash, existing_model = row
        if existing_hash == content_hash and existing_model == self.embedding_config.model:
            return False
        text = _embedding_text(title, summary, body)
        try:
            embedding = self.embedding_client.embed(text)
            vector = vector_literal(embedding)
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE aicos_context_docs
                    SET embedding = %s::vector,
                        embedding_model = %s,
                        embedding_content_hash = %s,
                        embedded_at = now()
                    WHERE source_ref = %s
                    """,
                    (vector, self.embedding_config.model, content_hash, source_ref),
                )
            self.conn.commit()
            return "embedded"
        except Exception as exc:  # noqa: BLE001 - embedding must not break text search
            self.conn.rollback()
            import sys
            print(f"[indexer] EMBEDDING ERROR {source_ref}: {exc}", file=sys.stderr)
            return "embedding_error"

    def _embed_batch(self, refs: list[tuple[str, str]]) -> dict[str, int]:
        """Embed stale docs in batches, then fall back per-doc on batch failure."""
        stats = {
            "embedded": 0,
            "skipped": 0,
            "embedding_errors": 0,
            "docs_submitted": 0,
            "approx_input_chars": 0,
            "approx_input_tokens": 0,
            "batches": 1,
        }
        if not refs:
            return stats
        if not self.vector_enabled or self.embedding_client is None or self.embedding_config is None:
            stats["skipped"] += len(refs)
            return stats
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT source_ref, title, summary, body, content_hash,
                       embedding_content_hash, embedding_model
                FROM aicos_context_docs
                WHERE source_ref = ANY(%s)
                """,
                ([source_ref for source_ref, _ in refs],),
            )
            rows = cur.fetchall()
        ref_hashes = dict(refs)
        inputs: list[tuple[str, str, str]] = []
        for source_ref, title, summary, body, content_hash, existing_hash, existing_model in rows:
            expected_hash = ref_hashes.get(str(source_ref))
            if expected_hash is None or str(content_hash) != expected_hash:
                stats["skipped"] += 1
                continue
            if existing_hash == expected_hash and existing_model == self.embedding_config.model:
                stats["skipped"] += 1
                continue
            text = _embedding_text(title, summary, body)
            inputs.append((str(source_ref), expected_hash, text))
        missing = len(refs) - len(rows)
        if missing > 0:
            stats["skipped"] += missing
        if not inputs:
            return stats
        stats["docs_submitted"] = len(inputs)
        stats["approx_input_chars"] = sum(len(text) for _, _, text in inputs)
        stats["approx_input_tokens"] = sum(approximate_tokens(text) for _, _, text in inputs)
        try:
            embeddings = self.embedding_client.embed_batch([text for _, _, text in inputs])
            if len(embeddings) != len(inputs):
                raise RuntimeError(f"embedding count mismatch: expected {len(inputs)}, got {len(embeddings)}")
            with self.conn.cursor() as cur:
                for (source_ref, content_hash, _), embedding in zip(inputs, embeddings):
                    cur.execute(
                        """
                        UPDATE aicos_context_docs
                        SET embedding = %s::vector,
                            embedding_model = %s,
                            embedding_content_hash = %s,
                            embedded_at = now()
                        WHERE source_ref = %s
                        """,
                        (vector_literal(embedding), self.embedding_config.model, content_hash, source_ref),
                    )
            self.conn.commit()
            stats["embedded"] += len(inputs)
        except Exception as exc:  # noqa: BLE001 - keep FTS usable if embedding batch fails
            self.conn.rollback()
            import sys
            print(f"[indexer] EMBEDDING BATCH ERROR: {exc}", file=sys.stderr)
            for source_ref, content_hash, _ in inputs:
                result = self._ensure_embedding(source_ref, content_hash)
                if result == "embedded":
                    stats["embedded"] += 1
                elif result == "embedding_error":
                    stats["embedding_errors"] += 1
                else:
                    stats["skipped"] += 1
        return stats

    def remove_file(self, path: Path) -> None:
        try:
            rel = str(path.relative_to(self.repo_root))
        except ValueError:
            return
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM aicos_context_docs WHERE source_ref = %s", (rel,)
            )
        self.conn.commit()

    def index_stats(self) -> dict[str, Any]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'aicos_context_docs'
                  AND column_name = ANY(%s)
                """,
                (["embedding", "embedding_model", "embedding_content_hash", "embedded_at"],),
            )
            embedding_columns = {row[0] for row in cur.fetchall()}
            has_embedding_columns = {
                "embedding",
                "embedding_model",
                "embedding_content_hash",
                "embedded_at",
            }.issubset(embedding_columns)
            cur.execute(
                """
                SELECT scope, context_kind, count(*) as n
                FROM aicos_context_docs
                GROUP BY scope, context_kind
                ORDER BY scope, context_kind
                """
            )
            rows = cur.fetchall()
            if has_embedding_columns:
                cur.execute(
                    """
                    SELECT
                      count(*) AS total_docs,
                      max(mtime) AS latest_source_mtime,
                      max(indexed_at) AS latest_indexed_at,
                      max(embedded_at) AS latest_embedded_at,
                      count(*) FILTER (WHERE embedding IS NOT NULL) AS embedded_docs,
                      count(*) FILTER (
                        WHERE embedding IS NULL
                           OR embedding_content_hash IS DISTINCT FROM content_hash
                      ) AS missing_or_stale_embeddings,
                      count(*) FILTER (WHERE freshness_label = 'stale') AS stale_docs
                    FROM aicos_context_docs
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT
                      count(*) AS total_docs,
                      max(mtime) AS latest_source_mtime,
                      max(indexed_at) AS latest_indexed_at,
                      count(*) FILTER (WHERE freshness_label = 'stale') AS stale_docs
                    FROM aicos_context_docs
                    """
                )
            summary = cur.fetchone()
        total = int(summary[0] or 0)
        if has_embedding_columns:
            latest_embedded_at = summary[3].isoformat() if summary[3] else None
            embedded_docs = int(summary[4] or 0)
            embedding_coverage = round(embedded_docs / total, 4) if total else 0
            missing_or_stale_embeddings = int(summary[5] or 0)
            stale_docs = int(summary[6] or 0)
        else:
            latest_embedded_at = None
            embedded_docs = None
            embedding_coverage = None
            missing_or_stale_embeddings = None
            stale_docs = int(summary[3] or 0)
        return {
            "total_docs": total,
            "latest_source_mtime": summary[1].isoformat() if summary[1] else None,
            "latest_indexed_at": summary[2].isoformat() if summary[2] else None,
            "latest_embedded_at": latest_embedded_at,
            "embedded_docs": embedded_docs,
            "embedding_coverage": embedding_coverage,
            "missing_or_stale_embeddings": missing_or_stale_embeddings,
            "embedding_columns": has_embedding_columns,
            "stale_docs": stale_docs,
            "breakdown": [{"scope": r[0], "kind": r[1], "count": r[2]} for r in rows],
        }

    # -- Internal --------------------------------------------------------

    def _scan_all(self):
        roots = [
            self.repo_root / "brain",
            self.repo_root / "agent-repo",
            self.repo_root / "packages" / "aicos-kernel" / "contracts",
        ]
        seen: set[Path] = set()
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.rglob("*.md")):
                if path in seen:
                    continue
                seen.add(path)
                if any(p in _SKIP_DIRS for p in path.parts):
                    continue
                yield path
