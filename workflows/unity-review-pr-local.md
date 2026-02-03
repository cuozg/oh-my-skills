---
description: Local PR reviews for Unity projects without GitHub posting. Use when reviewing code changes locally and generating a markdown review file.
---

# Unity Local PR Review Workflow

// turbo-all

## Steps

### 1. Read the skill instructions
```
view_file .agent/skills/unity-review-pr-local/SKILL.md
```

### 2. Get the PR number or branch
Ask the user for the PR number or branch name to review.

### 3. Fetch the diff
For PR:
```bash
gh pr diff --patch <number> > /tmp/pr_diff.patch
```
For local branch:
```bash
git diff main...HEAD > /tmp/pr_diff.patch
```

### 4. Analyze the diff
- Check against coding conventions in `.claude/rules/`
- Flag architectural issues, performance patterns, memory concerns
- Categorize findings by severity (🔴 Critical, 🟡 Major, 🔵 Minor, 💚 Suggestion)

### 5. Generate the review markdown
Create the review file at `Documents/Reviews/PR_<number>_review.md` using the template from `references/OUTPUT_TEMPLATE.md`.

### 6. Notify user
Provide a summary and the path to the generated review file.