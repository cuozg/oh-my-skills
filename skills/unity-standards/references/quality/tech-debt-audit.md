# Tech Debt Audit

## TODO/HACK Density

| Density (per 1000 LOC) | Grade |
|------------------------|-------|
| 0–2 | A |
| 3–5 | B |
| 6–10 | C |
| 11–20 | D |
| 20+ | F |

Search patterns: `TODO`, `HACK`, `FIXME`, `TEMP`, `XXX`, `WORKAROUND`

## Code Duplication

| Duplication Level | Grade |
|-------------------|-------|
| < 3% | A |
| 3–5% | B |
| 5–10% | C |
| 10–20% | D |
| > 20% | F |

Detection:
- Identical blocks ≥ 6 lines → extract method
- Near-identical blocks (1-2 param diff) → parameterize
- Copy-pasted MonoBehaviours → extract base class or SO

## Complexity Thresholds

| Metric | Acceptable | Flag At |
|--------|-----------|---------|
| Cyclomatic complexity | ≤ 10 | > 15 |
| Nesting depth | ≤ 3 | > 4 |
| Parameters per method | ≤ 4 | > 6 |
| Methods per class | ≤ 20 | > 30 |
| Fields per class | ≤ 10 | > 15 |

## Dead Code Detection

Flag and report:
- `private` methods with zero references
- `[SerializeField]` fields unused in code AND inspector
- Unreachable branches after `return`/`throw`
- Empty Unity callbacks (`Start`, `Update` with no body)
- Commented-out code blocks > 5 lines

## Unused Usings

- Remove all unused `using` directives
- Flag files with > 3 unused usings as **Low** issue
- Auto-fixable — note in findings

## Large Class Detection

| Class Size (LOC) | Action |
|-------------------|--------|
| ≤ 200 | Acceptable |
| 201–500 | Review for SRP violation |
| 501–800 | Flag as **Medium** — plan split |
| 801+ | Flag as **High** — mandatory refactor |

Split strategies:
- Extract inner state machine to separate class
- Move serialization to dedicated handler
- Split UI logic from business logic
- Use partial classes only for generated code

## Long Method Detection

| Method Length (LOC) | Action |
|---------------------|--------|
| ≤ 20 | Acceptable |
| 21–50 | Review readability |
| 51–100 | Flag as **Medium** — extract submethods |
| 100+ | Flag as **High** — mandatory refactor |

## Magic Number Detection

```csharp
// ✗ Magic numbers
if (health < 20) Flee();
transform.position += Vector3.up * 9.81f * dt;

// ✓ Named constants
private const int FleeHealthThreshold = 20;
private const float Gravity = 9.81f;
```

- Flag numeric literals in logic (except 0, 1, -1)
- Flag string literals used more than once
- Exempt: array indices, loop bounds, math constants
