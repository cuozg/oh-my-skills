---
name: visual-explainer
description: Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
metadata:
  author: nicobailon
  version: "0.5.1"
---

# Visual Explainer

Generate self-contained HTML files for diagrams, tables, and data visualizations. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering:** If table has 4+ rows or 3+ columns → HTML page, not ASCII.

## Workflow

### 1. Think — Pick Aesthetic

Pick one and commit. Vary each time — don't repeat the last choice.

**Preferred (constrained):** Blueprint · Editorial · Paper/ink · Monochrome terminal  
**Flexible (use with discipline):** Named IDE theme (Dracula, Nord, Catppuccin, Gruvbox, Solarized)  
**Forbidden:** Neon cyan+magenta, gradient mesh blobs, Inter font + violet accents, gradient text headings, glowing animated shadows

### 2. Structure — Read Templates First

| Content | Template/Approach |
|---|---|
| Architecture (text-heavy) | `./templates/architecture.html` |
| Flowchart/sequence/ER/state/mindmap/class | `./templates/mermaid-flowchart.html` (Mermaid) |
| Data table/comparison/audit | `./templates/data-table.html` |
| Slide deck (`--slides` or `/generate-slides`) | `./templates/slide-deck.html` + `./references/slide-patterns.md` |
| Prose page/README/article | CSS prose patterns in `./references/css-patterns.md` |

**Mermaid rules:** Always use `theme: 'base'` + `themeVariables`. Add zoom controls (+/−/reset/expand) to every diagram. Never use bare `<pre class="mermaid">` — always use the full `diagram-shell` pattern from the template. Prefer `flowchart TD` over `LR`. Use `<br/>` for line breaks (not `\n`). Never define `.node` as a page-level CSS class.

**4+ sections:** Load `./references/responsive-nav.md` for sticky sidebar TOC.

### 3. Style Rules

- **Fonts:** Pick from `./references/libraries.md` pairings. Forbidden as body font: Inter, Roboto, Arial, system-ui alone.
- **Colors:** CSS custom properties. Define `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, 3-5 accents. Forbidden accents: `#8b5cf6` / `#7c3aed` / `#a78bfa`, cyan+magenta+pink combo.
- **Animation:** Stagger fade-ins on load. Respect `prefers-reduced-motion`. Forbidden: glow pulse loops.
- **Hierarchy:** Vary card depth (hero → elevated → default → recessed). Not everything elevated.

### 4. Deliver

- Write to `~/.agent/diagrams/<descriptive-name>.html`
- Open: `open ~/.agent/diagrams/<file>.html` (macOS) or `xdg-open` (Linux)
- Tell user the file path

## Diagram Type Quick-Ref

| Type | Use |
|---|---|
| Architecture ≤10 nodes | Mermaid `graph TD` |
| Architecture text-heavy | CSS Grid cards |
| Architecture 15+ nodes | Hybrid: Mermaid overview + CSS detail cards |
| Flowchart/pipeline | Mermaid |
| Sequence/ER/state/mindmap/class | Mermaid |
| C4 | Mermaid `graph TD` + subgraph (NOT native C4Context) |
| Data table | HTML `<table>` |
| Timeline | CSS central line + cards |
| Dashboard | CSS Grid + Chart.js |

## Anti-Patterns (Slop Test)

Fail if 2+ of these are present: Inter/Roboto + purple gradient · gradient-clip text on headings · emoji section icons · glow-animated cards · cyan-magenta scheme · uniform card grid · three-dot code chrome.

## Reference Files

- `./references/css-patterns.md` — layout, SVG connectors, overflow protection, prose elements
- `./references/libraries.md` — font pairings, CDN links, Mermaid theming, Chart.js, anime.js
- `./references/responsive-nav.md` — sticky sidebar TOC for 4+ section pages
- `./references/slide-patterns.md` — slide engine, types, transitions, presets
- `./commands/` — prompt templates for diff-review, plan-review, project-recap, fact-check, share
