-- AICOS Context Search Schema
-- PostgreSQL 14+ with pg_trgm extension.
-- pgvector is enabled opportunistically by Python setup when the extension is
-- available; FTS remains available without pgvector.
--
-- Text search config: 'simple' — lowercase only, no stemming.
-- This handles Vietnamese and English equally without language-specific stemming.

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- -----------------------------------------------------------------------
-- aicos_context_docs: one row per indexed markdown file
-- -----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS aicos_context_docs (
  id               SERIAL PRIMARY KEY,

  -- Routing / scope
  scope            TEXT    NOT NULL,               -- projects/aicos, projects/sample-project, shared
  context_kind     TEXT    NOT NULL,               -- canonical, working, handoff, status_item, policy, contract, packet, task_state, workstream, artifact_ref, evidence, open_items, open_questions
  state_tag        TEXT    NOT NULL DEFAULT 'working',  -- canonical, working, evidence, execution, reference, frozen
  authority_level  TEXT    NOT NULL DEFAULT 'medium',   -- high, medium, low

  -- Ranking boost stored as column so ORDER BY needs no CASE expression
  -- canonical/policy → 2.0, working hot → 1.5-1.8, status_item → 1.0, evidence → 0.5
  authority_mult   REAL    NOT NULL DEFAULT 1.0,

  -- Role relevance tags — used for role-aware filtering in Phase 2
  role_tags        TEXT[]  NOT NULL DEFAULT '{}',  -- all, cto, architect, tech_lead, developer, qa, designer, writer

  -- Content
  source_ref       TEXT    NOT NULL UNIQUE,        -- path relative to repo root
  title            TEXT    NOT NULL DEFAULT '',
  summary          TEXT    NOT NULL DEFAULT '',    -- first meaningful paragraph or frontmatter summary
  body             TEXT    NOT NULL DEFAULT '',    -- full markdown body

  -- Freshness
  mtime            TIMESTAMPTZ NOT NULL,
  freshness_label  TEXT    NOT NULL DEFAULT 'fresh', -- fresh, aging, stale, stable

  -- Dedup / change detection
  content_hash     TEXT,

  -- FTS — auto-updated by trigger below
  search_vector    tsvector,

  indexed_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT aicos_ctx_scope_check    CHECK (scope ~ '^[a-z0-9_/-]+$'),
  CONSTRAINT aicos_ctx_kind_check     CHECK (context_kind IN (
    'canonical','working','handoff','status_item','policy','contract',
    'packet','task_state','workstream','artifact_ref','evidence','project_registry',
    'open_items','open_questions','current_state','current_direction'
  )),
  CONSTRAINT aicos_ctx_state_check    CHECK (state_tag IN (
    'canonical','working','evidence','execution','reference','frozen'
  )),
  CONSTRAINT aicos_ctx_auth_check     CHECK (authority_level IN ('high','medium','low')),
  CONSTRAINT aicos_ctx_fresh_check    CHECK (freshness_label IN ('fresh','aging','stale','stable'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_scope   ON aicos_context_docs(scope);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_kind    ON aicos_context_docs(context_kind);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_state   ON aicos_context_docs(state_tag);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_search  ON aicos_context_docs USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_roles   ON aicos_context_docs USING GIN(role_tags);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_mtime   ON aicos_context_docs(mtime DESC);
CREATE INDEX IF NOT EXISTS idx_aicos_ctx_title   ON aicos_context_docs USING GIN(title gin_trgm_ops);

-- -----------------------------------------------------------------------
-- Trigger: rebuild search_vector on content change
-- Weights: title=A (1.0), summary=B (0.4), body=C (0.2)
-- Using 'simple' config: lowercases, no stemming — works for Vietnamese
-- -----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION aicos_update_search_vector() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('simple', coalesce(NEW.title,   '')), 'A') ||
    setweight(to_tsvector('simple', coalesce(NEW.summary, '')), 'B') ||
    setweight(to_tsvector('simple', coalesce(NEW.body,    '')), 'C');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_aicos_search_vector ON aicos_context_docs;
CREATE TRIGGER trg_aicos_search_vector
  BEFORE INSERT OR UPDATE OF title, summary, body
  ON aicos_context_docs
  FOR EACH ROW EXECUTE FUNCTION aicos_update_search_vector();

-- -----------------------------------------------------------------------
-- Convenience view: active (non-frozen, non-evidence) docs only
-- -----------------------------------------------------------------------
CREATE OR REPLACE VIEW aicos_active_docs AS
  SELECT * FROM aicos_context_docs
  WHERE state_tag NOT IN ('frozen', 'evidence')
    AND freshness_label != 'stale';
