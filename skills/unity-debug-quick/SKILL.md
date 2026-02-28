---
name: unity-debug-quick
description: "Investigate Unity issues, diagnose errors, propose solutions, let user pick one, then delegate the fix to a sub-agent. Loops until user stops. Use when: (1) Console shows compiler errors or runtime exceptions, (2) Build fails or Play Mode is broken, (3) Tracing data flow to find where things go wrong, (4) Understanding why a value is wrong or null, (5) Explaining lifecycle or timing issues, (6) Assembly definition or package import errors, (7) Want proposed solutions and interactive fix application. Triggers: 'fix error', 'compiler error', 'CS0', 'NullReferenceException', 'MissingReferenceException', 'build failed', 'play mode broken', 'stack trace', 'exception', 'runtime error', 'console error', 'script error', 'assembly error', 'serialization error', 'missing script', 'broken prefab', 'fix this', 'not compiling', 'asmdef error', 'package error', 'type not found', 'namespace missing', 'explain why', 'why does this happen', 'what causes this', 'trace this issue', 'why is this null', 'debug and fix'."
---

# Unity Debug Quick

Investigate the issue. Output the tree. Ask user to pick a solution. Delegate the fix. Repeat until user stops. Handles both behavioral bugs and compiler/runtime errors — from NullReferenceException to build failures.

## Output Format

Use the Vercel-themed tree template from `references/output-template.md` for every response. Tree connectors (`├──`, `└──`) for flow, repro, verify, prevent, and solutions. Inline code (`cyan`) for all code identifiers, file refs, and values. **Bold** for failure points and labels. Emoji indicators for severity. No prose, no preamble — just the formatted tree, then the interactive prompt.

## Workflow

Follow [references/workflow.md](references/workflow.md) for the 7-step investigation flow (Parse → Read → Trace → Assess → Solve → Output → Fix Loop).

Use [../unity-shared/references/debug-tool-selection.md](../unity-shared/references/debug-tool-selection.md) for tool choices. Chain tools to build evidence. Stop once root cause is clear.

## Rules

- **Investigation is READ-ONLY**: Never edit project files during investigation phase.
- **Fix ONLY the reported issue**: Don't refactor surrounding code. Minimal, targeted fixes.
- **No commits**: No git operations.
- **Direct answer**: No report documents — answer in conversation.
- **Minimum 2 solutions**: Always propose 2-4 solutions.
- No preamble, no narration. Investigate directly, output the tree.
- Cite `File.cs:L##` inline throughout. No separate refs section.
- Code snippets only when they clarify — never dump full methods.
- Focus on the path that explains root cause. Don't explain everything.
- If uncertain, state "uncertain: {reason}" inside the tree and note what info would help.
- After the tree, ALWAYS present the interactive choice prompt. Ask user which solution to apply.
- When user picks a solution, delegate via `task()` with appropriate category and `load_skills=["unity-code-quick"]`. Never apply fixes directly.
- After fix delegation completes, verify with `lsp_diagnostics` then ask if there are more issues. Loop until user stops.

## Reference Files
- [output-template.md](references/output-template.md) — Vercel-themed tree output template
- [workflow.md](references/workflow.md) — 7-step investigation flow
- [debug-tool-selection.md](../unity-shared/references/debug-tool-selection.md) — Tool lookup table
- [debug-fix-loop.md](../unity-shared/references/debug-fix-loop.md) — Delegation and iteration workflow
 [common-fixes.md](../unity-shared/references/common-fixes.md) — Known fix patterns for common Unity errors
