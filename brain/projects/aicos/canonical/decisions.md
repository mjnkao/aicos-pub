# Decisions Của AICOS

Trạng thái: decisions tối thiểu cho phase hiện tại.

- Dùng migration an toàn: cấu trúc mới ở active root, dữ liệu cũ trong
  `backup/pre-restructure-20260418/`.
- Dùng GBrain làm substrate; PGLite là hướng local-first đầu tiên.
- Giữ service intelligence trong A2 skills/service knowledge, chưa hardcode sâu
  vào kernel.
- Chưa build UI hoặc public API trước khi CLI/local review flow ổn định.
- Codex hiện là A2-Core-C khi sửa AICOS; chuyển A2-Core-R trước thay đổi lớn.
- Chưa tách `RUL-26088` thành permanent files vì rules còn biến động.

