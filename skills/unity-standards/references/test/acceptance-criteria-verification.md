# Acceptance Criteria Verification

Shared reference for the `plan-test` skill. Defines **how** to parse Acceptance
Criteria (ACs) from a goal file, **which** test mode (Edit vs Play) to use for
each AC, and **what** shape the resulting verification report must take.

This file is the single source of truth for AC→test mapping. It intentionally
does not duplicate test-writing patterns — cross-link to the sibling files:

- [coverage-strategy.md](./coverage-strategy.md) — what to cover and why
- [edit-mode-patterns.md](./edit-mode-patterns.md) — fast, in-process tests
- [edit-mode-advanced.md](./edit-mode-advanced.md) — async, serialization, editor APIs
- [play-mode-patterns.md](./play-mode-patterns.md) — scene, coroutines, physics
- [naming-conventions.md](./naming-conventions.md) — test naming rules
- [test-case-format.md](./test-case-format.md) — the HTML QA template (different skill)

The `plan-test` skill reads a goal file, runs the parser in Section A, classifies
each AC using the matrix in Section B, and emits a markdown report using the
template in Section C.

---

## Section A — AC Parser Spec

### A.1 Goal File Location

Goal files live at `Docs/Goals/{feature-name}/{kebab-case-task}.md`, produced by
the `plan-goal` skill. Every goal file has two machine-readable blocks:

1. **YAML frontmatter** — status, priority, and dependency metadata.
2. **`## Acceptance Criteria` section** — a GitHub-style task list.

### A.2 Required Frontmatter Fields

Per `plan-goal` Rule 14, these five fields MUST be present:

| Field         | Type       | Example                          |
| ------------- | ---------- | -------------------------------- |
| `status`      | string     | `todo` \| `in_progress` \| `done` |
| `priority`    | string     | `P0` \| `P1` \| `P2` \| `P3`     |
| `created`     | ISO date   | `2026-04-10`                     |
| `updated`     | ISO date   | `2026-04-18`                     |
| `depends_on`  | list\|null | `[search/indexer-core]`          |

If any field is missing, the parser MUST emit a warning and continue — do not
abort. Treat missing `depends_on` as `[]`.

### A.3 AC Checkbox Regex

Each AC is a single line that matches:

```
^- \[([ x])\] (AC-\d{3}): (.+)$
```

Capture groups:

1. **state** — `" "` means unchecked (not yet delivered), `"x"` means author
   claims it is delivered.
2. **id** — zero-padded three-digit ID (`AC-001` … `AC-999`). IDs MUST be
   unique within a goal file.
3. **text** — the human-readable criterion. Trim trailing whitespace.

Only lines inside the `## Acceptance Criteria` section are considered. Stop at
the next `## ` heading or EOF.

### A.4 Output Schema

For each matched line the parser produces:

```json
{
  "id": "AC-001",
  "text": "Player jumps when Space pressed",
  "checked": false,
  "sourceLine": 23
}
```

- `id` — string, the `AC-###` token.
- `text` — string, the criterion body (no leading bullet, no checkbox).
- `checked` — boolean, `true` iff state was `x`.
- `sourceLine` — 1-based line number in the goal file (used for deep links in
  the report).

### A.5 Title / Feature / Task Extraction

- **Title** — first `# ` (H1) heading in the body. If absent, fall back to the
  kebab-case filename converted to Title Case.
- **Feature** — the parent folder name under `Docs/Goals/` (e.g. `search`).
- **Task** — the filename without the `.md` extension (e.g.
  `add-full-text-search`).

### A.6 Concrete Example

Source: `Docs/Goals/search/add-full-text-search.md`

```markdown
---
status: in_progress
priority: P1
created: 2026-04-10
updated: 2026-04-18
depends_on: [search/indexer-core]
---

# Add Full-Text Search

## Acceptance Criteria

- [x] AC-001: Query returns results in under 200 ms for a 10k-doc corpus
- [ ] AC-002: Highlighted snippets wrap matched terms in `<mark>` tags
- [ ] AC-003: Empty query returns an empty list, not an error
```

Parser output:

```json
{
  "title":   "Add Full-Text Search",
  "feature": "search",
  "task":    "add-full-text-search",
  "frontmatter": { "status": "in_progress", "priority": "P1", "depends_on": ["search/indexer-core"] },
  "acs": [
    { "id": "AC-001", "text": "Query returns results in under 200 ms for a 10k-doc corpus", "checked": true,  "sourceLine": 12 },
    { "id": "AC-002", "text": "Highlighted snippets wrap matched terms in `<mark>` tags",  "checked": false, "sourceLine": 13 },
    { "id": "AC-003", "text": "Empty query returns an empty list, not an error",           "checked": false, "sourceLine": 14 }
  ]
}
```

### A.7 Edge Cases

| Case                                  | Handling                                                                |
| ------------------------------------- | ----------------------------------------------------------------------- |
| Duplicate AC IDs                      | Emit warning, keep first occurrence, mark duplicates as `skipped`.      |
| Non-sequential IDs (AC-001, AC-003)   | Allowed. Do not renumber. Report in verification metadata.              |
| Nested bullets under an AC            | Ignored by the regex. Treat as human-readable notes only.               |
| Code fences inside the AC section     | Skip lines inside fenced blocks to avoid matching checkboxes in code.   |
| No `## Acceptance Criteria` heading   | Report is generated with zero ACs and a top-level `⚠️ parse warning`. |
| Trailing whitespace in text           | Trim. Preserve internal whitespace (matters for backtick code spans).   |
| AC lines indented (e.g. inside a list)| Reject. Top-level bullets only — prevents false positives in examples. |

---

## Section B — Editor vs Play Mode Decision Matrix

Each AC must be classified into **Edit Mode** or **Play Mode** before a test is
written. Edit Mode is faster, deterministic, and runs without loading scenes;
Play Mode exercises real MonoBehaviour lifecycle, physics, and coroutines.

| # | AC Concern                                  | Recommended Mode | Rationale                                                                          |
| - | ------------------------------------------- | ---------------- | ---------------------------------------------------------------------------------- |
| 1 | Pure C# logic / algorithms                  | Edit             | No Unity runtime required.                                                         |
| 2 | ScriptableObject data validation            | Edit             | Assets instantiate without scene context.                                          |
| 3 | Serialization / save-load                   | Edit             | Use `JsonUtility`, `EditorJsonUtility`; no PlayMode tick.                          |
| 4 | Editor tooling / menu items / inspectors    | Edit             | Lives in `Editor/` asmdef; PlayMode cannot load it.                                |
| 5 | Awake / Start / OnEnable ordering           | Play             | MonoBehaviour lifecycle only fires in Play.                                        |
| 6 | Update / FixedUpdate / LateUpdate behavior  | Play             | Requires frame pump.                                                               |
| 7 | Coroutines and `WaitForSeconds`             | Play             | Use `[UnityTest]` + `yield return`. Edit Mode lacks a coroutine scheduler.         |
| 8 | Physics collisions / triggers / raycasts    | Play             | Physics step only runs in Play.                                                    |
| 9 | Input — keyboard, mouse, gamepad, touch     | Play             | `Input` / Input System needs a live player loop.                                   |
| 10| UGUI / UI Toolkit event callbacks           | Play             | Event system and layout only run in Play.                                          |
| 11| Animator state transitions                  | Play             | Animator requires Play to advance graph.                                           |
| 12| Scene load / additive / unload              | Play             | `SceneManager.LoadSceneAsync` is Play-only for runtime scenes.                     |
| 13| Networking, file I/O, coroutine async flows | Play             | Needs a frame loop to drive completion.                                            |
| 14| Performance budgets (ms, allocs, GC)        | Play             | Must measure on a live player loop with representative load.                       |
| 15| Platform conditionals (`#if UNITY_IOS`, …)  | Edit             | Pure compile-gated code; verified in Edit via reflection on the compiled assembly. |

### B.1 How to Classify an AC

Run the AC text through these questions in order; stop at the first **Yes**:

1. Does the AC mention a **frame**, **tick**, **physics**, **collision**,
   **coroutine**, **animator**, **scene**, **input**, or a **UI event**?
   → **Play Mode**. See [play-mode-patterns.md](./play-mode-patterns.md).
2. Does the AC require measuring **performance**, **allocations**, or **GC**
   under realistic load? → **Play Mode**.
3. Is the AC about **pure logic**, **data shape**, **serialization**,
   **editor tooling**, or **compile-time behavior**?
   → **Edit Mode**. See [edit-mode-patterns.md](./edit-mode-patterns.md) and
   [edit-mode-advanced.md](./edit-mode-advanced.md) for async/serialization.
4. Ambiguous? → **Edit Mode** first (cheaper, faster). Escalate to Play only
   if the Edit test cannot express the behavior.

### B.2 Naming and Coverage Cross-Links

- Test method names MUST follow [naming-conventions.md](./naming-conventions.md).
- Coverage targets (min tests per class, happy/edge/negative ratio) live in
  [coverage-strategy.md](./coverage-strategy.md).

---

## Section C — Markdown Report Template

The `plan-test` skill writes the report to
`Docs/Goals/{feature-name}/{kebab-case-task}-test.md`. Use the exact structure
below. Status icons: ✅ Pass · ❌ Fail · ⏭️ Skip · ⚠️ Partial.

````markdown
---
goal: {feature}/{task}
generated: {ISO-8601 timestamp}
verifier: plan-test
total_acs: {n}
passed: {n}
failed: {n}
skipped: {n}
---

# Test Report — {Title}

## Executive Summary

- **Goal**: `Docs/Goals/{feature}/{task}.md`
- **Status**: {one-line verdict, e.g. "3/5 ACs verified, 1 failing, 1 skipped"}
- **Mode split**: {edit-count} Edit Mode · {play-count} Play Mode
- **Next action**: {concrete follow-up — e.g. "fix AC-002 snippet wrapping"}

## AC Results

### ✅ AC-001 — {criterion text}

- **Mode**: Edit
- **Test**: `Assets/Tests/EditMode/SearchQueryTests.cs::ReturnsResultsUnder200Ms`
- **Evidence**: 10k-doc corpus benchmark, median 142 ms (budget 200 ms).
- **Notes**: —

### ❌ AC-002 — {criterion text}

- **Mode**: Edit
- **Test**: `Assets/Tests/EditMode/SnippetFormatterTests.cs::WrapsMatchesInMark`
- **Evidence**: Expected `<mark>foo</mark>`, got `**foo**`.
- **Fix hint**: `SnippetFormatter.Wrap` still uses Markdown bold; swap to HTML.

### ⏭️ AC-003 — {criterion text}

- **Mode**: Edit
- **Reason**: Implementation not started — tracked in `Docs/Goals/search/empty-query-handling.md`.

## Rules

1. One `### {icon} AC-### — {text}` block per AC, in source order.
2. Every block lists **Mode**, **Test** (file + method, or `—` if none), and
   either **Evidence** (for pass/fail) or **Reason** (for skip/partial).
3. For ❌ and ⚠️ blocks, include a **Fix hint** with the smallest next step.
4. Never rewrite the AC text — copy it verbatim from the goal file so diffs
   stay grep-able.
5. Report is idempotent: re-running `plan-test` overwrites the file but keeps
   the filename stable.

## Verification Metadata

- **Parser warnings**: {list, or "none"}
- **Duplicate IDs**: {list, or "none"}
- **Missing frontmatter fields**: {list, or "none"}
- **Goal frontmatter snapshot**: `status={...}` `priority={...}` `updated={...}`
````

---

## Worked Example

Source goal excerpt (`Docs/Goals/player/core-movement.md`):

```markdown
## Acceptance Criteria

- [x] AC-001: Player jumps when Space pressed
- [x] AC-002: Score increments by 10 on pickup
```

### Classification

| AC     | Mode | Why                                                              |
| ------ | ---- | ---------------------------------------------------------------- |
| AC-001 | Play | Requires Input + MonoBehaviour `Update` + Rigidbody velocity.    |
| AC-002 | Edit | Pure logic — `ScoreService.Add(10)` on a POCO, no frame needed.  |

### Rendered Report Fragment

```markdown
### ✅ AC-001 — Player jumps when Space pressed

- **Mode**: Play
- **Test**: `Assets/Tests/PlayMode/PlayerJumpTests.cs::SpacePressed_AppliesUpwardVelocity`
- **Evidence**: After `InputTestFixture.Press(Keyboard.spaceKey)` and one
  physics step, `rigidbody.velocity.y` ≥ configured `jumpSpeed`.
- **Notes**: Uses Input System test fixture — see
  [play-mode-patterns.md](./play-mode-patterns.md).

### ✅ AC-002 — Score increments by 10 on pickup

- **Mode**: Edit
- **Test**: `Assets/Tests/EditMode/ScoreServiceTests.cs::OnPickup_AddsTen`
- **Evidence**: `new ScoreService().OnPickup(); Assert.AreEqual(10, svc.Score);`
- **Notes**: Pure AAA — see [edit-mode-patterns.md](./edit-mode-patterns.md).
```

Both ACs pass → report headline: **"2/2 ACs verified, 1 Edit · 1 Play"**.
