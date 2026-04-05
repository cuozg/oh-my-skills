# Domain-Specific Acceptance Criteria Examples

Reference file for writing high-quality acceptance criteria across different project domains. Each example demonstrates Observable, Specific, Testable, and Bounded criteria that an autonomous executor (`plan-work`) can verify without additional context.

---

## Unity — Runtime Feature

### Example: Add Health System with Damage and Healing

```markdown
## Acceptance Criteria
- [ ] `PlayerHealth` MonoBehaviour exists at `Assets/_Project/Scripts/Core/PlayerHealth.cs`
- [ ] `TakeDamage(float amount)` reduces `CurrentHealth` by `amount`, clamped to 0
- [ ] `Heal(float amount)` increases `CurrentHealth` by `amount`, clamped to `MaxHealth`
- [ ] `OnHealthChanged` UnityEvent fires with normalized health value (0-1) when health changes
- [ ] `OnDeath` UnityEvent fires exactly once when `CurrentHealth` reaches 0
- [ ] `lsp_diagnostics` reports zero errors on `PlayerHealth.cs`
- [ ] Unity console (`Unity_ReadConsole`) shows no compilation errors
```

### Example: Add Save System with JSON Serialization

```markdown
## Acceptance Criteria
- [ ] `SaveManager` singleton exists at `Assets/_Project/Scripts/Systems/SaveManager.cs`
- [ ] `Save(string slotName)` writes game state to `{Application.persistentDataPath}/saves/{slotName}.json`
- [ ] `Load(string slotName)` reads and deserializes the save file, returning the game state object
- [ ] Save file contains player position (Vector3), inventory item IDs (int[]), and current level name (string)
- [ ] `HasSave(string slotName)` returns true only if the file exists and is valid JSON
- [ ] Loading a corrupted/invalid file logs a warning and returns default state (no crash)
```

---

## Unity — Editor Tool

### Example: Custom Level Editor Window

```markdown
## Acceptance Criteria
- [ ] EditorWindow opens from menu `Tools/Level Editor` without errors
- [ ] Grid displays with configurable cell size (0.5 to 5 units, default 1)
- [ ] Left-click on grid cell places the selected prefab at snapped position
- [ ] Right-click on placed object removes it and destroys the GameObject
- [ ] Undo/Redo (`Ctrl+Z`/`Ctrl+Y`) works for both place and remove operations
- [ ] Window state (selected prefab, grid size) persists across domain reloads
```

---

## Flutter — Feature Implementation

### Example: Add Pull-to-Refresh on Feed Screen

```markdown
## Acceptance Criteria
- [ ] `FeedScreen` has a `RefreshIndicator` wrapping the list
- [ ] Pull-to-refresh triggers `feedProvider.refresh()` and shows the loading indicator
- [ ] After refresh completes, new items appear at the top of the list
- [ ] If refresh fails (network error), a `SnackBar` displays the error message and the old data remains visible
- [ ] Refresh is debounced — pulling again within 500ms of a completed refresh does not trigger a new request
- [ ] `dart analyze` reports zero errors on `lib/features/feed/`
```

### Example: Implement Onboarding Flow

```markdown
## Acceptance Criteria
- [ ] `OnboardingScreen` exists at `lib/features/onboarding/onboarding_screen.dart`
- [ ] Displays 3 pages: Welcome, Features, Get Started — navigable via horizontal swipe
- [ ] Page indicator dots show current position and update on swipe
- [ ] "Skip" button on pages 1-2 jumps directly to page 3
- [ ] "Get Started" button on page 3 navigates to `/home` and sets `hasSeenOnboarding: true` in SharedPreferences
- [ ] Subsequent app launches skip onboarding and go directly to `/home`
```

---

## Web / Next.js — Backend

### Example: Add Rate Limiting to API Routes

```markdown
## Acceptance Criteria
- [ ] Rate limiter middleware exists at `src/middleware/rate-limit.ts`
- [ ] Public endpoints (`/api/auth/login`, `/api/auth/register`) allow 10 requests per minute per IP
- [ ] Authenticated endpoints allow 60 requests per minute per user ID
- [ ] Exceeding the limit returns `429 Too Many Requests` with `{"error": "rate_limit_exceeded", "retryAfter": <seconds>}` body
- [ ] `Retry-After` header is set on 429 responses with seconds until reset
- [ ] Rate limit state uses Redis (existing `src/lib/redis.ts` client) — not in-memory
- [ ] Existing tests in `__tests__/api/` continue to pass
```

### Example: Add Pagination to List Endpoints

```markdown
## Acceptance Criteria
- [ ] All list endpoints (`/api/users`, `/api/posts`, `/api/comments`) accept `?page=N&limit=M` query params
- [ ] Default page is 1, default limit is 20, max limit is 100
- [ ] Response includes `meta: { total, page, limit, totalPages }` alongside `data` array
- [ ] Invalid page/limit values (negative, non-numeric) return 400 with descriptive error
- [ ] Cursor-based pagination is NOT used (stick to offset-based for simplicity)
- [ ] `npm run build` completes with exit code 0
```

---

## Infrastructure / DevOps

### Example: Set Up CI Pipeline for Flutter App

```markdown
## Acceptance Criteria
- [ ] `.github/workflows/ci.yml` exists and triggers on push to `main` and all PRs
- [ ] Pipeline runs: `dart format --set-exit-if-changed .`, `dart analyze`, `flutter test`
- [ ] Pipeline fails if any step fails (non-zero exit)
- [ ] Test results are uploaded as GitHub Actions artifacts
- [ ] Pipeline completes in under 10 minutes for a clean run
- [ ] `FLUTTER_VERSION` is pinned in the workflow file (not `latest`)
```

---

## Documentation

### Example: Document the Authentication System

```markdown
## Acceptance Criteria
- [ ] `docs/auth-system.md` exists with sections: Overview, Architecture, Token Flow, Error Handling, Extension Guide
- [ ] Architecture section includes a Mermaid sequence diagram showing the login → token → refresh flow
- [ ] All referenced files include actual paths verified to exist in the codebase
- [ ] Extension Guide shows how to add a new protected route (step-by-step with code snippets)
- [ ] No placeholder text ("TBD", "TODO", "add details here") remains in the document
```

---

## Anti-Patterns — Criteria to Avoid

These are examples of criteria that FAIL the quality bar. Each is too vague for autonomous execution.

| Bad Criterion | Problem | Better Version |
|---------------|---------|----------------|
| "Auth works" | Not testable | "POST `/api/auth/login` returns 200 with JWT for valid credentials" |
| "Code is clean" | Subjective | "`lsp_diagnostics` reports zero errors; no `as any` or `@ts-ignore`" |
| "Good error handling" | Vague | "All public methods catch exceptions and return typed error objects" |
| "Performance is acceptable" | Unbounded | "List endpoint responds in <200ms for 1000 records" |
| "Follows best practices" | Not verifiable | "Uses repository pattern matching `src/repositories/user.ts` convention" |
| "UI looks good" | Subjective | "Layout matches Figma frame `Login-v2` within 8px margin tolerance" |
