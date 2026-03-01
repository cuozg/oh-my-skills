# Task Patch Requirements

Each per-task `.patch` file MUST:

- Be a valid unified diff (`patch -p1 --dry-run < TASK-1.1.patch`)
- Include ALL files affected by that task
- Include 3 lines of context around each change
- Have complete method/class context (not just changed lines)
- Be independently reviewable

## Patch Naming

Patch filenames use sequential epic.task labels:

```
patches/TASK-1.1.patch
patches/TASK-1.2.patch
patches/TASK-2.1.patch
```

The same labels must appear in `tasks.json` and `tasks.html`.

## Cost-to-Detail Reference

- **S** <50 lines
- **M** 50-150 lines
- **L** 150-400 lines
- **XL** 400+ lines

Each task must produce a `.patch` file appropriate to its cost estimate.
