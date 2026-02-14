---
name: unity-event-system
description: "(opencode-project - Skill) Unity event-driven architecture and decoupling patterns. Covers C# events/delegates, UnityEvent, ScriptableObject event channels, generic event bus, observer pattern, and message-driven communication between systems. Use when: (1) Designing event-driven communication between systems, (2) Building ScriptableObject event channels, (3) Choosing between C# events and UnityEvent, (4) Implementing an event bus or message bus, (5) Decoupling tightly coupled MonoBehaviours, (6) Setting up observer pattern in Unity. Triggers: 'event system', 'UnityEvent', 'event bus', 'ScriptableObject event', 'observer pattern', 'C# event', 'delegate', 'event channel', 'message bus', 'decouple'."
---

# unity-event-system — Event-Driven Architecture & Decoupling

Design and implement event-driven communication patterns for Unity projects — enabling loosely coupled, testable, and maintainable game systems through proper event architecture.

## Purpose

Build robust event systems that decouple game systems from each other. Select the right event mechanism for each use case (C# events, UnityEvent, ScriptableObject channels, or event bus), implement type-safe event channels with proper subscription lifecycle, and eliminate the tight coupling that makes codebases brittle and untestable.

## Input

- **Required**: Communication requirement (which systems need to talk, what data flows between them, subscription lifetime)
- **Optional**: Existing architecture, performance constraints, inspector-configurability needs, testing requirements

## Output

Production-ready event infrastructure: event channels, listeners, bus implementations, and integration examples. All code compiles, follows `unity-code` quality standards, and includes proper subscribe/unsubscribe lifecycle management.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Decouple my health system from the UI" | Create ScriptableObject event channel for health changes, GameEventListener on UI to respond without direct reference |
| "Build an event bus for game-wide messages" | Implement generic `EventBus<T>` with type-safe subscribe/unsubscribe, automatic cleanup, and priority support |
| "Player death should trigger multiple systems" | Design GameEvent ScriptableObject raised on death, with listeners on UI, audio, camera shake, and respawn manager |
| "Choose between C# event and UnityEvent for my system" | Analyze use case — C# events for code-only listeners, UnityEvent for inspector-wired designer callbacks |

## Workflow

1. **Identify communication needs** — Map which systems produce events and which consume them
2. **Choose event mechanism** — C# events for performance, UnityEvent for inspector, ScriptableObject channels for asset-level decoupling
3. **Design event data** — Define what payload each event carries (primitives, structs, or readonly data objects)
4. **Implement event infrastructure** — Create channels, listeners, and bus as needed
5. **Wire subscriptions with lifecycle** — Subscribe in `OnEnable`, unsubscribe in `OnDisable` — no exceptions
6. **Validate decoupling** — Verify that neither producer nor consumer holds direct references to the other
7. **Test in isolation** — Confirm events fire correctly and systems respond independently

---

## Event Mechanism Comparison

### When to Use Each Pattern

| Mechanism | Best For | Pros | Cons |
|:----------|:---------|:-----|:-----|
| **C# `event Action<T>`** | Code-to-code, same-assembly, performance-critical | Zero allocation, fastest dispatch, type-safe | Not visible in Inspector, requires direct reference to publisher |
| **UnityEvent** | Designer-wired callbacks, inspector configuration | Inspector-visible, drag-and-drop, serialized | Reflection-based invocation, GC allocation on invoke, slower |
| **SO Event Channel** | Cross-scene, asset-level decoupling | No scene references needed, reusable asset, testable | Slightly more setup, indirect dispatch |
| **Generic Event Bus** | Global game-wide messaging, many-to-many | True decoupling, no references needed, centralized | Can become implicit dependency, harder to trace data flow |

### Decision Flow

```
Who configures the listener?
  Programmer only (code-to-code)
    -> C# event Action<T>
  Designer in Inspector
    -> UnityEvent (or SO channel with GameEventListener)
  Cross-scene / asset-level decoupling needed?
    -> ScriptableObject Event Channel
  Global broadcast to unknown listeners?
    -> Generic Event Bus
```

---

## Key Patterns

> **Full code examples for all event patterns**: See [Event Pattern Examples](references/event-pattern-examples.md) — covers C# events/delegates (PlayerHealth + HealthBarUI), ScriptableObject event channels (GameEvent + GameEventListener), typed generic event channels (TypedGameEvent<T> + concrete Int/Float/String implementations), and generic EventBus<T> with struct events, publisher, and subscriber examples.

---

## Best Practices

### Do

- **Always unsubscribe in `OnDisable`** — Every `+=` in `OnEnable` must have a matching `-=` in `OnDisable`
- **Use `?.Invoke()`** — Null-conditional prevents NullReferenceException when no listeners are subscribed
- **Iterate backwards when raising** — Allows listeners to safely unregister during callback invocation
- **Keep event payloads small** — Use structs for event data to avoid heap allocations
- **Use ScriptableObject channels for cross-scene** — They survive scene loads and require no scene references
- **Name events clearly** — `OnHealthChanged`, `OnPlayerDied`, `OnLevelCompleted` — past tense or changed-state naming
- **Prefer `Action<T>` over custom delegates** — Standard library types, no need for custom delegate declarations
- **Use `struct` for EventBus event types** — Prevents boxing, enables generic type dispatch without allocation

### Do Not

- **Never subscribe without unsubscribing** — Memory leaks, callbacks on destroyed objects, MissingReferenceException
- **Never use string-based event names** — Lose type safety, refactoring breaks silently, no compile-time checks
- **Never put heavy logic in event handlers** — Handlers should be fast; defer expensive work via coroutines or job queues
- **Never raise events in constructors** — Unity lifecycle is not guaranteed during construction
- **Never modify the subscriber list during iteration (without safeguards)** — Use backwards iteration or snapshot the list
- **Never use `UnityEvent` for performance-critical hot paths** — Reflection-based invoke has measurable overhead vs `Action<T>`
- **Never let the event bus become a god object** — If everything talks through a single bus with string keys, you've recreated tight coupling

---

## Performance Considerations

| Mechanism | Invoke Cost | Allocation | Inspector Support |
|:----------|:-----------|:-----------|:------------------|
| `Action<T>` | ~0.001ms | Zero | No |
| `UnityEvent` | ~0.01ms | Small (reflection) | Yes |
| SO Channel | ~0.002ms | Zero | Yes (via listener) |
| EventBus<T> | ~0.002ms | Zero (struct events) | No |

**Rule of thumb**: For events firing every frame (input, physics), use C# `Action<T>`. For events firing occasionally (UI clicks, game state changes), any mechanism works. Use UnityEvent only when inspector wiring is required.

---

## Handoff & Boundaries

### Delegates To

| Skill | When |
|:------|:-----|
| `unity-code` | General C# implementation beyond event-specific patterns |
| `ui-toolkit-patterns` | UI-specific event handling (button clicks, input field changes, pointer events) |
| `unity-refactor` | Refactoring existing tightly-coupled code to use event-driven patterns |

### Does Not Handle

- **UI Toolkit event system** — Pointer events, focus events, and UI Toolkit `EventBase<T>` belong to `ui-toolkit-*` skills
- **Unity Input System events** — Input action callbacks and input event routing belong to input system setup
- **Networking/multiplayer RPC** — Remote procedure calls and networked events belong to networking-specific code
- **Animation events** — AnimationEvent and StateMachineBehaviour callbacks are animation-domain concerns
