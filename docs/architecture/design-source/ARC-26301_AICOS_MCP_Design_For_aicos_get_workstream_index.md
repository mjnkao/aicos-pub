# ARC-26301 — AICOS MCP Design For `aicos_get_workstream_index`

**Status:** architecture-brief-v1  
**Project:** AICOS  
**Date:** 2026-04-19  
**Primary scope:** MCP read surface design  
**Purpose:** thiết kế trước tool `aicos_get_workstream_index` theo hướng:
- project-neutral
- scalable
- modular
- useful for many project types
- compatible with AICOS architecture
- không biến AICOS thành bên tự tạo workstream cho project

---

## 1. Executive Summary

`aicos_get_workstream_index` là một **routing/context-facing read tool**.

Nó không dùng để:
- tạo workstream mới
- quyết định thay project có tách lane hay không
- thay thế packet index
- thay thế startup bundle

Nó dùng để trả lời ngắn gọn:

> Trong project này hiện có những workstreams nào, mỗi workstream là gì, dùng khi nào, và route vào đâu?

### Core principle
AICOS chỉ đọc/trả về bản đồ workstream mà project đã chuẩn hóa hoặc chấp nhận.
AICOS không tự promote proposal thành active workstream nếu project chưa quyết định.

---

## 2. Why This Tool Exists

Nếu không có `aicos_get_workstream_index`, agent dễ phải suy ra routing từ:
- startup bundle
- packet index
- handoff/current
- current direction
- README/notes rải rác

Điều này có thể chấp nhận khi project nhỏ, nhưng về dài hạn dễ gây:
- lẫn lane
- broad reading
- packet usage sai
- route nhầm writeback

Tool này giải quyết đúng bài toán:
- **routing/context map**
- không gánh execution detail quá sâu

---

## 3. What This Tool Is Not

Tool này không phải:

- `aicos_get_packet_index`
- `aicos_get_current_direction`
- `aicos_query_project_context`
- `aicos_get_startup_bundle`

### Distinction
- `startup_bundle` = actor startup bundle
- `packet_index` = execution-facing packet map
- `current_direction` = current priority or next direction
- `query_project_context` = flexible bounded query
- `workstream_index` = project lane map

---

## 4. When This Tool Becomes Valuable

Tool này trở nên đặc biệt hữu ích khi project có:
- từ 3 workstreams trở lên
- nhiều packet gắn với nhiều lanes
- nhiều actors hoặc nhiều agent families
- recurring confusion about “which lane am I in?”
- need for clean routing before task execution

---

## 5. Input Shape

### Report Code: ARC-26302

Recommended minimal input:

```yaml
scope: "projects/<project-id>"      # required
actor: "A1 | A2-Core-C | A2-Core-R" # optional
include_candidate: false            # optional
status_filter:                      # optional
  - active
  - paused
  - deprecated
```

### Notes
- `scope` là bắt buộc
- `include_candidate` chỉ bật khi project muốn thấy candidate lanes
- `status_filter` giúp giữ output gọn

---

## 6. Output Shape

Recommended compact output:

```yaml
metadata:
  schema_version: "0.1"
  kind: "aicos.mcp.read_bundle"
  surface: "aicos_get_workstream_index"
  bundle_id: "workstream_index:<short-hash>"
  served_at: "<utc-iso-time>"
  scope: "projects/<project-id>"
  authority: "AICOS serves project-declared or project-accepted workstream structure; MCP is not the decision-maker for creating workstreams."
  source_refs:
    - path: "<repo-relative-path>"
      role: "workstream-index-source"
      exists: true

workstreams:
  - workstream_id: "<id>"
    title: "<short title>"
    purpose: "<short purpose>"
    when_to_use: "<short>"
    when_not_to_use: "<short optional>"
    main_entry_surfaces:
      - "<surface/path/ref>"
    typical_packets:
      - "<packet-id>"
    typical_outputs:
      - "<artifact kind or output kind>"
    default_writeback_lanes:
      - "<lane/path kind>"
    status: "candidate|active|paused|deprecated"
```

### Rules
- keep output bounded
- do not dump long markdown by default
- each workstream entry should be concise and routing-oriented

---

## 7. What Source This Tool Reads From

Tool này nên đọc từ **AICOS-side project context**, không nên đi trực tiếp vào external repo như primary authority.

Possible sources:
- project-level workstream index note in AICOS
- project routing/context note
- project evidence note that stores accepted workstream map
- compact normalized working/context surface

### Rule
AICOS only serves the workstream structure that the project has already declared, accepted, or normalized into AICOS.

---

## 8. Relationship To Workstream Suggestion Framework

A1 có thể dùng suggestion framework để đề xuất lane mới, nhưng `aicos_get_workstream_index` chỉ đọc:
- accepted workstreams
- or optionally candidates if project chooses to expose them

### Important
Do not let the tool blur:
- candidate suggestion
- accepted routing truth

If `include_candidate=false`, the tool should only return accepted/active structures.

---

## 9. Overlap Analysis

## 9.1. Overlap with `aicos_get_packet_index`
Some overlap exists, but not the same purpose.

- `packet_index` = packet execution map
- `workstream_index` = lane routing map

A packet can belong to a workstream, but packet index cannot fully replace lane routing.

## 9.2. Overlap with `aicos_get_current_direction`
Some overlap exists, but not the same purpose.

- `current_direction` = what should be prioritized now
- `workstream_index` = what lanes exist at all

## 9.3. Overlap with `aicos_get_startup_bundle`
Startup bundle may mention:
- default workstream
- current preferred path

But startup bundle should not become the full project lane atlas.

---

## 10. Why Design It Now Even If Not Implemented Immediately

Designing it now helps:
- keep packet index and routing logic conceptually separate
- give projects a clear target structure for workstream management
- avoid later ad hoc workstream metadata spread across README/handoff/packets
- keep MCP expansion modular

### Rule
Design now, implement when project complexity or actor confusion justifies it.

---

## 11. Validation Principles

When implementing later, validate that:
- `scope` exists
- workstream source exists
- entries are structurally coherent
- status values are valid
- output stays bounded

Do not enforce project-specific semantics in the generic tool itself.

---

## 12. Future Compatibility

This tool should remain compatible with:
- coding projects
- research projects
- content projects
- operations projects
- mixed-mode projects

That means:
- do not assume workstream equals code pipeline
- do not assume every workstream has packets
- do not assume every workstream has code outputs

Fields like:
- `typical_packets`
- `typical_outputs`
- `default_writeback_lanes`

may be empty lists where appropriate.

---

## 13. Recommended Repo Shape

Possible additions later:

```text
packages/aicos-kernel/contracts/mcp-bridge/
  workstream-index-surface.md

packages/aicos-kernel/aicos_kernel/
  mcp_workstream_index.py

integrations/local-mcp-bridge/
  aicos_mcp_stdio.py
```

Keep:
- contracts separate from implementation
- transport adapter thin

---

## 14. Final Recommendation

### Final recommendation

`aicos_get_workstream_index` should be designed now as a separate read surface because:

- it is not the same as packet index
- it is not the same as current direction
- it will likely matter as projects gain more lanes
- it helps keep routing/context logic clean

### Final rule
AICOS should use this tool to **serve** accepted workstream structure.
AICOS should not use this tool to **decide** workstream creation on behalf of projects.

---
