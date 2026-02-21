---
name: unity-event-system
description: "(opencode-project - Skill) Unity event-driven architecture and decoupling patterns. Covers C# events/delegates, UnityEvent, ScriptableObject event channels, generic event bus, observer pattern, and message-driven communication between systems. Use when: (1) Designing event-driven communication between systems, (2) Building ScriptableObject event channels, (3) Choosing between C# events and UnityEvent, (4) Implementing an event bus or message bus, (5) Decoupling tightly coupled MonoBehaviours, (6) Setting up observer pattern in Unity. Triggers: 'event system', 'UnityEvent', 'event bus', 'ScriptableObject event', 'observer pattern', 'C# event', 'delegate', 'event channel', 'message bus', 'decouple'."
---

# unity-event-system — Event-Driven Architecture & Decoupling

**Input**: Communication requirement (which systems talk, data flow, subscription lifetime) + optional architecture, perf constraints, inspector needs
**Output**: Production-ready event channels, listeners, bus implementations with proper subscribe/unsubscribe lifecycle

## Workflow

1. **Identify communication needs** — map producers and consumers
2. **Choose mechanism** — C# events for performance, UnityEvent for inspector, SO channels for asset-level decoupling
3. **Design event data** — small payloads (primitives, structs, readonly objects)
4. **Implement infrastructure** — channels, listeners, bus as needed
5. **Wire subscriptions** — subscribe in `OnEnable`, unsubscribe in `OnDisable` — no exceptions
6. **Validate decoupling** — no direct references between producer and consumer
7. **Test in isolation** — events fire correctly, systems respond independently

## Event Mechanism Comparison

| Mechanism | Best For | Pros | Cons |
|:----------|:---------|:-----|:-----|
| **C# `event Action<T>`** | Code-to-code, performance-critical | Zero allocation, fastest, type-safe | Not in Inspector, needs direct ref |
| **UnityEvent** | Designer-wired, inspector config | Inspector-visible, drag-and-drop | Reflection-based, GC on invoke |
| **SO Event Channel** | Cross-scene, asset-level | No scene refs, reusable, testable | More setup, indirect dispatch |
| **Generic Event Bus** | Global many-to-many messaging | True decoupling, centralized | Implicit dependency, hard to trace |

### Decision Flow
```
Programmer only (code-to-code) → C# event Action<T>
Designer in Inspector → UnityEvent (or SO channel with GameEventListener)
Cross-scene decoupling → ScriptableObject Event Channel
Global broadcast to unknown listeners → Generic Event Bus
```

## Key Patterns

> **Full code examples**: See [Event Pattern Examples](references/event-pattern-examples.md) — C# events, SO channels, typed generic channels, EventBus<T> with struct events.

## Best Practices

**Do**:
- Always unsubscribe in `OnDisable` — every `+=` needs matching `-=`
- Use `?.Invoke()` to prevent NullRef when no listeners
- Keep event payloads small (structs to avoid heap allocs)
- Use SO channels for cross-scene; name events clearly (`OnHealthChanged`, `OnPlayerDied`)
- Prefer `Action<T>` over custom delegates; use `struct` for EventBus event types

**Don't**:
- Subscribe without unsubscribing (memory leaks, MissingReferenceException)
- Use string-based event names (no type safety, silent breaks)
- Put heavy logic in handlers (defer via coroutines/job queues)
- Use `UnityEvent` for hot paths (reflection overhead)
- Let event bus become a god object

## Performance

| Mechanism | Invoke Cost | Allocation | Inspector |
|:----------|:-----------|:-----------|:----------|
| `Action<T>` | ~0.001ms | Zero | No |
| `UnityEvent` | ~0.01ms | Small | Yes |
| SO Channel | ~0.002ms | Zero | Yes (via listener) |
| EventBus<T> | ~0.002ms | Zero (struct) | No |

**Rule**: Per-frame events (input, physics) → `Action<T>`. Occasional events → any mechanism. UnityEvent only when inspector wiring needed.

## Boundaries

- **Delegates to**: `unity-code-deep` (general C#), `ui-toolkit-patterns` (UI events), `unity-refactor` (decoupling existing code)
- **Does not handle**: UI Toolkit EventBase<T>, Unity Input System callbacks, networking RPC, animation events
