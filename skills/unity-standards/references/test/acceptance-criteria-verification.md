# Acceptance Criteria Verification

Use this when turning Unity goals, plans, or manual acceptance criteria into
verifiable checks. Keep the output tied to evidence: tests, editor inspection,
Play Mode proof, console logs, screenshots, profiler captures, or PR diffs.

## Goal File AC Parser

Goal files normally live at `Docs/Goals/{feature}/{task}.md`.

Parse only top-level checklist items inside `## Acceptance Criteria`:

```regex
^- \[([ x])\] (AC-\d{3}): (.+)$
```

Capture:

| Field | Meaning |
| --- | --- |
| `state` | blank = not claimed complete, `x` = author claims complete |
| `id` | stable criterion ID, for example `AC-001` |
| `text` | criterion text, trimmed only at the ends |
| `sourceLine` | 1-based line number for report links |

Parser rules:

- Stop at the next `## ` heading or EOF.
- Skip fenced code blocks.
- Duplicate IDs: keep the first, warn on later duplicates.
- Missing or empty AC section: report zero ACs with a parse warning.
- Do not renumber ACs and do not rewrite AC text.
- Frontmatter is useful metadata, but missing fields should warn rather than
  abort verification.

Minimal parser output shape:

```json
{
  "title": "Add Level Timer",
  "feature": "timer",
  "task": "add-level-timer",
  "acs": [
    {
      "id": "AC-001",
      "text": "Timer pauses while the pause menu is open",
      "checked": false,
      "sourceLine": 18
    }
  ],
  "warnings": []
}
```

## Mode Selection

Choose the cheapest Unity Test Framework mode that can prove the criterion.

| AC Concern | Default Mode | Evidence |
| --- | --- | --- |
| Pure C# rules, algorithms, parsers, validators | Edit Mode | NUnit assertions |
| ScriptableObject data or serialization | Edit Mode | asset instance / JSON roundtrip |
| Editor tooling, inspectors, menus, importers | Edit Mode | editor API assertions |
| MonoBehaviour lifecycle, `Update`, coroutines | Play Mode | `[UnityTest]` frame progression |
| Physics, collisions, raycasts under simulation | Play Mode | fixed-step simulation evidence |
| Input, UI events, Animator, scene loading | Play Mode | scene/player-loop proof |
| Performance, GC, frame timing, memory | Play Mode or profiler run | measured target-path metrics |
| Platform/compiler branches | Compile plus targeted runtime if available | build/define evidence |
| Analytics events and schemas | Edit Mode, Play Mode, or captured event inspection | event name, timing, params, duplicate/missing checks |
| Remote config, blueprints, LiveOps gates | Edit Mode plus targeted runtime path | valid/missing/expired/malformed/rollback checks |
| Server API, IAP, purchase validation | Play Mode, integration test, sandbox, or documented inspection | success, failure, retry, double-submit, authoritative response |

If an AC is ambiguous, start with Edit Mode. Escalate to Play Mode only when the
behavior requires a live player loop, real scene lifecycle, or measured runtime
state.

## Verification Workflow

1. Map each AC to one proof method: automated test, editor validation, manual QA
   step, profiler capture, or documented inspection.
2. Prefer automated tests for deterministic logic and regression-prone gameplay.
3. Use manual QA only for visual feel, device/platform behavior, or flows that
   are not practical to automate in the current project.
4. Run the narrowest meaningful verification first; broaden only when the change
   touches shared systems.
5. Record failures against the AC ID and keep the original AC text intact.
6. For production features, include analytics, LiveOps/config, server/API, IAP,
   release, and monitoring proof when those surfaces are part of the change.

## Test Coverage Guidance

- Cover happy path, boundary path, and at least one invalid path for each core
  rule-heavy class.
- Pure C# should usually be Edit Mode and high coverage.
- MonoBehaviour orchestration can be lower coverage if scene smoke tests prove
  the lifecycle behavior.
- Do not chase 80% coverage by testing Unity boilerplate; spend tests where a
  regression would break gameplay, data, economy, UI flow, or platform builds.

See:

- `coverage-strategy.md` for coverage priority.
- `edit-mode-patterns.md` and `edit-mode-advanced.md` for Edit Mode tests.
- `play-mode-patterns.md` for scene, coroutine, physics, and UI tests.
- `naming-conventions.md` for class and method naming.
- `test-case-format.md` when the deliverable is a manual QA HTML test plan.

## Report Format

Write reports under the goal folder when a goal file exists:
`Docs/Goals/{feature}/{task}-test.md`.

Use this compact structure:

```markdown
---
goal: {feature}/{task}
generated: {ISO-8601 timestamp}
total_acs: {n}
passed: {n}
failed: {n}
skipped: {n}
---

# Test Report - {Title}

## Summary

- Goal: `Docs/Goals/{feature}/{task}.md`
- Verdict: {passed}/{total} ACs verified
- Verification: {Edit Mode tests, Play Mode tests, manual checks, profiler, etc.}
- Next action: {one concrete next step, or "None"}

## AC Results

### Pass AC-001 - {original criterion text}

- Evidence: `{test name}`, `{scene/prefab path}`, `{console/profiler artifact}`
- Notes: {short note or "None"}

### Fail AC-002 - {original criterion text}

- Evidence: {what failed}
- Expected: {expected behavior}
- Actual: {actual behavior}
- Fix direction: {minimal next fix}

### Skip AC-003 - {original criterion text}

- Reason: {blocked by missing scene/device/data/tooling}
- Required evidence: {what would prove it}
```

## Acceptance Criteria Writing Rules

Good ACs are observable, bounded, and testable:

- State one behavior per AC.
- Include concrete trigger, expected result, and relevant boundary.
- Mention scene, prefab, config key, platform, or data source when important.
- For product-facing features, include analytics, LiveOps/config, server
  authority, performance threshold, or post-release monitoring only when that is
  part of the requirement.
- Avoid vague words like "works", "nice", "fast", or "properly" unless backed by
  a threshold.

Examples:

```markdown
- [ ] AC-001: Match detection returns no matches for an empty 8x8 board
- [ ] AC-002: Pause menu blocks board input until Resume is clicked
- [ ] AC-003: WebGL save data hydrates from browser storage before home UI renders
- [ ] AC-004: Opening inventory allocates less than 1 KB GC after warmup
- [ ] AC-005: Reward claim sends exactly one `reward_claimed` event after the server confirms success
- [ ] AC-006: Missing reward config keeps the previous valid config and shows no claimable reward row
```
