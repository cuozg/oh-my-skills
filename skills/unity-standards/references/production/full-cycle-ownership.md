# Full-Cycle Unity Feature Ownership

Use this when a Unity task touches product goals, analytics, LiveOps, remote
config, server APIs, IAP, release readiness, post-launch monitoring, or systems
that must scale after the first implementation ships.

## Ownership Standard

A feature is not done just because code compiles, QA passes, or a build ships.
Treat it as done when players can use it smoothly, analytics are trustworthy,
performance is stable on target devices, LiveOps can operate it, and the system
can scale without immediate rework.

Before implementation, identify:

- Product goal: why the feature exists, target KPI, and success signal.
- Runtime owner: which client system owns state and transitions.
- Data owner: client save, remote config, backend, or server response.
- Operational owner: who can tune, disable, roll out, or recover the feature.
- Evidence owner: which logs, analytics, dashboards, tests, or profiler captures
  prove success after release.

## GDD And Technical Design

For non-trivial features, read the GDD, task, or goal file before code. Ask
direct questions in the source document or final response when requirements,
edge cases, ownership, or dependencies are unclear.

Technical design should cover:

- Client flow: local actions, runtime state, UI, errors, loading, and fallback.
- Player model: saved data only, default values, versioning, and migration.
- Config or blueprint: required fields, validation, refresh path, missing-data
  behavior, and rollback strategy.
- Server API: request/response shape, retries, idempotency, auth, error classes,
  and authoritative fields.
- Backend/data dependency: persistence, validation, economy integrity, and
  client/server separation.
- Integration points: analytics, assets, LiveOps controls, QA, release, and
  monitoring.

Do not estimate directly from a feature title. Break the work into UI, client
logic, backend/API, data/config, assets, analytics, QA, release, and monitoring
tasks, then add buffer for review, integration, bug fixing, and unclear
dependencies.

## Analytics Ownership

Analytics are production behavior, not a logging afterthought.

- Clarify each event's meaning, trigger timing, parameters, and owner.
- Validate event schema, required parameters, enum/string values, and data types.
- Prevent duplicate, missing, or out-of-order events during retries, offline
  flows, scene transitions, and repeated button taps.
- Keep revenue, purchase validation, install attribution, and other critical
  business events server-authoritative whenever the product has backend support.
- After release, monitor dashboards or raw live data for abnormal drops, spikes,
  missing events, or rollout mismatches.

Bad analytics can make a good feature look broken or cause wrong LiveOps and UA
decisions. If requirements are unclear, ask instead of inventing event meaning.

## LiveOps, Remote Config, And Blueprints

Config-driven architecture should speed iteration without moving broken state
into production.

- Prefer data/config for tuning, economy values, feature gates, and content that
  LiveOps must adjust without a binary release.
- Validate config before applying it. Keep the previous valid state when a new
  payload is missing, malformed, expired, or incompatible.
- Define default values, required fields, expired-data cleanup, version
  compatibility, and missing-config behavior.
- Avoid hardcoded logic when the requirement is explicitly LiveOps-driven, but do
  not over-configure one-off behavior.
- Keep config size and runtime post-processing measured. Large JSON payloads,
  dictionary generation, sorting, and dependency resolution can hurt startup.
- For long-running progression, store compact state and generate repeated or
  predictable data from templates instead of persisting infinite per-level data.

## Server API And Failure Behavior

Server integration must stay responsive under failure.

- Retry only idempotent operations unless the backend contract explicitly
  supports safe retry for the transaction.
- Separate network errors, timeouts, authentication errors, and business-rule
  errors because the UI response differs.
- Run independent requests in parallel only when the user flow and backend
  contract allow it; keep dependent requests ordered.
- Show loading or disabled interaction for active server operations so users do
  not perceive a frozen screen or double-submit an action.
- Hydrate local state from authoritative server responses when the backend owns
  the result. Do not recompute a different local truth in callbacks.

## Release, Compliance, And Monitoring

Release readiness includes build, store, and live checks:

- Confirm CI/build pipeline impact: version control, build automation,
  Addressables/bundles, distribution, and store release steps.
- For IAP, billing, privacy, tracking, or store-review behavior, verify current
  requirements from official sources via `../other/official-source-map.md`.
- Keep release notes, screenshots, preview media, disclosures, and IAP metadata
  aligned with actual gameplay and platform policy.
- Preserve crash symbolication and breadcrumbs for critical flows so Crashlytics,
  Bugsnag, Play Console, or equivalent tools can identify regressions.
- For crashes and ANRs, correlate stack traces with player actions, analytics,
  memory-heavy screens, asset loading, scene transitions, and network failures.
- State the post-release watch plan for risky features: dashboards, error rates,
  economy metrics, crash-free sessions, remote config rollout, and rollback path.

## Tradeoff Framing

When timeline and scope conflict, present options with consequences:

- Reduce scope: keep the core user value, cut non-essential polish or variants.
- Parallelize safely: split independent client, backend, asset, and QA tasks.
- Reuse systems: prefer proven local infrastructure over a new subsystem.
- Temporary workaround: acceptable only when risk, debt, owner, and cleanup path
  are explicit.
- Scalable fix: use when the feature is likely to grow, repeat, or become a
  LiveOps dependency.

Do not just report that a timeline is impossible. Provide a smaller deliverable,
an alternative solution, or a risk-managed tradeoff.

## Verification

Use the narrowest proof that covers the production surface:

- Product behavior: Play Mode, scene/prefab inspection, screenshots, or device
  smoke check for the user flow.
- Analytics: schema check, duplicate/missing event test, local capture, or live
  dashboard/raw event verification after rollout.
- Config/LiveOps: valid, missing, expired, malformed, rollback, and refresh paths.
- Server API: success, timeout, network failure, business error, retry, and
  double-submit paths.
- Performance: startup timeline, frame time, draw calls, memory, GC, bundle size,
  download size, or target-device measurement.
- Release: CI/build result, Addressables/content update validation, store/billing
  compliance source check, crash symbolication, and monitoring/rollback plan.
