---
name: bash-check
description: "Validate and check bash shell scripts for correctness and compatibility. Use this skill when: (1) Checking if a .sh file has syntax errors, (2) Verifying a script can run on the current shell version, (3) Validating script formatting and style, (4) Finding potential runtime issues before execution."
---

# Bash Check

Validate bash shell scripts for syntax errors, shell compatibility, and potential runtime issues.

## Output Requirement (MANDATORY)

**Every check report MUST follow the template**: [CHECK_REPORT.md](assets/templates/CHECK_REPORT.md)

Output the report directly to the user. No file save required.

Read the template first, then populate all sections.

## Workflow

### 1. Identify Target Script

Confirm the absolute path to the `.sh` file to validate.

### 2. Check Shell Version Compatibility

```bash
# Check current bash version
bash --version

# Check current shell
echo $SHELL
```

### 3. Syntax Validation

Run bash syntax check (dry-run mode):

```bash
bash -n /path/to/script.sh
```

This checks for syntax errors without executing the script.

### 4. ShellCheck Analysis (if available)

If `shellcheck` is installed, run comprehensive analysis:

```bash
# Check if shellcheck is available
which shellcheck

# Run shellcheck with all checks
shellcheck -x /path/to/script.sh

# Run with specific severity (error, warning, info, style)
shellcheck -S error /path/to/script.sh
```

Install shellcheck if needed: `brew install shellcheck` (macOS) or `apt install shellcheck` (Linux).

### 5. Manual Review Checklist

Verify the following aspects:

**Shebang Line**
- Script starts with proper shebang: `#!/bin/bash` or `#!/usr/bin/env bash`
- Shebang matches intended shell version

**Variable Handling**
- Variables are properly quoted: `"$variable"` instead of `$variable`
- Arrays use proper syntax: `"${array[@]}"`
- Default values used where appropriate: `${VAR:-default}`

**Exit Codes**
- Script uses `set -e` for fail-fast behavior (if appropriate)
- Critical commands check return codes
- Meaningful exit codes returned

**File Operations**
- File existence checked before operations: `[[ -f "$file" ]]`
- Permissions verified before write operations
- Temporary files handled safely with `mktemp`

**Portability**
- Avoid bashisms if POSIX compatibility needed
- Check for non-standard commands with `command -v`

### 6. Report Findings

Categorize issues by severity:
- **Error**: Script will fail to parse or execute
- **Warning**: Potential runtime issues or bugs
- **Info**: Style issues or best practice violations

## Common Issues

| Issue | Fix |
|-------|-----|
| `[: too many arguments` | Use `[[ ]]` instead of `[ ]` |
| `$'\r': command not found` | Convert line endings: `dos2unix script.sh` |
| `permission denied` | Add execute bit: `chmod +x script.sh` |
| Unbound variable | Use `set -u` or provide defaults |
