---
name: git-comment
description: "Generate comprehensive commit comments from pull requests or commit hashes. Use when analyzing code changes to produce structured documentation with High Level Summary and Specific Details sections. Triggers on: (1) PR review comment generation, (2) Commit message drafting, (3) Code change documentation, (4) Release notes generation from commits."
---

# Git Comment

Generate professional, structured commit comments by analyzing code changes from pull requests or specific commits.

## Output Requirement (MANDATORY)

**Every commit comment MUST follow the template**: [COMMIT_COMMENT.md](.claude/skills/git-comment/assets/templates/COMMIT_COMMENT.md)

Output the comment directly to the user. No file save required.

Read the template first, then populate all sections.

## Workflow

### Step 1: Identify the Input

Determine the input type:
- **Pull Request**: Use the PR number or URL
- **Commit Hash**: Use the commit SHA

### Step 2: Fetch the Changes

**For Pull Request:**
```bash
# Get PR diff
gh pr diff <pr_number> --patch > pr_changes.patch

# Get PR details
gh pr view <pr_number> --json title,body,files
```

**For Commit:**
```bash
# Get commit diff
git show <commit_hash> --stat --patch > commit_changes.patch

# Get commit message
git log -1 --format="%B" <commit_hash>
```

### Step 3: Analyze the Changes

Review the changes and identify:
1. **Files modified**: Group by category (features, bugfixes, refactoring, tests)
2. **Logic changes**: What behavior has changed
3. **Architecture impact**: How this affects the system structure
4. **Dependencies**: New imports, packages, or external dependencies

### Step 4: Generate the Comment

Produce a structured comment with two main sections:

#### Comment Structure

```markdown
## High Level Summary

[Brief 2-3 sentence overview of what this change accomplishes and why it matters]

**Type**: [Feature | Bugfix | Refactor | Chore | Test | Documentation]
**Impact**: [Low | Medium | High]
**Breaking Changes**: [Yes/No - if yes, describe]

## Specific Details

### Changes Made

- **[File/Component Name]**: [What changed and why]
- **[File/Component Name]**: [What changed and why]

### Logic Changes

- [Describe behavioral changes in plain language]
- [Focus on what the code does differently now]

### Technical Notes

- [Any important implementation details]
- [Performance considerations]
- [Dependencies added/removed]
```

### Step 5: Quality Checks

Before finalizing, verify:
- [ ] Summary accurately captures the intent
- [ ] All significant files are mentioned
- [ ] Logic changes are described in user-friendly language
- [ ] Technical details are relevant for reviewers
- [ ] Comment length is appropriate (not too verbose, not too sparse)

## Examples

### Example 1: Feature PR

**Input**: PR #1234 adding user authentication

**Output**:
```markdown
## High Level Summary

Implements OAuth2 authentication flow with Google and GitHub providers. Users can now sign in using their existing accounts, improving onboarding experience and security.

**Type**: Feature
**Impact**: High
**Breaking Changes**: No

## Specific Details

### Changes Made

- **AuthController.cs**: New controller handling OAuth callbacks and token validation
- **UserService.cs**: Extended to support external identity providers
- **appsettings.json**: Added OAuth configuration section

### Logic Changes

- Login flow now redirects to provider selection page
- Session tokens are now JWT-based with 24h expiry
- Failed login attempts trigger rate limiting after 5 tries

### Technical Notes

- Uses Microsoft.Identity.Web for token handling
- Requires CLIENT_ID and CLIENT_SECRET environment variables
- Database migration required for new OAuthProviders table
```

### Example 2: Bugfix Commit

**Input**: Commit abc123 fixing memory leak

**Output**:
```markdown
## High Level Summary

Fixes memory leak in particle system pooling that caused gradual performance degradation during extended gameplay sessions.

**Type**: Bugfix
**Impact**: Medium
**Breaking Changes**: No

## Specific Details

### Changes Made

- **ParticlePool.cs**: Added proper disposal in ReturnToPool method
- **EffectManager.cs**: Implemented IDisposable pattern

### Logic Changes

- Particle systems are now properly reset before being returned to pool
- Object references are nullified to allow garbage collection

### Technical Notes

- Memory profiling showed 15MB/hour leak is now eliminated
- Added unit tests to verify proper disposal
```

## Best Practices

1. **Be specific**: "Fixed null reference" → "Fixed NRE when user closes dialog before animation completes"
2. **Focus on why**: Explain the reasoning, not just what changed
3. **Use active voice**: "Added validation" instead of "Validation was added"
4. **Keep it scannable**: Use bullet points and short paragraphs
5. **Include context**: Mention related issues, tickets, or discussions
