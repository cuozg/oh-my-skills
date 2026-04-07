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
