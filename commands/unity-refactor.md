---
description: Refactor Unity C# code - extract, rename, restructure, decouple
agent: build
---

Load the `unity/unity-refactor` skill and perform the requested refactoring.

## Task

$ARGUMENTS

## Refactoring Types

- **Extract** - Pull methods, classes, or interfaces from complex code
- **Rename** - Rename symbols across the project safely
- **Restructure** - Reorganize MonoBehaviour hierarchies
- **Simplify** - Reduce complexity, deep nesting, long methods
- **Decouple** - Reduce tight coupling between systems
- **Replace anti-patterns** - Singletons, polling, magic numbers
- **Move** - Relocate code between files or namespaces
- **Clean up** - Remove dead code, obsolete patterns
- **Optimize** - Performance-oriented refactoring (GC, Update, allocations)

## Safety Requirements

1. Investigate before changing - understand all callers and dependencies
2. Use LSP tools (find references, goto definition) to ensure safety
3. Verify no compiler errors with `lsp_diagnostics` after each change
4. Preserve existing behavior - refactoring must not change functionality
