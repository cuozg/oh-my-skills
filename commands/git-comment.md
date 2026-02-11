---
description: Generate structured commit comments from PRs or commit hashes
agent: build
---

Load the `git/git-comment` skill and generate commit documentation.

## Task

$ARGUMENTS

## Output Format

Generate a structured comment with:

### High Level Summary
- Brief description of what changed and why
- Impact on the system

### Specific Details
- Per-file breakdown of changes
- Key logic changes explained
- Breaking changes highlighted
- Migration notes if applicable
