# Getting Started With AICOS

Status: public staging guide

This guide shows how to use AICOS as a local context/control-plane for your own
project.

## What You Get

AICOS gives a project:

- compact project truth digests;
- current working state;
- role-aware onboarding surfaces;
- task packets;
- handoff and checkpoint lanes;
- local MCP access for agents.

AICOS does not replace your project repo. Your project repo remains the
authority for code, tests, runtime artifacts, source data, and generated output.

## Quick Start

1. Clone this repo.
2. Inspect the sample project:

```bash
find examples/sample-project -maxdepth 3 -type f | sort
```

3. Copy the sample project structure for your own project:

```bash
mkdir -p my-aicos-context
cp -R examples/sample-project/* my-aicos-context/
```

4. Replace sample names and paths:

```text
sample-project -> your-project-id
Sample Research Digest -> Your Project Name
```

5. Fill in the canonical and working files first:

```text
brain/project/canonical/project-profile.md
brain/project/canonical/project-brief.md
brain/project/canonical/architecture-baseline.md
brain/project/working/current-state.md
brain/project/working/current-direction.md
brain/project/working/context-ladder.md
```

6. Create one task packet only after you know the first concrete work item.

## Local MCP

The local MCP bridge lives at:

```text
integrations/local-mcp-bridge/
```

It is the intended access path for agents that need AICOS context and
continuity tools.

## Project Roles

When starting an agent, identify both:

- AICOS access mode: how the agent reads/writes AICOS context;
- project-facing role: CEO, product owner, CTO, fullstack dev, reviewer,
  worker, or operator.

The project-facing role controls which context is relevant.

## Safety

Do not import private logs, secrets, handoffs, generated output bulk, or raw
source mirrors. Start with compact digests and expand only for selected tasks.
