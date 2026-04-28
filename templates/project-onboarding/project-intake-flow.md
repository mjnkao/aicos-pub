# AICOS Project Intake Flow

Status: active MVP flow
Updated: 2026-04-23

## Purpose

Define the minimum intake path for adding a project to AICOS without requiring
multiple clarification rounds and without importing broad external history by
default.

There are two modes:

- new project
- existing project import

## Mode 1: New Project

Use this when the project is starting now and does not already have substantial
context/history outside AICOS.

### Required Intake From A1/Human

- project id
- project name
- project type: code, content, design, research, ops, data, mixed, or other
- one-paragraph project summary
- desired first outcome
- known constraints
- expected artifact/runtime authority
- expected AICOS scope
- initial roles or collaborators, if known
- first useful task or decision

### A2-Core Output

A2-Core creates a compact project shell:

- `brain/projects/<project-id>/working/current-state.md`
- `brain/projects/<project-id>/working/current-direction.md`
- `brain/projects/<project-id>/working/handoff/current.md`
- `brain/projects/<project-id>/working/open-items.md`
- `brain/projects/<project-id>/working/open-questions.md`
- `brain/projects/<project-id>/working/context-ladder.md`
- project registry entry

Unknown fields should be marked as unknown or suggested defaults. Do not invent
specific project truth.

## Mode 2: Existing Project Import

Use this when a project already has a repo, docs, shared context, design files,
content archive, operational history, or other external context.

### Required Intake From A1/Human

- project id
- project name
- project type
- one-paragraph current project summary
- external authority location or artifact system
- what should remain external/runtime authority
- available source context inventory
- active/current context summary from the external project
- known risks or stale areas
- desired first AICOS-managed work
- whether AICOS may read files directly or must rely on text summaries

### A2-Core Output

A2-Core should instantiate or adapt the Import Kit:

- source inventory
- authority and lane mapping
- active context digest
- import validation checklist
- bootstrap output checklist
- A1 startup/import startup note when needed

Do not mirror the external project wholesale into AICOS. Import only current
active context needed for work, plus compact provenance refs.

## Authority Rule

AICOS is the context/control-plane authority after onboarding. External repos,
design tools, content systems, or operational systems remain runtime/artifact
authorities unless explicitly changed by a later decision.

## Writeback Rule

After A2-Core creates or imports the project, A1 should read/write AICOS-facing
continuity through MCP when available. Direct external artifact edits remain in
the external work authority.

## Follow-Up

Dedicated MCP intake tools may be added later if repeated onboarding shows this
markdown flow is too manual.
