# AICOS Project Working Rules

Trạng thái: canonical tối thiểu cho phase restructuring.
Ngày cập nhật: 2026-04-21.

## Boundary Rules

- `brain/` giữ durable knowledge, canonical truth, working reality, evidence,
  branch reality, status-items, current handoffs, và service knowledge.
- `agent-repo/` giữ operational rules/state của humans, A1, A2, startup cards,
  rule cards, task packets, và actor tasks; không phải project truth.
- `packages/aicos-kernel/` giữ deterministic contracts, validators, read/write
  serving operations, adapters, compaction primitives, và thin CLI behavior.
- `integrations/` giữ runtime bindings như local MCP stdio bridge; không phải
  project truth.
- `backend/` là serving substrate/index/engine state; không phải authority.
- `serving/` giữ generated capsules, option packets, promotion review packets,
  branch compare, truth helpers, feedback.
- External project repos giữ code/runtime authority của project đó. AICOS giữ
  context/control-plane authority.

## State Rules

- `canonical/` là truth đã đủ ổn định để làm startup context ngắn.
- `working/` là current best understanding, implementation state, risks, next
  steps.
- `evidence/` là raw/candidate/review-heavy material, không đọc mặc định.
- `branches/` là experiment reality, không override working/canonical nếu chưa
  review.
- `working/status-items/` là lane cho open items, open questions, tech debt,
  và decision follow-ups có stable item id.
- `working/handoff/current.md` là compact current continuity index, không phải
  append-only event log.
- Không ghi mọi chat turn vào self-brain. Chỉ ghi khi có state transition có ý
  nghĩa: decision, blocker đã rõ, option packet sẵn sàng, selected branch,
  direction đổi, risk đáng theo dõi, milestone hoàn thành, hoặc backlog đủ rõ.
- `working/current-state.md` không phải inbox cho mọi idea.

## Writeback Levels

- W1 No Write: clarify nhỏ, wording nhỏ, ý tưởng quá sơ khai.
- W2 Session/Runtime Write: scratch hoặc state tạm trong `agent-repo/`.
- W3 Working State Write: state transition đủ rõ trong `brain/.../working` hoặc
  branch lane.
- W4 Canonical Promotion: chỉ sau review/chấp thuận, không đi thẳng từ chat
  hằng ngày lên canonical.

## Checkpoint Discipline

- Shared checkpoint/writeback policy nằm ở
  `brain/shared/policies/checkpoint-writeback-policy.md`.
- Shared coordination policy nằm ở
  `brain/shared/policies/agent-coordination-policy.md`.
- Không để quá một milestone có ý nghĩa nằm riêng trong session mà chưa
  checkpoint.
- Checkpoint khi xong milestone, đổi scope/work context/actor, bị
  blocked/waiting, chuẩn bị pause dài, hoặc khi actor khác có thể phải tiếp
  tục.
- Checkpoint không đồng nghĩa promote canonical; nó chỉ làm continuity đủ rẻ
  cho actor tiếp theo.

## Actor Rules

- A1 làm project/business work; nếu gặp system issue thì ghi friction và chuyển
  sang A2.
- A2 sửa AICOS; không làm thay business delivery của A1.
- Codex hiện tại là A2-Core-C khi build/refactor/config AICOS, và dùng
  A2-Core-R ngắn trước quyết định kiến trúc lớn.
- A2-Serve là target future để cải thiện capsule/retrieval/promotion/branch
  quality cho A1; chưa là runtime lane active đầy đủ.
- Minimum viable A1 branch đã có startup card, rule cards, task packet index,
  và task-state convention dùng cho các real projects.
- A1 core rules phải generic-first. Project, workstream, branch, và task rules
  không được viết như global A1 rules.
- Future company/workspace scope layers có thể được thêm sau, nhưng không phải
  startup-default trong MVP.
- A1 core phải artifact-neutral: coding là một artifact type được hỗ trợ, không
  phải default universal cho mọi A1 task.
- A1 nên dùng MCP-first cho AICOS-facing context/control-plane read/write khi
  MCP khả dụng. A1 vẫn dùng direct local/repo/tool access cho actual project
  artifacts.
- A2-Core có thể dùng direct repo access khi bảo trì AICOS, nhưng phải giữ
  boundary và lane semantics tương thích với MCP.

## Chat Decision, Option, And Sync Rules

- Chat là kênh trao đổi và ra quyết định; AICOS mới giữ structured state.
- Khi human chọn option rõ ràng, agent commit bằng `aicos option choose
  <project-id> <blocker-id> <option-id>`.
- `aicos option choose` ghi selected option, selected branch, approval/choice
  lane, working direction/state, blocker/open-question status khi phù hợp.
- `aicos option choose` không promote canonical, không xóa option khác, không
  rewrite architecture truth, và không dùng backend làm authority.
- `aicos sync brain` chỉ sync `brain/` sang GBrain/PGLite để refresh retrieval.
  Nó không mutate truth, không promote state, không index `agent-repo/`,
  `backend/`, `backup/`, `imports/`, `scripts/` hoặc `integrations/` mặc định.
- `aicos sync brain` chưa được coi là retrieval correctness path cho đến khi
  embedding/vector freshness có status rõ.

## MCP Context/Control Plane Rules

- Local MCP là active MVP context/control-plane surface, không phải raw file RPC.
- Current write contract là `mcp-v0.6-write-contract-ack`.
- Semantic writes phải có `mcp_contract_ack`, `actor_role`, `agent_family`,
  `agent_instance_id`, `work_type`, và `work_lane`.
- `actor_role` là role lane của AICOS, ví dụ `A1`, `A2-Core-C`,
  `A2-Core-R`.
- `agent_family` là client/product family, ví dụ `codex`, `claude-code`,
  `gemini-antigravity`, hoặc `openclaw`; không dùng `A1`/`A2` làm
  `agent_family`.
- `work_lane` là coordination key chung cho code, content, design, research,
  ops, review, planning, và mixed work.
- Code work phải có `worktree_path`; nên có `work_branch`.
- Non-code work nên dùng `artifact_scope` và `artifact_refs` thay vì giả lập
  code/worktree metadata.
- `aicos_write_handoff_update` chỉ dành cho compact current continuity. Không
  dùng nó để tạo/đóng/list open items, open questions, tech debt, decision
  follow-ups, hoặc backlog.
- Dùng `aicos_update_status_item` cho lifecycle của open items/open
  questions/tech debt/decision follow-ups.
- Dùng `aicos_register_artifact_ref` khi durable artifact nằm ngoài AICOS hoặc
  không nên copy body vào AICOS.
- Status/query reads nên tránh stale/closed status-items theo mặc định; audit
  callers phải opt in bằng filter/flag rõ.
- Startup bundle có thể trả `continuity_signal`; empty `active_task_state`
  không có nghĩa project idle.

## Idea Capture Rules

- Open question quan trọng đi vào `brain/projects/aicos/working/open-questions.md`.
- Open item chưa đủ thành actor task đi vào
  `brain/projects/aicos/working/open-items.md`.
- Open item/open question/tech debt/decision follow-up có stable lifecycle nên
  đi vào `brain/projects/<project-id>/working/status-items/`.
- TODO/backlog rõ nhưng chưa làm ngay đi vào
  `agent-repo/classes/a2-service-agents/tasks/backlog/`.
- Candidate branch idea chưa được chọn đi vào evidence/candidate-decisions hoặc
  open questions; chưa tạo branch reality chính thức.
- Project-level tech debt đi vào `brain/projects/aicos/working/tech-debt.md`;
  tech debt có owner/scope rõ mới thành actor backlog.
- Risk suspicion đi vào `potential-risks.md`; risk đủ evidence/impact mới đi
  vào `active-risks.md`.
- Research material đi vào `brain/projects/aicos/evidence/research/`; research
  task có owner đi vào `agent-repo/.../tasks/...`.
- Decision đã chốt đi vào working/approval/branch lane tương ứng.

## Handoff Rules

- Handoff là continuity layer, không phải nơi lưu toàn bộ truth lâu dài.
- H1 current handoff index của project nằm ở
  `brain/projects/<project-id>/working/handoff/current.md`.
- H2 episodic handoff notes của project nằm ở
  `brain/projects/<project-id>/working/handoff/episodes/`, ghi theo từng
  pass/test/episode và đọc on-demand để xem provenance hoặc chi tiết.
- H3 self-brain digest: thông tin stable/current từ handoff phải được tiêu hóa
  vào `brain/projects/aicos/working/`.
- Historical migration notes, implementation notes, and review notes are
  provenance only; they are not part of the default public docs surface and are
  not the long-term home of active project handoff.
- Handoff cũ/provenance không nằm trên đường đọc startup; nếu cần audit thì xem
  `backup/handoff-provenance-20260418/`.
- `brain/shared/handoffs/` chỉ dùng cho handoff thật sự cross-project hoặc
  system-wide.
- Handoff stale/superseded chỉ là reference, không override H1 current index
  hoặc self-brain digest.
- Không đọc tất cả handoff cũ ở startup. Chỉ đọc current handoff index khi task
  là continuation, migration/state alignment, repo-wide architecture, hoặc cần
  biết newest/current vs stale.
- Khi handoff có nhiều MCP continuity blocks hoặc vượt ngưỡng đọc hợp lý, dùng
  `./aicos compact handoff projects/<project-id>` để gom thành digest ngắn.
- Handoff compaction không được xóa project truth; chi tiết có giá trị phải
  nằm trong status-items, checkpoints, task-state, evidence, hoặc episode refs.

## Task Continuity Rules

- Không build `transfer/`, takeover daemon, hoặc registry lớn trong phase hiện
  tại.
- Task continuity nên nằm trong task packet và actor task state hiện có.
- Task packet/task state nên dùng current identity model: `actor_role`,
  `agent_family`, `agent_instance_id`, `work_type`, `work_lane`,
  `coordination_status`, `artifact_scope`, `work_branch`, `worktree_path`,
  `task_status`, `what_is_done`, `what_is_blocked`, và `next_step`.
- Legacy fields như `actor_family`, `logical_role`, và `work_context` chỉ dùng
  để đọc provenance cũ hoặc compatibility; không dùng làm schema chính cho
  write mới.
- Cập nhật metadata này khi có checkpoint có ý nghĩa: blocked/waiting, đổi
  actor, đổi scope/branch, milestone xong, hoặc pause dài.
- Không cập nhật metadata cho từng micro-step, từng tool call, hoặc từng chat
  clarification.
- `handoff_refs` phải nhỏ và chọn lọc: ưu tiên current project handoff index,
  chỉ thêm episodic note khi thật sự cần.

## Reading Rules

- A2 đọc role rules và self-brain trước raw repo.
- A2-Core mới nên bắt đầu từ
  `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
  để biết tầng đọc tối thiểu, tầng đọc sâu, và rule đọc theo trigger.
- A1 mới nên bắt đầu từ
  `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`, xác định
  actor class, company/workspace/project scope, work context, và task packet
  trước khi đọc sâu.
- Mỗi project có thể cung cấp context ladder riêng tại
  `brain/projects/<project-id>/working/context-ladder.md` để giải thích hot
  context, conditional handoff, task packets, evidence, và deep source paths.
- Historical long-form design docs are source/evidence provenance, not default
  startup context. Use `docs/architecture/README.md` for current architecture.
- Backup legacy ở `backup/pre-restructure-20260418/` chỉ đọc khi cần migration,
  provenance, hoặc comparison.
- AICOS dùng hướng packet-first: role card, current state, current direction,
  packet index/task suggestion, rồi mới load task packet và rule cards theo
  trigger.
- A1 dùng MCP startup bundle/packet index khi có thể. Direct file fallback phải
  được ghi rõ nếu MCP unavailable.
- Nếu chưa có task cụ thể, agent không load tất cả task packets hoặc rules.
  Agent được phép dừng ở orientation + packet index và hỏi human nên tiếp tục
  task nào.

## External Co-Worker Context Boundary

- AICOS cung cấp context, rules, state summaries, task packets, và lookup paths
  cho Codex, Claude Code, OpenClaw, ChatGPT, Claude chat, và co-workers khác.
- AICOS không sở hữu, điều khiển, hay giả định cơ chế memory/context nội bộ của
  các co-workers bên ngoài.
- Contract đúng là: AICOS nói thông tin nào cần biết, thông tin nào authoritative,
  tra cứu thêm ở đâu, và ghi lại state transition có ý nghĩa; co-worker tự quản
  cách giữ context bên trong runtime/tool của họ.

## Implementation Rules

- Không hardcode capsule/option/promotion/retrieval intelligence quá sớm.
- Kernel chỉ nên code schema, validators, packet format, folder contract, write
  lanes, adapters, CLI wrappers, bounded read/write serving operations, và
  mechanical compaction helpers.
- Local MCP stdio bridge là active MVP surface. Remote/hosted MCP, auth/session,
  daemon, UI, public API, và full A2-Serve runtime lane chưa active.
- Trước khi scale nhiều project/agent, cần ADR cho truth-store strategy, policy
  cho cross-project context propagation, và criteria để graduate A2-Serve.
