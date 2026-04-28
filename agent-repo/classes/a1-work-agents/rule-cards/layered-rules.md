# Rule Card: A1 Layered Rules

Load when deciding which rules apply to an A1 task.

## Rule Stack

Use the smallest applicable stack:

1. A1 core rules: actor identity, checkpoint, writeback, escalation, packet-first
   startup, and artifact-neutral continuity.
2. Higher-scope rules if they exist and are relevant: company, then workspace.
3. Project rules: `brain/projects/<project-id>/...`.
4. Workstream/task rules: only from the selected packet, workstream note, or
   explicit human instruction. These lower layers define whether the work is
   code, docs, design, content, research, operations, or hybrid.

## Current MVP

Company/workspace A1 rule layers are future extension points. Do not require
them at startup unless a task packet or human explicitly points to them.

## Do Not

- turn one project rule into a global A1 rule
- turn one task workflow into a project rule
- load all possible rule layers by default
- treat code/git/repo assumptions as universal A1 defaults
- treat backend, serving, or raw evidence as authority
