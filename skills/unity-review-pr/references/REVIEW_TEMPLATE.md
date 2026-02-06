# Unity PR Review Template

This document defines the complete review format and Unity-specific review criteria. Every review MUST follow this structure.

---

## Review Output Structure

Submit **ONE GitHub review** containing:

1. **Summary Body** (`body`) - Main review comment with overview and issue counts
2. **Inline Comments** (`comments` array) - Each issue as a separate entry attached to file/line

### JSON Format

```json
{
  "body": "[SUMMARY]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    {
      "path": "Assets/Scripts/Example.cs",
      "line": 42,
      "side": "RIGHT",
      "body": "[INLINE COMMENT]"
    }
  ]
}
```

---

## Part 1: Summary Body Template

```markdown
## 🔍 Code Review - PR #[NUMBER]

**Scope**: [TICKET_ID] - [Brief description]

Overall this is [assessment]. See inline comments below for specific issues.

### ✅ Acceptance Criteria
Based on the changes in this PR, the following should be verified:

#### UI Verification
- [ ] [Specific screen/component] displays correctly
- [ ] [UI element] responds to user interaction
- [ ] [Visual element] renders correctly at different resolutions
- [ ] [Animation/transition] plays smoothly

#### Functional Verification
- [ ] [Feature/function] works as expected with valid inputs
- [ ] Edge cases handled correctly (null, empty, max values, boundary conditions)
- [ ] [System integration] communicates properly with [external system/service]
- [ ] Error handling works correctly for [specific error conditions]

#### Performance Verification
- [ ] No frame drops during [specific actions/operations]
- [ ] Memory usage remains stable during [specific gameplay scenarios]
- [ ] No GC spikes from [identified allocations]
- [ ] Load times acceptable for [specific assets/scenes]

#### Data Verification
- [ ] Existing saves/prefabs migrate correctly without data loss
- [ ] [Data structure] serializes and deserializes properly
- [ ] [ScriptableObject/Config] maintains expected values
- [ ] No breaking changes to serialized data format

### 🔴 Breaking Changes ([COUNT])
- [One-line description of each critical issue]

### 🟡 Potential Issues ([COUNT])
- [One-line description of each major issue]

### 🔵 Code Quality ([COUNT])
- [One-line description of each minor issue]

### Impact Analysis
- Files investigated: X
- Breaking call sites: Y
```

---

## Part 2: Inline Comment Templates

### 🔴 Critical Issue

```markdown
🔴 **[Issue Type]**: [Brief description]

**Impact Analysis**: [What breaks, how many affected]
- `File.cs:line` - [why it breaks]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

### 🟡 Major Issue

```markdown
🟡 **[Issue Type]**: [Brief description]

[Explain the concern and conditions]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

### 🔵 Minor Issue

```markdown
🔵 **[Issue Type]**: [Brief description]

[Brief explanation]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

---

## Unity-Specific Review Criteria

Review as an **expert Unity Developer**. Focus on these Unity-specific patterns:

### 🔴 Critical Unity Issues

| Issue | Detection | Why Critical |
|:------|:----------|:-------------|
| **GetComponent in Update/FixedUpdate** | `GetComponent<T>()` inside Update loops | Major performance hit, cache in Awake/Start |
| **Camera.main in hot paths** | `Camera.main` in Update/FixedUpdate | Calls FindGameObjectWithTag every time |
| **Find methods in runtime** | `Find()`, `FindObjectOfType()` in gameplay code | O(n) scene traversal every call |
| **Instantiate without pooling** | Frequent `Instantiate/Destroy` in gameplay | GC spikes, use object pooling |
| **String concatenation in Update** | `string + string` in hot paths | Allocates garbage every frame |
| **Missing null check after await** | `await` then use object without null check | Object may be destroyed during await |
| **Coroutine not stopped on disable** | `StartCoroutine` without tracking/stopping | Coroutine continues after object disabled |
| **Event not unsubscribed** | `+=` event without corresponding `-=` | Memory leak, callbacks on destroyed objects |

### 🟡 Major Unity Issues

| Issue | Detection | Why Major |
|:------|:----------|:----------|
| **SerializedField visibility** | `private` to `public` on serialized fields | Breaks prefab serialization |
| **Async void pitfall** | `async void` instead of `async Task` | Exceptions swallowed, can't await |
| **Missing [FormerlySerializedAs]** | Field rename without attribute | Loses serialized data on existing prefabs |
| **DOTween not killed** | `DOTween.To()` without `Kill()` on disable | Tween continues after object destroyed |
| **Unity lifecycle order** | Accessing other components in Awake | Execution order not guaranteed |
| **ScriptableObject mutation** | Modifying SO at runtime without clone | Changes persist in Editor, affects all refs |

### 🔵 Minor Unity Issues

| Issue | Detection | Why Minor |
|:------|:----------|:----------|
| **Magic numbers** | Hardcoded values like `0.5f`, `100` | Use `const` or `[SerializeField]` |
| **Debug.Log in production** | `Debug.Log` not wrapped in `#if UNITY_EDITOR` | Performance impact in builds |
| **Implicit vector operations** | `transform.position.x = 5` | Doesn't work, need temp variable |
| **Empty Unity callbacks** | Empty `Update()`, `Start()` methods | Still has overhead, remove if unused |

---

## Investigation Patterns

### Method Signature Changes

```bash
# Find all callers
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"

# Check for reflection usage
grep -rn "\"MethodName\"" Assets/Scripts/ --include="*.cs"
grep -rn "nameof(.*MethodName)" Assets/Scripts/ --include="*.cs"
```

**Report format:**
```markdown
🔴 **Breaking Change**: `ClassName.MethodName` signature changed.

**Before**: `void MethodName(int x)`
**After**: `void MethodName(Vector3 position)`

**Callers requiring update** (N found):
| File | Line | Current Call |
|:-----|:-----|:-------------|
| Foo.cs | 42 | `MethodName(1)` |
```

### Event/Delegate Changes

```bash
# Find subscribers
grep -rn "EventName\s*+=" Assets/Scripts/ --include="*.cs"
grep -rn "EventName\s*-=" Assets/Scripts/ --include="*.cs"
```

### Serialization Changes

```bash
# Find serialized references
grep -rn "TypeName" Assets/ --include="*.asset"
grep -rn "TypeName" Assets/ --include="*.prefab"
```

**Report format:**
```markdown
🟡 **Major**: Field `score` renamed to `playerScore`.

This will break serialization for existing prefabs/saves.

\`\`\`suggestion
[FormerlySerializedAs("score")]
public int playerScore;
\`\`\`
```

---

## Common Issue Types

### Critical (🔴)
- **Breaking Change**: Method/API signature changed affecting callers
- **NullReferenceException**: Code will crash on null input
- **Memory Leak**: Resources/events not properly cleaned up
- **Performance Regression**: GetComponent/Find in Update, massive allocations
- **Data Corruption**: Serialization breaks, wrong data saved/loaded
- **Race Condition**: Async code accessing destroyed objects

### Major (🟡)
- **Potential NullReferenceException**: May crash under certain conditions
- **Method Visibility Changed**: private → public affects encapsulation
- **Coupling Concern**: Cross-controller dependencies, tight coupling
- **Missing Null Check**: Defensive coding needed after async
- **Unity Lifecycle Issue**: Wrong initialization order

### Minor (🔵)
- **Naming Convention**: Doesn't follow project conventions
- **Dead Code**: Unreachable/unused code
- **Magic Number**: Hardcoded values should be constants
- **Missing Cleanup**: Empty callbacks, debug logs

---

## Complete Example

### JSON Payload

```json
{
  "body": "## 🔍 Code Review - PR #25103\n\n**Scope**: WHIP-55760 - Fix showdown hub display\n\nOverall this is a well-structured PR. See inline comments below for specific issues.\n\n### ✅ Acceptance Criteria\nBased on the changes in this PR, the following should be verified:\n\n#### UI Verification\n- [ ] Showdown hub displays active tournaments correctly\n- [ ] Tournament list filters out inactive tournaments\n- [ ] UI updates when tournament status changes\n\n#### Functional Verification\n- [ ] `GetActiveTournamentList()` returns only active tournaments with valid inputs\n- [ ] Edge cases handled correctly (null tournament list, empty list)\n- [ ] Method works correctly when called from `ShowdownHubController`\n\n#### Performance Verification\n- [ ] No frame drops when filtering tournament list\n- [ ] Memory usage stable when displaying multiple tournaments\n\n#### Data Verification\n- [ ] Tournament data structure maintains expected values\n- [ ] No breaking changes to tournament serialization\n\n### 🟡 Potential Issues (1)\n- Method visibility changed creating coupling\n\n### 🔵 Code Quality (1)\n- Potential null reference needs defensive check\n\n### Impact Analysis\n- Files investigated: 2\n- Breaking call sites: 0",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/M42/Career/CareerPvpController.cs",
      "line": 159,
      "side": "RIGHT",
      "body": "🟡 **Method Visibility Changed**: `private → public`\n\nThis method is now called from `ShowdownHubController`, creating coupling.\n\n**Concern**: `ShowdownHubController` now depends on `CareerPvpController` which may not always be instantiated.\n\n**Alternative**: Move to a static utility class to avoid cross-controller dependencies.\n\n```cs\n// In ShowdownHubUtils.cs\npublic static List<VersusTourneyItemData> GetActiveTournamentList(List<VersusTourneyItemData> items)\n{\n    // ... logic\n}\n```"
    },
    {
      "path": "Assets/Scripts/ShowdownIteration/ShowdownHubController.cs",
      "line": 77,
      "side": "RIGHT",
      "body": "🔵 **Missing Null Check After External Call**\n\n`persistentShowdownController` could be null or destroyed. Add defensive check:\n\n```suggestion\nif (persistentShowdownController != null && listTournaments != null) {\n    var activeTournaments = persistentShowdownController.GetActiveTournamentList(listTournaments);\n    // ...\n}\n```"
    }
  ]
}
```

---

## GitHub Submission

```bash
# Create JSON file with review data
cat > /tmp/review.json << 'EOF'
{
  "body": "## 🔍 Code Review...",
  "event": "REQUEST_CHANGES",
  "comments": [...]
}
EOF

# Submit via gh api
gh api \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --input /tmp/review.json
```

### Event Selection

| Condition | Event |
|:----------|:------|
| Any 🔴 Critical issues | `REQUEST_CHANGES` |
| Only 🟡/🔵 issues | `COMMENT` |
| No issues | `APPROVE` |

---

## Checklist Before Submitting

- [ ] Reviewed as expert Unity Developer
- [ ] Checked Unity-specific patterns (Update allocations, lifecycle, etc.)
- [ ] Summary body includes PR number and scope
- [ ] **Acceptance Criteria section included** with specific, actionable items
- [ ] Each issue is a separate entry in `comments` array
- [ ] Comments have correct `path`, `line`, `side: "RIGHT"`
- [ ] Investigated callers for breaking changes
- [ ] Severity levels are accurate
- [ ] Suggestions include code blocks
- [ ] Event matches severity
