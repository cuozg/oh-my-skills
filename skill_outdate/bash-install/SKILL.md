---
name: bash-install
description: >
  Use this skill when the user needs to install a CLI tool, library, runtime, or dependency on their
  machine or CI environment — handles package manager selection, auto-retry with fallback strategies,
  and post-install verification. Use it even when the user just says "I need X set up" or "get me Y
  installed" without specifying how. Do not use for npm/pip install of project dependencies managed
  by a package file — those are standard tool calls.
metadata:
  author: kuozg
  version: "1.0"
---
# bash-install

Install a tool or dependency using the appropriate package manager, with retry logic, fallback strategies, and post-install verification.

## When to Use

- Installing a CLI tool, library, or runtime on a developer machine or CI environment
- Setting up project dependencies that are not managed by a package file
- Recovering from a failed or partial installation
- Scripting repeatable environment setup

## Workflow

1. **Detect** — Identify OS and available package managers (Homebrew, apt, pip, npm, etc.)
2. **Plan** — Select primary install method and define 1-2 fallback strategies
3. **Install** — Execute installation with retry (up to 3 attempts on transient failures)
4. **Verify** — Run post-install check: `which {tool}`, `{tool} --version`, or smoke test
5. **Report** — Output installation result, installed version, and verification status

## Rules

- Always verify after install — do not assume success from exit code alone
- Retry up to 3 times on network or lock errors before failing
- Fall back to alternative install method if primary fails after retries
- Print clear status lines: installing, retrying, failed, success
- Never silently continue after a failed verification

## Output Format

Installation report: tool name, method used, version installed, verification result (pass/fail), and any fallback steps taken.

## Reference Files

- `references/install-strategies.md` — retry patterns, fallback chains, verification commands

Load references on demand via `read_skill_file("bash-install", "references/{file}")`.
