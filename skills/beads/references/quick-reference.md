# Beads Quick Reference

## Common Workflows

| Situation | Command |
|-----------|---------|
| Start session | `bd prime` |
| Find work | `bd ready` |
| Start issue | `bd update <id> --claim --status in_progress` |
| Finish issue | `bd update <id> --status closed && bd sync` |
| Create task | `bd create "title" -t task -p 2` |
| Child task | `bd create "title" -t task --parent <id>` |
| Dependency | `bd dep add <child> <parent>` |
| Health check | `bd doctor` |
| End session | Update all → `bd sync` → commit |

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `bd edit` | `bd update <id> --flags` |
| Forget sync | `bd sync` after every change |
| No ID in commit | Always `(bd-xxxx)` |
| Skip claim | `bd update <id> --claim` first |
