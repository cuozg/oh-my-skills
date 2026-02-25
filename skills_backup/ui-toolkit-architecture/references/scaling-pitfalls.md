# UI Toolkit Architecture — Scaling & Pitfalls

## Scaling Guidelines by Project Size

| Size | Strategy |
|------|----------|
| Small (1-5 screens) | Single UIDocument, screen toggling |
| Medium (5-15) | UIDocument per screen, ScreenManager |
| Large (15+) | Module-based, lazy loading, screen pooling |

### Large Projects

Group by module (Shop/, Inventory/, Social/), shared `Common/` folder, central `UIScreenManager`, lazy-load UXML on first access.

## Common Pitfalls & Fixes

| Pitfall | Fix |
|---------|-----|
| God Screen Controller (500+ lines) | Split into sub-controllers per panel |
| Inline styles in UXML | Always use USS classes |
| Deep inheritance chains | Composition with interfaces |
| Missing `partial` on [UxmlElement] | Source gen fails — always `partial class` |
| Q() in bindItem | Cache element refs in makeItem |
| No OnDisable cleanup | Unregister events in OnDisable |
