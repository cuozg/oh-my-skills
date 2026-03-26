# Local Review Workflow

Review locally changed Unity C# files by adding inline `// ── REVIEW` comments.

## 1. Determine Review Scope

| User Request | Diff Command | Scope |
|---|---|---|
| "review my changes" (default) | `git diff HEAD` | All unstaged + staged changes |
| "review staged changes" | `git diff --cached` | Only staged changes |
| "review this file" + path | Read full file | Specific file(s), no diff needed |
| "review since last commit" | `git diff HEAD~1` | Changes in last commit |

**If no changes found:** Check `git status`. If working tree is clean, inform user: "No local changes to review. Did you mean to review a specific file or PR?"

## 2. Filter to C# Files

From the diff output, select only `.cs` files. Ignore `.meta`, `.asset`, `.unity`, `.prefab` files (those are binary/serialized and reviewed differently — see quality audit for project-wide asset review).

If the user specifically asked to review a non-C# file, read and review it, but note that automated checklists are designed for C# code.

## 3. Read Full Files

Load complete file content for every changed `.cs` file — not just diff hunks. Full context is needed for:
- Subscribe/unsubscribe symmetry (OnEnable ↔ OnDisable)
- Lifecycle correctness (Awake → Start → OnEnable ordering)
- Cross-method data flow (a field set in Update, read in coroutine)
- Architecture patterns (class responsibility, dependency direction)

## 4. Spawn Parallel Review Subagents

Spawn 6 parallel subagents — one per criterion. Each runs as `task(category="quick", load_skills=["unity-standards"], run_in_background=true)`.

| # | Criterion | Checklist Section |
|---|-----------|-------------------|
| 1 | Logic | `review/checklist.md` — `## 1. Logic` |
| 2 | Unity Lifecycle | `review/checklist.md` — `## 2. Unity Lifecycle` |
| 3 | Serialization | `review/checklist.md` — `## 3. Serialization` |
| 4 | Performance | `review/checklist.md` — `## 4. Performance` |
| 5 | Security | `review/checklist.md` — `## 5. Security` |
| 6 | Concurrency | `review/checklist.md` — `## 6. Concurrency` |

See `unity-standards/references/review/parallel-review-criteria.md` for the subagent prompt template.

**Subagent prompt pattern:**
```
TASK: Review these C# files for {criterion_name} issues only.
CHECKLIST: Load `read_skill_file("unity-standards", "references/review/checklist.md")` — check every item under section {section_number}.
FILES: {file_paths_and_full_contents}
DIFF: {diff_hunks_for_context_on_what_changed}

MUST DO:
- Check EVERY item in your assigned section against the code
- Report as JSON array: [{path, line, severity, title, body}]
- severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE"
- For local review, check ALL code in changed files (not just changed lines)

MUST NOT DO:
- Review criteria outside your assigned section
- Suggest fixes that change behavior (leave that for the developer)
```

## 5. Collect Results

Use `background_output` on all 6 tasks. Each returns a JSON array of findings.

## 6. Aggregate and Validate

1. Merge all findings into a single list
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file path → line number
4. **Validate uncertain findings**: Use `lsp_goto_definition` / `lsp_find_references` for:
   - Dead code claims — verify nothing references the symbol
   - Missing unsubscription — verify the subscription actually exists
   - Unused variable — verify it's not used via reflection or serialization

## 7. Annotate Source Files

Insert `// ── REVIEW` comments using the format from `unity-standards/references/review/comment-format.md`:

```csharp
// ── REVIEW 🟠 HIGH #lifecycle
// What: OnEnable subscribes to PlayerEvents.OnDamage but OnDisable doesn't unsubscribe
// Why:  Causes duplicate handlers after disable/enable cycle, leading to double damage
```

Rules:
- Place comment on the line **above** the problem
- One comment per issue — do not combine unrelated findings
- Always include icon, label, and category tag on the header line

## 8. Apply Safe Fixes

Apply only trivial, safe, single-line fixes:
- Add null check: `if (component != null)`
- Cache GetComponent: move to `Awake`/`Start` field
- Add missing unsubscription in `OnDisable`/`OnDestroy`
- Add `CompareTag` replacement for `tag ==`
- Add `[FormerlySerializedAs]` for renamed fields

**Never apply** multi-line refactors, architectural changes, or behavioral modifications. Leave those as `// ── REVIEW` comments.

## 9. Queue Remaining Issues

For every finding NOT fixed inline, create a `task_create` entry:
- Subject: `[REVIEW] {severity} — {title}`
- Description: What, why, file:line, suggested approach

## Rules

- Always read full file, not just diff hunk
- Use `lsp_find_references` before flagging dead code
- Flag `Update()` allocations (LINQ, string concat, closures) as MEDIUM+
- Flag missing `OnDestroy` unsubscription when `OnEnable`/`Awake` subscribes
- Never commit — leave diff for user inspection
- Create `task_create` only for unfixed issues

## Output

Modified source files with inline `// ── REVIEW` comments + summary listing:
1. Total findings by severity
2. Fixes applied (with file:line)
3. Remaining unfixed issues (with task IDs if created)
