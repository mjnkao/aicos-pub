# Cross-Project Context Policy

Status: active MVP policy
Updated: 2026-04-22

## Purpose

Prevent agents from leaking or misapplying context across projects as AICOS
scales beyond one local project.

## Default Rule

Project context is isolated by default.

An agent working on `projects/<project-id>` should read that project's startup
bundle, registry entries, status items, handoff, task packets, and artifacts
before using another project's context.

## Allowed Cross-Project Reads

Cross-project context may be read when one of these is true:

- the current task explicitly names the other project;
- `brain/shared/project-registry.md` declares a dependency or shared-service
  relationship;
- the other project is AICOS itself and the task is about AICOS tooling,
  policy, MCP, onboarding, or serving behavior;
- the human asks for comparison, migration, import, public export, or audit;
- an artifact reference or task packet explicitly points to the other project.

## Disallowed Defaults

Agents must not:

- apply another project's current-state as current truth for this project;
- copy task/handoff/status continuity across projects by habit;
- treat external project docs as AICOS current truth unless imported/promoted;
- use a public-export or template project as private project truth;
- infer dependencies from branch names, recent commits, or similar filenames.

## Write Rule

When cross-project context influences work, the writeback should mention the
source project in `source_ref`, `artifact_refs`, or a short note. Do not write
updates for project A into project B's status/task/handoff lanes unless the
task explicitly owns that cross-project operation.

## Registry Rule

`brain/shared/project-registry.md` is the MVP discovery surface for known
projects and exposure mode. It is not a complete dependency graph yet.

Future project registry tooling may replace the markdown registry only after a
truth-store ADR update or explicit implementation decision.
