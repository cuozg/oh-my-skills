# Investigation Workflow

## Step 1: Find Affected Files

```
grep(pattern="ClassName|MethodName", include="*.cs")
glob(pattern="**/FeatureName*.cs")
```

- Search for class names, method names, string literals
- Check both Runtime and Editor assemblies
- Note file count → feeds into sizing

## Step 2: Trace Call Chains

```
lsp_find_references(filePath, line, character)
lsp_goto_definition(filePath, line, character)
```

- Start from the entry point (public API or Unity callback)
- Follow references 2–3 levels deep
- Map: caller → target → downstream
- Record each file touched

## Step 3: Check Test Coverage

- Search for test files: `glob(pattern="**/*Tests.cs")`
- Match test classes to source classes
- Note untested public methods
- Flag critical paths without tests

| Coverage | Risk Implication |
|----------|-----------------|
| Tests exist and pass | Low risk change |
| Tests exist but outdated | Medium risk |
| No tests for this area | High risk — add test task |

## Step 4: Find Side Effects

Event subscribers and observers:
```
grep(pattern="\\.On[A-Z]|event\s+|Action<|UnityEvent", include="*.cs")
grep(pattern="AddListener|RemoveListener", include="*.cs")
```

- Map all event publishers → subscribers
- Check ScriptableObject channel listeners
- Identify callback chains that cross system boundaries

## Step 5: Map Dependencies

Build a dependency list:
```
Source File → [depends on] → Target Files
          → [depended by] → Consumer Files
```

- `using` directives show compile-time deps
- `GetComponent<T>` shows runtime deps
- `[SerializeField]` references show asset deps
- Inspector references show scene-time deps

## Step 6: Assess Risks

For each affected area, score:

| Factor | Question |
|--------|----------|
| Blast radius | How many systems touched? |
| Data safety | Can this corrupt saves/prefs? |
| Player-facing | Will player notice if broken? |
| Reversibility | Can changes be rolled back? |
| Test coverage | Are changes verifiable? |

## Output Checklist

- [ ] File list with change type (modify/create/delete)
- [ ] Dependency graph (upstream + downstream)
- [ ] Risk score per affected area
- [ ] Untested critical paths identified
- [ ] Side effects and event chains documented
- [ ] Size estimate with confidence level
