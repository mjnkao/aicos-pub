# Trạng Thái Migration

Trạng thái: active root đã tách khỏi legacy data.

## Đã Move Vào Backup

Legacy data đã được move vào:

```text
backup/pre-restructure-20260418/
```

Trạng thái main cũ cũng đã được bảo toàn trên remote branch:

```text
backup/pre-restructure-main
```

Trong đó:

- `root/`: old root context, runtime/cache, old lanes, imports, reports,
  gateway, bridges, artifacts, data, tmp.
- `docs/`: old docs that were outside the active public documentation surface.
- `scripts/`: old scripts ngoài `scripts/aicos` và `scripts/gbrain_local.sh`.
- `previous-backup/`: backup cũ trước cleanup.

## Active Root Hiện Tại

```text
AGENTS.md
README.md
agent-repo/
aicos
backend/
backup/
brain/
docs/
integrations/
packages/
scripts/
serving/
tools/gbrain/
```

## Đã Migrate Tối Thiểu

- project identity và rules tối thiểu vào `brain/projects/aicos/canonical/`;
- current state/direction/risks/questions/status vào `brain/projects/aicos/working/`;
- review/source indexes vào `brain/projects/aicos/evidence/`;
- CLI/review flow outputs vào `serving/`.

## Chưa Migrate

- Chưa migrate hàng loạt old `canonical/`, `gateway/`, `bridges/`, `reports/`,
  `imports/`.
- Chưa chọn old source nào làm canonical mới ngoài các summary tối thiểu.

## Rule Khi Dùng Backup

Không đọc backup mặc định. Khi cần, đọc đúng path/branch liên quan, ghi source
path, và chỉ copy/migrate phần đã review vào cấu trúc mới.
