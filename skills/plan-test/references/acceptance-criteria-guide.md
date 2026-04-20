# Acceptance Criteria Guide

A criterion is **testable** when a third party, reading only the goal file and
the repo, can decide `met / partial / unmet` without asking the author. Use
this guide when writing or reviewing the `## Acceptance Criteria` section of
any goal file under `Docs/Goals/<feature>/<task>.md`.

---

## The Testability Rule

> Every criterion names **what**, **where**, and **how to observe it**.

If any of those three are missing, the criterion is not testable — it is a
wish. Split it or rewrite it.

---

## Good vs Bad Criteria

| Bad | Why it fails | Good |
|-----|--------------|------|
| Search should be fast | No threshold, no workload | Query p95 latency **< 200ms** for **10k indexed docs** under `tests/perf/search.bench.ts` |
| API works correctly | No endpoint, no response shape | `GET /api/search?q=<term>` returns `200` with body `{results: [{id, title, snippet}]}` |
| Handles errors | No error class, no behavior | Empty `q` returns `400` with `{error: "query required"}` |
| Code is clean | Subjective | `src/search/indexer.ts` passes `eslint --max-warnings 0` |
| Well tested | No target | Every exported function in `src/search/**` has a matching `*.test.ts` |
| Feature is documented | No location | `README.md` has a `## Search` section and `docs/api.md` lists the new endpoint |
| Works on mobile | No breakpoint, no device | Layout renders without horizontal scroll at viewport width **375px** on `/search` route |
| Secure | No threat named | Anonymous requests to `POST /api/index/rebuild` return `401` |

### The Transformation

For each bad criterion, apply this recipe:

1. **Name the artifact.** File path, endpoint, command, UI route.
2. **State the observable.** HTTP code, returned fields, log line, exit code, pixel position.
3. **Fix the threshold.** Numeric bound, exact string, enumerated value.
4. **Point at the verifier.** Test file, manual step, benchmark, linter.

---

## Verification Patterns by Criterion Type

The `verify_implementation.py` script uses these patterns. Write criteria that
match them, and automated verification works out of the box.

### 1. API behavior

> `GET /api/search?q=<term>` returns `200` with `{results: [...]}`.

**Verifier looks for:**
- Route string (`/api/search`) in source
- HTTP method handler (`router.get`, `app.get`, `@app.route`)
- Matching test file (`tests/search.test.ts`)

**Tip:** Always quote the path in backticks and include the HTTP method.

### 2. File existence

> `src/search/indexer.ts` exists and exports `class Indexer`.

**Verifier looks for:**
- Literal path resolves inside repo
- Symbol (`Indexer`) appears in that file

**Tip:** Use full repo-relative paths, not "the indexer".

### 3. Config / constant values

> `MAX_QUERY_LENGTH` in `src/search/config.ts` equals `256`.

**Verifier looks for:**
- Symbol appears in source with the stated literal

**Tip:** Name the exact identifier — `MAX_QUERY_LENGTH`, not "the limit".

### 4. UI state

> Route `/search` renders `<SearchInput>` with placeholder text **"Search docs…"**.

**Verifier looks for:**
- Component name in source
- Literal placeholder string quoted

**Tip:** Pin UI criteria to a route and a component, not a "page".

### 5. Error handling

> Calling `indexDocument(null)` throws `InvalidDocumentError`.

**Verifier looks for:**
- Error class name in source
- Test file referencing the error class

**Tip:** Name the exception class; never say "throws an error".

### 6. Performance

> `searchQuery()` p95 < **200ms** across **10000** indexed docs, measured by `tests/perf/search.bench.ts`.

**Verifier looks for:**
- Benchmark file exists
- Symbol appears in benchmark

**Tip:** Performance criteria **must** point at a benchmark file; otherwise
they become `❌ Unmet — no evidence` forever.

### 7. Security

> Anonymous `POST /api/index/rebuild` returns `401`.

**Verifier looks for:**
- Route handler
- Auth middleware symbol
- Test file asserting `401`

**Tip:** Name the status code and the unauthenticated actor.

### 8. Documentation

> `README.md` has a `## Search` section and `docs/api.md` lists `/api/search`.

**Verifier looks for:**
- Each named file exists
- Section heading / endpoint string appears inside

**Tip:** Pin doc criteria to files **and** headings.

---

## Criteria Count by Goal Scope

| Scope | Typical criteria count | Mode |
|-------|------------------------|------|
| Hotfix / small tweak | 2–5 | quick |
| Feature slice | 6–9 | quick or deep |
| Large feature / new subsystem | 10+ | deep |

A goal with **zero** acceptance criteria is not a goal — it's a note. Use
`plan-goal` to add criteria before running `plan-test`.

A goal with **>20** criteria is probably two goals. Split it.

---

## Checklist Before Running `plan-test`

- [ ] Every criterion starts with `- [ ]` or `- [x]` under `## Acceptance Criteria`
- [ ] Every criterion names at least one path, endpoint, symbol, or literal
- [ ] Performance criteria reference a benchmark file
- [ ] Security criteria name a status code or threat
- [ ] Doc criteria name the file **and** the section/heading
- [ ] No criterion uses the words *properly*, *correctly*, *well*, or *cleanly* without a concrete bound
