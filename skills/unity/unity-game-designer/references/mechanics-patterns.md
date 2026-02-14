# Game Mechanics Design Patterns

Reusable design patterns for game systems. Each pattern includes description, when to use it, and 2-3 concrete examples.

## Table of Contents

1. [Progression Patterns](#1-progression-patterns)
2. [Economy Patterns](#2-economy-patterns)
3. [Social & Multiplayer Patterns](#3-social--multiplayer-patterns)
4. [Monetization Patterns](#4-monetization-patterns)
5. [Engagement & Retention Patterns](#5-engagement--retention-patterns)
6. [Core Loop Archetypes](#6-core-loop-archetypes)

---

## 1. Progression Patterns

### 1.1 Linear Progression

**Description**: Player advances through sequentially ordered content. Each stage gates the next.

**When to Use**: Narrative-driven games, puzzle games with difficulty ramp, tutorial-heavy experiences.

**Advantages**: Easy to pace, clear direction, simple to balance.
**Risks**: Player gets stuck → churn. No replay value after completion.

**Examples**:
- **Candy Crush**: Numbered levels on a map. Must complete level N to unlock N+1. Star ratings add optional depth.
- **Monument Valley**: Handcrafted levels in fixed order. Each level introduces one new mechanic. No grind.
- **Call of Duty Campaign**: Linear missions with scripted set-pieces. Difficulty settings as the flex lever.

**Unity Notes**: Store progress as `int currentLevel` in PlayerPrefs or save file. Use ScriptableObject for level definitions.

---

### 1.2 Branching Progression

**Description**: Player chooses between multiple paths or skill trees. Decisions create distinct playstyles.

**When to Use**: RPGs, strategy games, games wanting high replay value or personalization.

**Advantages**: Player agency, replayability, builds identity/ownership.
**Risks**: Balance complexity grows exponentially. "Trap" builds frustrate players.

**Examples**:
- **Path of Exile**: Massive passive skill tree with hundreds of nodes. Players specialize deeply. Respec is costly but possible.
- **Civilization VI**: Tech tree and civic tree run in parallel. Each choice opens different units and buildings. Multiple victory conditions.
- **Hades**: Mirror of Night upgrades offer binary choices per slot. Simple branching with meaningful trade-offs.

**Unity Notes**: Model as graph (ScriptableObject nodes with `List<SkillNode> children`). Use bitmask or `HashSet<string>` for unlocked nodes.

---

### 1.3 Open-Ended / Sandbox Progression

**Description**: Player defines their own goals. Systems provide tools, not direction.

**When to Use**: Creative games, simulation, survival, player-driven economies.

**Advantages**: Massive engagement for invested players. Emergent content.
**Risks**: New players feel lost. Hard to measure "progression" for analytics.

**Examples**:
- **Minecraft**: No enforced progression. Players mine, build, explore at their own pace. Optional boss (Ender Dragon) as a loose goal.
- **Stardew Valley**: Open farm management. Seasons provide rhythm. Community Center provides optional structured goals.
- **Factorio**: Build increasingly complex factories. No fail state. Player-defined efficiency goals.

**Unity Notes**: Save systems must handle arbitrary world state. Consider chunk-based serialization for large worlds.

---

### 1.4 Prestige / Reset Progression

**Description**: Player resets progress to earn permanent bonuses, then progresses faster. The meta-loop.

**When to Use**: Idle games, incremental games, any game needing long-term retention beyond content ceiling.

**Advantages**: Infinite progression depth. "Fresh start" feeling. Solves power ceiling.
**Risks**: First prestige must feel worth it. Too many resets feel like treadmill.

**Examples**:
- **Adventure Capitalist**: Reset entire business empire for "angel investors" that multiply all future earnings. Each cycle is faster.
- **Rogue Legacy**: Die → start new character who inherits gold and upgrades. Castle layout rerolls each run.
- **Cookie Clicker**: Ascend for Heavenly Chips. Each prestige layer adds new systems.

**Unity Notes**: Store prestige data separately from run data. Use `[Serializable]` class hierarchy: `PrestigeData` (permanent) vs `RunData` (reset).

---

## 2. Economy Patterns

### 2.1 Dual Currency (Soft + Premium)

**Description**: Two currency types — soft (earned freely) and premium (earned slowly or purchased). Premium enables convenience, cosmetics, or acceleration.

**When to Use**: Any F2P game. Industry standard for mobile.

**Advantages**: Monetization without blocking free players. Clear value proposition for spenders.
**Risks**: Premium currency inflation. Players feel forced to buy. Exchange rate confusion.

**Examples**:
- **Clash of Clans**: Gold/Elixir (soft, earned from collectors and raids) + Gems (premium, slow drip + IAP). Gems speed up timers.
- **Fortnite**: V-Bucks (premium only, earned via Battle Pass or purchased). No soft currency — all cosmetic purchases.
- **Genshin Impact**: Mora (soft, abundant) + Primogems (premium, limited free sources). Primogems convert to gacha pulls.

**Balance Rule**: Free player should earn 5-10% of a premium currency pack per week. Enough to taste, not enough to satisfy.

---

### 2.2 Energy / Stamina Gating

**Description**: Resource that limits play sessions. Regenerates over time or can be purchased.

**When to Use**: Mobile games needing session pacing. Games where daily engagement > session length.

**Advantages**: Prevents content exhaustion. Creates return triggers. Monetizable.
**Risks**: Frustrates eager players. Can feel punitive. Wrong refill rate kills engagement.

**Examples**:
- **Candy Crush**: 5 lives, lose one per fail, regenerate 1 per 30 minutes. Optionally buy more or ask friends.
- **Fire Emblem Heroes**: Stamina bar for campaign maps. Higher-difficulty maps cost more stamina. Stamina potions as rewards.
- **Marvel Snap**: Cosmic energy for ranked matches. Prevents grinding leaderboard in a single session.

**Balance Rule**: Default energy should allow 3-5 meaningful sessions per day. Refill ads should feel like a good deal, not a necessity.

---

### 2.3 Crafting / Resource Conversion

**Description**: Multiple raw resources combine to create higher-value items. Creates meaningful resource management decisions.

**When to Use**: RPGs, survival games, base builders, any game wanting depth in resource management.

**Advantages**: Content multiplication (N resources → N² recipes). Player decision-making. Natural sink for excess resources.
**Risks**: Recipe complexity overwhelms casual players. Inventory management fatigue.

**Examples**:
- **Minecraft**: Wood → Planks → Sticks + Planks → Tools. Hierarchical crafting with discoverable recipes.
- **Monster Hunter**: Monster parts + ores → specific armor sets. Targeted farming with clear goals.
- **Stardew Valley**: Crops + tools → artisan goods. Time investment adds value (wine aging).

**Unity Notes**: Represent recipes as ScriptableObjects: `CraftingRecipe { List<ResourceAmount> inputs; ItemData output; float craftTime; }`.

---

## 3. Social & Multiplayer Patterns

### 3.1 Asynchronous Competition

**Description**: Players compete against each other's data/replays, not in real-time. No latency issues.

**When to Use**: Mobile games where real-time PvP is impractical. Casual competitive features. Leaderboard-driven games.

**Advantages**: No server tick rate concerns. Players can play on their schedule. Simpler networking.
**Risks**: Feels less exciting than real-time. Cheating harder to detect. Can feel like playing against bots.

**Examples**:
- **Clash Royale (War)**: Attack opponent's base layout while they're offline. Defend with pre-set configuration.
- **Mario Kart Tour**: Race against "ghost" data of other players. Feels competitive without real-time sync.
- **Wordle**: Same daily puzzle for everyone. Social comparison without direct interaction.

---

### 3.2 Cooperative Guilds / Clans

**Description**: Players form persistent groups that share goals, resources, and progress.

**When to Use**: Mid-core and hardcore games wanting long-term social retention. Games needing D30+ hooks.

**Advantages**: Social obligation drives retention. Group goals motivate individual play. Community self-moderates.
**Risks**: Guild drama causes churn. Dead guilds depress new members. Leader burnout.

**Examples**:
- **Clash of Clans**: Clans share troops, participate in Clan Wars. Leader hierarchy with permissions. Clan perks.
- **Guild Wars 2**: Guilds own a hall that members upgrade collectively. Guild missions require coordination.
- **Monster Strike**: Co-op quests where friends' characters assist your party. Low-friction social play.

---

### 3.3 Social Gifting / Sharing

**Description**: Players send and receive items, lives, or currency to/from friends. Low-friction social mechanic.

**When to Use**: Casual games wanting viral spread. Games needing daily return reasons.

**Advantages**: Free re-engagement channel. Strengthens social bonds. Feels generous, not competitive.
**Risks**: Gift spam annoys non-players. Becomes obligatory chore. Abuse via alt accounts.

**Examples**:
- **Candy Crush**: Send lives to friends. Request lives when out. Creates reciprocity obligation.
- **Pokemon GO**: Trade Pokemon with nearby friends. Special trades for rare Pokemon. Lucky trades.
- **Animal Crossing**: Visit friends' islands. Drop items as gifts. Collaborative decoration.

---

## 4. Monetization Patterns

### 4.1 Battle Pass / Season Pass

**Description**: Time-limited progression track with free and premium tiers. Premium tier purchased for season duration.

**When to Use**: Games with regular content updates. Any game wanting predictable recurring revenue. Live-service games.

**Advantages**: Predictable revenue. Keeps players engaged across season. FOMO drives purchase. Fair — effort still required.
**Risks**: Too many passes fatigues players. Must deliver enough value. Late-season joiners feel cheated.

**Examples**:
- **Fortnite**: 100 tiers per season. Free tier gets some rewards. Premium unlocks exclusive skins, V-Bucks (pays for next pass). XP from challenges.
- **Clash Royale**: Gold Pass with queue skip, exclusive tower skin, and extra rewards on existing progression. Low price point ($4.99).
- **Halo Infinite**: Season pass that never expires. Players can work on it at their pace. No FOMO pressure.

**Design Rules**:
- Free tier must feel generous enough to showcase premium value
- Premium should be earnable through play (not just purchase)
- Season duration: 4-8 weeks (shorter = more revenue, longer = less pressure)

---

### 4.2 Gacha / Loot Box

**Description**: Randomized reward system where players spend currency for a chance at rare items.

**When to Use**: Collection-driven games. Games with character/weapon variety. Markets where legally permitted.

**Advantages**: High revenue per user. Collection drive. Excitement of random reward.
**Risks**: Legal restrictions in many markets. PR backlash. Can feel predatory. Requires pity/guarantee systems.

**Examples**:
- **Genshin Impact**: "Wish" system with 0.6% base 5-star rate. Hard pity at 90 pulls. Soft pity increases rate after 75 pulls. Featured character guaranteed on second pity.
- **Fire Emblem Heroes**: Orb-based summoning with color selection. Rates increase with each non-5-star pull within a session.
- **FIFA Ultimate Team**: Card packs with player ratings. Market for trading. Pack weight disclosure required by law.

**Design Rules**:
- Always implement pity/guarantee system
- Disclose rates prominently
- No gameplay-critical items exclusive to gacha
- Provide alternative earn paths for everything

---

### 4.3 Cosmetic-Only Monetization

**Description**: All purchases are visual/aesthetic only. No gameplay advantage for money.

**When to Use**: Competitive games where fairness matters. Games with strong community. Premium-priced games adding live-service revenue.

**Advantages**: Fair perception. No pay-to-win complaints. High goodwill. Whales spend on status.
**Risks**: Lower revenue ceiling. Requires constant art pipeline. Not all audiences value cosmetics.

**Examples**:
- **League of Legends**: Champion skins from $5-$30. Chromas, ward skins, emotes. Champions earnable with free currency.
- **CS:GO/CS2**: Weapon skins with rarity tiers. Player-driven marketplace. Status through rare drops.
- **Fortnite**: Skins, emotes, gliders, pickaxes. All cosmetic. Shop rotates daily to create urgency.

---

### 4.4 Ad-Supported (Rewarded Ads)

**Description**: Players watch optional video ads in exchange for in-game rewards.

**When to Use**: F2P games targeting broad casual audiences. Games where IAP conversion is low. Secondary revenue stream alongside IAP.

**Advantages**: Monetizes non-payers. Player-initiated = less intrusive. Scales with DAU.
**Risks**: Ad fatigue reduces effectiveness. Revenue per view is low. Some players hate all ads.

**Examples**:
- **Subway Surfers**: Watch ad to continue run after death. Watch ad for 2x rewards. Optional, never forced.
- **Crossy Road**: Ad plays between runs. Rewarded ad for free character unlock chance. Interstitial at natural breaks.
- **Idle Miner Tycoon**: 2x production boost for watching ad. Multiple ad placements, all optional, all rewarded.

**Design Rules**:
- Always rewarded, never forced
- Maximum 5-8 ad views per day before diminishing returns
- Ad placement at natural break points (between rounds, after death)
- Reward must feel worth the 30-second interruption

---

## 5. Engagement & Retention Patterns

### 5.1 Daily Login / Streak Rewards

**Description**: Escalating rewards for consecutive daily logins. Missing a day may reset or continue from last checkpoint.

**When to Use**: Any game wanting D1-D7 retention improvement. Simple to implement, universally effective.

**Examples**:
- **Forgiving streak**: Rewards escalate D1-D7, then cycle. Missing a day doesn't reset — pick up where you left off.
- **Punishing streak**: Miss a day = reset to D1. Higher stakes but risk of "already lost streak, why bother?"
- **Calendar-based**: Monthly calendar with fixed rewards. Collect what you can, no penalty for misses.

---

### 5.2 Limited-Time Events

**Description**: Temporary content or challenges that create urgency and give veteran players fresh goals.

**When to Use**: Live-service games. Any game past 3 months post-launch. Games needing re-engagement spikes.

**Examples**:
- **Seasonal events**: Halloween, New Year themed content with exclusive rewards. 2-4 week duration.
- **Competitive events**: Time-limited leaderboard with unique rewards for top performers. 3-7 day duration.
- **Collaborative events**: Community-wide goal (e.g., "defeat 1M bosses globally"). Collective reward.

---

### 5.3 Daily Quests / Missions

**Description**: Rotating objectives that direct player activity and reward completion.

**When to Use**: Any game wanting structured daily engagement. Particularly effective when combined with Battle Pass XP.

**Examples**:
- **3-quest daily**: Complete 3 varied quests for a bonus chest. Quests rotate daily. Refreshable for currency.
- **Tiered daily**: Complete 5 → 10 → 15 activity points for escalating rewards. Any activity contributes.
- **Weekly + daily**: Daily quests for small rewards, weekly quests for larger rewards. Two engagement cycles.

---

## 6. Core Loop Archetypes

Common core loop structures by genre. Use as starting points, not rigid formulas.

### 6.1 Battle Loop (RPG / Strategy)

```
Prepare (equip, plan) → Fight (execute strategy) → Reward (loot, XP) → Upgrade (power up) → [repeat]
```

**Key Tension**: Preparation quality determines fight outcome.

### 6.2 Build Loop (City Builder / Tycoon)

```
Earn resources → Build/Expand → Earn more resources → Optimize → [repeat]
```

**Key Tension**: What to build next (opportunity cost).

### 6.3 Explore Loop (Adventure / Open World)

```
Discover (new area) → Challenge (puzzle, enemy) → Reward (item, story) → Unlock (new area) → [repeat]
```

**Key Tension**: Curiosity about what's next.

### 6.4 Match Loop (Puzzle / Casual)

```
Start round → Play (solve/match) → Score → Feedback (stars, rank) → Next round → [repeat]
```

**Key Tension**: Improving personal score / clearing all content.

### 6.5 Create Loop (Sandbox / Creative)

```
Imagine → Build → Share → Get feedback → Iterate → [repeat]
```

**Key Tension**: Self-expression and community recognition.

### 6.6 Idle Loop (Incremental)

```
Set up automation → Leave (offline progress) → Return → Collect → Upgrade automation → [repeat]
```

**Key Tension**: Optimizing offline earnings. Prestige timing decisions.

---

## Pattern Selection Guide

When choosing patterns, match them to the game's constraints:

| Constraint | Recommended Patterns |
|:---|:---|
| Mobile, casual audience | Linear progression, Energy gating, Rewarded ads, Daily rewards |
| Mobile, mid-core | Branching progression, Dual currency, Battle pass, Guilds |
| PC, hardcore | Open-ended progression, Crafting, Real-time PvP, Cosmetic monetization |
| Short dev timeline | Linear progression, Soft currency only, Cosmetic shop |
| Live-service plan | Battle pass, Limited events, Daily quests, Prestige systems |
| Competitive focus | Cosmetic-only monetization, Async/Real-time PvP, Leaderboards |
