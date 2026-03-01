---
name: bash-optimize
description: "Optimize and refactor bash shell scripts for clarity, performance, and maintainability. Use this skill when: (1) Improving script readability and logic flow, (2) Reducing script execution time, (3) Refactoring complex conditionals or loops, (4) Applying bash best practices and modern syntax."
---

# Bash Optimize

## Input

Path to `.sh` file. Optional: focus — `performance`, `clarity`, `safety`, or `all` (default).

## Output

Structured report per [OPTIMIZATION_REPORT.md](assets/templates/OPTIMIZATION_REPORT.md). Read template first, populate all sections, output directly to user.

## Examples

| Trigger | Input |
|---------|-------|
| "Optimize this build script" | `scripts/build.sh` |
| "Speed up this script" | `ci/test-runner.sh`, focus=performance |

## Workflow

1. Analyze current script — purpose, functions, dependencies, complex patterns
2. Apply optimization patterns — performance, clarity, modern bash, error handling
3. Report findings — categorize by Performance / Clarity / Safety / Style

**Optimization patterns:** see bash-patterns.md (loaded below)

## Shared References

Load shared bash resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/other/bash-patterns.md")
```

## Reference Files
- workflow.md — Step-by-step optimization workflow
