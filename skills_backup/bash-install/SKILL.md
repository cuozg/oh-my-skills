---
name: bash-install
description: "Install software, packages, and tools with automatic retry and fallback strategies. Use this skill when: (1) Installing CLI tools or packages, (2) Setting up development dependencies, (3) An installation fails and alternative methods are needed, (4) Verifying installed software works correctly."
---

# Bash Install

## Input

Package/tool name (e.g., `shellcheck`, `jq`, `node`). Optional: version, platform, preferred package manager.

## Output

Structured report per [INSTALL_REPORT.md](assets/templates/INSTALL_REPORT.md). Read template first, populate all sections, output directly to user.

## Examples

| Trigger | Input |
|---------|-------|
| "Install shellcheck" | `shellcheck` — detects OS, tries brew/apt, verifies |
| "Set up Node.js v20" | `node`, version=20 — tries brew/nvm/apt, pins version |

## Workflow

1. Identify package name, version, platform
2. Detect system environment — OS, architecture, available package managers
3. Installation strategy order — platform-specific fallback chain
4. Execute installation — try primary, fall through on failure
5. Verify installation — `command -v`, `--version`
6. Handle failures — diagnose, try next method, search alternatives, direct binary, source build
7. Report results — version, path, post-install steps or all failure details

## Reference Files
- workflow.md — Step-by-step install workflow

