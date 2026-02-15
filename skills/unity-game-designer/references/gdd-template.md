# Game Design Document Template

Production-ready GDD structure. Mark sections "N/A" with justification if not applicable.

## 1. Executive Summary

```markdown
**Title**: [Game Name]
**Genre**: [Primary] / [Secondary]
**Platform**: [Mobile / PC / Console / Cross-platform]
**Target Audience**: [Age range, player archetype]
**Monetization Model**: [F2P / Premium / Hybrid]
**Session Length**: [Target duration]
**Elevator Pitch**: [2-3 sentences: what player does, why fun, what's unique]

**Competitive References**:
| Game | What We Borrow | What We Improve |
|:---|:---|:---|
| [Ref 1] | [Mechanic] | [Differentiation] |
```

## 2. Core Loop & Gameplay

```markdown
### 2.1 Core Loop Diagram
[Action] → [Reward] → [Investment] → [Return to Action]

### 2.2 Session Flow
1. **Entry**: [what they see first]
2. **Engagement**: [primary activity]
3. **Resolution**: [win/lose/timer/energy]
4. **Return Hook**: [notifications, timers, daily rewards]

### 2.3 Core Fantasy
[One sentence fantasy fulfillment]

### 2.4 Primary Controls
| Input | Action | Platform Notes |
|:---|:---|:---|
| [Tap/Click] | [Action] | [Notes] |
```

## 3. Game Mechanics

```markdown
### 3.1 [Mechanic Name]
**Purpose**: [Problem it solves]
**Rules**: 1. [Rule] 2. [Rule]
**Player Choices**: [Meaningful decisions]
**Failure State**: [What happens on fail]
**Mastery Curve**: [How skill expression grows]
**Unity Notes**: Scene, Key Components, Data sources
```

## 4. Progression System

```markdown
### 4.1 Model
**Type**: [Linear / Branching / Open-ended]
**Primary Axis**: [character, account, gear, skill tree]

### 4.2 Milestone Schedule
| Milestone | Unlock Trigger | Content Unlocked | Est. Time |
|:---|:---|:---|:---|
| Tutorial Complete | Finish level 3 | Shop, Daily Rewards | 10 min |
| Mid-game | Reach level 30 | Hard mode, Crafting | 1 week |

### 4.3 Power Curve
- **Early (0-2h)**: Rapid growth, frequent rewards
- **Mid (2-20h)**: Steady growth, resource choices
- **Late (20h+)**: Diminishing returns, prestige mechanics

### 4.4 Retention Anchors
| Day | Hook | System |
|:---|:---|:---|
| D1 | Tutorial + first reward | FTUE |
| D7 | First weekly event | Events |
| D30 | Seasonal content | Meta-progression |
```

## 5. Economy & Monetization

```markdown
### 5.1 Currency Table
| Currency | Type | Earn Rate (Free) | Purchase | Primary Sink |
|:---|:---|:---|:---|:---|
| Gold | Soft | 100/battle | N/A | Upgrades |
| Gems | Premium | 5/day | $0.99=80 | Speed-ups |

### 5.2 Sink/Source Balance
Sources: [list with rates]
Sinks: [list with costs]
Goal: Player feels "almost enough"

### 5.3 Revenue Streams
| Stream | Price | Value Proposition |
|:---|:---|:---|
| Starter Pack | $1.99 | 5x value, one-time |
| Battle Pass | $4.99/season | Exclusive cosmetics |

### 5.4 Ethical Guardrails
- [ ] No pay-to-win in competitive modes
- [ ] Spending caps for high spenders
- [ ] All gameplay content earnable free
- [ ] Clear odds for randomized purchases
```

## 6. UX Flow

```markdown
### 6.1 Screen Map
Main Menu → [Gameplay] → [Results] → [Main Menu]
         → [Shop] / [Inventory] / [Social] / [Settings]

### 6.2 FTUE
| Step | Screen | Action | Response | Duration |
|:---|:---|:---|:---|:---|
| 1 | Tutorial 1 | Tap to attack | Guided highlight | 30s |

Goals: Core loop < 3 min, fun moment < 30s, minimize text

### 6.3 Navigation: Max 2 taps to any primary feature
### 6.4 Accessibility: Color-blind, text size, screen reader, remappable controls
```

## 7. Content & Level Design

```markdown
**Format**: [Levels / Open World / Procedural]
**Launch Count**: [Number]  **Post-Launch Cadence**: [Frequency]

### Difficulty Curve
| Segment | Levels | New Mechanic |
|:---|:---|:---|
| Tutorial | 1-5 | Core combat |
| Mid | 21-50 | Team composition |

### Live Events
| Type | Frequency | Duration | Rewards |
|:---|:---|:---|:---|
| Daily Challenge | Daily | 24h | Soft currency |
| Seasonal Event | Monthly | 14d | Limited item |
```

## 8. Social & Multiplayer

```markdown
| Feature | Type | Unlock | Benefit |
|:---|:---|:---|:---|
| Friends | Passive | Level 5 | Gifts |
| Guild | Cooperative | Level 10 | Raids |
| PvP | Competitive | Level 15 | Leaderboards |

**Mode**: [Real-time / Async / Turn-based]
**Server**: [Full / Partial authority]
**Matchmaking**: [ELO / Trophies / Level]
```

## 9. Technical Constraints

```markdown
### Target Platforms
| Platform | Min Spec | Target FPS | Max Memory |
|:---|:---|:---|:---|
| iOS | iPhone 8+ | 60 | 1.5 GB |
| Android | SD 660+ | 30 | 1.2 GB |

### Unity Config
- Version: [e.g., Unity 6], Pipeline: [URP/HDRP], UI: [UI Toolkit/uGUI]

### Performance Budgets
| System | Budget |
|:---|:---|
| Draw calls | <200/frame |
| Triangles | <500K/frame |
| Scene load | <3 seconds |
```

## 10. Implementation Roadmap

```markdown
| Phase | Duration | Content | Status |
|:---|:---|:---|:---|
| Pre-production | 4 weeks | Prototype core loop | [Status] |
| Alpha | 8 weeks | Core + 20 levels | [Status] |
| Beta | 6 weeks | Full content + economy | [Status] |
| Soft Launch | 4 weeks | Limited release | [Status] |

### MVP: Core loop, Tutorial, Progression (10h+), Economy v1, Settings
```

## Appendices

```markdown
## A: Art Direction
Style, Color Palette, Character Design, Environment, UI Style, Reference Board link

## B: Audio Design
Music Style, Key SFX, Voice Acting, Adaptive Music, Audio Budget

## C: Localization
Launch Languages, String Count, RTL Support, Cultural Considerations, Pipeline Tool

## D: Analytics Events
| Event | Trigger | Parameters | Purpose |
|:---|:---|:---|:---|
| session_start | App open | device, os | DAU |
| level_complete | Win | level_id, time | Funnel |
| purchase | IAP complete | product_id, price | Revenue |
| currency_earn | Any source | type, amount, source | Economy |
```
