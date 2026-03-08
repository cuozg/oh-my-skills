---
name: unity-code-optimize
description: Simplify and optimize Unity C# code for clarity, consistency, and performance without changing behavior. Triggers — 'optimize code', 'simplify this', 'clean up code', 'improve readability', 'reduce allocations', 'code optimization'.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-code-optimize

Annotate and fix Unity C# code — improve clarity, reduce allocations, enforce conventions, preserve behavior. Every finding is an inline `// ── REVIEW` comment with an applied fix when safe.

## When to Use

- Code works but is hard to read, inconsistent, or overly complex
- Recent changes introduced allocation-heavy patterns or anti-patterns
- Method bodies exceed ~30 lines and need decomposition
- Redundant null checks, nested conditionals, or duplicated logic
- Performance-sensitive paths use LINQ, string concat, or frequent GetComponent

## Workflow

1. **Scope** — Identify target files. Default: `git diff --name-only HEAD~1` (recently modified `.cs` files). If user specifies files, use those instead.
2. **Discover conventions** — Load `unity-standards` via `read_skill_file`. Read 2-3 neighboring files to capture local style (naming, spacing, region usage, comment style).
3. **Analyze** — For each file, identify optimization opportunities across all categories (see Categories below). Prioritize by impact — hot-path issues first, style issues last. Target **5–8 findings per file**. If more issues exist, report only the highest-impact ones and drop STYLE/LOW findings. Merge related issues (e.g., two methods both exposing internal lists = one finding).
4. **Annotate + Fix** — For each finding, insert a comment block above the problem line following the format from `unity-standards/references/review/comment-format.md`:
   ```
   // ── REVIEW {icon} {LABEL} #{category}
   // What: 1-line summary of the optimization opportunity
   // Why:  1-3 lines — impact + evidence (variable names, call sites, frequency)
   ```
   Apply the fix directly below the comment when safe (single-line, no cross-file deps, no public API change). Leave code unchanged when fix needs a design decision or touches other files.
5. **Verify** — Run `lsp_diagnostics` on every changed file. Zero new errors. Zero new warnings.
6. **Summary** — Print a summary: files changed, total findings by severity, any issues skipped with reason.

## Severity Guide

| Icon | Label | When to use for optimization |
|------|-------|------------------------------|
| 🟠   | HIGH     | Hot-path allocation (LINQ in Update, GetComponent per frame), major clarity issue that hides bugs |
| 🟡   | MEDIUM   | Cacheable lookups, magic numbers in logic, methods >30 lines, dead code |
| 🔵   | LOW      | Minor readability improvement, slightly unclear naming, string concat outside hot path |
| ⚪   | STYLE    | Formatting preference, comment style, region usage |

Optimization findings should not use 🔴 CRITICAL — that severity is reserved for crash/data-loss bugs found during code review, not optimization opportunities.

## Categories

`#clarity` `#consistency` `#allocation` `#redundancy` `#caching` `#decomposition`

## Rules

- **Behavior preservation is absolute** — no functional changes. If unsure, skip the optimization.
- **Comment format is mandatory** — every finding uses `// ── REVIEW` with icon, label, category, What, and Why lines per `comment-format.md`.
- **One finding per comment** — never combine multiple issues in one comment block.
- **Place comment above the problem line** — not at the top of the file or method.
- **Apply fix below comment when safe** — cache lookups, extract constants, add guard clauses, flatten nesting, replace LINQ in hot paths.
- **Leave code unchanged** when fix needs design decision, touches other files, or changes public API.
- **Match local conventions** — don't impose external style if the file/project disagrees.
- **Clarity over cleverness** — readable code beats compact code. No nested ternaries.
- **No speculative optimization** — only flag what is measurably or obviously wasteful.
- **Finding count discipline** — 5–8 findings per file. When a file has many issues, keep HIGH and MEDIUM, drop LOW and STYLE. Merge identical patterns (e.g., two getters exposing internal lists → one finding covering both).
- **Preserve public API** — never rename or change signatures of public/protected members.
- **Skip test files** — unless explicitly requested.
- **Never commit** — leave the annotated diff for user inspection.

## Standards

Load `unity-standards` for all coding conventions. Key references:

- `references/review/comment-format.md` — inline review comment syntax and severity
- `references/code-standards/naming.md` — casing, prefixes, field conventions
- `references/code-standards/linq.md` — hot-path rules, allocation-safe alternatives
- `references/code-standards/collections.md` — collection choice, pre-sizing, pooling
- `references/code-standards/refactoring-patterns.md` — extract, decompose, composition
- `references/review/performance-checklist.md` — allocations, Update, physics, rendering

Load via `read_skill_file("unity-standards", "references/<path>")`.
