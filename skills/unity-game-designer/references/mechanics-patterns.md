# Game Mechanics Design Patterns

## 1. Progression Patterns

### 1.1 Linear Progression
Sequential content, each stage gates next. **Use for**: narrative, puzzle, tutorial-heavy games.
- Store as `int currentLevel` in PlayerPrefs. Use ScriptableObject for level definitions.
- **Risks**: stuck → churn, no replay value.

### 1.2 Branching Progression
Multiple paths/skill trees creating distinct playstyles. **Use for**: RPGs, strategy, high replay value.
- Model as graph: SO nodes with `List<SkillNode> children`. Use `HashSet<string>` for unlocked nodes.
- **Risks**: exponential balance complexity, "trap" builds.

### 1.3 Open-Ended / Sandbox
Player defines own goals; systems provide tools. **Use for**: creative, simulation, survival.
- Save systems must handle arbitrary world state. Consider chunk-based serialization.
- **Risks**: new players lost, hard to measure progression.

### 1.4 Prestige / Reset
Reset progress for permanent bonuses, progress faster each cycle. **Use for**: idle/incremental, long-term retention.
- Separate `PrestigeData` (permanent) vs `RunData` (reset) with `[Serializable]` classes.
- **Risks**: first prestige must feel worth it.

## 2. Economy Patterns

### 2.1 Dual Currency (Soft + Premium)
Soft earned freely, premium earned slowly or purchased. Industry standard for F2P mobile.
- **Balance**: Free player earns 5-10% of premium pack per week.
- Represent as ScriptableObjects with earn rates and sinks.

### 2.2 Energy / Stamina Gating
Limits play sessions, regenerates over time or purchasable.
- **Balance**: Allow 3-5 meaningful sessions/day. Refill ads = good deal, not necessity.

### 2.3 Crafting / Resource Conversion
Raw resources combine into higher-value items. N resources → N² recipes.
- `CraftingRecipe { List<ResourceAmount> inputs; ItemData output; float craftTime; }`
- **Risks**: recipe complexity overwhelms casuals.

## 3. Social & Multiplayer Patterns

### 3.1 Asynchronous Competition
Compete against others' data/replays, not real-time. Simpler networking, no latency.

### 3.2 Cooperative Guilds / Clans
Persistent groups sharing goals/resources. Social obligation drives D30+ retention.

### 3.3 Social Gifting / Sharing
Send/receive items between friends. Free re-engagement channel.

## 4. Monetization Patterns

### 4.1 Battle Pass / Season Pass
Time-limited free+premium progression track. Predictable recurring revenue.
- Free tier must showcase premium value. Season: 4-8 weeks. Premium earnable through play.

### 4.2 Gacha / Loot Box
Randomized rewards for currency spend. High ARPU but legal restrictions.
- **Required**: pity/guarantee system, rate disclosure, no gameplay-critical exclusives, alternative earn paths.

### 4.3 Cosmetic-Only
Visual-only purchases, no gameplay advantage. Fair perception, high goodwill.
- Lower revenue ceiling. Requires constant art pipeline.

### 4.4 Rewarded Ads
Optional video ads for in-game rewards. Monetizes non-payers.
- Always rewarded, never forced. Max 5-8/day. Place at natural break points.

## 5. Engagement & Retention Patterns

### 5.1 Daily Login / Streak Rewards
Escalating rewards for consecutive logins. Variants: forgiving (no reset), punishing (reset on miss), calendar-based.

### 5.2 Limited-Time Events
Temporary content creating urgency. Types: seasonal (2-4 weeks), competitive (3-7 days), collaborative (community-wide goal).

### 5.3 Daily Quests / Missions
Rotating objectives directing daily activity. Effective with Battle Pass XP.

## 6. Core Loop Archetypes

| Archetype | Loop | Key Tension |
|:---|:---|:---|
| **Battle** (RPG) | Prepare → Fight → Reward → Upgrade | Preparation determines outcome |
| **Build** (Tycoon) | Earn → Build → Earn more → Optimize | Opportunity cost |
| **Explore** (Adventure) | Discover → Challenge → Reward → Unlock | Curiosity |
| **Match** (Puzzle) | Play → Score → Feedback → Next round | Improving score |
| **Create** (Sandbox) | Build → Share → Feedback → Iterate | Self-expression |
| **Idle** (Incremental) | Automate → Leave → Collect → Upgrade | Prestige timing |

## Pattern Selection Guide

| Constraint | Recommended Patterns |
|:---|:---|
| Mobile, casual | Linear progression, Energy gating, Rewarded ads, Daily rewards |
| Mobile, mid-core | Branching progression, Dual currency, Battle pass, Guilds |
| PC, hardcore | Open-ended progression, Crafting, Real-time PvP, Cosmetic monetization |
| Short dev timeline | Linear progression, Soft currency only, Cosmetic shop |
| Live-service | Battle pass, Limited events, Daily quests, Prestige systems |
| Competitive focus | Cosmetic-only monetization, Async/Real-time PvP, Leaderboards |
