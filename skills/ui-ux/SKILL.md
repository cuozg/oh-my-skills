---
name: ui-ux
description: "UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
---
# UI/UX Pro Max

Design intelligence for web and mobile. Searchable database of 67 styles, 96 palettes, 57 font pairings, 99 UX rules, 25 chart types across 13 stacks.

## Action Router

Detect the user's intent and jump to the matching mode:

| User Intent | Mode | What to Do |
|---|---|---|
| "Build a landing page", "Create a dashboard" | **Build** | Step 1 → 2 → 3 → 4 |
| "Review my UI", "Check this for UX issues" | **Review** | Jump to Review Mode |
| "Fix the contrast", "Improve this layout" | **Fix** | Jump to Fix Mode |
| "What colors for fintech?", "Best font for SaaS?" | **Lookup** | Run one search, return answer |

---

## Build Mode (Full Workflow)

### Step 1: Extract Requirements

From the user's request, identify:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode
- **Industry**: healthcare, fintech, gaming, education, beauty, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System

Run this command to get a complete design recommendation with reasoning:

```bash
python3 <skill-path>/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

This searches 5 domains (product, style, color, landing, typography), applies reasoning rules, and returns: pattern, style, colors, typography, effects, and anti-patterns.

To persist across sessions:
```bash
python3 <skill-path>/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

Creates `design-system/MASTER.md` (global rules) and `design-system/pages/` for per-page overrides. When building a specific page, check `pages/[page].md` first — its rules override Master.

### Step 3: Supplement with Domain Searches

After the design system, get details for specific needs:

```bash
python3 <skill-path>/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|---|---|---|
| Style options | `style` | `"glassmorphism dark"` |
| Chart recs | `chart` | `"real-time dashboard"` |
| UX rules | `ux` | `"animation accessibility"` |
| Font alternatives | `typography` | `"elegant luxury serif"` |
| Landing structure | `landing` | `"hero social-proof"` |
| Icons | `icons` | `"navigation action"` |
| React perf | `react` | `"suspense waterfall bundle"` |
| Web a11y | `web` | `"aria focus keyboard"` |

### Step 4: Stack Guidelines

Get implementation-specific rules (default: `html-tailwind`):

```bash
python3 <skill-path>/scripts/search.py "<keyword>" --stack html-tailwind
```

Stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`, `astro`, `nuxtjs`, `nuxt-ui`

### Step 5: Implement

Apply the design system to code. Key translation rules:

| Design System Output | Implementation |
|---|---|
| Color hex values | Tailwind custom colors or CSS variables |
| Font pairing + Google URL | `<link>` in head or `@import` in CSS |
| Style effects (blur, glow) | Tailwind utilities or raw CSS |
| Section order | Page structure / component order |
| Anti-patterns | Things to actively avoid in code |

---

## Review Mode

When reviewing existing UI code, search for violations:

1. **Run UX audit**: `--domain ux` with keywords from the code (animation, z-index, accessibility, touch)
2. **Run web audit**: `--domain web` for aria, focus, semantic HTML issues
3. **Run stack audit**: `--stack <detected-stack>` for framework-specific issues
4. **Check against Pre-Delivery Checklist** (below)

Report findings as: `[SEVERITY] Issue — Do: X, Don't: Y`

---

## Fix Mode

When fixing specific UI issues:

1. Search the relevant domain for the exact issue
2. Apply the "Do" pattern from search results
3. Verify the "Don't" pattern is removed
4. Re-check with Pre-Delivery Checklist

---

## Lookup Mode

For quick questions, run a single search and return the answer directly. No need for the full workflow.

---

## Domains Reference

| Domain | Contents | Records |
|---|---|---|
| `product` | Product type → style/pattern mapping | 96 |
| `style` | UI styles with CSS, effects, checklists | 67 |
| `typography` | Font pairings with Google Fonts URLs | 57 |
| `color` | Hex palettes by product type | 96 |
| `landing` | Page patterns with section orders | 30 |
| `chart` | Chart types with library recs | 25 |
| `ux` | UX guidelines with Do/Don't | 99 |
| `icons` | Icon recommendations by category | 100 |
| `react` | React/Next.js performance patterns | 44 |
| `web` | Web interface a11y guidelines | 30 |

---

## Common Rules for Professional UI

These are frequently overlooked. Violating them makes UI look amateurish:

### Icons & Visual Elements

| Rule | Do | Don't |
|---|---|---|
| No emoji icons | SVG icons (Heroicons, Lucide, Simple Icons) | Emojis as UI icons |
| Stable hover | Color/opacity transitions | Scale transforms that shift layout |
| Brand logos | Official SVG from Simple Icons | Guessing logo paths |
| Icon sizing | Fixed viewBox (24x24), w-6 h-6 | Mixed sizes |

### Interaction

| Rule | Do | Don't |
|---|---|---|
| Cursor | `cursor-pointer` on all clickable elements | Default cursor on interactive |
| Hover feedback | Visual change (color, shadow, border) | No indication of interactivity |
| Transitions | `transition-colors duration-200` | Instant or >500ms |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|---|---|---|
| Glass cards (light) | `bg-white/80` or higher | `bg-white/10` (invisible) |
| Text contrast | `#0F172A` (slate-900) | `#94A3B8` (slate-400) |
| Muted text | `#475569` (slate-600) minimum | gray-400 or lighter |
| Borders | `border-gray-200` in light | `border-white/10` (invisible) |

### Layout

| Rule | Do | Don't |
|---|---|---|
| Floating navbar | `top-4 left-4 right-4` spacing | Stuck to `top-0 left-0 right-0` |
| Content padding | Account for fixed navbar height | Content behind fixed elements |
| Container width | Consistent `max-w-6xl` or `max-w-7xl` | Mixed container widths |

---

## Pre-Delivery Checklist

Verify before delivering ANY UI code:

**Visual Quality**
- [ ] No emojis as icons (SVG only)
- [ ] Consistent icon set (Heroicons or Lucide)
- [ ] Hover states don't cause layout shift
- [ ] Brand logos verified (Simple Icons)

**Interaction**
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Focus states visible for keyboard navigation

**Contrast & Modes**
- [ ] Light mode text: 4.5:1 minimum contrast
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both light/dark modes

**Layout & Responsive**
- [ ] Floating elements have edge spacing
- [ ] No content behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

**Accessibility**
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
