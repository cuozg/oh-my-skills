# Test Case Patterns for Unity Games

## ID Convention

Format: `{MODULE}-{SECTION}-{SEQ}` (e.g., `SSL-SP-001`, `SHOP-UI-003`)

Module: 2-5 uppercase chars. Section codes: `SP` (surfacing points), `UI`, `FUNC` (functional), `EDGE`, `INTG` (integration), `PERF`, `SEC`, `DATA`.

## Test Case Structure

| Field | Required | Description |
|---|---|---|
| ID | Yes | Unique identifier per convention |
| Title | Yes | Verb + object pattern |
| Preconditions | Yes | Setup state before execution |
| Steps | Yes | Numbered atomic actions |
| Expected Results | Yes | Observable outcomes per step |
| Priority | Yes | Critical / High / Medium / Low |
| Notes | No | Context, known issues, dependencies |

**Continuation rows**: Multi-phase scenarios share section, omit Title on subsequent rows.

## Section Organization

1. **Location-based**: Group by WHERE feature surfaces (home, pre-match, post-match, HUD, currency depletion)
2. **Layer-based**: UI/UX → Functional → Integration → Edge Cases
3. **User Journey**: Discovery → Interaction → Transaction → Post-Action → Error Recovery

## Writing Style

- **Preconditions**: Dash-prefixed, `- Setup SSL Offer with SP = Home`
- **Steps**: Action verb first: Start, Go to, Tap on, Observe, Wait, Select. One action per step.
- **Expected Results**: Present tense, specific: "The SSL Offer automatically appears". Include negative assertions.

## Common Patterns by Feature Type

**Popup/Offer**: Trigger at surfacing points, UI correctness, priority ordering, cooldown, count limits, purchase flows, schedule constraints, eligibility, stock limits.

**Currency/Economy**: Earn → verify balance, spend → verify deduction, insufficient funds block, overflow protection, cross-session persistence, server reconciliation.

**Match/Battle**: Pre-match setup, core loop, post-match rewards, win/loss/draw, disconnect handling, timeout, matchmaking edge cases.

**Event/Tournament**: Availability window, entry requirements, progress tracking, reward tiers, leaderboard accuracy, event end behavior.

**Inventory/Collection**: Acquisition, usage/equip, sorting/filtering, capacity limits, removal, duplicate handling.
