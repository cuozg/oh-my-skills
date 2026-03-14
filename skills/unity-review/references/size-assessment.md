# PR Size Assessment

## Classification

After fetching PR files, classify by counting **changed C# files** and **changed functions/methods**.

| Size | C# Files Changed | Functions Changed | Review Mode |
|------|:-:|:-:|---|
| **Minor** | 1-2 | 1-5 | Quick (single-pass) |
| **Large** | 3+ | 6+ | Deep (parallel subagents) |

Either threshold triggers Large — e.g. 1 file with 8 changed functions = Large.

## How to Count

1. Filter PR file list to `*.cs` files only (ignore `.meta`, `.asset`, `.unity`, docs)
2. Count C# files with `status != "unchanged"`
3. For each file, scan the diff for method-level changes:
   - Count `+` or `-` lines inside method bodies
   - A method counts as "changed" if it has any modified lines
   - New methods count. Deleted methods count. Renamed = delete + add = 2.

## Routing

### Minor PR → Quick Review

- Review all files yourself in a single pass
- Load all 6 checklists from `unity-standards` and check inline
- Still produce findings as `[{path, line, severity, title, body}]`
- Same output format, same inline comment format, same verify step

### Large PR → Deep Review

- Spawn 6 parallel subagents (one per criterion)
- Follow `unity-standards/references/review/parallel-review-criteria.md`
- Aggregate, deduplicate, build review JSON, submit, verify

## Edge Cases

- **Mixed file types**: Only C# files affect classification. Asset-only PRs = Minor.
- **Generated code**: Exclude auto-generated files (`.Designer.cs`, `*.g.cs`) from count.
- **Test-only PRs**: Test files count toward thresholds normally.
- **Borderline**: When in doubt, prefer Deep — over-reviewing beats missing issues.
