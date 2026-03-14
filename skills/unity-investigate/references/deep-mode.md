# Deep Investigation Mode

Full-system investigation producing a structured report with Mermaid diagrams, cited evidence, and risk tables.

## Workflow

### 1. Scope

Define system boundaries before exploring code:
- **Entry points** — public API, Unity callbacks, event handlers that start the flow
- **Exit points** — what the system outputs or triggers downstream
- **Key actors** — classes, services, ScriptableObjects involved
- **Boundary** — what is IN scope vs adjacent systems

### 2. Discover

Map all files and classes systematically:

```
glob(pattern="**/{SystemName}*.cs")
grep(pattern="ClassName|InterfaceName", include="*.cs")
lsp_goto_definition → follow type hierarchy
lsp_find_references → find all consumers
```

Build a file list: `FileName.cs` — role (entry/core/data/output).

### 3. Analyze

Trace execution paths through the system:
- Follow the primary flow: entry → processing → output
- Record dependencies (what this system depends ON)
- Record consumers (what depends on THIS system)
- Note state mutations, caching, and side effects
- Cross-reference with `unity-standards` `plan/investigation-workflow.md` for structured tracing

### 4. Diagram

Create at least one Mermaid diagram (two recommended):

**Execution flow** — `flowchart TD` showing the primary path through the system
**Structure** — `classDiagram` showing class relationships and interfaces

Use `read_skill_file("unity-standards", "references/other/mermaid-syntax.md")` for syntax reference.

### 5. Assess

Identify risks using these lenses:

| Lens | What to Look For |
|------|------------------|
| Coupling | Tight dependencies, missing interfaces, direct class references |
| Blast radius | How many systems break if this system changes |
| Hidden deps | Runtime GetComponent, FindObjectOfType, string-based lookups |
| Test coverage | Untested critical paths |
| Data safety | Can changes corrupt saves/prefs/state |

Score each risk: High / Medium / Low with `file:line` evidence.

### 6. Load Template

**MANDATORY** — Load the template before writing:
```
read_skill_file("unity-standards", "references/plan/investigation-template.md")
```

### 7. Write Report

Fill every section of the template. Rules:
- Cite `file:line` for every factual claim
- Include at least one Mermaid diagram
- Bullets over prose in all sections
- No speculation — investigate first, then conclude
- Never skip or rename template sections

### 8. Save

Save to `Documents/Investigations/{SystemName}_{YYYY-MM-DD}.md`

Add a one-paragraph executive summary at the top covering: what is this system, what does it do, key findings.

## Quality Checklist

- [ ] All template sections filled (Executive Summary, System Map, Execution Flow, Data Flow, Risks, References)
- [ ] At least one Mermaid diagram rendered correctly
- [ ] Every claim has `file:line` citation
- [ ] Risk table has severity + evidence + mitigation
- [ ] No empty sections or TODO placeholders
