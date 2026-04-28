# Handoff Summary Của AICOS

Trạng thái: digest/reference phụ. Không phải startup authority và không thay
thế H1 current handoff index.

Authority hiện tại:

```text
brain/projects/aicos/working/handoff/current.md
```

## Mô Hình Handoff

- H1 current handoff index:
  `brain/projects/aicos/working/handoff/current.md`
- H2 episodic handoff notes: bounded notes trong
  `brain/projects/aicos/working/handoff/episodes/`, đọc on-demand.
- H3 self-brain digest: thông tin stable/current được tiêu hóa vào
  `brain/projects/aicos/working/`.

Convention hiện tại: project continuity sống cùng project. `docs/migration/`
giữ implementation/migration notes và provenance; không còn là nhà mặc định cho
active project handoff.

## Startup Path Ngắn

Startup mặc định đọc theo startup card, không cần đọc file summary này.

Đọc trước:

1. `agent-repo/classes/a2-service-agents/startup-cards/a2-core.md`
2. `brain/projects/aicos/canonical/role-definitions.md`
3. `brain/projects/aicos/canonical/project-working-rules.md`
4. `brain/projects/aicos/working/current-state.md`
5. `brain/projects/aicos/working/current-direction.md`

Chỉ đọc current handoff index khi task là continuation, migration/state
alignment, repo-wide architecture, hoặc cần biết newest/current vs stale.

Không đọc toàn bộ episodic handoffs ở startup.

Nếu chưa có task cụ thể, chỉ xem orientation + task packet index rồi hỏi human
nên tiếp tục task nào. Không load toàn bộ task packets mặc định.

Nếu cần review flow MVP, xem:

- `serving/branching/option-packets/aicos__blocker-001.md`
- `agent-repo/classes/humans/approvals/manager-choice-blocker-001.md`
- `brain/projects/aicos/branches/blocker-001-option-a/`

Không đọc backup mặc định.
