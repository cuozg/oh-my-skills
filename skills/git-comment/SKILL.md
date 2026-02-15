---
name: git-comment
description: "Generate comprehensive commit comments from pull requests or commit hashes. Use when analyzing code changes to produce structured documentation with High Level Summary and Specific Details sections. Triggers on: (1) PR review comment generation, (2) Commit message drafting, (3) Code change documentation, (4) Release notes generation from commits."
---

# Git Comment

## Input/Output

**Input**: PR number/URL or commit SHA. Optional: repo path, output format.
**Output**: Structured comment per [COMMIT_COMMENT.md](.opencode/skills/git/git-comment/assets/templates/COMMIT_COMMENT.md) — output directly to user.

## Workflow

1. **Fetch changes**:
   - PR: `gh pr diff <pr> --patch` + `gh pr view <pr> --json title,body,files`
   - Commit: `git show <hash> --stat --patch` + `git log -1 --format="%B" <hash>`
2. **Analyze**: Group files by category, identify logic/behavior changes, architecture impact, dependencies
3. **Generate comment** using template structure:
   ```markdown
   ## High Level Summary
   {2-3 sentence overview}
   **Type**: {Feature|Bugfix|Refactor|Chore|Test|Documentation}
   **Impact**: {Low|Medium|High}
   **Breaking Changes**: {Yes/No}

   ## Specific Details
   ### Changes Made
   - **{File}**: {What and why}
   ### Logic Changes
   - {Behavioral changes}
   ### Technical Notes
   - {Implementation details, perf, deps}
   ```
4. **Verify**: Summary captures intent, all significant files mentioned, logic described clearly

## Example

**Input**: PR #1234 (OAuth2 auth)

```markdown
## High Level Summary
Implements OAuth2 authentication with Google/GitHub providers, improving onboarding and security.
**Type**: Feature | **Impact**: High | **Breaking Changes**: No

## Specific Details
### Changes Made
- **AuthController.cs**: OAuth callbacks and token validation
- **UserService.cs**: External identity provider support
### Logic Changes
- Login redirects to provider selection; JWT tokens with 24h expiry
### Technical Notes
- Uses Microsoft.Identity.Web; requires CLIENT_ID/CLIENT_SECRET env vars
- DB migration needed for OAuthProviders table
```

## Best Practices

- Be specific: "Fixed NRE when user closes dialog before animation completes" not "Fixed null reference"
- Focus on **why**, use active voice, keep scannable with bullets
