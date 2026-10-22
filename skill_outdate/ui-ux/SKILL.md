---
name: ui-ux
description: "UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
---
# UI/UX Pro Max

Design intelligence for web and mobile. Searchable database of 67 styles, 96 palettes, 57 font pairings, 99 UX rules, 25 chart types across 13 stacks.

## Action Router

| User Intent | Mode |
|---|---|
| "Build a landing page", "Create a dashboard" | **Build** → Steps 1–5 |
| "Review my UI", "Check for UX issues" | **Review** → Run audits + checklist |
| "Fix the contrast", "Improve this layout" | **Fix** → Search domain → apply Do pattern → re-check |
| "What colors for fintech?", "Best font for SaaS?" | **Lookup** → Single search, return answer |

## Build Mode

**Step 1 — Extract:** product type · style keywords · industry · stack (default: `html-tailwind`)

**Step 2 — Design System:**
```bash
python3 <skill-path>/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
# Persist: add --persist  →  creates design-system/MASTER.md + design-system/pages/
```

**Step 3 — Domain Searches:** `python3 <skill-path>/scripts/search.py "<keyword>" --domain <domain>`

| Need | Domain |
|---|---|
| Style options | `style` |
| Chart recs | `chart` |
| UX rules | `ux` |
| Font alternatives | `typography` |
| Landing structure | `landing` |
| Icons | `icons` |
| React perf | `react` |
| Web a11y | `web` |

**Step 4 — Stack:** `python3 <skill-path>/scripts/search.py "<keyword>" --stack html-tailwind`  
Stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`, `astro`, `nuxtjs`, `nuxt-ui`

**Step 5 — Implement:** Apply design system. Color hex → CSS vars/Tailwind. Font → `<link>`. Effects → utilities/raw CSS. Section order → component order. Avoid anti-patterns listed.

## Review Mode

1. `--domain ux` audit (animation, z-index, accessibility, touch)
2. `--domain web` audit (aria, focus, semantic HTML)
3. `--stack <detected>` for framework-specific issues
4. Check Pre-Delivery Checklist

Report: `[SEVERITY] Issue — Do: X, Don't: Y`

## Pre-Delivery Checklist

**Visual:** No emoji icons (SVG only) · consistent icon set · hover states no layout shift · brand logos verified  
**Interaction:** `cursor-pointer` on all clickables · hover transitions 150–300ms · focus states visible  
**Contrast:** Light mode 4.5:1 min · glass elements visible in light mode · borders visible both modes  
**Layout:** Floating elements have edge spacing · no content behind fixed navbars · responsive at 375/768/1024/1440px · no horizontal scroll on mobile  
**A11y:** All images have alt · form inputs have labels · color not sole indicator · `prefers-reduced-motion` respected

## Common Rules

| Rule | Do | Don't |
|---|---|---|
| Icons | SVG (Heroicons/Lucide) | Emojis as UI icons |
| Hover | Color/opacity transitions | Scale transforms shifting layout |
| Cursor | `cursor-pointer` on clickables | Default cursor on interactive |
| Glass (light) | `bg-white/80`+ | `bg-white/10` (invisible) |
| Text contrast | `#0F172A` (slate-900) | `#94A3B8` (slate-400) |
| Navbar | `top-4 left-4 right-4` spacing | Stuck to `top-0 left-0 right-0` |
