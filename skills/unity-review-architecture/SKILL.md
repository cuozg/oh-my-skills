---
name: unity-review-architecture
description: >
  Use this skill to review a GitHub PR for architectural concerns — dependency injection patterns, event
  systems, assembly boundaries, coupling, and SOLID principle violations. Use when a PR introduces new
  systems, services, or manager classes, or when the user says "review the architecture," "check the DI
  setup," "is this well-structured," or wants feedback on structural quality of a PR. Posts comments
  directly to the GitHub PR. Do not use for logic review — use unity-review-code-pr.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-review-architecture

Review a GitHub PR for architectural concerns: dependency injection, event systems, assembly boundaries, coupling, and SOLID principle violations — then post comments to the PR.

## When to Use

- A PR introduces new systems, services, or manager classes
- Changes touch assembly definitions, dependency injection setup, or event buses
- Suspecting tight coupling, circular dependencies, or God-object growth

## Workflow

1. **Fetch PR** — list changed files via `gh api repos/{owner}/{repo}/pulls/{pr}/files`
2. **Identify architecture files** — filter for `.cs`, `.asmdef`, `.asset`, dependency containers
3. **Read changed files** — load full content; trace public API surface changes
4. **Check DI** — verify dependencies injected via constructor or interface, not `GetComponent` chains
5. **Check events** — confirm event channels are typed ScriptableObjects or C# events; no static bus overuse
6. **Check assemblies** — `.asmdef` boundaries respected; no back-references from Runtime → Editor
7. **Check coupling** — measure fan-out; flag classes with 6+ direct dependencies
8. **Check SOLID** — single responsibility, open/closed, interface segregation violations
9. **Post comments** — build payload and submit via `gh api` (see `unity-standards/references/review/architecture-checklist.md`)

## Rules

- Flag `FindObjectOfType` or `GameObject.Find` in production code as CRITICAL
- Flag concrete class injection (not interface) as WARNING
- Flag assemblies with bidirectional references as CRITICAL
- Flag static singleton access from non-manager classes as WARNING
- Flag classes over 300 lines without clear single responsibility as NOTE
- Flag event systems without unsubscription as WARNING
- Never suggest rewriting entire systems — scope comments to the PR changes
- Use severity prefix: `[CRITICAL]`, `[WARNING]`, `[NOTE]` in every comment body
- Do not duplicate issues already flagged by unity-review-code-pr
- Post comments only; do not approve or request-changes

## Output Format

**MANDATORY**: Use `unity-standards/references/review/pr-submission.md` as the output template — JSON payload, event decision, batching rules, and gh CLI commands. All comments MUST be submitted in a single review `POST` call following that template exactly.

Architecture comments posted to the GitHub PR. Print a local summary with coupling metrics and any CRITICAL violations.

## Standards

Load `unity-standards` for architecture criteria. Key references:

- `review/pr-submission.md` — **MANDATORY** output template: JSON payload, event decision, batching, gh CLI
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern

Load via `read_skill_file("unity-standards", "references/<path>")`.
