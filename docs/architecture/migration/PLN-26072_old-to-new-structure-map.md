# PLN-26072 Old To New Structure Map

Status: initial migration map

Update: legacy root data was moved to
`backup/pre-restructure-20260418/` on 2026-04-18. Paths below describe the old
lane identity and where to look for legacy material now.

## Mapping

| Old lane | Legacy backup path | New target interpretation | Current action |
| --- | --- | --- |
| `canonical/` | `backup/pre-restructure-20260418/root/canonical/` | Source reference for `brain/.../canonical` and `brain/.../working` | Migrate selectively after review. |
| `brains/` | `backup/pre-restructure-20260418/root/brains/` | Existing GBrain-facing material | Use as adapter reference if needed. |
| `gateway/` | `backup/pre-restructure-20260418/root/gateway/` | Deterministic contracts and serving helpers | Migrate useful parts into `packages/aicos-kernel/` or `serving/` later. |
| `bridges/` | `backup/pre-restructure-20260418/root/bridges/` | Runtime integrations and MCP setup | Map into `integrations/` and class-specific `agent-repo/.../mcp` later. |
| `reports/` | `backup/pre-restructure-20260418/root/reports/` | Evidence, queues, and feedback | Route reviewed material into `brain/.../evidence`, `agent-repo/.../queues`, or `serving/feedback`. |
| old `backup/` contents | `backup/pre-restructure-20260418/previous-backup/` | Reference/archive lane | Preserve until operator approves deletion. |
| old `scripts/` | `backup/pre-restructure-20260418/scripts/` | Local utilities and CLI wrappers | Reintroduce only reviewed scripts; active root keeps `scripts/aicos` and `scripts/gbrain_local.sh`. |

## Rule

No legacy material should be read by default. Use the backup only for explicit
migration, provenance, or comparison tasks.
