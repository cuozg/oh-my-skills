---
description: Plan Unity features with structured HTML output and diff patches
agent: build
---

Load the `unity/unity-plan` skill and execute the full planning workflow.

## Task

Plan the following Unity feature or change:

$ARGUMENTS

## Requirements

1. **Investigate** the existing codebase to understand current architecture and dependencies
2. **Analyze** requirements and identify affected systems
3. **Break down** the work into epics and tasks with clear acceptance criteria
4. **Estimate** effort and identify risks
5. **Generate** implementation plan as HTML files in `Documents/Plans/`
6. **Generate** a unified diff patch file with 100% code changes

## Output

Deliver a folder of HTML files:
- `overview.html` - High-level plan summary
- `tasks.html` - Detailed task breakdown
- `estimates.html` - Effort estimates
- `dependencies.html` - System dependencies
- `timeline.html` - Implementation timeline
- Plus a unified diff patch file
