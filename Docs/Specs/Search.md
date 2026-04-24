# Search Feature Specification

## Status
Completed on 2026-04-24 for `[Search] Add Full-Text Search`.

## Overview
The Search feature provides a reusable Node service for one search entry point across published articles and public user profiles. The repository snapshot does not contain an application router or UI, so the feature is implemented as a library exported from `src/index.js:1` and `src/search/index.js:1-10`.

## Public API
Applications create a search function with `createSearchService({ providers })` from `src/search/searchService.js:6`. The service validates a query, loads searchable article and profile records in parallel through provider methods, runs each domain searcher, and returns one response containing combined and per-type result collections from `src/search/searchService.js:23-37`.

The package-level export re-exports the search module from `src/index.js:1`. The search module exports article search, profile search, in-memory providers, the service factory, result constants, search states, and query validation from `src/search/index.js:1-10`.

## Search Flow
1. `createSearchService` validates the provider shape before returning a search function (`src/search/searchService.js:6-8`, `src/search/searchService.js:41-48`).
2. Each search call validates and tokenizes the query (`src/search/searchService.js:9-10`, `src/search/validateSearchQuery.js:4-20`).
3. Invalid blank queries return an `invalid-query` response without calling providers (`src/search/searchService.js:12-21`).
4. Valid queries call both provider boundaries in parallel (`src/search/searchService.js:23-26`).
5. Article and profile records are searched independently (`src/search/searchService.js:28-29`).
6. The response includes `results`, `articles`, `profiles`, and `meta` counts (`src/search/searchService.js:51-67`).

## Result Model
Search result types are explicit constants: `article` and `profile` (`src/search/searchTypes.js:1-2`). Search states are `results`, `no-results`, and `invalid-query` (`src/search/searchTypes.js:4-8`).

Article results include `type`, `id`, `slug`, `title`, `excerpt`, `url`, `score`, and `matchedFields` (`src/search/articleSearch.js:31-40`). Profile results include `type`, `id`, `username`, `displayName`, `bio`, `url`, `score`, and `matchedFields` (`src/search/profileSearch.js:32-41`).

## Full-Text Matching
Article search uses weighted full-text fields for `title` and `body` (`src/search/articleSearch.js:5-8`). Profile search uses weighted fields for `displayName`, `username`, and `bio` (`src/search/profileSearch.js:5-9`).

The full-text scorer normalizes text, tokenizes alphanumeric terms, applies lightweight stemming, scores exact/prefix/substring token matches, and adds a phrase score when the normalized field contains the normalized query (`src/search/fullText.js:3-12`, `src/search/fullText.js:14-28`, `src/search/fullText.js:30-55`, `src/search/fullText.js:58-80`).

## Ranking
Each supported content type is ranked independently by descending relevance score, with stable ID ordering for ties (`src/search/articleSearch.js:17-20`, `src/search/profileSearch.js:18-21`, `src/search/fullText.js:83-89`).

The unified response concatenates already-ranked article and profile arrays while preserving the separate `articles` and `profiles` collections for UI rendering (`src/search/searchService.js:51-61`).

## Validation And Empty States
Blank or whitespace-only queries produce `ok: false`, an empty normalized query, no terms, and the shared validation error (`src/search/validateSearchQuery.js:4-14`, `src/search/searchTypes.js:10`). The service short-circuits before provider calls and returns empty result arrays (`src/search/searchService.js:12-21`).

Queries with no matching article or profile results return `ok: true` and `state: "no-results"` rather than throwing (`src/search/searchService.js:31-36`).

## Provider Boundaries And Visibility
The default in-memory providers expose `getSearchableArticles` and `getSearchableProfiles` methods (`src/search/searchProviders.js:1-14`). They return new shallow copies of records instead of source object references (`src/search/searchProviders.js:8-12`, `src/search/searchProviders.js:32-34`).

Default article visibility requires records to be searchable, published when a status exists, and public when a visibility value exists (`src/search/searchProviders.js:17-23`). Default profile visibility requires records to be searchable and public when a visibility value exists (`src/search/searchProviders.js:25-30`).

Production repositories can replace the in-memory providers as long as they preserve the same boundary: provider methods return only records the current user may search, and the search service handles validation, matching, ranking, and response shape.

## Tests And Verification
The service unit tests cover one-entry-point mixed results, typed results, no-results responses, and blank-query provider short-circuiting (`src/search/searchService.test.js:6-25`, `src/search/searchService.test.js:27-45`, `src/search/searchService.test.js:47-62`, `src/search/searchService.test.js:64-82`).

The integration test verifies visible article/profile fixtures are searchable, draft/private records are excluded, and source fixture data is not mutated (`src/search/search.integration.test.js:8-22`).

Verification commands for the completed goal:
- `npm test` passed with 7 test files and 14 tests.
- `npm run test:coverage` passed with 96.75% statement coverage and 81.15% branch coverage.
- `node --check` over changed JavaScript files passed.

## Extension Points
Database-backed apps should implement provider methods with native full-text indexes or query builders while keeping the same `getSearchableArticles` and `getSearchableProfiles` contract. UI layers should render from the `results` array when they need one unified list, or from `articles` and `profiles` when they need per-type sections.
