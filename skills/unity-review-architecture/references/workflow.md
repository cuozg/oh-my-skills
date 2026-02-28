# Architecture Review Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.cs` files. If none found, APPROVE with note `No C# files to review for architecture.`

### 2. Load Architecture Standards

```python
use_skill("unity-shared")  # Load authoritative architecture patterns
```

### 3. Deep Investigate (Parallel)

Spawn 2-3 `@explore` agents to trace: dependency injection usage, event subscriptions, assembly references, cross-system calls.

### 4. Architecture Review

For each changed `.cs` file, read the ENTIRE file (not just diff). Apply patterns from [ARCHITECTURE_PATTERNS.md](ARCHITECTURE_PATTERNS.md). Check for new circular dependencies introduced by the PR. Architecture issues that are pre-existing should only be flagged if the PR makes them worse.

### 5. Build `/tmp/review-architecture.json`

```json
{
  "body": "## Architecture Review\n**Scope**: [N files reviewed]\n...",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/Services/MatchService.cs",
      "line": 15,
      "side": "RIGHT",
      "body": "**🔴 Manual Instantiation of Injected Service**: `new LobbyService()` bypasses DI.\n- **Why**: Dependencies won't be resolved; class becomes untestable.\n- **Fix**:\n```suggestion\nprivate readonly ILobbyService _lobbyService;\npublic MatchService(ILobbyService lobbyService) { _lobbyService = lobbyService; }\n```"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Always set `event` to `"COMMENT"`.

### 6. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-architecture.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.
