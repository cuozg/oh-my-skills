# Code Quality Checklist

> For full-project quality audits. PR-level code review → see `review/review-csharp.md`.

---

## Testing

### Coverage
- All public API methods have at least one unit test
- Edge cases tested: null, empty, boundary values, overflow
- Integration tests for system boundaries (save/load, network, scene transitions)
- Play Mode tests for MonoBehaviour lifecycle-dependent logic
- Edit Mode tests for pure logic and editor tools
- Regression test added for every bug fix

### Quality
- Tests follow Arrange-Act-Assert pattern
- Each test verifies one behavior (single assert concept)
- Test names describe scenario and expected outcome: `Method_Scenario_Expected`
- No test interdependencies — each test is self-contained
- Mocks/stubs used for external dependencies (no real network/file I/O in unit tests)
- Test data created via builders or factories (no shared mutable fixtures)

---

## Anti-Pattern Quick Reference

> Detailed anti-pattern tables with Issue/Fix → see `review/review-csharp.md`.

| Severity | Anti-Patterns |
|----------|--------------|
| 🔴 Critical | Empty catch, async void, BinaryFormatter, public mutable collection |
| 🟡 Major | God class, feature envy, shotgun surgery, deep nesting, long method |
| 🔵 Medium | Primitive obsession, speculative generality, middle man, data clumps |
