# Assembly Definition Setup & Checklist

> Extracted from `unity-test/SKILL.md` — assembly definition configuration, templates, compilation error troubleshooting, test discovery issues, and pitfalls.

## Assembly Definition Setup & Checklist

Test folders **require** assembly definition (`.asmdef`) files to compile correctly. Without an `.asmdef`, test scripts are compiled into the default `Assembly-CSharp` assembly, which does **not** reference NUnit or Unity TestRunner — causing `CS0246` errors for `NUnit.Framework`, `[TestFixture]`, `[Test]`, etc.

### Why `.asmdef` Files Are Required

Unity's Test Framework packages (`com.unity.test-framework@1.1.33`, `com.unity.ext.nunit@1.0.6`) provide NUnit as a **precompiled DLL** (`nunit.framework.dll`). Test assemblies must explicitly declare this dependency via `overrideReferences` + `precompiledReferences` in their `.asmdef`.

### New Test Folder Checklist

When creating a new test folder, **always**:

- [ ] Create an `.asmdef` file in the test folder root
- [ ] Set `"overrideReferences": true`
- [ ] Add `"nunit.framework.dll"` to `precompiledReferences`
- [ ] Add `"UnityEngine.TestRunner"` and `"UnityEditor.TestRunner"` to `references`
- [ ] Set `"defineConstraints": ["UNITY_INCLUDE_TESTS"]`
- [ ] For Edit Mode: set `"includePlatforms": ["Editor"]`
- [ ] For Play Mode: leave `includePlatforms` empty `[]`
- [ ] Set `"autoReferenced": false`
- [ ] Verify compilation: `unityMCP_check_compile_errors` returns zero errors

### EditMode `.asmdef` Template

```json
{
    "name": "EditModeTests",
    "rootNamespace": "",
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": [
        "Editor"
    ],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

### PlayMode `.asmdef` Template

```json
{
    "name": "PlayModeTests",
    "rootNamespace": "",
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

### Referencing Game Code from Tests

To reference game code (e.g., classes in `Assembly-CSharp`):
- If the game code has **no** `.asmdef`, test assemblies can access it implicitly — no additional configuration needed.
- If the game code has its **own** `.asmdef`, add that assembly name to the test `.asmdef`'s `references` array.
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences` — it is not a precompiled DLL and will cause unreliable behavior.

## Common Test Compilation Errors & Troubleshooting

### CS0246: "The type or namespace name 'NUnit' could not be found"

**Cause**: Test `.cs` files are in a folder without an `.asmdef`, so they compile into `Assembly-CSharp` which lacks NUnit references.

**Solution**: Create an `.asmdef` file in the test folder using the templates above.

**Symptoms** (cascading errors from a single root cause):
```
error CS0246: The type or namespace name 'NUnit' could not be found
error CS0246: The type or namespace name 'TestFixture' could not be found
error CS0246: The type or namespace name 'TestFixtureAttribute' could not be found
error CS0246: The type or namespace name 'Test' could not be found
error CS0246: The type or namespace name 'TestAttribute' could not be found
error CS0246: The type or namespace name 'SetUp' could not be found
error CS0246: The type or namespace name 'SetUpAttribute' could not be found
error CS0246: The type or namespace name 'TearDown' could not be found
error CS0246: The type or namespace name 'Assert' could not be found
```

All of these resolve by adding a single `.asmdef` file with the correct configuration.

### CS0246: "The type or namespace name 'UnityEngine.TestTools' could not be found"

**Cause**: Same root cause — missing `.asmdef` with `UnityEngine.TestRunner` reference.

**Solution**: Ensure `"UnityEngine.TestRunner"` is in the `references` array of the `.asmdef`.

### Troubleshooting Steps

1. **Check for `.asmdef`**: Does the test folder contain an `.asmdef` file? If not, create one.
2. **Verify `overrideReferences`**: Must be `true` to enable `precompiledReferences`.
3. **Verify `precompiledReferences`**: Must contain `"nunit.framework.dll"`.
4. **Verify `references`**: Must contain `"UnityEngine.TestRunner"` and `"UnityEditor.TestRunner"`.
5. **Verify `defineConstraints`**: Must contain `"UNITY_INCLUDE_TESTS"`.
6. **Check `includePlatforms`**: EditMode tests must have `["Editor"]`; PlayMode tests should have `[]`.
7. **Refresh Unity**: After creating/modifying `.asmdef`, use `unityMCP_refresh_unity` or reimport.
8. **Check package installation**: Verify `com.unity.test-framework` is installed in Package Manager.

## Common Test Discovery Issues & Solutions

These issues differ from compilation errors — tests **compile successfully** but the Test Runner shows "No tests to show" or does not list them.

### "No tests to show" in Test Runner Window

**Symptom**: Test scripts compile without errors, but the EditMode Test Runner window shows "No tests to show" or an empty test tree.

**Root Cause**: The tests are compiled into an assembly the Test Runner does not recognize as a test assembly. This typically happens when an `.asmdef` file is misconfigured.

**Common Causes & Solutions**:

| Cause | Diagnosis | Solution |
|:------|:----------|:---------|
| Invalid `.asmdef` with `Assembly-CSharp.dll` in `precompiledReferences` | Open `.asmdef` → check `precompiledReferences` for `Assembly-CSharp.dll` | Remove the `.asmdef` entirely and move tests to `Editor/` folder, OR fix the `.asmdef` (see [Assembly Definition Pitfalls](#assembly-definition-pitfalls)) |
| Missing `defineConstraints` | `.asmdef` has no `UNITY_INCLUDE_TESTS` constraint | Add `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` |
| Wrong `includePlatforms` | EditMode `.asmdef` missing `["Editor"]` | Set `"includePlatforms": ["Editor"]` for EditMode tests |
| Missing TestRunner references | `.asmdef` lacks `UnityEngine.TestRunner` / `UnityEditor.TestRunner` | Add both to `references` array |
| Tests in wrong folder | Tests in `EditMode/` without valid `.asmdef` | Move to `Editor/` folder (recommended) or create valid `.asmdef` |

### Troubleshooting Steps for Test Discovery

1. **Check Test Runner window**: `Window > General > Test Runner > EditMode` tab
2. **Verify test folder location**: Prefer `Assets/Scripts/Test/Editor/` (no `.asmdef` needed)
3. **If using `.asmdef`**: Open the `.asmdef` in text editor and verify:
   - `precompiledReferences` does NOT contain `Assembly-CSharp.dll`
   - `precompiledReferences` contains `nunit.framework.dll`
   - `references` contains `UnityEngine.TestRunner` and `UnityEditor.TestRunner`
   - `defineConstraints` contains `UNITY_INCLUDE_TESTS`
   - `includePlatforms` is `["Editor"]` for EditMode
4. **Force reimport**: Right-click test folder → Reimport, then check Test Runner again
5. **If still failing**: Delete the `.asmdef` and move tests to an `Editor/` folder

### Real-World Example: WWE Champions Fix

**Before (broken)**: `Assets/Scripts/Test/EditMode/EditModeTests.asmdef` contained:
```json
{
    "precompiledReferences": ["Assembly-CSharp.dll", "nunit.framework.dll"]
}
```
Tests compiled but Test Runner showed "No tests to show" because `Assembly-CSharp.dll` is not a precompiled DLL — it corrupted the assembly resolution.

**After (fixed)**: Removed `.asmdef`, moved tests to `Assets/Scripts/Test/Editor/`. Tests immediately appeared in Test Runner with zero configuration.

## Assembly Definition Pitfalls

Misconfigured `.asmdef` files are the **#1 cause** of test discovery failures. Tests compile without errors but the Test Runner cannot find them.

### NEVER Add `Assembly-CSharp.dll` to `precompiledReferences`

`Assembly-CSharp` is **not** a precompiled DLL — it is Unity's default compilation output for scripts outside any `.asmdef`. Adding it to `precompiledReferences` causes:

1. **Silent assembly resolution failure** — the `.asmdef` looks for a literal `Assembly-CSharp.dll` in precompiled paths, which does not exist there
2. **Tests compile** — because Unity's compilation pipeline still resolves the reference through other means
3. **Test Runner ignores the assembly** — the corrupted reference metadata makes the assembly unrecognizable as a test assembly
4. **"No tests to show"** — the end result is a completely silent failure

### Correct vs Incorrect `.asmdef` Configuration

**❌ INCORRECT** — causes silent test discovery failure:
```json
{
    "name": "EditModeTests",
    "overrideReferences": true,
    "precompiledReferences": [
        "Assembly-CSharp.dll",
        "nunit.framework.dll"
    ],
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ]
}
```

**✅ CORRECT** — if you must use `.asmdef`:
```json
{
    "name": "EditModeTests",
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": ["Editor"],
    "defineConstraints": ["UNITY_INCLUDE_TESTS"],
    "autoReferenced": false
}
```

**✅ BEST** — use `Editor/` folder instead (no `.asmdef` needed):
```
Assets/Scripts/Test/Editor/MyTests.cs  ← compiles into Assembly-CSharp-Editor automatically
```

### How Game Code Access Works Without `Assembly-CSharp.dll`

When game code has **no** `.asmdef` (compiles into `Assembly-CSharp`):
- `Assembly-CSharp-Editor` (from `Editor/` folders) **automatically** references `Assembly-CSharp`
- Test `.asmdef` assemblies **implicitly** reference `Assembly-CSharp` — no configuration needed

When game code has its **own** `.asmdef` (e.g., `GameCore`):
- Add `"GameCore"` to the test `.asmdef`'s `references` array
- `Editor/` folder tests still access it if `GameCore` is `autoReferenced: true`

## References

- [TEST_EXAMPLES.md](TEST_EXAMPLES.md) — Comprehensive examples: multiple test classes per feature, Edit/Play Mode, mocking, parameterized, event testing, integration testing
