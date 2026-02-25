# Skill Delegation Audit & Enhancement v2 — AUTO-DELEGATE

## TL;DR

> **Quick Summary**: Add AUTO-DELEGATE logic to 9 skills so they automatically spawn background tasks to specialist skills after completing their primary work. Each skill stays focused on its core purpose.
> 
> **Deliverables**:
> - 9 skills updated with AUTO-DELEGATE logic (inline sections + updated YAML descriptions)
> - Updated README.md with new Delegates column in all skill tables
> - All skills validated with `skill-validator` and ≤ 100 lines
> 
> **Estimated Effort**: Medium (4-6 hours)
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 → Tasks 2-10 (parallel) → Tasks 11-12

---

## Context

### Original Request
Update the existing skill-delegation-audit plan. Change ALL delegation from PROACTIVE-ASK (ask user first) to AUTO-DELEGATE (automatically spawn background tasks). Each skill should focus on its core purpose and use other skills to do secondary work — like `unity-review-code-local` already does.

### Interview Summary
**Key Discussions**:
- All AUTO-DELEGATE mode — no asking, no PROACTIVE-ASK anywhere
- Only `unity-review-code-local` (already has delegation) changes code locally
- PR review skills (review-general, review-architecture, review-asset) are EXCLUDED — they only provide suggestions in GitHub comments, wrong-branch risk for local fixes
- Investigation/document skills auto-delegate to GENERATE secondary outputs (tests, code, implementations), not to apply fixes
- Multi-target delegation allowed (a skill can delegate to multiple specialists)

**Research Findings**:
- 34 total skills audited; 3 already have cross-skill delegation, 1 has self-delegation
- 9 skills identified as delegation targets (sufficient headroom, clear delegation opportunities)
- Canonical pattern from `unity-review-code-local`: `task(category="quick", load_skills=["target"], run_in_background=true)`
- Delegation takes 3-5 lines per skill

### Metis Review
**Identified Gaps** (addressed):
- PR review skills (review-general, review-architecture, review-asset) excluded: wrong-branch risk still applies
- Added "skip delegation if no actionable findings" to every delegation section
- Added QA check for no PROACTIVE-ASK remnants in modified skills
- Added maximum 5 parallel delegations per invocation guardrail
- YAML descriptions: append only, never rewrite
- Delegation is one-directional: target skills MUST NOT delegate back to source

---

## Work Objectives

### Core Objective
Add AUTO-DELEGATE logic to 9 skills so they automatically spawn background tasks to specialist skills after completing their primary output.

### Concrete Deliverables
- 9 modified SKILL.md files with `## Delegation` sections using AUTO-DELEGATE pattern
- Updated YAML `description` fields (append delegation clause)
- Updated README.md with Delegates column in all skill tables
- All skills passing `skill-validator`

### Definition of Done
- [ ] All 9 target skills have AUTO-DELEGATE logic
- [ ] All modified SKILL.md files ≤ 100 lines
- [ ] All modified skills pass `skill-validator`
- [ ] All modified YAML descriptions mention delegation (append, not rewrite)
- [ ] README.md has Delegates column with correct targets
- [ ] No PROACTIVE-ASK remnants (no "ask user" / "Want me to" / "If yes" language)
- [ ] No regressions in existing 4 delegating skills

### Must Have
- AUTO-DELEGATE logic added to all 9 target skills
- Canonical `task()` syntax: `task(category="quick", load_skills=["target-skill"], prompt="...", run_in_background=true)`
- "Skip delegation if no actionable findings" clause in every delegation section
- README Delegates column

### Must NOT Have (Guardrails)
- DO NOT modify any skill's core workflow, tool selection, or output format
- DO NOT rename, move, or restructure any skill directory
- DO NOT modify scripts/ in any skill
- DO NOT change reference files other than adding `references/delegation.md` (only if SKILL.md would exceed 100L)
- DO NOT touch the 4 skills that already have working delegation (debug-quick, review-code-local, review-code-pr, review-prefab)
- DO NOT touch PR review skills (review-general, review-architecture, review-asset) — wrong-branch risk
- DO NOT touch self-contained/specialist skills (code-quick, code-deep, code-editor, test-unit, bash-optimize, etc.)
- DO NOT exceed 100 lines on any SKILL.md
- DO NOT rewrite YAML descriptions — APPEND delegation clause only
- DO NOT add PROACTIVE-ASK language ("ask user", "Want me to", "If yes")
- DO NOT allow circular delegation (target skills must not delegate back)
- DO NOT spawn more than 5 parallel background delegations per invocation

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (skill-validator, wc, grep tools)
- **Automated tests**: None (markdown instruction files, not executable code)
- **Framework**: skill-validator + bash checks

### QA Policy
Every task includes agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Skill files**: Use Bash — run skill-validator, check line count, grep for delegation keywords
- **README**: Use Bash — grep for Delegates column, check table formatting

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation — define delegation pattern):
└── Task 1: Define canonical AUTO-DELEGATE template

Wave 2 (After Wave 1 — ALL 9 skills in MAX PARALLEL):
├── Task 2: unity-debug-deep (74L, 26 headroom) → code-quick
├── Task 3: unity-debug-log (47L, 53 headroom) → code-quick
├── Task 4: unity-investigate-quick (37L, 63 headroom) → code-quick
├── Task 5: unity-investigate-deep (40L, 60 headroom) → code-quick
├── Task 6: unity-review-quality (78L, 22 headroom) → code-quick
├── Task 7: unity-test-case (68L, 32 headroom) → test-unit
├── Task 8: unity-document-system (39L, 61 headroom) → code-quick + test-unit
├── Task 9: unity-document-tdd (54L, 46 headroom) → code-quick
└── Task 10: bash-check (64L, 36 headroom) → bash-optimize

Wave 3 (After ALL skills — README + validation):
├── Task 11: Update README.md with Delegates column
└── Task 12: Final validation sweep

Critical Path: Task 1 → Tasks 2-10 → Tasks 11-12
Parallel Speedup: ~70% faster than sequential
Max Concurrent: 9 (Wave 2)
```

### Dependency Matrix

| Task | Blocked By | Blocks |
|------|-----------|--------|
| 1 | — | 2-10 |
| 2-10 | 1 | 11 |
| 11 | 2-10 | 12 |
| 12 | 11 | — |

### Agent Dispatch Summary

- **Wave 1**: 1 task — T1 → `quick` + `skill-creator`
- **Wave 2**: 9 tasks — T2-T10 → `quick` + `skill-creator`
- **Wave 3**: 2 tasks — T11 → `quick`, T12 → `unspecified-high`

---

## TODOs

- [ ] 1. Define Canonical AUTO-DELEGATE Template

  **What to do**:
  - Define the single AUTO-DELEGATE pattern that all subsequent tasks will copy. No PROACTIVE-ASK pattern.
  - **AUTO-DELEGATE pattern** (all skills in this plan):
    ```markdown
    ## Delegation
    After completing [primary output], auto-delegate actionable items:
    - For each [actionable finding/recommendation/deliverable]:
      `task(category="quick", load_skills=["target-skill"], prompt="[file path + context + exact work description]", run_in_background=true)`
    - Skip delegation if no actionable findings.
    - Max 5 parallel delegations. If more, batch into groups.
    ```
  - This is a DOCUMENTATION task — no files created, just establishing the pattern for implementers

  **Must NOT do**:
  - Create shared reference files across skills (each skill is self-contained)
  - Create any PROACTIVE-ASK pattern — AUTO-DELEGATE only
  - Modify any existing skill

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (alone)
  - **Blocks**: Tasks 2-10
  - **Blocked By**: None

  **References**:
  - `skills/unity-review-code-local/SKILL.md:53-57` — Canonical AUTO-DELEGATE reference (one task per finding, run_in_background=true)

  **Acceptance Criteria**:
  - [ ] AUTO-DELEGATE pattern documented with exact `task()` syntax
  - [ ] Pattern includes `run_in_background=true`
  - [ ] Pattern includes "skip if no actionable findings"
  - [ ] Pattern includes "max 5 parallel delegations"
  - [ ] No PROACTIVE-ASK language present

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify AUTO-DELEGATE pattern is complete
    Tool: Bash (grep)
    Steps:
      1. Verify pattern contains "task(category" and "run_in_background"
      2. Verify pattern contains "skip delegation" clause
      3. Verify NO "ask user" or "Want me to" or "If yes" language exists
    Expected Result: AUTO-DELEGATE pattern complete, zero PROACTIVE-ASK remnants
    Evidence: .sisyphus/evidence/task-1-patterns-verified.txt
  ```

  **Commit**: NO (documentation task — patterns are used by subsequent tasks)

---

- [ ] 2. Add AUTO-DELEGATE to unity-debug-deep

  **What to do**:
  - Read `skills/unity-debug-deep/SKILL.md` (currently 74 lines, 26 headroom)
  - Add `## Delegation` section after the Rules section with AUTO-DELEGATE pattern
  - Delegation target: `unity-code-quick` — after producing the analysis document with proposed solutions, auto-delegate implementing each proposed solution as a background task
  - Include in delegation prompt: file path, solution description, expected outcome from the analysis document
  - Add "Skip delegation if no actionable solutions proposed"
  - Update YAML `description`: append "Auto-delegates proposed solution implementations to unity-code-quick."
  - Run `skill-validator`, verify ≤ 100 lines

  **Must NOT do**:
  - Change the existing workflow steps
  - Remove the "Never modifies code" constraint (the SKILL itself doesn't modify code — it delegates to code-quick which does)
  - Change the output format or template reference
  - Add any "ask user" / "Want me to" language

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3-10)
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-debug-deep/SKILL.md` — Current skill to modify (74 lines)
  - `skills/unity-review-code-local/SKILL.md:53-57` — Canonical AUTO-DELEGATE pattern to follow
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] SKILL.md has `## Delegation` section with AUTO-DELEGATE pattern
  - [ ] Contains `task(category="quick", load_skills=["unity-code-quick"]` and `run_in_background=true`
  - [ ] Contains "Skip delegation if no actionable" clause
  - [ ] YAML description appended with delegation mention
  - [ ] No "ask user" / "Want me to" / "If yes" language anywhere
  - [ ] `skill-validator skills/unity-debug-deep` passes
  - [ ] `wc -l skills/unity-debug-deep/SKILL.md` ≤ 100

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify AUTO-DELEGATE section present and valid
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-debug-deep/SKILL.md → assert 1
      2. grep -c "unity-code-quick" skills/unity-debug-deep/SKILL.md → assert ≥ 1
      3. grep -c "run_in_background" skills/unity-debug-deep/SKILL.md → assert ≥ 1
      4. grep -ci "ask user\|want me to\|if yes\|if user" skills/unity-debug-deep/SKILL.md → assert 0
      5. wc -l skills/unity-debug-deep/SKILL.md → assert ≤ 100
    Expected Result: All assertions pass
    Evidence: .sisyphus/evidence/task-2-debug-deep-verified.txt

  Scenario: Verify skill-validator passes
    Tool: Bash
    Steps:
      1. Run skill-validator on skills/unity-debug-deep
      2. Assert no FAIL results
    Expected Result: Validator passes
    Evidence: .sisyphus/evidence/task-2-debug-deep-validator.txt
  ```

  **Commit**: YES (group with Tasks 3-5)
  - Message: `feat(skills): add auto-delegation to debug & investigate skills`
  - Files: `skills/unity-debug-deep/SKILL.md`

---

- [ ] 3. Add AUTO-DELEGATE to unity-debug-log

  **What to do**:
  - Read `skills/unity-debug-log/SKILL.md` (currently 47 lines, 53 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `unity-code-quick` — after generating log snippets, auto-delegate inserting them into the source files
  - Include in delegation prompt: each log snippet, target file path, insertion point (line number)
  - Add "Skip delegation if no log snippets generated"
  - Update YAML `description`: append "Auto-delegates log insertion to unity-code-quick."
  - The SKILL itself remains "READ-ONLY: never edit project files" — the delegation creates a SEPARATE task that does the editing

  **Must NOT do**:
  - Change the READ-ONLY constraint of the skill itself
  - Change the output format or workflow

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4-10)
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-debug-log/SKILL.md` — Current skill (47 lines)
  - `skills/unity-review-code-local/SKILL.md:53-57` — Canonical AUTO-DELEGATE pattern
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] SKILL.md has `## Delegation` section with AUTO-DELEGATE
  - [ ] Contains `task(` with `unity-code-quick` and `run_in_background=true`
  - [ ] No PROACTIVE-ASK language
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify AUTO-DELEGATE section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-debug-log/SKILL.md → assert 1
      2. grep -c "run_in_background" skills/unity-debug-log/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/unity-debug-log/SKILL.md → assert 0
      4. wc -l skills/unity-debug-log/SKILL.md → assert ≤ 100
    Expected Result: All assertions pass
    Evidence: .sisyphus/evidence/task-3-debug-log-verified.txt
  ```

  **Commit**: YES (group with Tasks 2, 4, 5)
  - Message: `feat(skills): add auto-delegation to debug & investigate skills`
  - Files: `skills/unity-debug-log/SKILL.md`

---

- [ ] 4. Add AUTO-DELEGATE to unity-investigate-quick

  **What to do**:
  - Read `skills/unity-investigate-quick/SKILL.md` (currently 37 lines, 63 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `unity-code-quick` — if investigation reveals a fixable issue, auto-delegate implementing the fix
  - Keep it minimal (3-5 lines) to match the skill's "speed over ceremony" identity
  - Update YAML `description`: append "Auto-delegates fixes to unity-code-quick when issues found."

  **Must NOT do**:
  - Change the "Answer the question. Nothing else." core identity
  - Change the output format
  - Add verbose delegation instructions — keep minimal

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-investigate-quick/SKILL.md` — Current skill (37 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present, AUTO-DELEGATE pattern, no PROACTIVE-ASK
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify AUTO-DELEGATE section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-investigate-quick/SKILL.md → assert 1
      2. grep -c "unity-code-quick" skills/unity-investigate-quick/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/unity-investigate-quick/SKILL.md → assert 0
      4. wc -l skills/unity-investigate-quick/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-4-investigate-quick-verified.txt
  ```

  **Commit**: YES (group with Tasks 2, 3, 5)
  - Message: `feat(skills): add auto-delegation to debug & investigate skills`

---

- [ ] 5. Add AUTO-DELEGATE to unity-investigate-deep

  **What to do**:
  - Read `skills/unity-investigate-deep/SKILL.md` (currently 40 lines, 60 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `unity-code-quick` — after producing investigation report with recommendations, auto-delegate implementing recommended improvements
  - Update YAML `description`: append "Auto-delegates recommended improvements to unity-code-quick."

  **Must NOT do**:
  - Change the investigation workflow or tool selection
  - Change the output location (Documents/Investigations/)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-investigate-deep/SKILL.md` — Current skill (40 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present, AUTO-DELEGATE pattern, no PROACTIVE-ASK
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify AUTO-DELEGATE section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-investigate-deep/SKILL.md → assert 1
      2. grep -c "unity-code-quick" skills/unity-investigate-deep/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/unity-investigate-deep/SKILL.md → assert 0
      4. wc -l skills/unity-investigate-deep/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-5-investigate-deep-verified.txt
  ```

  **Commit**: YES (group with Tasks 2, 3, 4)
  - Message: `feat(skills): add auto-delegation to debug & investigate skills`

---

- [ ] 6. Add AUTO-DELEGATE to unity-review-quality

  **What to do**:
  - Read `skills/unity-review-quality/SKILL.md` (currently 78 lines, 22 headroom)
  - Add `## Delegation` section — BRIEF (5-8 lines max due to limited headroom)
  - Delegation target: `unity-code-quick` — after producing the quality report, auto-delegate fixing Critical/High findings
  - If ≤ 100 lines cannot be achieved inline, create `references/delegation.md` with detailed instructions and add a `read_skill_file` call in SKILL.md
  - Update YAML `description`: append "Auto-delegates Critical/High fixes to unity-code-quick."

  **Must NOT do**:
  - Change the READ-ONLY constraint
  - Change the grading criteria or review workflow

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-review-quality/SKILL.md` — Current skill (78 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] Delegation logic present (inline or in references/delegation.md)
  - [ ] Contains `run_in_background=true`, no PROACTIVE-ASK language
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify delegation and line count
    Tool: Bash
    Steps:
      1. grep -rc "delegat" skills/unity-review-quality/ → assert ≥ 1
      2. grep -c "run_in_background" skills/unity-review-quality/SKILL.md → assert ≥ 1 (or check references/)
      3. grep -ci "ask user\|want me to" skills/unity-review-quality/SKILL.md → assert 0
      4. wc -l skills/unity-review-quality/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-6-review-quality-verified.txt
  ```

  **Commit**: YES (group with Tasks 7-10)
  - Message: `feat(skills): add auto-delegation to review, test, document & bash skills`

---

- [ ] 7. Add AUTO-DELEGATE to unity-test-case

  **What to do**:
  - Read `skills/unity-test-case/SKILL.md` (currently 68 lines, 32 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `unity-test-unit` — after generating QA test case document, auto-delegate generating actual C# unit test scripts based on the test cases
  - Update YAML `description`: append "Auto-delegates C# test generation to unity-test-unit."

  **Must NOT do**:
  - Change the QA methodology or HTML output format

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-test-case/SKILL.md` — Current skill (68 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present with `unity-test-unit` as target
  - [ ] No PROACTIVE-ASK language
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify delegation section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-test-case/SKILL.md → assert 1
      2. grep -c "unity-test-unit" skills/unity-test-case/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/unity-test-case/SKILL.md → assert 0
      4. wc -l skills/unity-test-case/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-7-test-case-verified.txt
  ```

  **Commit**: YES (group with Tasks 6, 8-10)
  - Message: `feat(skills): add auto-delegation to review, test, document & bash skills`

---

- [ ] 8. Add AUTO-DELEGATE to unity-document-system (MULTI-TARGET)

  **What to do**:
  - Read `skills/unity-document-system/SKILL.md` (currently 39 lines, 61 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern — MULTI-TARGET
  - Delegation targets:
    - `unity-code-quick` — auto-delegate implementing extension points described in the guide
    - `unity-test-unit` — auto-delegate generating tests for the documented system
  - Update YAML `description`: append "Auto-delegates implementation to unity-code-quick and tests to unity-test-unit."

  **Must NOT do**:
  - Change the READ-ONLY investigation workflow
  - Change the template or output location

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-document-system/SKILL.md` — Current skill (39 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present with BOTH `unity-code-quick` AND `unity-test-unit` as targets
  - [ ] No PROACTIVE-ASK language
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify multi-target delegation
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-document-system/SKILL.md → assert 1
      2. grep -c "unity-code-quick" skills/unity-document-system/SKILL.md → assert ≥ 1
      3. grep -c "unity-test-unit" skills/unity-document-system/SKILL.md → assert ≥ 1
      4. grep -ci "ask user\|want me to" skills/unity-document-system/SKILL.md → assert 0
      5. wc -l skills/unity-document-system/SKILL.md → assert ≤ 100
    Expected Result: All pass, both targets present
    Evidence: .sisyphus/evidence/task-8-document-system-verified.txt
  ```

  **Commit**: YES (group with Tasks 6, 7, 9, 10)
  - Message: `feat(skills): add auto-delegation to review, test, document & bash skills`

---

- [ ] 9. Add AUTO-DELEGATE to unity-document-tdd

  **What to do**:
  - Read `skills/unity-document-tdd/SKILL.md` (currently 54 lines, 46 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `unity-code-quick` — after producing the TDD, auto-delegate generating skeleton code from the implementation strategy
  - Update YAML `description`: append "Auto-delegates skeleton code generation to unity-code-quick."

  **Must NOT do**:
  - Change the investigation workflow or quality bar

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/unity-document-tdd/SKILL.md` — Current skill (54 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present, AUTO-DELEGATE, no PROACTIVE-ASK
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify delegation section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/unity-document-tdd/SKILL.md → assert 1
      2. grep -c "unity-code-quick" skills/unity-document-tdd/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/unity-document-tdd/SKILL.md → assert 0
      4. wc -l skills/unity-document-tdd/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-9-document-tdd-verified.txt
  ```

  **Commit**: YES (group with Tasks 6, 7, 8, 10)
  - Message: `feat(skills): add auto-delegation to review, test, document & bash skills`

---

- [ ] 10. Add AUTO-DELEGATE to bash-check

  **What to do**:
  - Read `skills/bash-check/SKILL.md` (currently 64 lines, 36 headroom)
  - Add `## Delegation` section with AUTO-DELEGATE pattern
  - Delegation target: `bash-optimize` — after validation report, auto-delegate fixing found issues
  - Update YAML `description`: append "Auto-delegates fixes to bash-optimize."

  **Must NOT do**:
  - Change the validation workflow (syntax check, ShellCheck, manual review)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 11
  - **Blocked By**: Task 1

  **References**:
  - `skills/bash-check/SKILL.md` — Current skill (64 lines)
  - Task 1 output — AUTO-DELEGATE template

  **Acceptance Criteria**:
  - [ ] `## Delegation` section present with `bash-optimize` as target
  - [ ] No PROACTIVE-ASK language
  - [ ] `skill-validator` passes, ≤ 100 lines

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify delegation section
    Tool: Bash
    Steps:
      1. grep -c "## Delegation" skills/bash-check/SKILL.md → assert 1
      2. grep -c "bash-optimize" skills/bash-check/SKILL.md → assert ≥ 1
      3. grep -ci "ask user\|want me to" skills/bash-check/SKILL.md → assert 0
      4. wc -l skills/bash-check/SKILL.md → assert ≤ 100
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-10-bash-check-verified.txt
  ```

  **Commit**: YES (group with Tasks 6, 7, 8, 9)
  - Message: `feat(skills): add auto-delegation to review, test, document & bash skills`

---

- [ ] 11. Update README.md with Delegates Column

  **What to do**:
  - Read `README.md`
  - Add a 7th "Delegates" column to ALL skill tables
  - For skills WITH delegation, show target: e.g., `→ unity-code-quick`
  - For skills WITHOUT delegation, show `—`
  - Include existing delegations (review-code-local, debug-quick, review-code-pr, review-prefab) AND new ones from Tasks 2-10

  **Must NOT do**:
  - Change any other content in README.md
  - Change skill descriptions or table structure beyond adding the column

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 2-10

  **References**:
  - `README.md` — Current file

  **Delegation mapping for README**:
  | Skill | Delegates Column Value |
  |-------|----------------------|
  | unity-debug-quick | → `unity-code-quick` (existing) |
  | unity-debug-deep | → `unity-code-quick` (new) |
  | unity-debug-log | → `unity-code-quick` (new) |
  | unity-debug-fix | — |
  | unity-investigate-quick | → `unity-code-quick` (new) |
  | unity-investigate-deep | → `unity-code-quick` (new) |
  | unity-review-code-local | → `unity-code-quick` (existing) |
  | unity-review-code-pr | → `unity-code-quick` (existing) |
  | unity-review-prefab | → subagent tasks (existing) |
  | unity-review-quality | → `unity-code-quick` (new) |
  | unity-test-case | → `unity-test-unit` (new) |
  | unity-document-system | → `unity-code-quick` + `unity-test-unit` (new) |
  | unity-document-tdd | → `unity-code-quick` (new) |
  | bash-check | → `bash-optimize` (new) |
  | All others | — |

  **Acceptance Criteria**:
  - [ ] All skill tables have 7 columns (added Delegates)
  - [ ] Delegation targets accurate per mapping above
  - [ ] README renders correctly in markdown

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Verify Delegates column exists
    Tool: Bash
    Steps:
      1. grep -c "Delegates" README.md → assert ≥ 10
      2. grep "unity-code-quick" README.md → verify delegation targets
      3. grep "bash-optimize" README.md → verify bash-check delegation
      4. grep "unity-test-unit" README.md → verify test-case delegation
    Expected Result: All delegation targets correctly shown
    Evidence: .sisyphus/evidence/task-11-readme-verified.txt
  ```

  **Commit**: YES
  - Message: `docs: add Delegates column to README skill tables`
  - Files: `README.md`

---

- [ ] 12. Final Validation Sweep

  **What to do**:
  - Run `skill-validator` on ALL 9 modified skills
  - Verify ALL modified SKILL.md files ≤ 100 lines
  - Verify ALL modified YAML descriptions mention delegation (appended, not rewritten)
  - Verify NO PROACTIVE-ASK remnants across all modified skills: `grep -rci "ask user\|want me to\|if yes\|if user requests" skills/{target}/SKILL.md` → assert 0
  - Verify the 4 pre-existing delegating skills were NOT modified
  - Check README.md table rendering
  - Report pass/fail summary

  **Must NOT do**:
  - Modify any files (READ-ONLY verification task)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after Task 11)
  - **Blocks**: None (final task)
  - **Blocked By**: Task 11

  **Acceptance Criteria**:
  - [ ] All 9 skills pass `skill-validator`
  - [ ] All 9 SKILL.md files ≤ 100 lines
  - [ ] All 9 YAML descriptions mention delegation
  - [ ] Zero PROACTIVE-ASK remnants across all modified skills
  - [ ] All `task()` calls contain `run_in_background=true`
  - [ ] Pre-existing 4 delegation skills unchanged
  - [ ] README table renders correctly

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Full validation sweep
    Tool: Bash
    Steps:
      1. for skill in unity-debug-deep unity-debug-log unity-investigate-quick unity-investigate-deep unity-review-quality unity-test-case unity-document-system unity-document-tdd bash-check; do echo "=== $skill ==="; wc -l skills/$skill/SKILL.md; grep -c "## Delegation" skills/$skill/SKILL.md; grep -ci "ask user\|want me to" skills/$skill/SKILL.md; done
      2. Verify each skill shows ≤ 100 lines, 1 delegation section, 0 PROACTIVE-ASK matches
      3. git diff --name-only → verify only expected files changed
    Expected Result: All 9 skills valid, zero PROACTIVE-ASK, no unexpected changes
    Evidence: .sisyphus/evidence/task-12-final-sweep.txt

  Scenario: Verify no regressions in existing delegation skills
    Tool: Bash
    Steps:
      1. git diff HEAD -- skills/unity-review-code-local/SKILL.md skills/unity-debug-quick/SKILL.md skills/unity-review-code-pr/SKILL.md skills/unity-review-prefab/SKILL.md → assert empty
    Expected Result: No changes to existing delegation skills
    Evidence: .sisyphus/evidence/task-12-no-regressions.txt
  ```

  **Commit**: NO (read-only verification)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify delegation exists in skill (read file, grep). For each "Must NOT Have": search for forbidden patterns (PROACTIVE-ASK language, workflow changes). Check evidence files exist.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `skill-validator` on all 9 modified skills. Review all changed SKILL.md files for: consistent AUTO-DELEGATE syntax, correct `task()` parameters, proper `run_in_background=true`. Check for AI slop: excessive delegation instructions, PROACTIVE-ASK remnants.
  Output: `Validator [PASS/FAIL] | Skills [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Verify each modified skill's SKILL.md reads naturally — delegation section flows with existing content. Verify README Delegates column aligns with actual skill delegation targets. Cross-check all 9 skills.
  Output: `Skills [N/N coherent] | README [PASS/FAIL] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Verify no PR review skills were touched. Verify no PROACTIVE-ASK language anywhere.
  Output: `Tasks [N/N compliant] | PROACTIVE-ASK [CLEAN/N occurrences] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

| Group | Tasks | Message | Files |
|-------|-------|---------|-------|
| 1 | 2-5 | `feat(skills): add auto-delegation to debug & investigate skills` | 4 SKILL.md files |
| 2 | 6-10 | `feat(skills): add auto-delegation to review, test, document & bash skills` | 5 SKILL.md files + possible references/ |
| 3 | 11 | `docs: add Delegates column to README skill tables` | README.md |

---

## Success Criteria

### Verification Commands
```bash
# All modified skills ≤ 100 lines
for s in unity-debug-deep unity-debug-log unity-investigate-quick unity-investigate-deep unity-review-quality unity-test-case unity-document-system unity-document-tdd bash-check; do wc -l skills/$s/SKILL.md; done
# Expected: all ≤ 100

# All have AUTO-DELEGATE
for s in unity-debug-deep unity-debug-log unity-investigate-quick unity-investigate-deep unity-review-quality unity-test-case unity-document-system unity-document-tdd bash-check; do echo "$s: $(grep -c '## Delegation' skills/$s/SKILL.md)"; done
# Expected: all show 1

# All have run_in_background=true
for s in unity-debug-deep unity-debug-log unity-investigate-quick unity-investigate-deep unity-review-quality unity-test-case unity-document-system unity-document-tdd bash-check; do echo "$s: $(grep -c 'run_in_background' skills/$s/SKILL.md)"; done
# Expected: all show ≥ 1

# Zero PROACTIVE-ASK remnants
for s in unity-debug-deep unity-debug-log unity-investigate-quick unity-investigate-deep unity-review-quality unity-test-case unity-document-system unity-document-tdd bash-check; do echo "$s: $(grep -ci 'ask user\|want me to\|if yes\|if user' skills/$s/SKILL.md)"; done
# Expected: all show 0

# README has Delegates column
grep -c "Delegates" README.md
# Expected: ≥ 10

# No changes to pre-existing delegation skills
git diff HEAD -- skills/unity-review-code-local/ skills/unity-debug-quick/ skills/unity-review-code-pr/ skills/unity-review-prefab/
# Expected: empty
```

### Final Checklist
- [ ] All 9 skills have AUTO-DELEGATE logic
- [ ] All SKILL.md files ≤ 100 lines
- [ ] All YAML descriptions updated (appended)
- [ ] Zero PROACTIVE-ASK language in any modified skill
- [ ] All `task()` calls include `run_in_background=true`
- [ ] README has Delegates column with accurate targets
- [ ] Pre-existing delegating skills untouched
- [ ] PR review skills untouched
- [ ] Self-contained skills untouched
- [ ] All skills pass skill-validator
