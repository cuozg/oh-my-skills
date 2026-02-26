# Input → Command

| Input | Command |
|:------|:--------|
| None | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |

## Severity

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.
