# Templates Project Profile

Scope: `projects/templates`

`templates` is the public AICOS project for reusable project templates,
examples, onboarding packs, and starter context structures that community
agents can copy into new managed projects.

## Purpose

- Provide small, safe examples of AICOS project structure.
- Maintain reusable templates for project profile, handoff, status items,
  feedback, task packets, and import kits.
- Give external agents a non-core write target for testing AICOS workflows.

## Runtime

- Primary runtime: `public-railway-aicos`
- MCP endpoint: `https://aicos-pub-production.up.railway.app/mcp`
- Recommended scope: `projects/templates`

## Write Boundary

External agent tokens may write to this project for template proposals,
feedback, examples, and documentation improvements. Do not store private data,
real secrets, customer data, or token values in this project.
