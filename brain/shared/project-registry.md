# Public AICOS Project Registry

Status: active

This registry lists public-safe project scopes available through AICOS Railway.
Project truth remains under `brain/projects/<project-id>/`.

## Projects

### aicos

- Scope: `projects/aicos`
- Role: Public AICOS core/runtime project
- Protected writes: yes
- First reads:
  - `aicos_get_startup_bundle`
  - `aicos_get_handoff_current`
  - `aicos_get_status_items`

### aicos-pub

- Scope: `projects/aicos-pub`
- Role: Public-export and community distribution lane
- Protected writes: no
- First reads:
  - `aicos_get_handoff_current`
  - `aicos_get_startup_bundle`

### templates

- Scope: `projects/templates`
- Role: Public templates and reusable examples
- Protected writes: no
- First reads:
  - `aicos_get_handoff_current`
  - `aicos_get_startup_bundle`

### agents-dashboard

- Scope: `projects/agents-dashboard`
- Alias: `projects/agents-pm-dashboard`
- Role: AI Agent PM Dashboard coordination scope
- Local code path: `/Users/minh/Projects/agents-pm-dashboard`
- Git repository: `git@github.com:mjnkao/ai-agent-pm-dashboard.git`
- GitHub URL: `https://github.com/mjnkao/ai-agent-pm-dashboard`
- Protected writes: no
- First reads:
  - `aicos_get_handoff_current`
  - `aicos_get_startup_bundle`
  - `aicos_query_project_context`

## Agent Notes

If an agent is working on the dashboard repo, prefer
`scope=projects/agents-dashboard`. The alias `projects/agents-pm-dashboard`
exists only to reduce confusion with the local folder name.
