---
name: unity-investigate
description: >
  Investigate Unity codebases — from quick Q&A to comprehensive system analysis reports. Auto-triages
  request complexity: simple questions (how does X work, what calls Y, trace this flow) get direct inline
  answers; complex requests (system analysis, pre-refactor audit, architecture investigation, team
  documentation) produce a structured markdown report with Mermaid diagrams, cited evidence, and risk
  tables. Use whenever the user asks "how does X work," "what calls this method," "trace the flow,"
  "explain this system," "investigate this architecture," "do a deep investigation," "I need an
  investigation report," "full analysis of this system," or any question about codebase structure and
  relationships. Also use when the user wants to understand an unfamiliar subsystem before modifying it.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-investigate

Investigate Unity codebases. Auto-triage into Quick (inline answer) or Deep (report with diagrams).

## Triage

Classify the request before starting work:

| Signal | Mode |
|--------|------|
| Single symbol, method, or class question | **Quick** |
| "How does X work?" / "What calls Y?" | **Quick** |
| Tracing one call chain or data flow | **Quick** |
| User says "quick" / "briefly" / "explain" | **Quick** |
| User says "investigate" / "analyze" / "report" / "audit" | **Deep** |
| System spans 3+ classes or multiple assemblies | **Deep** |
| Pre-refactor audit or onboarding documentation needed | **Deep** |
| User wants a saved document or team-facing output | **Deep** |

When ambiguous, start Quick — escalate to Deep if the answer requires 3+ files or cross-system tracing.

---

## Quick Mode

Answer the question in the fewest tool calls possible.

### Workflow

1. **Parse** — Extract the exact symbol, file, or concept from the question.
2. **Find** — `lsp_goto_definition` on the target symbol to locate its declaration.
3. **Trace** — `lsp_find_references` or `grep` to follow call chains one level deep.
4. **Stop** — Halt the moment the question can be answered; skip unused steps.
5. **Reply** — Format as summary + 1-3 typed detail blocks.

---

## Deep Mode

Produce a comprehensive investigation report. Follow this workflow:

### 1. Scope & Discovery
Define boundaries and map the system systematically:
- **Entry Points**: Public APIs, Unity callbacks (Awake/Start), event handlers.
- **Exit Points**: Data outputs, event triggers, state mutations.
- **Map Files**:
  ```text
  glob(pattern="**/{SystemName}*.cs")
  grep(pattern="ClassName|InterfaceName", include="*.cs")
  lsp_goto_definition -> follow type hierarchy
  ```

### 2. Detailed Tracing
Follow execution paths and side effects:
- **Call Chains**: `lsp_find_references` from entry points 2-3 levels deep.
- **Side Effects**:
  ```text
  grep(pattern="\\.On[A-Z]|event\s+|Action<|UnityEvent", include="*.cs")
  grep(pattern="AddListener|RemoveListener", include="*.cs")
  ```
- **Dependencies**: Note `using` directives (compile-time) and `GetComponent` (runtime).

### 3. Test & Safety Analysis
Check for coverage and data implications:
- **Coverage**: `glob(pattern="**/*Tests.cs")` to match source to test files.
- **Risk Assessment**:
  | Factor | Question |
  |--------|----------|
  | Blast Radius | How many systems are touched or break if this changes? |
  | Data Safety | Can this corrupt saves, PlayerPrefs, or global state? |
  | Test Coverage | Are critical paths tested? Score: High/Med/Low. |

### 4. Diagram & Documentation
Create Mermaid diagrams and write the report:
- **Diagrams**: Create an Execution Flow (`flowchart TD`) and Structure (`classDiagram`).
- **Template**: Mandatory `read_skill_file("unity-standards", "references/plan/investigation-template.md")`.
- **Output**: Save to `Documents/Investigations/{SystemName}_{YYYY-MM-DD}.md`.

### Quality Checklist
- [ ] Executive Summary covers purpose and key findings.
- [ ] Every claim has a `file:line` citation.
- [ ] At least one Mermaid diagram renders correctly.
- [ ] Risk table includes severity, evidence, and mitigation.
- [ ] Side effects and event chains are documented.

---

## Standards

Load `unity-standards` for convention context:
- `code-standards/lifecycle-async-errors.md` — Order of execution rules.
- `code-standards/architecture-systems.md` — Architecture patterns.
- `plan/investigation-template.md` — The mandatory report template.
- `other/unity-mcp-routing-matrix.md` — MCP tool routing for scene/asset inspection.
