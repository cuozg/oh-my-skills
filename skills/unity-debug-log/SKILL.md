---
name: unity-debug-log
description: >
  Use this skill to generate formatted Debug.Log snippets for copy-paste — [DBG] prefix, color tags,
  string interpolation, wrapped in #if UNITY_EDITOR guards. Read-only: never writes to project files.
  Use when the user needs quick log statements to trace values, says "add some debug logs," "I need to
  trace this value," "give me logging for this method," or wants color-coded console output to diagnose
  runtime behavior.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-debug-log

Generate formatted Debug.Log snippets ready for manual copy-paste — never modifies project files directly.

## When to Use

- Need a quick log statement to trace a value at a specific point
- Want color-coded, prefixed logs to stand out in the Console
- Generating log wrappers for methods, coroutines, or event handlers
- Adding temporary instrumentation without modifying file structure

## Workflow

1. **Identify** — determine what value/event/method to trace and in which class/method
2. **Format** — apply [DBG] prefix, color tag, string interpolation, and UNITY_EDITOR guard
3. **Output** — print the snippet as a code block (do not write to any project file)

## Rules

- Never write snippets to project files — output only as text
- Always prefix with `[DBG]` followed by class and method name
- Always wrap in `#if UNITY_EDITOR` / `#endif` unless user requests permanent logs
- Use `$"..."` string interpolation, not string concatenation
- Apply `<color=X>` tag to the prefix; keep message body uncolored for readability
- Use `Debug.LogWarning` for unexpected-but-handled states, `Debug.LogError` for failures
- Include the calling context (`this.name`, index, or key) when logging inside loops
- Keep each snippet self-contained — no helper methods unless requested
- Do not suggest permanent logging infrastructure (that belongs in unity-code-quick)
- Load format examples if color codes or compound formats are needed

## Output Format

Formatted code block(s) — copy-paste ready. Text output only.

## Standards

Load `unity-standards` for logging guidance. Key references:

- `debug/log-format.md` — [DBG] prefix, color tags, UNITY_EDITOR guard
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, physics

Load via `read_skill_file("unity-standards", "references/debug/<file>")`.
