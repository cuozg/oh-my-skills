# CSS Design System for App Prototyping

Interactive app prototype CSS reference. Mobile-first, Material 3 / iOS inspired patterns.

## Table of Contents
1. [Theme Setup](#theme-setup)
2. [Typography](#typography)
3. [Screen Transitions](#screen-transitions)
4. [Component Patterns](#component-patterns)
5. [Micro-interactions](#micro-interactions)
6. [Responsive Breakpoints](#responsive-breakpoints)
7. [Background Patterns](#background-patterns)
8. [Safe Area](#safe-area)
9. [Scrolling](#scrolling)
10. [Dark Mode](#dark-mode)
11. [Visual Styles](#visual-styles)
12. [Extended Palettes](#extended-palettes)
13. [Extended Font Pairings](#extended-font-pairings)
14. [Scroll Animations](#scroll-animations)

---

## Theme Setup
Six curated palettes with light and dark mode variants.

```css
:root {
  /* Default: Slate Palette */
  --bg: #f8fafc; --surface: #ffffff; --surface-elevated: #ffffff; --border: #e2e8f0;
  --text: #0f172a; --text-dim: #64748b; --primary: #3b82f6; --primary-dim: #dbeafe;
  --accent: #0891b2; --accent-dim: #ecfeff; --danger: #ef4444; --success: #22c55e;
}

[data-theme="ocean"] {
  --bg: #f0f9ff; --surface: #ffffff; --surface-elevated: #ffffff; --border: #bae6fd;
  --text: #0c4a6e; --text-dim: #0ea5e9; --primary: #0284c7; --primary-dim: #e0f2fe;
  --accent: #06b6d4; --accent-dim: #ecfeff; --danger: #f43f5e; --success: #10b981;
}

[data-theme="forest"] {
  --bg: #f0fdf4; --surface: #ffffff; --surface-elevated: #ffffff; --border: #bbf7d0;
  --text: #064e3b; --text-dim: #10b981; --primary: #059669; --primary-dim: #dcfce7;
  --accent: #84cc16; --accent-dim: #f7fee7; --danger: #e11d48; --success: #22c55e;
}

[data-theme="sunset"] {
  --bg: #fff7ed; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fed7aa;
  --text: #7c2d12; --text-dim: #f97316; --primary: #ea580c; --primary-dim: #ffedd5;
  --accent: #facc15; --accent-dim: #fefce8; --danger: #dc2626; --success: #16a34a;
}

[data-theme="berry"] {
  --bg: #fdf2f8; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fbcfe8;
  --text: #701a75; --text-dim: #db2777; --primary: #be185d; --primary-dim: #fce7f3;
  --accent: #d946ef; --accent-dim: #fdf4ff; --danger: #e11d48; --success: #059669;
}

[data-theme="rose"] {
  --bg: #fff1f2; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fecdd3;
  --text: #881337; --text-dim: #fb7185; --primary: #e11d48; --primary-dim: #ffe4e6;
  --accent: #f43f5e; --accent-dim: #fff1f2; --danger: #be123c; --success: #10b981;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f172a; --surface: #1e293b; --surface-elevated: #334155; --border: #334155;
    --text: #f8fafc; --text-dim: #94a3b8; --primary: #3b82f6; --primary-dim: #1e3a8a;
    --accent: #22d3ee; --accent-dim: #164e63; --danger: #f87171; --success: #4ade80;
  }
}
```

## Typography
Font pairings via Google Fonts CDN.

```html
<!-- CDN Links -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=DM+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;500;600;700&family=Space+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Code&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&family=Space+Mono&display=swap" rel="stylesheet">
```

```css
/* Font Pairing CSS Declarations */
.font-inter { font-family: 'Inter', system-ui, -apple-system, sans-serif; --font-mono: 'JetBrains Mono', monospace; }
.font-merriweather { font-family: 'Merriweather', serif; --font-body: 'Source Sans 3', sans-serif; }
.font-jakarta { font-family: 'Plus Jakarta Sans', sans-serif; --font-mono: 'DM Mono', monospace; }
.font-bricolage { font-family: 'Bricolage Grotesque', sans-serif; --font-mono: 'Space Mono', monospace; }
.font-dm { font-family: 'DM Sans', sans-serif; --font-mono: 'Fira Code', monospace; }
.font-nunito { font-family: 'Nunito', sans-serif; --font-mono: 'Space Mono', monospace; }
```

## Screen Transitions
Full-screen app navigation transitions.

```css
.screen {
  position: fixed; inset: 0;
  opacity: 0; pointer-events: none;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease;
  background: var(--bg);
  z-index: 10;
}
.screen.active { opacity: 1; pointer-events: auto; transform: none !important; z-index: 20; }

/* Transitions */
.slide-left { transform: translateX(100%); }
.slide-right { transform: translateX(-100%); }
.slide-up { transform: translateY(100%); }
.slide-down { transform: translateY(-100%); }
.fade { transform: scale(1); opacity: 0; }
.scale-up { transform: scale(0.9); opacity: 0; }
.none { transition: none; }
```

## Component Patterns
Core UI elements for app prototypes.

```css
/* Navigation Bar */
.nav-bar {
  position: sticky; top: 0; height: 56px; display: flex; align-items: center;
  padding: 0 16px; background: var(--surface); border-bottom: 1px solid var(--border);
  z-index: 100; gap: 12px;
}
.nav-title { font-weight: 600; font-size: 18px; color: var(--text); flex: 1; }

/* Bottom Tab Bar */
.tab-bar {
  position: fixed; bottom: 0; left: 0; right: 0; height: 64px;
  background: var(--surface); border-top: 1px solid var(--border);
  display: flex; justify-content: space-around; align-items: center;
  padding-bottom: env(safe-area-inset-bottom);
}
.tab-item { display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-dim); }
.tab-item.active { color: var(--primary); }

/* Cards */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 16px; margin: 8px 16px;
}
.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 16px; }

/* Buttons */
.btn {
  height: 48px; border-radius: 24px; display: inline-flex; align-items: center;
  justify-content: center; padding: 0 24px; font-weight: 600; border: none;
  cursor: pointer; transition: transform 0.1s, filter 0.2s;
}
.btn-primary { background: var(--primary); color: white; }
.btn-secondary { background: var(--primary-dim); color: var(--primary); }
.btn-fab {
  position: fixed; bottom: 80px; right: 16px; width: 56px; height: 56px;
  border-radius: 28px; background: var(--primary); color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Forms */
.input {
  width: 100%; height: 48px; border-radius: 12px; border: 1px solid var(--border);
  padding: 0 16px; background: var(--surface); color: var(--text); font-size: 16px;
}
.toggle {
  width: 52px; height: 32px; border-radius: 16px; background: var(--border);
  position: relative; transition: background 0.2s;
}
.toggle.active { background: var(--primary); }
.toggle::after {
  content: ''; position: absolute; left: 2px; top: 2px; width: 28px; height: 28px;
  background: white; border-radius: 14px; transition: transform 0.2s;
}
.toggle.active::after { transform: translateX(20px); }

/* Overlays */
.overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 200;
  display: flex; align-items: flex-end; opacity: 0; pointer-events: none; transition: opacity 0.3s;
}
.overlay.active { opacity: 1; pointer-events: auto; }
.bottom-sheet {
  background: var(--surface); border-radius: 24px 24px 0 0; width: 100%;
  padding: 24px; transform: translateY(100%); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.overlay.active .bottom-sheet { transform: translateY(0); }

/* Avatar & Badges */
.avatar { width: 40px; height: 40px; border-radius: 20px; background: var(--primary-dim); display: flex; align-items: center; justify-content: center; font-weight: 600; color: var(--primary); }
.badge { padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 600; background: var(--primary); color: white; }
```

## Micro-interactions
Interactive feedback for app elements.

```css
.btn:active { transform: scale(0.97); }
.card:hover { transform: translateY(-2px); border-color: var(--primary); }
.list-item { opacity: 0; transform: translateY(10px); animation: staggerIn 0.4s forwards; animation-delay: calc(var(--i) * 0.05s); }
@keyframes staggerIn { to { opacity: 1; transform: none; } }
.btn-fab::after { content: ''; position: absolute; inset: 0; border-radius: inherit; box-shadow: 0 0 0 0 var(--primary); animation: pulse 2s infinite; }
@keyframes pulse { 70% { box-shadow: 0 0 0 10px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
```

## Responsive Breakpoints
Mobile-first layout switching.

```css
.sidebar { display: none; }
@media (min-width: 768px) {
  .app-layout { display: flex; }
  .sidebar { display: flex; flex-direction: column; width: 240px; border-right: 1px solid var(--border); height: 100vh; }
  .tab-bar { display: none; }
  .screen { left: 240px; }
}
```

## Background Patterns
Visual depth for screen containers.

```css
.bg-dots { background-image: radial-gradient(var(--border) 1px, transparent 0); background-size: 20px 20px; }
.bg-mesh { background: radial-gradient(at 0% 0%, var(--primary-dim) 0, transparent 50%), radial-gradient(at 100% 100%, var(--accent-dim) 0, transparent 50%); }
```

## Safe Area
Handling modern device cutouts.

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```
```css
body { padding-top: env(safe-area-inset-top); padding-bottom: env(safe-area-inset-bottom); }
```

## Scrolling
App-like scrolling behavior.

```css
.scroll-y { overflow-y: auto; -webkit-overflow-scrolling: touch; scroll-behavior: smooth; }
.carousel { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 12px; padding-bottom: 8px; }
.carousel-item { scroll-snap-align: center; flex: 0 0 80%; }
.hide-scrollbar::-webkit-scrollbar { display: none; }
```

## Dark Mode
Dark mode refinements.

```css
@media (prefers-color-scheme: dark) {
  .card { background: var(--surface); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
  .btn-secondary { background: #334155; color: #f8fafc; }
  .input::placeholder { color: #475569; }
}
```

## Visual Styles
Popular visual style implementations. Pick one per prototype.

### Glassmorphism
Best for: modern SaaS, finance dashboards, data visualization overlays.

```css
.glass { background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; }
.glass-card { background: rgba(255,255,255,0.1); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 20px; }
@media (prefers-color-scheme: dark) {
  .glass { background: rgba(0,0,0,0.25); border-color: rgba(255,255,255,0.1); }
  .glass-card { background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.08); }
}
```

### Neumorphism / Soft UI
Best for: wellness apps, meditation, premium settings screens.

```css
.neu { background: var(--bg); border-radius: 16px; box-shadow: 6px 6px 12px rgba(0,0,0,0.08), -6px -6px 12px rgba(255,255,255,0.8); }
.neu-inset { box-shadow: inset 4px 4px 8px rgba(0,0,0,0.06), inset -4px -4px 8px rgba(255,255,255,0.7); }
.neu-btn { background: var(--bg); border: none; border-radius: 12px; padding: 12px 24px; box-shadow: 4px 4px 8px rgba(0,0,0,0.08), -4px -4px 8px rgba(255,255,255,0.8); cursor: pointer; }
.neu-btn:active { box-shadow: inset 2px 2px 5px rgba(0,0,0,0.06), inset -2px -2px 5px rgba(255,255,255,0.7); }
```

### Brutalism
Best for: design portfolios, creative agencies, bold editorial.

```css
.brutal { border: 3px solid var(--text); box-shadow: 4px 4px 0 var(--text); border-radius: 0; }
.brutal-btn { background: var(--primary); color: #fff; border: 3px solid var(--text); box-shadow: 4px 4px 0 var(--text); font-weight: 800; text-transform: uppercase; padding: 12px 24px; cursor: pointer; }
.brutal-btn:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 var(--text); }
.brutal-card { background: var(--surface); border: 3px solid var(--text); box-shadow: 6px 6px 0 var(--text); padding: 20px; }
```

### Bento Grid
Best for: dashboards, feature showcases, Apple-style product pages.

```css
.bento { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 12px; }
.bento-item { background: var(--surface); border-radius: 20px; padding: 20px; min-height: 120px; }
.bento-item.span-2 { grid-column: span 2; }
.bento-item.span-2-row { grid-row: span 2; }
.bento-item.span-full { grid-column: 1 / -1; }
@media (max-width: 768px) { .bento { grid-template-columns: repeat(2, 1fr); } }
```

### Aurora / Gradient Mesh
Best for: hero backgrounds, creative SaaS, premium feature sections.

```css
.aurora-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; overflow: hidden; }
.aurora-bg::before { content: ''; position: absolute; inset: -50%; background: radial-gradient(circle at 30% 40%, rgba(120,200,255,0.3), transparent 60%), radial-gradient(circle at 70% 60%, rgba(200,120,255,0.2), transparent 50%); animation: auroraMove 8s ease-in-out infinite alternate; }
@keyframes auroraMove { to { transform: translate(5%, 3%) scale(1.05); } }
```

### Editorial / Magazine
Best for: blog platforms, news apps, reading apps, recipe apps.

```css
.editorial { max-width: 680px; margin: 0 auto; }
.editorial h1 { font-size: clamp(32px, 5vw, 56px); line-height: 1.1; letter-spacing: -0.02em; }
.editorial .dropcap::first-letter { font-size: 3.5em; float: left; line-height: 0.8; padding-right: 8px; font-weight: 700; color: var(--primary); }
.editorial blockquote { border-left: 4px solid var(--primary); padding-left: 20px; font-style: italic; color: var(--text-dim); margin: 32px 0; }
.editorial .pull-quote { font-size: 1.4em; font-weight: 600; text-align: center; padding: 24px 40px; color: var(--primary); border-top: 2px solid var(--border); border-bottom: 2px solid var(--border); margin: 32px 0; }
```

## Extended Palettes
14 additional industry-specific palettes. Complement the 6 base palettes (Slate, Ocean, Forest, Sunset, Berry, Rose).

```css
[data-theme="midnight"] {
  --bg: #0f0d1a; --surface: #1a1726; --surface-elevated: #252036; --border: #2d2640;
  --text: #e8e4f0; --text-dim: #9b8fc2; --primary: #6366f1; --primary-dim: #2e2464;
  --accent: #a78bfa; --accent-dim: #2e1f5e; --danger: #f87171; --success: #4ade80;
}
[data-theme="copper"] {
  --bg: #fffbeb; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fde68a;
  --text: #78350f; --text-dim: #a16207; --primary: #92400e; --primary-dim: #fef3c7;
  --accent: #f59e0b; --accent-dim: #fefce8; --danger: #dc2626; --success: #16a34a;
}
[data-theme="sage"] {
  --bg: #f0fdf4; --surface: #ffffff; --surface-elevated: #ffffff; --border: #bbf7d0;
  --text: #14532d; --text-dim: #16a34a; --primary: #166534; --primary-dim: #dcfce7;
  --accent: #86efac; --accent-dim: #f0fdf4; --danger: #e11d48; --success: #22c55e;
}
[data-theme="indigo"] {
  --bg: #eef2ff; --surface: #ffffff; --surface-elevated: #ffffff; --border: #c7d2fe;
  --text: #1e1b4b; --text-dim: #6366f1; --primary: #312e81; --primary-dim: #e0e7ff;
  --accent: #818cf8; --accent-dim: #eef2ff; --danger: #ef4444; --success: #10b981;
}
[data-theme="coral"] {
  --bg: #fff7ed; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fed7aa;
  --text: #7c2d12; --text-dim: #ea580c; --primary: #9f1239; --primary-dim: #ffe4e6;
  --accent: #fb923c; --accent-dim: #fff7ed; --danger: #dc2626; --success: #16a34a;
}
[data-theme="charcoal"] {
  --bg: #171717; --surface: #262626; --surface-elevated: #404040; --border: #404040;
  --text: #f5f5f5; --text-dim: #a3a3a3; --primary: #a3a3a3; --primary-dim: #2a2a2a;
  --accent: #22d3ee; --accent-dim: #164e63; --danger: #f87171; --success: #4ade80;
}
[data-theme="terracotta"] {
  --bg: #fef3c7; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fde68a;
  --text: #78350f; --text-dim: #a16207; --primary: #78350f; --primary-dim: #fef9c3;
  --accent: #fbbf24; --accent-dim: #fefce8; --danger: #dc2626; --success: #16a34a;
}
[data-theme="mint"] {
  --bg: #f0fdfa; --surface: #ffffff; --surface-elevated: #ffffff; --border: #99f6e4;
  --text: #134e4a; --text-dim: #0d9488; --primary: #0d9488; --primary-dim: #ccfbf1;
  --accent: #5eead4; --accent-dim: #f0fdfa; --danger: #e11d48; --success: #22c55e;
}
[data-theme="wine"] {
  --bg: #fdf2f8; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fbcfe8;
  --text: #4c0519; --text-dim: #be185d; --primary: #4c0519; --primary-dim: #fce7f3;
  --accent: #be185d; --accent-dim: #fdf2f8; --danger: #e11d48; --success: #059669;
}
[data-theme="steel"] {
  --bg: #f3f4f6; --surface: #ffffff; --surface-elevated: #ffffff; --border: #d1d5db;
  --text: #111827; --text-dim: #6b7280; --primary: #374151; --primary-dim: #e5e7eb;
  --accent: #3b82f6; --accent-dim: #eff6ff; --danger: #ef4444; --success: #22c55e;
}
[data-theme="amber"] {
  --bg: #fffbeb; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fde68a;
  --text: #78350f; --text-dim: #b45309; --primary: #78350f; --primary-dim: #fef3c7;
  --accent: #d97706; --accent-dim: #fffbeb; --danger: #dc2626; --success: #16a34a;
}
[data-theme="lavender"] {
  --bg: #faf5ff; --surface: #ffffff; --surface-elevated: #ffffff; --border: #e9d5ff;
  --text: #3b0764; --text-dim: #7c3aed; --primary: #6b21a8; --primary-dim: #f3e8ff;
  --accent: #c084fc; --accent-dim: #faf5ff; --danger: #e11d48; --success: #059669;
}
[data-theme="teal"] {
  --bg: #f0fdfa; --surface: #ffffff; --surface-elevated: #ffffff; --border: #99f6e4;
  --text: #134e4a; --text-dim: #14b8a6; --primary: #134e4a; --primary-dim: #ccfbf1;
  --accent: #2dd4bf; --accent-dim: #f0fdfa; --danger: #ef4444; --success: #22c55e;
}
[data-theme="gold"] {
  --bg: #fefce8; --surface: #ffffff; --surface-elevated: #ffffff; --border: #fef08a;
  --text: #713f12; --text-dim: #a16207; --primary: #713f12; --primary-dim: #fef9c3;
  --accent: #eab308; --accent-dim: #fefce8; --danger: #dc2626; --success: #16a34a;
}

/* Dark mode variants for extended palettes */
@media (prefers-color-scheme: dark) {
  [data-theme="copper"] { --bg: #1c1007; --surface: #2a1a0b; --border: #44300f; --text: #fef3c7; --text-dim: #d97706; --primary-dim: #451a03; --accent-dim: #422006; }
  [data-theme="sage"] { --bg: #052e16; --surface: #0a3d1f; --border: #14532d; --text: #dcfce7; --text-dim: #4ade80; --primary-dim: #052e16; --accent-dim: #064e3b; }
  [data-theme="indigo"] { --bg: #1e1b4b; --surface: #2a2668; --border: #312e81; --text: #e0e7ff; --text-dim: #a5b4fc; --primary-dim: #1e1b4b; --accent-dim: #2e2464; }
  [data-theme="coral"] { --bg: #1c0a00; --surface: #2a1508; --border: #44260f; --text: #fff7ed; --text-dim: #fb923c; --primary-dim: #4c0519; --accent-dim: #431407; }
  [data-theme="terracotta"] { --bg: #1c1007; --surface: #2a1a0b; --border: #44300f; --text: #fef3c7; --text-dim: #fbbf24; --primary-dim: #451a03; --accent-dim: #422006; }
  [data-theme="mint"] { --bg: #042f2e; --surface: #083d3a; --border: #134e4a; --text: #ccfbf1; --text-dim: #5eead4; --primary-dim: #042f2e; --accent-dim: #064e3b; }
  [data-theme="wine"] { --bg: #1a0010; --surface: #2a0820; --border: #4c0519; --text: #fce7f3; --text-dim: #f472b6; --primary-dim: #4c0519; --accent-dim: #500724; }
  [data-theme="steel"] { --bg: #111827; --surface: #1f2937; --border: #374151; --text: #f3f4f6; --text-dim: #9ca3af; --primary-dim: #1f2937; --accent-dim: #1e3a5f; }
  [data-theme="amber"] { --bg: #1c1007; --surface: #2a1a0b; --border: #44300f; --text: #fffbeb; --text-dim: #f59e0b; --primary-dim: #451a03; --accent-dim: #422006; }
  [data-theme="lavender"] { --bg: #1a0030; --surface: #2a0848; --border: #3b0764; --text: #f3e8ff; --text-dim: #c084fc; --primary-dim: #3b0764; --accent-dim: #4c1d95; }
  [data-theme="teal"] { --bg: #042f2e; --surface: #083d3a; --border: #134e4a; --text: #f0fdfa; --text-dim: #2dd4bf; --primary-dim: #042f2e; --accent-dim: #064e3b; }
  [data-theme="gold"] { --bg: #1c1505; --surface: #2a200a; --border: #44360f; --text: #fefce8; --text-dim: #facc15; --primary-dim: #422006; --accent-dim: #3f3005; }
}
```

## Extended Font Pairings
8 additional pairings for specialized aesthetics.

```html
<!-- CDN Links -->
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&family=Fira+Code&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Code+Pro&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
/* Outfit + IBM Plex Mono -- SaaS, developer tools */
.font-outfit { font-family: 'Outfit', sans-serif; --font-mono: 'IBM Plex Mono', monospace; }
/* Sora + Inter -- modern startup, landing pages */
.font-sora { font-family: 'Sora', sans-serif; --font-body: 'Inter', sans-serif; }
/* Playfair Display + Lato -- editorial luxury, premium brands */
.font-playfair { font-family: 'Playfair Display', serif; --font-body: 'Lato', sans-serif; }
/* Rubik + Fira Code -- playful developer, creative coding */
.font-rubik { font-family: 'Rubik', sans-serif; --font-mono: 'Fira Code', monospace; }
/* Manrope + JetBrains Mono -- clean productivity, admin panels */
.font-manrope { font-family: 'Manrope', sans-serif; --font-mono: 'JetBrains Mono', monospace; }
/* Cormorant Garamond + Montserrat -- elegant wellness, luxury lifestyle */
.font-cormorant { font-family: 'Cormorant Garamond', serif; --font-body: 'Montserrat', sans-serif; }
/* Archivo + Source Code Pro -- bold tech, engineering dashboards */
.font-archivo { font-family: 'Archivo', sans-serif; --font-mono: 'Source Code Pro', monospace; }
/* Crimson Pro + Work Sans -- literary, education platforms */
.font-crimson { font-family: 'Crimson Pro', serif; --font-body: 'Work Sans', sans-serif; }
```

## Scroll Animations
Lightweight scroll-driven animations for prototypes.

### Fade-in on Scroll (IntersectionObserver)

```html
<script>
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
</script>
```

```css
.reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal.visible { opacity: 1; transform: none; }
.reveal-left { opacity: 0; transform: translateX(-24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal-left.visible { opacity: 1; transform: none; }
.reveal-scale { opacity: 0; transform: scale(0.92); transition: opacity 0.5s ease, transform 0.5s ease; }
.reveal-scale.visible { opacity: 1; transform: none; }
```

### Counter Animation (Stats)

```html
<script>
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const dur = 1500;
  const start = performance.now();
  (function tick(now) {
    const p = Math.min((now - start) / dur, 1);
    el.textContent = Math.floor(p * target).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  })(start);
}
const cio = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { animateCounter(e.target); cio.unobserve(e.target); } });
}, { threshold: 0.5 });
document.querySelectorAll('[data-target]').forEach(el => cio.observe(el));
</script>
```

### Parallax (Subtle)

```css
.parallax-container { overflow-y: auto; perspective: 1px; height: 100vh; }
.parallax-slow { transform: translateZ(-1px) scale(2); position: absolute; inset: 0; z-index: -1; }
.parallax-normal { transform: translateZ(0); position: relative; z-index: 1; background: var(--bg); }
```
