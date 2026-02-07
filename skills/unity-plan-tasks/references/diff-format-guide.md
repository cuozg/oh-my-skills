# Diff Format Guide

All code changes use **unified diff format** — the standard GitHub diff format. One consistent format for every change.

## Table of Contents

- [Unified Diff Syntax Explained](#unified-diff-syntax-explained)
- [Format Structure](#format-structure)
- [Examples](#examples)
- [New Files](#new-files)
- [Deleted Files](#deleted-files)
- [Common Patterns](#common-patterns)
- [Common Mistakes](#common-mistakes)

---

## Unified Diff Syntax Explained

A unified diff has three parts: **file header**, **hunk header**, and **change lines**.

```
--- a/Assets/Scripts/Player.cs          ← File being modified (original)
+++ b/Assets/Scripts/Player.cs          ← File being modified (new version)
@@ -8,7 +8,8 @@ public class Player                ← Hunk header: location of change
     [SerializeField] private int _hp;  ← Context line (unchanged, space prefix)
     private float _speed = 5f;         ← Context line (unchanged, space prefix)
 
-    public void TakeDamage(int dmg)     ← Removed line (- prefix)
+    public void TakeDamage(int dmg,     ← Added line (+ prefix)
+        bool isCrit = false)            ← Added line (+ prefix)
     {
         _hp -= dmg;                     ← Context line (unchanged, space prefix)
     }
```

**Line-by-line breakdown:**

| Line prefix | Meaning |
|-------------|---------|
| `--- a/...` | Original file path |
| `+++ b/...` | Modified file path |
| `@@ -old,count +new,count @@` | Hunk header: starting line and line count in old/new file |
| ` ` (space) | Context line — unchanged, shown for placement |
| `-` | Removed line — exists in original, deleted in new |
| `+` | Added line — does not exist in original, added in new |

**Hunk header format**: `@@ -8,7 +8,8 @@` means: starting at line 8, show 7 lines from old file and 8 lines from new file. Optional text after `@@` shows the enclosing scope (class/method name).

---

## Format Structure

Every diff block follows this layout:

````markdown
### 3.X `Assets/Scripts/Path/To/File.cs`

**Purpose**: [Why this change is needed]

```diff
--- a/Assets/Scripts/Path/To/File.cs
+++ b/Assets/Scripts/Path/To/File.cs
@@ -line,count +line,count @@ optional scope context
 context line (3-5 lines around changes)
-removed line
+added line
 context line
```
````

### Rules

- One diff block per file — never mix files in a single block
- Always include file header (`--- a/...` and `+++ b/...`)
- Always include hunk header (`@@ ... @@`)
- Include 3-5 context lines around changes so placement is unambiguous
- Preserve original indentation exactly (spaces vs tabs)
- Add a **Purpose** line above each diff block
- Use `diff` language tag on the fenced code block for syntax highlighting

---

## Examples

### Example 1: C# Simple 1-Line Property Change

**Purpose**: Add dash speed field to player controller

```diff
--- a/Assets/Scripts/PlayerController.cs
+++ b/Assets/Scripts/PlayerController.cs
@@ -5,6 +5,7 @@ public class PlayerController : MonoBehaviour
 {
     [SerializeField] private float _moveSpeed = 5f;
+    [SerializeField] private float _dashSpeed = 12f;
 
     private void Update()
     {
```

### Example 2: C# Method Refactoring (Multi-Line)

**Purpose**: Cache Rigidbody reference and extract jump force to serialized field

```diff
--- a/Assets/Scripts/PlayerController.cs
+++ b/Assets/Scripts/PlayerController.cs
@@ -3,28 +3,34 @@
 public class PlayerController : MonoBehaviour
 {
     [SerializeField] private float _moveSpeed = 5f;
-    private bool _isJumping;
+    [SerializeField] private float _jumpForce = 5f;
+
+    private Rigidbody _rb;
+
+    private void Awake()
+    {
+        _rb = GetComponent<Rigidbody>();
+    }
 
     private void Update()
     {
         float h = Input.GetAxis("Horizontal");
         float v = Input.GetAxis("Vertical");
-        transform.Translate(new Vector3(h, 0, v)
-            * _moveSpeed * Time.deltaTime);
+        var dir = new Vector3(h, 0, v);
+        transform.Translate(dir * _moveSpeed * Time.deltaTime);
 
         if (Input.GetKeyDown(KeyCode.Space))
             Jump();
     }
 
     private void Jump()
     {
-        _isJumping = true;
-        GetComponent<Rigidbody>().AddForce(
-            Vector3.up * 5f, ForceMode.Impulse);
+        _rb.AddForce(Vector3.up * _jumpForce, ForceMode.Impulse);
     }
 }
```

### Example 3: JSON Configuration File

**Purpose**: Add failover region to server configuration

```diff
--- a/Assets/Resources/server_config.json
+++ b/Assets/Resources/server_config.json
@@ -1,6 +1,14 @@
 {
-    "serverUrl": "https://us-east.example.com",
-    "cdnUrl": "https://cdn.example.com",
+    "regions": {
+        "primary": {
+            "serverUrl": "https://us-east.example.com",
+            "cdnUrl": "https://cdn-east.example.com"
+        },
+        "fallback": {
+            "serverUrl": "https://eu-west.example.com",
+            "cdnUrl": "https://cdn-west.example.com"
+        }
+    },
     "maxRetries": 3,
-    "timeout": 30
+    "timeout": 30,
+    "failoverEnabled": true
 }
```

### Example 4: Unity .asset YAML File

**Purpose**: Restructure flat attack fields into grouped config objects

```diff
--- a/Assets/Prefabs/Enemy.asset
+++ b/Assets/Prefabs/Enemy.asset
@@ -2,5 +2,10 @@
 MonoBehaviour:
   m_Script: {fileID: 11500000, guid: def456}
-  attackDamage: 10
-  attackRange: 2.0
-  attackCooldown: 1.5
+  attackConfig:
+    baseDamage: 10
+    critMultiplier: 1.5
+    range: 2.0
+    cooldown: 1.5
+  defenseConfig:
+    armor: 5
+    dodgeChance: 0.1
```

### Example 5: XML Manifest File (Android)

**Purpose**: Add camera and internet permissions for AR feature

```diff
--- a/Assets/Plugins/Android/AndroidManifest.xml
+++ b/Assets/Plugins/Android/AndroidManifest.xml
@@ -3,6 +3,8 @@
     package="com.company.game"
     android:versionCode="1">
 
+    <uses-permission android:name="android.permission.CAMERA" />
+    <uses-permission android:name="android.permission.INTERNET" />
     <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
 
     <application
```

---

## New Files

For entirely new files, skip the diff format. Use a fenced code block with the language tag and mark the file as `_(new)_`:

````markdown
### 3.X `Assets/Scripts/NewFeature.cs` _(new)_

```csharp
using UnityEngine;

public class NewFeature : MonoBehaviour
{
    // full file content
}
```
````

## Deleted Files

Mark with `_(deleted)_` and describe what is being removed:

```markdown
### 3.X `Assets/Scripts/Deprecated/OldManager.cs` _(deleted)_

Entire file removed — functionality moved to `NewManager.cs`.
```

---

## Common Patterns

Typical change signatures you will produce:

| Pattern | What it looks like |
|---------|-------------------|
| Add a field/property | Only `+` lines after existing field declarations |
| Rename a symbol | Paired `-` and `+` lines with the name changed |
| Replace method body | `-` block of old body, `+` block of new body |
| Add using/import | `+` line at top of file within the imports section |
| Change config value | Single `-`/`+` pair on the value line |
| Add new method | `+` block inserted between context lines |
| Remove dead code | Only `-` lines with surrounding context |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing file header (`---`/`+++`) | Always include both lines |
| Missing hunk header (`@@`) | Always include with line numbers |
| No context lines around changes | Include 3-5 unchanged lines for placement |
| Mixing multiple files in one block | One diff block per file |
| Wrong indentation in diff lines | Copy exact whitespace from source |
| Forgetting Purpose line | Add `**Purpose**: ...` above every diff block |
| Using HTML tables or Before/After | Always use unified diff format |
