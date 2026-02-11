---
description: Deep investigation and debugging of Unity errors with root cause analysis
agent: build
---

Load the `unity/unity-debug` skill and perform a deep debug investigation.

## Task

$ARGUMENTS

## Workflow

1. **Reproduce** - Understand the conditions that trigger the error
2. **Trace** - Follow the stack trace or execution path to the source
3. **Analyze** - Determine the root cause (not just symptoms)
4. **Document** - Create a detailed debug report with:
   - Error description and reproduction steps
   - Root cause analysis
   - Affected systems and side effects
   - Recommended fix with code changes
5. **Fix** - Apply the fix if straightforward, or escalate with detailed findings

## Input

Provide any of:
- Stack trace or error message
- Description of unexpected behavior
- Steps to reproduce
- Affected scene/prefab/script
