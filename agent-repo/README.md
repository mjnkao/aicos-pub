# AICOS Agent Repo

Status: active actor-operations lane for restructuring MVP

`agent-repo/` holds operational behavior for humans and agent classes. It is
not the project truth lane.

It contains:

- startup cards and onboarding ladders;
- rule cards and longer rules;
- task packet indexes and selected task packets;
- actor task/backlog lanes;
- human approval/manager/reviewer role policies.

Project reality belongs in `brain/projects/<project-id>/`. Agents should use
the smallest actor-appropriate ladder first, then load only the task packet,
rule card, or source files required by the selected task.
