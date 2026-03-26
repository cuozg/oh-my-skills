---
name: unity-review
description: >
  Use this skill to review Unity code changes, GitHub pull requests, or audit entire Unity projects for
  quality. Covers three modes: local review (inline // REVIEW comments on changed C# files), PR review
  (parallel specialist reviews of .cs, .prefab, .shader files with APPROVE/REQUEST_CHANGES via GitHub
  API), and project audit (A-F grades on architecture, performance, best practices, tech debt as HTML
  report). MUST use whenever the user mentions reviewing code, checking changes, evaluating a pull
  request, auditing project quality, or assessing merge readiness. Also use when they say "look over my
  changes," "check this PR," "code review," "is this ready to merge," "rate this codebase," "tech debt,"
  "quality report," "check the prefabs," "review the assets," or wants any feedback on Unity code,
  assets, or architecture before merging or committing.
metadata:
  author: kuozg
  version: "2.0"
---

# unity-review

Detect review target, classify changed file types and size, delegate specialist reviews to parallel subagents, aggregate findings, deliver results — inline comments for local, GitHub comments + APPROVE/REQUEST_CHANGES for PRs, HTML reports for audits.

## Step 1 — Detect Review Mode

| Signal | Mode | First Action |
|--------|------|-------------|
| PR URL/number, "PR", "pull request", "merge", "is this ready" | **PR Review** | `read_skill_file("unity-review", "references/pr-review-workflow.md")` |
| "review my code", "check changes", specific file path, no PR context | **Local Review** | `read_skill_file("unity-review", "references/local-review-workflow.md")` |
| "audit project", "quality report", "tech debt", "rate codebase", "grade" | **Project Audit** | `read_skill_file("unity-review", "references/quality-audit-workflow.md")` |

If ambiguous, ask: "Should I review your local changes, a GitHub PR, or audit the whole project?"

## Step 2 — Load Standards

For all modes, load `unity-standards` checklists via `read_skill_file("unity-standards", "references/<path>")`:

| Mode | Required References |
|------|-------------------|
| **PR Review** | `review/checklist.md`, `review/pr-submission.md`, `review/parallel-review-criteria.md` (for Large PRs) |
| **Local Review** | `review/checklist.md`, `review/comment-format.md`, `review/parallel-review-criteria.md` |
| **Project Audit** | `quality/grading-criteria.md`, `quality/architecture-audit.md`, `quality/performance-audit.md`, `quality/best-practices-audit.md`, `quality/tech-debt-audit.md`, `quality/html-report-format.md` |

## Step 3 — Execute

### PR Review

Follow `references/pr-review-workflow.md` — a self-contained 11-step workflow:

1. Resolve owner/repo → 2. Fetch PR metadata → 3. Fetch file content → 4. Assess PR size (Minor/Large) → 5. Classify files and route to specialists (`references/pr-specialist-reviews.md`) → 6. Aggregate findings → 7. Check for prior reviews → 8. Make final decision (APPROVE/REQUEST_CHANGES/COMMENT) → 9. Build review body → 10. Submit via `gh api` → 11. Verify submission

**Key rules:**
- Minor PR (1-2 CS files, 1-5 functions) → single-pass review
- Large PR (3+ files or 6+ functions) → parallel subagents (one per checklist criterion)
- Always fetch full file content, not just diff hunks
- One review submission per run — never call reviews API twice
- Verify submission succeeded before reporting done

### Local Review

Follow `references/local-review-workflow.md`:

1. Determine scope (all changes / staged / specific file) → 2. Filter to `.cs` files → 3. Read full files → 4. Spawn 6 parallel subagents (one per review criterion) → 5. Collect results → 6. Aggregate and validate with LSP → 7. Insert `// ── REVIEW` comments → 8. Apply safe single-line fixes → 9. Queue remaining issues via `task_create`

**Key rules:**
- Always read full file, not just diff hunk
- Use `lsp_find_references` before flagging dead code
- Never commit — leave diff for user inspection

### Project Audit

Follow `references/quality-audit-workflow.md`:

1. Scope files → 2. Analyze architecture → 3. Analyze performance → 4. Evaluate best practices → 5. Measure tech debt → 6. Grade A-F per rubric → 7. Generate HTML report

**Key rules:**
- Read-only — never modify source code
- Every grade must cite evidence (file:line)
- Include "Top 5 Priority Fixes" ranked by severity × frequency

## Comment Format (PR)

````
**{🔴|🟠|🟡|🔵|⚪} Title** — `SEVERITY`

{what is wrong, why it matters}

```suggestion
{corrected code}
```
````

Suggestion blocks required for MEDIUM+ severity.

## Comment Format (Local)

```csharp
// ── REVIEW {icon} {LABEL} #{category}
// What: 1-line summary
// Why:  1-3 lines — impact + evidence
```

## Severity Scale

🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW → ⚪ STYLE

### Minimum Severity Floors

These issues must NEVER be graded below the stated level:

| Issue | Floor |
|-------|:-----:|
| Missing event unsubscription (OnEnable += / no OnDisable -=) | HIGH |
| Coroutine not stopped on lifecycle exit | HIGH |
| `async void` outside Unity event handlers | MEDIUM |
| `GetComponent` / `Find*` per frame (Update/FixedUpdate) | MEDIUM |
| Missing null check on deserialized gameplay data | MEDIUM |
| Hardcoded API keys, passwords, tokens | CRITICAL |
| `m_Script: {fileID: 0}` (missing MonoBehaviour in prefab) | CRITICAL |
| LINQ / string concat / lambda allocations in Update | MEDIUM |
| `FindObjectOfType` in production code for runtime wiring | HIGH |
| Missing `[FormerlySerializedAs]` on renamed serialized field | HIGH |
| `DestroyImmediate` in runtime code | HIGH |

## Error Handling

| Problem | Action |
|---------|--------|
| `gh` not installed or not authenticated | Tell user: `brew install gh && gh auth login` |
| PR number not found (404) | Verify owner/repo. Check if PR is in a fork. |
| No local changes found | Check `git status`. Inform user if working tree is clean. |
| Project too large (1000+ files) for audit | Use sampling strategy (see quality audit workflow). |
| Subagent returns empty findings | That's fine — no issues in that criterion. Include in summary. |
| Review submission fails (422) | Re-fetch HEAD SHA. Check comment size (<32KB). Retry. |
