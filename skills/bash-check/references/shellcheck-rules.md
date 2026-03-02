# shellcheck-rules.md

## Common ShellCheck Codes

| Code | Severity | Issue | Fix |
|---|---|---|---|
| SC2086 | Warning | Unquoted variable `$VAR` | Use `"$VAR"` |
| SC2046 | Warning | Unquoted command substitution | Use `"$(cmd)"` |
| SC2006 | Style | Backtick substitution | Replace `` `cmd` `` with `$(cmd)` |
| SC2164 | Warning | `cd` without error check | Use `cd dir || exit 1` |
| SC2181 | Style | Checking `$?` after command | Use `if cmd; then` directly |
| SC2155 | Warning | Declare and assign on same line | Split: `local var; var=$(cmd)` |
| SC2034 | Warning | Variable assigned but never used | Remove or prefix with `_` |
| SC2154 | Warning | Variable referenced but not assigned | Initialize before use |
| SC1091 | Info | Can't follow sourced file | Add `# shellcheck source=path` |
| SC2162 | Warning | `read` without `-r` flag | Use `read -r` |
| SC2219 | Warning | `let` expression | Use `(( expr ))` instead |

## Header Best Practices

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

## Quoting Patterns

```bash
# Bad
cp $src $dst
find $dir -name $pattern

# Good
cp "$src" "$dst"
find "$dir" -name "$pattern"
```

## Disable Suppressions (use sparingly)

```bash
# shellcheck disable=SC2086
eval $command  # intentional word-splitting
```

## Running ShellCheck

```bash
shellcheck script.sh                    # single file
shellcheck -S error script.sh          # errors only
shellcheck -x script.sh               # follow source
shellcheck --format=json script.sh    # JSON output for CI
```
