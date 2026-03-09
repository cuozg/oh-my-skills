---
name: unity-code-quick
description: Use for small runtime Unity C# work that should stay in one .cs file — create or update a MonoBehaviour, ScriptableObject, interface, enum, struct, data model, or static helper, or add a narrow method to one existing runtime file. Reach for this on quick scripts, boilerplate, and one-file fixes. Do not use it for editor tooling, UI Toolkit, tests, or anything that needs 2+ files or architectural planning.
metadata:
  author: kuozg
  version: "1.1"
---

# unity-code-quick

Deliver small runtime Unity C# changes that fit one file. Match project conventions, keep the diff narrow, and finish with a clean compilable file.

## When to Use

- New runtime MonoBehaviour, ScriptableObject, interface, enum, struct, or utility class
- Small change to one existing runtime `.cs` file
- Boilerplate or data-model work that clearly fits one file
- Narrow bug fix where the correct fix stays inside one file

## Do Not Use

- Editor tooling, inspectors, drawers, gizmos, menu items → `unity-code-editor`
- UI Toolkit screens or styling → `unity-uitoolkit-create`
- Unit tests → `unity-test-unit`
- Multi-file features, refactors, or cross-system wiring → `unity-code-deep`

## Workflow

1. **Scope** — Confirm the request can be solved in one runtime file. If it spills into more files, switch skills.
2. **Discover** — Read the target file or 1-2 nearby files for naming, namespace, field, and attribute patterns.
3. **Implement** — Make the smallest complete change that satisfies the request.
4. **Verify** — Run diagnostics on the changed file. Fix every introduced issue before finishing.

## Rules

- Keep the change inside one `.cs` file. Do not create helper files, tests, or editor code.
- Match existing namespace, access modifier, attribute, and serialization patterns before falling back to `unity-standards`.
- Prefer explicit `using` directives; do not assume implicit usings.
- Use `[SerializeField] private` fields or `[field: SerializeField]` auto-properties to match the surrounding pattern.
- Add XML docs only for public API that benefits from them. Skip noise comments.
- Never leave `TODO`, placeholder logic, or partially wired code.
- If the request is ambiguous, choose the simplest runtime implementation that fully satisfies it.

## Output Format

Edit or create the actual `.cs` file. End with a short report: file path, what changed, diagnostics status.

## Standards

Load `unity-standards` for coding conventions. Read only what the task needs:

- `references/code-standards/code-patterns.md` — MonoBehaviour, ScriptableObject, interface, UnityEvent templates
- `references/code-standards/naming.md` — file, type, member naming
- `references/code-standards/serialization.md` — `[SerializeField]`, `[field: SerializeField]`, SO data
- `references/code-standards/null-safety.md` — guards, `TryGet`, nullable handling
- `references/code-standards/lifecycle.md` — Unity message order, coroutine rules

Load via `read_skill_file("unity-standards", "references/<path>")`.
