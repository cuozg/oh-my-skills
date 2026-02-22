# UX Screen Specification Examples — Game HUD

## Example C: Game HUD (Landscape 16:9)

### Overview
| Field | Value |
|---|---|
| Screen ID | SCR-HUD-001 |
| Purpose | Real-time battle HUD: health, abilities, timer, score, controls |
| Device | Mobile (Landscape), 16:9/19.5:9 |
| Priority | P0 - Critical |

**Performance paramount:** No layout recalculations or GC allocations during battle. All client-driven, no server calls.
**Safe Area:** Left/right 44pt inset on notched devices.

**Nav:** Battle loading / countdown → HUD → Victory/Defeat / Pause quit / Disconnect

### Wireframe
```
+------------------------------------------------------------------+
| [Portrait] [====HP====] [==Enemy HP==] [Timer]    [Score] [Pause]|
|            [====MP====] [Boss Name   ]            [Auto] [Speed] |
|            [buff icons]                                          |
|                         (3D Battle Scene)              x12       |
|                                                         [Ult]   |
| [MiniMap]                                         [A1-A4 cluster]|
+------------------------------------------------------------------+
```

### UI Elements

| ID | Type | Required | Key Notes |
|---|---|---|---|
| `HUD_HPBar` | Slider | Yes | Gradient green→yellow→red by %, numeric value |
| `HUD_MPBar` | Slider | Yes | Blue fill, depletes on ability use |
| `HUD_Portrait` | Image | Yes | 64x64pt circular |
| `HUD_EnemyHP` | Slider | Yes | Red fill, boss name above, multi-phase support |
| `HUD_Timer` | TMP | Yes | Red <30s, pulse <10s |
| `HUD_Score` | TMP | No | Pop+settle on change |
| `HUD_PauseBtn` | Button | Yes | 44x44pt |
| `HUD_Ability1-4` | Button | Yes | 72x72pt, cooldown radial fill, MP cost check |
| `HUD_UltimateBtn` | Button | Yes | 88x88pt, charge % ring, golden glow at 100% |
| `HUD_MiniMap` | RawImage | No | 120x120pt, rotates with camera |
| `HUD_ComboCounter` | TMP | No | Fades after 2s idle, milestones at x5/x10/x25 |
| `HUD_BuffIcons` | HLayout | No | 24x24pt icons with duration overlay |
| `HUD_AutoPlayToggle` | Toggle | No | Unlocks at level 10 |
| `HUD_SpeedToggle` | Button | No | Cycles 1x→2x→3x, requires auto-play |

### Key Interactive Details
- **HPBar:** Fill animates 0.3s EaseOut. Damage flash white 0.1s. Critical (<20%): red + pulse 0.5s loop.
- **Abilities:** Ready=full color. Cooldown=grey radial wipe+timer. Not enough MP=desaturated, red cost. Ready flash once.
- **Ultimate:** Charging=grey+%. Fully charged=golden burst+glow loop. Activation=screen-wide flash 0.2s.
- **Timer:** >30s white, <30s yellow, <10s red+scale pulse 1.0→1.1 (0.5s loop).
- **Combo:** Scale pop 1.0→1.3→1.0 (0.15s). Milestones: color flash+particle burst.

### Interactions
1. **Tap Ability** → Activate, start cooldown, deduct MP. On cooldown: shake 0.2s. No MP: flash MP bar red.
2. **Tap Ultimate** → Cinematic trigger, reset charge. Not charged: show % tooltip.
3. **Tap Pause** → Pause time, dim HUD 40%, show pause menu.
4. **Toggle Auto-Play** → Enable/disable AI play. Locked <Lv10: "Unlock at Level 10" toast.
5. **Cycle Speed** → 1x→2x→3x→1x. Requires auto-play enabled.

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
