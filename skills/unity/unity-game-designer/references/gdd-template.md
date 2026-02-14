# Game Design Document Template

Production-ready GDD structure. Populate every section. Mark sections as "N/A" with justification if truly not applicable — never leave sections blank.

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Core Loop & Gameplay](#2-core-loop--gameplay)
3. [Game Mechanics](#3-game-mechanics)
4. [Progression System](#4-progression-system)
5. [Economy & Monetization](#5-economy--monetization)
6. [User Experience (UX) Flow](#6-user-experience-ux-flow)
7. [Content & Level Design](#7-content--level-design)
8. [Social & Multiplayer](#8-social--multiplayer)
9. [Technical Constraints & Platform Notes](#9-technical-constraints--platform-notes)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Appendix A: Art Direction](#appendix-a-art-direction)
12. [Appendix B: Audio Design](#appendix-b-audio-design)
13. [Appendix C: Localization](#appendix-c-localization)
14. [Appendix D: Analytics Events](#appendix-d-analytics-events)

---

## 1. Executive Summary

One paragraph, no jargon. Readable by stakeholders who will not read the rest.

### Template

```markdown
## 1. Executive Summary

**Title**: [Game Name]
**Genre**: [Primary Genre] / [Secondary Genre]
**Platform**: [Mobile / PC / Console / Cross-platform]
**Target Audience**: [Age range, player archetype]
**Monetization Model**: [F2P / Premium / Hybrid]
**Session Length**: [Target session duration]
**Elevator Pitch**: [2-3 sentences: what the player does, why it's fun, what makes it unique]

**Competitive References**:
| Game | What We Borrow | What We Improve |
|:---|:---|:---|
| [Reference 1] | [Mechanic/feel] | [Our differentiation] |
| [Reference 2] | [Mechanic/feel] | [Our differentiation] |
```

### Guidance

- The pitch must answer: What does the player DO? Why is it FUN? What is UNIQUE?
- Avoid feature lists. Focus on the feeling and fantasy.
- Competitive references should show awareness, not copying.

---

## 2. Core Loop & Gameplay

The repeating cycle of actions that defines moment-to-moment play.

### Template

```markdown
## 2. Core Loop & Gameplay

### 2.1 Core Loop Diagram

[Action] → [Reward] → [Investment] → [Return to Action]

Example (Idle RPG):
Fight Monsters → Earn Gold/XP → Upgrade Heroes → Fight Harder Monsters

### 2.2 Session Flow

1. **Entry**: Player opens game → [what they see first]
2. **Engagement**: [Primary activity for the session]
3. **Resolution**: [How the session ends — win/lose/timer/energy]
4. **Return Hook**: [Why the player comes back — notifications, timers, daily rewards]

### 2.3 Core Fantasy

[One sentence: what fantasy does the player fulfill?]
Example: "Become the commander of an unstoppable army"

### 2.4 Primary Controls

| Input | Action | Platform Notes |
|:---|:---|:---|
| [Tap/Click] | [Action] | [Mobile: thumb-reachable] |
| [Swipe/Drag] | [Action] | [Consider touch area size] |
```

### Guidance

- The core loop should be describable in under 30 words.
- Every action must have a clear feedback signal (visual, audio, haptic).
- Session flow must account for interrupted sessions on mobile.

---

## 3. Game Mechanics

Individual systems that compose the gameplay experience.

### Template

```markdown
## 3. Game Mechanics

### 3.1 [Mechanic Name]

**Purpose**: [What problem this mechanic solves for the player]
**Rules**:
1. [Rule 1]
2. [Rule 2]
3. [Rule 3]

**Player Choices**: [Meaningful decisions the player makes]
**Failure State**: [What happens when the player fails]
**Mastery Curve**: [How skill expression increases over time]

**Unity Implementation Notes**:
- Scene: [Which scene this mechanic lives in]
- Key Components: [MonoBehaviours, ScriptableObjects]
- Data: [What data drives this mechanic — config files, blueprints]

### 3.2 [Next Mechanic]
[Repeat structure]
```

### Guidance

- Each mechanic must serve the core loop or progression.
- Document edge cases and interaction between mechanics.
- Keep mechanics modular — one should not require another to function at MVP.

---

## 4. Progression System

How the player advances through content and grows in power/skill.

### Template

```markdown
## 4. Progression System

### 4.1 Progression Model

**Type**: [Linear / Branching / Open-ended / Hybrid]
**Primary Axis**: [What the player levels — character, account, gear, skill tree]
**Pacing**: [How fast progression feels — hours per milestone]

### 4.2 Milestone Schedule

| Milestone | Unlock Trigger | Content Unlocked | Estimated Time |
|:---|:---|:---|:---|
| Tutorial Complete | Finish level 3 | Shop, Daily Rewards | 10 min |
| Chapter 1 Clear | Beat boss 1 | PvP Arena, Guild | 2 hours |
| Mid-game | Reach level 30 | Hard mode, Crafting | 1 week |
| End-game | Reach level cap | Leaderboards, Raids | 1 month |

### 4.3 Power Curve

Describe the relationship between time invested and player power.

**Early game (0-2 hours)**: Rapid growth, frequent rewards
**Mid game (2-20 hours)**: Steady growth, introduce resource choices
**Late game (20+ hours)**: Diminishing returns, prestige/reset mechanics

### 4.4 Retention Anchors

| Day | Hook | System |
|:---|:---|:---|
| D1 | Complete tutorial, first reward | FTUE flow |
| D3 | Unlock social features | Guild/friends |
| D7 | Complete first weekly event | Events system |
| D30 | Prestige or seasonal content | Meta-progression |
```

### Guidance

- Progression pacing is the #1 lever for retention. Be explicit about timing.
- Include "what if the player is stuck?" escape valves.
- Document both free and paid progression tracks if F2P.

---

## 5. Economy & Monetization

All virtual currencies, resources, sinks, and sources.

### Template

```markdown
## 5. Economy & Monetization

### 5.1 Currency Table

| Currency | Type | Earn Rate (Free) | Purchase Option | Primary Sink |
|:---|:---|:---|:---|:---|
| Gold | Soft | 100/battle | N/A | Upgrades |
| Gems | Premium | 5/day (ads) | $0.99 = 80 | Speed-ups, cosmetics |
| Energy | Gating | 1/5 min, cap 30 | 10 gems = 5 energy | Play sessions |

### 5.2 Sink/Source Balance

**Sources** (how currency enters the economy):
- [Source 1]: [Rate]
- [Source 2]: [Rate]

**Sinks** (how currency leaves the economy):
- [Sink 1]: [Cost]
- [Sink 2]: [Cost]

**Balance Goal**: Player should feel "almost enough" — never flooded, never starved.

### 5.3 Monetization Model

**Model**: [F2P with IAP / Premium / Battle Pass / Subscription / Hybrid]

**Revenue Streams**:
| Stream | Price Range | Value Proposition |
|:---|:---|:---|
| Starter Pack | $1.99 | 5x value, one-time | 
| Battle Pass | $4.99/season | Exclusive cosmetics + resources |
| Gem Packs | $0.99 - $99.99 | Convenience currency |
| Ad Rewards | Free (ad view) | 2x rewards, energy refill |

### 5.4 Ethical Guardrails

- [ ] No pay-to-win advantage in competitive modes
- [ ] Spending caps or cooling-off prompts for high spenders
- [ ] All gameplay-relevant content earnable without paying
- [ ] Clear odds disclosure for any randomized purchases
```

### Guidance

- Economy must be modeled in a spreadsheet before implementation.
- Document the "whale vs. minnow" experience gap.
- Every premium currency purchase must feel like a good deal.

---

## 6. User Experience (UX) Flow

Screen-by-screen navigation and first-time user experience.

### Template

```markdown
## 6. User Experience (UX) Flow

### 6.1 Screen Map

Main Menu → [Gameplay] → [Results] → [Main Menu]
         → [Shop]
         → [Inventory]
         → [Social]
         → [Settings]

### 6.2 First-Time User Experience (FTUE)

| Step | Screen | Player Action | System Response | Duration |
|:---|:---|:---|:---|:---|
| 1 | Splash | Watch intro | Cinematic/skip | 15s |
| 2 | Name Entry | Enter name | Validate, save | 10s |
| 3 | Tutorial 1 | Tap to attack | Guided highlight | 30s |
| 4 | Tutorial 2 | Open inventory | Forced equip | 20s |
| 5 | Free play | Complete level 1 | Full rewards | 2 min |
| 6 | Tutorial 3 | Visit shop | Highlight free item | 15s |

**FTUE Goals**:
- Teach core loop in under 3 minutes
- First "fun moment" within 30 seconds
- Minimize text — show, don't tell

### 6.3 Navigation Principles

- Maximum 2 taps to reach any primary feature
- Back button always available
- Loading screens show tips or progress
- Popup frequency: max 1 on session start

### 6.4 Accessibility

- [ ] Color-blind mode
- [ ] Adjustable text size
- [ ] Screen reader support
- [ ] Remappable controls (PC/Console)
```

### Guidance

- FTUE is the highest-impact design area. Iterate aggressively.
- Every screen must have a clear call-to-action.
- Test navigation flow with a paper prototype before implementation.

---

## 7. Content & Level Design

Levels, chapters, events, and content cadence.

### Template

```markdown
## 7. Content & Level Design

### 7.1 Content Structure

**Format**: [Levels / Chapters / Open World / Procedural]
**Total at Launch**: [Number of levels/areas]
**Post-Launch Cadence**: [New content frequency]

### 7.2 Difficulty Curve

| Segment | Levels | Difficulty | New Mechanic Introduced |
|:---|:---|:---|:---|
| Tutorial | 1-5 | Very Easy | Core combat |
| Early | 6-20 | Easy | Elemental types |
| Mid | 21-50 | Medium | Team composition |
| Late | 51-100 | Hard | Min-maxing, synergies |

### 7.3 Live Events

| Event Type | Frequency | Duration | Rewards |
|:---|:---|:---|:---|
| Daily Challenge | Daily | 24h | Soft currency |
| Weekly Tournament | Weekly | 7 days | Exclusive cosmetic |
| Seasonal Event | Monthly | 14 days | Limited character/item |
```

### Guidance

- Content must outpace player consumption for the first 6 months.
- Procedural generation can extend content but must feel curated.
- Live events keep end-game players engaged.

---

## 8. Social & Multiplayer

Player interaction systems — cooperative, competitive, or both.

### Template

```markdown
## 8. Social & Multiplayer

### 8.1 Social Features

| Feature | Type | Unlock Condition | Benefit |
|:---|:---|:---|:---|
| Friends List | Passive | Level 5 | Send/receive gifts |
| Guild | Cooperative | Level 10 | Guild raids, perks |
| PvP Arena | Competitive | Level 15 | Leaderboards, rewards |
| Chat | Communication | Level 5 | Global, guild, whisper |

### 8.2 Multiplayer Architecture

**Mode**: [Real-time / Async / Turn-based / Hybrid]
**Server Authority**: [Full / Partial / Client-authoritative]
**Matchmaking**: [ELO / Trophies / Level-based]

### 8.3 Anti-Cheat & Moderation

- [Server-validated actions]
- [Chat filtering]
- [Reporting system]
```

---

## 9. Technical Constraints & Platform Notes

Unity-specific and platform-specific requirements.

### Template

```markdown
## 9. Technical Constraints & Platform Notes

### 9.1 Target Platforms

| Platform | Min Spec | Target FPS | Max Memory |
|:---|:---|:---|:---|
| iOS | iPhone 8+ | 60 fps | 1.5 GB |
| Android | Snapdragon 660+ | 30 fps | 1.2 GB |
| PC | GTX 1060 | 60 fps | 4 GB |

### 9.2 Unity Configuration

- **Unity Version**: [e.g., Unity 6]
- **Render Pipeline**: [URP / HDRP / Built-in]
- **UI Framework**: [UI Toolkit / uGUI]
- **Networking**: [Netcode for GameObjects / Mirror / Custom]
- **Build Size Target**: [<200 MB initial, <1 GB total with assets]

### 9.3 Performance Budgets

| System | Budget |
|:---|:---|
| Draw calls | <200 per frame |
| Triangles | <500K per frame |
| Textures | Max 2K for mobile |
| Audio | Compressed, streaming for music |
| Scene load | <3 seconds |

### 9.4 Platform-Specific Notes

**Mobile**:
- Battery drain considerations
- Thermal throttling handling
- Background/foreground lifecycle
- Push notification strategy

**PC**:
- Keyboard + mouse bindings
- Resolution scaling
- Windowed/fullscreen modes

**Console**:
- Platform certification requirements
- Controller haptics
- Achievement/trophy integration
```

---

## 10. Implementation Roadmap

Phased delivery plan with priorities.

### Template

```markdown
## 10. Implementation Roadmap

### 10.1 Phase Overview

| Phase | Duration | Content | Status |
|:---|:---|:---|:---|
| Pre-production | 4 weeks | Prototype core loop | [Status] |
| Alpha | 8 weeks | Core gameplay + 20 levels | [Status] |
| Beta | 6 weeks | Full content + economy | [Status] |
| Soft Launch | 4 weeks | Limited market release | [Status] |
| Global Launch | 2 weeks | Full release | [Status] |

### 10.2 MVP Feature Set

**Must Have** (launch blockers):
- [ ] Core gameplay loop
- [ ] Tutorial/FTUE
- [ ] Basic progression (10+ hours)
- [ ] Economy v1
- [ ] Settings menu

**Should Have** (soft launch):
- [ ] Social features
- [ ] Live events framework
- [ ] Analytics integration
- [ ] Monetization v1

**Nice to Have** (post-launch):
- [ ] Advanced social (guilds, chat)
- [ ] Seasonal content
- [ ] Cross-platform sync
```

### Guidance

- MVP scope should be achievable in 12 weeks by the team.
- Soft launch metrics must be defined before Alpha starts.
- Each phase should have clear go/no-go criteria.

---

## Appendix A: Art Direction

```markdown
## Appendix A: Art Direction

**Art Style**: [Stylized / Realistic / Pixel / Low-poly / 2D]
**Color Palette**: [Primary, secondary, accent colors]
**Character Design**: [Proportions, style reference images]
**Environment**: [Themes, biome types, lighting mood]
**UI Style**: [Clean/minimal / Ornate/themed / Diegetic]

**Reference Board**: [Link to mood board or reference images]
```

---

## Appendix B: Audio Design

```markdown
## Appendix B: Audio Design

**Music Style**: [Genre, mood, tempo]
**Sound Effects**: [Key SFX list: UI clicks, combat hits, rewards]
**Voice Acting**: [Yes/No, languages, character count]
**Adaptive Music**: [Does music change with gameplay state?]

**Audio Budget**:
- Total audio assets: [Target size]
- Compression: [Format, quality level]
- Streaming: [Which tracks stream vs. preload]
```

---

## Appendix C: Localization

```markdown
## Appendix C: Localization

**Launch Languages**: [List]
**Post-Launch Languages**: [List]
**String Count Estimate**: [Number]
**Right-to-Left Support**: [Yes/No]
**Cultural Considerations**: [Content that may need regional variants]
**Localization Pipeline**: [Tool, format — e.g., CSV export, Localazy, Crowdin]
```

---

## Appendix D: Analytics Events

```markdown
## Appendix D: Analytics Events

### Core Events

| Event Name | Trigger | Parameters | Purpose |
|:---|:---|:---|:---|
| session_start | App open | device, os, version | DAU tracking |
| level_complete | Win condition | level_id, time, score | Progression funnel |
| level_fail | Lose condition | level_id, attempt, reason | Difficulty tuning |
| purchase | IAP complete | product_id, price, currency | Revenue |
| ad_watched | Ad completes | ad_type, placement | Ad revenue |
| tutorial_step | FTUE progress | step_id, duration | Onboarding funnel |

### Economy Events

| Event Name | Trigger | Parameters |
|:---|:---|:---|
| currency_earn | Any source | currency_type, amount, source |
| currency_spend | Any sink | currency_type, amount, sink |
| item_acquire | Get item | item_id, source |
| item_consume | Use item | item_id, context |
```

### Guidance

- Every event must have a documented "so what" — what decision does this data inform?
- Keep event names snake_case and consistent.
- Log sparingly on mobile to respect battery and bandwidth.
