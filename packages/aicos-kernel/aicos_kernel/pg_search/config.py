"""PostgreSQL connection config for AICOS search.

Environment variables:
    AICOS_PG_DSN   — full DSN, e.g. postgresql://user:pass@host:5432/aicos
                     Overrides all other env vars below.
    AICOS_PG_HOST  — default: localhost
    AICOS_PG_PORT  — default: 5432
    AICOS_PG_DB    — default: aicos
    AICOS_PG_USER  — default: (current OS user)
    AICOS_PG_PASS  — default: (empty)
"""
from __future__ import annotations

import os
from pathlib import Path

# Optional import — engine degrades gracefully when psycopg2 not installed
try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

SCHEMA_SQL = Path(__file__).parent / "schema.sql"


def dsn() -> str:
    if explicit := os.environ.get("AICOS_PG_DSN", "").strip():
        return explicit
    host = os.environ.get("AICOS_PG_HOST", "localhost")
    port = os.environ.get("AICOS_PG_PORT", "5432")
    db   = os.environ.get("AICOS_PG_DB",   "aicos")
    user = os.environ.get("AICOS_PG_USER", "")
    pw   = os.environ.get("AICOS_PG_PASS", "")
    if user and pw:
        return f"postgresql://{user}:{pw}@{host}:{port}/{db}"
    if user:
        return f"postgresql://{user}@{host}:{port}/{db}"
    return f"postgresql://{host}:{port}/{db}"


def connect():
    """Return a psycopg2 connection or raise ImportError / OperationalError."""
    if not HAS_PSYCOPG2:
        raise ImportError(
            "psycopg2 is not installed. "
            "Run: pip install psycopg2-binary"
        )
    try:
        connect_timeout = int(os.environ.get("AICOS_PG_CONNECT_TIMEOUT_SECONDS", "5"))
    except ValueError:
        connect_timeout = 5
    try:
        statement_timeout = int(os.environ.get("AICOS_PG_STATEMENT_TIMEOUT_MS", "15000"))
    except ValueError:
        statement_timeout = 15000
    try:
        lock_timeout = int(os.environ.get("AICOS_PG_LOCK_TIMEOUT_MS", "5000"))
    except ValueError:
        lock_timeout = 5000
    conn = psycopg2.connect(dsn(), connect_timeout=max(1, connect_timeout))
    with conn.cursor() as cur:
        cur.execute("SET statement_timeout = %s", (max(0, statement_timeout),))
        cur.execute("SET lock_timeout = %s", (max(0, lock_timeout),))
    conn.commit()
    return conn


def try_connect():
    """Return (conn, None) on success, (None, error_str) on failure."""
    try:
        conn = connect()
        return conn, None
    except ImportError as exc:
        return None, str(exc)
    except Exception as exc:
        return None, f"PostgreSQL connection failed: {exc}"


def apply_schema(conn) -> None:
    """Create tables, indexes, and triggers if they don't exist."""
    sql = SCHEMA_SQL.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def apply_vector_schema(conn, dimensions: int) -> tuple[bool, str]:
    """Enable pgvector-backed embedding columns when the extension is available."""
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                f"""
                ALTER TABLE aicos_context_docs
                  ADD COLUMN IF NOT EXISTS embedding vector({int(dimensions)}),
                  ADD COLUMN IF NOT EXISTS embedding_model TEXT,
                  ADD COLUMN IF NOT EXISTS embedding_content_hash TEXT,
                  ADD COLUMN IF NOT EXISTS embedded_at TIMESTAMPTZ
                """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_aicos_ctx_embedding_hnsw
                ON aicos_context_docs
                USING hnsw (embedding vector_cosine_ops)
                WHERE embedding IS NOT NULL
                """
            )
        conn.commit()
        return True, "pgvector active"
    except Exception as exc:
        conn.rollback()
        return False, f"pgvector unavailable: {exc}"
