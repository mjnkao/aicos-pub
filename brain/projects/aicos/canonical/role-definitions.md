# Định Nghĩa Vai Trò

Trạng thái: canonical tối thiểu cho role model hiện tại.

## Role Model Principle

`A1` và `A2` không phải tên nghề nghiệp của agent.

Chúng là **service-boundary classes**:

- `A1`: actors dùng AICOS như một service để làm việc trong company,
  workspace, project, workstream, hoặc task.
- `A2`: actors sửa, vận hành, hoặc cải thiện chính hệ thống AICOS.

Vai trò gần với human như Product Owner, CTO, Tech Lead, Architect, Fullstack
Developer, QA, Designer, Content Writer, Researcher, Manager, Reviewer, hoặc
domain-specific roles khác là **project/company roles**. Các role này có thể
được một human hoặc một agent đảm nhiệm trong một task cụ thể.

AICOS phải luôn tách hai câu hỏi:

- actor này đang dùng AICOS hay đang sửa AICOS?
- actor này đang đóng vai gì trong project/company hiện tại?

## Humans

Humans là first-class actors: manager, reviewer, approver, team lead.
Humans chọn option, review promotion, chốt các thay đổi quan trọng, và là
nguồn phê duyệt khi state cần chuyển từ working sang canonical.

## A1

A1 là actors dùng AICOS như context/control/intelligence service để làm việc
trên project reality: đọc requirements, decisions, working state, tạo
deliverables, ghi blockers/findings/handoffs, và sinh project options khi bị
block.

Một A1 luôn nên có project/company role cụ thể khi task cần: ví dụ Product
Owner, Tech Lead, Architect, Fullstack Developer, QA, Designer, Content Writer,
Researcher, Operations Manager, hoặc role domain-specific khác. Với coding
project, các role thường gần với software team roles. Với non-code project,
role có thể là writer, editor, strategist, analyst, manager, designer, hoặc
reviewer.

A1 không sở hữu việc sửa AICOS kernel, service skills, runtime/config, hay
serving mechanics.

Nếu A1 gặp vấn đề thuộc hệ thống AICOS, A1 ghi friction hoặc blocker rồi chuyển
sang lane A2 phù hợp.

## A2

A2 là actors làm việc trên system reality của AICOS: cấu trúc repo, kernel,
CLI, serving, integrations, service skills, migration,
retrieval/capsule/promotion quality.

A2 cũng có thể có human-like service role khi sửa chính AICOS: ví dụ AICOS CTO,
AICOS Architect, Kernel Engineer, MCP Engineer, Retrieval Engineer, QA/Reviewer,
Documentation Architect, hoặc Product/Service Designer. Các role này mô tả góc
nhìn chuyên môn trong việc cải thiện AICOS, nhưng actor vẫn là A2 vì đối tượng
công việc là chính AICOS.

A2 không làm thay business/project delivery của A1.

## A2-Core

A2-Core thay đổi chính AICOS. Đây là nhánh đang active nhất hiện nay.

- A2-Core-R: reasoning về architecture, policy, tradeoff, migration.
- A2-Core-C: coding/build/config/refactor/CLI/package changes.

Codex hiện tại mặc định là `A2-Core-C` khi sửa repo AICOS, và chuyển ngắn sang
`A2-Core-R` trước các thay đổi lớn.

## A2-Serve

A2-Serve cải thiện cách AICOS phục vụ A1: capsule quality, retrieval quality,
promotion hygiene, branch compare, option quality, feedback synthesis.

A2-Serve là target architecture/future branch, chưa phải runtime lane active
đầy đủ trong phase hiện tại.

## Chat Decision Flow

Chat channel là nơi human và agent trao đổi, nhưng không phải source of truth
duy nhất. Khi human chọn hướng xử lý, agent đang làm việc phải commit quyết
định đó vào AICOS state bằng lane/command phù hợp, ví dụ
`aicos option choose`.

`aicos sync brain` chỉ refresh retrieval substrate từ `brain/`; nó không thay
thế human decision và không promote canonical truth.
