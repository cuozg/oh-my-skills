# Game HUD — Data & Rules

### Data
All client-side. HP/MP/Timer/Cooldowns update per-frame via cached refs. Combo/Score on events. Buffs on add/remove. Object pool buff icons and combo text.

### Rules
- **R-HUD-001** 🔴 Zero GC allocs per frame. Pre-allocated StringBuilders, no concat/boxing/LINQ.
- **R-HUD-002** 🔴 HP/MP bars update same frame as damage event (LateUpdate sync).
- **R-HUD-003** 🔴 Clear visual distinction: cooldown vs not-enough-MP vs ready.
- **R-HUD-004** 🟡 Combo auto-hides after 2s. Milestones (x5/x10/x25/x50/x100) get special VFX.
- **R-HUD-005** 🟡 Respect landscape safe areas, no interactive element within 44pt of edges.
- **R-HUD-006** 🟢 Speed toggle only when auto-play on. Disabling auto-play resets to 1x.

### Canvas Hierarchy
```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (ref: 1920x1080, match: 0.5)
+-- SafeArea (landscape insets)
    +-- TopLeftGroup [Portrait 64x64 | HPBar 200x16 | MPBar 180x12 | BuffIcons]
    +-- TopCenterGroup [EnemyHP 300x16 | EnemyName | Timer]
    +-- TopRightGroup [Score | PauseBtn 44x44 | AutoPlay 44x44 | Speed 44x44]
    +-- CenterRight [ComboCounter]
    +-- BottomLeft [MiniMap 120x120]
    +-- BottomRight [UltimateBtn 88x88 | Ability1-4 72x72]
```

### Animations
- **Battle Start:** Slide in from edges, 0.4s staggered 0.05s, EaseOutBack
- **Damage:** HP fill 0.3s EaseOut + white flash 0.1s + red vignette 0.2s
- **Cooldown:** Radial clockwise grey overlay (linear). Ready: golden flash 0.3s.
- **Ultimate Charged:** Golden burst 0.5s + glow loop 1.5s + bob 2s
- **Battle End:** HUD fades 0.5s. Victory: fly up+confetti. Defeat: darken+sink.

## Template Usage Guide

1. Copy Sections 1-14 + 5B from template, replace `[PLACEHOLDERS]`
2. Fill: Overview (SCR-XXXX-NNN), Nav Flow, Wireframe, States, Elements, Interactions
3. Fill: Data, Rules (RULE-NNN), Accessibility, Responsive, Animations, Acceptance (AC-NNN)

### Element States Checklist

| Type | States | Key |
|---|---|---|
| Button | Default/Pressed/Disabled | ≥44pt tap target |
| Toggle | On/Off/Disabled | Track color, transition |
| Slider | Default/Dragging/Disabled | Fill, thumb, range |
| Dropdown | Closed/Open/Disabled | Max height, scroll |
| Tab | Active/Inactive | Indicator, anim |
| Progress | Empty/Filling/Full | Gradient, label |
| Timer | Running/Paused/Expired/Warning | Threshold, pulse |
| Input | Empty/Focused/Filled/Error/Disabled | Char limit, validation |

### Best Practices
- Consistent IDs: `SCR-[FEATURE]-[NNN]`, `RULE-NNN`, `AC-NNN`
- Document all states: Loading, Empty, Populated, Error, Offline minimum
- Exact values (pt, hex, ms) — no vague terms ("large", "bright")
- Tap targets ≥44x44pt (iOS) / ≥48x48dp (Android)
- Fallback values for every data-driven field
- Version specs, cross-reference Screen IDs in nav flow

### Unity UI Performance
- Separate Canvases for static/dynamic (rebuild is O(n))
- Disable `Raycast Target` on non-interactive, Layout Groups when static
- Pool spawned UI; atlas sprites by screen; use TMP with pre-gen atlases
- Minimize overdraw; prefer DOTween over Animator for simple tweens
- **Budget:** <2ms/frame UI on mid-range devices
