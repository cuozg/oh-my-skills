---
name: decisions
---

# Quick Decision Trees

Answer design questions quickly using these decision trees.

## "Should I use field injection or constructor injection?"

Constructor injection for services. For MonoBehaviours, use initialization methods or `[SerializeField]` references.

## "Should I use events or direct method calls?"

Events (C# events, delegates, or event bus) for cross-system communication. Direct calls for same-system internal logic.

## "Should I use async/await or coroutines?"

UniTask for all new async code. Coroutines only for legacy code maintenance.

## "Should I cache this?"

If called more than once per frame: **yes, cache it**.

## Assembly Definition Structure

```
YourProject.Core/          # Shared interfaces, models, utils
YourProject.Services/      # Business logic services
YourProject.UI/            # UI controllers and views
YourProject.Editor/        # Editor-only tools
```

Each assembly should:
- Have a `.asmdef` file
- Reference only what it needs
- Use `internal` by default, `[InternalsVisibleTo]` for tests
