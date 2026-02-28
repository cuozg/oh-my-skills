# QA Methodology for Unity Game Testing

## Test Case Design Techniques

**Equivalence Partitioning**: Divide inputs into valid/invalid groups, test one per partition. E.g., currency: negative, zero, minimum, typical, maximum, overflow.

**Boundary Value Analysis**: Test at and around boundaries. Timer at 0s/1s/max-1s/max. Inventory at 0/1/max-1/max/max+1.

**State Transition**: Map all game states and transitions. Verify valid transitions occur, invalid are blocked, state persists across scene loads/backgrounding/reconnection.

**Decision Table**: For multi-condition features (e.g., offer eligibility: VIP level × currency × schedule × stock → result).

## Unity-Specific Testing Areas

**Scene/Navigation**: Correct screen loads, back button, deep links, transition animations, loading states.

**UI/UX**: Positioning, text truncation, responsive layout (16:9/18:9/20:9/iPad), touch targets (min 44x44pt), animations, localization fitting, safe area compliance.

**Data Persistence**: Save/load across sessions, PlayerPrefs integrity, server sync after reconnection, offline mode, version migration.

**Performance**: Frame rate, memory spikes, asset loading times, network latency, battery impact.

**Platform-Specific**: iOS (notch, dynamic island, haptics, IAP sandbox), Android (back button, varied screens, split screen), WebGL (browser compatibility, memory limits).

## Priority Classification

- **P0 Critical**: Core loop broken, data loss, crash/ANR, security vulnerability, payment failure
- **P1 High**: Major feature broken, progression blocker, significant UI broken, server failure
- **P2 Medium**: Minor deviation, non-blocking UI issues, edge case failures, performance degradation
- **P3 Low**: Cosmetic, typo, enhancement suggestions, rare edge cases with workarounds

## Edge Case Heuristics (CRUCSPIC-STMP)

**C**oncurrency, **R**ace conditions, **U**ndo/redo, **C**ancellation, **S**tate (unexpected), **P**ermissions, **I**nterruption (phone call/backgrounding), **C**onnectivity (offline/slow/reconnect), **S**cale (zero/one/max), **T**ime (timezones/DST/midnight), **M**emory (low/cache full), **P**latform (OS/device/screen)

Game-specific: double-tap purchase, rapid screen switching during load, app kill during save, clock manipulation, concurrent event endings, currency overflow, network timeout mid-transaction, session expiry.

## Test Coverage Categories

Functional, UI/UX, Integration, Boundary/Edge, Error Handling, Performance, Security, Compatibility, Regression, Data Integrity.
