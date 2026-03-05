# Multi-File Workflow — Dependency Ordering & Structure

## File Creation Order

Always write files in dependency order to catch errors early:

```
1. Interfaces / base types          (IState, IDamageable)
2. Data models / ScriptableObjects  (EnemyData, GameEvent<T>)
3. Core implementations             (StateMachine, ServiceLocator)
4. Concrete implementations         (PatrolState, ChaseState)
5. MonoBehaviour consumers          (EnemyController, HealthPresenter)
6. Wiring / registration            (GameBootstrap, SceneSetup)
```

## Namespace Strategy

```
Company.Project.Feature           ← feature root
Company.Project.Feature.Data      ← SOs, configs, enums
Company.Project.Feature.Events    ← event channels
Company.Project.Feature.UI        ← views, presenters
```

Match existing project namespaces. If none exist, use `Game.Feature`.
One namespace = one folder. Never split a namespace across unrelated folders.

## Assembly Definition Awareness

Before adding cross-system references, check for `.asmdef` files:

```
Assets/Scripts/Core/Core.asmdef           ← interfaces, data, events
Assets/Scripts/Gameplay/Gameplay.asmdef    ← depends on Core
Assets/Scripts/UI/UI.asmdef               ← depends on Core
Assets/Scripts/Editor/Editor.asmdef       ← depends on Core, Gameplay
```

**Rules:**
- Never add circular asmdef references
- Shared types (interfaces, events, data) belong in the lowest-level asmdef
- If no asmdefs exist, don't create them unless asked
- Check existing asmdef refs with: `grep -r "reference" *.asmdef`

## Cross-File Dependency Checklist

Before implementation, answer:

- [ ] Which existing files will be modified? (list paths)
- [ ] Which new files will be created? (list paths + responsibilities)
- [ ] Are there asmdef boundaries to respect?
- [ ] Which interfaces/base types must exist before implementations?
- [ ] How does the new code register with existing systems? (bootstrap, DI, inspector wiring)
- [ ] Which ScriptableObject assets need to be created in the project?

## Scoping Heuristic

| Files | Complexity | Approach |
|-------|-----------|----------|
| 2–3   | Low       | Write sequentially, verify at end |
| 4–7   | Medium    | Plan file list, verify per tier |
| 8+    | High      | Consider unity-plan-quick first, then implement |

## Integration Points

When adding to existing systems, identify wiring method:
- **Inspector refs** — SerializeField drag-drop (document which GO needs which ref)
- **Service locator** — Register in bootstrap
- **Event channels** — Create SO asset, wire in OnEnable/OnDisable
- **Static access** — Singleton.Instance (use sparingly)

Document integration steps in the final report so the user knows what to wire in Unity Editor.
