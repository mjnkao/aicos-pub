# Hướng Triển Khai Hiện Tại Của AICOS

Trạng thái: hướng triển khai hiện tại.

## Ưu Tiên Hiện Nay

1. Làm self-brain của AICOS ngắn gọn, dễ đọc, dùng làm startup context.
2. Giữ Codex ở lane A2-Core khi sửa chính AICOS.
3. Ổn định active root mới trước khi migrate sâu từ backup.
4. Giữ service intelligence trong A2 skills/service knowledge, chưa hardcode.
5. Dùng `./aicos` CLI và markdown review flow trước UI/API.
6. Commit decision từ chat bằng state transition rõ ràng, không ghi mọi message.
7. Với mọi MCP semantic write của A1/A2, bắt buộc ghi actor identity và
   `work_type`/`work_lane` để nhiều agent có thể làm song song mà không dẫm
   lane. Code work phải ghi `worktree_path`; `work_branch` là metadata riêng
   cho code; content/design/research dùng `artifact_scope` và `artifact_refs`.
8. MCP contract/schema hiện là `0.5`. Mọi semantic write phải gửi
   `mcp_contract_ack: "mcp-v0.5-write-contract-ack"`. Agent đã cache schema cũ
   cần refresh `tools/list` hoặc restart/re-enable AICOS MCP trước khi write.
   Dùng `aicos_update_status_item` để đổi trạng thái open item/open question/
   tech debt/decision follow-up, `aicos_query_project_context` để query bounded
   hot context, và `aicos_register_artifact_ref` để đăng ký artifact refs.
9. Với team/LAN, dùng HTTP daemon tối thiểu có token. Không mở non-loopback
   daemon không auth trừ khi human chấp nhận mạng cô lập/trusted.
10. Policy/rule candidate và workstream proposal phải đi qua lane đề xuất hoặc
   status item, không tự promote thành active policy/workstream.
11. Ưu tiên reuse-first cho search/context intelligence: học và tái sử dụng
   GBrain hoặc hệ thống AI-native/open-source tốt khi fit kiến trúc. Chỉ tự
   code phần AICOS-specific boundary, MCP contract, authority mapping, và
   fallback cần thiết.
12. Kiến trúc dài hạn nên đi theo hướng Option C:
    AICOS là semantic/control-plane core với runtime services ở giữa và
    provider/profile/pack layers ở dưới, để có thể đổi substrate theo quy mô
    công ty và tích hợp tốt với dashboard/task tools như Plane hoặc ClickUp mà
    không biến AICOS thành PM tool.
13. Trước khi modularize sâu hơn, phải có một Phase 0.5 để ổn định operating
    surface đang chạy: ưu tiên buộc các A1 đi qua HTTP daemon cho mọi
    AICOS-facing read/write, không cho A1 fallback sang ghi markdown trực tiếp.
    Chỉ `A2-Core-R` và `A2-Core-C` mới được fallback sang direct file writes
    khi MCP HTTP thật sự bị block; mặc định ngay cả A2 cũng phải thử HTTP MCP
    trước để lộ friction thật.
14. Cần chuẩn hóa actor-role model theo nhiều chiều: `A1`/`A2` là taxonomy
    nội bộ của chính dự án AICOS; với các project khác, AICOS nên coi agent
    của họ như external work actors dùng AICOS làm control-plane, còn
    functional roles (CTO/coder/marketer/...) và service roles
    (internal/external actor, tương đương) phải là lớp mô hình tách riêng.

## Phase 0 Decision Anchors

Trong pass hiện tại, mọi quyết định kiến trúc lớn nên được neo vào đúng 4
artifact này trước:

1. Product framing / build-vs-buy:
   `brain/projects/aicos/evidence/research/aicos-problem-framing-and-build-vs-buy-20260428.md`
2. Execution decision table:
   `brain/projects/aicos/evidence/research/aicos-execution-decision-table-20260428.md`
3. Option C north-star:
   `brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`
4. Option C transition checklist:
   `brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`

Nếu một đề xuất không giải thích rõ nó đang:
- bảo vệ semantic/control-plane của AICOS,
- hay giảm phần substrate custom,

thì chưa nên được ưu tiên.

## Đang Làm Trước

- canonical identity/rules tối thiểu cho AICOS;
- working state thật của repo;
- migration/evidence indexes;
- startup order mới: role rules -> A2 taxonomy -> self-brain -> raw repo.
- policy pack mới được normalize vào canonical/working/A2 lanes thay vì copy
  nguyên văn vào startup-critical files.

## Cố Tình Chưa Làm

- chưa optimize sâu A1 business/project logic;
- chưa build UI;
- chưa build public API;
- chưa activate full A2-Serve runtime;
- chưa ép GStack thành core;
- chưa import toàn bộ legacy backup vào brain;
- chưa triển khai full project intake/import MCP flow;
- chưa làm policy-candidate/workstream proposal lifecycle tools ngoài mức lane
  tối thiểu.

## Nguyên Tắc Phase Này

Viết ít nhưng đúng. Self-brain phải giúp agent hiểu hiện trạng nhanh hơn, không
trở thành một lớp docs dài khác.

State writeback chỉ xảy ra ở commit point có ý nghĩa: decision, blocker, option
packet, selected branch, risk, milestone, open question, hoặc backlog rõ.

MCP continuity writeback phải đủ định danh để agent mới biết ai đang làm gì:
role lane, agent family, instance id, generic work lane, coordination status,
và artifact/branch/worktree scope khi có. Đây áp dụng cho A1 lẫn A2; không
phải rule riêng cho coding worker.

Status item writeback dùng cùng identity model. Khi đổi trạng thái item, agent
phải ghi `reason` ngắn và link evidence/detail bằng `source_ref` hoặc
`artifact_refs` nếu giải thích dài hơn.

Query/read expansion hiện ưu tiên HTTP daemon + PostgreSQL hybrid search khi
daemon/PG/pgvector/embedding key sẵn sàng. Nếu thiếu dependency, fallback theo
thứ tự PostgreSQL FTS rồi markdown-direct bounded query. Kết quả query vẫn là
serving/index output, không phải truth.

GBrain có thể là substrate học hỏi hoặc reuse từng phần cho embedding,
chunking, hybrid/RRF, query expansion, health, và freshness model. Không ép
GBrain thành authority hoặc coupling bắt buộc nếu làm rối AICOS; reuse phải
giữ `brain/` là truth và MCP là control-plane boundary.

North-star architecture for this direction now lives at:
`brain/projects/aicos/evidence/research/aicos-option-c-architecture-north-star-20260428.md`.

Execution checklist for moving toward that north-star now lives at:
`brain/projects/aicos/evidence/research/aicos-option-c-transition-checklist-20260428.md`.

Retrieval freshness nghĩa là agent phải biết index/search đang phản ánh phiên
bản nào của `brain/`. AICOS now has `./aicos brain status` plus sync/index
timestamps for GBrain/PGLite and PostgreSQL search; `./aicos sync brain`
defaults to full GBrain import, while `--text-only` is the explicit opt-out.
Daemon startup keeps FTS available first and refreshes embeddings in background
when PG/pgvector/OpenAI config is available.

Với code work, `worktree_path` được coi là checkout occupancy signal. Không để
agent instance mới sửa cùng worktree/lane đang active của instance khác nếu chưa
có continuation, handoff, review, takeover, hoặc pair-work rõ ràng.

Mặc định tạo/dùng worktree riêng cho parallel implementation, khác `work_lane`,
khác branch, dirty state chưa rõ, hoặc nguy cơ sửa cùng file. Reuse worktree chỉ
khi đó là continuation, handoff, review, takeover, hoặc pair-work rõ.

`aicos sync brain` được dùng sau refresh point quan trọng để GBrain/PGLite thấy
state mới từ `brain/`; không dùng nó để mutate truth.

## Selected Direction: blocker-001

Active branch: `blocker-001-option-a`
Chosen option: `option-a`
Reason: Ưu tiên hướng tối thiểu, reversible, chứng minh flow chat decision -> AICOS state trước khi migrate sâu.

Next execution should follow the selected branch and keep broader alternatives as reviewable branches, not delete them.
