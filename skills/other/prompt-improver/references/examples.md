# Prompt Improvement Examples

Before/after pairs showing prompt transformations. Three examples covering bug fix, refactoring, and multi-task splitting.

---

## Example 1: Bug Report → Actionable Debugging Prompt

**Before** (4/15): `The search is broken, users are complaining`

**After** (13/15):
```
## Goal
Fix: search returns no results for accented characters (e.g., "café", "naïve").

## Context
- Endpoint: `GET /api/search?q={query}` in `src/controllers/SearchController.ts`
- Uses Elasticsearch `products_v2` via `src/services/SearchService.ts`
- "résumé" → 0 results, "resume" → works. Likely missing Unicode normalization.

## Requirements
1. Check if ES analyzer supports Unicode folding
2. Add ICU folding or fix `SearchService.buildQuery()`
3. Ensure "cafe" matches "café"
4. Add test cases for accented queries

## Success Criteria
- `?q=café` returns same results as `?q=cafe`
- ASCII queries unchanged; all search tests pass
```

**Techniques**: Specificity, Context Injection, Verification Criteria

---

## Example 2: "Refactor This" → Scoped Refactoring

**Before** (3/15): `Refactor the user service, it's a mess`

**After** (14/15):
```
## Goal
Extract validation, notification, and persistence from `UserService` into SRP classes.

## Context
`UserService.ts` (847 lines) handles CRUD, validation, hashing, emails, audit, image upload.

## In Scope
- Split into: `UserService.ts` (orchestration), `UserValidator.ts`, `UserNotifier.ts`, `UserRepository.ts`
- Update DI in `src/config/di.ts` and tests

## Out of Scope
- Public API contract, `UserController.ts`, DB schema, query optimization

## Constraints
- Each class gets own interface; constructor injection; compatible method signatures

## Success Criteria
1. `UserService.ts` < 150 lines
2. Each class has focused unit tests
3. Integration tests pass unchanged
4. Zero circular dependencies
5. `dotnet build && dotnet test` clean
```

**Techniques**: Structure, Scope Bounding, Constraint Definition, Verification Criteria

---

## Example 3: Multi-Task → Focused Single Prompt

**Before** (3/15): `The dashboard needs work. It's slow, charts look bad, need date filter, export broken on Firefox.`

**After** (13/15) — one focused prompt:
```
## Goal
Add date range filter to analytics dashboard.

## Context
- `src/pages/Dashboard.tsx`, data via `useAnalyticsData()` hook
- Currently hardcoded 30 days; `react-date-range` already in package.json

## Requirements
1. Date range picker above charts with presets: 7d, 30d, 90d, Custom
2. Update `useAnalyticsData()` to accept `startDate`/`endDate`
3. Persist selection in URL query params
4. Default: 30 days (matches current)

## Constraints
- API already supports `start`/`end` params — no backend changes
- Don't modify chart components; date picker must be keyboard accessible

## Success Criteria
- "Last 7 days" updates all charts; custom range with future dates shows "No data"
- Page refresh preserves selection; default matches current behavior

NOTE: Performance, chart styling, Firefox export → separate prompts.
```

**Techniques**: Scope Bounding (split multi-task), Structure, Specificity
