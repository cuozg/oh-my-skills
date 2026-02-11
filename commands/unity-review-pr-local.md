---
description: Review code changes locally and generate a markdown review report
agent: build
---

Load the `unity/unity-review-pr-local` skill and review changes locally.

## Task

$ARGUMENTS

## Workflow

1. **Identify changes** - Analyze uncommitted changes, a specific branch, or commit range
2. **Review** against Unity conventions, performance patterns, and best practices
3. **Generate** a local markdown review file (not posted to GitHub)
4. **Categorize** findings by severity: critical, major, minor, suggestion

## Output

Generate a review markdown file with:
- Summary of changes
- Per-file review comments
- Performance considerations
- Architecture feedback
- Suggested improvements
