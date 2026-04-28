"""AICOS PostgreSQL search engine package.

Public API:
    PgSearchEngine   — query interface for the daemon
    BrainIndexer     — file scanner / upsert for brain/ files
    apply_schema     — run schema.sql DDL (idempotent)
    apply_vector_schema — enable optional pgvector columns/index
    try_connect      — connect to pg, return (conn, err_str)
"""
from .config import apply_schema, apply_vector_schema, try_connect
from .embedding import EmbeddingClient, embedding_config
from .engine import PgSearchEngine
from .indexer import BrainIndexer

__all__ = [
    "PgSearchEngine",
    "BrainIndexer",
    "EmbeddingClient",
    "apply_schema",
    "apply_vector_schema",
    "embedding_config",
    "try_connect",
]
