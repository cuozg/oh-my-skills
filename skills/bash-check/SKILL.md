---
name: bash-check
description: Validate shell scripts with syntax check and ShellCheck lint — use for 'check script', 'validate bash', 'lint shell', 'shellcheck', 'check shell script'
---
# bash-check

Validate shell scripts using `bash -n` syntax checking and ShellCheck static analysis, then produce a findings report.

## When to Use

- Before committing or deploying a shell script
- Auditing an existing script for latent bugs or unsafe patterns
- Verifying a script written by another author
- CI pre-check for shell scripts in a repository

## Workflow

1. **Read** — Read the target script in full
2. **Syntax** — Run `bash -n {script}` to catch parse errors
3. **Lint** — Run `shellcheck {script}` to get all warnings and errors
4. **Review** — Manually check: quoting, `set -e`/`-u`/`-o pipefail`, uninitialized variables, subshell leaks
5. **Report** — Compile findings into a validation report with severity, line, description, and suggested fix

## Rules

- Run both `bash -n` and `shellcheck` — neither alone is sufficient
- Report every finding, not just errors — warnings matter
- Include the fix for each finding, not just the problem
- Note any `# shellcheck disable` suppressions and whether they are justified

## Output Format

Validation report listing: severity (error/warning/info), line number, ShellCheck code, description, and suggested fix. Summary line: pass/fail with finding count.

## Reference Files

- `references/shellcheck-rules.md` — common ShellCheck codes and their fixes

Load references on demand via `read_skill_file("bash-check", "references/{file}")`.
