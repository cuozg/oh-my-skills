# Risk Assessment

## Risk Level Table

| Level | Impact | Likelihood | Action |
|-------|--------|-----------|--------|
| Low | Minor inconvenience | Unlikely | Accept, document |
| Medium | Feature degradation | Possible | Mitigate, monitor |
| High | System failure | Likely | Mitigate before start |
| Critical | Data loss / security | Any | Block until resolved |

## Risk Categories

### Technical Risk
- New API/framework with no team experience
- Complex algorithms (pathfinding, procedural gen)
- Threading / async patterns
- Platform-specific behavior differences

### Integration Risk
- Third-party SDK version conflicts
- Multiple systems modified simultaneously
- Shared data format changes
- Assembly dependency changes

### Performance Risk
- Operations in hot paths (Update, FixedUpdate)
- Large dataset processing (100+ entities)
- Memory allocation in real-time loops
- Shader complexity on target hardware

### Data Migration Risk
- Save file format changes (existing users affected)
- ScriptableObject field renames (serialization break)
- Prefab structure changes (variant chain break)
- PlayerPrefs key changes

### UX Risk
- Input handling changes (player-facing)
- UI layout restructuring
- Animation state machine modifications
- Audio system changes (timing-sensitive)

## Scoring Formula

```
Risk Score = Impact (1-4) × Likelihood (1-4)

1-4   → Low
5-8   → Medium
9-12  → High
13-16 → Critical
```

| | Unlikely (1) | Possible (2) | Likely (3) | Certain (4) |
|---|---|---|---|---|
| **Minor (1)** | 1 Low | 2 Low | 3 Low | 4 Low |
| **Moderate (2)** | 2 Low | 4 Low | 6 Med | 8 Med |
| **Major (3)** | 3 Low | 6 Med | 9 High | 12 High |
| **Severe (4)** | 4 Low | 8 Med | 12 High | 16 Crit |

## Mitigation Strategies

| Strategy | When |
|----------|------|
| Spike/prototype | Unknown technical feasibility |
| Feature flag | Risky runtime behavior change |
| Rollback plan | Data migration, save format change |
| Incremental rollout | UX changes, major refactor |
| Parallel implementation | Critical path replacement |
| Extra testing | Integration or performance risk |
