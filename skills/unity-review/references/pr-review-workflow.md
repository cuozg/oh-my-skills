# PR Review Workflow

Complete end-to-end workflow for reviewing Unity GitHub pull requests.

## 1. Resolve Owner/Repo

```bash
gh repo view --json owner,name --jq '{owner: .owner.login, repo: .name}'
```

## 2. Fetch PR Metadata

```bash
# File list with patches
gh api repos/{owner}/{repo}/pulls/{pr}/files \
  --jq '.[] | {filename: .filename, status: .status, patch: .patch}'

# Raw unified diff (full context)
gh api repos/{owner}/{repo}/pulls/{pr} \
  -H "Accept: application/vnd.github.v3.diff"

# PR description and labels
gh api repos/{owner}/{repo}/pulls/{pr} \
  --jq '{title: .title, body: .body, labels: [.labels[].name], head_sha: .head.sha}'
```

**Early exits:**
- If labels contain `skip-review` or `no-review` → stop, inform user.
- If PR is draft → note in output, review anyway (feedback is valuable early).

## 3. Fetch File Content at PR Head

```bash
gh api repos/{owner}/{repo}/contents/{path}?ref={head_sha} \
  --jq '.content' | base64 -d
```

Or `git show {head_sha}:{path}` if repo is checked out locally (faster, preferred).

Always fetch **full file content** — diff hunks alone lack context for lifecycle analysis, subscribe/unsubscribe symmetry, and cross-method data flow.

## 4. Assess PR Size

Classify by counting changed C# files and changed functions to determine review depth.

| Size | C# Files Changed | Functions Changed | Review Approach |
|------|:-:|:-:|---|
| **Minor** | 1-2 | 1-5 | Single-pass (review all yourself inline) |
| **Large** | 3+ | 6+ | Deep (parallel subagents per criterion) |

Either threshold triggers Large — e.g. 1 file with 8 changed functions = Large.

**How to count:**
1. Filter PR files to `*.cs` only (ignore `.meta`, `.asset`, `.unity`, docs)
2. Count files with `status != "unchanged"`
3. For each file, count methods with any `+` or `-` lines. New = 1, deleted = 1, renamed = 2.

**Edge cases:**
- Exclude auto-generated files (`*.Designer.cs`, `*.g.cs`) from count
- Asset-only PRs (no `.cs`) = Minor
- Test-only PRs count normally toward thresholds
- When borderline → prefer Deep (over-reviewing beats missing issues)
- PRs with no description and >200 changed lines → add WARNING in review body

## 5. Classify Files and Route to Specialists

Spawn specialist reviews in parallel based on file types present. See `pr-specialist-reviews.md` for detailed routing.

| File Type | Specialist |
|-----------|-----------|
| `.cs` | Code review (Minor → single-pass, Large → parallel subagents) |
| `.prefab`, `.unity` | Prefab/scene review (one subagent per file) |
| `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` | Asset review |
| `.cs` with new systems/services/managers, `.asmdef` | Architecture review |

For Minor PRs, review all `.cs` files in a single pass loading all 6 checklist sections from `unity-standards/references/review/checklist.md`.

For Large PRs, spawn 6 parallel subagents (one per criterion) per `unity-standards/references/review/parallel-review-criteria.md`.

## 6. Aggregate Findings

1. Collect all findings arrays from specialist reviews
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file path → line number
4. Map to right-side file line numbers (not diff position): `line` = actual line in file at HEAD, `side` always `RIGHT`

## 7. Check for Prior Reviews

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --jq '[.[] | select(.user.type != "Bot" or .user.login == "<your-bot>") | {id, user: .user.login, state, submitted_at}]'
```

- If a previous review from the same bot exists → acknowledge it, don't re-flag identical issues
- If the PR author has responded to prior comments → note addressed items

## 8. Make Final Decision

**REQUEST_CHANGES** if ANY of:
- Unresolved CRITICAL issues exist
- Hardcoded API keys or passwords found
- Missing null check on deserialized data touching gameplay state
- Security vulnerabilities that could lead to data exposure

**APPROVE** if:
- No CRITICAL issues
- All HIGH issues have suggestion blocks with fixes
- No security blockers

**COMMENT** if:
- Only MEDIUM/LOW/STYLE findings (informational, non-blocking)

## 9. Build Review Body

```
## Code Review — PR #{number}
{1-2 sentence verdict}

| | Category | Findings | Top Severity |
|---|---|:---:|---|
| 💥 | Breaking / Crash Risk | {n} | 🔴 CRITICAL |
| ⚠️ | Bugs / Incorrect Behavior | {n} | 🟠 HIGH |
| 🎮 | Unity-Specific Risks | {n} | 🟡 MEDIUM |
| 💡 | Improvements | {n} | 🔵 LOW / ⚪ STYLE |

**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT
```

Rules:
- State decision as first word of body: "APPROVE", "REQUEST_CHANGES", or "COMMENT"
- Summarize specialist findings before decision
- If prior reviews exist, acknowledge them
- Include both inline comments (from specialists) and body (from decision) in a single submission

## 10. Submit Review

Build `review.json` per `unity-standards/references/review/pr-submission.md`:

```json
{
  "event": "REQUEST_CHANGES",
  "body": "{review body from step 9}",
  "comments": [
    {
      "path": "Assets/Scripts/Player.cs",
      "line": 42,
      "side": "RIGHT",
      "body": "**🔴 Issue Title** — `CRITICAL`\n\n{what + why}\n\n```suggestion\n{fix}\n```"
    }
  ]
}
```

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json
```

Suggestion blocks required for MEDIUM+ severity findings.

## 11. Verify Submission

**Mandatory — never skip:**

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --jq '.[-1] | {id, state, submitted_at}'
```

If `id` is absent or command errors → fix the root cause and re-run step 10. Loop until confirmed.

## Error Handling

| Error | Recovery |
|-------|----------|
| `gh api` 404 | Verify owner/repo/PR number. Check if PR is in a fork (use fork's owner). |
| `gh api` 403 | Token lacks repo scope. Instruct user: `gh auth refresh -s repo` |
| `gh api` 422 on review POST | Payload too large (>32KB per comment) → split long comments. Or stale `commit_id` → re-fetch HEAD SHA. |
| Rate limit (403 + `X-RateLimit-Remaining: 0`) | Wait for reset. Log: "GitHub rate limit hit, retry after {reset_time}." |
| Empty diff / no files | PR may be a draft with no commits yet → inform user, skip review. |
| 100+ files in PR | Prioritize `.cs` files. Warn user that asset/config files were sampled, not exhaustively reviewed. |

## Notes

- Always use `event: "APPROVE"`, `"REQUEST_CHANGES"`, or `"COMMENT"` — never other values
- One final review submission per run — do not call the reviews API twice
- Never post individual line comments from the decision step — use body only; inline comments go in the `comments` array
- Rate limit: 5000 authenticated requests/hour
