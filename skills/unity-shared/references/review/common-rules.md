# Common Code Review Rules

Rules shared by `unity-review-code-pr` and `unity-review-code-local`.

## Input → Diff Command

| Input | Command |
| :------ | :--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |
| Feature/logic request | Find relevant files via grep/LSP |

## Severity

| Severity | Emoji | Meaning |
| :---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |

## Evidence & Investigation

- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
- One issue = one comment (severity + evidence + suggestion/fix description).
- Same issue in N files → full explanation on first occurrence, short reference on rest (batch pattern).

## File Reading

- Only review `.cs` files. Read **full files**, not just diffs. Logic bugs hide in surrounding context.
- Trace data flow end-to-end. Verify lifecycle ordering.

## Unity-Specific

- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.

## Fix Delegation

- Delegate code fixes to `unity-code-quick` via `task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)`.
- Include in delegation prompt: file path, line number, the review comment, and the exact fix to apply.
- One task per fix or per file. Multiple fixes → multiple parallel background tasks.

## Severity Usage

- Severity labels are for categorization only.
- This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.
