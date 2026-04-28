# Potential Risks Của AICOS

Trạng thái: risk suspicions hoặc concerns chưa đủ evidence để active track.

| Potential risk | Vì sao cần chú ý | Routing |
| --- | --- | --- |
| Agent đọc nhầm backup handoff cũ như current truth | Backup vẫn giữ lịch sử để audit, nhưng không phải đường đọc active | H1 mới và startup rules phải trỏ thẳng về `brain/projects/aicos/working/handoff/current.md` |
| Quá nhiều lane nhỏ làm agent bối rối | Open question, open item, tech debt, backlog có thể bị dùng lẫn | Giữ rule ngắn: project understanding ở `brain`, actor execution ở `agent-repo` |
| DB registry được thêm quá sớm | Có thể làm DB bị hiểu nhầm là authority | Chỉ dùng DB cho index/lookup/runtime support khi markdown truth đã rõ |
| Shared lane bị dùng như chỗ đổ mọi thứ | Project-specific handoff hoặc risk có thể bị đưa sai vào `brain/shared` | Shared chỉ dùng khi thật sự cross-project hoặc system-wide |

## Promotion Rule

Chỉ chuyển risk sang `active-risks.md` khi có impact/evidence đủ rõ và cần
theo dõi thường xuyên.
