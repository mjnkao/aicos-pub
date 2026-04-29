# Handoff Hiện Tại Của Project AICOS

Ngày: 2026-04-21
Trạng thái: sole H1 current handoff index cho `projects/aicos`
Actor lane chính: A2-Core

## Mục Đích

File này là điểm đọc handoff hiện tại cho agent hoặc ChatGPT khi cần tiếp tục
work trên AICOS. Nó là index ngắn, không phải lịch sử đầy đủ và không phải nơi
dump mọi thay đổi nhỏ.

`brain/projects/aicos/working/handoff/current.md` là sole current handoff index
cho `projects/aicos`.

## Quy Ước Hiện Tại

- H1 current handoff index của project: file này.
- H2 episodic handoff notes: `brain/projects/aicos/working/handoff/episodes/`.
- H3 self-brain digest: các file ngắn trong `brain/projects/aicos/working/`.
- `brain/projects/aicos/working/handoff-summary.md` chỉ là digest/reference phụ,
  không phải startup authority và không ngang quyền với file này.
- `docs/migration/` giữ implementation notes, migration notes, và provenance.
  Không dùng làm nhà mặc định lâu dài cho active project handoff.
- Handoff cũ đã được move vào `backup/handoff-provenance-20260418/` để kiểm tra
  khi cần; không nằm trên đường đọc startup.

## Newest / Current

- Active handoff lane đã được chuẩn hóa mềm từ `docs/migration/` sang
  `brain/projects/aicos/working/handoff/current.md`.
- Startup vẫn theo hướng packet-first và index-first: không load toàn bộ docs,
  handoffs, rules, hoặc task packets khi chưa có task cụ thể.
- Task packet chỉ load đầy đủ khi task đã được chọn hoặc strongly implied.
- `./aicos context start A2-Core-C projects/aicos` tồn tại ở MVP form.
- `./aicos sync brain` là serving/retrieval refresh cho `brain/`, không mutate
  truth và không promote state.
- `./aicos option choose` đã có MVP flow để ghi manager choice vào structured
  state.
- Handoff-ready task metadata đã được normalize mỏng vào task packet template,
  A2 task-state convention, và các task packets hiện có; không tạo transfer
  subsystem riêng.
- CHK-26216 real-project readiness pass đã tạo shared onboarding foundation,
  minimum viable A1 branch, test templates, và `sample-project`
  first-project foundation.
- A1-26224 đã được normalize vào A1 startup/rule/task conventions: A1 core
  generic, rule layers tách bạch, continuation metadata rõ hơn, và future
  company/workspace layers được giữ như extension points.
- A1-26233 đã refine A1 thành artifact-neutral: coding vẫn được hỗ trợ, nhưng
  A1 core không mặc định repo/code/git/commit là mô hình universal.
- IMP-26249/BRG-26250 pass đã tạo scaffold cho `sample-project` first
  cross-repo test và local MCP bridge contract mỏng. MCP local bridge hiện đã
  có read/write surface; sample project đã được promoted thành active AICOS-managed
  project.
- KIT-26261 pass đã tạo shared Import Kit templates tại
  `brain/shared/templates/project-import-kit/`. Đây là reusable foundation,
  chưa phải sample project instantiation và chưa phải import execution.
- IMP-26269/KIT audit pass đã refine shared Import Kit cho full active context
  import + isolated checkout, và instantiate sample project import execution hub tại
  `brain/projects/sample-project/evidence/import-kit/`. sample project import kit
  hiện là provenance/reference after promotion, không phải startup lane.
- Context ladder pass đã thêm A2-Core, A2-Serve placeholder, A1, và project
  context ladders để agent mới có front door + overview trước khi đọc sâu.
- MCP Phase 1 read-serving pass đã thêm contract + operations layer +
  local stdio adapter mỏng cho `aicos_get_startup_bundle`,
  `aicos_get_handoff_current`, `aicos_get_packet_index`, và
  `aicos_get_task_packet`.
- MCP Phase 2 write-tool pass đã thêm semantic tools:
  `aicos_record_checkpoint`, `aicos_write_task_update`,
  `aicos_write_handoff_update`, `aicos_update_status_item`, và
  `aicos_register_artifact_ref`. Đây là lane-aware continuity writeback, không
  phải generic raw file edit API.
- MCP actor identity/lane metadata pass đã làm semantic writes áp dụng chung
  cho A1 và A2: mọi write phải có `actor_role`, `agent_family`,
  `agent_instance_id`, `work_type`, và `work_lane`. `work_branch`/`worktree_path`
  là code metadata, trong đó `worktree_path` bắt buộc khi `work_type=code`;
  content/design/research/ops dùng `artifact_scope` và `artifact_refs`. Startup
  bundle expose `active_task_state` để agent mới thấy các lane/worktree song
  song trước khi chọn việc.
- Shared coordination policy hiện nằm tại
  `brain/shared/policies/agent-coordination-policy.md`; hot paths nên trỏ tới
  policy này thay vì copy dài rule vào nhiều nơi.
- Worktree coordination rule hiện áp dụng cho mọi agent instance: cùng
  `agent_family` không có nghĩa được sửa chung worktree. Reuse worktree chỉ hợp
  lệ khi cùng lane và có completed/handoff-ready, explicit handoff,
  human-approved takeover, review, hoặc pair-work.
- Worktree mới nên được tạo/dùng cho parallel implementation, khác `work_lane`,
  khác branch, dirty state chưa rõ, hoặc nguy cơ sửa cùng file. Existing
  worktree chỉ reuse cho continuation, handoff, review, takeover, hoặc pair-work.
- Agent front-door refresh đã cập nhật `AGENTS.md`, A1/A2 onboarding ladders,
  và project context ladders để agent mới biết đọc overview ở đâu, đọc sâu ở
  đâu, và khi nào dùng MCP-first thay vì raw AICOS file access.
- MCP status-item pass đã thêm `aicos_update_status_item` để agent có thể cập
  nhật trạng thái open item, open question, tech debt, hoặc decision follow-up
  theo `item_id` ổn định thay vì append handoff section gây noise. Startup
  bundle expose `active_status_items` và `recent_status_items`.
- MCP contract/schema currently is `0.5`
  (`mcp-v0.6-write-contract-ack`). Any agent that cached MCP tools before this
  change should refresh `tools/list` or restart/re-enable AICOS MCP before
  writing.
- MCP query now has three tiers: HTTP daemon + PostgreSQL hybrid search with
  pgvector embeddings when available, PostgreSQL FTS fallback, and
  markdown-direct fallback for local/stdout or missing PG.
- Retrieval freshness now has explicit observability: `./aicos brain status`
  reports GBrain sync freshness, PG index freshness, embedding freshness,
  coverage, and missing/stale embeddings. `./aicos sync brain` defaults to full
  GBrain import; `--text-only` is the explicit opt-out.
- HTTP daemon no longer blocks startup on embedding every document. It indexes
  text/FTS first, serves immediately, and runs embedding refresh in a background
  pass when PG/pgvector/OpenAI config is available.
- Pass 4-7 added ADR-001 truth-store strategy, shared project registry,
  cross-project context policy, role-aware serving policy, project health,
  feedback digest, and structured feedback writes.
- Roadmap reconciliation on 2026-04-23 closed stale ARCH-R-03/ARCH-R-06,
  deferred A2-Serve graduation criteria per user instruction, added minimal
  policy-candidate/workstream-proposal lanes, hardened LAN daemon token
  behavior, and added `aicos install cli`.
- GBrain review continuation on 2026-04-24 did not restart from scratch. It
  reused automation-produced checkpoint/feedback and added a concrete gap map:
  `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`.
  Current judgment: AICOS has already reused the right low-risk pieces from
  GBrain, but still lacks strong retrieval eval discipline, direct-get object
  fetch, chunk-aware retrieval for long docs, and relation-aware serving beyond
  audit-only adjacency.
- CTO substrate review on 2026-04-24 added a stronger strategic judgment:
  `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`.
  Current recommendation is not "replace AICOS with GBrain", but to evaluate
  AICOS as a thinner semantic/control-plane layer over a more GBrain-derived
  retrieval/runtime substrate, with explicit keep/migrate/retire inventory
  before any deeper migration.
- Co-founder/product framing review on 2026-04-28 added a clearer problem
  statement:
  `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`.
  Current judgment: AICOS exists to stop operational context breakdown in
  multi-agent project work. It should not collapse into a generic memory/search
  product, but it also should not keep building substrate layers that partners
  already handle better.
- Option C north-star architecture on 2026-04-28 added a clearer long-term
  target:
  `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`.
  Current judgment: the future shape should be semantic core + runtime services
  + provider layers + deployment profiles + packs, with future support for
  human+AI shared dashboards through integrations rather than turning AICOS into
  a PM tool clone. Deployment profiles are now framed as `solo`, `small-team`,
  `company-100`, and future `enterprise`; the current GBrain + PG hybrid +
  HTTP MCP + team auth path should be treated as a substrate bundle inside the
  `small-team` profile.

## Still Current

- `brain/` là durable project/system reality.
- `agent-repo/` là actor operations, tasks, rules, và packets; không phải
  project truth.
- `backend/` và GBrain/PGLite là substrate/index/runtime support; không phải
  authority layer.
- A2-Core đang active để sửa AICOS. A2-Serve vẫn là future/runtime target, chưa
  active đầy đủ.
- No UI, public API, hoặc full orchestration runtime trong scope hiện tại.

## Backup / Không Đọc Mặc Định

- Các handoff files cũ đã được move vào `backup/handoff-provenance-20260418/`.
  Chỉ đọc khi cần audit/provenance, không dùng để khởi động agent mới.
- Bất kỳ câu nào nói `aicos sync brain` chỉ là preflight đều stale.
- Bất kỳ câu nào nói `context start` chỉ là hypothetical đều stale.
- Bare command `aicos ...` works after running `./aicos install cli` into a
  PATH directory. Without that install, use `./aicos ...` in the repo local.

## Current CLI Surface Ngắn

```text
./aicos context start A2-Core-C projects/aicos
./aicos capsule build project aicos
./aicos option generate <project-id> <blocker-id>
./aicos option choose <project-id> <blocker-id> <option-id>
./aicos mcp read startup-bundle --actor A1 --scope projects/<project-id>
./aicos mcp read packet-index --actor A1 --scope projects/<project-id>
./aicos mcp read task-packet --actor A1 --scope projects/<project-id> --packet-id <packet-id>
./aicos mcp read status-items --actor A1 --scope projects/<project-id>
./aicos mcp read workstream-index --actor A1 --scope projects/<project-id>
./aicos mcp read project-registry --actor A1 --scope projects/<project-id>
./aicos mcp read project-health --actor A1 --scope projects/<project-id>
./aicos mcp read feedback-digest --actor A1 --scope projects/<project-id>
./aicos mcp read query-project-context --actor A1 --scope projects/<project-id> --query "<query>"
./aicos mcp write record-checkpoint '<json-payload>'
./aicos mcp write task-update '<json-payload>'
./aicos mcp write handoff-update '<json-payload>'
./aicos mcp write status-item '<json-payload>'
./aicos mcp write artifact-ref '<json-payload>'
./aicos mcp write feedback '<json-payload>'
./aicos install cli --bin-dir ~/.local/bin
./aicos sync brain
./aicos sync brain --text-only
./aicos brain status
```

## Open Follow-Ups

- Có cần audit handoff backup để trích thêm nội dung còn giá trị vào self-brain
  mới không?
- Khi nào `context start` nên mở rộng ngoài `A2-Core-C` / `projects/aicos`?
- Khi nào task packet metadata đủ chín để thêm registry/summary giàu hơn?
- Chuẩn hóa project intake/import flow thành MCP tools/template cho project mới
  và existing-project import.
- Chạy LAN/team MCP usage test thật từ máy hoặc checkout khác, sau đó quyết
  định session/audit/deployment hardening tiếp theo.
- Validate full PG+pgvector+embedding runtime on a configured machine and tune
  cost/rate-limit policy for background embedding refresh.
- Review status-items đang open tại
  `brain/projects/aicos/working/status-items/`, đặc biệt ARCH-R-01 đến
  ARCH-R-10.
- Use the new GBrain gap map to choose the next search pass instead of broad
  re-review: eval corpus/benchmark first, then direct-get/chunking/relation
  serving only if justified.
- Use the substrate decision memo to guide next architecture passes: inventory
  current custom substrate, identify what remains AICOS-owned semantics, and
  test substrate reduction first on retrieval/runtime rather than on broad
  schema changes.
- Use the new product framing note before approving more architecture work:
  check whether a proposed feature strengthens AICOS as a context
  control-plane, or merely grows AICOS into a broader memory platform.
- Use the Option C north-star before approving large runtime/UI work: prefer
  profile/provider modularization and task/coworker semantics first, then
  dashboard integration later.
- Use the Option C transition checklist to sequence execution: first stabilize
  the current HTTP operating surface, then module inventory, semantic-core
  extraction, provider boundaries, profile formalization, and only later
  coworker/dashboard integration work.
- Keep the actor-model normalization work visible while doing that checklist:
  `A1` / `A2` should stay an AICOS-internal maintenance model, while projects
  using AICOS should be free to express their own functional roles and service
  roles without inheriting AICOS taxonomy by accident.
- Treat the following as the current Phase 0 anchor set before wider refactors:
  product framing / build-vs-buy memo, execution decision table, Option C
  north-star, and Option C transition checklist. If a new proposal conflicts
  with one of these, resolve that conflict explicitly instead of silently
  drifting.
- Phase 0.5 has reached a good-enough transition point. The stabilization note is at
  `brain/projects/aicos/evidence/research/aicos-phase-0-5-stabilization-pass-20260428.md`;
  the working compatibility matrix is at
  `brain/projects/aicos/working/mcp-client-compatibility-matrix.md`. Current
  state: HTTP MCP token/read/write paths pass at daemon level for the main
  tokens, PostgreSQL hybrid search is restored and fresh, and real client-level
  smoke should continue opportunistically as A1s use the system.

## Next Agent Notes

- Đừng dùng `current-state.md` làm inbox.
- Đừng đọc toàn bộ `docs/New design/` hoặc `docs/migration/` ở startup.
- Đừng đọc `backup/handoff-provenance-20260418/` trừ khi human yêu cầu audit
  hoặc cần đối chiếu migration history.
- Nếu chưa có task cụ thể, đọc orientation + packet index rồi hỏi human muốn
  tiếp tục việc nào.
- Nếu agent mới chưa biết đọc ở đâu, bắt đầu từ ladder phù hợp:
  `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
  hoặc `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`.
- Nếu là A1 và cần đọc/ghi AICOS-facing context/control-plane, dùng HTTP daemon
  MCP path như đường mặc định. Không fallback sang direct AICOS markdown writes
  chỉ vì tiện; mục tiêu là để friction thật được phát hiện và sửa. Chỉ
  `A2-Core-R` và `A2-Core-C` mới có thể fallback sang direct file writes khi
  MCP HTTP thật sự bị block hoặc khi restructuring nội bộ AICOS yêu cầu.
- Nếu cần đổi trạng thái open item/open question/tech debt/decision follow-up,
  dùng `aicos_update_status_item`; không append handoff section để thay thế.
- Khi có lỗi Phase 0.5 mới, bắt đầu từ compatibility matrix thay vì review lại
  từ đầu. Việc còn lại là real-client smoke cho Codex Desktop, Claude Code,
  Claude Desktop, Antigravity, và OpenClaw/mjnclaw khi các agent đó tiếp tục
  dùng AICOS. Không giữ Phase 1 bị block chỉ vì chưa có đủ real-client smoke.
- Nếu cần provenance của normalization storage/handoff, xem
  `docs/migration/STR-26185_storage_structure_implementation_note.md`.
- Nếu cần provenance của handoff-ready task metadata, xem
  `docs/migration/HMD-26210_handoff_ready_task_metadata_implementation_note.md`.
- Nếu cần provenance của real-project readiness pass, xem
  `docs/migration/CHK-26216_real_project_readiness_implementation_note.md`.
- Nếu cần provenance của A1 identity/layered-rules pass, xem
  `docs/migration/A1-26224_a1_identity_layered_rules_implementation_note.md`.
- Nếu cần provenance của A1 artifact-neutral pass, xem
  `docs/migration/A1-26233_a1_artifact_neutral_implementation_note.md`.
- Nếu cần provenance của sample project import/MCP bridge scaffold, xem
  `docs/migration/IMP-26249_BRG-26250_btc_import_bridge_scaffold_note.md`.
- Nếu cần provenance của shared Import Kit templates, xem
  `docs/migration/KIT-26261_import_kit_template_system_note.md`.
- Nếu cần provenance của IMP-26269 kit audit/readiness pass, xem
  `docs/migration/IMP-26269_KIT_AUDIT_import_readiness_note.md`.
- Nếu cần provenance của MCP Phase 1 read-serving pass, xem
  `docs/migration/MCP_PHASE1_READ_SERVING_20260419.md`.
- Nếu cần provenance của MCP Phase 2 write tools pass, xem
  `docs/migration/MCP_PHASE2_WRITE_TOOLS_20260419.md`.
- Nếu cần provenance của agent onboarding/front-door refresh, xem
  `docs/migration/AGENT_ONBOARDING_FRONT_DOOR_REFRESH_20260419.md`.

## Recent Continuity Digest

Detailed MCP continuity blocks were compacted on 2026-04-21 to keep this file an
H1 current handoff index instead of an append-only log.

- `sample-project` is the active project name. Old "Crypto Trading"
  follow-ups about slice selection/import truth are resolved in
  `projects/sample-project`.
- The MCP status-item capability gap is resolved. Use
  `aicos_update_status_item` and
  `brain/projects/<project-id>/working/status-items/` for open item/open
  question/tech debt/decision follow-up lifecycle updates.
- Architecture review items are tracked as structured status-items:
  `brain/projects/aicos/working/status-items/arch-r-01.md` through
  `arch-r-10.md`.
- Handoff compaction itself remains tracked by ARCH-R-01 until a reusable
  command or policy exists.

## MCP Continuity Update: 20260422T032925Z-47a106395b

Status: `completed`
Write id: `20260422T032925Z-47a106395b`
Written at: `2026-04-22T03:29:25+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `charming-nobel-eeb666`
Agent display name: `unknown`
Work type: `code`
Work lane: `aicos-mcp-daemon-http-pg-search`
Coordination status: `handoff_ready`
Artifact scope: `unspecified`
Work branch: `feat/pg-search-engine`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Two branches pushed. Merge `feat/pg-search-engine` (superset): HTTP daemon (ThreadingHTTPServer + TTL cache) + pg_search package (schema/indexer/intent/engine). Vietnamese-safe 'simple' FTS. Authority boost (canonical=2.0, handoff=1.5). Freshness penalty (stale=0.5×). Graceful PG fallback. Docker Compose included. pgvector-ready for Phase 3. `feat/mcp-daemon-http-cache` is redundant after this merge. See integrations/mcp-daemon/README.md for merge notes.

### Next Step

Codex merges `feat/pg-search-engine` into main. `docker compose up -d`, `pip install psycopg2-binary`, start daemon. Verify /health → search_engine=postgresql_fts.

### Trace Refs

- artifact_refs:
  - `feat/pg-search-engine`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/`
  - `integrations/mcp-daemon/docker-compose.yml`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T040902Z-1a815741a2

Status: `completed`
Write id: `20260423T040902Z-1a815741a2`
Written at: `2026-04-23T04:09:02+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `claude-code`
Agent instance id: `claude-code-ops-20260423-infra`
Agent display name: `unknown`
Work type: `ops`
Work lane: `local-infra-setup`
Coordination status: `handoff_ready`
Artifact scope: `PostgreSQL + LaunchAgents + MCP client config + install docs`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `unknown`
Legacy actor family: `claude-code`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Ops session 2026-04-23: fixed Claude Desktop config (merged duplicate mcpServers keys); Claude Desktop now uses aicos_mcp_stdio.py. Claude Code CLI uses aicos_mcp_http_first.py (HTTP-first, stdio fallback). Postgres.app installed locally (DB aicos, user aicos, pgvector 0.8.1, port 5432). LaunchAgents created for mcp-daemon and https-proxy (ports 8000/8443). mkcert TLS cert installed. scripts/aicos-daemon-start.sh created (PG-wait wrapper for LaunchAgent). Fixed pg_search indexer scope bug (README.md guard). Created docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md.

### Next Step

Codex: implement SSE transport in aicos_mcp_daemon.py (item IMPL-MCP-DAEMON-SSE) so Claude Desktop custom connector works on LAN. See status item for test steps and spec link.

### Trace Refs

- none

### Notes

Current LAN status: HTTP daemon on port 8000 serves LAN agents via claude mcp add --transport http. Claude Desktop requires SSE (GET /mcp → text/event-stream) which is not yet implemented. HTTPS proxy on 8443 is ready to forward once daemon adds SSE. No token configured in current local setup (trusted home network). OPENAI_API_KEY not set — pgvector active but no embeddings yet.

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T082055Z-103a6894d8

Status: `ready_for_next`
Write id: `20260423T082055Z-103a6894d8`
Written at: `2026-04-23T08:20:55+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-lan-review`
Agent display name: `unknown`
Work type: `review`
Work lane: `mcp-daemon-lan-review`
Coordination status: `handoff_ready`
Artifact scope: `LAN daemon review and portability cleanup`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Reviewed Claude Code LAN experiment checkpoint. Accepted direction: LaunchAgent namespace standardized to `ai.aicos.*`, LAN helper rewritten as portable repo-relative script, and LAN host remains env/config driven rather than hardcoded. Not yet promoted: query-string token auth; recorded as open question `RISK-QUERY-TOKEN-AUTH` pending human decision because of URL leakage risk.

### Next Step

If approved, Codex can either remove query-token auth entirely or keep it behind an explicit off-by-default config flag. Current repo cleanup for labels/helper/docs is already applied.

### Trace Refs

- artifact_refs:
  - `brain/projects/aicos/evidence/checkpoints/20260423t075745z-7e7f55ba2c.md`
  - `integrations/mcp-daemon/start-lan.sh`
  - `scripts/aicos-install-launchagents`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/mcp-daemon/README.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T083328Z-65732cd0d3

Status: `ready_for_next`
Write id: `20260423T083328Z-65732cd0d3`
Written at: `2026-04-23T08:33:28+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-query-token-reject`
Agent display name: `unknown`
Work type: `review`
Work lane: `mcp-daemon-security-review`
Coordination status: `handoff_ready`
Artifact scope: `Claude LAN experiment review and rejection of query-token auth`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Query-token auth workaround from Claude's LAN experiment was explicitly rejected by human and removed from daemon auth. Accepted cleanup remains: `ai.aicos.*` LaunchAgent namespace, portable LAN helper, and env-driven host binding. Follow-up captured as open item `AICOS-MCP-SSE-AUTH-INTEROP` for a safer long-term interoperability design for SSE clients that cannot attach headers.

### Next Step

Do not reintroduce URL token auth. Next architecture pass should choose a safer interop design such as short-lived session bootstrap, local sidecar header injection, or a fuller streamable HTTP implementation.

### Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `brain/projects/aicos/working/status-items/risk-query-token-auth.md`
  - `brain/projects/aicos/working/status-items/aicos-mcp-sse-auth-interop.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T085948Z-ce1ac39395

Status: `ready_for_next`
Write id: `20260423T085948Z-ce1ac39395`
Written at: `2026-04-23T08:59:48+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-ops-hardening`
Agent display name: `unknown`
Work type: `code`
Work lane: `ops-stability`
Coordination status: `handoff_ready`
Artifact scope: `ops hardening, monitor, persistent logs, portable proxy defaults`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Implemented the next ops hardening pass: persistent logs moved into LaunchAgent installer paths under ~/Library/Logs/aicos, a local health monitor script and LaunchAgent were added, log trimming is now part of monitor runs, HTTPS proxy defaults were made portable, and docs/install/README were updated. Current machine runtime still needs an out-of-sandbox restart/reload of LaunchAgents to pick up the new daemon/monitor/proxy behavior.

### Next Step

From a normal host shell, run scripts/aicos-install-launchagents, then verify ai.aicos.mcp-daemon and ai.aicos.health-monitor are loaded, health-status.json updates every 60s, and restart/reindex the daemon so brain status is no longer stale.

### Trace Refs

- artifact_refs:
  - `scripts/aicos-install-launchagents`
  - `integrations/mcp-daemon/aicos_health_monitor.py`
  - `integrations/mcp-daemon/aicos_https_proxy.py`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/mcp-daemon/README.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T090305Z-9358388a05

Status: `ready_for_next`
Write id: `20260423T090305Z-9358388a05`
Written at: `2026-04-23T09:03:05+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-vm-lan-setup`
Agent display name: `unknown`
Work type: `ops`
Work lane: `vm-lan-connectivity`
Coordination status: `handoff_ready`
Artifact scope: `VM/OpenClaw LAN connectivity setup`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Prepared AICOS local config for VM/LAN access. Local daemon env now uses non-loopback LAN bind (`AICOS_DAEMON_HOST=0.0.0.0`) and the portable LAN helper prints the detected macOS VM bridge URL (`bridge100`, currently 192.168.64.1) so a VM agent such as OpenClaw can connect like a LAN client. The host shell still needs a real restart of the daemon/LaunchAgents outside sandbox for the running process to pick up this config.

### Next Step

From the host shell, restart the daemon or rerun scripts/aicos-install-launchagents, then configure the VM agent to use http://192.168.64.1:8000/mcp with Authorization: Bearer <AICOS_DAEMON_TOKEN>.

### Trace Refs

- artifact_refs:
  - `.runtime-home/aicos-daemon.env`
  - `integrations/mcp-daemon/start-lan.sh`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T091740Z-9e968395ca

Status: `ready_for_next`
Write id: `20260423T091740Z-9e968395ca`
Written at: `2026-04-23T09:17:40+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-vm-connect-guide`
Agent display name: `unknown`
Work type: `content`
Work lane: `vm-lan-connectivity`
Coordination status: `handoff_ready`
Artifact scope: `VM agent HTTP MCP quick-connect guide`
Work branch: `unknown`
Worktree path: `<AICOS_PRIVATE_REPO>`
Execution context: `unknown`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Added a dedicated operator-facing quick-connect guide for VM agents: docs/install/AICOS_VM_AGENT_HTTP_MCP_CONNECT.md. It contains the current VM bridge URL pattern, bearer-header requirement, Codex form values, Claude/OpenClaw-style setup snippets, first MCP reads, and host-side restart steps. The main install guide and OpenClaw integration now point to this file as the front door for VM/remote attach-only workflows.

### Next Step

When a human wants another VM agent to connect, send this one file instead of the full install runbook: docs/install/AICOS_VM_AGENT_HTTP_MCP_CONNECT.md.

### Trace Refs

- artifact_refs:
  - `docs/install/AICOS_VM_AGENT_HTTP_MCP_CONNECT.md`
  - `docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`
  - `integrations/openclaw/README.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T125615Z-f10802301f

Status: `partial`
Write id: `20260423T125615Z-f10802301f`
Written at: `2026-04-23T12:56:15+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-next-priorities`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-next-priorities`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Current next priorities after read-identity/audit rollout: keep audit logs queryable from CLI, continue LAN security hardening, and design the cleaner SSE/HTTP interoperability path while preserving fresh hybrid search.

### Next Step

Implement audit CLI/query first, then harden LAN ingress with low-cost controls before returning to broader SSE/interop design.

### Trace Refs

- artifact_refs:
  - `brain/projects/aicos/working/status-items/AICOS-AUDIT-OBSERVABILITY-CLI.md`
  - `brain/projects/aicos/working/status-items/AICOS-SEARCH-EVAL-QUALITY.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T130001Z-e0ee14417f

Status: `partial`
Write id: `20260423T130001Z-e0ee14417f`
Written at: `2026-04-23T13:00:01+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-desktop-a2-core-20260423-next-pass`
Agent display name: `unknown`
Work type: `planning`
Work lane: `aicos-next-priorities`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Freshness is currently healthy (`brain status` fresh for GBrain/PG/embedding). Audit observability now has a usable CLI and daemon-side audit correlation. LAN hardening gained token labels plus optional IP/CIDR allowlist, but broader HTTPS/session/fallback work remains open.

### Next Step

Use the new audit CLI for real incident/debug loops, then continue with safer SSE/HTTP interoperability and broader LAN fallback/security work.

### Trace Refs

- artifact_refs:
  - `brain/projects/aicos/working/status-items/AICOS-AUDIT-OBSERVABILITY-CLI.md`
  - `brain/projects/aicos/working/status-items/AICOS-LAN-SECURITY-HARDENING.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T130616Z-0073b72b69

Status: `ready_for_next`
Write id: `20260423T130616Z-0073b72b69`
Written at: `2026-04-23T13:06:16+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-runtime-hardening`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Freshness/runtime pass completed: brain sync and PG index are fresh again, audit summary CLI is live, and daemon health now publishes auth capabilities plus supported client profiles to reduce connector confusion.

### Next Step

Continue with LAN security baseline: decide whether to enable allowlist by default for LAN mode and write a minimal auth/audit operating policy for non-local clients.

### Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/kernel.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/README.md`
  - `<AICOS_PRIVATE_REPO>/docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T140526Z-6e87ef47a9

Status: `ready_for_next`
Write id: `20260423T140526Z-6e87ef47a9`
Written at: `2026-04-23T14:05:26+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-learning-loop`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Learning-loop MVP is live: startup/project-health now nudge first-contact or repeated-friction feedback, write results can nudge session-close feedback, and operators can review recurring signals with ./aicos feedback summary.

### Next Step

Watch real agent usage, then tighten promotion rules from feedback into status items/tool candidates if recurring patterns appear.

### Trace Refs

- artifact_refs:
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/mcp_read_serving.py`
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `<AICOS_PRIVATE_REPO>/packages/aicos-kernel/aicos_kernel/kernel.py`
  - `<AICOS_PRIVATE_REPO>/integrations/mcp-daemon/README.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T162532Z-c27be15c5c

Status: `ready_for_next`
Write id: `20260423T162532Z-c27be15c5c`
Written at: `2026-04-23T16:25:32+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-runtime-hardening`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Stabilized daemon health monitoring and token operations. Added labeled tokens for antigravity plus two reserved spares in local secret storage, hardened /health so PG stats failures degrade instead of crashing the endpoint, and changed monitor behavior to alert once per outage then emit recovery instead of repeating noise every cycle.

### Next Step

Commit and push the AICOS runtime hardening/docs changes, then use the new antigravity token for VM/LAN MCP setup as needed.

### Trace Refs

- artifact_refs:
  - `integrations/mcp-daemon/aicos_health_monitor.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `packages/aicos-kernel/aicos_kernel/pg_search/engine.py`
  - `.runtime-home/aicos-daemon-token-registry.json`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260423T170301Z-0f57e8e63e

Status: `ready_for_next`
Write id: `20260423T170301Z-0f57e8e63e`
Written at: `2026-04-23T17:03:01+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-current`
Agent display name: `unknown`
Work type: `ops`
Work lane: `aicos-learning-loop`
Coordination status: `active`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``

### Summary

Added feedback-closure gating to the learning loop. Session-close MCP writes now require one prior feedback closure for the same scope + agent_family + agent_instance_id + work_lane, and agents can satisfy it with either a real issue or feedback_type=no_issue. Error responses point to a quick no_issue example so external agents can recover without guessing.

### Next Step

Reload HTTP MCP clients if they cache tool schemas, then observe whether new agent sessions actually record no_issue or real feedback before closing work.

### Trace Refs

- artifact_refs:
  - `packages/aicos-kernel/aicos_kernel/mcp_write_serving.py`
  - `integrations/mcp-daemon/aicos_mcp_daemon.py`
  - `docs/install/AICOS_MCP_WRITE_COOKBOOK.md`
  - `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.

## MCP Continuity Update: 20260428T155840Z-ca7b6c9767

Status: `ready_for_next`
Write id: `20260428T155840Z-ca7b6c9767`
Written at: `2026-04-28T15:58:40+00:00`

### Actor Identity

Actor role: `A2-Core-C`
Agent family: `codex`
Agent instance id: `codex-thread-20260428-cto-overall-review`
Agent display name: `Codex Desktop`
Work type: `planning`
Work lane: `cto-overall-review`
Coordination status: `completed`
Artifact scope: `unspecified`
Work branch: `unknown`
Worktree path: `unknown`
Execution context: `codex-desktop`
Legacy actor family: `codex`
Legacy logical role: `A2-Core-C`
Work context: ``
Runtime: `private-local-aicos`
MCP name: `aicos_http`
Agent position: `internal_agent`
Functional role: `AICOS CTO/maintainer`
Runtime identity map:
```json
{
  "identity_private": {
    "actor_role": "A2-Core-C",
    "agent_position": "internal_agent",
    "functional_role": "AICOS CTO/maintainer",
    "mcp_name": "aicos_http",
    "project_scope": "projects/aicos",
    "runtime": "private-local-aicos"
  }
}
```

### Summary

Trace Ref hygiene and relation audit cleanup are complete and pushed at commit 3ad7c51. AICOS/sample project relation audits now have 0 broken source refs; scope_refs/session_refs are supported in parsing/write schema; retrieval gate passes 57/59 top3 and 59/59 top5. Current CTO view: running surface is stable enough; next product/architecture work should focus on keep/reuse/migrate/retire inventory and security/runtime decisions, not adding graph/dashboard prematurely.

### Next Step

From CTO view, do one of two tracks next: (1) create concrete keep/reuse/migrate/retire inventory for current modules/substrates; or (2) if preparing wider team usage, harden LAN/HTTPS/SPOF decisions. Keep aicos_get_related_context deferred until real adjacency misses appear.

### Trace Refs

- artifact_refs:
  - `3ad7c51 Normalize trace refs for relation audit`

### Notes

none

Boundary: MCP semantic handoff update; compact current continuity only.
