# Architecture Review Checklist

## Dependency Injection

- [ ] Dependencies injected via constructor or interface — not `GetComponent` on other objects
- [ ] No `FindObjectOfType` / `GameObject.Find` in production code (CRITICAL)
- [ ] Service locator pattern used only at composition root
- [ ] Concrete class injection flagged as WARNING (prefer interface)

## Event Systems

- [ ] Event channels are typed (C# events or ScriptableObject channels) — not `string` keys
- [ ] Every `+=` in `OnEnable`/`Awake` has matching `-=` in `OnDisable`/`OnDestroy`
- [ ] No static event bus accessed from more than 3 distinct systems (coupling signal)
- [ ] Events not used for synchronous data flow (use method calls instead)

## Assembly Definitions

- [ ] Runtime assemblies do not reference Editor assemblies (CRITICAL if violated)
- [ ] No circular `.asmdef` references
- [ ] New systems placed in appropriate assembly — not dumped into Assembly-CSharp

## Coupling

- [ ] Classes with 6+ direct public dependencies flagged as WARNING
- [ ] No bidirectional direct references between feature modules
- [ ] Manager classes do not directly call each other — use events or interfaces

## SOLID

- [ ] Single Responsibility: classes over 300 lines checked for split opportunity (NOTE)
- [ ] Open/Closed: new behaviour added via extension, not direct modification of base classes
- [ ] Interface Segregation: interfaces have ≤ 5 methods unless justified
- [ ] Dependency Inversion: high-level modules depend on abstractions

## Severity Guide

- CRITICAL: breaks compilation, causes runtime crash, or violates Assembly boundaries
- WARNING: likely runtime bug, memory leak, or strong coupling
- NOTE: design smell, maintainability risk, or minor violation
