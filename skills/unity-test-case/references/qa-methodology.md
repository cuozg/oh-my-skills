# QA Methodology for Unity Game Testing

## Table of Contents
1. [Test Case Design Techniques](#techniques)
2. [Unity-Specific Testing Areas](#unity-areas)
3. [Priority Classification](#priority)
4. [Edge Case Identification Heuristics](#edge-cases)
5. [Test Coverage Categories](#coverage)

---

## Test Case Design Techniques <a id="techniques"></a>

### Equivalence Partitioning
Divide inputs into valid/invalid groups. Test one value per partition.
- Currency amounts: negative, zero, minimum, typical, maximum, overflow
- Level ranges: below min, at min, mid-range, at max, above max

### Boundary Value Analysis
Test at and around boundaries.
- Timer at 0s, 1s, max-1s, max
- Inventory at 0, 1, max-1, max, max+1
- Currency exactly at price, price-1, price+1

### State Transition Testing
Map all game states and transitions. Verify:
- Valid transitions occur correctly
- Invalid transitions are blocked
- State persists across scene loads, app backgrounding, reconnection

### Decision Table Testing
For features with multiple conditions (e.g., offer eligibility):

| VIP Level | Has Currency | In Schedule | Stock > 0 | Result |
|-----------|-------------|-------------|-----------|--------|
| Met       | Yes         | Yes         | Yes       | Can purchase |
| Met       | No          | Yes         | Yes       | Show disabled |
| Not Met   | Yes         | Yes         | Yes       | Show VIP required |
| Met       | Yes         | No          | Yes       | Don't show offer |
| Met       | Yes         | Yes         | No        | Don't show offer |

---

## Unity-Specific Testing Areas <a id="unity-areas"></a>

### Scene/Screen Navigation
- Verify correct screen loads
- Back button behavior
- Deep link navigation
- Scene transition animations
- Loading state handling

### UI/UX Testing
- Element positioning and alignment
- Text truncation and overflow
- Responsive layout across resolutions (16:9, 18:9, 20:9, iPad)
- Touch target sizes (minimum 44x44 points)
- Animation playback and timing
- Localization text fitting
- Safe area compliance (notch, home indicator)

### Data Persistence
- Save/load state across sessions
- PlayerPrefs integrity
- Server sync after reconnection
- Offline mode behavior
- Data migration between versions

### Performance Indicators
- Frame rate during feature interaction
- Memory allocation spikes
- Asset loading times
- Network request latency
- Battery impact on mobile

### Platform-Specific
- iOS: notch, dynamic island, haptics, IAP sandbox
- Android: back button, varied screen sizes, split screen
- WebGL: browser compatibility, memory limits

---

## Priority Classification <a id="priority"></a>

### Critical (P0)
- Core game loop broken
- Data loss or corruption
- Crash/ANR
- Security vulnerability
- Payment/IAP failure

### High (P1)
- Major feature not working as designed
- Blocker for progression
- Significant UI/UX broken
- Server communication failure

### Medium (P2)
- Minor feature deviation
- Non-blocking UI issues
- Edge case failures
- Performance degradation (not crash)

### Low (P3)
- Cosmetic issues
- Minor text/typo
- Enhancement suggestions
- Rare edge cases with workarounds

---

## Edge Case Identification Heuristics <a id="edge-cases"></a>

### CRUCSPIC-STMP Mnemonic
- **C**oncurrency: Multiple simultaneous actions
- **R**ace conditions: Timing-dependent behavior
- **U**ndo/redo: Reversibility of actions
- **C**ancellation: Mid-operation cancellation
- **S**tate: Unexpected starting states
- **P**ermissions: Missing or revoked permissions
- **I**nterruption: Phone call, notification, backgrounding
- **C**onnectivity: Offline, slow, reconnection
- **S**cale: Zero items, one item, maximum items
- **T**ime: Timezones, DST, midnight boundary, server time mismatch
- **M**emory: Low memory, cache full
- **P**latform: OS version, device model, screen size

### Common Game-Specific Edge Cases
- Double-tap on purchase button
- Rapid screen switching during loading
- App kill during save operation
- Clock manipulation (time travel)
- Multiple offers/events ending simultaneously
- Currency overflow (Int32.MaxValue)
- Network timeout during transaction
- Session expiry mid-interaction

---

## Test Coverage Categories <a id="coverage"></a>

Standard categories to ensure comprehensive coverage:

1. **Functional**: Does the feature work as specified?
2. **UI/UX**: Does it look and feel correct?
3. **Integration**: Does it work with other systems?
4. **Boundary/Edge**: What happens at limits?
5. **Error Handling**: How does it handle failures?
6. **Performance**: Is it fast and efficient enough?
7. **Security**: Can it be exploited?
8. **Compatibility**: Does it work across platforms/devices?
9. **Regression**: Does it break existing features?
10. **Data Integrity**: Is data saved/loaded correctly?
