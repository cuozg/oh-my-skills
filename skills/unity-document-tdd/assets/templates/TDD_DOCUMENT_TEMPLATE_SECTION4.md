<!-- PART 4/4 of TDD_DOCUMENT_TEMPLATE.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

### 8.2 Integration Tests
<!-- System-level tests ensuring components work together. -->
*   [ ] Verify `FeatureController` initializes `UIManager`.
*   [ ] Verify Save/Load cycle preserves state.

### 8.3 Manual Testing Checklist
<!-- QA steps. -->
- [ ] Step 1: ...
- [ ] Step 2: ...

## 9. Performance Considerations

### 9.1 Memory Budget
*   **Texture Memory**: ~5MB (Atlas)
*   **Heap Allocation**: Zero alloc in Update loop.

### 9.2 CPU Budget
*   **Target**: < 0.5ms per frame on target device.

### 9.3 Optimization Strategies
*   Cache Component references (no `GetComponent` in Update).
*   Use `StringBuilder` for text updates.

## 10. Platform Considerations
| Platform | Concern | Approach |
|:---|:---|:---|
| **Mobile** | Battery drain | Throttle updates when idle. |
| **All** | Screen safe area | Use UI Toolkit SafeArea container. |

## 11. Security & Data Privacy
*   No PII stored.
*   Save data obfuscation (optional).

## 12. Open Questions
<!-- Things we don't know yet. -->
- [ ] ?

## 13. References
<!-- Links to tickets, docs, designs. -->
- [JIRA-123](...)
- [Figma Design](...)

## 14. Change Log
| Date | Author | Change Description |
|:---|:---|:---|
| {Date} | AI Assistant | Initial Draft |
