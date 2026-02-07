---
name: bash-optimize
description: "Optimize and refactor bash shell scripts for clarity, performance, and maintainability. Use this skill when: (1) Improving script readability and logic flow, (2) Reducing script execution time, (3) Refactoring complex conditionals or loops, (4) Applying bash best practices and modern syntax."
---

# Bash Optimize

Analyze and optimize bash scripts for better performance, clarity, and maintainability.

## Output Requirement (MANDATORY)

**Every optimization report MUST follow the template**: [OPTIMIZATION_REPORT.md](.claude/skills/bash-optimize/assets/templates/OPTIMIZATION_REPORT.md)

Output the report directly to the user. No file save required.

Read the template first, then populate all sections.

## Workflow

### 1. Analyze Current Script

Read the entire script to understand:
- Overall purpose and flow
- Key functions and their dependencies
- Areas with complex logic or repeated patterns

### 2. Performance Optimizations

**Reduce Subshell Usage**

```bash
# ❌ Slow: subshell for variable assignment
var=$(echo "$input" | tr '[:lower:]' '[:upper:]')

# ✅ Fast: bash built-in
var="${input^^}"
```

**Use Built-in String Operations**

```bash
# ❌ External command
basename "$filepath"

# ✅ Parameter expansion
${filepath##*/}

# ❌ External command  
dirname "$filepath"

# ✅ Parameter expansion
${filepath%/*}
```

**Optimize Loops**

```bash
# ❌ Reading file line by line with cat
cat file.txt | while read line; do
  echo "$line"
done

# ✅ Direct redirection
while IFS= read -r line; do
  echo "$line"
done < file.txt
```

**Reduce Fork Overhead**

```bash
# ❌ Multiple forks
files=$(ls -1 | wc -l)

# ✅ Globbing + array
files=(*)
count=${#files[@]}
```

### 3. Clarity Improvements

**Function Organization**
- Extract repeated code into functions
- Use descriptive function names: `validate_input()`, `cleanup_temp_files()`
- Add function documentation comments

**Variable Naming**
- Use `snake_case` for variables
- Use `UPPERCASE` for constants/environment variables
- Use meaningful names: `file_count` instead of `fc`

**Conditional Simplification**

```bash
# ❌ Nested if statements
if [[ condition1 ]]; then
  if [[ condition2 ]]; then
    action
  fi
fi

# ✅ Combined condition
if [[ condition1 && condition2 ]]; then
  action
fi
```

**Case Statement for Multiple Conditions**

```bash
# ❌ Long if-elif chain
if [[ "$type" == "a" ]]; then
  action_a
elif [[ "$type" == "b" ]]; then
  action_b
elif [[ "$type" == "c" ]]; then
  action_c
fi

# ✅ Case statement
case "$type" in
  a) action_a ;;
  b) action_b ;;
  c) action_c ;;
esac
```

### 4. Modern Bash Practices

**Use `[[ ]]` over `[ ]`**
- More predictable with unquoted variables
- Supports `&&`, `||`, regex `=~`

**Use `$(command)` over backticks**
```bash
# ❌ Backticks
result=`command`

# ✅ Dollar-parentheses
result=$(command)
```

**Use Arrays for Lists**
```bash
# ❌ Space-separated string
files="file1.txt file2.txt file3.txt"

# ✅ Array
files=("file1.txt" "file2.txt" "file3.txt")
for f in "${files[@]}"; do
  process "$f"
done
```

### 5. Error Handling

**Add Strict Mode Header**
```bash
#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
```

**Trap for Cleanup**
```bash
cleanup() {
  rm -rf "$temp_dir"
}
trap cleanup EXIT
```

### 6. Documentation

Add header comment block:
```bash
#!/bin/bash
#
# script_name.sh - Brief description
#
# Usage: script_name.sh [options] <args>
#
# Options:
#   -h    Show help
#   -v    Verbose mode
#
```

## Optimization Checklist

| Category | Check |
|----------|-------|
| **Performance** | Replace external commands with built-ins |
| **Performance** | Avoid unnecessary subshells |
| **Performance** | Use efficient loop constructs |
| **Clarity** | Extract functions for repeated code |
| **Clarity** | Use descriptive names |
| **Clarity** | Simplify nested conditionals |
| **Safety** | Add strict mode where appropriate |
| **Safety** | Handle errors gracefully |
| **Style** | Consistent indentation (2 or 4 spaces) |
| **Style** | Add comments for complex logic |
