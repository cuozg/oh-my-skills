---
name: bash-optimize
description: "Optimize and refactor bash shell scripts for clarity, performance, and maintainability. Use this skill when: (1) Improving script readability and logic flow, (2) Reducing script execution time, (3) Refactoring complex conditionals or loops, (4) Applying bash best practices and modern syntax."
---

# Bash Optimize

## Input

Path to `.sh` file. Optional: focus — `performance`, `clarity`, `safety`, or `all` (default).

## Output

Structured report per [OPTIMIZATION_REPORT.md](assets/templates/OPTIMIZATION_REPORT.md). Read template first, populate all sections, output directly to user.

## Examples

| Trigger | Input |
|---------|-------|
| "Optimize this build script" | `scripts/build.sh` |
| "Speed up this script" | `ci/test-runner.sh`, focus=performance |

## Workflow

### 1. Analyze Current Script
Understand purpose, functions, dependencies, complex/repeated patterns.

### 2. Performance Optimizations

```bash
# Subshells → built-ins
var=$(echo "$input" | tr '[:lower:]' '[:upper:]')  # ❌
var="${input^^}"                                      # ✅

# External cmds → parameter expansion
basename "$filepath"  # ❌ → ${filepath##*/}   ✅
dirname "$filepath"   # ❌ → ${filepath%/*}    ✅

# Loop optimization
cat file.txt | while read line; do echo "$line"; done  # ❌
while IFS= read -r line; do echo "$line"; done < file.txt  # ✅

# Fork reduction
files=$(ls -1 | wc -l)  # ❌
files=(*); count=${#files[@]}  # ✅
```

### 3. Clarity Improvements
- Extract repeated code into descriptive functions
- `snake_case` vars, `UPPERCASE` constants
- Combine nested `if` → `if [[ cond1 && cond2 ]]`
- Replace long if-elif chains with `case` statements

### 4. Modern Bash Practices
- `[[ ]]` over `[ ]` (supports `&&`, `||`, `=~`)
- `$(command)` over backticks
- Arrays over space-separated strings

### 5. Error Handling
```bash
set -euo pipefail
IFS=$'\n\t'

cleanup() { rm -rf "$temp_dir"; }
trap cleanup EXIT
```

### 6. Documentation
Add header: script name, description, usage, options.

## Optimization Checklist

| Category | Check |
|----------|-------|
| Performance | Replace external commands with built-ins, avoid subshells, efficient loops |
| Clarity | Extract functions, descriptive names, simplify conditionals |
| Safety | Strict mode, error handling |
| Style | Consistent indentation, comments for complex logic |
