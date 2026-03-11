---
name: unity-test-unit
description: >
  Use this skill to write Edit Mode and Play Mode unit tests for Unity C# using Arrange-Act-Assert
  pattern with 10+ test cases per class. Use when the user says "write tests," "unit test this class,"
  "add test coverage," "create tests for X," or wants automated verification of a MonoBehaviour,
  ScriptableObject, or utility class. Do not use for manual QA test case documentation — use
  unity-test-case for that.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-test-unit

Write Unity unit tests using Edit Mode and Play Mode with Arrange-Act-Assert pattern, minimum 10 test cases per class.

## When to Use

- Adding test coverage to an existing MonoBehaviour, ScriptableObject, or utility class
- Writing tests for a new system before or after implementation
- Increasing test coverage on a specific file or method
- Verifying edge cases, boundary values, and error paths in game logic

## Workflow

1. **Read** — Read the target class(es) to understand public API, dependencies, and state
2. **Identify** — List 10+ test cases: happy paths, edge cases, boundary values, null/invalid inputs
3. **Classify** — Decide Edit Mode vs Play Mode per test (Play Mode only for coroutines/physics/lifecycle)
4. **Write** — Implement tests using AAA pattern with `[Test]` or `[UnityTest]` attributes
5. **Verify** — Check compilation; fix any missing assembly references or namespace issues

## Rules

- Use Arrange-Act-Assert in every test body
- Minimum 10 test cases per class under test
- Prefer Edit Mode tests; use Play Mode only when coroutines or Unity lifecycle are required
- Name tests: `MethodName_Condition_ExpectedResult`
- Place test files in `Assets/Tests/EditMode/` or `Assets/Tests/PlayMode/`
- Add `[SetUp]` / `[TearDown]` to avoid state leaking between tests
- Never call `Debug.Log` in tests — use `Assert` only

## Output Format

Test scripts with `[Test]` / `[UnityTest]` attributes, placed in the correct test assembly folder, compiling without errors.

## Reference Files

- `references/test-patterns.md` — NSubstitute mocking + test case categories (loads `unity-standards/references/test/edit-mode-patterns.md` for AAA, assertions, SetUp/TearDown)
- `references/unity-test-attributes.md` — [Test], [UnityTest], [SetUp], [TearDown], Edit vs Play mode

Load references on demand via `read_skill_file("unity-test-unit", "references/{file}")` and `read_skill_file("unity-standards", "references/test/edit-mode-patterns.md")`.

## Standards

Load `unity-standards` for test conventions. Key references:

- `test/edit-mode-patterns.md` — [Test], Assert, mocking, setup/teardown
- `test/play-mode-patterns.md` — [UnityTest], yield, scene loading
- `test/naming-conventions.md` — MethodName_Scenario_Expected format
- `test/coverage-strategy.md` — what to test, boundary values, edge cases

Load via `read_skill_file("unity-standards", "references/test/<file>")`.
