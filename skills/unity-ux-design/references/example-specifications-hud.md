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
