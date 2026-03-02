# Test Patterns — Skill Extensions

> **Canonical reference**: `unity-standards/references/test/edit-mode-patterns.md`
> Load via: `read_skill_file("unity-standards", "references/test/edit-mode-patterns.md")`

Standards covers AAA pattern, assertions, SetUp/TearDown, ScriptableObject testing,
exception testing, and manual mocking. Below are extensions unique to this skill.

## Mocking with NSubstitute

```csharp
// Create substitute
var mockRepo = Substitute.For<IRepository>();

// Set return value
mockRepo.GetById(1).Returns(new Entity { Id = 1 });

// Verify call
mockRepo.Received(1).Save(Arg.Any<Entity>());
```

## Test Case Categories to Cover

- **Happy path** — expected inputs, normal flow
- **Boundary** — min/max values, empty collections, zero
- **Edge** — null inputs, empty strings, max int
- **Negative** — invalid state, exception paths
- **State** — before/after mutation checks
