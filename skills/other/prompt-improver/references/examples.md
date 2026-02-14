# Prompt Improvement Examples

Before/after pairs showing real prompt transformations for coding agent tasks. Study these to internalize the improvement patterns.

---

## Example 1: Vague Feature Request → Structured Implementation Spec

### Before (Score: 5/15)
```
Add dark mode to the app
```

### After (Score: 14/15)
```
## Goal
Add a dark mode toggle to the Settings screen that persists the user's theme preference.

## Context
The app currently uses hardcoded light theme colors defined in `src/styles/theme.ts`. 
The Settings screen is at `src/screens/SettingsScreen.tsx`. We use React Navigation 
and styled-components.

## Requirements
1. Add a toggle switch to SettingsScreen labeled "Dark Mode"
2. Create a dark theme palette in `src/styles/darkTheme.ts` mirroring the structure of `theme.ts`
3. Use React Context (`ThemeContext`) to provide the active theme to all components
4. Persist the preference to AsyncStorage under key `@app:theme`
5. Load the saved preference on app startup in `App.tsx`

## Constraints
- Follow existing color token naming in `theme.ts`
- Do NOT modify third-party component styles directly — wrap them if needed
- Support system theme detection as a future enhancement (not in this PR)

## Success Criteria
1. Toggle switches between light and dark themes instantly
2. Preference survives app restart
3. All existing screens render correctly in both themes
4. No TypeScript errors; all existing tests pass
```

**Techniques applied**: Specificity, Structure, Context Injection, Constraint Definition, Scope Bounding, Verification Criteria

---

## Example 2: Bug Report → Actionable Debugging Prompt

### Before (Score: 4/15)
```
The search is broken, users are complaining
```

### After (Score: 13/15)
```
## Goal
Fix: search returns no results when the query contains accented characters (e.g., "café", "naïve").

## Context
- Search endpoint: `GET /api/search?q={query}` in `src/controllers/SearchController.ts`
- Uses Elasticsearch index `products_v2` via `src/services/SearchService.ts`
- Bug report: users searching for "résumé" or "piñata" get 0 results, but "resume" and "pinata" work
- Likely cause: missing Unicode normalization or analyzer configuration

## Requirements
1. Investigate whether the Elasticsearch analyzer on `products_v2` supports Unicode folding
2. Add ICU folding analyzer if missing, or fix the query builder in `SearchService.buildQuery()`
3. Ensure searches for "cafe" also match "café" (accent-insensitive search)
4. Add test cases for accented character queries

## Success Criteria
1. `GET /api/search?q=café` returns the same results as `q=cafe`
2. Existing search functionality unchanged for ASCII queries
3. All search-related tests pass
```

**Techniques applied**: Specificity (exact reproduction), Context Injection (file paths, service names), Verification Criteria

---

## Example 3: "Refactor This" → Specific Refactoring with Scope

### Before (Score: 3/15)
```
Refactor the user service, it's a mess
```

### After (Score: 14/15)
```
## Goal
Extract validation, notification, and persistence logic from `UserService` into focused, single-responsibility classes.

## Context
`UserService.ts` (currently 847 lines) handles user CRUD, email validation, password hashing, 
welcome email sending, audit logging, and profile image upload. It violates SRP and is hard to test.

## Scope
### In Scope
- Split `UserService.ts` into:
  - `UserService.ts` — orchestration only (create, update, delete flows)
  - `UserValidator.ts` — email format, password strength, uniqueness checks
  - `UserNotifier.ts` — welcome email, password reset email
  - `UserRepository.ts` — database operations (already partially exists)
- Update dependency injection registrations in `src/config/di.ts`
- Update existing tests to use the new class structure

### Out of Scope
- Do NOT change the public API contract (controller layer stays the same)
- Do NOT modify `UserController.ts` beyond updating the injected service
- Do NOT change database schema or migrations
- Do NOT optimize queries (separate task)

## Constraints
- Each new class must have its own interface (e.g., `IUserValidator`)
- Use constructor injection, not service locator
- Keep method signatures compatible — the controller should not change

## Success Criteria
1. `UserService.ts` reduced to <150 lines (orchestration only)
2. Each extracted class has focused unit tests
3. All existing integration tests pass without modification
4. Zero circular dependencies between the new classes
5. `dotnet build` and `dotnet test` pass cleanly
```

**Techniques applied**: Structure, Scope Bounding (explicit in/out), Constraint Definition, Verification Criteria, Specificity

---

## Example 4: UI Request → Detailed Component Specification

### Before (Score: 4/15)
```
Make a nice settings page
```

### After (Score: 14/15)
```
## Goal
Create a Settings screen with grouped preference controls using UI Toolkit.

## Context
- The app uses Unity 6 with UI Toolkit for runtime UI
- Existing screens follow the pattern in `Assets/UI/Screens/ProfileScreen/` (UXML + USS + C# controller)
- Design tokens are in `Assets/UI/Themes/tokens.uss`
- The ScreenManager at `Assets/Scripts/UI/ScreenManager.cs` handles navigation

## Requirements
1. Create `SettingsScreen.uxml` with these groups:
   - **Audio**: Master Volume (slider 0-100), Music (toggle), SFX (toggle)
   - **Display**: Resolution (dropdown), Fullscreen (toggle), VSync (toggle)
   - **Account**: Username (label), Logout (button)
2. Create `SettingsScreen.uss` using existing design tokens for colors, spacing, typography
3. Create `SettingsScreenController.cs` inheriting from `BaseScreenController`
4. Bind controls to `PlayerPrefs` for persistence
5. Add a back button that calls `ScreenManager.NavigateBack()`

## Constraints
- Follow the UXML/USS/C# triad pattern from `ProfileScreen`
- Use semantic USS class names (e.g., `.settings-group`, `.settings-label`)
- Do NOT use inline styles in UXML
- Support both mouse and gamepad navigation (use `focusable="true"` on interactive elements)

## Success Criteria
1. Screen renders correctly at 1920x1080 and 1280x720
2. All controls read/write PlayerPrefs on value change
3. Back button returns to the previous screen
4. USS uses only tokens from `tokens.uss` — no hardcoded colors
```

**Techniques applied**: Context Injection (existing patterns, file paths), Structure, Example Seeding (UI groups), Constraint Definition, Verification Criteria

---

## Example 5: Performance Issue → Structured Optimization Prompt

### Before (Score: 4/15)
```
The game is lagging, please optimize it
```

### After (Score: 13/15)
```
## Goal
Reduce frame time spikes during combat from 45ms+ to consistently under 16.6ms (60 FPS target).

## Context
- Unity 6 project targeting mobile (iOS/Android) with URP
- Profiler shows spikes during combat when 10+ enemies are on screen
- Main suspects: `EnemyAI.Update()` doing per-frame raycasts and `DamageNumberManager` instantiating/destroying TextMeshPro objects every hit
- Combat system: `Assets/Scripts/Combat/`
- Enemy AI: `Assets/Scripts/AI/EnemyAI.cs`

## Requirements
1. Profile `EnemyAI.Update()` — replace per-frame raycasts with interval-based checks (every 0.2s)
2. Implement object pooling for damage number popups using Unity's `ObjectPool<T>`
3. Audit `CombatManager.ProcessHits()` for GC allocations — eliminate `List<T>` allocations in hot path
4. Verify with Unity Profiler: no frame exceeds 16.6ms with 15 enemies active

## Constraints
- Do NOT change combat gameplay feel (timing, damage values stay the same)
- Use Unity's built-in `ObjectPool<T>` — no third-party pooling libraries
- Keep AI behavior identical — only change execution frequency, not logic

## Success Criteria
1. Profiler shows no frames above 16.6ms in 60-second combat test with 15 enemies
2. GC allocations during combat: 0 per frame (excluding initialization)
3. All combat unit tests pass
4. No visual difference in AI behavior or damage numbers
```

**Techniques applied**: Specificity (exact measurements), Context Injection (profiler findings), Constraint Definition, Verification Criteria, Chain-of-Thought (numbered steps)

---

## Example 6: "Fix the Tests" → Targeted Test Repair

### Before (Score: 3/15)
```
Fix the tests, they're failing
```

### After (Score: 13/15)
```
## Goal
Fix 3 failing tests in the `OrderService` test suite caused by the recent shipping calculator refactor.

## Context
- `npm test -- --testPathPattern=OrderService` shows 3 failures:
  1. `OrderService.calculateTotal › should include shipping for orders under $50` — expected 54.99, got 49.99
  2. `OrderService.calculateTotal › should apply free shipping over $50` — expected 55.00, got 60.00
  3. `OrderService.applyDiscount › should calculate discount before shipping` — assertion on shipping amount fails
- Root cause: `ShippingCalculator.getRate()` signature changed from `(subtotal: number)` to `(order: Order)` in PR #234
- Test file: `src/services/__tests__/OrderService.test.ts`
- Implementation: `src/services/OrderService.ts`, `src/services/ShippingCalculator.ts`

## Requirements
1. Update the mock for `ShippingCalculator.getRate()` in the test file to match the new signature
2. Update test assertions to reflect the new shipping logic (free shipping threshold moved from $50 to $75)
3. Verify no other test files mock `ShippingCalculator`

## Constraints
- Only modify test files — the implementation in `ShippingCalculator.ts` is correct
- Do NOT change the shipping threshold values — they are intentional business logic changes
- Keep test descriptions accurate to what they're testing

## Success Criteria
1. `npm test -- --testPathPattern=OrderService` — all tests pass
2. `npm test` — full suite passes (no regressions)
3. Test descriptions match actual test behavior
```

**Techniques applied**: Specificity (exact error messages), Context Injection (root cause, PR reference), Scope Bounding (tests only), Verification Criteria

---

## Example 7: Natural Language → Technical Specification

### Before (Score: 5/15)
```
I want users to be able to invite their friends to the app
```

### After (Score: 14/15)
```
## Goal
Implement a friend invitation system that lets users send invite links via email or shareable URL.

## Context
- Auth system: Firebase Auth (`src/services/AuthService.ts`)
- User model: `src/models/User.ts` — has `id`, `email`, `displayName`, `referralCode` (exists but unused)
- Email service: SendGrid via `src/services/EmailService.ts` (already configured)
- No existing invitation logic

## Requirements
1. Generate a unique invite link per user using their `referralCode`: `https://app.example.com/invite/{referralCode}`
2. Create `InvitationService.ts` with methods:
   - `generateInviteLink(userId: string): string`
   - `sendInviteEmail(fromUserId: string, toEmail: string): Promise<void>`
   - `redeemInvite(referralCode: string, newUserId: string): Promise<void>`
3. Create `POST /api/invitations/send` endpoint accepting `{ email: string }`
4. Create `GET /api/invitations/redeem/:code` endpoint for link clicks
5. Track invitations in a new `invitations` DB table: `id`, `inviter_id`, `invitee_email`, `status`, `created_at`, `redeemed_at`
6. Add "Invite Friends" button to the profile screen that opens a share sheet (mobile) or copy-link dialog (web)

## Constraints
- Rate limit: max 10 invites per user per day
- Do NOT auto-create accounts from invites — just track the referral for when they sign up
- Use existing `EmailService` — do NOT add new email providers
- Follow existing controller/service/repository pattern

## MUST NOT DO
- Do NOT send invite emails without rate limiting
- Do NOT expose user emails in the invite link or API responses

## Success Criteria
1. User can generate and copy an invite link
2. User can send invite email — recipient receives it within 30 seconds
3. When invitee signs up via link, `invitations` table records the referral
4. Rate limiting blocks the 11th invite in a 24-hour window with a clear error message
5. All new endpoints have integration tests
```

**Techniques applied**: Full Structure, Context Injection, Constraint Definition, Scope Bounding, Verification Criteria, Chain-of-Thought Decomposition

---

## Example 8: Ambiguous Multi-Task → Focused Single Prompt

### Before (Score: 3/15)
```
The dashboard needs work. It's slow, the charts look bad, and we need to add a date filter. 
Also the export button doesn't work on Firefox.
```

### After — Split into focused prompt (showing one) (Score: 13/15)
```
## Goal
Add a date range filter to the analytics dashboard that filters all chart data.

## Context
- Dashboard: `src/pages/Dashboard.tsx`
- Charts fetch data from `GET /api/analytics/summary?period=30d` via `useAnalyticsData()` hook
- Currently hardcoded to 30 days — no user-selectable range
- Using recharts for visualization, date-fns for date manipulation

## Requirements
1. Add a date range picker component above the charts (use `react-date-range` — already in package.json)
2. Update `useAnalyticsData()` hook to accept `startDate` and `endDate` parameters
3. Update API call to pass `?start={ISO}&end={ISO}` query parameters
4. Default range: last 30 days (matches current behavior)
5. Preset options: "Last 7 days", "Last 30 days", "Last 90 days", "Custom range"
6. Persist selected range in URL query params for shareable links

## Constraints
- The API already supports `start` and `end` query params — no backend changes needed
- Do NOT modify chart components — only change the data they receive
- Date picker must be keyboard accessible

## Success Criteria
1. Selecting "Last 7 days" updates all charts to show 7-day data
2. Custom range with future dates shows appropriate "No data" state
3. Refreshing the page preserves the selected date range from URL
4. Default behavior (no URL params) matches current 30-day view exactly

---
NOTE: The other issues (performance, chart styling, Firefox export bug) should be 
separate prompts — each with their own Goal, Scope, and Success Criteria.
```

**Techniques applied**: Scope Bounding (split multi-task), Structure, Specificity, Context Injection, Verification Criteria
