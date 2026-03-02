# Plan Workflow

## Scoping Checklist

Before writing the plan document, confirm:
- [ ] Entry point(s) identified (file:line)
- [ ] All affected files listed
- [ ] External dependencies enumerated
- [ ] Out-of-scope items explicitly stated
- [ ] Risk areas flagged with evidence

## Plan Document Structure

`Documents/Plans/PLAN_{Name}.md` must contain:

```markdown
# PLAN: {Name}

## Request
{1-2 sentences: what is being built and why}

## Impact
- Files changed: {list}
- Systems affected: {list}
- Risk: {low|medium|high} — {reason with file:line}

## Tasks
1. {Task subject} [{size}] → skill:{name}
2. {Task subject} [{size}] → skill:{name}
```

## Size Guide

| Size | Hours | Description |
|------|-------|-------------|
| XS | 0-2h | Single isolated change |
| S | 2-8h | Small feature, 1-2 files |
| M | 1-3d | Feature spanning 2-5 files |
| L | 3-10d | Complex feature, 5+ files |

## Dependency Mapping

- Tasks with no dependencies → run in parallel
- Only block a task when it truly needs the prior task's output
- Minimize chains — every unnecessary `blockedBy` delays delivery
