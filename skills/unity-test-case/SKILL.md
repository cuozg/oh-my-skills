---
name: unity-test-case
description: "Expert QA professional for Unity game projects. Deep investigate game features, understand game logic and systems, and generate comprehensive test case documents in HTML format. Use when: (1) Creating test cases for a game feature or system, (2) Analyzing a feature for QA coverage, (3) Generating test case documentation, (4) Reviewing test completeness for game mechanics, (5) Creating QA plans for Unity gameplay systems. Triggers: 'test cases', 'QA', 'test plan', 'test coverage', 'create test cases for', 'generate test cases', 'quality assurance', 'test document', 'test case document'."
---

# Unity Test Case Generator

**Input**: Game feature/system to test + optional feature spec, existing test cases, priority areas

## Output
Comprehensive test case document in HTML format covering all test scenarios for the feature.

## Workflow

1. **Investigate** — read relevant C# scripts, map state machines/logic flows, identify entry points/triggers
2. **Analyze** — list configurable params, integration points, server/persistence dependencies
3. **Design** — test cases using test-case-patterns.md + edge case heuristics from qa-methodology.md (loaded below)
4. **Generate** — HTML from `assets/test-case-template.html`, replace `{{PLACEHOLDER}}` values, calculate summary stats
5. **Save** to `Documents/TestCases/{FeatureName}_TestCases.html`

## Shared References

Load shared QA resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/qa-methodology.md")
read_skill_file("unity-shared", "references/test-case-patterns.md")
```

## Reference Files
- `assets/test-case-template.html` — dark-themed responsive template
- workflow.md — Test case generation workflow
