# Task Detail: [Task ID] - [Task Name]

> ⚠️ **REVIEW-ONLY** — This document contains proposed changes as diffs. No code has been modified. Approve before passing to an executor skill.

## Review Status

- [ ] Code changes reviewed
- [ ] Risks acknowledged
- [ ] Test cases validated
- [ ] **Approved for execution**

**Reviewer**: _[Name/Date]_

---

## 1. Requirement & Investigation

- **Source Plan**: [Link to original plan]
- **Epic**: [Epic name/number]
- **Code Investigation Summary**:
  - Relevant files: `path/to/file.cs`
  - Current execution flow: [Description]
  - Dependencies: [List of components involved]

## 2. Implementation Strategy

- **Overview**: High-level explanation of the approach.
- **Steps**:
  1. [Step 1]
  2. [Step 2]

## 3. Code Changes (Unified Diff Format)

> All changes use unified diff format (the GitHub standard). See [diff-format-guide.md](../../references/diff-format-guide.md) for full conventions and examples. Always use this exact format for all code changes.

### 3.1 `Assets/Scripts/Path/To/File.cs`

**Purpose**: [What this change accomplishes]

```diff
--- a/Assets/Scripts/Path/To/File.cs
+++ b/Assets/Scripts/Path/To/File.cs
@@ -8,7 +8,8 @@ public class PlayerStats : MonoBehaviour
     [SerializeField] private int _health = 100;
     [SerializeField] private float _moveSpeed = 5f;
 
-    public void Initialize()
+    public void Initialize(int shield = 0)
     {
         _health = 100;
+        _shield = shield;
     }
```

_Add more diff sections (3.2, 3.3, …) as needed. All use the same unified diff format._

## 4. New Files

> List any files created from scratch. Provide full content in a fenced code block with the language tag.

### 4.1 `Assets/Scripts/Path/To/NewFile.cs` _(new)_

```csharp
// Full file content here
```

_Omit this section if no new files are needed._

## 5. Potential Risks & Brainstorming

- **Unclear Points**: [Items to clarify with user]
- **Architectural Impact**: [Possible side effects]
- **Breaking Changes**: [Any API or behavior changes]

## 6. Test Cases

- **Case 1: [Name]**
  - **Prerequisites**: [Setup needed]
  - **Action**: [What to do]
  - **Expected Result**: [Success criteria]
- **Case 2: [Name]**
  - …

## 7. Definition of Done

- [ ] All diffs approved by reviewer
- [ ] Code applied by executor skill
- [ ] Compiles without errors
- [ ] Passes all test cases
- [ ] Documentation updated (if applicable)
