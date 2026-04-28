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
