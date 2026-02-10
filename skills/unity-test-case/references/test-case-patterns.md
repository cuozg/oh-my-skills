# Test Case Patterns for Unity Games

## Table of Contents
1. [ID Convention](#id-convention)
2. [Test Case Structure](#structure)
3. [Section Organization Patterns](#section-patterns)
4. [Writing Style Guide](#writing-style)
5. [Common Test Patterns by Feature Type](#common-patterns)

---

## ID Convention <a id="id-convention"></a>

Format: `{MODULE}-{SECTION}-{SEQ}`

Examples:
- `SSL-SP-001` (Sale System Lite, Surfacing Points, test 1)
- `SHOP-UI-003` (Shop, UI/UX, test 3)
- `MATCH-FUNC-012` (Match, Functional, test 12)

Module abbreviation: 2-5 uppercase chars derived from feature name.
Section codes: `SP` (surfacing points), `UI` (UI/UX), `FUNC` (functional), `EDGE` (edge cases), `INTG` (integration), `PERF` (performance), `SEC` (security), `DATA` (data integrity).

---

## Test Case Structure <a id="structure"></a>

Each test case MUST include:

| Field | Required | Description |
|-------|----------|-------------|
| ID | Yes | Unique identifier following convention above |
| Title | Yes | Concise, descriptive name (verb + object pattern) |
| Preconditions | Yes | Setup state required before test execution |
| Steps | Yes | Numbered, atomic actions the tester performs |
| Expected Results | Yes | Observable outcomes per step or group of steps |
| Priority | Yes | Critical / High / Medium / Low |
| Notes | No | Additional context, known issues, dependencies |

### Continuation Rows
When a test scenario requires multiple phases (e.g., setup → action → verify → followup), use continuation rows that share the same section but omit the Title. This groups related steps under one logical test.

Example pattern from reference:
```
Row 1: Title="Cooldown" | Steps="Start game, go to home" | Expected="Offer A appears"
Row 2: Title="" | Steps="Go to another screen, back to home" | Expected="Offer B appears"
Row 3: Title="" | Steps="Wait cooldown X1, back to home" | Expected="Offer A appears"
```

---

## Section Organization Patterns <a id="section-patterns"></a>

Organize test cases into sections by testing concern:

### Pattern 1: Location/Trigger-Based (for features that appear at multiple points)
Group by WHERE the feature surfaces:
- Home screen
- Pre-match screens
- Post-match screens
- HUD elements
- Currency depletion points

### Pattern 2: Layer-Based (for complex features)
1. **UI/UX**: Visual correctness, layout, badges, text
2. **Functional**: Business logic, rules, calculations
3. **Integration**: Interaction with other systems
4. **Edge Cases**: Boundary conditions, error states

### Pattern 3: User Journey (for flow-oriented features)
1. **Discovery**: How user finds the feature
2. **Interaction**: Core usage flow
3. **Transaction**: Purchase/confirm/submit
4. **Post-Action**: Results, rewards, state changes
5. **Error Recovery**: Failure handling

---

## Writing Style Guide <a id="writing-style"></a>

### Preconditions
- Start each with a dash (`-`)
- Use "Setup" prefix: `- Setup SSL Offer with SP = Home`
- State player requirements: `- The player is VIP level 5`
- State data requirements: `- Offer stock is 1`

### Steps
- Start each with a dash (`-`)
- Begin with action verb: Start, Go to, Tap on, Observe, Wait, Select
- First step is typically: `- Start the game`
- Be specific about navigation: `- Go to Career HUB` → `- Go to Career Daily Tour`
- One action per step

### Expected Results
- Start each with a dash (`-`)
- Use present tense: "displays", "appears", "is active"
- Be specific: "The SSL Offer automatically appears" not "Offer shows"
- Include negative assertions: "The player is unable to purchase"
- End UI checks with: "There is no UI issue"

---

## Common Test Patterns by Feature Type <a id="common-patterns"></a>

### Popup/Offer System
1. Trigger at each surfacing point → verify display
2. UI element correctness (banner, badges, buttons, text)
3. Priority ordering between multiple offers
4. Cooldown mechanics between displays
5. Global count limits
6. Purchase success/failure flows
7. Schedule/timing constraints
8. Eligibility conditions (VIP, level, etc.)
9. Stock/inventory limits
10. Platform-specific variants (mobile vs web)

### Currency/Economy
1. Earn currency → verify balance update
2. Spend currency → verify deduction and item receipt
3. Insufficient funds → verify block and messaging
4. Overflow protection at max values
5. Cross-session persistence
6. Server reconciliation after offline period

### Match/Battle Flow
1. Pre-match setup and lineup
2. Match gameplay core loop
3. Post-match results and rewards
4. Win/loss/draw state handling
5. Disconnect during match
6. Timeout handling
7. Matchmaking edge cases

### Event/Tournament
1. Event availability window (start/end)
2. Entry requirements
3. Progress tracking
4. Reward tiers and distribution
5. Leaderboard accuracy
6. Event end behavior (grace period, cleanup)

### Inventory/Collection
1. Item acquisition and display
2. Item usage/equip/unequip
3. Sorting and filtering
4. Capacity limits
5. Item removal/consumption
6. Duplicate handling
