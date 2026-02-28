# Unity Best Practices - Advanced Topics

## Data Structures & Algorithms

- [ ] Collections sized appropriately (Array for fixed size, List for dynamic)
- [ ] Dictionary keys are immutable and have good hashCode
- [ ] Searches use appropriate structures (dict lookup vs linear scan)
- [ ] Time complexity understood (O(n) searches in Update = bad)

## Networking & Multiplayer

- [ ] Network messages validated before processing (no deserialization attacks)
- [ ] Latency compensated (client prediction, server reconciliation)
- [ ] Bandwidth usage monitored (logging amount sent/received per frame)
- [ ] Cheating vectors identified (especially on client-side logic)
- [ ] Proper netcode pattern used (authoritative server or deterministic client)

## Accessibility

- [ ] UI elements have proper color contrast (WCAG AA standard)
- [ ] Text is resizable (not hardcoded pixel sizes)
- [ ] Button targets are large enough for touch (48dp minimum)
- [ ] Colorblind modes considered (not color-only indicators)
- [ ] Audio has captions (if speech present)

## Scripting Standards

- [ ] Null checks consistent (defensive programming)
- [ ] Constants used instead of magic numbers
- [ ] Comments explain WHY not WHAT (code shows what)
- [ ] Method signatures clear (parameters named, return type obvious)
- [ ] No "temp" or "test" code left in production
