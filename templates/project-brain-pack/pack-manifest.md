# Project Brain Pack Manifest

Status: template
Pack id: `aicos-project-brain-pack-v0`

## Boundary

This pack defines the minimum files a project brain needs so human managers and
AI agents can orient, continue, report feedback, and avoid stale context.

The pack is template material. It is not authoritative truth for any real
project until copied or mounted as a project-specific brain.

## Required Files

```text
canonical/project-profile.md
working/context-ladder.md
working/current-state.md
working/current-direction.md
working/handoff/current.md
working/open-items.md
working/open-questions.md
working/status-items/sample-next-step.md
working/feedback/README.md
working/task-state/README.md
evidence/README.md
```

## Optional Files

```text
canonical/architecture.md
canonical/decisions.md
working/artifact-refs/
working/workstreams/
evidence/import-kit/
```

Add optional files only when the project has real content. Do not add empty
folders just to look complete.

## Replace Before Use

- `sample-project`
- `Sample Project`
- owner names
- repo/runtime paths
- current status
- task/status item IDs

## Minimal A1 Read Order

1. `working/context-ladder.md`
2. `canonical/project-profile.md`
3. `working/current-state.md`
4. `working/current-direction.md`
5. `working/handoff/current.md` only for continuation/newest-state checks
6. `working/status-items/` only after current orientation

## Minimal Writeback Lanes

- Checkpoints: `evidence/checkpoints/` through MCP semantic write tools.
- Handoff: `working/handoff/current.md` through MCP semantic write tools.
- Status items: `working/status-items/` through MCP semantic write tools.
- Feedback: `working/feedback/` through MCP semantic write tools.

## Safety

A1 agents should not write raw markdown directly into AICOS brain state when
HTTP MCP is available. A2 maintainers may edit template files directly when
maintaining AICOS itself.
