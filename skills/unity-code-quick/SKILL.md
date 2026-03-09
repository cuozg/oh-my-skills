---
name: unity-code-quick
description: Use whenever the user wants a small Unity runtime C# change that should stay inside one .cs file — a MonoBehaviour, ScriptableObject, interface, enum, struct, data model, static helper, or a narrow edit to an existing runtime script. Reach for it even when they ask for a quick script or one-file fix. Do not use it for editor tooling, UI Toolkit, tests, optimization-only passes, or anything that needs multiple files or architecture planning.
metadata:
  author: kuozg
  version: "1.2"
---

# unity-code-quick

Deliver small runtime Unity C# work that stays inside one file. Match local patterns first, keep the diff narrow, and finish with a compilable handoff.

## When to Use

- New runtime MonoBehaviour, ScriptableObject, interface, enum, struct, or utility class
- Narrow change to one existing runtime `.cs` file
- Boilerplate, data-model work, or a bug fix that stays correct without adding files, editor code, or tests

## Do Not Use

- Editor tooling, inspectors, drawers, gizmos, menu items → `unity-code-editor`
- UI Toolkit screens or styling → `unity-uitoolkit-create`
- Unit tests → `unity-test-unit`
- Multi-file features, refactors, or cross-system wiring → `unity-code-deep`
- Optimization-only cleanup with no behavior change → `unity-code-optimize`

## Workflow

1. **Qualify** — Confirm one runtime `.cs` file is enough. If the work spills into more files or another domain, switch skills.
2. **Discover** — Read the target file plus 1-2 nearby runtime files for namespace, usings, field order, attributes, and serialization style.
3. **Implement** — Make the smallest complete change that satisfies the request.
4. **Verify** — Run diagnostics on the changed file and fix introduced issues.
5. **Handoff** — Report the changed path, what changed, diagnostics status, and any Unity Editor follow-up.

## Rules

- Keep the change inside one `.cs` file. Do not create helper files, tests, or editor code.
- Match existing namespace, access modifier, attribute, and serialization patterns before falling back to `unity-standards`.
- If the repo is silent, prefer explicit `using` directives and inspector-friendly serialized fields that match surrounding style.
- Keep the surface minimal. Do not invent namespaces, XML docs, attributes, or extra polish unless the prompt or nearby files justify them.
- Add XML docs only for public API that benefits from them. Skip noise comments.
- For bug fixes or narrow edits, change only the necessary code path; do not refactor adjacent systems.
- Never leave `TODO`, placeholder logic, or partially wired code.
- If the request is ambiguous, choose the simplest runtime implementation that fully satisfies it.

## Standards

Load `unity-standards` only for the references the task needs:

- `references/code-standards/single-file-runtime-workflow.md` — routing, scope checks, local pattern capture, handoff
- `references/code-standards/code-patterns.md` — MonoBehaviour, ScriptableObject, interface, UnityEvent templates
- `references/code-standards/naming.md` — file, type, member naming
- `references/code-standards/serialization.md` — `[SerializeField]`, `[field: SerializeField]`, SO data
- `references/code-standards/null-safety.md` — guards, `TryGet`, nullable handling
- `references/code-standards/lifecycle.md` — Unity message order, coroutine rules

Load via `read_skill_file("unity-standards", "references/<path>")`.
