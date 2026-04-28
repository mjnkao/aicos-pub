# PRM-26151 — Codex Prompt To Place AICOS Policy Files Into The Repo

You are working on the `aicos` repository as **A2-Core-C**.

Your task is to take the recent policy/rule artifacts and integrate them into the repo in the **smallest correct form**, rather than leaving them as external standalone docs only.

## Source files to ingest

Use the following source materials:

1. `RUL-26088_AICOS_Temporary_Role_Rules_For_Codex.md`
2. `A2S-26102_AICOS_A2_Taxonomy_A2_Rules_and_AICOS_Self_Brain_Working_Spec.md`
3. `FLW-26124_Codex_A2_Core_Guide_For_Human_Chat_Decision_Flow_Option_Choose_And_Sync_Brain.md`
4. `POL-26140_AICOS_Policy_For_Capturing_New_Ideas_Open_Questions_TODOs_TechDebt_And_Candidate_Branch_Ideas.md`
5. `POL-26145_AICOS_State_Writeback_And_Sync_Policy.md`
6. `POL-26150_AICOS_Policy_Pack_Consolidated_Guide.md`

## Primary goal

Normalize the useful content of these files into the correct lanes inside the repo, while keeping the self-brain concise.

Do **not** simply dump all source files verbatim into canonical or working.

## Language rule

For new or updated files under:

- `brain/projects/aicos/canonical/`
- `brain/projects/aicos/working/`

use **Vietnamese with proper diacritics**.

If there is a real technical reason you cannot safely use Vietnamese with diacritics in a specific place, use **English**.  
Do **not** use Vietnamese without diacritics.

Technical terms may remain mixed Vietnamese + English where appropriate.

## What to update in the repo

### 1. Canonical files

Review and update these files with normalized concise content:

- `brain/projects/aicos/canonical/role-definitions.md`
- `brain/projects/aicos/canonical/project-working-rules.md`

These two files should absorb the most important stable points from:
- role clarity
- A2 taxonomy
- writeback policy
- option choose / sync brain flow boundaries

### 2. Working files

Review and update these files if needed:

- `brain/projects/aicos/working/current-direction.md`
- `brain/projects/aicos/working/open-questions.md`
- `brain/projects/aicos/working/active-risks.md`
- `brain/projects/aicos/working/architecture-working-summary.md`

These should reflect:
- current A2-Core focus
- A2-Serve not yet fully active
- writeback by state transition, not every message
- unresolved questions around `option choose` / `sync brain`
- any meaningful risks introduced by these policies

### 3. Evidence / policy reference lanes

If suitable lanes do not exist yet, create minimal ones without overbuilding:

- `brain/projects/aicos/evidence/candidate-decisions/README.md`
- optionally a small policy source reference file or index in evidence if needed

Use these for:
- candidate branch ideas
- candidate decisions not yet committed
- provenance/reference to longer policy sources if helpful

### 4. A2 operational lanes

Review and update the relevant A2 rule lanes so A2-Core behavior is clear:

- `agent-repo/classes/a2-service-agents/rules/`
- `agent-repo/classes/a2-service-agents/tasks/backlog/`

Ensure the repo reflects:
- A2-Core vs future A2-Serve distinction
- idea capture rules
- writeback and sync behavior
- backlog vs risk vs open-question routing

## Important constraints

### Do not

- do not copy all source files verbatim into canonical
- do not turn `current-state.md` into a general inbox
- do not overbuild new folder trees unless clearly needed
- do not create official branch realities for unapproved branch ideas
- do not add UI or public API in this task
- do not hardcode unstable policy logic into code just because you are touching docs
- do not use Vietnamese without diacritics in self-brain files

### Do

- preserve concise self-brain summaries
- keep source material available by reference if needed
- map each policy to the smallest correct lane
- prefer normalization over duplication
- keep repo startup context easier, not harder

## Deliverables

1. Updated repo files in the correct lanes
2. A short implementation note summarizing:
   - which files were updated
   - what was normalized from each source file
   - what was intentionally left only as source/reference
   - any unresolved questions or conflicts

## Acceptance criteria

This task is done only if:

- role clarity is concise and visible in canonical lane
- A2 taxonomy is visible but not overexplained in startup-critical files
- writeback policy is reflected in project-working-rules or equivalent stable lane
- new-idea capture policy is reflected in the appropriate working/evidence/A2 backlog lanes
- self-brain remains concise and readable
- startup reading order becomes easier, not more complex

Proceed incrementally and keep the repo coherent.
