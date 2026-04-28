# AICOS Execution Decision Table

Status: architecture execution table  
Date: 2026-04-28  
Scope: `projects/aicos`

## Purpose

Turn the product framing, GBrain reuse critique, and broader market landscape
into an execution-oriented decision table.

This is not a final migration plan. It is the working table that helps AICOS
decide:

- what must stay AICOS-owned;
- what should be strongly considered for reuse/wrapping/forking;
- what is candidate for retirement;
- what nearby systems are relevant comparison points.

## Reference Systems Considered

- GBrain
- Memobase
- Membase
- GitAgent
- LangGraph / LangMem
- CrewAI
- Mem0
- Onyx
- Coworker OM1
- Letta
- Zep / Graphiti
- Atlan

## Reading Key

- **Keep**: core AICOS-owned layer; should remain product-owned.
- **Reuse/Wrap**: use external substrate ideas or components without giving up
  AICOS control-plane semantics.
- **Migrate/Fork candidate**: worth evaluating for deeper substrate adoption or
  a GBrain-derived path.
- **Retire**: likely custom code or direction that should stop growing if a
  stronger external substrate path is confirmed.

## Decision Table

| AICOS area | Why it exists | Closest external parallels | Current AICOS value | Decision | Why |
| --- | --- | --- | --- | --- | --- |
| Authority model (`truth` / `working` / `evidence` / `history`) | Keeps current truth and provenance unambiguous | Atlan (governance mindset), GBrain (primary home), Coworker OM1 (org memory) | Very high | **Keep** | This is core AICOS differentiation and not well solved as a generic reusable module |
| Project/runtime authority split | Separates AICOS control-plane from external repos/runtime systems | Weak direct match | Very high | **Keep** | This is one of the most important product-level semantics AICOS owns |
| Startup bundle / orientation / handoff discipline | Reduces startup confusion and continuity loss | LangGraph persistence/memory, Letta memory model, GitAgent framework conventions | Very high | **Keep** | External systems validate the need, but not the exact AICOS project-control shape |
| Status/checkpoint/handoff/feedback/artifact object model | Structured writeback and continuity semantics | LangGraph checkpoints, Letta memory blocks, GitAgent logs, Coworker OM1 traces | Very high | **Keep** | AICOS-specific operating model, not just memory storage |
| Actor/lane/worktree identity and coordination | Prevents ownership ambiguity and collisions | GitAgent identity/audit, Coworker organizational memory | Very high | **Keep** | This is closer to AICOS's real moat than memory itself |
| Project/company/workspace control-plane model | Organizes context at the right operational levels | Coworker OM1, Atlan context/governance, Onyx enterprise knowledge platform | High | **Keep** | Product identity layer; should not be outsourced |
| Project intake/import workflow | Brings new projects into AICOS cleanly | Weak direct match | High | **Keep** | Operational lifecycle specific to AICOS vision |
| MCP semantic read/write contracts | Enforces structured control-plane access | GBrain MCP, Memobase MCP, Mem0 tooling surfaces | High | **Keep**, but **Reuse/Wrap** runtime substrate beneath | Contract layer is AICOS-owned; transport/runtime implementation can be reduced |
| Retrieval/search substrate | Finds relevant context fast and cheaply | GBrain, Onyx, Mem0, Zep/Graphiti, Letta archival memory | Medium as custom value, high as capability | **Reuse/Wrap / Migrate candidate** | AICOS needs it, but it is not where AICOS is most differentiated |
| Search mode system (direct/keyword/hybrid) | Prevents misuse of search and improves retrieval quality | GBrain, Onyx, Letta, Zep | Medium | **Reuse/Wrap** | Strong substrate behavior already exists elsewhere |
| Chunking / snippet retrieval | Makes long-doc retrieval practical | GBrain, Letta archival memory, Onyx contextual retrieval, Zep Graphiti | Medium | **Reuse/Wrap / Migrate candidate** | Needed, but likely better sourced from a stronger substrate path |
| Embedding/index freshness / doctor / verify loop | Keeps search trustworthy | GBrain, Mem0, Onyx, LangGraph persistence discipline | Medium | **Reuse/Wrap / Migrate candidate** | This is operational substrate, not core AICOS differentiation |
| Maintenance jobs / recurring review loop | Prevents silent degradation | GBrain, LangGraph long-running state patterns, Coworker continuous OM1 updates | Medium | **Reuse/Wrap** | Use external patterns aggressively; keep only AICOS-specific policies |
| Relation hygiene / adjacency audit | Improves “what is related?” routing without graph overbuild | GBrain link discipline, Zep/Graphiti graph memory, Coworker OM1 graph recall | Medium | **Keep + Reuse patterns** | AICOS should keep the semantics, but learn from graph-aware systems |
| Relation-aware serving / graph retrieval | Stronger answers over connected project context | Zep/Graphiti, Coworker OM1, Atlan metadata graph | Low today, potentially high later | **Evaluate later** | Valuable, but easy to overbuild before relation hygiene is mature |
| Generic memory storage / retrieval plumbing | Persistent recall across sessions and threads | Memobase, Membase, Mem0, Letta, GBrain | Low as unique product value | **Reuse/Wrap / Migrate candidate** | This is a textbook substrate layer |
| Generic agent orchestration persistence | Long-running state/checkpoints/threads | LangGraph, CrewAI, Letta | Low as unique product value | **Reuse/Wrap** | Useful, but should not replace AICOS semantics |
| Enterprise knowledge search + connectors | Broad organizational search across apps/docs | Onyx, Coworker OM1, Atlan | Medium | **Reuse patterns; maybe partner** | Useful for future company/workspace context, but not core AICOS control-plane by itself |
| Permission-aware organizational memory | Large-scale enterprise context with boundaries | Coworker OM1, Atlan | Medium to high long-term | **Future reuse/partner candidate** | Very relevant to long-term "company knowledge for AI agents" path |
| Generic second-brain / universal memory positioning | Broad memory product for many use cases | Membase, Memobase, Mem0, Letta | Low as AICOS-specific value | **Do not pivot into this** | Would blur product identity and broaden scope too early |

## Product Examples By Category

### Systems that are strongest as substrate/memory/runtime

- **GBrain**: best current reference for search/query/runtime discipline
- **Mem0 / Memobase / Membase / Letta**: strongest references for memory layer
- **LangGraph / CrewAI**: strongest references for stateful agent runtime and
  orchestration

### Systems that are strongest as context/governance layer

- **Atlan**: strongest governance/context-layer analog, but in data/metadata
  domain
- **Coworker OM1**: strongest “organizational memory” analog to AICOS long-term
  direction
- **Onyx**: strongest enterprise knowledge + agents + search analog
- **Zep / Graphiti**: strongest graph-memory analog for evolving context

### Systems that validate AICOS identity / audit / versioning concerns

- **GitAgent**

## Practical Execution Guidance

### Things AICOS should actively stop expanding unless justified

1. custom generic memory plumbing
2. custom search substrate work when external substrate is already stronger
3. broad product drift into generic enterprise search or generic second-brain
   territory
4. graph-heavy ambitions before relation hygiene and product semantics are ready

### Things AICOS should actively continue investing in

1. authority boundaries
2. control-plane object model
3. startup/handoff/status/checkpoint semantics
4. multi-agent ownership and continuity rules
5. intake/import/governance behavior

### Things AICOS should evaluate for substrate reduction next

1. retrieval eval + benchmark discipline
2. direct/keyword/hybrid mode runtime
3. chunking and long-doc retrieval
4. doctor/verify/maintenance loop
5. generic memory retrieval/storage plumbing

## Best Next Step

The next architecture pass should produce a concrete inventory of current AICOS
modules and classify each into:

- **Keep**
- **Reuse/Wrap**
- **Migrate/Fork candidate**
- **Retire**

That will turn this product-level decision table into an implementation
roadmap.
