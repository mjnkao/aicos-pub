# Storage Structure Normalization

Ngày: 2026-04-18
Actor lane: A2-Core
Loại: H2 episodic handoff note

## Context

`STR-26185` chuẩn hóa nơi lưu handoff, open items, open questions, risks,
research, và agent tasks. Điểm thay đổi quan trọng là active project handoff
nên sống cùng project trong `brain/projects/aicos/working/handoff/current.md`,
không ở lâu dài trong historical migration notes.

## Việc Đã Làm

- Tạo H1 current handoff index mới ở
  `brain/projects/aicos/working/handoff/current.md`.
- Tạo H2 episodes lane cho project handoff.
- Bổ sung project working lanes cho open items, potential risks, và tech debt.
- Bổ sung evidence research lane.
- Move handoff files cũ ra `backup/handoff-provenance-20260418/` để agent mới
  không đọc nhầm đường cũ.
- Đánh dấu `brain/shared/handoffs/` là reserved cho handoff thật sự shared hoặc
  system-wide, không dùng mặc định cho project handoff.

## Tradeoff

Không giữ handoff cũ trên đường đọc active. Nội dung current cần thiết đã được
đưa vào H1 mới và self-brain; file cũ được giữ trong backup để audit khi cần.

## Future Work

- Migrate episodic handoffs cũ on-demand nếu một task cần nối lại lịch sử.
- Mở rộng `context start` để ưu tiên H1 mới khi startup cần handoff.
- Xem lại historical migration notes định kỳ để tránh bị hiểu nhầm là current
  truth.
