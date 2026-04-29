# Trạng Thái Hiện Tại Của AICOS

Trạng thái: self-brain/working-state đang được chuẩn hóa.

## Tóm Tắt

AICOS đã được chuyển sang active root mới. Trạng thái cũ của `main` được giữ ở
remote branch `backup/pre-restructure-main`; local backup/runtime material không
được dùng làm startup truth.

Active root hiện gồm:

- `brain/`
- `agent-repo/`
- `packages/aicos-kernel/`
- `serving/`
- `backend/`
- `integrations/`
- `docs/architecture/`
- `docs/install/`
- `tools/gbrain/`

## Đã Có

- `brain/projects/aicos/` làm self-brain cho chính AICOS.
- `agent-repo/` tách A1, A2, humans, future class.
- `packages/aicos-kernel/` có schemas, contracts, CLI mỏng.
- `serving/` có generated capsules, option packets, branch compare, promotion
  review packets.
- `backend/` là substrate scaffold, chưa là truth.
- `./aicos` CLI đã chạy được các command MVP.
- A2-Core có startup card, rule cards ngắn, và task packet template tối thiểu
  để hỗ trợ packet-first loading.
- A2-Core/A1 context ladders đã có để external co-workers như Codex, Claude
  Code, OpenClaw, hoặc ChatGPT vào đúng đường đọc tối thiểu trước khi đọc sâu.
- Root `AGENTS.md` hiện trỏ agent mới về actor context ladders trước: A2-Core,
  A2-Serve placeholder, hoặc A1. Project nào có `working/context-ladder.md`
  thì dùng ladder đó để hiểu tổng quan trước khi đọc sâu.
- `./aicos context start A2-Core-C projects/aicos` đã chạy được ở MVP scope.
- Continuity authority khi cần handoff:
  `brain/projects/aicos/working/handoff/current.md`.
- Task packets và A2 task-state convention đã có metadata mỏng để task dễ
  handoff hơn mà không cần transfer/takeover subsystem riêng.
- Real-project readiness foundation đã có: shared checkpoint policy,
  onboarding templates, minimum viable A1 branch, và `sample-project`
  first-project promotion.
- A1 layered-rules model đã được chuẩn hóa nhẹ: A1 core, future
  company/workspace layers, project layer, và workstream/task layer được phân
  biệt mà chưa build governance framework lớn.
- A1 artifact-neutral model đã được refine: A1 core không mặc định là coding
  worker, hỗ trợ code/docs/design/content/research/hybrid artifacts qua task
  packet và work-context metadata.
- Sample Project đã được promoted thành active AICOS-managed project:
  AICOS là context/control-plane authority, sample project repo là code/runtime authority,
  và sample project `shared-context/` là reference/history/provenance.
- Shared Import Kit template system đã được thêm ở
  `brain/shared/templates/project-import-kit/` để instantiate cho future
  cross-repo projects. sample project import kit hiện là provenance/reference sau promotion
  pass, không còn là active startup lane.
- Local MCP Phase 1 read-serving đã có operations layer + stdio adapter mỏng
  cho startup bundle, handoff/current, packet index, và selected task packet.
- Local MCP Phase 2 semantic write tools đã có operations layer + stdio wiring
  cho checkpoint, task update, handoff update, status-item update, và
  artifact-ref registration. Đây không phải raw file write API.
- MCP semantic writes hiện yêu cầu actor/work-lane identity cho mọi actor lane,
  gồm A1 và A2. Required identity gồm `actor_role`, `agent_family`,
  `agent_instance_id`, `work_type`, và `work_lane`; code work có thể thêm
  `work_branch` và phải có `worktree_path`, còn non-code work nên dùng
  `artifact_scope` và `artifact_refs`.
- MCP contract/schema hiện là `0.5`
  (`mcp-v0.6-write-contract-ack`). Agent đã cache MCP tools/schema trước thay
  đổi này phải refresh `tools/list` hoặc restart/re-enable AICOS MCP trước khi
  write. Contract `0.5` dùng `aicos_update_status_item` cho open items/open
  questions/tech debt/decision follow-ups và `aicos_register_artifact_ref` cho
  compact artifact refs.
- Shared coordination policy:
  `brain/shared/policies/agent-coordination-policy.md`.
- Startup bundle hiện expose `active_task_state` để agent mới thấy lane nào
  đang active/blocked/paused/completed, agent family nào đang làm, instance nào,
  và artifact/branch/worktree scope nào liên quan trước khi chọn việc.
- Startup bundle hiện expose thêm `active_status_items` và
  `recent_status_items` để agent thấy trạng thái open/resolved gần đây mà không
  phải đọc cả handoff dài.
- MCP read surface hiện có `aicos_query_project_context`,
  `aicos_get_status_items`, và `aicos_get_workstream_index`. Default local
  stdio vẫn là markdown-direct bounded query; HTTP daemon ưu tiên PostgreSQL
  hybrid search với pgvector embedding khi có `OPENAI_API_KEY`, fallback về
  PostgreSQL FTS rồi markdown-direct.
- MCP read/write surface hiện có thêm project registry, project health,
  feedback digest, và structured feedback write. Feedback là signal cải tiến
  service/context, không phải task continuity hoặc canonical truth.
- Relation hygiene hiện có MVP low-risk path: `./aicos audit relations`
  derives adjacency only from explicit Trace Refs and writes a derived audit
  index under `.runtime-home/aicos/`; markdown vẫn là truth.
- GBrain search reuse review hiện đã được mở rộng thành gap map cụ thể giữa
  GBrain và AICOS tại
  `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`.
  Judgment hiện tại: AICOS đã reuse đúng phần low-risk/high-value, nhưng vẫn
  còn thiếu retrieval eval discipline, direct-get object model, chunk-aware
  retrieval, và relation-aware serving.
- CTO-level substrate review now also exists at
  `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`.
  Current judgment: AICOS should remain the semantic/control-plane layer, but
  should evaluate reducing custom retrieval/runtime substrate work in favor of
  a more GBrain-derived substrate boundary.
- Co-founder-level product framing and build-vs-buy memo now exists at
  `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`.
  Current judgment: AICOS is a multi-agent project context control-plane, not
  merely a memory/search product. Short term it should avoid overclaiming
  "all company knowledge", but long term it should preserve a path for
  company/workspace knowledge that AI agents genuinely need.
- Option C architecture north-star now exists at
  `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`.
  Current judgment: AICOS should evolve toward a stable semantic core with
  runtime services, provider layers, deployment profiles, and
  company/workspace/project packs, rather than one fixed stack. Deployment
  profiles should be understood as `solo`, `small-team`, `company-100`, and
  future `enterprise`; the current GBrain + PG hybrid + HTTP MCP + team auth
  path is an implementation bundle inside the `small-team` profile, not the
  profile itself.
- Option C transition checklist now includes a dedicated Phase 0.5
  stabilization pass before deeper modularization. Current judgment: A1 agents
  should be forced onto the HTTP daemon path for AICOS-facing read/write
  operations so real MCP friction stays visible; only `A2-Core-R` and
  `A2-Core-C` may fall back to direct file writes when HTTP MCP is genuinely
  blocked or when restructuring internals requires it.
- Option C direction now also requires actor-model normalization. Current
  judgment: `A1` / `A2` should remain AICOS-internal maintenance taxonomy,
  while projects using AICOS may define their own functional roles and service
  roles. AICOS should not leak its own internal role taxonomy into every
  project it serves.
- Phase 0 direction-lock should now be treated as materially established:
  product framing, execution decision table, Option C north-star, and Option C
  transition checklist are the four main architecture anchors for near-term
  work. Future passes should update those anchors deliberately rather than
  drifting through ad hoc note sprawl.
- Phase 0.5 stabilization has reached a good-enough transition point.
  Health/token/tools/startup/read/write smoke passes at daemon level for the
  main labeled token paths. PostgreSQL hybrid search was restored through
  Postgres.app + daemon restart, `aicos_query_project_context` now returns
  hybrid FTS/vector results, and `./aicos brain status` reports GBrain sync,
  PG index, and embedding freshness as fresh. Remaining work should move with
  real client usage: real client UI/runtime confirmation is still pending, and
  the first concrete schema friction is that read bootstrap accepts
  `work_type=orientation`, while semantic writes currently require a write type
  such as `ops` or `planning`.
- `brain/shared/project-registry.md` là MVP discovery surface cho project known
  to AICOS. Cross-project context mặc định isolated; dùng shared policy trước
  khi lấy context từ project khác.
- ADR-001 đã chốt truth-store strategy hiện tại: markdown/agent-repo là source
  truth; DB/FTS/vector/cache/daemon là serving/index layer cho đến khi có
  migration trigger rõ.
- `worktree_path` là tín hiệu occupancy của checkout đang được dùng, không phải
  owner vĩnh viễn. Agent instance khác chỉ nên dùng lại cùng worktree khi tiếp
  tục cùng `work_lane` sau completed/handoff-ready, handoff rõ ràng, takeover,
  review, hoặc pair-work được human cho phép; rule này áp dụng cả giữa hai
  thread cùng `agent_family`.
- Tạo hoặc dùng worktree riêng cho parallel implementation, khác `work_lane`,
  khác branch, dirty state chưa rõ, hoặc nguy cơ sửa cùng file. Reuse worktree
  chỉ dành cho continuation, handoff, review, takeover, hoặc pair-work rõ ràng.
- A1 nên dùng MCP-first cho AICOS-facing context/control-plane read/write khi
  MCP khả dụng; direct local access vẫn đúng cho code/runtime/artifact work của
  project bên ngoài.
- Project intake/import hiện có MVP flow tách rõ project mới tinh và existing
  project import tại `brain/shared/templates/project-onboarding/project-intake-flow.md`.

## Flow Đã Chứng Minh

Đã chứng minh flow local:

```text
blocked -> options -> manager choice -> working state update
```

Nguồn chính:

- blocker: `agent-repo/classes/a1-work-agents/tasks/blocked/blocker-001.md`
- option packet: `serving/branching/option-packets/aicos__blocker-001.md`
- manager choice: `agent-repo/classes/humans/approvals/manager-choice-blocker-001.md`
- selected branch: `brain/projects/aicos/branches/blocker-001-option-a/`

## Context Delivery Đã Có

- Startup card: `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
- Rule cards: `agent-repo/classes/a2-service-agents/rule-cards/`
- Task packets: `agent-repo/classes/a2-service-agents/task-packets/`
- Task packet template:
  `packages/aicos-kernel/contracts/task-packet-template.md`
- Sole H1 current handoff index, chỉ đọc khi task cần continuation/alignment:
  `brain/projects/aicos/working/handoff/current.md`
- Old handoff provenance backup, không đọc mặc định:
  `backup/handoff-provenance-20260418/`
- Task packet index:
  `agent-repo/classes/a2-service-agents/task-packets/README.md`
- Real-project onboarding kit:
  `brain/shared/templates/project-onboarding/`
- Cross-repo Import Kit templates:
  `brain/shared/templates/project-import-kit/`
- AICOS project context ladder:
  `brain/projects/aicos/working/context-ladder.md`
- A1 onboarding ladder:
  `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`
- A2-Core onboarding ladder:
  `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
- MCP local bridge contract:
  `packages/aicos-kernel/contracts/mcp-bridge/local-mcp-bridge-contract.md`
- MCP integration guide:
  `integrations/local-mcp-bridge/README.md`
- Structured status items:
  `brain/projects/aicos/working/status-items/`
- Brain-level resolver:
  `brain/RESOLVER.md`
- Query/search guide:
  `docs/install/AICOS_QUERY_SEARCH_GUIDE.md`
- Detailed GBrain gap map:
  `brain/projects/aicos/evidence/research/aicos-gbrain-search-gap-map-20260424.md`
- GBrain substrate decision memo:
  `brain/projects/aicos/evidence/research/aicos-on-gbrain-substrate-decision-memo-20260424.md`
- Product framing / build-vs-buy memo:
  `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
- Option C architecture north-star:
  `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`
- Option C transition checklist:
  `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`
- Phase 0.5 stabilization pass:
  `brain/projects/aicos/evidence/research/aicos-phase-0-5-stabilization-pass-20260428.md`
- MCP client compatibility matrix:
  `brain/projects/aicos/working/mcp-client-compatibility-matrix.md`

## Context Loading Hiện Tại

AICOS đang chuyển sang mô hình packet-first:

- AICOS cung cấp role/rules/state/task packets và access paths đúng scope.
- AICOS không quản lý memory/context nội bộ của Codex, Claude Code, OpenClaw
  hoặc co-workers bên ngoài.
- Agent nên load hot context ngắn trước, rồi chỉ load rule cards hoặc source
  docs dài khi task thật sự cần.

## Chưa Active Đầy Đủ

- Retrieval freshness is now observable through `./aicos brain status`.
  `./aicos sync brain` defaults to full GBrain import and supports
  `--text-only` as an explicit opt-out. HTTP daemon indexes text first and runs
  embedding refresh in background when PG/pgvector/OpenAI config is available.
  Live PG+embedding validation still depends on runtime dependencies and keys.
- A2-Serve mới là target architecture, chưa là runtime lane đầy đủ.
- MCP HTTP daemon đã có mức LAN tối thiểu. Team/LAN mode phải chạy có token;
  auth/session/audit sâu và hosted/server deployment vẫn chưa active.
- UI và public API chưa làm.
- Chuẩn project intake/import đã có markdown MVP flow; chưa có dedicated MCP
  intake tools.
- Policy/rule promotion candidate và workstream proposal flow mới ở mức lane
  tối thiểu, chưa có lifecycle tool riêng.

## Manager Decision: blocker-001

Recorded at: `2026-04-18T04:15:56+00:00`

- Blocker: `blocker-001`
- Selected option: `option-a`
- Selected branch: `blocker-001-option-a`
- Manager choice packet: `agent-repo/classes/humans/approvals/manager-choice-blocker-001.md`
- Branch state: `brain/projects/aicos/branches/blocker-001-option-a/selection-state.md`

The project has a committed working direction for this blocker. Canonical truth remains unchanged until a separate promotion/review step.
