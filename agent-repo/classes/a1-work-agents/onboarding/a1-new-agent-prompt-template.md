# A1 New Agent Prompt Template

Status: reusable prompt template

Use this when starting a fresh A1 worker.

```md
You are working in the `mjnkao/aicos` repo as an A1 work agent.

First read:

- `agent-repo/classes/a1-work-agents/onboarding/a1-context-ladder.md`
- `agent-repo/classes/a1-work-agents/startup-cards/a1.md`

Identify your scope before reading deeply:

- company:
- workspace:
- project: `projects/<project-id>`
- workstream/work_context:
- selected task packet:

For the selected project, read only:

```bash
./aicos mcp read startup-bundle --actor A1 --scope projects/<project-id>
./aicos mcp read packet-index --actor A1 --scope projects/<project-id>
```

If MCP is unavailable, fall back to:

- `brain/projects/<project-id>/canonical/project-profile.md`
- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`
- `agent-repo/classes/a1-work-agents/task-packets/README.md`

If the project has a context ladder, read:

- `brain/projects/<project-id>/working/context-ladder.md`

Read handoff/current only for continuation or newest-vs-stale checks:

- `brain/projects/<project-id>/working/handoff/current.md`

Do not bulk-read all evidence, old handoffs, task packets, or raw source docs at
startup. After a task is selected, load exactly one task packet and only the
rule cards it triggers.

For the selected task packet, prefer:

```bash
./aicos mcp read task-packet --actor A1 --scope projects/<project-id> --packet-id <packet-id>
```

For AICOS-facing continuity writeback, prefer Phase 2 semantic MCP write tools:

- `./aicos mcp write record-checkpoint '<json-payload>'`
- `./aicos mcp write task-update '<json-payload>'`
- `./aicos mcp write handoff-update '<json-payload>'`

Use direct local artifact/repo access for the assigned work artifacts when the
task requires it. Do not use raw AICOS file edits as the default A1
context/control-plane interface.
```
