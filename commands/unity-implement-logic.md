---
description: Implement C# game logic with Unity best practices
agent: build
---

Load the `unity/unity-code` skill and implement the requested feature.

## Task

$ARGUMENTS

## Requirements

1. Write clean, commented, performant C# code
2. Follow project conventions from `.opencode/rules/unity-csharp-conventions.md`
3. Follow asset rules from `.opencode/rules/unity-asset-rules.md`
4. Use Unity 6 features where appropriate (Awaitable, New Input System)
5. Avoid anti-patterns: polling in Update, magic numbers, tight coupling, GC allocations in hot paths
6. Verify with `lsp_diagnostics` that there are no compiler errors
7. If a plan exists in `Documents/Plans/` or `Documents/Tasks/`, follow it exactly
