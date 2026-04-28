# Scope Layer Note Template

Status: future-extensible placeholder

Use this only when a company, workspace, project, workstream, or task needs a
small local rule note.

```yaml
scope: ""
layer: ""        # global | company | workspace | project | workstream | task
applies_to: ""
status: "draft"
loaded_when: ""
```

## Rules

- Do not create scope notes unless a real rule exists.
- Do not make company/workspace layers startup-default merely because this
  template exists.
- Keep higher-scope rules broad; keep task rules narrow.
- Project-specific rules must not override A1 core identity or lane boundaries
  silently.
