---
name: unity-code-optimize
description: Simplify and optimize Unity C# code for clarity, consistency, and performance without changing behavior. Triggers — 'optimize code', 'simplify this', 'clean up code', 'improve readability', 'reduce allocations', 'code optimization'.
---

# unity-code-optimize

Refine recently modified Unity C# code — improve clarity, reduce allocations, enforce conventions, preserve behavior.

## When to Use

- Code works but is hard to read, inconsistent, or overly complex
- Recent changes introduced allocation-heavy patterns or anti-patterns
- Method bodies exceed ~30 lines and need decomposition
- Redundant null checks, nested conditionals, or duplicated logic
- Performance-sensitive paths use LINQ, string concat, or frequent GetComponent

## Workflow

1. **Scope** — Identify target files. Default: `git diff --name-only HEAD~1` (recently modified `.cs` files). If user specifies files, use those instead.
2. **Discover conventions** — Load `unity-standards` bundles. Read 2-3 neighboring files to capture local style (naming, spacing, region usage, comment style).
3. **Analyze** — For each file, identify:
   - Clarity issues (deep nesting, long methods, unclear names, magic numbers)
   - Consistency issues (naming violations, formatting drift, mixed patterns)
   - Performance issues (hot-path allocations, repeated lookups, boxing, LINQ in Update)
   - Redundancy (dead code, duplicate logic, unnecessary null checks on non-nullable)
4. **Simplify** — Apply changes in-place. One edit call per file. Prioritize:
   - Extract method for blocks >15 lines with a single responsibility
   - Cache repeated lookups (`GetComponent`, `Find`, `Camera.main`)
   - Replace deep nesting with early returns / guard clauses
   - Convert magic numbers to `const` or `static readonly`
   - Prefer `TryGetComponent` over `GetComponent` + null check
   - Use `switch` expressions over chained `if-else` when mapping values
   - Pre-size collections when count is known
5. **Verify** — Run `lsp_diagnostics` on every changed file. Zero new errors. Zero new warnings.
6. **Report** — Output a summary: files changed, what changed and why, anything skipped with reason.

## Rules

- **Behavior preservation is absolute** — no functional changes. If unsure, skip.
- **Match local conventions** — don't impose external style if the file/project disagrees.
- **Clarity over cleverness** — readable code beats compact code. No nested ternaries.
- **Recently modified scope** — only touch files from recent changes unless user overrides.
- **No speculative optimization** — only optimize what is measurably or obviously wasteful.
- **One concern per edit** — don't mix clarity refactors with performance changes in the same edit range.
- **Preserve public API** — never rename or change signatures of public/protected members.
- **Skip test files** — unless explicitly requested.

## Output Format

Inline file modifications via `edit` tool + change summary after all files are processed.

## Standards

Load `unity-standards` for all coding conventions. Key references:
- `references/code-standards/naming.md` — casing, prefixes, field conventions
- `references/code-standards/formatting.md` — braces, spacing, regions
- `references/code-standards/linq.md` — hot-path rules, allocation-safe alternatives
- `references/code-standards/collections.md` — collection choice, pre-sizing, pooling
- `references/code-standards/null-safety.md` — null-check patterns, TryGet
- `references/code-standards/refactoring-patterns.md` — extract, decompose, composition
- `references/review/performance-checklist.md` — allocations, Update, physics, rendering

Load via `read_skill_file("unity-standards", "references/<path>")`.
