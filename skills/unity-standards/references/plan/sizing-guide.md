# Sizing Guide

## Size Table

| Size | Hours | Files | Scope | Example |
|------|-------|-------|-------|---------|
| XS | 1–2h | 1 | Single method/class change | Add `[Tooltip]` to all fields |
| S | 2–4h | 1–3 | Single feature, one system | New ScriptableObject + editor |
| M | 4–16h | 3–10 | Cross-system, multi-file | Inventory system with UI binding |
| L | 16–40h | 10–25 | Cross-system, new patterns | Save/load with versioning + migration |
| XL | 40+h | 25+ | Architectural, multi-sprint | ECS migration, networking layer |

## Sizing Factors

### File Count

| Files Changed | Weight |
|---------------|--------|
| 1 | Base |
| 2–3 | +1 size if crossing systems |
| 4–10 | Minimum M |
| 10+ | Minimum L |

### Boundaries Crossed

- Same assembly → no adjustment
- 2 assemblies → +1 size
- 3+ assemblies → +2 sizes
- Editor + Runtime → +1 size

### Test Coverage Required

| Size | Test Expectation |
|------|-----------------|
| XS | Manual verification only |
| S | 2–5 unit tests |
| M | 10–20 tests, edit + play mode |
| L | Full test suite, integration tests |
| XL | Test plan document, CI pipeline |

### Risk Multiplier

| Risk Level | Adjustment |
|------------|-----------|
| Low | No change |
| Medium | +25% hours |
| High | +50% hours |
| Critical | +100% hours, require spike first |

## Quick Decision Tree

```
1 file, no new patterns? → XS or S
Multiple files, same system? → S or M
Crosses system boundaries? → M or L
New architecture pattern? → L or XL
Requires data migration? → bump +1 size
```

## Confidence Levels

- **High** — similar work done before, clear scope
- **Medium** — known patterns, some unknowns
- **Low** — new territory, add investigation task first
