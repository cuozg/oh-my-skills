# Skill Refactor + Shared Reorg (Combined)

## TL;DR

> **Quick Summary**: Create shared skill infrastructure for all 9 groups (following unity-plan-shared pattern), deduplicate scripts across skills, rename `unity-code-standards` → `unity-code-shared`, unify tracing scripts, then extract workflow/template/example content from all 29 consumer skills' SKILL.md into `references/workflow.md`. Every SKILL.md stays <100 lines.
> 
> **Deliverables**:
> - 8 new `{group}-shared/` skill directories with SKILL.md indexes
> - 5 duplicate `post_review.py` → 1 canonical copy in `unity-review-shared/`
> - 2 duplicate `trace_logic.py` → 1 canonical copy in `unity-investigate-shared/`
> - `unity-code-standards/` renamed to `unity-code-shared/` with all consumer references updated
> - Unified tracing module (`trace_unified.py`) replacing 3 separate scripts
> - 29 refactored consumer skills with `references/workflow.md` extracted
> - All SKILL.md ↔ reference content duplication eliminated
> - All skills pass `skill-validator` and `skill-deps`
> 
> **Estimated Effort**: XL (29 consumer skills + 8 new shared skills + script dedup + tracing unification)
> **Parallel Execution**: YES — 8 waves + final verification
> **Critical Path**: W1 (shared scaffolds) → W2 (rename + consumer refs) → W3-5 (workflow extraction) → W6 (tracing + audit) → W7 (validation) → Final

---

## Context

### Original Request
Combine two existing plans (`skill-refactor.md` and `skill-shared-reorg.md`) into one conflict-free plan. The two plans had opposing guardrails — Plan 1 said "each skill stays self-contained" while Plan 2 created shared cross-skill modules. User chose to do BOTH: shared infrastructure AND workflow extraction.

### Interview Summary
**Key Discussions**:
- Direction: Both shared skills AND per-skill workflow.md extraction — no self-containment guardrail
- Execution order: Shared infra first → workflow extraction → validation
- Description fields: UPDATE unity-code-quick's description (rename reference)
- Tiny skills: ALWAYS create workflow.md even for 37L skills — consistency wins

**Research Findings**:
- 5 identical `post_review.py` (4352B each, MD5-verified) across review skills
- 2 identical `trace_logic.py` (7177B) + test across investigate skills
- 3 tracing scripts with DIFFERENT APIs (pure Python vs subprocess) — merge requires refactoring
- 10 files across 7 skills reference `unity-code-standards` — all need updating
- `run_skill_script` is NEVER used — all scripts invoked via hardcoded bash paths
- README.md also references `unity-code-standards`

### Metis Review
**Identified Gaps** (addressed):
- Script invocation pattern mismatch: Plan 2 assumed `run_skill_script` — actually hardcoded bash paths → Corrected in all tasks
- `unity-code-quick` description field contains `unity-code-standards` → Will be updated during rename
- README.md has dangling `unity-code-standards` reference → Added to rename task blast radius
- New shared skills need to be exempt from `workflow.md` requirement → Added as guardrail
- Wave ordering: workflow extraction must read CURRENT state, not original line counts → Enforced per task
- Use `git mv` for directory rename to preserve history → Added to rename task
- 12 skills have no `references/` directory (not 8 as originally stated) → Corrected count
- Empty scripts directories must be cleaned up after moves → Added acceptance criteria

---

## Work Objectives

### Core Objective
Create shared skill infrastructure for all 9 groups, eliminate script duplication, then extract workflow content from each consumer skill's SKILL.md into dedicated reference files. Every skill follows progressive disclosure standards.

### Concrete Deliverables
- 8 new `{group}-shared/` directories with valid SKILL.md indexes
- `unity-code-standards/` renamed to `unity-code-shared/`
- Zero duplicate scripts (same MD5) across different skills
- 29 consumer skills each with `references/workflow.md`
- Unified tracing module replacing 3 separate scripts
- All SKILL.md ↔ reference content duplication eliminated
- All skills pass `skill-validator`

### Definition of Done
- [ ] `ls -d skills/*-shared skills/git-shared skills/bash-shared | wc -l` → 9 (all shared skills exist)
- [ ] `find skills/ -name "post_review.py" | wc -l` → 1
- [ ] `find skills/ -name "trace_logic.py" | wc -l` → 1
- [ ] `test ! -d skills/unity-code-standards && echo "RENAMED"` → RENAMED
- [ ] `wc -l skills/*/SKILL.md | awk '$1 >= 100 {print}' | grep -v skill-creator | wc -l` → 0
- [ ] `grep -r 'unity-code-standards' skills/ README.md --include='*.md' | wc -l` → 0
- [ ] `git diff skills/skill-creator/ | wc -l` → 0
- [ ] `python3 -m pytest skills/unity-review-shared/scripts/tests/ skills/unity-investigate-shared/scripts/tests/ skills/unity-plan-shared/scripts/tests/` → all pass
- [ ] `skill-validator` passes for all 42 skills (34 original + 8 new shared)

### Must Have
- All 9 shared skill directories exist with valid SKILL.md (following unity-plan-shared pattern)
- Zero duplicate scripts (same MD5) across different skills
- All `read_skill_file("unity-code-standards", ...)` → `read_skill_file("unity-code-shared", ...)`
- All `use_skill("unity-code-standards")` → `use_skill("unity-code-shared")`
- All hardcoded bash paths to `post_review.py` point to `unity-review-shared/scripts/`
- Every consumer skill (29 total) has `references/workflow.md`
- Content is MOVED not rewritten — preserve exact wording (except updating changed paths)
- Unified tracing module with backward-compatible CLI interfaces

### Must NOT Have (Guardrails)
- ❌ Do NOT modify `skills/skill-creator/` in any way
- ❌ Do NOT modify `unity-plan-shared/quick/deep/detail` content (validate only)
- ❌ Do NOT rewrite or rephrase extracted content — MOVE verbatim (except path updates)
- ❌ Do NOT consolidate review-quality checklists with code-shared/review references (complementary, not duplicate)
- ❌ Do NOT treat `requirements.txt` deduplication as priority
- ❌ Do NOT add features to existing scripts during moves — move first, refactor separately
- ❌ Do NOT create `references/workflow.md` for `*-shared` skills (they're indexes, not workflows)
- ❌ Do NOT use `run_skill_script` references in task instructions (it's not used — all scripts use bash paths)
- ❌ Reference files must NOT exceed 100 lines
- ❌ SKILL.md files must NOT exceed 100 lines (except skill-creator which is excluded)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES — `skill-validator`, `skill-deps`, pytest
- **Automated tests**: YES (tests-after) — verify existing tests pass after moves, add tests for unified tracing
- **Framework**: pytest + `skill-validator` + bash assertions

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/`.

- **Script validation**: pytest — verify existing tests pass at new locations
- **Reference validation**: `skill-validator` + `skill-deps` for every modified skill
- **Path validation**: grep — verify all `../` paths resolve, no dangling references
- **Line count validation**: `wc -l` — verify <100L constraints

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — shared scaffolds + script dedup):
├── Task 1: Baseline validation sweep [quick]
├── Task 2: Create unity-review-shared + move post_review.py [quick]
├── Task 3: Create unity-investigate-shared + move trace_logic.py [quick]
├── Task 4: Create git-shared, bash-shared, unity-test-shared, unity-document-shared scaffolds [quick]
├── Task 5: Create unity-debug-shared + move common-fixes.md [quick]

Wave 2 (After Wave 1 — rename + consumer path updates):
├── Task 6: Rename unity-code-standards → unity-code-shared + update ALL refs [deep]
├── Task 7: Update 4 review-* SKILL.md for shared script paths [quick]
├── Task 8: Update 2 investigate-* SKILL.md for shared script paths [quick]
├── Task 9: Move code-deep's 3 shared refs to code-shared + update code-quick [quick]

Wave 3 (After Wave 2 — workflow extraction batch A: standalone skills):
├── Task 10: Extract workflow for bash-check, bash-install, bash-optimize [quick]
├── Task 11: Extract workflow for git-comment, git-commit [quick]
├── Task 12: Extract workflow for git-description, git-squash [quick]
├── Task 13: Extract workflow for flatbuffers-coder [quick]

Wave 4 (After Wave 2 — workflow extraction batch B: code + debug skills):
├── Task 14: Extract workflow for unity-code-deep, unity-code-editor [quick]
├── Task 15: Extract workflow for unity-code-quick [quick]
├── Task 16: Extract workflow for unity-debug-deep, unity-debug-log [quick]
├── Task 17: Extract workflow for unity-debug-quick [quick]

Wave 5 (After Wave 2 — workflow extraction batch C: investigate + review + doc + test):
├── Task 18: Extract workflow for unity-investigate-quick, unity-investigate-deep [quick]
├── Task 19: Extract workflow for unity-review-code-local, unity-review-code-pr [quick]
├── Task 20: Extract workflow for unity-review-architecture, unity-review-asset [quick]
├── Task 21: Extract workflow for unity-review-general, unity-review-prefab [quick]
├── Task 22: Extract workflow for unity-review-quality [quick]
├── Task 23: Extract workflow for unity-document-system, unity-document-tdd [quick]
├── Task 24: Extract workflow for unity-test-unit, unity-test-case [quick]
├── Task 25: Extract workflow for mermaid [quick]

Wave 6 (After Wave 5 — tracing unification + dedup audit):
├── Task 26: Create trace_unified.py in investigate-shared [deep]
├── Task 27: Update document-* skills to use unified tracing [quick]
├── Task 28: Audit all SKILL.md for SKILL.md ↔ reference duplication [unspecified-high]

Wave 7 (After all — validation):
├── Task 29: Full validation sweep — all 42 skills [deep]

Wave FINAL (After T29 — independent review, 4 parallel):
├── Task F1: Plan compliance audit [oracle]
├── Task F2: Code quality review [unspecified-high]
├── Task F3: Reference integrity QA [unspecified-high]
├── Task F4: Scope fidelity check [deep]

Critical Path: T1 → T2-5 → T6-9 → T10-25 → T26-28 → T29 → F1-F4
Parallel Speedup: ~75% faster than sequential
Max Concurrent: 8 (Waves 3, 4, 5 can run together after Wave 2)
```

### Dependency Matrix

| Task | Blocked By | Blocks |
|------|-----------|--------|
| 1 | — | 2-5 |
| 2 | 1 | 7, 29 |
| 3 | 1 | 8, 26, 27, 29 |
| 4 | 1 | 29 |
| 5 | 1 | 17, 29 |
| 6 | 1 | 9, 14, 15, 29 |
| 7 | 2 | 19-22, 29 |
| 8 | 3 | 18, 29 |
| 9 | 6 | 14, 15, 29 |
| 10-13 | 1 | 29 |
| 14 | 6, 9 | 29 |
| 15 | 6, 9 | 29 |
| 16 | 1 | 29 |
| 17 | 5 | 29 |
| 18 | 8 | 29 |
| 19-22 | 7 | 29 |
| 23 | 1 | 27, 29 |
| 24-25 | 1 | 29 |
| 26 | 3 | 27, 29 |
| 27 | 23, 26 | 29 |
| 28 | 1 | 29 |
| 29 | 1-28 | F1-F4 |
| F1-F4 | 29 | — |

### Agent Dispatch Summary

- **Wave 1**: 5 tasks — T1 `quick`, T2-T5 `quick`
- **Wave 2**: 4 tasks — T6 `deep`, T7-T9 `quick`
- **Waves 3-5**: 16 tasks — all `quick`
- **Wave 6**: 3 tasks — T26 `deep`, T27 `quick`, T28 `unspecified-high`
- **Wave 7**: 1 task — T29 `deep`
- **FINAL**: 4 tasks — F1 `oracle`, F2-F3 `unspecified-high`, F4 `deep`

---

## TODOs


### Wave 1 — Foundation: Shared Scaffolds + Script Deduplication

- [ ] 1. Baseline Validation Sweep

  **What to do**:
  - Run `skill-validator` for every skill in `skills/` (except skill-creator)
  - Run `wc -l skills/*/SKILL.md` to capture current line counts
  - Verify MD5 of all `post_review.py` and `trace_logic.py` copies match
  - Save baseline report to `.sisyphus/evidence/task-1-baseline.txt`

  **Must NOT do**: Do NOT modify any files
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 1 (first) | Blocks: 2-5 | Blocked By: None
  **References**: `skills/` all dirs; `skill-validator`; `skill-deps`

  **Acceptance Criteria**:
  - [ ] Baseline report saved with MD5 checksums verified identical

  **QA Scenarios**:
  ```
  Scenario: Baseline capture
    Tool: Bash
    Steps:
      1. wc -l skills/*/SKILL.md > .sisyphus/evidence/task-1-baseline.txt
      2. find skills/ -name 'post_review.py' -exec md5 -r {} \; >> baseline
      3. Assert: all MD5s identical per script
    Evidence: .sisyphus/evidence/task-1-baseline.txt
  ```
  **Commit**: NO

- [ ] 2. Create `unity-review-shared/` + Move `post_review.py`

  **What to do**:
  - Create `skills/unity-review-shared/` with SKILL.md (pure index, <40L)
  - Description: `"Shared scripts and references for the Unity PR review pipeline. Not intended to be activated directly."`
  - Create `scripts/`, `scripts/tests/` subdirectories
  - Move `unity-review-prefab/scripts/post_review.py` → `unity-review-shared/scripts/post_review.py`
  - Move `unity-review-prefab/scripts/test_post_review.py` → `unity-review-shared/scripts/tests/test_post_review.py`
  - Create `scripts/tests/conftest.py` (match unity-plan-shared pattern)
  - Delete 4 duplicate `post_review.py` from: architecture, asset, code-pr, general
  - Clean up empty `scripts/` dirs from those 4 skills

  **Must NOT do**: Do NOT modify post_review.py content; Do NOT modify review SKILL.md refs yet (Task 7)
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 1 (with 3,4,5) | Blocks: 7, 29 | Blocked By: 1
  **References**: `skills/unity-plan-shared/SKILL.md` (shared skill pattern); `skills/unity-review-prefab/scripts/post_review.py` (canonical, 145L); `test_post_review.py` (222L); 4 duplicate copies to delete

  **Acceptance Criteria**:
  - [ ] `find skills/ -name 'post_review.py' | wc -l` → 1
  - [ ] `python3 -m pytest skills/unity-review-shared/scripts/tests/test_post_review.py` → PASS
  - [ ] `skill-validator` passes for unity-review-shared
  - [ ] No empty `scripts/` dirs in review skills

  **QA Scenarios**:
  ```
  Scenario: post_review.py deduplication
    Tool: Bash
    Steps:
      1. find skills/ -name 'post_review.py' | wc -l → assert 1
      2. python3 -m pytest skills/unity-review-shared/scripts/tests/ -v → assert pass
      3. find skills/unity-review-{architecture,asset,code-pr,general} -type d -name scripts -empty → assert none
    Evidence: .sisyphus/evidence/task-2-review-shared.txt
  ```
  **Commit**: YES (groups with T3-5) — `refactor(skills): create shared skill scaffolds and deduplicate scripts`

- [ ] 3. Create `unity-investigate-shared/` + Move `trace_logic.py`

  **What to do**:
  - Create `skills/unity-investigate-shared/` with SKILL.md (pure index, <40L)
  - Description: `"Shared scripts and references for Unity codebase investigation. Not intended to be activated directly."`
  - Create `scripts/`, `scripts/tests/` subdirectories
  - Move `unity-investigate-quick/scripts/trace_logic.py` → `unity-investigate-shared/scripts/trace_logic.py`
  - Move `unity-investigate-quick/scripts/test_trace_logic.py` → `unity-investigate-shared/scripts/tests/test_trace_logic.py`
  - Delete `unity-investigate-deep/scripts/trace_logic.py` and `test_trace_logic.py` (verified identical)
  - Keep reference files in their respective skills

  **Must NOT do**: Do NOT modify trace_logic.py content; Do NOT move trace_system.py/trace_architecture.py yet (Task 26); Do NOT modify investigate SKILL.md refs yet (Task 8)
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 1 (with 2,4,5) | Blocks: 8, 26, 27, 29 | Blocked By: 1
  **References**: `unity-plan-shared/SKILL.md` (pattern); `unity-investigate-quick/scripts/trace_logic.py` (canonical, 220L); `test_trace_logic.py` (390L); duplicate in unity-investigate-deep

  **Acceptance Criteria**:
  - [ ] `find skills/ -name 'trace_logic.py' | wc -l` → 1
  - [ ] `python3 -m pytest skills/unity-investigate-shared/scripts/tests/test_trace_logic.py` → PASS
  - [ ] `skill-validator` passes for unity-investigate-shared

  **QA Scenarios**:
  ```
  Scenario: trace_logic.py deduplication
    Tool: Bash
    Steps:
      1. find skills/ -name 'trace_logic.py' | wc -l → assert 1
      2. python3 -m pytest skills/unity-investigate-shared/scripts/tests/ -v → assert pass
    Evidence: .sisyphus/evidence/task-3-investigate-shared.txt
  ```
  **Commit**: YES (groups with T2)

- [ ] 4. Create Minimal Shared Scaffolds: git-shared, bash-shared, unity-test-shared, unity-document-shared

  **What to do**:
  - Create 4 shared skill directories, each with minimal SKILL.md (<30L, pure index)
  - Descriptions: `"Shared references for {group} skills. Not intended to be activated directly."`
  - Each has valid frontmatter + empty References/Scripts tables with placeholder comment
  - Do NOT create references/ or scripts/ subdirs until they have content

  **Must NOT do**: Do NOT move any existing files into these; Do NOT add content beyond minimal index
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 1 (with 2,3,5) | Blocks: 29 | Blocked By: 1
  **References**: `skills/unity-plan-shared/SKILL.md` (pattern)

  **Acceptance Criteria**:
  - [ ] All 4 exist with valid frontmatter; `skill-validator` passes; all <30L; each has activation guard

  **QA Scenarios**:
  ```
  Scenario: All 4 scaffold skills valid
    Tool: Bash
    Steps:
      1. For each: skill-validator passes, wc -l <30, grep 'Not intended to be activated directly'
    Evidence: .sisyphus/evidence/task-4-scaffolds.txt
  ```
  **Commit**: YES (groups with T2)

- [ ] 5. Create `unity-debug-shared/` + Move `common-fixes.md`

  **What to do**:
  - Create `skills/unity-debug-shared/` with SKILL.md (<40L) + `references/` dir
  - Description: `"Shared references for Unity debugging skills. Not intended to be activated directly."`
  - Move `unity-debug-quick/references/common-fixes.md` → `unity-debug-shared/references/common-fixes.md`
  - Update `unity-debug-quick/SKILL.md` to reference `../unity-debug-shared/references/common-fixes.md`

  **Must NOT do**: Do NOT move fix-loop.md, response-template.md, analysis-template.md, debug-log-reference.md (skill-specific)
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 1 (with 2,3,4) | Blocks: 17, 29 | Blocked By: 1
  **References**: `unity-plan-shared/SKILL.md` (pattern); `unity-debug-quick/references/common-fixes.md` (49L)

  **Acceptance Criteria**:
  - [ ] `unity-debug-shared/references/common-fixes.md` exists; original location does NOT
  - [ ] `unity-debug-quick/SKILL.md` references `../unity-debug-shared/`
  - [ ] `skill-validator` passes for both

  **QA Scenarios**:
  ```
  Scenario: common-fixes.md moved correctly
    Tool: Bash
    Steps:
      1. test -f skills/unity-debug-shared/references/common-fixes.md → exists
      2. test ! -f skills/unity-debug-quick/references/common-fixes.md → gone
      3. grep '../unity-debug-shared/' skills/unity-debug-quick/SKILL.md → match
    Evidence: .sisyphus/evidence/task-5-debug-shared.txt
  ```
  **Commit**: YES (groups with T2)

### Wave 2 — Rename + Consumer Path Updates

- [ ] 6. Rename `unity-code-standards/` → `unity-code-shared/` + Update ALL References

  **What to do**:
  - Use `git mv skills/unity-code-standards/ skills/unity-code-shared/` to preserve history
  - Update `SKILL.md` frontmatter: `name: unity-code-shared`
  - Update description to include `Not intended to be activated directly`
  - Find and update ALL references to old name across these files:
    1. `unity-code-deep/SKILL.md` — `use_skill("unity-code-standards")` → `use_skill("unity-code-shared")`
    2. `unity-code-deep/references/patterns-advanced.md` — text reference
    3. `unity-code-deep/references/patterns-core.md` — text reference
    4. `unity-code-quick/SKILL.md` — `read_skill_file` calls + text refs + **description field**
    5. `unity-review-architecture/SKILL.md` — `use_skill`
    6. `unity-review-architecture/references/ARCHITECTURE_PATTERNS.md` — text
    7. `unity-review-code-local/SKILL.md` — `read_skill_file` calls
    8. `unity-review-code-pr/SKILL.md` — `read_skill_file` calls
    9. `unity-review-general/references/APPROVAL_CRITERIA.md` — text
    10. `unity-code-shared/SKILL.md` — self-references
    11. `README.md` — skill table entry
  - Run `grep -r 'unity-code-standards' skills/ README.md --include='*.md'` to verify zero remaining

  **Must NOT do**: Do NOT change content/structure of ref files (only rename string); Do NOT move code-deep refs yet (Task 9)
  **Recommended Agent Profile**: `deep` + [`skill-creator`] — High blast radius, 11+ files across 7+ skills
  **Parallelization**: Wave 2 | Blocks: 9, 14, 15, 29 | Blocked By: 1
  **References**: `unity-code-standards/SKILL.md` (97L, 37 ref files); `unity-code-quick/SKILL.md`; `unity-review-code-pr/SKILL.md`; `unity-review-code-local/SKILL.md`; `unity-review-architecture/SKILL.md`; `README.md`

  **Acceptance Criteria**:
  - [ ] `test -d skills/unity-code-shared && test ! -d skills/unity-code-standards`
  - [ ] `grep -r 'unity-code-standards' skills/ README.md --include='*.md' | wc -l` → 0
  - [ ] `skill-validator` passes for unity-code-shared
  - [ ] `skill-deps` shows no broken references from consumer skills

  **QA Scenarios**:
  ```
  Scenario: Rename complete with zero dangling references
    Tool: Bash
    Steps:
      1. test -d skills/unity-code-shared && test ! -d skills/unity-code-standards
      2. grep -rn 'unity-code-standards' skills/ README.md --include='*.md' --include='*.py' → assert 0
      3. grep -c 'unity-code-shared' skills/unity-code-deep/SKILL.md skills/unity-code-quick/SKILL.md → each ≥1
    Evidence: .sisyphus/evidence/task-6-code-rename.txt
  ```
  **Commit**: YES — `refactor(skills): rename unity-code-standards to unity-code-shared`

- [ ] 7. Update 4 Review Skills' SKILL.md for Shared Script Paths

  **What to do**:
  - Update hardcoded bash paths in these 4 SKILL.md files to point to `unity-review-shared/scripts/post_review.py`:
    1. `unity-review-architecture/SKILL.md`
    2. `unity-review-asset/SKILL.md`
    3. `unity-review-code-pr/SKILL.md`
    4. `unity-review-general/SKILL.md`
  - NOTE: These use hardcoded bash paths like `./skills/unity-review-architecture/scripts/post_review.py` — NOT `run_skill_script`
  - Update to: `./skills/unity-review-shared/scripts/post_review.py`
  - Also update `unity-review-prefab/SKILL.md` (5th skill — had the canonical copy)
  - Verify each SKILL.md stays under 100 lines

  **Must NOT do**: Do NOT change functional behavior; Do NOT modify reference files; Do NOT touch unity-review-quality or unity-review-code-local (no scripts)
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 2 (with 6,8,9) | Blocks: 19-22, 29 | Blocked By: 2
  **References**: `unity-review-{architecture,asset,code-pr,general,prefab}/SKILL.md`; `unity-review-shared/` (from Task 2)

  **Acceptance Criteria**:
  - [ ] All 5 review SKILL.md files reference `unity-review-shared` for post_review.py
  - [ ] `grep -rn 'scripts/post_review' skills/unity-review-*/SKILL.md` shows only `unity-review-shared/` paths
  - [ ] All 5 pass `skill-validator`

  **QA Scenarios**:
  ```
  Scenario: All review skills use shared script path
    Tool: Bash
    Steps:
      1. grep -n 'post_review' skills/unity-review-{architecture,asset,code-pr,general,prefab}/SKILL.md
      2. Assert all matches contain 'unity-review-shared'
      3. Assert no matches contain local scripts/post_review path
    Evidence: .sisyphus/evidence/task-7-review-refs.txt
  ```
  **Commit**: YES (groups with T8,9) — `refactor(skills): update consumer skills to use shared references`

- [ ] 8. Update 2 Investigate Skills' SKILL.md for Shared Script Paths

  **What to do**:
  - Update `unity-investigate-quick/SKILL.md` and `unity-investigate-deep/SKILL.md` to reference `../unity-investigate-shared/scripts/trace_logic.py` instead of local scripts
  - Update hardcoded bash paths (NOT `run_skill_script` — it's not used)
  - Remove now-empty `scripts/` directories from both investigate skills (if no other scripts remain)

  **Must NOT do**: Do NOT modify reference files; Do NOT move output-template.md or analysis-rules.md (skill-specific)
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 2 (with 6,7,9) | Blocks: 18, 29 | Blocked By: 3
  **References**: `unity-investigate-quick/SKILL.md`; `unity-investigate-deep/SKILL.md`; `unity-investigate-shared/` (from Task 3)

  **Acceptance Criteria**:
  - [ ] Both SKILL.md files reference `../unity-investigate-shared/scripts/trace_logic.py`
  - [ ] No investigate skill has a local `scripts/trace_logic.py`
  - [ ] Both pass `skill-validator`

  **QA Scenarios**:
  ```
  Scenario: Both investigate skills use shared trace script
    Tool: Bash
    Steps:
      1. grep trace_logic skills/unity-investigate-{quick,deep}/SKILL.md → all point to investigate-shared
      2. find skills/unity-investigate-{quick,deep}/scripts -name 'trace_logic.py' → assert 0
    Evidence: .sisyphus/evidence/task-8-investigate-refs.txt
  ```
  **Commit**: YES (groups with T7)

- [ ] 9. Move code-deep's 3 Shared Refs to `unity-code-shared/` + Update code-quick

  **What to do**:
  - Move 3 reference files from `unity-code-deep/references/` to `unity-code-shared/references/`:
    1. `SCRIPT_TEMPLATE.md` (79L)
    2. `patterns-core.md` (89L)
    3. `patterns-advanced.md` (98L)
  - Update `unity-code-deep/SKILL.md` to reference `../unity-code-shared/references/` for these 3
  - Update `unity-code-quick/SKILL.md` to reference `../unity-code-shared/references/` instead of `../unity-code-deep/references/`
  - Add entries to `unity-code-shared/SKILL.md` References table

  **Must NOT do**: Do NOT modify content of the 3 files; Do NOT move other code-deep refs not consumed by code-quick; Do NOT restructure code-shared's existing subdirectories
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 2 (with 6,7,8) | Blocks: 14, 15, 29 | Blocked By: 6
  **References**: `unity-code-deep/references/SCRIPT_TEMPLATE.md` (79L); `patterns-core.md` (89L); `patterns-advanced.md` (98L); `unity-code-quick/SKILL.md` (9 cross-refs to update)

  **Acceptance Criteria**:
  - [ ] 3 files exist in `unity-code-shared/references/`; do NOT exist in `unity-code-deep/references/`
  - [ ] `grep 'unity-code-deep/references' skills/unity-code-quick/SKILL.md` → 0 matches
  - [ ] `grep 'unity-code-shared/references' skills/unity-code-quick/SKILL.md | wc -l` → ≥3
  - [ ] `skill-validator` passes for code-shared, code-deep, code-quick

  **QA Scenarios**:
  ```
  Scenario: References moved and all links updated
    Tool: Bash
    Steps:
      1. test -f skills/unity-code-shared/references/patterns-core.md
      2. test ! -f skills/unity-code-deep/references/patterns-core.md
      3. grep 'unity-code-deep/references' skills/unity-code-quick/SKILL.md → assert empty
    Evidence: .sisyphus/evidence/task-9-code-refs.txt
  ```
  **Commit**: YES (groups with T7)

### Waves 3-5 — Workflow Extraction (All Consumer Skills)

> **CRITICAL INSTRUCTION FOR ALL WORKFLOW EXTRACTION TASKS**:
> - Read the CURRENT state of each SKILL.md (prior waves may have modified it)
> - Do NOT reference original line counts from this plan — they may have changed
> - Extract workflow/template/example/tool-usage content into `references/workflow.md`
> - Create `references/` directory if it doesn't exist
> - Content is MOVED verbatim (except updating paths changed by prior waves)
> - SKILL.md retains: frontmatter, title, input/output summary, concise workflow reference, rules/constraints, reference index
> - Both SKILL.md and all reference files must be <100 lines
> - Run `skill-validator` for each modified skill
> - Follow `skills/unity-code-deep/SKILL.md` (51L, 3 refs) as the model structure

- [ ] 10. Extract Workflow: bash-check, bash-install, bash-optimize

  **What to do**:
  - For each: read SKILL.md → identify workflow/template/example content → extract to `references/workflow.md`
  - Create `references/` directory for all 3 (none exist currently)
  - bash-optimize (78L): also extract optimization patterns to `references/patterns.md`
  - bash-check (64L), bash-install (71L): extract workflow + template content

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 3 (with 11,12,13) | Blocks: 29 | Blocked By: 1
  **References**: `skills/bash-*/SKILL.md`; `skills/unity-code-deep/SKILL.md` (MODEL pattern)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; all SKILL.md <100L; all refs <100L; `skill-validator` passes for all 3

  **Commit**: YES — `refactor(skills): extract workflow refs for bash-check, bash-install, bash-optimize`

- [ ] 11. Extract Workflow: git-comment, git-commit

  **What to do**:
  - git-comment (89L): extract workflow steps, template format, examples → `references/workflow.md`, `references/template.md`
  - git-commit (63L): extract commit message format, examples → `references/workflow.md`, `references/template.md`
  - Create `references/` directory for both (none exist)

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 3 (with 10,12,13) | Blocks: 29 | Blocked By: 1
  **References**: `skills/git-comment/SKILL.md` (89L); `skills/git-commit/SKILL.md` (63L)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; git-comment reduced to <70L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for git-comment, git-commit`

- [ ] 12. Extract Workflow: git-description, git-squash

  **What to do**:
  - git-description (57L): extract workflow → `references/workflow.md`
  - git-squash (62L): extract workflow, examples → `references/workflow.md`, `references/examples.md`
  - Create `references/` directory for both

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 3 (with 10,11,13) | Blocks: 29 | Blocked By: 1
  **References**: `skills/git-description/SKILL.md` (57L); `skills/git-squash/SKILL.md` (62L)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for git-description, git-squash`

- [ ] 13. Extract Workflow: flatbuffers-coder

  **What to do**:
  - Create `references/` directory (doesn't exist)
  - Extract schema pattern code example → `references/schema-pattern.md`
  - Extract workflow steps → `references/workflow.md`

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 3 (with 10,11,12) | Blocks: 29 | Blocked By: 1
  **References**: `skills/flatbuffers-coder/SKILL.md` (49L)

  **Acceptance Criteria**:
  - [ ] Has `references/workflow.md`; SKILL.md <100L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for flatbuffers-coder`

- [ ] 14. Extract Workflow: unity-code-deep, unity-code-editor

  **What to do**:
  - unity-code-deep (~51L after T9 ref moves): extract Phase 0-3 steps → `references/workflow.md`
  - unity-code-editor (45L): extract workflow → `references/workflow.md`
  - NOTE: Read CURRENT state — T9 moved 3 ref files out of code-deep

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 4 (with 15,16,17) | Blocks: 29 | Blocked By: 6, 9
  **References**: `skills/unity-code-deep/SKILL.md`; `skills/unity-code-editor/SKILL.md` (45L)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-code-deep, unity-code-editor`

- [ ] 15. Extract Workflow: unity-code-quick

  **What to do**:
  - Create `references/` directory (doesn't exist)
  - Extract workflow → `references/workflow.md`
  - NOTE: Read CURRENT state — T6 renamed code-standards refs, T9 updated cross-refs

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 4 (with 14,16,17) | Blocks: 29 | Blocked By: 6, 9
  **References**: `skills/unity-code-quick/SKILL.md` (61L)

  **Acceptance Criteria**:
  - [ ] Has `references/workflow.md`; SKILL.md <100L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-code-quick`

- [ ] 16. Extract Workflow: unity-debug-deep, unity-debug-log

  **What to do**:
  - unity-debug-deep (74L): extract workflow → `references/workflow.md`. Has `analysis-template.md` already.
  - unity-debug-log (47L): extract workflow → `references/workflow.md`. Has `debug-log-reference.md` already.

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 4 (with 14,15,17) | Blocks: 29 | Blocked By: 1
  **References**: `skills/unity-debug-deep/SKILL.md` (74L); `skills/unity-debug-log/SKILL.md` (47L)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-debug-deep, unity-debug-log`

- [ ] 17. Extract Workflow: unity-debug-quick

  **What to do**:
  - Extract tool selection table → `references/tool-selection.md`
  - Create `references/workflow.md` from workflow steps
  - NOTE: Read CURRENT state — T5 moved common-fixes.md to debug-shared, reference already updated
  - Deduplicate Rules vs Hard Constraints overlap if present

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 4 (with 14,15,16) | Blocks: 29 | Blocked By: 5
  **References**: `skills/unity-debug-quick/SKILL.md` (60L); existing refs: `response-template.md`, `fix-loop.md` (note: common-fixes.md now in `../unity-debug-shared/`)

  **Acceptance Criteria**:
  - [ ] Has `references/workflow.md` and `references/tool-selection.md`; SKILL.md reduced; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-debug-quick`

- [ ] 18. Extract Workflow: unity-investigate-quick, unity-investigate-deep

  **What to do**:
  - Extract workflow steps → `references/workflow.md` for each
  - NOTE: Read CURRENT state — T8 updated script paths to investigate-shared
  - Keep tool tables inline if core operational knowledge

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 19-25) | Blocks: 29 | Blocked By: 8
  **References**: `skills/unity-investigate-quick/SKILL.md` (37L); `skills/unity-investigate-deep/SKILL.md` (40L)

  **Acceptance Criteria**:
  - [ ] Each has `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-investigate-quick, unity-investigate-deep`

- [ ] 19. Extract Workflow: unity-review-code-local, unity-review-code-pr

  **What to do**:
  - unity-review-code-local (68L): extract Load References block → `references/workflow.md`; extract input-to-diff mapping → `references/tool-usage.md`
  - unity-review-code-pr (100L AT CEILING): MUST extract workflow + tool usage to get under 80L. Create `references/workflow.md` and `references/tool-usage.md`
  - NOTE: Read CURRENT state — T7 updated script paths; T6 renamed code-standards refs

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18,20-25) | Blocks: 29 | Blocked By: 7
  **References**: `skills/unity-review-code-local/SKILL.md` (68L); `skills/unity-review-code-pr/SKILL.md` (100L — highest priority); existing refs in both

  **Acceptance Criteria**:
  - [ ] Both have `references/workflow.md`; unity-review-code-pr reduced to <80L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-review-code-local, unity-review-code-pr`

- [ ] 20. Extract Workflow: unity-review-architecture, unity-review-asset

  **What to do**:
  - unity-review-architecture (100L AT CEILING): MUST extract workflow + inline checklists → `references/workflow.md`. Target <80L.
  - unity-review-asset (96L near ceiling): extract workflow + checklist → `references/workflow.md`. Target <80L.
  - NOTE: Read CURRENT state — T7 updated script paths; T6 renamed code-standards refs

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18,19,21-25) | Blocks: 29 | Blocked By: 7
  **References**: `skills/unity-review-architecture/SKILL.md` (100L); `skills/unity-review-asset/SKILL.md` (96L)

  **Acceptance Criteria**:
  - [ ] Both have `references/workflow.md`; both reduced to <80L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-review-architecture, unity-review-asset`

- [ ] 21. Extract Workflow: unity-review-general, unity-review-prefab

  **What to do**:
  - unity-review-general (90L): extract workflow → `references/workflow.md`. Target <75L.
  - unity-review-prefab (88L): extract workflow → `references/workflow.md`. Target <75L.
  - NOTE: Read CURRENT state — T7 updated script paths

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18-20,22-25) | Blocks: 29 | Blocked By: 7
  **References**: `skills/unity-review-general/SKILL.md` (90L); `skills/unity-review-prefab/SKILL.md` (88L)

  **Acceptance Criteria**:
  - [ ] Both have `references/workflow.md`; both reduced to <80L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-review-general, unity-review-prefab`

- [ ] 22. Extract Workflow: unity-review-quality

  **What to do**:
  - Extract severity classification + grading criteria tables → `references/grading.md`
  - Create `references/workflow.md` from workflow section
  - Already has 10 ref files — do NOT reorganize those

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18-21,23-25) | Blocks: 29 | Blocked By: 1
  **References**: `skills/unity-review-quality/SKILL.md` (78L); 10 existing ref files

  **Acceptance Criteria**:
  - [ ] Has `references/workflow.md`; reduced to <65L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-review-quality`

- [ ] 23. Extract Workflow: unity-document-system, unity-document-tdd

  **What to do**:
  - unity-document-system (39L): create `references/` dir + `references/workflow.md`
  - unity-document-tdd (54L): create `references/` dir + `references/workflow.md`; optionally extract focus area mapping

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18-22,24,25) | Blocks: 27, 29 | Blocked By: 1
  **References**: `skills/unity-document-system/SKILL.md` (39L); `skills/unity-document-tdd/SKILL.md` (54L)

  **Acceptance Criteria**:
  - [ ] Both have `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-document-system, unity-document-tdd`

- [ ] 24. Extract Workflow: unity-test-unit, unity-test-case

  **What to do**:
  - unity-test-unit (58L, 5 refs): create `references/workflow.md`
  - unity-test-case (68L, 2 refs): create `references/workflow.md`; extract test sections table + priorities

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18-23,25) | Blocks: 29 | Blocked By: 1
  **References**: `skills/unity-test-unit/SKILL.md` (58L); `skills/unity-test-case/SKILL.md` (68L)

  **Acceptance Criteria**:
  - [ ] Both have `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for unity-test-unit, unity-test-case`

- [ ] 25. Extract Workflow: mermaid

  **What to do**:
  - Create `references/workflow.md`; extract diagram types table + examples + best practices

  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 5 (with 18-24) | Blocks: 29 | Blocked By: 1
  **References**: `skills/mermaid/SKILL.md` (51L); `skills/mermaid/references/MERMAID_PATTERNS.md`

  **Acceptance Criteria**:
  - [ ] Has `references/workflow.md`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): extract workflow refs for mermaid`

### Wave 6 — Tracing Unification + Dedup Audit

- [ ] 26. Create Unified Tracing Module in `unity-investigate-shared/`

  **What to do**:
  - Read and analyze all 3 tracing scripts:
    - `unity-investigate-shared/scripts/trace_logic.py` (220L, pure Python)
    - `unity-document-system/scripts/trace_system.py` (164L, subprocess-based)
    - `unity-document-tdd/scripts/trace_architecture.py` (121L, subprocess-based)
  - Create `skills/unity-investigate-shared/scripts/trace_unified.py` that:
    - Provides common core (`walk_files`, `grep_lines`) based on trace_logic.py's pure-Python approach
    - Exposes CLI subcommands: `trace_unified.py logic|system|architecture <args>`
    - Maintains backward-compatible CLI interfaces
  - Write tests: `scripts/tests/test_trace_unified.py`
  - Keep original `trace_logic.py` as-is until Task 27 updates consumers
  - Update `investigate-shared/SKILL.md` to document the unified script

  **Must NOT do**: Do NOT remove trace_system.py/trace_architecture.py from document skills yet (Task 27); Do NOT change trace_logic.py behavior; Do NOT add features beyond what originals provide
  **Recommended Agent Profile**: `deep` + [`bash-check`] — Requires understanding 3 APIs and creating unified module
  **Parallelization**: Wave 6 | Blocks: 27, 29 | Blocked By: 3
  **References**: `investigate-shared/scripts/trace_logic.py` (220L); `unity-document-system/scripts/trace_system.py` (164L); `unity-document-tdd/scripts/trace_architecture.py` (121L); existing tests

  **Acceptance Criteria**:
  - [ ] `trace_unified.py` exists with 3 modes
  - [ ] Each mode produces equivalent output to original script
  - [ ] `python3 -m pytest skills/unity-investigate-shared/scripts/tests/test_trace_unified.py` → PASS

  **QA Scenarios**:
  ```
  Scenario: Unified tracing works for all 3 modes
    Tool: Bash
    Steps:
      1. python3 trace_unified.py logic "test" --root skills/ → exit 0, output has matches
      2. python3 trace_unified.py system "SKILL" --root skills/ → exit 0, structured output
      3. python3 -m pytest test_trace_unified.py -v → all pass
    Evidence: .sisyphus/evidence/task-26-unified-tracing.txt
  ```
  **Commit**: YES — `feat(skills): create unified tracing module in investigate-shared`

- [ ] 27. Update Document Skills to Use Unified Tracing

  **What to do**:
  - Update `unity-document-system/SKILL.md` to reference `../unity-investigate-shared/scripts/trace_unified.py system`
  - Update `unity-document-tdd/SKILL.md` to reference `../unity-investigate-shared/scripts/trace_unified.py architecture`
  - Remove `unity-document-system/scripts/trace_system.py`
  - Remove `unity-document-tdd/scripts/trace_architecture.py`
  - Update `unity-document-shared/SKILL.md` to reference the unified script
  - Clean up empty scripts/ dirs if applicable

  **Must NOT do**: Do NOT modify document skills' reference files or templates; Do NOT change behavior
  **Recommended Agent Profile**: `quick` + [`skill-creator`]
  **Parallelization**: Wave 6 (after T26) | Blocks: 29 | Blocked By: 23, 26
  **References**: `unity-document-system/SKILL.md`; `trace_system.py` (164L, to remove); `unity-document-tdd/SKILL.md`; `trace_architecture.py` (121L, to remove)

  **Acceptance Criteria**:
  - [ ] `test ! -f skills/unity-document-system/scripts/trace_system.py`
  - [ ] `test ! -f skills/unity-document-tdd/scripts/trace_architecture.py`
  - [ ] Both SKILL.md files reference `trace_unified.py`; `skill-validator` passes

  **Commit**: YES — `refactor(skills): migrate document skills to unified tracing module`

- [ ] 28. Audit All SKILL.md for SKILL.md ↔ Reference Content Duplication

  **What to do**:
  - For EVERY skill (except skill-creator): read SKILL.md + ALL reference files
  - Check skill-creator's rule: "Information should live in either SKILL.md or references, not both"
  - Look for: duplicate tool instructions, repeated code patterns, duplicated checklist items
  - For violations: keep in whichever location makes more sense, remove from other, add link
  - Document all changes in summary

  **Must NOT do**: Do NOT change behavior/triggers/descriptions; Do NOT consolidate review-quality checklists with code-shared refs; Do NOT create new refs (only deduplicate); Do NOT modify skill-creator
  **Recommended Agent Profile**: `unspecified-high` + [`skill-creator`] — Judgment calls about what's duplicated vs complementary
  **Parallelization**: Wave 6 (with 26,27) | Blocks: 29 | Blocked By: 1 (best after Waves 3-5)
  **References**: All 42 skill directories; `skill-creator/SKILL.md` (duplication rule)

  **Acceptance Criteria**:
  - [ ] No >3 consecutive identical lines between any SKILL.md and its reference files
  - [ ] All modified SKILL.md <100L; all modified refs <100L; `skill-validator` passes

  **Commit**: YES — `refactor(skills): remove SKILL.md \u2194 reference content duplication`

### Wave 7 — Validation

- [ ] 29. Full Validation Sweep — All 42 Skills

  **What to do**:
  - Run `skill-validator` for ALL skill directories
  - Run `wc -l skills/*/SKILL.md` — assert ALL <100L (except skill-creator)
  - Run `wc -l skills/*/references/*.md` — assert ALL <100L
  - Verify every consumer skill has `references/workflow.md` (exclude *-shared, skill-creator, plan-*)
  - Run `skill-deps` for all shared skills — verify no broken references
  - Run `grep -r 'unity-code-standards' skills/ README.md --include='*.md'` — assert 0
  - Run `find skills/ -name 'post_review.py' | wc -l` — assert 1
  - Run `find skills/ -name 'trace_logic.py' | wc -l` — assert 1
  - Run all test suites: pytest for review-shared, investigate-shared, plan-shared
  - Verify `git diff skills/skill-creator/` is empty
  - Compare against baseline from Task 1
  - Fix any issues found and re-validate
  - Save final report to `.sisyphus/evidence/task-29-final-validation.txt`

  **Must NOT do**: Do NOT modify skill-creator; report findings first, fix if needed
  **Recommended Agent Profile**: `deep` + [`skill-creator`]
  **Parallelization**: Wave 7 (solo) | Blocks: F1-F4 | Blocked By: 1-28 (all)
  **References**: `.sisyphus/evidence/task-1-baseline.txt` (baseline); all 42 skill directories

  **Acceptance Criteria**:
  - [ ] ALL skills pass `skill-validator`
  - [ ] ALL SKILL.md <100L (except skill-creator)
  - [ ] ALL reference files <100L
  - [ ] ALL consumer skills have `references/workflow.md`
  - [ ] Zero dangling references; zero duplicate scripts; zero `unity-code-standards` mentions
  - [ ] skill-creator untouched; plan-* skills untouched
  - [ ] All pytest suites pass

  **QA Scenarios**:
  ```
  Scenario: Full validation passes
    Tool: Bash
    Steps:
      1. wc -l skills/*/SKILL.md | awk '$1 >= 100 {print}' | grep -v skill-creator → assert empty
      2. grep -r 'unity-code-standards' skills/ README.md --include='*.md' → assert 0
      3. find skills/ -name 'post_review.py' | wc -l → 1; find skills/ -name 'trace_logic.py' | wc -l → 1
      4. python3 -m pytest skills/*/scripts/tests/ → all pass
      5. git diff skills/skill-creator/ → empty
    Evidence: .sisyphus/evidence/task-29-final-validation.txt
  ```
  **Commit**: YES (if fixes applied) — `chore(skills): resolve validation issues from combined refactor`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan. Verify all 9 shared skills exist, all duplicates eliminated, all workflow.md files created.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `skill-validator` on all 42 skill directories. Check all SKILL.md files for: broken markdown links, `../` references pointing to non-existent paths, `read_skill_file`/`use_skill` calls with non-existent skill names. Verify no orphaned files left behind from moves. Run `find skills/ -type d -name "scripts" -empty` to find empty script dirs.
  Output: `Validator [N pass/N fail] | Broken Refs [N] | Orphaned Files [N] | VERDICT`

- [ ] F3. **Reference Integrity QA** — `unspecified-high`
  Run all tests: `python3 -m pytest skills/unity-review-shared/ skills/unity-investigate-shared/ skills/unity-plan-shared/`. Verify every `../` relative path in every SKILL.md resolves to an existing file. Verify `find skills/ -name "*.py" -not -name "test_*" -not -name "__*" -not -name "conftest*" | xargs md5 -r | sort -k1,1 | awk '{print $1}' | uniq -d` is empty (no duplicate scripts by content). Verify `grep -r 'unity-code-standards' skills/ README.md | wc -l` is 0. Save evidence.
  Output: `Tests [N/N pass] | Relative Paths [N/N resolve] | Duplicate Scripts [CLEAN/N] | Dangling Refs [CLEAN/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built, nothing beyond spec was added. Verify `git diff skills/skill-creator/` is empty. Verify `git diff skills/unity-plan-shared/ skills/unity-plan-quick/ skills/unity-plan-deep/ skills/unity-plan-detail/` is empty (validate-only, no modifications). Check "Must NOT do" compliance. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | skill-creator [UNTOUCHED] | plan-skills [UNTOUCHED] | VERDICT`

---

## Commit Strategy

- **Wave 1**: `refactor(skills): create shared skill scaffolds and deduplicate scripts`
- **Wave 2**: `refactor(skills): rename code-standards→code-shared and update consumer refs`
- **Waves 3-5**: One commit per task group: `refactor(skills): extract workflow refs for {skill-names}`
- **Wave 6**: `feat(skills): create unified tracing module` + `refactor(skills): remove SKILL.md ↔ reference duplication`
- **Wave 7**: `chore(skills): validate all skills pass validator and deps checks` (if fixes needed)
- **Total**: ~20-22 commits

---

## Success Criteria

### Verification Commands
```bash
# All 9 shared skills exist
ls -d skills/unity-{review,investigate,code,debug,document,test,plan}-shared skills/git-shared skills/bash-shared | wc -l
# Expected: 9

# No duplicate scripts
find skills/ -name "post_review.py" | wc -l  # Expected: 1
find skills/ -name "trace_logic.py" | wc -l  # Expected: 1

# Rename complete
test ! -d skills/unity-code-standards && echo "RENAMED"  # Expected: RENAMED
test -d skills/unity-code-shared && echo "EXISTS"         # Expected: EXISTS

# No references to old name
grep -r "unity-code-standards" skills/ README.md --include="*.md" | wc -l  # Expected: 0

# All SKILL.md under 100 lines (excluding skill-creator)
wc -l skills/*/SKILL.md | awk '$1 >= 100 {print}' | grep -v skill-creator | wc -l  # Expected: 0

# All consumer skills have workflow.md (excluding shared + skill-creator + plan-*)
for d in skills/*/; do
  name=$(basename "$d")
  [[ "$name" == "skill-creator" ]] && continue
  [[ "$name" == *"-shared"* ]] && continue
  [[ "$name" == "unity-plan-"* ]] && continue
  [ -f "$d/references/workflow.md" ] || echo "MISSING: $name"
done
# Expected: no output

# All reference files under 100 lines
find skills/*/references/ -name "*.md" -exec sh -c 'lines=$(wc -l < "$1"); [ "$lines" -ge 100 ] && echo "$1: $lines"' _ {} \;
# Expected: no output

# skill-creator untouched
git diff skills/skill-creator/ | wc -l  # Expected: 0

# All tests pass
python3 -m pytest skills/unity-review-shared/scripts/tests/ skills/unity-investigate-shared/scripts/tests/ skills/unity-plan-shared/scripts/tests/
# Expected: all pass

# No empty script directories
find skills/ -type d -name "scripts" -empty 2>/dev/null
# Expected: no output
```

### Final Checklist
- [ ] All "Must Have" present (9 shared skills, 29 workflow.md files, zero duplicates, rename complete)
- [ ] All "Must NOT Have" absent (no skill-creator changes, no plan-* changes, no content rewrites, no requirement.txt dedup)
- [ ] All tests pass
- [ ] All 42 skills pass skill-validator
- [ ] All cross-references resolve (skill-deps clean)
