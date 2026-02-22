# Costing Standard

- **XS**: 1-2h (Trivial change)
- **S**: 2-4h (Small task)
- **M**: 4-8h (Standard task)
- **L**: 8-16h (Large complex task)
- **XL**: 16-32h (Major subsystem work - consider breaking down)

## Task Types

- New Feature
- Enhancement
- Bug Fix
- Refactor
- Configuration
- Testing
- Documentation

## Quality Checklist

- [ ] Context documents read before investigation
- [ ] Architecture decisions from docs reflected in plan
- [ ] Existing vs new work explicitly identified
- [ ] Every epic has ONE all-in-one table (8 columns: #, Name, Type, Desc, Goal, Code Changes, Acceptance, Cost)
- [ ] No separate per-task detail sections — everything inline in table rows
- [ ] Code Changes column links to `.patch` file in `Documents/Plans/patches/`
- [ ] Each `.patch` file uses unified diff format and applies via `git apply`
- [ ] Acceptance Criteria are short and outcome-focused (no implementation steps)
- [ ] Dependency graph and execution order included
- [ ] Cost summary consistent with per-task estimates
- [ ] Output file path is `Documents/Plans/PLAN_{FeatureName}.md`
- [ ] Template structure matches `assets/templates/PLAN_DOCUMENT_TEMPLATE.md` exactly
