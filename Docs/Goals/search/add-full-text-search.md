---
status: completed
priority: high
created: 2026-04-13
updated: 2026-04-24
completed: 2026-04-24
depends_on: []
---

# [Search] Add Full-Text Search

## Objective
Add a search feature to the app that supports full-text search across both articles and user profiles so users can find published content and relevant people from a single search experience.

## Context
The request is to add a high-priority search capability spanning two content domains: articles and user profiles. Project exploration found a JavaScript/Node workspace with `package.json` at the repository root, an existing goals registry at `Docs/Goals/Master.md`, and no current `src/` or `app/` application entrypoints checked into this repository snapshot. This goal should define the product and implementation boundaries clearly enough for execution once the app module or service boundaries are identified.

Relevant paths discovered during planning:
- `package.json` — confirms a JavaScript-based repository context
- `Docs/Goals/Master.md` — central goal registry that tracks this feature work
- `Docs/Goals/search/add-full-text-search.md` — goal definition for the new search feature

## Acceptance Criteria
- [x] Users can submit a search query from a single search entry point and receive combined results from both articles and user profiles in one response or unified results view
- [x] Article results are matched using full-text search against article title and body content, and profile results are matched using full-text search against display name, username, and bio fields
- [x] Search results clearly identify the result type (`article` or `profile`) so the UI can render the correct destination and presentation for each item
- [x] Results are ranked by relevance within each supported content type, and empty-result queries return a defined no-results state instead of an error
- [x] Search requests ignore empty or whitespace-only queries and return a validation error or no-op response without triggering a full search operation
- [x] The implementation does not remove or break existing article browsing or user profile discovery flows while adding the new search capability

## Constraints
- Must support both articles and user profiles in the same feature scope; do not ship article-only or profile-only search as the final result for this goal
- Must use full-text matching semantics rather than exact-match-only filtering
- Must preserve existing data models and public user/profile visibility rules when exposing search results
- Must keep the goal scoped to search behavior and result delivery, not unrelated recommendation, tagging, or analytics work

## Notes
- Non-interactive test assumption: the initial release should prioritize a single unified search experience over separate search screens for each content type
- Non-interactive test assumption: indexing strategy, storage engine, and UI framework can be chosen during implementation as long as the acceptance criteria remain satisfied
- If the application already has separate article and profile data services, prefer composing them behind a single search service or endpoint rather than duplicating query logic in multiple places
