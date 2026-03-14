---
name: unity-review
description: >
  Unified Unity review skill — reviews local changes, GitHub PRs, or full projects. For local changes,
  adds inline // REVIEW comments to C# files. For GitHub PRs, classifies changed files by type (.cs,
  .prefab, .mat, .shader, etc.), assesses change size, spawns parallel specialist reviews (code,
  architecture, assets, prefabs), aggregates findings, and posts APPROVE or REQUEST_CHANGES via GitHub
  API. For project audits, grades architecture, performance, best practices, and tech debt A-F with an
  HTML report. Use whenever the user says "review my code," "review this PR," "check my changes,"
  "review PR #123," "audit this project," "code quality report," "is this ready to merge," "check the
  prefabs," "review the assets," or wants any form of Unity code, asset, or architecture review.
---
# unity-review

Detect review target, classify changed file types and size, delegate specialist reviews to parallel subagents, aggregate findings, deliver results — inline comments for local, GitHub comments + APPROVE/REQUEST_CHANGES for PRs, HTML reports for audits.

## Step 1 — Detect Review Mode

| Signal | Mode | Reference |
|--------|------|-----------|
| PR URL/number, "PR", "pull request", "merge" | **PR Review** | `references/pr-review-workflow.md` |
| "review my code", "check changes", specific file, no PR | **Local Review** | `references/local-review-workflow.md` |
| "audit project", "quality report", "tech debt", "rate codebase" | **Project Audit** | `references/quality-audit-workflow.md` |

## Step 2 — Execute

### PR Review

1. **Fetch PR** — follow `references/pr-review-workflow.md`
2. **Classify files** by type and spawn specialist subagents in parallel:
   - `.cs` → code review (size-aware routing per `references/size-assessment.md`)
   - `.prefab`, `.unity` → prefab/scene review (one subagent per file)
   - `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` → asset review
   - `.cs` with new systems/services/managers or `.asmdef` → architecture review
3. **Specialist rules** — `references/pr-specialist-reviews.md`
4. **Aggregate** — deduplicate by (path, line), keep highest severity, sort file → line
5. **Final decision** — APPROVE or REQUEST_CHANGES per `references/final-decision.md`
6. **Submit** — single review POST per `unity-standards/references/review/pr-submission.md`
7. **Verify** — confirm posted, retry on failure

### Local Review

Follow `references/local-review-workflow.md`:
`git diff` → read .cs files → 6 parallel subagents (one per criterion) → aggregate → insert `// ── REVIEW` comments → apply safe fixes → `task_create` for unfixed issues.

### Project Audit

Follow `references/quality-audit-workflow.md`:
Scope files → analyze 4 categories → grade A-F per `references/quality-grading-rubric.md` → generate HTML report.

## Comment Format (PR)

````
**{🔴|🟠|🟡|🔵|⚪} Title** — `SEVERITY`

{what is wrong, why it matters}

```suggestion
{corrected code}
```
````

Suggestion blocks required for MEDIUM+ severity.

## Severity Scale

🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW → ⚪ STYLE

Minimum floors: GetComponent/Find* per frame → MEDIUM · Missing event unsub → HIGH · Coroutine not stopped on lifecycle exit → HIGH · `async void` → MEDIUM

## Standards

Load `unity-standards` for all checklists via `read_skill_file("unity-standards", "references/<path>")`:

- `review/` — logic, lifecycle, serialization, performance, security, concurrency, architecture, asset, prefab checklists
- `review/comment-format.md`, `review/pr-submission.md`, `review/parallel-review-criteria.md`
- `quality/` — grading-criteria, architecture-audit, performance-audit, best-practices-audit, tech-debt-audit, html-report-format
