# Requirements Của AICOS

Trạng thái: requirements tối thiểu cho MVP hiện tại.

- Active root phải phản ánh kiến trúc mới, không lẫn legacy context.
- Legacy data phải nằm trong `backup/pre-restructure-20260418/` và chỉ đọc khi
  có nhu cầu rõ.
- `brain/`, `agent-repo/`, `backend/`, `serving/` phải giữ boundary rõ.
- AICOS phải có self-brain ngắn gọn cho chính nó.
- A2 startup phải đọc role rules, A2 taxonomy, và self-brain trước raw repo.
- CLI local `./aicos` phải tiếp tục hỗ trợ capsule, option, branch, promote,
  validate, sync preflight.
- MVP phải chứng minh được flow `blocked -> options -> manager choice`.

