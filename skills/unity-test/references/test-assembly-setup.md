# Assembly Definition Setup & Checklist

> Assembly definition configuration for Unity Test Framework.

## Why `.asmdef` Required

Test folders need `.asmdef` files — without one, scripts compile into `Assembly-CSharp` which lacks NUnit references, causing `CS0246` errors.

### New Test Folder Checklist
- `overrideReferences`: true
- `precompiledReferences`: `["nunit.framework.dll"]`
- `references`: `["UnityEngine.TestRunner", "UnityEditor.TestRunner"]`
- `defineConstraints`: `["UNITY_INCLUDE_TESTS"]`
- EditMode: `includePlatforms: ["Editor"]` | PlayMode: `includePlatforms: []`
- `autoReferenced`: false

### EditMode `.asmdef`
```json
{
    "name": "EditModeTests",
    "references": ["UnityEngine.TestRunner", "UnityEditor.TestRunner"],
    "includePlatforms": ["Editor"],
    "overrideReferences": true,
    "precompiledReferences": ["nunit.framework.dll"],
    "autoReferenced": false,
    "defineConstraints": ["UNITY_INCLUDE_TESTS"]
}
```

PlayMode: same but `"includePlatforms": []`

### Referencing Game Code
- No game `.asmdef` → test assemblies access implicitly
- Game has `.asmdef` → add its name to test `references`
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences`

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| CS0246 "NUnit not found" | Missing `.asmdef` | Create with config above |
| "No tests to show" | `Assembly-CSharp.dll` in precompiledReferences | Remove it |
| Tests not discovered | Missing `UNITY_INCLUDE_TESTS` | Add to defineConstraints |
| Wrong platform | EditMode needs `["Editor"]` | Fix includePlatforms |

**NEVER** add `Assembly-CSharp.dll` to `precompiledReferences` — it's not a precompiled DLL, causes silent test discovery failure.

**Simplest approach**: Use `Editor/` folder (no `.asmdef` needed):
```
Assets/Scripts/Test/Editor/MyTests.cs  ← compiles into Assembly-CSharp-Editor automatically
```

## References
- [TEST_EXAMPLES.md](TEST_EXAMPLES.md) — Edit/Play Mode test examples, mocking, parameterized tests
