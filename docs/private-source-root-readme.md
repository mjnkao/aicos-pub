# AICOS

Status: restructuring MVP

This root now contains the new AICOS structure only, plus the GBrain substrate
tooling needed for local-first MVP work.

## Current Structure

- `brain/`: durable knowledge, working reality, evidence, branch reality, and
  service knowledge.
- `agent-repo/`: operational rules and runtime lanes for A1, A2, humans, and
  future agent classes.
- `packages/aicos-kernel/`: deterministic schemas, contracts, validators,
  renderers, promotion primitives, write lanes, GBrain adapter, and thin CLI.
- `serving/`: generated capsules, branch packets, promotion review packets,
  truth helpers, and feedback.
- `backend/`: serving substrate only, not authority.
- `integrations/`: runtime and manual sync integration lanes.
- `docs/New design/`: current restructuring design documents.
- `docs/migration/`: migration notes and status.
- `backup/pre-restructure-20260418/`: legacy data moved out of the active root.

## Legacy Data

Old data is preserved in the remote Git branch:

```text
backup/pre-restructure-main
```

During the local cleanup, old data was also moved to a local ignored backup
folder:

```text
backup/pre-restructure-20260418/
```

Do not read or apply legacy material by default. If old material is needed,
inspect the backup branch or local backup folder selectively and copy only
reviewed, relevant pieces into the new structure.

## Local CLI

Use:

```bash
./aicos --help
```

## Full Local Install

For a fresh machine or a new agent installing AICOS from the GitHub repo, use:

```text
docs/install/AICOS_FULL_INSTALL_FOR_AGENTS.md
```

That guide covers HTTP daemon, PostgreSQL/pgvector, optional embeddings,
Codex HTTP-first MCP proxy, and fallback behavior.

## Agent Entry Points

All agents should read `AGENTS.md` first, then use the smallest matching
context ladder:

- A2-Core maintaining AICOS:
  `agent-repo/classes/a2-service-agents/onboarding/a2-core-context-ladder.md`
- A2-Serve candidate:
  `agent-repo/classes/a2-service-agents/onboarding/a2-serve-context-ladder.md`
- A1 project work:
  `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`
- Project-specific overview, when present:
  `brain/projects/<project-id>/working/context-ladder.md`

These ladders summarize what each file/group is for so a new agent can orient
without loading the whole repo. Source files remain authoritative.

A1 agents should use local MCP-first access for AICOS-facing context/control
plane reads/writes when available. Direct local repo/artifact access remains
correct for actual project work.
