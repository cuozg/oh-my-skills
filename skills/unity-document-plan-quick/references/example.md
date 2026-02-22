# Example Assessment

**Input**: "Add daily login reward system"

**Result**:

```
## Assessment: Daily Login Reward System

### Size: Medium
New system with data persistence and UI, but follows existing reward patterns.
- 6-8 files: model, manager, UI screen, save data, config SO, tests
- Existing RewardManager and popup patterns can be extended
- Needs new persistent timestamp tracking

### Time Estimate: 12-20 hours
Core logic is straightforward; UI and edge cases add time.
- Core logic + data model: 3-5h
- UI screen + animations: 4-6h
- Save/load + timezone edge cases: 3-5h
- Testing + polish: 2-4h

### Risk: Medium
Timezone and calendar-day boundaries are the main difficulty.
- Server vs local time discrepancy can allow exploits
- Day-rollover logic across timezones is error-prone
- Offline/clock-manipulation detection needed
- Save data migration if reward structure changes later

### Impact
- **SaveManager**: New daily-login data block in save file
- **RewardManager**: New reward source type to integrate
- **MainMenuUI**: New button/indicator for daily reward status
- **Analytics**: New events for login streak tracking
```
