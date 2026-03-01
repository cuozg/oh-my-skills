---
name: git-squash
description: "Squash multiple related commits into organized, well-documented commits. Use when consolidating messy commit history, preparing clean commits for PR, or organizing commits by feature/bugfix. Triggers on: (1) Pre-merge commit cleanup, (2) PR commit organization, (3) History consolidation, (4) Release branch preparation."
---

# Git Squash

## Input

Commit range (`start..end`), count (`-n`), or PR number. Optional: grouping strategy (`by-feature`|`by-type`|`auto`).

## Output
ALWAYS use this exact format:
- Squash plan per [output-template.md](references/output-template.md) — present for user approval before executing

## Reference Files
- [output-template.md](references/output-template.md) — Squash plan template for user approval
- workflow.md — Step-by-step squash workflow
