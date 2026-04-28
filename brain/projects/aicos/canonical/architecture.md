# Kiến Trúc AICOS

Trạng thái: canonical tối thiểu, còn đang evolve.

MVP hiện tách các phần chính:

- AICOS Kernel: contracts, schemas, validators, packet formats, write lanes,
  GBrain adapter, CLI mỏng.
- A2 Service Skills: policy và service intelligence còn thay đổi.
- GBrain: substrate cho retrieval, indexing, sync, MCP/CLI.
- GStack: optional cho coding workflow, không phải control plane của MVP.

Boundary bắt buộc:

- `brain/` giữ durable knowledge và system/work reality.
- `agent-repo/` giữ operational state/rules của actors.
- `backend/` là serving substrate, không phải truth.
- `serving/` giữ generated packets và review surfaces.

