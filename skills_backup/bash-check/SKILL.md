---
name: bash-check
description: "Validate and check bash shell scripts for correctness and compatibility. Use this skill when: (1) Checking if a .sh file has syntax errors, (2) Verifying a script can run on the current shell version, (3) Validating script formatting and style, (4) Finding potential runtime issues before execution."
---

# Bash Check

## Input

Path to `.sh` file. Optional: target shell version or POSIX-compliance flag.

## Output

Structured report per [CHECK_REPORT.md](assets/templates/CHECK_REPORT.md). Read template first, populate all sections, output directly to user.

## Examples

| Trigger | Input |
|---------|-------|
| "Check this script for errors" | `scripts/deploy.sh` |
| "Is this script POSIX compatible?" | `utils/backup.sh` |

## Workflow

1. Identify target script — confirm absolute path
2. Check shell version — `bash --version`, `echo $SHELL`
3. Syntax validation — `bash -n script.sh`
4. ShellCheck analysis — `shellcheck -x script.sh`
5. Manual review checklist (shebang, quoting, exit codes, portability)
6. Report findings — categorize as Error / Warning / Info

## Reference Files
- workflow.md — Step-by-step validation workflow

