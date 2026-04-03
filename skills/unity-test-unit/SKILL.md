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

Write Unity unit tests using Edit Mode and Play Mode with Arrange-Act-Assert pattern, minimum 10 test cases per class. Every test suite MUST cover both valid-data and invalid-data paths. **Comprehensive invalid-data testing is non-negotiable** — most production bugs originate from untested failure paths, not from happy-path logic.

## When to Use

- Adding test coverage to an existing MonoBehaviour, ScriptableObject, or utility class
- Writing tests for a new system before or after implementation
- Increasing test coverage on a specific file or method
- Verifying edge cases, boundary values, and error paths in game logic

## Data-Focused Test Design (MANDATORY)

Every test suite is organized around **three core data categories**. All three are required — skipping invalid-data or boundary tests is a blocking failure.

### Category 1: Valid Data (Happy Path)

Tests that confirm the system works correctly with well-formed inputs:

- Normal expected values → correct output
- Typical real-world data combinations → expected behavior
- State transitions with valid triggers → correct new state
- Multiple valid inputs in sequence → consistent cumulative behavior

**What counts as "valid":** Any input that the method's contract says it accepts. If a method takes `int damage` where damage ≥ 0, then 0, 1, 50, and 9999 are all valid. Document the contract in the test name.

### Category 2: Invalid / Malformed Data (Failure Path) — CRITICAL

**Agents MUST test failure paths with the same rigor as happy paths.** This is where real bugs hide. Every public method must be exercised with every category of bad input it could receive.

- **Null inputs** — null references passed to every parameter that accepts objects. Every object parameter = one null test, no exceptions. In Unity: null `GameObject`, null from `GetComponent<T>()`, unassigned `[SerializeField]` references, null delegate/callback
- **Empty data** — empty strings `""`, whitespace-only strings `"  "`, empty collections `new List<T>()`, zero-length arrays `new T[0]`, empty dictionaries. In Unity: empty `AnimationCurve`, `ScriptableObject` with no data populated
- **Out-of-range values** — negative where positive expected, overflow, underflow, `int.MaxValue`, `int.MinValue`, `float.NaN`, `float.PositiveInfinity`, `float.NegativeInfinity`. In Unity: negative `Time.deltaTime`, layer index out of range, invalid `LayerMask`
- **Malformed inputs** — non-numeric string where a number is expected, strings with special characters (`<script>`, `\0`, `\n`), wrong enum cast `(MyEnum)999`, invalid GUID/ID strings, path strings with illegal characters. In Unity: invalid tag name, nonexistent scene name, malformed `Resources.Load` path
- **Invalid state** — calling methods before initialization, after disposal, in wrong sequence, on destroyed GameObjects, on disabled components, during scene transitions. In Unity: accessing `transform` after `Destroy()`, calling `StartCoroutine` on inactive object, reading from uninitialized `[SerializeField]`
- **Duplicate data** — adding the same item twice, duplicate keys, re-registering an already registered listener
- **Concurrent edge cases** — operations on destroyed GameObjects, null components, accessing disposed resources

**What counts as "invalid":** Any input or state that falls outside the method's documented or implied contract. If the method doesn't explicitly handle it, it MUST still be tested to verify the failure behavior is safe and predictable. **When in doubt, it's invalid — test it.**

For each invalid input, assert the **exact expected behavior**: exception type thrown, default value returned, error state set, or operation silently rejected. Never assert only that "it doesn't crash." Use `Assert.Throws<T>`, `Assert.IsNull`, or explicit state checks. **Every failure-path assertion must name the specific outcome** — `Assert.Throws<ArgumentNullException>`, not just `Assert.Throws<Exception>`.

### Category 3: Boundary Values — REQUIRED

Boundary tests sit at the exact edges where valid meets invalid. They catch off-by-one errors, fence-post bugs, and range-check failures.

For every numeric parameter or collection with a size constraint, test:

- **At minimum** — exact lower bound (e.g. `health = 0`)
- **At maximum** — exact upper bound (e.g. `health = maxHealth`)
- **Just below minimum** — one step below lower bound (e.g. `health = -1`)
- **Just above maximum** — one step above upper bound (e.g. `health = maxHealth + 1`)
- **Typical midpoint** — a representative value well within range

For non-numeric boundaries: first/last element of a collection, empty vs single-element collection, string at max length vs one-over.

### Minimum Distribution

Of the 10+ required test cases per class:
- At least **3 valid-data** tests (happy path, typical combinations)
- At least **3 boundary-value** tests (at-min, at-max, just-outside)
- At least **4 invalid-data** tests (null, empty, malformed, invalid state)
- Remaining tests cover additional edge cases and state transitions

## Workflow

1. **Read** — Read the target class(es) to understand public API, dependencies, and state
2. **Enumerate Data Contract (BLOCKING GATE)** — For each public method, enumerate cases per-parameter BEFORE writing any test code:
   - **Per parameter**: list concrete valid values, then list every invalid variant — null, empty, malformed, out-of-range, wrong type
   - **Per object state**: list valid calling states (initialized, active) vs invalid states (before init, after `Destroy`, wrong sequence, disposed)
   - **Define the contract explicitly**: write one sentence per parameter stating what "valid" means — everything outside that sentence is invalid and MUST be tested
   - Map each case to a Category: valid (Cat 1), boundary (Cat 3), or invalid (Cat 2)
   - Total must be 10+ test cases (3+ valid, 3+ boundary, 4+ invalid)
   - **Do NOT write test code until every parameter has valid/invalid/boundary cases listed**
3. **Classify** — Decide Edit Mode vs Play Mode per test (Play Mode only for coroutines/physics/lifecycle)
4. **Write** — Implement tests using AAA pattern with `[Test]` or `[UnityTest]` attributes
5. **Verify** — Check compilation; fix any missing assembly references or namespace issues
6. **Coverage Gate (BLOCKING)** — Before declaring the suite complete, verify:
   - Every object/reference parameter has a null-input test
   - Every string parameter has empty `""` and whitespace `"  "` tests
   - Every collection parameter has an empty-collection test
   - Every numeric parameter has at-min, at-max, and just-outside-range tests
   - Every method with preconditions has an invalid-state test (called before init, after destroy, in wrong sequence)
   - Every failure-path test asserts **specific behavior** (exception type, return value, or state) — not just "doesn't crash"
   - Distribution meets minimum: 3+ valid, 3+ boundary, 4+ invalid

## Rules

- Use Arrange-Act-Assert in every test body
- Minimum 10 test cases per class under test (3+ valid, 3+ boundary, 4+ invalid)
- **Every parameter that accepts an object MUST have a null-input test**
- **Every collection parameter MUST have an empty-collection test**
- **Every numeric parameter MUST have boundary tests at min, max, and just-outside**
- **Every failure path MUST assert specific behavior** — exception type via `Assert.Throws<T>`, return value via `Assert.AreEqual`, or state via explicit property checks. "Does not throw" is only acceptable when silent rejection is the documented contract.
- Use `Assert.Throws<T>` for expected exceptions — never catch-and-ignore
- Use negative assertions (`Assert.AreNotEqual`, `Assert.IsFalse`, `Assert.IsNull`) to verify what should NOT happen
- Prefer Edit Mode tests; use Play Mode only when coroutines or Unity lifecycle are required
- Name tests: `MethodName_Condition_ExpectedResult` (include data state in Condition, e.g. `_WithNullInput_`, `_WithEmptyList_`, `_WithNegativeValue_`, `_AtMaxBoundary_`, `_WithMalformedString_`)
- Place test files in `Assets/Tests/EditMode/` or `Assets/Tests/PlayMode/`
- Add `[SetUp]` / `[TearDown]` to avoid state leaking between tests
- Never call `Debug.Log` in tests — use `Assert` only
- Use `[TestCase]` for parameterized valid/invalid data variants on the same method

## Output Format

Test scripts with `[Test]` / `[UnityTest]` attributes, placed in the correct test assembly folder, compiling without errors.

## Reference Files

- `references/test-patterns.md` — Data-focused test patterns, NSubstitute mocking, valid/invalid data examples (loads `unity-standards/references/test/edit-mode-patterns.md` for AAA, assertions, SetUp/TearDown)
- `references/unity-test-attributes.md` — [Test], [UnityTest], [SetUp], [TearDown], Edit vs Play mode

Load references on demand via `read_skill_file("unity-test-unit", "references/{file}")` and `read_skill_file("unity-standards", "references/test/edit-mode-patterns.md")`.

## Standards

Load `unity-standards` for test conventions. Key references:

- `test/edit-mode-patterns.md` — [Test], Assert, mocking, setup/teardown
- `test/play-mode-patterns.md` — [UnityTest], yield, scene loading
- `test/naming-conventions.md` — MethodName_Scenario_Expected format
- `test/coverage-strategy.md` — what to test, boundary values, edge cases

Load via `read_skill_file("unity-standards", "references/test/<file>")`.
