# Open Items Của AICOS

Trạng thái: project-level unresolved items, chưa nhất thiết là actor tasks.

## Items

1. Khi nào cần audit lại handoff cũ trong `backup/handoff-provenance-20260418/`
   để trích thêm nội dung vào self-brain mới?
2. Xác định thời điểm `./aicos context start` nên mở rộng ngoài
   `A2-Core-C` / `projects/aicos`.
3. Xác định khi nào task packet metadata cần registry hoặc summary giàu hơn.
4. Xác định cách tách shared operating policies cho A1 mà không kéo theo
   A2-Core taxonomy.
5. Xác định tiêu chí khi nào provider-backed hoặc serving-backed registries là
   cần thiết cho task packets, handoffs, queues, candidate decisions, hoặc sync
   ledger, mà không làm lệch semantic core hoặc chuyển markdown truth thành
   implementation detail quá sớm.
6. Chạy local MCP read/write usage test thật từ external checkout khác máy hoặc
   khác project checkout để kiểm chứng LAN/team path.
7. Sau usage test, quyết định có cần harden validation/session/audit trước khi
   mở rộng MCP surface hay không.
8. Hoàn thiện retrieval freshness/status cho HTTP daemon + PostgreSQL hybrid
   search: báo rõ text/FTS/embedding index fresh hay stale, embedding coverage,
   last indexed time, và fallback mode hiện tại.
9. Review reuse-first search substrate: so sánh phần AICOS đang tự code với
   GBrain/open-source AI-native components để quyết định phần nào nên reuse,
   wrap, hoặc bỏ qua. Trọng tâm: embedding batching, chunking, hybrid/RRF,
   query expansion, health/freshness, và pgvector schema.
10. Đánh giá có nên generalize `aicos_update_status_item` thành
    `aicos_upsert_working_item` hoặc alias tương đương để bao phủ
    `active_risk`, `assumption`, `dependency`, `candidate_decision`. Tránh tạo
    thêm nhiều write tool song song nếu một working-item model đủ rõ.
11. Xem xét có cần read primitive riêng như `aicos_get_current_direction` cho
    agent cần định hướng nhanh nhưng không cần full startup bundle. Chỉ thêm
    nếu startup bundle/query hiện tại khiến agent load thừa context.
12. Dọn và thống nhất connector/auth interoperability matrix cho các client
    chính (`Claude Desktop`, `Claude Code`, `Codex Desktop`,
    `Antigravity/Gemini IDE`) để tránh tactical drift ở lớp config, proxy, và
    auth path.
13. Hoàn thiện LAN security baseline vượt mức shared bearer token tối thiểu:
    policy rõ hơn cho non-local clients, allowlist/ingress controls phù hợp,
    và audit/auth model đủ chắc cho trusted team LAN.
14. Chạy search evaluation thật cho AICOS: so sánh markdown-direct,
    PostgreSQL FTS, và hybrid/vector retrieval trên query thật của A1/A2 để
    xác định chất lượng tăng bao nhiêu và phần nào đáng giữ/reuse.
15. Thiết kế hosted/team deployment path tối thiểu vượt single-machine SPOF:
    nêu rõ deployment shape, remote access boundary, và trách nhiệm của daemon,
    proxy, index/search, và secrets handling.
16. Nâng project intake/import từ markdown MVP flow lên tooling path rõ hơn
    khi đủ chín, nhưng vẫn giữ lightweight-first và không overbuild trước khi
    usage pattern ổn định.
17. Chuyển GBrain search reuse review từ architecture note sang execution plan
    cụ thể: dựng retrieval eval corpus cho AICOS, benchmark FTS vs hybrid,
    xác định direct-get cases có thật, và thử chunking strategy theo từng
    context kind trước khi mở relation-aware serving.
18. Làm substrate inventory cho AICOS theo hướng "keep / migrate / retire":
    tách phần semantics/control-plane phải giữ ở AICOS khỏi phần retrieval /
    health / maintenance / query-runtime đang là candidate để giảm custom code
    và reuse GBrain-derived substrate nhiều hơn.
19. Chuyển product framing mới thành artifact dùng được cho kiến trúc và GTM:
    xác định rõ direct users, indirect beneficiaries, core painkiller, short-
    term product boundary, và future path cho company/workspace knowledge dùng
    cho AI agents mà không làm AICOS phình thành universal knowledge system quá
    sớm.
20. Chuẩn hóa lại actor-role model cho AICOS theo nhiều chiều: tách
    AICOS-internal actor classes (`A1`/`A2`) khỏi project-facing functional
    roles (CTO/coder/marketer/...) và service roles (internal/external actor,
    hoặc tương đương), để AICOS không áp taxonomy nội bộ của chính nó lên mọi
    project khác.

Resolved in current MVP:

- Hardcoded local path reduction: install docs use `<AICOS_REPO_PATH>` and CLI
  wrapper resolves repo root from its own location. `aicos install cli` provides
  a portable symlink path.
- LAN/team access minimum: HTTP daemon can bind to LAN with token auth; deeper
  session/audit/hosted deployment remains future work.
- Structured feedback capture/read: `aicos_record_feedback`,
  `aicos_get_feedback_digest`, and `aicos_get_project_health` exist.
- Policy/rule promotion candidate minimum: use
  `working/policy-candidates/` plus status-item/artifact-ref until a dedicated
  lifecycle tool is justified.
- Workstream proposal minimum: use `working/workstream-proposals/`; only
  accepted/materialized workstreams should appear in `aicos_get_workstream_index`.
- Project onboarding/intake minimum: `brain/shared/templates/project-onboarding/project-intake-flow.md`
  now separates new project intake from existing project import. Dedicated MCP
  intake tools remain future work.

sample project/Crypto first-slice/import items đã được giải quyết trong
`projects/sample-project`; các import-kit files hiện là
provenance/reference, không phải active AICOS open items.

## Routing Rule

Nếu item trở thành việc cụ thể có owner và trạng thái thực thi, chuyển sang
`agent-repo/.../tasks/...`. Nếu item là câu hỏi cần quyết định, chuyển hoặc
link sang `open-questions.md`.
