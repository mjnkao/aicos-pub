# Trạng Thái Implementation

Trạng thái: current implementation surface, cập nhật theo repo hiện tại.
Ngày cập nhật: 2026-04-21.

File này là bản tóm tắt tình trạng build/run của AICOS. Nó không thay thế
contract, source code, hay status-items; khi có conflict, ưu tiên contract/code
hiện tại và các status-items mới nhất.

## Active Runtime Surface

`./aicos` hiện có các nhóm command:

- `capsule`: build context capsules cho company/workspace/project/branch/actor.
- `branch`: compare branch reality.
- `option`: generate và commit manager choice.
- `promote`: review/copy giữa evidence, working, canonical.
- `validate`: deterministic checks cho capsule/branch.
- `context`: MVP startup context cho A2-Core/AICOS.
- `sync`: refresh `brain/` sang GBrain/PGLite serving substrate.
- `mcp`: debug/read/write surface cho local MCP context/control plane.
- `compact`: bounded compaction surface, hiện có `compact handoff`.

## Implemented AICOS Foundations

- Active root: `brain/`, `agent-repo/`, `packages/aicos-kernel/`, `serving/`,
  `backend/`, `integrations/`, `docs/`, `scripts/`, `tools/gbrain/`.
- `brain/projects/aicos/` là self-brain của AICOS.
- A1/A2/human actor structure đã có trong `agent-repo/`.
- A2-Core và A1 onboarding ladders đã là front door cho agent mới.
- Project context ladder đã có tại
  `brain/projects/aicos/working/context-ladder.md`.
- `sample-project` đã là active AICOS-managed project đầu tiên:
  AICOS giữ context/control-plane, external repo giữ code/runtime authority.
- Shared onboarding/import-kit templates đã có cho future projects.

## MCP / Context-Control Plane

Local MCP bridge hiện là active MVP surface, không còn chỉ là ý tưởng:

- Phase 1 read tools:
  `aicos_get_startup_bundle`, `aicos_get_handoff_current`,
  `aicos_get_packet_index`, `aicos_get_task_packet`,
  `aicos_get_status_items`, `aicos_get_workstream_index`,
  `aicos_query_project_context`.
- Phase 2 write tools:
  `aicos_record_checkpoint`, `aicos_write_task_update`,
  `aicos_write_handoff_update`, `aicos_update_status_item`,
  `aicos_register_artifact_ref`.
- Current write contract: `mcp-v0.6-write-contract-ack`.
- Startup bundle exposes:
  `active_task_state`, `recent_completed_task_state`, `active_status_items`,
  `recent_status_items`, and `continuity_signal`.
- Status/query reads hide stale/closed status-items by default; audit callers
  can opt in with `include_stale` or explicit filters.

## Verified / Exercised

- Project/branch capsule build for AICOS.
- Option packet and manager choice flow for `blocker-001`.
- Branch validation and promotion review packet generation.
- GBrain/PGLite text import from `brain/`.
- A2-Core startup bundle via `./aicos context start A2-Core-C projects/aicos`
  and MCP read debug surface.
- MCP semantic write paths for checkpoint, task update, handoff update,
  status-item update, and artifact-ref registration.
- Handoff compaction command exists for manual compaction of append-heavy
  current handoffs.

## Known Thin / Not Yet Mature

- Retrieval freshness observability now exists through `./aicos brain status`,
  `sync brain --text-only/--full`, PG index freshness, embedding coverage, and
  daemon health `search_status`. Full hybrid runtime validation still requires
  a machine with PostgreSQL/pgvector, Python PG driver, and embedding config.
- Markdown remains the authority store. This is productive for restructuring,
  but it has concurrency and conflict limits; ARCH-R-03 tracks the need for a
  truth-store ADR before scale.
- A2-Serve remains a target architecture, not an active runtime lane with
  graduation criteria. ARCH-R-04 tracks the activation trigger gap.
- Cross-project context propagation is not designed yet. ARCH-R-06 tracks the
  missing project registry/dependency/isolation policy.
- MCP query is bounded markdown-direct search, not semantic/vector-backed
  context intelligence. ARCH-R-07 and ARCH-R-02 are related.
- Status item type validation/guidance is still weak. ARCH-R-09 tracks the
  risk of noisy or misclassified project status.
- Bare `aicos ...` still has PATH friction; `./aicos ...` is the reliable local
  command form. ARCH-R-05 tracks this.
- UI, public API, remote/hosted MCP, auth/session, daemonization, and broad
  workflow automation are intentionally not active.

## CTO Assessment

The current direction is sound for local-first restructuring: Markdown
authority plus deterministic kernel plus MCP control-plane is the right MVP
shape. The long-term risk is not the architecture concept; it is letting
Markdown append logs, direct-file writeback, and bounded keyword search become
the permanent operating model after multiple projects and agents are active.

The next architectural checkpoints should be:

1. Decide truth-store strategy before concurrency pressure forces a reactive
   migration.
2. Define A2-Serve graduation criteria before onboarding a third active
   project.
3. Add project registry and cross-project context policy before context starts
   leaking implicitly between projects.
4. Make retrieval freshness observable before relying on GBrain/vector search
   for correctness.
