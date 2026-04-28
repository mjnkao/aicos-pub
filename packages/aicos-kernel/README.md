# AICOS Kernel

Status: active deterministic MVP substrate

The AICOS Kernel owns deterministic structure and local execution surfaces. It
does not own evolving service intelligence.

Current responsibilities:

- stable contracts and schema-oriented docs;
- packet rendering and validation primitives;
- safe write/read lane helpers;
- local CLI command groups;
- MCP read/write serving operations;
- GBrain adapter behavior;
- bounded mechanical helpers such as handoff compaction.

Current local CLI surface includes:

- `capsule`
- `branch`
- `option`
- `promote`
- `validate`
- `context`
- `sync`
- `mcp`
- `compact`

Evolving policy, option quality, promotion recommendation, retrieval strategy,
A2-Serve behavior, and project-health interpretation should mature in service
knowledge, skills, policies, or reviewed design docs before becoming kernel
logic.
