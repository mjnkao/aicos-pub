# Tech Debt Của AICOS

Trạng thái: project-level tech debt notes. Không phải actor backlog mặc định.

| Debt | Impact | Possible routing |
| --- | --- | --- |
| Bare `aicos ...` chưa ổn định nếu wrapper chưa có trong PATH | Docs/rule cards phải dùng `./aicos ...`, fresh thread dễ bị command not found | Tạo actor task khi quyết định sửa PATH/install wrapper |
| `context start` mới ở MVP scope | Chưa đủ cho A1/A2-Serve hoặc nhiều project | Mở rộng sau khi startup model ổn định |
| Task packet summaries còn mỏng | Agent chọn packet chậm hơn trong fresh-thread startup | Bổ sung metadata/index khi có thêm packet thật |
| Handoff cũ nằm trong backup riêng | Provenance còn hữu ích nhưng không được nằm trên đường đọc active | Audit/trích xuất on-demand khi human yêu cầu hoặc khi thiếu lịch sử |
| Schema/validation cho packet chưa full JSON Schema | Linh hoạt tốt trong giai đoạn đầu nhưng dễ drift khi nhiều actor dùng | Chờ packet shape đủ ổn định rồi formalize |

## Routing Rule

Tech debt chỉ thành actor task khi có owner, scope, và success condition cụ thể.
