# Assembly Definitions & Setup Checklist

## Directory Structure

```
Assets/Scripts/Test/
├── Editor/                    ← EditMode (no .asmdef needed)
│   ├── FeatureA/
│   │   └── InventoryTests.cs
│   └── Helpers/
│       └── TestDoubles.cs
└── PlayMode/                  ← Requires .asmdef
    ├── PlayModeTests.asmdef
    └── PlayerMovementTests.cs
```

`Editor/` auto-includes NUnit + TestRunner references. No `.asmdef` config needed.

## Assembly Definitions

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

### PlayMode `.asmdef`

Same but `"includePlatforms": []` (empty = all platforms for device testing).

### Referencing Game Code

- **No game `.asmdef`** (default `Assembly-CSharp`): Tests access implicitly
- **Game has `.asmdef`** (e.g., `GameCore`): Add `"GameCore"` to test `references`
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences`

## ❌ Common `.asmdef` Pitfall

Adding `"Assembly-CSharp.dll"` to `precompiledReferences` → tests compile but Test Runner shows "No tests". **Fix**: Remove it or use `Editor/` folder.

## Pre-Creation Checklist

1. `Editor/` folder (no `.asmdef` needed) or valid `.asmdef` with `overrideReferences: true`, `precompiledReferences: ["nunit.framework.dll"]`, `defineConstraints: ["UNITY_INCLUDE_TESTS"]`
2. `[TestFixture]` class, `[Test]`/`[UnityTest]` methods, `Subject_Scenario_Expected` naming
3. Verify in `Window > General > Test Runner`
