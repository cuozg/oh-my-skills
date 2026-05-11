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
  version: "1.3"
---
# unity-test-unit

Write Unity unit tests: Edit Mode + Play Mode, Arrange-Act-Assert, minimum 10 test cases per class.

## Data Categories (ALL THREE REQUIRED — Skipping Any Is a Blocking Failure)

**Category 1: Valid Data (Happy Path)** — normal inputs → correct output, typical combinations, state transitions with valid triggers.

**Category 2: Invalid/Malformed Data (CRITICAL)** — test every failure path with same rigor as happy paths:
- **Null** — null ref for every object parameter, null `[SerializeField]`, null from `GetComponent<T>()`
- **Empty** — `""`, `"  "`, `new List<T>()`, `new T[0]`, empty `ScriptableObject`
- **Out-of-range** — negative where positive expected, `int.MaxValue/MinValue`, `float.NaN`, `float.PositiveInfinity`
- **Malformed** — wrong enum cast `(MyEnum)999`, invalid GUID/path, strings with `<script>`, `\0`, `\n`
- **Invalid state** — before init, after `Destroy()`, wrong sequence, on disabled/destroyed component
- **Duplicate** — same item twice, duplicate keys, re-registering listener

Assert **specific behavior** per failure path: `Assert.Throws<ArgumentNullException>` (not just `Assert.Throws<Exception>`), `Assert.IsNull`, explicit state check. Never assert only "it doesn't crash."

**Category 3: Boundary Values (REQUIRED)** — at-min · at-max · just-below-min · just-above-max · midpoint. For collections: empty · single-element · first/last element.

**Minimum distribution:** 3+ valid · 3+ boundary · 4+ invalid = 10+ total per class.

## Workflow

1. **Read** target class: public API, dependencies, state
2. **Enumerate Data Contract (BLOCKING GATE)** — Before writing any test:
   - Per parameter: list concrete valid values + every invalid variant (null, empty, malformed, out-of-range)
   - Per object state: valid calling states vs invalid states
   - Define contract in 1 sentence per parameter — everything outside = invalid
   - Total must meet: 3+ valid, 3+ boundary, 4+ invalid
3. **Classify** — Edit Mode vs Play Mode (Play Mode only for coroutines/physics/lifecycle)
4. **Write** — AAA pattern with `[Test]` or `[UnityTest]`
5. **Verify** — compilation, missing assembly refs, namespace issues
6. **Coverage Gate (BLOCKING)** — Before done, verify:
   - Every object parameter has null-input test
   - Every string has `""` and `"  "` tests
   - Every collection has empty-collection test
   - Every numeric has at-min, at-max, just-outside tests
   - Every method with preconditions has invalid-state test
   - Every failure path asserts specific behavior — not just "doesn't crash"

## Rules

- Minimum 10 cases per class (3+ valid, 3+ boundary, 4+ invalid)
- `Assert.Throws<T>` for expected exceptions — never catch-and-ignore
- Edit Mode preferred; Play Mode only when coroutines/lifecycle required
- Naming: `MethodName_Condition_ExpectedResult` (e.g. `_WithNullInput_`, `_AtMaxBoundary_`)
- Place in `Assets/Tests/EditMode/` or `Assets/Tests/PlayMode/`
- `[SetUp]`/`[TearDown]` to prevent state leakage
- `[TestCase]` for parameterized variants
- Never `Debug.Log` in tests — `Assert` only

## References

Via `read_skill_file("unity-test-unit", "references/<file>")`:
- `test-patterns.md` — data-focused patterns, NSubstitute mocking
- `unity-test-attributes.md` — [Test], [UnityTest], Edit vs Play mode

Via `read_skill_file("unity-standards", "references/test/<file>")`:
- `edit-mode-patterns.md` · `play-mode-patterns.md` · `naming-conventions.md` · `coverage-strategy.md`
