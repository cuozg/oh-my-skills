---
name: bash-optimize
description: >
  Use this skill to refactor an existing shell script for clarity, performance, and maintainability
  without changing its behavior. Use it when the user says a script is "messy," "hard to read," "slow,"
  or asks to "clean up" or "improve" a .sh file. Covers removing unnecessary subshells, simplifying
  conditionals, improving variable quoting, and applying best practices. Do not use for validation-only
  tasks — use bash-check for that.
metadata:
  author: kuozg
  version: "1.0"
---
# bash-optimize

Refactor an existing shell script to improve readability, reduce complexity, and apply best practices — behavior must not change.

## When to Use

- A working script has grown hard to read or maintain
- Performance bottlenecks exist (e.g., unnecessary subshells, repeated calls)
- Script lacks `set -euo pipefail` or proper quoting
- Preparing a script for team ownership or long-term maintenance

## Workflow

1. **Read** — Read the full script and understand its intended behavior
2. **Identify** — List specific issues: quoting gaps, useless forks, repeated code, poor naming, missing guards
3. **Refactor** — Apply improvements: extract functions, fix quoting, add `set -euo pipefail`, replace anti-patterns
4. **Verify** — Confirm the refactored script produces identical behavior for all identified execution paths
5. **Report** — List every change made with before/after examples

## Rules

- Never change observable behavior — refactor only
- Apply `set -euo pipefail` at the top unless the script explicitly requires lenient error handling
- Quote all variable expansions unless word-splitting is intentional
- Replace `$(cat file)` with `< file` redirection where appropriate
- Extract repeated logic into named functions
- Prefer `[[ ]]` over `[ ]` for conditionals in bash scripts

## Output Format

Optimized script (inline replacement) plus a report listing each change, the problem it solved, and the pattern applied.
