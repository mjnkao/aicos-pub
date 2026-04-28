"""AICOS PostgreSQL search engine.

Replaces the naive markdown-direct keyword search in mcp_read_serving.py
with proper PostgreSQL FTS (tsvector + ts_rank_cd) plus:
  - authority_mult boost  (canonical > working > evidence)
  - freshness penalty     (stale docs ranked lower)
  - intent-guided kind filter  (route query to relevant context_kinds)
  - why_matched snippet   (show which part of doc matched)

Usage:
    engine = PgSearchEngine(conn, repo_root)
    results = engine.search(
        query="trạng thái hiện tại",
        scope="projects/aicos",
        actor="A1",
        context_kinds=[],   # empty = auto-detect from intent
        max_results=5,
        include_stale=False,
    )
"""
from __future__ import annotations

import re
import textwrap
from datetime import datetime, timezone
from typing import Any

from .embedding import EmbeddingClient, EmbeddingConfig, vector_literal
from .intent import suggest_kinds

# ts_rank_cd weights: {D, C, B, A} → {body(C), summary(B), title(A)}
# D weight unused; A=title gets 1.0, B=summary 0.6, C=body 0.2
_TS_WEIGHTS = "{0.05, 0.2, 0.6, 1.0}"

_FRESHNESS_MULT = {
    "stable": 1.0,
    "fresh":  1.0,
    "aging":  0.85,
    "stale":  0.5,
}

_SNIPPET_LEN = 380
_KIND_ALIASES = {
    "status_items": "status_item",
    "packets": "packet",
    "workstreams": "workstream",
    "artifacts": "artifact_ref",
}


def _contains_any(query: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, query, flags=re.IGNORECASE | re.UNICODE) for pattern in patterns)


def _is_strategic_review(query: str) -> bool:
    return _contains_any(query, [
        r"\bcto\b", r"\bceo\b", r"strategic review", r"architecture review",
        r"technical review", r"product review", r"build.?vs.?buy", r"scalability",
        r"đóng vai", r"vai trò cto", r"vai trò ceo", r"đọc tổng quan",
        r"thiết kế kiến trúc", r"đánh giá", r"phản biện", r"rủi ro kiến trúc",
        r"định hướng sản phẩm", r"chiến lược",
    ])


def direct_read_nudges(query: str) -> list[dict[str, str]]:
    """Suggest cheaper structured MCP reads for common A1/human-manager intents."""
    nudges: list[dict[str, str]] = []

    def add(tool: str, reason: str) -> None:
        if not any(item["tool"] == tool for item in nudges):
            nudges.append({"tool": tool, "reason": reason})

    startup_or_role = _contains_any(query, [
        r"read first", r"before starting", r"before continuing", r"what should .* read",
        r"manager .* read", r"worker .* read", r"bắt đầu", r"đọc gì", r"nên đọc",
    ])
    project_discovery = _contains_any(query, [
        r"what projects", r"list projects", r"projects exist", r"project registry",
        r"có project", r"dự án nào", r"danh sách dự án",
    ])
    current_work = _contains_any(query, [
        r"đang làm đến đâu", r"đang làm gì", r"đang làm", r"làm đến đâu",
        r"where are we", r"what.s happening", r"current progress", r"project state",
    ])
    coordination = _contains_any(query, [
        r"who .* doing", r"which agents", r"avoid overlap", r"stepping on",
        r"ai đang làm", r"agent.*đang", r"chồng chéo", r"dẫm chân",
    ])
    next_work = _contains_any(query, [
        r"what .* next", r"next work", r"should be done next", r"việc gì tiếp",
        r"làm gì tiếp", r"nên làm gì",
    ])
    strategic_review = _is_strategic_review(query)

    if startup_or_role or strategic_review or (current_work and next_work):
        add("aicos_get_startup_bundle", "Best first read for role/project orientation before broad search.")
    if project_discovery:
        add("aicos_get_project_registry", "Best direct read for discovering registered projects.")
    if current_work or coordination or next_work or strategic_review:
        add("aicos_get_handoff_current", "Best direct read for current continuity and takeover context.")
        add("aicos_get_status_items", "Best direct read for open items, tech debt, blockers, and decision follow-ups.")
        add("aicos_get_project_health", "Best direct read for project health, authority, and coordination signals.")
    if coordination:
        add("aicos_get_feedback_digest", "Useful secondary read for recent A1 friction and coordination signals.")
    if not nudges:
        return []
    return nudges


def _priority_boost(row: dict[str, Any], query: str) -> tuple[float, list[str]]:
    """Small rule boost for current-control surfaces; keeps PG/FTS as primary signal."""
    ref = str(row.get("source_ref") or "")
    kind = str(row.get("context_kind") or "")
    boost = 0.0
    signals: list[str] = []

    startup_or_role = _contains_any(query, [
        r"read first", r"before starting", r"before continuing", r"what should .* read",
        r"manager .* read", r"worker .* read", r"bắt đầu", r"đọc gì", r"nên đọc",
    ])
    next_or_current = _contains_any(query, [
        r"what .* next", r"next work", r"should be done next", r"việc gì tiếp",
        r"làm gì tiếp", r"nên làm gì", r"đang làm đến đâu", r"đang làm gì",
        r"where are we", r"current progress",
    ])
    coordination = _contains_any(query, [
        r"who .* doing", r"which agents", r"avoid overlap", r"stepping on",
        r"ai đang làm", r"chồng chéo", r"dẫm chân",
    ])
    project_discovery = _contains_any(query, [
        r"what projects", r"list projects", r"projects exist", r"project registry",
        r"có project", r"dự án nào",
    ])
    strategic_review = _is_strategic_review(query)
    strategic_product = strategic_review and _contains_any(query, [
        r"\bceo\b", r"product", r"business", r"market", r"build.?vs.?buy",
        r"sản phẩm", r"chiến lược", r"tự xây", r"mua", r"dùng .*gbrain",
        r"mem0", r"letta", r"zep", r"graphiti",
    ])

    if (startup_or_role or strategic_review) and ref.endswith(("context-ladder.md", "current-state.md", "current-direction.md", "handoff/current.md")):
        boost += 0.04
        signals.append("current_startup_surface_boost")
    if next_or_current and kind in {"status_item", "handoff", "current_state", "current_direction"}:
        boost += 0.025
        signals.append("current_work_surface_boost")
    if coordination and kind in {"handoff", "status_item", "task_state", "policy"}:
        boost += 0.025
        signals.append("coordination_surface_boost")
    if project_discovery and kind == "project_registry":
        boost += 0.05
        signals.append("project_registry_boost")
    if strategic_review and (
        kind in {"current_direction", "canonical", "policy", "contract", "evidence", "status_item"}
        or any(part in ref for part in [
            "architecture",
            "north-star",
            "semantic-core",
            "provider-interface",
            "deployment-profile",
            "problem-framing",
            "build-vs-buy",
            "market-landscape",
        ])
    ):
        boost += 0.035
        signals.append("strategic_review_surface_boost")
    if strategic_product and any(part in ref for part in [
        "problem-framing",
        "build-vs-buy",
        "market-landscape",
        "substrate-decision",
        "gbrain-substrate-decision",
    ]):
        boost += 0.06
        signals.append("strategic_product_anchor_boost")

    return boost, signals


def _snippet(body: str, query: str) -> str:
    """Extract a short relevant excerpt from body."""
    terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) >= 2]
    lower = body.lower()
    positions = [lower.find(t) for t in terms if lower.find(t) >= 0]
    if not positions:
        return textwrap.shorten(body.replace("\n", " "), _SNIPPET_LEN, placeholder="…")
    start = max(0, min(positions) - 100)
    end   = min(len(body), start + _SNIPPET_LEN)
    chunk = body[start:end].replace("\n", " ").strip()
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(body) else ""
    return f"{prefix}{chunk}{suffix}"


class PgSearchEngine:
    def __init__(
        self,
        conn,
        repo_root,
        embedding_client: EmbeddingClient | None = None,
        embedding_config: EmbeddingConfig | None = None,
        vector_enabled: bool = False,
    ) -> None:
        self.conn = conn
        self.repo_root = repo_root
        self.embedding_client = embedding_client
        self.embedding_config = embedding_config
        self.vector_enabled = vector_enabled

    # ------------------------------------------------------------------
    # Main search entry point
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        scope: str,
        actor: str = "A1",
        context_kinds: list[str] | None = None,
        max_results: int = 5,
        include_stale: bool = False,
        project_role: str = "",
    ) -> dict[str, Any]:
        max_results = max(1, min(max_results, 15))

        # If caller didn't specify kinds, auto-detect from intent
        if not context_kinds:
            context_kinds = suggest_kinds(query)
        context_kinds = [_KIND_ALIASES.get(kind, kind) for kind in context_kinds]

        fts_rows = self._query(query, scope, context_kinds, include_stale, max_results * 4, project_role)
        control_rows = self._control_surface_rows(query, scope, context_kinds, include_stale)
        strategic_rows = self._strategic_anchor_rows(query, scope, context_kinds, include_stale)
        vector_rows: list[dict[str, Any]] = []
        vector_status = "unavailable"
        if self.vector_enabled and self.embedding_client is not None and self.embedding_config is not None and self.embedding_config.enabled:
            try:
                query_embedding = self.embedding_client.embed(query)
                vector_rows = self._vector_query(query_embedding, scope, context_kinds, include_stale, max_results * 4, project_role)
                vector_status = "active"
            except Exception as exc:  # noqa: BLE001 - semantic search fallback
                vector_status = f"fallback: {exc}"
        elif self.embedding_config is not None:
            vector_status = self.embedding_config.reason

        results = self._fuse_and_trim(fts_rows + control_rows + strategic_rows, vector_rows, query, max_results)
        nudges = direct_read_nudges(query)

        return {
            "metadata": {
                "kind": "aicos.mcp.query_result",
                "engine": "postgresql_hybrid" if vector_rows else "postgresql_fts",
                "scope": scope,
                "query": query,
                "intent_kinds": context_kinds,
                "include_stale": include_stale,
                "project_role": project_role or "any",
                "vector_status": vector_status,
                "served_at": datetime.now(timezone.utc).isoformat(),
            },
            "query": query,
            "context_kinds": context_kinds if context_kinds else "auto_all",
            "direct_read_nudges": nudges,
            "results": results,
            "boundary": (
                "PostgreSQL hybrid search uses vector similarity when available, "
                "then fuses it with FTS/authority/freshness ranking. "
                "Results are refs and compact summaries, not full file dumps."
            ),
        }

    def index_stats(self) -> dict[str, Any]:
        try:
            self.conn.rollback()
        except Exception:
            pass
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
                SELECT count(*), scope, context_kind
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
        total = sum(r[0] for r in rows)
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
            "breakdown": [
                {"count": r[0], "scope": r[1], "kind": r[2]} for r in rows
            ],
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _query(
        self,
        query: str,
        scope: str,
        kinds: list[str],
        include_stale: bool,
        limit: int,
        project_role: str,
    ) -> list[dict[str, Any]]:
        shared_kinds = [kind for kind in kinds if kind in {"policy", "contract", "project_registry"}]
        where_parts = [
            "search_vector @@ websearch_to_tsquery('simple', %s)",
            "(scope = %s OR (scope = 'shared' AND context_kind = ANY(%s)))",
        ]
        params: list[Any] = [query, scope, shared_kinds]

        if kinds:
            where_parts.append("context_kind = ANY(%s)")
            params.append(kinds)

        if not include_stale:
            where_parts.append("freshness_label != 'stale'")
            where_parts.append("NOT (context_kind = 'status_item' AND body ~* '(^|\\n)Status:\\s*(resolved|closed|stale|deferred)')")
        if project_role:
            where_parts.append("(%s = ANY(role_tags) OR 'all' = ANY(role_tags))")
            params.append(project_role)

        where = " AND ".join(where_parts)
        params.append(limit)

        sql = f"""
            SELECT *
            FROM (
                SELECT
                    source_ref,
                    title,
                    summary,
                    body,
                    context_kind,
                    state_tag,
                    authority_level,
                    authority_mult,
                    freshness_label,
                    mtime,
                    role_tags,
                    ts_rank_cd(
                        '{_TS_WEIGHTS}',
                        search_vector,
                        websearch_to_tsquery('simple', %s)
                    ) AS fts_score
                FROM aicos_context_docs
                WHERE {where}
            ) ranked
            ORDER BY fts_score * authority_mult DESC
            LIMIT %s
        """
        # fts_score param needs to be first in params list
        full_params = [query] + params

        with self.conn.cursor() as cur:
            cur.execute(sql, full_params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def _vector_query(
        self,
        query_embedding: list[float],
        scope: str,
        kinds: list[str],
        include_stale: bool,
        limit: int,
        project_role: str,
    ) -> list[dict[str, Any]]:
        shared_kinds = [kind for kind in kinds if kind in {"policy", "contract", "project_registry"}]
        where_parts = [
            "embedding IS NOT NULL",
            "(scope = %s OR (scope = 'shared' AND context_kind = ANY(%s)))",
        ]
        where_params: list[Any] = [scope, shared_kinds]

        if kinds:
            where_parts.append("context_kind = ANY(%s)")
            where_params.append(kinds)
        if not include_stale:
            where_parts.append("freshness_label != 'stale'")
            where_parts.append("NOT (context_kind = 'status_item' AND body ~* '(^|\\n)Status:\\s*(resolved|closed|stale|deferred)')")
        if project_role:
            where_parts.append("(%s = ANY(role_tags) OR 'all' = ANY(role_tags))")
            where_params.append(project_role)

        where = " AND ".join(where_parts)
        vector = vector_literal(query_embedding)
        params = [vector, *where_params, vector, limit]
        sql = f"""
            SELECT
                source_ref,
                title,
                summary,
                body,
                context_kind,
                state_tag,
                authority_level,
                authority_mult,
                freshness_label,
                mtime,
                role_tags,
                (1 - (embedding <=> %s::vector)) AS vector_score
            FROM aicos_context_docs
            WHERE {where}
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def _control_surface_rows(
        self,
        query: str,
        scope: str,
        kinds: list[str],
        include_stale: bool,
    ) -> list[dict[str, Any]]:
        """Inject current-control docs for manager/startup/coordination intents."""
        if _is_strategic_review(query):
            return []
        nudges = direct_read_nudges(query)
        if not nudges:
            return []

        wanted_refs: list[str] = []
        wanted_kinds: set[str] = set()
        tool_names = {item["tool"] for item in nudges}
        project_id = scope.removeprefix("projects/")

        if "aicos_get_startup_bundle" in tool_names:
            wanted_refs.extend([
                f"brain/projects/{project_id}/working/context-ladder.md",
                f"brain/projects/{project_id}/working/current-state.md",
                f"brain/projects/{project_id}/working/current-direction.md",
            ])
            wanted_kinds.update({"current_state", "current_direction"})
        if "aicos_get_handoff_current" in tool_names:
            wanted_refs.append(f"brain/projects/{project_id}/working/handoff/current.md")
            wanted_kinds.add("handoff")
        if "aicos_get_project_registry" in tool_names:
            wanted_refs.append("brain/shared/project-registry.md")
            wanted_kinds.add("project_registry")

        if kinds:
            wanted_kinds = {kind for kind in wanted_kinds if kind in kinds}
            wanted_refs = [
                ref for ref in wanted_refs
                if (
                    ("current-state.md" in ref and "current_state" in wanted_kinds)
                    or (("current-direction.md" in ref or "context-ladder.md" in ref) and "current_direction" in wanted_kinds)
                    or ("handoff/current.md" in ref and "handoff" in wanted_kinds)
                    or ("project-registry.md" in ref and "project_registry" in wanted_kinds)
                )
            ]
        if not wanted_refs:
            return []

        where_parts = ["source_ref = ANY(%s)"]
        params: list[Any] = [wanted_refs]
        if not include_stale:
            where_parts.append("freshness_label != 'stale'")
            where_parts.append("NOT (context_kind = 'status_item' AND body ~* '(^|\\n)Status:\\s*(resolved|closed|stale|deferred)')")
        where = " AND ".join(where_parts)
        sql = f"""
            SELECT
                source_ref,
                title,
                summary,
                body,
                context_kind,
                state_tag,
                authority_level,
                authority_mult,
                freshness_label,
                mtime,
                role_tags,
                0.0 AS fts_score,
                'control_surface' AS match_signal
            FROM aicos_context_docs
            WHERE {where}
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        order = {ref: idx for idx, ref in enumerate(wanted_refs)}
        return sorted(rows, key=lambda row: order.get(str(row.get("source_ref")), 999))

    def _strategic_anchor_rows(
        self,
        query: str,
        scope: str,
        kinds: list[str],
        include_stale: bool,
    ) -> list[dict[str, Any]]:
        """Inject a small role-aware anchor set for CTO/CEO strategic reviews."""
        if not _is_strategic_review(query) or scope != "projects/aicos":
            return []

        wanted_refs = []
        if _contains_any(query, [r"\bceo\b", r"product", r"business", r"market", r"build.?vs.?buy", r"sản phẩm", r"chiến lược"]):
            wanted_refs.extend([
                "brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md",
                "brain/projects/aicos/evidence/research/aicos-market-landscape-and-substrate-comparison-20260428.md",
                "brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md",
                "brain/projects/aicos/working/status-items/aicos-problem-framing-build-vs-buy.md",
                "brain/projects/aicos/working/status-items/aicos-gbrain-substrate-decision.md",
            ])
        wanted_refs.extend([
            "brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md",
            "brain/projects/aicos/evidence/research/aicos-phase-2-semantic-core-boundary-20260428.md",
            "brain/projects/aicos/evidence/research/aicos-phase-3-provider-interface-sketch-20260428.md",
        ])
        if _contains_any(query, [r"scalab", r"điểm nghẽn", r"rủi ro", r"risk", r"spof", r"deployment"]):
            wanted_refs.extend([
                "brain/projects/aicos/evidence/research/aicos-phase-4-deployment-profiles-20260428.md",
                "brain/projects/aicos/working/status-items/risk-pg-truth-store.md",
                "brain/projects/aicos/working/status-items/arch-single-machine-spof.md",
            ])
        if _contains_any(query, [r"misalign", r"lệch", r"option c", r"dashboard", r"coworker", r"pm integration"]):
            wanted_refs.extend([
                "brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md",
                "brain/projects/aicos/evidence/research/aicos-phase-6-human-ai-coworker-model-20260428.md",
                "brain/projects/aicos/evidence/research/aicos-phase-7-pm-integration-contract-20260428.md",
            ])

        wanted_refs = list(dict.fromkeys(wanted_refs))
        if kinds:
            allowed_by_kind = {
                "evidence": "/evidence/",
                "status_item": "/working/status-items/",
                "status_items": "/working/status-items/",
            }
            wanted_refs = [
                ref for ref in wanted_refs
                if any(marker in ref for kind, marker in allowed_by_kind.items() if kind in kinds)
            ]
        if not wanted_refs:
            return []

        where_parts = ["source_ref = ANY(%s)"]
        params: list[Any] = [wanted_refs]
        if not include_stale:
            where_parts.append("freshness_label != 'stale'")
            where_parts.append("NOT (context_kind = 'status_item' AND body ~* '(^|\\n)Status:\\s*(resolved|closed|stale|deferred)')")
        sql = f"""
            SELECT
                source_ref,
                title,
                summary,
                body,
                context_kind,
                state_tag,
                authority_level,
                authority_mult,
                freshness_label,
                mtime,
                role_tags,
                0.0 AS fts_score,
                'strategic_anchor' AS match_signal
            FROM aicos_context_docs
            WHERE {" AND ".join(where_parts)}
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        order = {ref: idx for idx, ref in enumerate(wanted_refs)}
        return sorted(rows, key=lambda row: order.get(str(row.get("source_ref")), 999))

    def _fuse_and_trim(
        self,
        fts_rows: list[dict[str, Any]],
        vector_rows: list[dict[str, Any]],
        query: str,
        max_results: int,
    ) -> list[dict[str, Any]]:
        by_ref: dict[str, dict[str, Any]] = {}
        for rank, row in enumerate(fts_rows, 1):
            item = by_ref.setdefault(row["source_ref"], {"row": row, "rrf": 0.0, "signals": []})
            item["rrf"] += 1.0 / (60 + rank)
            item["signals"].append(str(row.get("match_signal") or "fts"))
        for rank, row in enumerate(vector_rows, 1):
            item = by_ref.setdefault(row["source_ref"], {"row": row, "rrf": 0.0, "signals": []})
            item["rrf"] += 1.0 / (60 + rank)
            item["signals"].append("vector")

        for item in by_ref.values():
            boost, signals = _priority_boost(item["row"], query)
            if boost:
                item["rrf"] += boost
                item["signals"].extend(signals)

        ranked = sorted(by_ref.values(), key=lambda item: item["rrf"], reverse=True)
        results = []
        for rank, item in enumerate(ranked[:max_results], 1):
            row = item["row"]
            fts   = float(row.get("fts_score") or 0)
            vector = float(row.get("vector_score") or 0)
            auth  = float(row["authority_mult"] or 1.0)
            fresh = _FRESHNESS_MULT.get(row["freshness_label"], 1.0)
            final_score = (float(item["rrf"]) + fts + max(vector, 0)) * auth * fresh

            mtime = row["mtime"]
            mtime_str = mtime.isoformat() if isinstance(mtime, datetime) else str(mtime)

            results.append({
                "rank":            rank,
                "score":           round(final_score, 4),
                "match_signals":   item["signals"],
                "kind":            row["context_kind"],
                "state":           row["state_tag"],
                "authority":       row["authority_level"],
                "freshness":       row["freshness_label"],
                "ref":             row["source_ref"],
                "title":           row["title"] or row["source_ref"],
                "summary":         _snippet(row["body"] or row["summary"] or "", query),
                "mtime":           mtime_str,
            })
        return results
