# Public Documentation Cleanup Guide

Status: draft

## Rule

Do not copy project-specific documents into the public repo verbatim.

Each document should be classified before export:

- Public template: safe reusable structure with placeholders.
- Public summary: sanitized explanation of the concept without private project
  details.
- Private only: contains project context, handoffs, evidence, logs, decisions,
  private names, business data, or local machine assumptions.

## Project-Specific Documents

Documents about a concrete project should usually become one of:

- `examples/sample-project/...` if the content can be rewritten as synthetic
  sample data.
- `templates/...` if the structure is reusable and all concrete context is
  removed.
- `docs/concepts/...` if the idea is useful but the source material is private.

Avoid exporting:

- handoffs
- checkpoints
- evidence
- source inventories
- delivery surfaces
- real project context ladders
- imported prompt packages
- private operational notes

## Role-Specific Context Docs

AICOS should expose project context by project-facing role, not only by internal
AICOS actor class. Public docs should distinguish:

- AICOS-internal actor class: A1, A2, A2-Core, A2-Serve.
- External project role: CEO, product owner, CTO, fullstack dev, reviewer,
  worker, operator.

Role-aware onboarding and query tools should accept the project role and current
state, then return bounded context appropriate to that role.
