# Rủi Ro Đang Active Của AICOS

Trạng thái: risks đang active.

| Risk | Impact | Mitigation hiện tại |
| --- | --- | --- |
| Lẫn A1/A2 role | Codex có thể làm project work thay vì sửa AICOS, hoặc ngược lại | Dùng `RUL-26088`, A2 taxonomy, và `AGENTS.md` để phân lane |
| Lẫn A2-Core/A2-Serve | Build core system có thể bị trộn với service support cho A1 | Ghi rõ Codex hiện là A2-Core-C; A2-Serve chưa active đầy đủ |
| Self-brain quá dài | Startup context lại nặng như docs cũ | Viết summary ngắn, source docs để trong evidence/source references |
| Hardcode service logic quá sớm | Capsule/option/promotion policy khó evolve | Kernel chỉ giữ substrate; policy ở A2 skills/service knowledge |
| Legacy backup leak vào startup | Old context có thể override kiến trúc mới | Backup chỉ đọc khi cần migration/provenance/comparison |
| Retrieval runtime có thể thiếu PG/embedding dependency | Query vẫn chạy fallback nhưng semantic/vector coverage có thể bằng 0 trên máy chưa cấu hình đủ | `./aicos brain status` reports GBrain sync, PG index, embedding coverage, and stale/missing embeddings; daemon starts FTS first and refreshes embeddings in background |
| Backend bị hiểu là truth | Authority drift | Nhắc rõ `backend/` là substrate, không phải source of truth |
| Policy pack bị copy quá dài vào startup | Startup context lại phình và khó dùng | Normalize nội dung ổn định vào canonical/working/A2 rules; giữ nguồn dài làm reference |
| Candidate branch idea bị activate quá sớm | Branch reality bị loạn vì ý tưởng chưa được chọn | Chỉ tạo `branches/` sau manager/agent flow quyết định thử branch |
