# AICOS Issue Map

Status: working map for staged discussion and prioritization.

Purpose: keep important AICOS design problems visible without forcing deep work
on all of them at once. Use this map to decide what to discuss first, what can
wait, and which issues depend on others.

## Foundation Issues

These shape the long-term quality of AICOS truth, readability, and scalability.
They should usually be understood before deeper productization.

1. Information architecture for `brain/`
   - How to keep markdown-first truth modular, readable, and maintainable.
   - How to avoid oversized files and uncontrolled document sprawl.

2. Multi-resolution reading model
   - How to provide executive, architecture, implementation, and task-level
     views without duplicating truth.
   - How different actors should enter the same project at different depth.

3. Canonical vs working vs evidence boundaries
   - What belongs in canonical truth, current working reality, evidence, and
     generated views.
   - How to prevent authority confusion as the repo grows.

4. Soft grammar vs rigid templates
   - Which structural primitives should be standardized across projects.
   - Which parts should remain project-specific and adaptable.

5. Project-specific information architecture profiles
   - How each project can define its own reading surfaces and modular structure
     while still fitting the AICOS system.

## Enabler Issues

These improve continuity, coordination, and practical adoption once the
foundation is clearer.

6. Context ladder design across projects
   - When a project needs its own context ladder.
   - How ladders should stay concise, actor-aware, and level-based.

7. Task packet and handoff depth
   - How much detail task packets and handoffs should carry.
   - How to keep continuity cheap without turning handoff into heavy docs.

8. Cross-project knowledge model
   - What belongs at company, workspace, project, workstream, and task levels.
   - How shared knowledge and project-specific knowledge should connect.

9. Import and sync strategy for external projects
   - How much truth to import from project repos into AICOS.
   - How to keep imported context useful without making it stale or heavy.

10. MCP-first context/control-plane boundaries
   - Which AICOS operations should go through MCP.
   - How MCP should relate to raw repo access, external repos, and local-first
     workflows.

## Later-Stage Productization Issues

These matter a lot, but they should follow stronger foundations and a clearer
operating model.

11. Storage strategy evolution
   - When markdown-first remains enough.
   - When thin DB-backed registries or structured stores become worth adding.

12. Coordination and orchestration surface
   - How AICOS should evolve from context/control-plane substrate toward richer
     coordination for humans and agents.
   - What task visibility, actor tracking, and dashboard surfaces are actually
     needed.

13. Product surface progression
   - When CLI + markdown review flow is no longer enough.
   - When UI, public API, remote transport, auth, or stronger workflow
     automation should become active priorities.

## Suggested Use

- First: expand or refine this issue map until the major problem space feels
  complete enough.
- Second: prioritize the issues by leverage, urgency, and dependency.
- Third: choose one issue at a time for deeper framing, tradeoff analysis, and
  implementation planning.

Do not treat this file as a canonical solution. It is a working map for staged
A2-Core discussion.
