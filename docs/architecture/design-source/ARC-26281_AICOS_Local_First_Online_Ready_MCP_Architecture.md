# ARC-26281 — AICOS Local-First, Online-Ready MCP Architecture For Multi-Actor Project Work

**Status:** architecture-brief-v1
**Project:** AICOS
**Date:** 2026-04-19
**Primary scope:** AICOS MCP design
**Purpose:** thiết kế kiến trúc MCP cho AICOS theo các mục tiêu:

- chạy tốt trên **local** ngay bây giờ
- không cản trở việc chuyển thành **online MCP server** sau này
- tối ưu cho **A1 MCP-first context usage**
- vẫn cho phép **A2 direct repo access** khi phù hợp
- hỗ trợ nhiều **actor** và nhiều **agent family** khác nhau cùng tham gia một project
- ưu tiên:
  - nhanh
  - tiết kiệm token
  - context đủ và đúng
  - tiến hóa được theo thời gian

Các agent family được giả định có thể cùng tham gia:

- Codex
- Claude
- OpenClaw
- future A1/A2 runtimes khác

---

## 1. Executive Summary

### Core architectural direction

AICOS nên xây MCP theo hướng:

### **local-first, contract-stable, online-ready**

Điều đó có nghĩa là:

#### Phase hiện tại
- MCP chạy local
- transport ưu tiên `stdio`
- mục tiêu chính là giải quyết:
  - cross-folder context access
  - packet/handoff/startup retrieval
  - structured writeback/checkpoint
  - permission-safe multi-agent collaboration

#### Phase sau
- cùng contract đó có thể được expose qua server transport online
- không cần rewrite toàn bộ surface
- chỉ thay transport, auth/session, deployment model, và một số operational controls

### Strategic rule

AICOS MCP **không phải truth layer mới**.

AICOS MCP là:
- **access / control-plane layer**
- đứng trước AICOS truth
- expose đúng context/control surfaces cần cho actor
- validate/write back có kiểm soát

### Authority remains unchanged

- `brain/` = durable truth
- `agent-repo/` = actor operations/rules/packets
- external project repo = code/runtime authority
- MCP = structured access path, not the truth store

---

## 2. Design Goals

## 2.1. Local-first practicality
MCP phải chạy tốt trên local ngay, không đòi:
- remote infra
- cloud daemon
- central deployment
- auth stack lớn

## 2.2. Online-ready evolution
MCP contract phải được thiết kế sao cho:
- local `stdio` hôm nay
- local daemon ngày mai
- online server về sau

vẫn dùng cùng logic surface ở mức cao.

## 2.3. A1 MCP-first context discipline
A1 phải dùng MCP cho:
- startup
- handoff
- packet retrieval
- checkpoint/writeback

để tránh phụ thuộc broad filesystem access và stale local copies.

## 2.4. A2 flexibility
A2 vẫn có thể:
- đọc trực tiếp repo AICOS
- sửa trực tiếp file AICOS
- dùng MCP khi tiện

A2 không bị khóa cứng bởi policy của A1.

## 2.5. Token-efficient context serving
MCP phải giảm broad reading và context wandering.
Nó không được trở thành “cat file over RPC”.

## 2.6. Multi-actor / multi-family compatibility
Codex, Claude, OpenClaw, hoặc future clients phải có thể cùng gọi một contract logic ổn định.

## 2.7. Evolvable over time
MCP phải mở rộng được:
- surface
- validation
- cache
- transport
- observability
- auth/session
mà không phải rewrite từ đầu.

---

## 3. Non-Goals

MCP architecture này không nhằm:

- thay thế toàn bộ raw file access cho mọi actor
- ép A2 phải qua MCP cho mọi thao tác
- trở thành truth store mới
- mirror toàn bộ repo/project context thành resource thô
- build full event bus hoặc orchestration engine ngay
- build remote multi-tenant infra ở phase hiện tại
- biến local MCP thành framework nặng trước khi read/write surfaces cốt lõi được chứng minh

---

## 4. Authority Model

## 4.1. AICOS truth authority
AICOS truth vẫn nằm ở:

- `brain/`
- `agent-repo/` (cho actor operations)
- selected AICOS runtime/support lanes nếu có

MCP không thay đổi authority này.

## 4.2. External project authority
External repo/checkout vẫn là authority cho:

- code
- scripts
- tests
- runtime
- generated runtime artifacts
- repo-local workflow

## 4.3. MCP authority
MCP không phải authority cho nội dung.
MCP chỉ là authority cho:

- **how context is served**
- **how writeback is accepted**
- **how actor intent is mapped into AICOS lanes**
- **how validations are enforced**

### Rule
MCP is an access/control plane, not a source-of-truth plane.

---

## 5. Actor / Agent Family Model

## 5.1. Two actor classes
At minimum, design should distinguish:

### A2 actors
- system shapers / maintainers
- may access AICOS directly
- may use MCP optionally
- lower need for strict mediation

### A1 actors
- work operators
- should be MCP-first for AICOS-facing context/control operations
- often operate in external checkout
- most sensitive to permission constraints

## 5.2. Multiple agent families
AICOS MCP should assume clients may include:

- Codex
- Claude
- OpenClaw
- future custom A1/A2 runtimes

### Rule
Do not design MCP around the quirks of only one client.

## 5.3. Client-specific adapters allowed
Client-specific wrappers/adapters may exist later, but:
- core MCP surface should remain family-neutral
- per-client adaptation should stay thin

---

## 6. Architectural Layers

### Layer 1 — Truth layer
Files in AICOS and external repos.

### Layer 2 — MCP operations layer
Core implementation logic that:
- reads normalized context
- builds compact bundles
- validates writeback payloads
- maps writes to correct lanes

### Layer 3 — Transport layer
Current:
- local `stdio`

Later:
- local host/daemon
- online HTTP transport

### Layer 4 — Client adapter layer
How Codex / Claude / OpenClaw consume MCP.

### Rule
Keep Layer 2 stable.
Allow Layer 3 and Layer 4 to evolve.

---

## 7. Transport Strategy

## 7.1. Phase 1 — local stdio
Recommended now:
- MCP server launched as local subprocess
- best fit for local tool clients
- smallest operational burden
- good for permission-safe local bridging

## 7.2. Phase 2 — optional local host/daemon
If needed later:
- a local always-on bridge host
- useful for shared caching, session reuse, local metrics, or multi-client coordination

## 7.3. Phase 3 — online-ready server
Later, the same logical surface can be exposed via online transport.
At that point, you add:
- auth
- session management
- deployment
- network security
- tenancy controls

### Rule
Do not bake online assumptions into current Phase 1 implementation.

---

## 8. Surface Design Principle

### Core rule
Design **bundle-first**, not file-first.

That means:
- do not expose every file as the primary unit
- do not make agents fetch 15 tiny things to reconstruct one startup state

Instead expose:
- compact bundles
- compact indexes
- compact targeted write tools

### Why
This improves:
- speed
- token efficiency
- consistency
- permission control
- multi-client portability

---

## 9. Recommended A1-Facing Surface

## 9.1. Read-serving first
### Report Code: ARC-26282

Recommended initial read surface:

- `aicos_get_startup_bundle`
- `aicos_get_handoff_current`
- `aicos_get_packet_index`
- `aicos_get_task_packet`

### Why these first
These are the minimum needed to stop depending on raw cross-folder access.

## 9.2. Writeback next
Recommended initial write surface:

- `aicos_record_checkpoint`
- `aicos_write_task_update`
- `aicos_write_handoff_update`

### Why these next
These enforce continuity discipline and remove the need for raw file writes into AICOS.

## 9.3. Later optional read surfaces
Later, consider:

- `aicos_get_current_direction`
- `aicos_get_open_questions`
- `aicos_get_open_items`
- `aicos_get_active_risks`
- `aicos_get_workstream_index`

### Rule
Do not launch with a giant surface.

---

## 10. Resource / Tool / Prompt Split

AICOS MCP should separate concerns clearly.

## 10.1. Resources
Use for:
- stable or semi-stable read surfaces
- context bundles
- indexes
- current compact digests

Examples:
- startup bundle resource
- handoff/current resource
- packet index resource

## 10.2. Tools
Use for:
- explicit action
- writeback
- checkpointing
- mutation with validation

Examples:
- checkpoint write
- task update write
- handoff update write

## 10.3. Prompts
Use for:
- guided startup flows
- optional operator helpers
- human-triggered guidance surfaces

### Rule
Do not collapse everything into tools.
Do not use prompts as the primary truth path.

---

## 11. Context Packaging Strategy

## 11.1. Startup bundle
Must be:
- compact
- packet-first
- lane-aware
- enough for actor startup without broad reading

Should include:
- role/scope
- current-state digest
- current-direction digest if needed
- handoff pointer or compact handoff
- packet index
- rule card pointers

## 11.2. Packet bundle
Should include:
- selected packet content
- minimal rule pointers
- allowed write lanes
- expected success condition
- handoff refs

## 11.3. Handoff bundle
Should include:
- current H1 handoff
- enough recency/authority markers
- no broad history dump

### Rule
Each bundle must answer one operational question well.

---

## 12. Freshness / Versioning / Traceability

To keep A1 honest and reduce stale-context drift:

## 12.1. Every served bundle should have trace metadata
For example:
- bundle id
- source refs
- timestamp
- version or revision marker

## 12.2. Every meaningful writeback should refer to served context
For example:
- startup bundle ref
- packet ref
- handoff ref if continuation-sensitive

## 12.3. Completion review should require MCP trace
If an A1 result cannot say:
- what startup/packet/handoff surfaces it used
then it should be treated as weakly grounded.

### Rule
Traceability is part of anti-laziness design.

---

## 13. Cache Strategy

## 13.1. Local cache is optional
A local cache may exist later for:
- faster repeated startup
- client convenience
- temporary staging

## 13.2. Local cache is secondary
Cache must remain:
- non-authoritative
- replaceable
- refreshable
- ignorable by reviewers

## 13.3. Prefer server-built compact bundles over client-built cache heuristics
The server should own:
- bundle shaping
- freshness markers
- version refs

### Rule
Do not let cache become shadow authority.

---

## 14. Performance Strategy

## 14.1. Optimize for fewer, richer reads
Prefer:
- one startup bundle
- one packet bundle
- one handoff bundle

over:
- many tiny file-like reads

## 14.2. Keep bundle size bounded
Bundles should be:
- short enough for token economy
- rich enough for correct action
- split by purpose

## 14.3. Keep write payloads small and explicit
Write tools should accept:
- narrow structured payloads
- explicit intended effect
- actor/scope/task refs

### Rule
Do not make MCP chatty.

---

## 15. Token Strategy

## 15.1. MCP can reduce token cost
If designed well, MCP reduces token cost by:
- avoiding broad raw file reads
- reducing repeated startup wandering
- serving compact normalized context

## 15.2. MCP can increase token cost if designed badly
It will become expensive if:
- bundles are bloated
- file contents are mirrored too literally
- agents call too many tiny surfaces repeatedly

## 15.3. Token discipline principle
The right question is not:
- “MCP hay direct raw access rẻ hơn?”

The right question is:
- “What surface returns exactly enough context for the actor’s next bounded action?”

---

## 16. Multi-Actor Concurrency Considerations

## 16.1. Many actors may touch one project
AICOS should assume:
- multiple A1 actors
- A2 maintainers
- multiple agent families
- same project, different sessions

## 16.2. Coordination should happen through structured continuity
MCP should help unify:
- current state reads
- packet reads
- checkpoint writes
- handoff updates

## 16.3. Avoid file-level race assumptions
Do not assume all clients will coordinate safely through raw file edits.

### Rule
Use structured write tools to reduce cross-client ambiguity.

---

## 17. Evolution Strategy

This is one of the most important sections.

## 17.1. Start with stable contract, not big implementation
Evolve:
- contract first
- minimal implementation second
- richer surface later

## 17.2. Version surfaces explicitly
When the MCP contract grows, use:
- clear version markers
- deprecation notes
- compatibility windows where possible

## 17.3. Add new surface only after evidence
A new read/write tool should only be added when:
- repeated actor pain exists
- current bundles are not enough
- the new surface has clear bounded purpose

## 17.4. Keep transport swappable
Do not let local-only assumptions leak into the operations layer.

## 17.5. Preserve phase separation
- Phase 1: read-serving
- Phase 2: writeback
- Phase 3: richer surfaces / cache / observability
- Phase 4: online deployment concerns

### Rule
Evolution should be additive and evidence-driven.

---

## 18. Recommended Implementation Sequence

## 18.1. Phase 1 — A1 read-serving MCP
Implement only:
- startup bundle
- handoff/current
- packet index
- selected packet

Goal:
- remove raw cross-folder read dependency

## 18.2. Phase 2 — A1 writeback MCP
Implement:
- checkpoint
- task update
- handoff update

Goal:
- remove raw cross-folder write dependency

## 18.3. Phase 3 — observability and cache
Add only if needed:
- request logging
- metrics
- local cache
- trace helpers

## 18.4. Phase 4 — online-ready hardening
Later:
- auth
- sessions
- multi-client HTTP transport
- deployment packaging

---

## 19. Recommended Review Questions

### Checklist Code: ARC-26283

- [ ] Does the surface solve a real A1 cross-folder problem?
- [ ] Is the bundle compact and bounded?
- [ ] Is the write payload structured and small?
- [ ] Does the design reduce dependence on broad filesystem permissions?
- [ ] Is the surface family-neutral across Codex / Claude / OpenClaw?
- [ ] Can the same operations layer survive a later transport change?
- [ ] Does the design avoid making cache or MCP itself into a truth store?
- [ ] Does the design provide enough traceability to detect stale-context behavior?

---

## 20. Final Architectural Recommendation

### Final recommendation

Build AICOS MCP as:

- **local-first**
- **bundle-first**
- **A1 MCP-first for context/control-plane**
- **A2 direct-access optional**
- **transport-swappable**
- **multi-family compatible**
- **token-aware**
- **evolution-ready**

### Practical form

Right now:
- local `stdio`
- read-serving first
- writeback second
- no giant surface
- no truth-store duplication

Later:
- same operations layer
- online-capable transport
- stronger session/auth controls
- richer observability
- broader multi-actor coordination

### Final rule
Do not build MCP as “RPC around raw files.”
Build it as a **compact context/control plane** that serves the right actor the right amount of truth at the right time.

---
