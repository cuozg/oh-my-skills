---
name: unity-review-pr
description: "Deep-investigation PR reviews for Unity projects. Analyzes not just code changes but their IMPACT on the entire codebase. Use when: (1) Reviewing PRs with logic changes that may break dependent systems, (2) Identifying cascading effects from API/interface changes, (3) Finding hidden coupling issues, (4) Verifying changes don't break callers/consumers. Triggers: 'review PR', 'check this PR', 'PR #123', any GitHub PR link."
---

# Unity PR Reviewer (Deep Investigation)

Review PRs by analyzing both the changes AND their impact on the codebase.

> [!CAUTION]
> **MANDATORY**: Every review MUST be pushed to GitHub using `gh` CLI. A review is NOT complete until the `gh pr review` command has been executed successfully.

## Core Philosophy

**Surface reviews miss breaking changes.** A PR that changes method signature, event behavior, or data flow can break dozens of callers. This skill investigates the ripple effects.

## Severity Levels

| Level | Use When |
|:------|:---------|
| 🔴 **Critical** | Breaking changes to callers, memory leaks, crashes, data corruption |
| 🟡 **Major** | Hidden coupling issues, missing null checks, `GetComponent` in Update |
| 🔵 **Minor** | Naming inconsistencies, style violations |
| 💚 **Suggestion** | Readability improvements, modern C# patterns |

## Review Workflow

### Phase 1: Fetch & Parse

```bash
# Get PR diff
gh pr diff <number> --patch > pr_diff.patch

# Get PR info (files changed, description)
gh pr view <number> --json title,body,files
```

### Phase 2: Identify High-Risk Changes

Scan the diff for these risk indicators:

| Change Type | Risk | Investigation Required |
|:------------|:-----|:-----------------------|
| Method signature change | 🔴 | Find ALL callers via LSP/grep |
| Public field/property removed | 🔴 | Find ALL references |
| Event signature change | 🔴 | Find ALL subscribers |
| Interface method change | 🔴 | Find ALL implementations |
| Virtual method override | 🟡 | Check base class contract |
| ScriptableObject field change | 🟡 | Check serialized assets |
| Enum value added/removed | 🟡 | Find switch statements |
| Constructor parameter change | 🔴 | Find ALL instantiation sites |

### Phase 3: Deep Investigation

For EACH high-risk change, investigate the codebase:

```bash
# Find all callers of changed method
# Use LSP references or grep patterns

# Example: Method "ProcessReward" changed signature
grep -r "ProcessReward" Assets/Scripts/ --include="*.cs"

# Example: Event "OnMatchComplete" parameters changed  
grep -r "OnMatchComplete" Assets/Scripts/ --include="*.cs"

# Example: Interface IRewardHandler method changed
grep -r "IRewardHandler" Assets/Scripts/ --include="*.cs"
```

**For each caller found:**
1. Read the calling code
2. Check if the call is still compatible
3. If NOT compatible → 🔴 Critical issue

### Phase 4: Logic Flow Analysis

Trace the execution path of changed code:

1. **Entry points**: What triggers this code? (UI, events, lifecycle)
2. **Dependencies**: What does this code depend on? (services, data)
3. **Side effects**: What does this code modify? (state, events, external)
4. **Exit points**: What consumes the output? (return values, out params)

Flag issues when:
- Changed logic breaks expected behavior of callers
- New null paths introduced without null checks downstream
- Event timing changes affect subscribers
- Data format changes break consumers

### Phase 5: Pattern Audit

Check changed files against Unity patterns:

```csharp
// 🔴 GetComponent in Update
void Update() { GetComponent<Rigidbody>(); }

// 🔴 Camera.main in loop  
void Update() { Camera.main.transform; }

// 🟡 String concat in hot path
void Update() { label.text = "Score: " + score; }

// 🔴 Missing null check after await
async Awaitable DoAsync() {
    await Awaitable.WaitForSecondsAsync(1f);
    transform.position = Vector3.zero; // May be destroyed!
}

// 🔴 Breaking change without updating callers
public void OldMethod(int x) { }  // Changed from (int x, int y)
```

### Phase 6: Draft Review

Structure findings in categories:

```markdown
## 🔴 Breaking Changes (X issues)
[List changes that WILL break existing code]

## 🟡 Potential Issues (Y issues)  
[List changes that MAY cause problems]

## 🔵 Code Quality (Z issues)
[Style, naming, minor improvements]

## 💚 Suggestions
[Nice-to-haves]
```

### Phase 7: Submit (MANDATORY)

> [!IMPORTANT]
> This phase is **NOT OPTIONAL**. You MUST push the review to GitHub.

**Option A: Using the helper script**
```bash
bash .claude/skills/unity-review-pr/scripts/post_review.sh <number> review.json
```

**Option B: Direct gh command**
```bash
# For APPROVE
gh pr review <number> --approve --body "<review_body>"

# For REQUEST_CHANGES
gh pr review <number> --request-changes --body "<review_body>"

# For COMMENT only
gh pr review <number> --comment --body "<review_body>"
```

**Verification**: After submitting, confirm the review was posted:
```bash
gh pr view <number> --json reviews --jq '.reviews[-1]'
```

## Comment Format

Include impact analysis in critical findings:

```markdown
🔴 **Critical**: Method signature changed from `ProcessReward(int amount)` to `ProcessReward(RewardData data)`.

**Impact Analysis**: Found 12 callers that will break:
- `RewardManager.cs:45` - Direct call
- `QuestSystem.cs:123` - Event handler
- `DailyBonus.cs:67` - Coroutine call
[...]

\`\`\`suggestion
// Consider: Add overload for backward compatibility
public void ProcessReward(int amount) => ProcessReward(new RewardData { Amount = amount });
\`\`\`
```

## Approval Logic

| Condition | Event |
|:----------|:------|
| No 🔴 or 🟡 issues | APPROVE |
| Only 🔵/💚 issues | COMMENT |
| Any 🔴 issues | REQUEST_CHANGES |

## Investigation Tools

Use these in order of preference:

1. **LSP find references** - Most accurate for symbol usage
2. **AST grep** - Pattern-based code search
3. **Text grep** - Fallback for string matching

See [DEEP_INVESTIGATION.md](references/DEEP_INVESTIGATION.md) for investigation patterns.
See [REVIEW_JSON_SPEC.md](references/REVIEW_JSON_SPEC.md) for output format.

---

## Critical Rules

> [!CAUTION]
> **NEVER skip the GitHub submission step!**

1. ✅ **ALWAYS** push review to GitHub using `gh pr review`
2. ✅ **ALWAYS** verify the review was posted successfully
3. ❌ **NEVER** consider a review complete without GitHub submission
4. ❌ **NEVER** just output review text without pushing to GitHub

**The review workflow is incomplete until the `gh pr review` command returns success.**
