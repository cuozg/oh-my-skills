# Deep Mode — Multi-File Unity Features

Build complete features spanning 2+ runtime C# files with proper dependency ordering and cross-file wiring.

For architecture patterns, DI integration, event systems, and namespace strategy, refer to code-standards (loaded via the routing table). This file covers only the workflow.

## Workflow

1. **Qualify** — confirm 2+ runtime files needed; switch to Quick if single-file suffices
2. **Discover** — read affected files + nearby files for namespaces, asmdefs, registration patterns, and folder layout
3. **Plan** — list every file, its responsibility, dependency order, and which code-standards sections to load
4. **Implement** — contracts/data first → concrete logic → wiring/registration
5. **Verify** — `lsp_diagnostics` per dependency tier, then all files together
6. **Handoff** — changed paths, architecture notes, verification result, editor follow-up

## File Creation Order

Write files in dependency order — lower layers first:

```
1. Interfaces / base types          (IState, IDamageable, IService)
2. Data models / ScriptableObjects  (EnemyData, WaveConfig, GameEvent<T>)
3. Core implementations             (StateMachine, DamageCalculator)
4. Concrete implementations         (PatrolState, ChaseState, MeleeAttack)
5. MonoBehaviour consumers          (EnemyController, HealthPresenter)
6. Wiring / registration            (GameBootstrap, SceneSetup, LifetimeScope)
```

Each layer depends only on layers above it. Writing in order lets `lsp_diagnostics` catch real errors at each tier without false positives from missing types.

## Scoping Heuristic

| File Count | Complexity | Approach |
|-----------|-----------|----------|
| 2-3 | Low | Write sequentially, verify at end |
| 4-7 | Medium | Plan file list, verify per dependency tier |
| 8+ | High | Consider `unity-plan` first, then implement |

## Verification Rhythm

All verification uses two steps: `lsp_diagnostics` first, then `Unity.ReadConsole` for Unity console errors.

- **2-3 files**: diagnostics + console check after the last file
- **4-7 files**: diagnostics + console check after shared abstractions, again after concrete implementations, once after wiring
- **8+ files**: diagnostics + console check per dependency tier (interfaces → data → logic → consumers → wiring)

### Console Verification (MANDATORY)

After each verification point, run:

1. **`lsp_diagnostics`** on all changed files in the current tier
2. **`Unity.ReadConsole`** `{ Action: "Get", Types: ["Error", "Warning"], Count: 50, Format: "Detailed" }` — reads Unity console

**Parse console output:**
- `error CS####` → fix immediately before writing the next tier
- `warning CS####` → note; fix if it indicates a real bug
- Assembly errors → check asmdef boundaries and package dependencies
- Clean → proceed to next tier

**If Unity MCP is not available:** Run `lsp_diagnostics` only and note in handoff: "Console verification unavailable — verify in Unity Editor console."
**If LSP is not available but MCP is:** `Unity.ReadConsole` becomes the primary check; note LSP limitation in handoff.

Catching errors tier-by-tier prevents cascading failures. A missing interface in tier 1 would cause false errors in every tier below — fix before proceeding.

## Cross-File Checklist

Before writing:
- [ ] Which existing files will be modified?
- [ ] Which new files will be created?
- [ ] Are there asmdef boundaries to respect?
- [ ] Which interfaces/base types must exist before implementations?
- [ ] How does the new code register with existing systems?
- [ ] Which ScriptableObject assets need to be created in the editor?
- [ ] If DI framework mentioned (VContainer, Zenject, etc.) — which MonoBehaviours need `[Inject]` method/constructor injection, and which types need container registration?

For architecture patterns (state machine, service layer, event system, DI wiring) → code-standards `architecture-systems.md` § Architecture Patterns / § Dependency Management.

### DI Wiring Reminder

When the prompt mentions a DI container (VContainer, Zenject, etc.), the system needs **both sides** wired:

1. **Registration** — LifetimeScope / Installer registers types with the container
2. **Injection** — Consumer MonoBehaviours use `[Inject]` for method/property injection (since MonoBehaviours can't use constructor injection)

Missing either side means the DI integration is incomplete. Check both before marking the task done.

## Handoff Template

After completing Deep mode work, report:

```
Files created/modified:
- path/to/File.cs — [responsibility]
- path/to/File2.cs — [responsibility]

Wiring needed:
- [Inspector assignment / DI registration / asset creation]

Diagnostics: [clean / N warnings]
Console verification: [clean / N errors / MCP unavailable]

Follow-up:
- [ScriptableObject assets to create]
- [Prefab components to add]
- [Scene objects to configure]
```
