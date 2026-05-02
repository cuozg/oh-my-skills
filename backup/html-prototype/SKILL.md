---
name: html-prototype
description: >
  Create interactive HTML app prototypes and landing pages as a single self-contained
  HTML file with full-screen layouts, multi-screen navigation, smooth transitions,
  clickable controls, fake auth/data, and product-aware visual design. MUST use when
  the user describes an app idea and wants to see it, prototype it, mock up screens,
  build a clickable demo, landing page, marketing site, product page, interactive
  wireframe, app demo, or any multi-screen flow with navigation. Also use for app
  concepts like recipe, fitness, dashboard, SaaS, e-commerce, social, chat, finance,
  booking, wellness, or education when the user wants to visualize the flow or test
  screen transitions. Do not use for static diagrams, production code, or game
  prototypes.
metadata:
  author: cuongnp
  version: "2.0"
---

# HTML Prototype

Generate a complete, interactive app prototype as a single self-contained HTML file. The prototype should feel like a real app — smooth screen transitions, clickable navigation, realistic fake data, and polished visual design. Every screen the user needs, wired together with working navigation.

The output is always a **single HTML file** that opens in any browser. No build tools, no dependencies beyond CDN fonts. The user clicks buttons, navigates between screens, and experiences the app flow exactly as it would work in production — except the data is fake and the backend doesn't exist.

**Supports two modes:**
- **App Prototype**: Multi-screen app with navigation, transitions, and fake data (mobile or desktop)
- **Landing Page**: Single-scroll marketing site with sections, CTAs, and scroll animations

## Workflow

### 1. Analyze the Concept

Extract from the user's description:

- **App purpose**: What problem does it solve? Who uses it?
- **Product type**: What industry/category? (fintech, health, SaaS, e-commerce, social, etc.)
- **Prototype mode**: Is this a multi-screen app or a landing page? If unclear, default to app prototype.
- **Screen inventory**: Every screen the app needs — don't skip secondary screens (settings, profile, empty states, error states, onboarding). For landing pages: every section needed.
- **Navigation flow**: How screens connect — which button leads where
- **Key interactions**: Forms, toggles, search, filters, swipe gestures
- **Data model**: What entities exist (users, posts, products, books, etc.)

If the description is vague, ask ONE clarifying question about the core use case. But err toward assumptions — prototypes thrive on reasonable defaults.

### 2. Design Intelligence — Choose the Visual System

Before mapping screens, determine the visual identity based on the product type. Read `references/design-intelligence.md` and look up the user's product category to get:

- **Recommended visual style** (Minimalism, Glassmorphism, Soft UI, Brutalism, etc.)
- **Color palette** with specific hex values matched to the industry
- **Font pairing** from Google Fonts that fits the app's personality
- **Anti-patterns** specific to this product type (what to avoid)
- **Navigation pattern** (bottom tabs, sidebar, top bar)

This step prevents the common failure of defaulting to generic blue/white for every prototype. A fintech app should feel different from a wellness app — the design intelligence reference encodes those differences.

If the product type doesn't match any category exactly, pick the closest one and adapt.

### 3. Map the Screens

Before writing HTML, map every screen. Each screen needs:

| Field | Description |
|-------|-------------|
| **ID** | Machine name: `login`, `dashboard`, `book-detail` |
| **Title** | Human-readable name |
| **Components** | What's on the screen: nav bar, card list, form, fab button |
| **Entry points** | Which screens navigate TO this one |
| **Exit points** | Which screens this one navigates TO |
| **Data** | What fake data this screen displays |

Read `references/app-archetypes.md` for common app types and their typical screen maps. This saves time — most apps share patterns (auth flow → home → list → detail → settings). For landing pages, read `references/landing-patterns.md` instead.

### 4. Apply the Visual Direction

With the design intelligence recommendations in hand, make the final visual decisions. Read `references/css-system.md` for CSS implementations of each style.

**Decisions already made by design intelligence (step 2):**
- Color palette (use the hex values from the lookup)
- Font pairing (use the Google Fonts from the lookup)
- Visual style (Minimalism, Glassmorphism, etc.)

**Decisions still needed:**
1. **Layout frame** — Mobile-first (390px viewport, bottom tab bar) or desktop-first (sidebar nav, wide content area). For landing pages: always desktop-first with responsive stacking.
2. **Transition style** — Default: slide-left forward, slide-right back, fade for tabs, slide-up for modals. For landing pages: scroll-triggered fade-in.

### 5. Generate the Prototype

**Read `templates/spa-shell.html` first** — it's a complete working BookShelf app that demonstrates every pattern. Use it as your reference architecture. Don't copy it verbatim; adapt its router, transitions, and data patterns for the user's app.

**Architecture overview:**

```
┌─ <section class="screen" data-screen="screen-id"> ─── one per screen
│   Full-viewport content with its own layout
└─ JavaScript router handles hash-based navigation
   CSS transitions animate between screens
   APP_DATA object holds all fake data
   APP_STATE object holds auth and UI state
```

**Key implementation patterns** (all demonstrated in the template):

- **SVG Icons**: Define a `const SVG = { home: '...', search: '...', back: '...' }` object with inline SVG strings for all icons. Never use emoji.
- **Screen Hooks**: Use a `SCREEN_HOOKS` object mapping screen IDs to render functions. The router calls the hook when a screen becomes active, so content is populated dynamically from `APP_DATA`.
- **Transition Trick**: After adding the enter class, call `element.offsetHeight` to force a reflow before adding `.active`. Without this, CSS transitions won't animate — the browser batches the class changes.
- **Tab Bar**: Render the tab bar inside each tabbed screen (not globally), so it travels with the screen during transitions. Use a shared `renderTabBar()` function.

**The prototype MUST include:**

- Every screen from the screen map — no shortcuts
- Working navigation between every connected screen pair
- Smooth CSS transition animations (300-400ms, ease-out curves)
- Responsive layout that works at 390px (mobile) and 1200px+ (desktop)
- Light/dark mode via `prefers-color-scheme`
- Status bar or navigation chrome appropriate to the app type
- Realistic fake data — real names, real dates, real numbers (never "Lorem ipsum" or "Test User")
- Interactive form elements — inputs accept text, toggles switch visually, dropdowns open
- Loading/empty states where appropriate

### 6. Deliver

**Output location:** Save to `~/.agent/prototypes/` with a descriptive filename based on the app concept: `book-reader-app.html`, `fitness-tracker.html`, `recipe-manager.html`.

**Open in browser:**
- macOS: `open ~/.agent/prototypes/filename.html`
- Linux: `xdg-open ~/.agent/prototypes/filename.html`

Tell the user the file path so they can re-open, share, or iterate.

---

## Screen Transition System

The router supports directional transitions that feel natural — forward navigation pushes content left, back navigation pulls it right, modals slide up from the bottom.

| Transition | When to use | Feel |
|-----------|-------------|------|
| `slide-left` | Navigate deeper (list → detail, home → subpage) | Moving forward |
| `slide-right` | Navigate back (detail → list, subpage → home) | Returning |
| `slide-up` | Open modal, bottom sheet, overlay | Revealing |
| `slide-down` | Close modal, dismiss overlay | Dismissing |
| `fade` | Switch tabs, same-level navigation | Lateral movement |
| `scale-up` | Open detail from card (zoom into content) | Focusing |
| `none` | Initial load, auth redirect | Instant |

The router tracks navigation history to automatically choose forward vs. back transitions. Explicitly set transitions for modals and special cases.

**Timing:** 300ms for screen transitions, 150ms for micro-interactions (button press, toggle). Use `cubic-bezier(0.4, 0, 0.2, 1)` for natural deceleration.

---

## Fake Data & Auth

**Auth flow:** Use `APP_STATE.isLoggedIn` boolean. The login screen validates that both fields are non-empty (no real validation), sets `isLoggedIn = true`, and navigates forward. Protected screens check the flag on entry and redirect to login if `false`. A logout button resets the flag and navigates to login.

**Generating realistic fake data** is critical — the prototype should look like a screenshot of a real app. Guidelines by domain:

| Domain | Examples |
|--------|----------|
| **Books** | "The Great Gatsby" by F. Scott Fitzgerald, 4.2★, 218 pages |
| **E-commerce** | "Wireless Noise-Cancelling Headphones" — $149.99, 4.7★ (2,341 reviews) |
| **Social** | "Sarah Chen" posted 2h ago, 47 likes, 12 comments |
| **Fitness** | 8,432 steps today, 3.2 km, 247 cal burned |
| **Finance** | Checking ••••4829: $3,247.50, +$1,200.00 on Mar 15 |
| **Food/Recipe** | "Spicy Thai Basil Chicken" — 25 min, 4 servings, 380 cal |
| **Productivity** | "Q2 Marketing Plan" — 3/7 tasks done, due Apr 15, assigned to Alex |

Store data in `const APP_DATA = { ... }` at the top of the script section. Components read from this object to render lists, cards, and detail views.

---

## Visual Design Principles

The goal is an app that looks **designed**, not generated. A real designer would never ship flat gray cards with Inter font and purple accents — so neither should this skill.

### Typography

Pick a font pairing that matches the app's personality. Load via Google Fonts CDN.

**Recommended pairings:**
- **Professional/Finance**: Inter + JetBrains Mono (yes, Inter is fine for apps — it's overused in diagrams, not in app UIs)
- **Editorial/Reading**: Merriweather + Source Sans 3 (serif body for reading apps)
- **Modern/Social**: Plus Jakarta Sans + DM Mono (rounded, friendly)
- **Bold/E-commerce**: Bricolage Grotesque + Space Mono (characterful, punchy)
- **Clean/Productivity**: DM Sans + Fira Code (precise, reliable)
- **Playful/Lifestyle**: Nunito + Space Mono (soft, approachable)

### Color

Build the palette from the app's domain, not from defaults. Use CSS custom properties for everything.

**Curated app palettes:**

| Name | Primary | Accent | Surface | Use for |
|------|---------|--------|---------|---------|
| **Ocean** | `#0c4a6e` | `#0ea5e9` | `#f0f9ff` | Finance, productivity, professional |
| **Forest** | `#14532d` | `#22c55e` | `#f0fdf4` | Health, fitness, nature |
| **Sunset** | `#7c2d12` | `#f97316` | `#fff7ed` | Food, social, lifestyle |
| **Berry** | `#581c87` | `#a855f7` | `#faf5ff` | Creative, music, entertainment |
| **Slate** | `#1e293b` | `#64748b` | `#f8fafc` | Minimal, tools, developer |
| **Rose** | `#881337` | `#f43f5e` | `#fff1f2` | Shopping, fashion, dating |

Always define both light and dark variants via `prefers-color-scheme`.

### Micro-interactions

Small animations that make the prototype feel alive:

- **Button press**: `transform: scale(0.97)` on `:active`, 100ms transition
- **Card tap**: Subtle shadow lift on hover/active
- **Toggle switch**: Smooth slide with background color change
- **Screen entrance**: Staggered fade-in for list items using `--i` CSS variable
- **Pull-to-refresh indicator**: Rotating spinner (CSS only)
- **Floating action button**: Scale-in on screen enter, pulse shadow on hover

### Anti-Slop Rules

These patterns signal "AI made this" — avoid them:

- Neon dashboard aesthetic (cyan + magenta + purple on dark background)
- Gradient text on headings
- Animated glowing box-shadows
- Emoji as navigation icons (use inline SVG or CSS shapes instead)
- Uniform card grid where every card has identical styling
- "Lorem ipsum" or "Test User 1" placeholder text
- Perfectly symmetrical layouts with no visual hierarchy
- Three-dot window chrome on any element

---

## File Structure

Every prototype is a single self-contained `.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>App Name — Prototype</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, themes, screen layouts, transitions, components */
  </style>
</head>
<body>
  <div id="app">
    <section class="screen" data-screen="splash">...</section>
    <section class="screen" data-screen="login">...</section>
    <section class="screen" data-screen="home">...</section>
    <!-- More screens -->
  </div>

  <script>
    // APP_DATA — all fake data
    // APP_STATE — auth, selections, UI state
    // Router — hash-based navigation with transition support
    // Screen init functions — populate screens from APP_DATA
    // Event handlers — button clicks, form submits, toggles
  </script>
</body>
</html>
```

---

## Quality Checks

Before delivering, run through `references/ux-checklist.md` for the full checklist. At minimum, verify:

- [ ] **Every screen** from the screen map is present and reachable
- [ ] **Every navigation path** works — click button → correct screen with smooth transition
- [ ] **Back navigation** works — browser back button or in-app back arrows
- [ ] **Fake auth** works — login with any non-empty fields, protected screens redirect, logout works
- [ ] **Fake data** looks real — no placeholders, no "Lorem ipsum"
- [ ] **Forms are interactive** — text inputs accept typing, toggles switch visually, dropdowns open
- [ ] **Transitions are smooth** — no flicker, no layout jump, correct direction (forward=slide-left, back=slide-right)
- [ ] **Mobile layout** — works at 375px width with touch-friendly targets (44px minimum)
- [ ] **Desktop layout** — uses the extra space well (wider cards, sidebar nav, multi-column)
- [ ] **Both themes** — light and dark mode both look intentional, not broken
- [ ] **Self-contained** — opens cleanly with no console errors, no broken fonts
- [ ] **No emoji icons** — all icons use inline SVG, never emoji characters
- [ ] **Cursor pointer** — every clickable element has cursor:pointer
- [ ] **Hover states** — all interactive elements respond to hover with smooth transition
- [ ] **Design coherence** — palette, typography, and style match the product type (use design intelligence reference)
- [ ] **File is saved** to `~/.agent/prototypes/` and opened in browser

---

## References

Load on demand — don't read all at once:

- `references/design-intelligence.md` — Industry-to-design mapping: 30+ product types with recommended style, palette, typography, anti-patterns, and navigation patterns. **Read this first** when building any prototype to make informed design decisions.
- `references/css-system.md` — Full design system: CSS variables, theme setup, visual styles (glassmorphism, neumorphism, brutalism, bento grid, aurora), extended palettes (20+ industry-specific), transition CSS, component patterns, responsive breakpoints, scroll animations
- `references/screen-patterns.md` — HTML/CSS patterns for common app screens: auth, dashboard, list/detail, settings, onboarding, modals, empty states
- `references/app-archetypes.md` — Screen maps for common app types: what screens each type needs, navigation flows, data models. Covers 13 types including SaaS dashboards and landing pages.
- `references/landing-patterns.md` — HTML/CSS patterns for landing page sections: hero variants, feature grids, testimonials, pricing tables, FAQ accordions, CTA sections, footers, scroll animations
- `references/ux-checklist.md` — Pre-delivery UX quality checklist: accessibility, touch targets, hover states, transitions, form patterns. Run through this before delivering any prototype.

Load via `read_skill_file("html-prototype", "references/<file>")`.

The template at `templates/spa-shell.html` is a complete working example demonstrating all patterns. Read it as a reference architecture — don't copy it verbatim, but follow its router pattern and transition system.

## Escalation

| From | To | When |
|------|----|------|
| html-prototype | flutter-code + flutter-ui | User wants to build the real app in Flutter |
| html-prototype | nextjs-backend | User wants to build the actual backend |
| html-prototype | visual-explainer | User needs a static diagram, not an interactive app |
| html-prototype | frontend-design | User wants production-quality frontend code |
| html-prototype | phaser-coder | User wants a game prototype |
| html-prototype | unity-prototype | User wants a Unity game prototype |
