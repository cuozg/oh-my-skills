# Single-File Runtime Workflow

## Route Before Writing

- One runtime `.cs` file or narrow bug fix → `unity-code` (Quick mode)
- 2+ runtime files, new abstractions, or registration steps → `unity-code` (Deep mode)
- Editor tooling or inspectors → `unity-code` (Editor mode)
- UI Toolkit screens or styling → `unity-uitoolkit`
- Tests → `unity-test-unit`
- Optimization-only cleanup with no behavior change → `unity-code` (Optimize mode)

## Scope Checklist

- [ ] Runtime code only
- [ ] One `.cs` file is enough
- [ ] No extra helper, editor, or test files needed
- [ ] No new scene, prefab, or bootstrap wiring beyond what one file can expose
- [ ] Request is implementation, not architecture planning

## Local Pattern Capture

Read the target file or 1-2 nearby runtime files before writing. Match:

- Namespace and folder conventions
- Explicit `using` directives already present
- Field ordering and access modifiers
- Serialized-field pattern: `[SerializeField] private` vs `[field: SerializeField]`
- Attribute usage such as `RequireComponent`, `Header`, and `Tooltip`
- XML doc and comment density

If the repo is silent, prefer explicit usings, clear access modifiers, and inspector-friendly serialized data.

## Implementation Rules

- One type per file; file name matches type name
- Solve the requested behavior completely inside the file
- Narrow bug fix: change the smallest correct code path; skip opportunistic refactors
- Keep the surface minimal; avoid invented namespaces, XML docs, attributes, or helper polish unless the prompt or local files call for them
- Keep public API only where the request needs it
- No `TODO`, stubs, placeholder returns, or “wire this later” notes

## Verification & Handoff

- Run diagnostics on the changed file
- Confirm no accidental second file or editor dependency was introduced
- Report the changed path, what changed, diagnostics status, and any Unity Editor follow-up such as inspector assignment or asset creation
