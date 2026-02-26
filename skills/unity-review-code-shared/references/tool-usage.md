# Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |
| Feature/logic request | Find relevant files via grep/LSP |

## Severity

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |
