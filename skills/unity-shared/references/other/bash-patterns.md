# Bash Optimize — Patterns

## Performance Optimizations

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

## Clarity Improvements
- Extract repeated code into descriptive functions
- `snake_case` vars, `UPPERCASE` constants
- Combine nested `if` → `if [[ cond1 && cond2 ]]`
- Replace long if-elif chains with `case` statements

## Modern Bash Practices
- `[[ ]]` over `[ ]` (supports `&&`, `||`, `=~`)
- `$(command)` over backticks
- Arrays over space-separated strings

## Error Handling
```bash
set -euo pipefail
IFS=$'\n\t'

cleanup() { rm -rf "$temp_dir"; }
trap cleanup EXIT
```

## Documentation
Add header: script name, description, usage, options.
