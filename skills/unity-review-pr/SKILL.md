---
name: unity-review-pr
description: "Code reviewer for Unity C# projects. Reviews code changes (uncommitted, commits, branches, or PRs) and provides actionable feedback focused on bugs, structure, and performance. Use when: reviewing PRs, checking uncommitted changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', any GitHub PR link, commit hash, branch name."
---

# Unity Code Reviewer

Review code changes and provide actionable feedback.

## Determining What to Review

Based on input, determine which review type to perform:

| Input Type | Detection | Commands |
|:-----------|:----------|:---------|
| **No arguments** | Default | `git diff` (unstaged), `git diff --cached` (staged), `git status --short` (untracked) |
| **Commit hash** | 40-char SHA or short hash | `git show <hash>` |
| **Branch name** | Branch identifier | `git diff <branch>...HEAD` |
| **PR URL/number** | Contains "github.com", "pull", or looks like PR number | `gh pr view <input>`, `gh pr diff <input>` |

## Gathering Context

**Diffs alone are not enough.** After getting the diff:

1. Identify which files changed from the diff
2. Use `git status --short` to find untracked files, read their full contents
3. Read full file(s) to understand existing patterns, control flow, error handling
4. Check for conventions files (CONVENTIONS.md, AGENTS.md, .editorconfig)

Code that looks wrong in isolation may be correct given surrounding logic—and vice versa.

## PR Description Requirements

**Every PR description MUST contain two mandatory sections.** Check these first before reviewing code.

### Required Sections

| Section | Purpose | Status if Missing |
|:--------|:--------|:------------------|
| **## High Level Summary** | Brief overview of what the PR accomplishes and why | 🔴 **Must update** |
| **## Specific details of the changes made** | Detailed breakdown of what changed in each file/component | 🔴 **Must update** |

### Validation Workflow

1. **Fetch PR description:**
   ```bash
   gh pr view <number> --json body --jq '.body'
   ```

2. **Check for required sections:**
   - Look for `## High Level Summary` or similar heading
   - Look for `## Specific details` or similar heading

3. **If either section is missing or empty:**
   - Add to review as 🔴 **Critical** issue
   - Mark as **Must update** before code review can be approved
   - Include template for the author to fill in

### Missing Section Template

If sections are missing, include this in your review:

```markdown
🔴 **Critical**: PR description is incomplete.

The following required sections are missing or empty:

- [ ] **## High Level Summary** - [MISSING/EMPTY - Must update]
  > Provide a brief 2-3 sentence overview of what this PR accomplishes and why it matters.

- [ ] **## Specific details of the changes made** - [MISSING/EMPTY - Must update]
  > List each file/component changed and describe what was modified and why.

**Action Required**: Please update the PR description with the missing sections before this PR can be approved.
```

### Valid Description Example

```markdown
## High Level Summary

This PR adds OAuth2 authentication support using Google and GitHub providers.
Users can now sign in with their existing accounts, improving security and
reducing friction during onboarding.

## Specific details of the changes made

### AuthController.cs
- Added `HandleOAuthCallback()` method for processing provider responses
- Implemented token validation using Microsoft.Identity.Web

### UserService.cs
- Extended `CreateUser()` to accept external identity provider data
- Added `LinkExternalAccount()` for connecting existing accounts

### appsettings.json
- Added OAuth configuration section with client ID placeholders
```

### Approval Impact

| Description Status | Review Action |
|:-------------------|:--------------|
| Both sections present and complete | Continue with code review |
| Either section missing | REQUEST_CHANGES immediately |
| Sections present but empty/placeholder | REQUEST_CHANGES immediately |

> [!IMPORTANT]
> A PR cannot be approved if either **High Level Summary** or **Specific details of the changes made** is missing or incomplete. This is non-negotiable.

## What to Look For

### Bugs (Primary Focus)

- Logic errors, off-by-one mistakes, incorrect conditionals
- If-else guards: missing guards, incorrect branching, unreachable code paths
- Edge cases: null/empty/undefined inputs, error conditions, race conditions
- Security issues: injection, auth bypass, data exposure
- Broken error handling that swallows failures or throws unexpectedly

### Structure

- Does it follow existing patterns and conventions?
- Are there established abstractions it should use but doesn't?
- Excessive nesting that could be flattened with early returns

### Performance (Only Flag If Obviously Problematic)

- O(n²) on unbounded data
- N+1 queries
- Blocking I/O on hot paths
- `GetComponent` in Update loops
- `Camera.main` in hot paths

## Before You Flag Something

**Be certain.** If you call something a bug, be confident it actually is one.

- Only review the changes - do NOT review pre-existing code that wasn't modified
- Don't flag something as a bug if you're unsure - investigate first
- Don't invent hypothetical problems - if an edge case matters, explain the realistic scenario where it breaks
- If uncertain and can't verify with tools, say "I'm not sure about X" rather than flagging as definite

**Don't be a zealot about style:**

- Verify code is *actually* in violation before complaining
- Some "violations" are acceptable when they're the simplest option
- Excessive nesting is a legitimate concern regardless of other style choices
- Only flag style preferences if they clearly violate established project conventions

## Investigation Tools

Use these to inform your review:

1. **Codebase search** - Find how existing code handles similar problems
2. **Web search** - Research best practices if unsure about a pattern
3. **grep/find** - Locate references, patterns, and prior art

## Severity Levels

| Level | Use When |
|:------|:---------|
| 🔴 **Critical** | Breaking changes, memory leaks, crashes, data corruption |
| 🟡 **Major** | Hidden coupling, missing null checks, performance issues |
| 🔵 **Minor** | Naming inconsistencies, style violations |
| 💚 **Suggestion** | Readability improvements, modern C# patterns |

## Review Workflow

### Phase 0: Validate PR Description (For PRs Only)

**Before reviewing code, check the PR description for required sections.**

```bash
# Fetch PR description
gh pr view <number> --json body --jq '.body'
```

Check for:
- [ ] `## High Level Summary` - Present and contains meaningful content
- [ ] `## Specific details of the changes made` - Present and contains meaningful content

**If either is missing or empty:** Note it as a 🔴 Critical issue to include in the final review. **Continue with the full code review** - do not stop here.

**Proceed to Phase 1 regardless of description status.** The missing description issue will be included when submitting the review to GitHub.

### Phase 1: Fetch Changes

```bash
# For PR
gh pr diff <number> --patch > pr_diff.patch
gh pr view <number> --json title,body,files

# For uncommitted
git diff
git diff --cached
git status --short
```

### Phase 2: Read Full Context

For each modified file:
```bash
# Read full file to understand context
cat <filepath>

# Or view specific sections if file is large
```

### Phase 3: Analyze Changes

1. **Identify high-risk changes**: signature changes, removed fields, interface changes
2. **Trace impact**: Find all callers/consumers of changed code
3. **Verify correctness**: Check if changes break callers

```bash
# Find callers of changed method
grep -r "MethodName" Assets/Scripts/ --include="*.cs"
```

### Phase 4: Draft Review

Structure findings clearly:

```markdown
## Summary
[One-line summary of review outcome]

## 🔴 Critical (X issues)
[Issues that WILL break existing code or cause serious problems]

## 🟡 Major (Y issues)
[Issues that MAY cause problems under specific conditions]

## 🔵 Minor (Z issues)
[Style, naming, minor improvements]

## 💚 Suggestions
[Nice-to-haves, not blocking]
```

### Phase 5: Submit to GitHub

```bash
# For APPROVE (no critical/major issues)
gh pr review <number> --approve --body "<review_body>"

# For REQUEST_CHANGES (has critical issues)
gh pr review <number> --request-changes --body "<review_body>"

# For COMMENT only (minor issues or suggestions)
gh pr review <number> --comment --body "<review_body>"

# For merged/closed PRs - post as comment
gh pr comment <number> --body "## Post-Merge Review\n\n<review_body>"
```

## Output Guidelines

1. **Be direct** about bugs - explain clearly why it's a bug
2. **Communicate severity** - don't overstate
3. **Specify conditions** - state scenarios/inputs where bug arises
4. **Keep tone matter-of-fact** - not accusatory or overly positive
5. **Be scannable** - reader should quickly understand without reading closely
6. **No flattery** - avoid "Great job", "Thanks for" phrasing

### Comment Format

```markdown
🔴 **Critical**: Method signature changed from `ProcessReward(int amount)` to `ProcessReward(RewardData data)`.

**Impact**: Found 12 callers that need updating:
- `RewardManager.cs:45`
- `QuestSystem.cs:123`

**Condition**: All direct callers will fail to compile.

\`\`\`suggestion
// Add overload for backward compatibility
public void ProcessReward(int amount) => ProcessReward(new RewardData { Amount = amount });
\`\`\`
```

## Approval Logic

| Condition | Action |
|:----------|:-------|
| No 🔴 or 🟡 issues | APPROVE |
| Only 🔵/💚 issues | COMMENT |
| Any 🔴 issues | REQUEST_CHANGES |

---

See [DEEP_INVESTIGATION.md](references/DEEP_INVESTIGATION.md) for investigation patterns.
See [REVIEW_JSON_SPEC.md](references/REVIEW_JSON_SPEC.md) for output format.

---

## Critical Rules

> [!CAUTION]
> **NEVER skip the GitHub submission step!**

1. ✅ **ALWAYS** push review to GitHub using `gh pr review` or `gh pr comment`
2. ✅ **ALWAYS** push even if PR is **merged** or **closed**
3. ✅ **ALWAYS** verify the review was posted successfully
4. ❌ **NEVER** consider a review complete without GitHub submission
5. ❌ **NEVER** just output review text without pushing to GitHub
6. ❌ **NEVER** skip submission because "PR is already merged"

**The review workflow is incomplete until the review is visible on GitHub.**

### Handling Merged/Closed PRs

If `gh pr review` fails because PR is merged/closed:

```bash
# Fallback: Post as comment instead
gh pr comment <number> --body "## Post-Merge Review\n\n<review_body>"
```

The goal is to ensure the review is **recorded on GitHub** for documentation purposes, regardless of PR state.
