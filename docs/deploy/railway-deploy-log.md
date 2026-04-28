# Railway Deploy Log

Status: in progress
Started: 2026-04-28

## Goal

Deploy `aicos-pub` to Railway and verify that the public package can run the
current AICOS HTTP MCP daemon surface closely enough to the private AICOS
runtime for public testing.

## Current Deploy Shape

- App entrypoint: `scripts/aicos-railway-start`
- Railway config: `railway.toml`
- Runtime: Python via Nixpacks
- Service: `integrations/mcp-daemon/aicos_mcp_daemon.py`
- Public safety: `AICOS_DAEMON_TOKEN` is required for Railway/public deploy
- Search mode: `--no-pg` for first deploy, so the daemon uses markdown-direct
  fallback without requiring a Railway PostgreSQL plugin

## Log

### 2026-04-28 local preflight

Findings:

- Repo had no `.gitignore`, package metadata, Railway config, or start command.
- Sensitive scan did not find real secrets. Token examples were normalized to
  placeholder form such as `AICOS_DAEMON_TOKEN=<set-a-strong-token>`.
- `aicos-pub` contains the public continuity bundle from AICOS, including
  architecture docs, migration notes, research memos, working state, status
  items, open questions, and task state.

Fixes applied:

- Added `.gitignore` for runtime homes, Python caches, local tool state,
  env files, logs, database files, and private key material.
- Added `pyproject.toml` so Railway/Nixpacks can install Python dependencies.
- Added `railway.toml` with healthcheck `/health`.
- Added `scripts/aicos-railway-start` to launch the HTTP MCP daemon on
  `$PORT`, require `AICOS_DAEMON_TOKEN`, and use `--no-pg` for first deploy.
- Normalized token examples away from secret-like placeholder values.

Verification:

- `./aicos --help` passed.
- Python compile for kernel, bridge, and daemon files passed.
- Sensitive marker scan passed after placeholder cleanup.

### 2026-04-28 local Railway start preflight

Command:

```bash
PORT=8765 AICOS_DAEMON_TOKEN=<test-token> scripts/aicos-railway-start
```

Error:

```text
scripts/aicos-railway-start: line 13: exec: python: not found
```

Cause:

- The start script assumed `python` exists in PATH. On this machine only
  `python3` is available.

Fix:

- Updated `scripts/aicos-railway-start` to use `${PYTHON:-python3}`.

Retest:

- Daemon started on `0.0.0.0:8765` with token auth.
- Authenticated `/health` returned `status: ok` and `search_engine:
  markdown_direct`.
- Authenticated `tools/list` returned MCP tools.
- Authenticated `aicos_get_project_health` for `projects/aicos` returned the
  exported public continuity bundle state.

Additional deploy issue:

- Unauthenticated `/health` returns `401` when token auth is enabled.
- Railway `healthcheckPath` cannot attach a bearer token, so `healthcheckPath =
  "/health"` would make an otherwise healthy token-protected service fail
  deployment health checks.

Fix:

- Removed `healthcheckPath` from `railway.toml` for the first public deploy.
  Runtime verification should use an authenticated smoke request after deploy.

### 2026-04-28 Railway project setup

Actions:

- Created Railway project `aicos-pub`.
- Created Railway service `aicos-pub`.
- Set `AICOS_DAEMON_TOKEN` through `railway variable set --stdin` so the token
  was not printed to terminal output.
- Pushed initial GitHub commit `c80f8df`.

### 2026-04-28 Railway deploy attempt 1

Command:

```bash
railway up --ci --message "Initial aicos-pub Railway deploy"
```

Result:

- Build failed during Nixpacks install.

Error excerpt:

```text
error: error in 'egg_base' option: 'packages/aicos-kernel' does not exist or is not a directory
```

Cause:

- Nixpacks detected `pyproject.toml` and generated an install phase that copied
  only `pyproject.toml` into `/app` before running `pip install .`.
- The package uses `package-dir = {"": "packages/aicos-kernel"}`, so the build
  metadata references a directory that had not been copied yet.

Fix:

- Added `nixpacks.toml` to override the install phase.
- The Railway build now creates `/opt/venv` and installs only
  `psycopg2-binary`; the daemon runs directly from repository source via
  `scripts/aicos-railway-start`.

### 2026-04-28 Railway deploy attempt 2

Command:

```bash
railway up --ci --message "Fix Nixpacks config for aicos-pub"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `7fa1bfb5-6dff-45fa-aecf-7d6314af44f6`
- Railway domain: `https://aicos-pub-production.up.railway.app`

Runtime logs:

```text
PostgreSQL disabled via --no-pg flag
AICOS MCP daemon started
health: http://0.0.0.0:8080/health
```

Smoke tests:

- Unauthenticated `/health` returned `401`, expected for token-protected public
  deploy.
- Authenticated `/health` returned `status: ok`, `search_engine:
  markdown_direct`, and `auth: token_required`.
- Authenticated MCP `aicos_get_project_health` for `projects/aicos` returned
  the exported public continuity state with `active_status_item_count: 23`,
  `blocked_status_item_count: 0`, `active_task_count: 0`, and
  `recent_feedback_count: 5`.

Current gap:

- First Railway deploy intentionally runs with `--no-pg`, so search is
  markdown-direct fallback rather than PostgreSQL hybrid/pgvector. This proves
  the public package can boot and serve MCP state, but it is not yet equivalent
  to the private AICOS runtime when that runtime has PostgreSQL hybrid search
  enabled.

Follow-up:

- Add a Railway PostgreSQL service and switch from `--no-pg` to
  `AICOS_PG_DSN`-backed hybrid search.
- Decide whether to expose unauthenticated `/health` with a minimal public
  payload, or keep authenticated health and avoid Railway healthcheckPath.

### 2026-04-28 Railway PostgreSQL/pgvector setup

Actions:

- Added Railway PostgreSQL service:

```bash
railway add --database postgres --json
```

- Railway created service `Postgres` with service id
  `e6b0325f-19b5-4705-a4b3-e54c67efa9bc`.
- Postgres image: `ghcr.io/railwayapp-templates/postgres-ssl:18`.
- Postgres volume: `postgres-volume`, mounted at
  `/var/lib/postgresql/data`, 4.9 GB quota.
- Updated `scripts/aicos-railway-start` so Railway starts PostgreSQL mode when
  either `AICOS_PG_DSN` or `DATABASE_URL` is present, and falls back to
  `--no-pg` only when no DSN is configured.

Variables configured on service `aicos-pub`:

```bash
railway variable set --service aicos-pub 'AICOS_PG_DSN=${{Postgres.DATABASE_URL}}' --skip-deploys
railway variable set --service aicos-pub AICOS_DAEMON_EXTRA_TOKENS=<redacted> --skip-deploys
railway variable set --service aicos-pub 'AICOS_DAEMON_TOKEN_SCOPE_POLICY=<redacted-json>' --skip-deploys
railway variable set --service aicos-pub 'AICOS_EMBEDDINGS=auto' --skip-deploys
```

Token policy:

- Created three extra labeled bearer tokens: `codex-test`, `openclaw-test`,
  and `community-test`.
- Token values were generated with `openssl rand -hex 24` and were not printed
  into logs.
- Extra tokens may read `projects/*` and may write only `projects/aicos-pub`.
- No token was added to `AICOS_DAEMON_INTERNAL_TOKEN_LABELS`, so protected
  writes to `projects/aicos` remain blocked for public/test clients.

Issue during variable setup:

```text
Failed to fetch: error sending request for url (https://backboard.railway.com/graphql/v2)
operation timed out
```

Fix:

- Re-ran verification with `railway variable list --service aicos-pub --kv`
  and confirmed these variables exist: `AICOS_PG_DSN`,
  `AICOS_DAEMON_EXTRA_TOKENS`, `AICOS_DAEMON_TOKEN_SCOPE_POLICY`, and
  `AICOS_EMBEDDINGS`.

OpenAI embedding key:

- Local shell did not have `OPENAI_API_KEY`, so no key was copied to Railway.
- With `AICOS_EMBEDDINGS=auto`, AICOS will enable vector embedding search after
  `OPENAI_API_KEY` is added and the service is redeployed or restarted.

Deploy command:

```bash
railway up --ci --message "Enable Railway PostgreSQL for aicos-pub"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `9217ed17-07ce-45db-bc86-f8ecc290cf6e`
- Railway domain: `https://aicos-pub-production.up.railway.app`

Runtime logs:

```text
Starting Container
08:34:14 [INFO] aicos-daemon: Connecting to PostgreSQL...
08:34:16 [INFO] aicos-daemon:   auth     : token required
08:34:16 [INFO] aicos-daemon:   internal token labels: (none)
08:34:16 [INFO] aicos-daemon:   token scope policy labels: codex-test, community-test, openclaw-test
```

Smoke tests:

- Unauthenticated `/health` returned `401`, expected for token-protected public
  deploy.
- Authenticated `/health` returned `status: ok`.
- Authenticated `/health` reported `search_engine: postgresql_fts`.
- `search_status.postgresql` reported `active`.
- `search_status.vector` reported `pgvector active`.
- `search_status.embeddings` reported `OPENAI_API_KEY not set`.
- `index.total_docs` reported `170`.
- `index.embedding_columns` reported `true`.
- `index.embedded_docs` reported `0`.
- Authenticated MCP `tools/list` returned tool schemas.
- Authenticated MCP `aicos_query_project_context` for `projects/aicos`
  returned results through engine `postgresql_fts`.
- The `community-test` extra bearer token successfully authenticated against
  `/health`.

Current parity state:

- AICOS public Railway runtime now boots with Railway PostgreSQL and pgvector
  schema support.
- It is not yet full PostgreSQL hybrid/vector parity with a private AICOS
  runtime that has embeddings enabled, because `OPENAI_API_KEY` is not set.
- Expected next step for full hybrid parity: set `OPENAI_API_KEY` on the
  Railway `aicos-pub` service, keep `AICOS_EMBEDDINGS=auto`, redeploy/restart,
  then verify `search_engine: postgresql_hybrid` or query metadata showing
  active vector results after embeddings are indexed.

### 2026-04-28 Railway OpenAI embedding env handoff

Added files:

- `docs/deploy/railway-embedding.env.example`
- `scripts/aicos-railway-apply-embedding-env`

Local-only secret file:

- `.runtime-home/railway-embedding.env`
- This file is ignored by git through `.runtime-home/`.

Setup flow:

```bash
cp docs/deploy/railway-embedding.env.example .runtime-home/railway-embedding.env
$EDITOR .runtime-home/railway-embedding.env
scripts/aicos-railway-apply-embedding-env
railway up --ci --message "Enable OpenAI embeddings for aicos-pub"
```

The apply script:

- Refuses to run if `OPENAI_API_KEY` is missing or still the placeholder.
- Sends `OPENAI_API_KEY` through `railway variable set --stdin` so the key is
  not printed.
- Sets `AICOS_EMBEDDINGS=auto`.
- Sets `AICOS_EMBEDDING_MODEL=text-embedding-3-small`.
- Sets `AICOS_EMBEDDING_DIMENSIONS=1536`.
- Sets `AICOS_EMBEDDING_BATCH_SIZE=32`.

Expected verification after deploy:

- `/health` should report `search_status.embeddings: enabled`.
- Initial `embedding_index` may show `pending` while indexing.
- After reindex completes, `embedded_docs` should rise above `0`.
- Query metadata should report `engine: postgresql_hybrid` when vector rows are
  returned.

### 2026-04-28 Railway OpenAI embedding deploy

Actions:

- Filled local ignored file `.runtime-home/railway-embedding.env` with
  `OPENAI_API_KEY`.
- Applied embedding variables without printing secrets:

```bash
scripts/aicos-railway-apply-embedding-env
```

- Deployed:

```bash
railway up --ci --message "Enable OpenAI embeddings for aicos-pub"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `1fc6e8ba-a672-405f-a767-727adabed321`

Issue after first container start:

```text
PostgreSQL unavailable (Schema apply failed: canceling statement due to lock timeout)
```

Observed health response:

- `search_engine: markdown_direct`
- `search_status.postgresql: schema failed: canceling statement due to lock timeout`
- `search_status.vector: not_initialized`
- `search_status.embeddings: not_initialized`

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Result after restart:

- PostgreSQL recovered without code changes.
- `/health` reported `search_engine: postgresql_hybrid`.
- `search_status.postgresql: active`.
- `search_status.vector: pgvector active`.
- `search_status.embeddings: enabled`.
- Initial `embedding_index: running`.

Final embedding verification:

- `embedding_index: completed`.
- `total_docs: 170`.
- `embedded_docs: 170`.
- `missing_or_stale_embeddings: 0`.
- `embedding_coverage: 1.0`.
- `embedding_errors: 0`.

MCP query verification:

- Query: `current AICOS status and next tasks`.
- Tool: `aicos_query_project_context`.
- Scope: `projects/aicos`.
- Query metadata reported `engine: postgresql_hybrid`.
- Query metadata reported `vector_status: active`.
- Returned results included `match_signals` with `vector`, including
  `brain/projects/aicos/working/current-state.md`,
  `brain/projects/aicos/working/architecture-working-summary.md`,
  `brain/projects/aicos/working/issue-map.md`,
  `brain/projects/aicos/working/current-milestones.md`, and related working
  context refs.

Current parity state:

- Railway `aicos-pub` now matches the local AICOS retrieval mode for the public
  exported corpus: PostgreSQL + pgvector + OpenAI embeddings +
  `postgresql_hybrid`.
- Remaining expected difference from private local AICOS is corpus size/content:
  Railway public export indexed 170 docs, while private local AICOS may index
  additional private docs.

### 2026-04-28 Railway agent bearer tokens

Actions:

- Added three dedicated Railway bearer token labels:
  `codex-agent-01`, `claude-agent-01`, and `openclaw-agent-01`.
- Preserved existing test token labels.
- Updated `AICOS_DAEMON_EXTRA_TOKENS` on Railway.
- Updated `AICOS_DAEMON_TOKEN_SCOPE_POLICY` so the new labels may read
  `projects/*` and write only `projects/aicos-pub`.
- Wrote local-only token values to `.runtime-home/aicos-pub-agent-tokens.md`.
  This path is ignored by git and must not be committed.
- Added public connection guide:
  `docs/install/AICOS_PUB_RAILWAY_AGENT_CONNECT.md`.

Issue:

- `railway service restart` did not immediately expose the new token labels in
  `/health`; the running deployment still reported only the old labels.

Fix:

- Ran `railway service redeploy --service aicos-pub --yes --json`.
- Waited until deployment `b631379f-2251-4be0-99d4-540e84fbaaba` became
  `SUCCESS`.
- The redeployed container saw the new labels.

Second issue:

- The redeployed container again hit the known PostgreSQL schema lock timeout
  and temporarily fell back to `markdown_direct`.

Fix:

- Ran `railway service restart --service aicos-pub --yes --json`.
- Retested with `codex-agent-01`.

Final verification:

- New token authenticated successfully.
- `/health` reported accepted token labels including `codex-agent-01`,
  `claude-agent-01`, and `openclaw-agent-01`.
- `/health` reported `search_engine: postgresql_hybrid`.
- `/health` reported `search_status.embeddings: enabled`.
- `/health` reported `index.embedding_coverage: 1.0`.

### 2026-04-28 Codex A2-core public MCP token

Actions:

- Added Railway bearer token label `codex-a2-core-pub`.
- Policy for `codex-a2-core-pub`:
  - read `projects/*`
  - write `projects/aicos-pub`
- Did not add `codex-a2-core-pub` to
  `AICOS_DAEMON_INTERNAL_TOKEN_LABELS`, so it is not an internal maintainer
  token for protected private scopes.
- Stored the token locally outside git:
  - `<codex-home>/secrets/aicos-pub-codex-a2-core-pub.token`
  - `.runtime-home/codex-a2-core-pub-token.md`
- Added Codex MCP config in `<codex-home>/config.toml`:
  - server name: `aicos_pub`
  - URL: `https://aicos-pub-production.up.railway.app/mcp`
  - auth: `Authorization: Bearer <codex-a2-core-pub-token>`

Issue:

- Initial write smoke to `projects/aicos-pub` returned
  `missing_project_scope` because the Railway public corpus did not yet include
  `brain/projects/aicos-pub`.

Fix:

- Added minimal public MCP scope files:
  - `brain/projects/aicos-pub/canonical/project-profile.md`
  - `brain/projects/aicos-pub/working/handoff/current.md`
  - `brain/projects/aicos-pub/working/status-items/README.md`
  - `brain/projects/aicos-pub/working/feedback/README.md`
- Committed and pushed commit `0d6abca`.
- Deployed with:

```bash
railway up --ci --message "Add aicos-pub public MCP scope"
```

Second issue:

- Deploy again hit the known PostgreSQL schema lock timeout and temporarily
  reported `search_engine: markdown_direct`.

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Final verification:

- `/health` authenticated with `codex-a2-core-pub`.
- `/health` reported `search_engine: postgresql_hybrid`.
- `/health` reported `search_status.postgresql: active`.
- `/health` reported `search_status.embeddings: enabled`.
- `/health` reported `index.embedding_coverage: 1.0`.
- `/health` breakdown included `projects/aicos-pub` docs.
- MCP `tools/list` returned 17 tools with `codex-a2-core-pub`.
- MCP `aicos_record_feedback` successfully wrote to
  `brain/projects/aicos-pub/working/feedback/20260428t101817z-8057b9bc4a.md`.

### 2026-04-28 Sync A2 runtime identity and retrieval updates

Context:

- A2 updated private AICOS with runtime identity schema v0.6 and retrieval
  evaluation/runtime improvements.
- Private local MCP handoff for `projects/aicos-pub` indicated the proposal was
  accepted for A2 review/implementation.

Public-export pipeline fixes needed during sync:

- `scripts/aicos-retrieval-eval` has no file extension, so placeholder
  transforms did not originally rewrite private project markers inside it.
- `.gitignore` intentionally contains local tool-state directories, so scrub
  should not treat `.gitignore` as leaked tool residue.
- `aicos-daemon.env.example` is an env example file, so placeholder transforms
  must include `*.env.example`.

Fixes applied in private `public-export/sync-aicos-pub.sh`:

- Added `aicos-retrieval-eval` to transformed files.
- Added `*.env.example` to transformed files.
- Allowed `scan_regex` to accept extra `rg` flags.
- Excluded `.gitignore` from the local tool residue marker scan.

Sync result:

- Export scan passed.
- Public verification passed:
  - `./aicos --help`
  - Python compile for kernel, daemon, and local MCP bridge modules
  - public sensitive marker scan
- Public-only Railway setup guides were restored after sync because private
  `docs/install/` does not yet carry them.
- Commit pushed: `83ea5cf`.

Notable exported changes:

- Runtime identity schema v0.6 status and feedback records.
- New `mcp_tool_definitions.py` and `mcp_tool_schema.py`.
- Retrieval eval token fallback and two-project regression gate updates.
- Additional retrieval and module inventory research/status notes.
- PostgreSQL schema/search metadata improvements.

Deploy:

```bash
railway up --ci --message "Sync A2 runtime identity and retrieval updates"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `88b4626b-4a34-4d44-98f8-4e4c3fa5579d`.

Known issue repeated:

- First post-deploy health check reported `search_engine: markdown_direct`.
- PostgreSQL status reported `schema failed: canceling statement due to lock timeout`.

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Final verification:

- `/health` reported `search_engine: postgresql_hybrid`.
- `search_status.postgresql: active`.
- `search_status.vector: pgvector active`.
- `search_status.embeddings: enabled`.
- `embedding_index: completed`.
- `total_docs: 187`.
- `embedded_docs: 187`.
- `embedding_coverage: 1.0`.
- Project breakdown included `projects/aicos` with 166 docs and
  `projects/aicos-pub` with 5 docs.
- MCP `tools/list` returned 17 tools.
- MCP query for runtime identity schema returned `postgresql_hybrid` with
  `vector_status: active` and vector-ranked runtime identity refs.

## 2026-04-28 - Deploy log and exported feedback follow-up

Context:

- After the A2 sync deployment above, the public deploy log itself and one new
  exported private feedback record were committed to `main`.
- Commit pushed: `3b465c6`.

Deploy:

```bash
railway up --ci --message "Deploy A2 sync deployment log"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `36c490d9-97eb-4e71-a205-516b170a7966`.

Known issue repeated:

- First post-deploy health check reported `search_engine: markdown_direct`.
- PostgreSQL status reported `schema failed: canceling statement due to lock timeout`.

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Final verification:

- `/health` reported `search_engine: postgresql_hybrid`.
- `search_status.postgresql: active`.
- `search_status.vector: pgvector active`.
- `search_status.embeddings: enabled`.
- `embedding_index: completed`.
- `total_docs: 188`.
- `embedded_docs: 188`.
- `embedding_coverage: 1.0`.
- Project breakdown included `projects/aicos` with 167 docs and
  `projects/aicos-pub` with 5 docs.
- MCP `tools/list` returned 17 tools.
- MCP query for runtime identity schema returned `postgresql_hybrid` with
  `vector_status: active`.

## 2026-04-28 - Final log-only deploy verification

Context:

- The deploy log entry above was committed and pushed as `535a85c`.
- A final Railway deploy was run to verify the deploy log update and current
  exported public tree.

Deploy:

```bash
railway up --ci --message "Deploy final A2 sync log entry"
```

Result:

- Build succeeded.
- Deploy succeeded.
- Deployment id: `0a96a187-afcc-4443-9a1b-c7aefd77b6a2`.

Known issue repeated:

- First post-deploy health check reported `search_engine: markdown_direct`.
- PostgreSQL status reported `schema failed: canceling statement due to lock timeout`.
- A health retry immediately after restart briefly returned HTTP 502 while the
  container was still warming.

Fix:

```bash
railway service restart --service aicos-pub --yes --json
```

Final verification:

- `/health` reported `search_engine: postgresql_hybrid`.
- `search_status.postgresql: active`.
- `search_status.vector: pgvector active`.
- `search_status.embeddings: enabled`.
- `embedding_index: completed`.
- `total_docs: 188`.
- `embedded_docs: 188`.
- `embedding_coverage: 1.0`.
- Project breakdown included `projects/aicos` with 167 docs and
  `projects/aicos-pub` with 5 docs.
- MCP `tools/list` returned 17 tools.
- MCP query for runtime identity schema returned `postgresql_hybrid` with
  `vector_status: active`.
