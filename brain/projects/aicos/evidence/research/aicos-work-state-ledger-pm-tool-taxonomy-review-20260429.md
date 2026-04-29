# AICOS Work State Ledger PM Tool Taxonomy Review

Status: research memo
Date: 2026-04-29
Scope: `projects/aicos`
Actor: `A2-Core-R/C`

## Purpose

Research how general-purpose PM/work-tracking tools model work before AICOS
defines its own Work State Ledger.

The goal is not to copy a PM tool. The goal is to reuse proven vocabulary and
relationship patterns so AICOS can normalize tasks, checklist items, open
items, open questions, tech debt, decision follow-ups, phases, and milestones
without becoming a PM product.

## Sources Reviewed

Primary/general-purpose:

- Plane work items / projects / cycles / modules:
  `https://www.mintlify.com/makeplane/plane/features/issues`
- Plane cycles:
  `https://plane.so/cycles`
- ClickUp tasks API:
  `https://developer.clickup.com/docs/tasks`
- ClickUp relationships:
  `https://help.clickup.com/hc/en-us/articles/6309965212567-Create-task-Relationships`
- Asana object hierarchy:
  `https://developers.asana.com/docs/object-hierarchy`
- Notion database/page properties and relations:
  `https://developers.notion.com/guides/data-apis/working-with-databases`
  and `https://developers.notion.com/reference/page-property-values`
- Airtable linked records:
  `https://support.airtable.com/docs/linking-records-in-airtable`
- Trello boards/lists/cards and checklists:
  `https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/`
  and `https://developer.atlassian.com/cloud/trello/rest/api-group-checklists/`
- Monday subitems and multi-level boards:
  `https://support.monday.com/hc/en-us/articles/360011905480-All-about-subitems`
  and `https://developer.monday.com/api-reference/docs/working-with-multi-level-boards`

Secondary/software-heavy references were intentionally not used as the primary
model. Linear, Jira, and GitHub Issues remain useful later, but AICOS must also
serve content, design, research, ops, and hybrid projects.

## Comparison Table

| Tool | Best reusable concept | Object hierarchy | Relationship model | Checklist/subtask handling | Status model | Fit for coding/content/design/research | What AICOS should reuse | What AICOS should not copy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Plane | Work item as flexible unit; cycles/modules as optional planning overlays | Workspace -> Project -> Work Items; cycles/modules/pages inside projects | Sub-work items, relations, blockers, duplicates, modules, cycles | Sub-work items can break down larger items; modules/cycles group work without becoming parent truth | Custom workflow states; cycle states active/upcoming/completed | Strong for software but increasingly useful for agent work and docs/issues together | Work item core, optional cycles/modules, blocker/related/duplicate links, progressive complexity | Do not inherit software-first sprint bias as default for all projects |
| ClickUp | Rich hierarchy plus explicit relationships/dependencies | Workspace -> Space -> Folder -> List -> Task -> Subtask/checklist | Parent field for subtasks; task links and dependencies via relationships | Subtasks are task-like; checklists are lighter embedded completion lists | Status and priority per task/list | Good general-purpose fit across ops/content/design, but can become hierarchy-heavy | Parent/subtask vs checklist distinction; dependency/link separation | Do not copy deep hierarchy or force all projects into Space/Folder/List structure |
| Asana | Work Graph: tasks can belong to multiple projects; subtasks are tasks with one task parent | Workspace/Org -> Team -> Project -> Task; Portfolios group projects; Goals above work | Tasks can be in multiple projects; dependencies; subtasks can also be in projects | Subtasks are tasks, but with one task parent; Asana warns against deep sub-subtasks | Project sections and task status/completion; goals and portfolios above | Very good general work model for non-code and cross-functional work | Multi-home/derived views, task-as-basic-unit, portfolio/project/task distinction | Do not copy full portfolio/goal system yet |
| Notion | Database/page as flexible typed record with relations/rollups | Workspace/page tree + databases; pages are records inside databases | Relation properties link pages across databases; rollups summarize related pages | No native task-subtask hierarchy by default; relation/self-relation can model it | Status property and arbitrary selects | Excellent for content/research/design context and custom schemas | Pages/records as inspectable source-linked objects; relation properties; status as schema field | Do not make arbitrary database schemas the semantic core |
| Airtable | Separate tables plus linked records for many-to-many modeling | Base -> Table -> Record -> Fields/views/interfaces | Linked records model 1-n/n-n relationships; fields define workflow-specific attributes | No native task checklist model; child tables or linked records model checklists/subtasks | Select/status fields per table | Strong for structured content/research/ops data, less natural for agent handoff by itself | Linked-record discipline, separate tables for distinct object types, view-specific projections | Do not turn every AICOS relation into a table/database too early |
| Trello | Simple board/list/card/checklist model | Workspace/Org -> Board -> List -> Card -> Checklist -> Check item | Lists are workflow columns; cards have labels/members/actions/checklists; limited native relation semantics | Checklist items are embedded under card/checklist; not full tasks by default | List membership often represents workflow status; cards can be archived | Good simple model for lightweight teams/content/design, weak for complex dependencies | Card + checklist distinction; checklist items as lightweight children; board/list as view, not truth | Do not use list position as authoritative state for AICOS truth |
| Monday.com | Board/item/subitem with columns and multi-level subitems | Workspace/folder -> Board -> Group -> Item -> Subitem levels | Connected boards/dependency columns; subitems can have separate column structure | Subitems add deeper structure and can have their own columns; multi-level boards now exist | Status columns and board-specific workflows | Broad general-purpose fit, strong for ops/content but can become schema-heavy | Item/subitem plus columns; separate parent/child field schemas; status columns as projection | Do not copy UI/table-centric board semantics into AICOS core |

## Relationship Patterns Worth Reusing

### 1. One Core Work Object

Most tools converge on one primary unit:

- Plane: work item / issue
- ClickUp: task
- Asana: task
- Trello: card
- Airtable/Notion/Monday: record/item/page

AICOS should use one normalized core object: `work_item`.

Existing names such as open item, open question, tech debt, decision follow-up,
task, phase, milestone, and checklist item should become `work_item.kind` or
`work_item.subtype`, not separate unrelated state systems.

### 2. Parent-Child Is Useful But Should Stay Shallow

Asana explicitly treats subtasks as tasks with one task parent, but warns
against deep sub-subtasks. ClickUp and Monday support deeper hierarchy, but
deep hierarchy often creates ambiguity and reporting friction.

AICOS should allow:

- one parent per hierarchical child;
- shallow nesting by default;
- checklist items as lightweight children;
- links for non-hierarchical relationships.

### 3. Links Are Not Parents

Tools separate hierarchy from links:

- ClickUp has parent/subtask and separate relationships/dependencies.
- Plane supports sub-work items plus relations/blockers/duplicates.
- Airtable and Notion use relation fields for arbitrary links.

AICOS should distinguish:

- `parent_of` / `child_of`
- `blocks` / `blocked_by`
- `relates_to`
- `duplicates` / `duplicated_by`
- `derived_from`
- `supersedes` / `superseded_by`

### 4. Checklist Items Are Usually Lightweight

Trello check items are embedded under checklists/cards. ClickUp has both
subtasks and checklist items. This distinction is useful.

AICOS should treat checklist items as work items only when needed for state
reconciliation, but with a lightweight default:

- checklist item has stable ID, title, status, source ref;
- it may not need owner, full metadata, or handoff unless promoted.

### 5. Views Are Projections, Not Truth

Trello lists, Asana sections, Airtable views, Notion database views, and Monday
boards/views show that visual grouping is not the same as semantic truth.

AICOS should keep:

- status/task/checklist truth in Work State Ledger records;
- dashboard/PM/board views as derived projections.

### 6. Multi-Home Should Be Rare And Explicit

Asana supports tasks in multiple projects. Airtable/Notion support many-to-many
links. These are powerful but dangerous for AICOS authority.

AICOS should not multi-home truth by default. If one item appears in many
views, it should be the same `work_item_id` rendered in multiple derived views.

## AICOS Fit Analysis

### Best Fit To Reuse

- Plane: work item, sub-work item, relation type, module/cycle as optional
  grouping, AI/coworker-friendly direction.
- Asana: Work Graph idea, multi-project projection caution, shallow subtask
  warning.
- ClickUp: distinction between task/subtask/checklist and explicit
  dependency/relationship.
- Airtable/Notion: linked-record/page relation discipline and flexible
  structured fields for non-code projects.
- Trello: lightweight checklist item semantics.

### Poor Fit To Copy Directly

- Full PM hierarchy with many containers.
- Sprint/cycle default for all work.
- Board/list position as truth.
- Deep subtask/sub-subtask hierarchy as normal.
- Bidirectional PM sync before AICOS has stable work-state identity.
- Arbitrary database schema as AICOS semantic core.

## Recommended AICOS Direction

AICOS should define a small Work State Ledger with:

- one core `work_item`;
- `kind` for task/open question/tech debt/decision follow-up/checklist item;
- shallow parent-child hierarchy;
- explicit typed links for blockers/related/duplicates/derived;
- source refs and state refs as first-class fields;
- derived views for checklists, open items, dashboard, and PM tools;
- no PM UI, no board truth, no sprint assumption.

This gives AICOS enough structure to prevent checklist/status drift while
keeping Plane/ClickUp/Asana/etc. as future display or sync surfaces rather than
semantic authority.

## Next Step

Write the minimal AICOS Work State Ledger schema proposal:

- object types;
- lifecycle states;
- parent-child rules;
- link types;
- source/state/derived refs;
- reconciliation rules;
- anti-PM boundaries.
