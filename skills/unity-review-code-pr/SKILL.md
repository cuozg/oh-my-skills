---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs with surgical focus on code logic - correctness, edge cases, state management, data flow, concurrency, and Unity-specific patterns. After review, push comments directly to GitHub via the API.

## Input → Command

| Input | Command |
|:------|:--------|
| None | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |

## Severity → Approval

| Severity | Meaning | Approval |
|:---------|:--------|:---------|
| CRITICAL | Crash, data loss, security, breaking API | `REQUEST_CHANGES` (block) |
| HIGH | Logic bugs, missing tests, arch violations | `REQUEST_CHANGES` |
| MEDIUM | Code quality, conventions, minor perf | `COMMENT` (allow merge) |
| LOW | Style preferences, typos, micro-optimization | `APPROVE` (with suggestions) |
| CLEAN | No issues | `APPROVE` |

Full decision tree: [APPROVAL_CRITERIA.md](references/APPROVAL_CRITERIA.md).

## Load References

Before any review work, load these references:

```python
read_skill_file("unity-code-standards", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-standards", "references/review/csharp-quality.md")
read_skill_file("unity-code-standards", "references/review/performance-review.md")
read_skill_file("unity-code-standards", "references/review/unity-specifics.md")
```

These are the review checklists. Apply them against every changed `.cs` file.

## Workflow

### 1. Fetch PR Diff

```bash
gh pr diff <N> --name-only   # Get changed files
gh pr view <N> --json title,body,files,number  # Get PR context
```

Filter to `.cs` files ONLY. If no `.cs` files, skip review and APPROVE with note `No C# files to review.`

### 2. Load Review References

Load all 4 reference files from `unity-code-standards`:

```python
read_skill_file("unity-code-standards", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-standards", "references/review/csharp-quality.md")
read_skill_file("unity-code-standards", "references/review/performance-review.md")
read_skill_file("unity-code-standards", "references/review/unity-specifics.md")
```

### 3. Fetch Full Diff

```bash
gh pr diff <N>   # Full diff for .cs files
```

### 4. Read Full File Context

For each changed `.cs` file, read the ENTIRE file (not just the diff). Logic bugs hide in surrounding context. Use `read` tool to get full file content for each changed file.

### 5. Deep Investigate (Parallel)

Spawn 2-3 `@explore` agents in background to gather evidence:

- **Call-site analysis**: For each modified public method/property, find all callers and count call sites.
- **State flow**: Trace state transitions - what sets each field and what reads it.
- **Data contract**: Check serialization, API boundaries, and event payloads.

### 6. Logic Review

Apply loaded review checklists against each changed file. Focus areas:

- Control flow (branches, loops, early returns, switches)
- State management (field mutations, init order, lifetime)
- Data flow (input validation, null propagation, type safety)
- Edge cases (zero, null, empty, max, negative, concurrent)
- Unity lifecycle (Awake/OnEnable/Start/OnDisable/OnDestroy balance)
- Serialization safety (field renames, type changes, migration)
- Memory safety (per-frame allocations, event leaks, resource disposal)
- Async patterns (cancellation, shared state, thread safety)

### 7. Build `/tmp/review.json`

Assemble the final review JSON per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

```json
{
  "body": "[SUMMARY - see body template below]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    { "path": "Assets/Scripts/Example.cs", "line": 42, "side": "RIGHT", "body": "[INLINE]" }
  ]
}
```

Do NOT include `commit_id` - `post_review.sh` injects it automatically.

Summary body template:

```markdown
## Code Review - PR #[N]
**Scope**: [PR title]
[One-sentence overall assessment].

### Findings Summary
| Severity | Count |
|:---------|:------|
| 🔴 Critical | [N] |
| 🟡 High | [N] |
| 🔵 Medium | [N] |
| 🟢 Low | [N] |

### Acceptance Criteria
- [ ] No critical or high severity issues remain
- [ ] Feature works; edge cases handled
- [ ] No frame drops, GC spikes
- [ ] No breaking serialization changes

### Breaking Changes ([N])
### Potential Issues ([N])
### Unity-Specific Concerns ([N])
### Code Quality ([N])
### Impact Analysis
- Files reviewed: X · Total findings: Y
```

### 8. Submit

```bash
./skills/unity-review-code-pr/scripts/post_review.sh <pr_number> /tmp/review.json
```

Fallback (merged/closed): handled automatically by `post_review.sh`.

## Suggestion Syntax Quick Reference

| Type | JSON fields | Notes |
|:-----|:------------|:------|
| Single-line | `"line": 42` | Suggestion replaces that one line |
| Multi-line | `"start_line": 10, "line": 15` | Suggestion replaces lines 10–15 |
| Large rewrite | Single `"line"` | Use `<details>` block instead of suggestion |

`line` = file line number (not diff position). `side` always `"RIGHT"`. Full syntax in [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Inline Comment Format

**🔴 Critical / 🟡 High:**

```markdown
**[Issue]**: [What's wrong]
**Evidence**: [Proof - caller count, file:line, YAML key]
**Why**: [Impact]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🔵 Medium:**

```markdown
**[Issue]**: [What to improve]
**Why**: [Reason]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🟢 Low:**

```markdown
**Suggestion**: [What could be better]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

Full format and syntax details: [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Evidence Rules

- 🔴 Critical needs: caller count + affected files + reproduction scenario.
- 🟡 High needs: trigger conditions + what state leads to the bug.
- 🔵 Medium needs: brief explanation of why current code is suboptimal.
- 🟢 Low needs: brief note.
- Never flag without evidence. Investigate before commenting.

## Rules

- ✅ Only review `.cs` files. Skip all other file types.
- ✅ Read the full file, not just the diff. Logic bugs need context.
- ✅ Trace data flow end-to-end. Follow the value from source to sink.
- ✅ One issue = one comment. Each with severity emoji + Evidence + Why + suggestion.
- ✅ Same issue in N files -> full explanation on first, short ref + suggestion on rest (batch pattern).
- ✅ Check what happens when assumptions are violated (null, empty, concurrent, out-of-order).
- ✅ Verify event subscribe/unsubscribe pairs. Check lifecycle ordering.
- ✅ If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- ✅ For serialization-related findings, check whether the project has migration/versioning support.
- ✅ Submit even if PR is merged - `post_review.sh` handles the fallback.
- ❌ Never combine issues. Never skip submission. Never flag without evidence.
- ❌ Never hardcode `commit_id` - `post_review.sh` auto-injects it.
- ❌ Never modify source files. This is a read-only review.
- ❌ Never review non-`.cs` files (prefabs, assets, shaders, scenes).
- ❌ Never delegate to sub-skills. This skill does the review directly.
