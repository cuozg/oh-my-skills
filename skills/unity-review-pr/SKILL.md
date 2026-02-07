---
name: unity-review-pr
description: "Expert Unity Developer code reviewer. Reviews PRs, commits, branches, or uncommitted changes with focus on Unity-specific patterns, performance, and best practices. Accepts Pull Request links as input. Use when: reviewing PRs, checking changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity Code Reviewer

Review code changes as an **expert Unity Developer**. Each issue is a separate inline comment the author must resolve before merge.

## Output Requirement (MANDATORY)

**Every review MUST follow the template**: [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md)

Submit using: [post_review.sh](.claude/skills/unity-review-pr/scripts/post_review.sh) `<pr_number> /tmp/review.json`

Read the template first, then populate all sections. No variations. No negotiation.

> [!IMPORTANT]
> **ALL reviews MUST follow [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md)**
> **Submit using [post_review.sh](.claude/skills/unity-review-pr/scripts/post_review.sh)**

## Input

**Pull Request Link**: Accepts GitHub PR URL (e.g., `https://github.com/owner/repo/pull/123`) or PR number (`#123`).

## Determining What to Review

| Input Type | Detection | Commands |
|:-----------|:----------|:---------|
| **No arguments** | Default | `git diff`, `git diff --cached`, `git status --short` |
| **Commit hash** | SHA or short hash | `git show <hash>` |
| **Branch name** | Branch identifier | `git diff <branch>...HEAD` |
| **PR URL/number** | Contains "github.com", "pull", or PR number | `gh pr view`, `gh pr diff` |

## Review Focus

### Unity-Specific Patterns (Primary)

**🔴 Critical - Flag Immediately:**
- `GetComponent` / `Camera.main` in Update/FixedUpdate loops
- `Find*` methods in runtime code
- Missing null checks after `await` (object may be destroyed)
- Events subscribed but never unsubscribed
- Coroutines not stopped on disable
- Instantiate/Destroy without pooling in hot paths

**🟡 Major - Should Fix:**
- `async void` instead of `async Task`
- Missing `[FormerlySerializedAs]` on field renames
- DOTween not killed on disable
- ScriptableObject mutation at runtime
- SerializedField visibility changes

**🔵 Minor - Consider:**
- Magic numbers (should be const or serialized)
- Debug.Log in production paths
- Empty Unity callbacks (Update, Start)

### General Code Quality

- Logic errors, off-by-one, incorrect conditionals
- Null/empty input handling
- Security issues (injection, auth bypass)
- Broken error handling
- Excessive nesting (use early returns)

## Workflow

### Phase 1: Fetch Changes

```bash
# For PR
gh pr diff <number> --patch
gh pr view <number> --json title,body,files

# For uncommitted
git diff && git diff --cached && git status --short
```

### Phase 2: Investigate Codebase

**Delegate to subagent** to understand patterns, not just diffs.

Use `@explore` or `@librarian` subagent to:
- Read full files for context
- Find callers of changed methods
- Trace event subscribers/publishers
- Check for similar patterns in codebase
- Identify breaking change impact

### Phase 2.5: Generate Acceptance Criteria

**MUST create Acceptance Criteria section** based on the PR changes to guide testing and verification.

**Analyze the PR changes and identify:**
1. What **UI screens/components** were added or modified?
2. What **logic/algorithms** were changed?
3. What **features** were added, modified, or removed?
4. What **functions/methods** have new or changed signatures?
5. What **data/serialization** formats were affected?
6. What **integrations** with external systems were touched?

**For each change, create specific, testable acceptance criteria.**

See [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md) for the **Acceptance Criteria template format**.

### Phase 3: Analyze for Unity Issues

For each change, check:
- [ ] Any Unity hot-path patterns (Update, FixedUpdate)?
- [ ] Async code with proper null checks?
- [ ] Event subscriptions balanced with unsubscribes?
- [ ] Serialization changes with migration attributes?
- [ ] Breaking API changes affecting callers?

### Phase 4: Create Review JSON

**MUST follow [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md) exactly.**

Create `/tmp/review.json`:

### Phase 5: Submit Using Script

**ALWAYS use [post_review.sh](.claude/skills/unity-review-pr/scripts/post_review.sh) to submit:**

**Script usage:**
```bash
./post_review.sh <pr_number> <review_json_file>
```

## Approval Logic

| Condition | Event |
|:----------|:------|
| Any 🔴 Critical | `REQUEST_CHANGES` |
| Only 🟡/🔵 | `COMMENT` |
| No issues | `APPROVE` |

---

## Critical Rules

> [!CAUTION]
> - **MUST follow [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md)**
> - **MUST submit using [post_review.sh](.claude/skills/unity-review-pr/scripts/post_review.sh)**
> - **Each issue MUST be a separate inline comment!**

### Always

1. ✅ Follow REVIEW_TEMPLATE.md format exactly
2. ✅ Review as expert Unity Developer - check Unity patterns first
3. ✅ Generate Acceptance Criteria based on PR changes (UI, logic, features, data)
4. ✅ Submit using `post_review.sh <PR_NUMBER> /tmp/review.json`
5. ✅ Each issue is a separate `comments` entry
6. ✅ Verify review was posted successfully
7. ✅ Submit even if PR is merged/closed

### Never

1. ❌ Deviate from REVIEW_TEMPLATE.md format
2. ❌ Skip Acceptance Criteria section
3. ❌ Combine multiple issues into one comment
4. ❌ Skip GitHub submission
5. ❌ Flag issues without investigating callers/impact
6. ❌ Miss Unity-specific patterns (Update allocations, async safety)

**Review is incomplete until each issue is a resolvable comment on GitHub.**

### Fallback for Merged/Closed PRs

```bash
gh pr comment <number> --body "## Post-Merge Review\n\n<body>"
```
