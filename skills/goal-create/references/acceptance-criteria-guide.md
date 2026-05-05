# Acceptance Criteria Writing Guide

Use this reference when `goal-create` needs to turn a request into criteria that
`goal-execute` can verify without asking the user for missing context.

## Required Format

Acceptance criteria must live under one `## Acceptance Criteria` heading and use
unchecked Markdown checkboxes:

```markdown
## Acceptance Criteria
- [ ] {observable behavior or artifact}
- [ ] {bounded edge case or error path}
- [ ] {verification command, test, or evidence source}
```

Use 3-7 feature criteria for a normal goal. If a goal needs more than 7 feature
criteria, split it. Verification hygiene criteria such as build, analyzer, or
console checks are allowed, but they do not replace feature criteria.

## Writing Rules

- Write one behavior per checkbox.
- Name concrete files, commands, APIs, screens, data fields, or UI states when
  they are known.
- Include the expected result, not just the action.
- Cover the main success path plus important failure or edge cases.
- Prefer measurable bounds over adjectives: exact limits, statuses, paths,
  counts, timeouts, roles, permissions, or response shapes.
- Make every criterion independently verifiable. The executor should be able to
  point to code, tests, logs, screenshots, or command output as evidence.
- Do not hide implementation scope inside broad words like "properly",
  "correctly", "clean", "optimized", "robust", or "best practices".

## Criterion Shape

Use this generic pattern:

```text
{Subject} {does observable action} when {condition}, producing {expected result}
```

Good criteria usually include at least three of these:

| Element | Purpose |
|---------|---------|
| Subject | The file, component, route, command, system, or user-visible surface |
| Condition | The input, state, permission, platform, or edge case being exercised |
| Expected result | The exact output, state transition, UI behavior, status code, or artifact |
| Evidence | The test, command, console output, screenshot, or file inspection that proves it |

## Generic Example

```markdown
## Acceptance Criteria
- [ ] `FeatureSettings` loads its default values from `config/feature-settings.json` when no user override exists
- [ ] Invalid setting values are rejected with a clear validation error that names the invalid field
- [ ] The user-facing screen displays the saved setting after refresh without requiring a manual reload
- [ ] Existing behavior outside the feature area remains unchanged, verified by the current regression test command
- [ ] The documented verification command completes with exit code 0
```

## Rewrite Weak Criteria

| Weak | Better |
|------|--------|
| "Feature works" | "The feature screen saves a valid value and displays the saved value after refresh" |
| "Handle errors" | "Invalid input returns a validation error that names the rejected field" |
| "Use secure storage" | "Secrets are read from environment variables and no token value is committed to source files" |
| "Good performance" | "The list view renders 100 items without blocking input for more than 100 ms in the existing profiler check" |
| "Tests pass" | "The project's documented test command completes with exit code 0" |

## Final Check

Before writing the goal file, read the criteria as if you were seeing the
project for the first time. If any checkbox could be satisfied in two different
ways, tighten it until only one observable interpretation remains.
