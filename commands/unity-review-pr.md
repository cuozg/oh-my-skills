---
description: Review pull requests on GitHub with Unity-specific best practices
agent: build
---

Load the `unity/unity-review-pr` skill and review the specified PR.

## Task

Review this PR: $ARGUMENTS

## Review Focus

1. **Unity patterns** - Proper MonoBehaviour usage, lifecycle, serialization
2. **Performance** - GC allocations, Update loops, memory leaks, pooling
3. **Architecture** - SOLID principles, coupling, separation of concerns
4. **Code style** - Project conventions from `.opencode/rules/unity-csharp-conventions.md`
5. **Asset rules** - Compliance with `.opencode/rules/unity-asset-rules.md`
6. **Edge cases** - Null checks, race conditions, error handling
7. **Security** - No secrets, proper input validation

Post review comments directly on the GitHub PR.
