---
name: unity-review-architecture
description: "Review Unity project architecture in GitHub PRs — dependency management, event systems, assembly structure, cross-system coupling, and architectural pattern compliance. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing architecture in PRs, validating dependency/coupling changes before merge. Triggers: 'review architecture', 'architecture review', 'DI review', 'coupling review', 'PR architecture review', 'review PR architecture'."
---

# Architecture PR Reviewer

Review architecture patterns across PR changes in `.cs` files. Push review comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers dependency management, event systems, assembly structure, cross-system coupling.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity Labels

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Breaks functionality, data loss, crashes |
| HIGH | 🟡 | Performance, UX, or logic issues |
| MEDIUM | 🔵 | Style, maintainability, minor UX |
| LOW | 🟢 | Naming, conventions, suggestions |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Key Concern Areas

| Area | What to Check |
|:-----|:-------------|
| Dependency Management | Proper DI, no service locators, no `FindObjectOfType` for service resolution |
| Event Architecture | Subscribe/unsubscribe pairing, no direct coupling via events |
| Assembly Structure | No circular dependencies, correct `.asmdef` references |
| Cross-system Coupling | Services don't reference MonoBehaviours directly, proper abstractions |
| Data Flow | Interface-based data access, no direct field mutation across systems |

## Workflow

Follow the 6-step workflow: Fetch PR → Load Standards → Investigate → Review → Build JSON → Submit.
Read [workflow.md](references/workflow.md) before starting any review.

## Rules

- Only review `.cs` files for architecture concerns. Read full files, not just diffs.
- One issue = one comment. Every comment needs severity + evidence + suggestion.
- Always load `unity-code-shared` for authoritative architecture patterns.
- Pre-existing issues: only flag if the PR makes them worse.
- Batch pattern: full explanation on first occurrence, short reference on subsequent. Submit even if PR is merged.
- Never hardcode `commit_id` or modify source files.

## Reference Files
- [workflow.md](references/workflow.md) — 6-step review workflow with JSON format and submit commands
- [ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md) — Complete architecture pattern catalog
