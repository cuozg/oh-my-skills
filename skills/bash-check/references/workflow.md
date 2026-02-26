# Bash Check — Workflow

## 1. Identify Target Script
Confirm absolute path to the `.sh` file.

## 2. Check Shell Version
```bash
bash --version
echo $SHELL
```

## 3. Syntax Validation
```bash
bash -n /path/to/script.sh
```

## 4. ShellCheck Analysis
```bash
which shellcheck
shellcheck -x /path/to/script.sh
shellcheck -S error /path/to/script.sh
```
Install if needed: `brew install shellcheck` / `apt install shellcheck`

## 5. Manual Review Checklist
- **Shebang**: `#!/bin/bash` or `#!/usr/bin/env bash`
- **Variables**: quoted `"$variable"`, arrays `"${array[@]}"`, defaults `${VAR:-default}`
- **Exit codes**: `set -e`, check return codes, meaningful exits
- **File ops**: `[[ -f "$file" ]]`, permission checks, `mktemp` for temp files
- **Portability**: avoid bashisms if POSIX needed, use `command -v`

## 6. Report Findings
Categorize: **Error** (parse/execute fail) | **Warning** (runtime risk) | **Info** (style)

## Common Issues

| Issue | Fix |
|-------|-----|
| `[: too many arguments` | Use `[[ ]]` instead of `[ ]` |
| `$'\r': command not found` | `dos2unix script.sh` |
| `permission denied` | `chmod +x script.sh` |
| Unbound variable | `set -u` or provide defaults |
