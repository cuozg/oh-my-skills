---
name: unity-debug-explain
description: "Investigate Unity codebase to understand and explain issues, flows, or logic directly to the user. Reads code, traces execution, and delivers a clear explanation — never modifies code. Use when: (1) User asks 'why does X happen?', (2) Need to understand a bug or unexpected behavior, (3) Explaining how a system or feature works, (4) Tracing data flow from input to output, (5) Understanding why a value is wrong, (6) Explaining lifecycle or timing issues. Triggers: 'explain why', 'why does this happen', 'how does this work', 'explain this bug', 'what causes this', 'trace this issue', 'understand this behavior', 'why is this null', 'explain the flow', 'walk me through this'."
---

# Unity Debug Explain

**Input**: User question about code behavior, a bug, or how something works
**Output**: Direct explanation using the Response Template below. NEVER modify project files.

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Explain only.
- **Never commit**: No git operations.
- **Direct answer**: No report documents. Answer the user directly in conversation.
- **ALWAYS use template**: Follow the Response Template exactly.

## Workflow

1. **Parse Question** — What exactly does the user want to understand? Extract: the subject (class/method/system), the confusion (what vs why vs how), and the scope (single method vs cross-system).
2. **Read Code** — Open the relevant file(s). Read ±50 lines around the target. Understand the logic.
3. **Trace** — Follow the execution path. Use LSP tools to trace callers, definitions, references. Map the data flow from source to the point of confusion.
4. **Explain** — Deliver the answer using the Response Template. Be direct. Answer the question.

## Tool Selection

| Need | Tool |
|:---|:---|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find who calls it | `lsp_find_references` |
| Find symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| Broad sweep | `glob` |

Chain tools only when the first result doesn't fully answer the question. Stop the moment you can explain.

## Response Template

ALWAYS use this exact structure:

```
## Explanation: {Short title of what's being explained}

### What's Happening

{2-5 sentences explaining what the code actually does. Be specific — reference actual class names, method names, variable names. Cite with `FileName.cs:L##`.}

### Why

{2-5 sentences explaining WHY it works this way — the root cause, the design decision, or the bug. This is the core of the explanation.}

### Execution Flow

1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens at this step}
2. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens next}
3. ...{continue until the flow reaches the point of interest}

### Key Evidence

- **{Label}** — `File.cs:L##` — {the specific line/logic that proves the explanation}
- **{Label}** — `File.cs:L##` — {another piece of evidence if needed}

### Answer

{1-3 sentences directly answering the user's question. No hedging. If you're unsure, say so.}
```

## Template Rules

- **What's Happening**: Factual description. No speculation. Cite file:line.
- **Why**: The actual reason. Not "it might be" — trace it and prove it.
- **Execution Flow**: Numbered steps following actual call chain. Minimum 2 steps, maximum 8.
- **Key Evidence**: 1-3 items. Bold label + file:line + explanation. Only include evidence that supports the explanation.
- **Answer**: Direct answer to the user's original question. Start with the answer, not context.

## Rules

- Answer the question directly. No preamble, no narration.
- Cite with `FileName.cs:L##` inline throughout.
- Code snippets only when they clarify the explanation — never dump full methods.
- If the question spans multiple systems, focus on the path that answers the question. Don't explain everything.
- If you can't determine the answer with certainty, say "I'm not certain because {reason}" — never guess.
- If the question is actually a request to fix something, say so and suggest using `unity-debug-fix` or `unity-fix-errors` instead.
