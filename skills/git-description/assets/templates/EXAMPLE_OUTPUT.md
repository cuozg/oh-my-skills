## ✅ Checklist
- [ ] Did you dev test your changes?
- [ ] Did you check the login flow. Tried login and logout
- [ ] Did you check and clean up any new errors/warnings that might have been introduced with these changes?
- [ ] Are there any prefab conflicts?
- [ ] If prefab conflicts exist, have you regenerated the low/med prefabs?

## 🔍High Level Summary
Add real-time multiplayer lobby with matchmaking queue and ready-check flow. Replaces the previous static lobby screen with a dynamic, event-driven system that supports up to 8 players.

## 🔍 Specific details of the changes made
### Matchmaking System
- **MatchmakingManager.cs**: New singleton managing queue state, server polling, and match assignment. Uses coroutine-based retry with exponential backoff.
- **MatchmakingAPI.cs**: REST client for matchmaking service endpoints. Handles auth token refresh on 401.

### Lobby UI
- **LobbyScreenController.cs**: Rebuilt from MonoBehaviour to UI Toolkit. Binds player slots via runtime data binding.
- **LobbyScreen.uxml / LobbyScreen.uss**: New layout with responsive player grid and ready-check buttons.

### Data Changes
- **PlayerLobbyData.cs**: New ScriptableObject container for lobby state. Serializes via JsonUtility.

## 🔍 Linked Feature TDD (if applicable).
https://docs.google.com/document/d/1abc...

## 🎯 JIRA Ticket(s) (if applicable)
https://scopely.atlassian.net/browse/WHIP-4521

## 🏗️ Build Number - Build Links

## 👀 Screenshots (if applicable)

## 💬 Additional Notes
- **Breaking**: Removes legacy `LobbyManager` — any code referencing it must migrate to `MatchmakingManager.Instance`.
- **Config**: Requires new `MATCHMAKING_URL` entry in server config.
- **Test focus**: Ready-check timeout edge case when a player disconnects mid-countdown.
