# Acceptance Criteria Guide

A criterion is **testable** when an autonomous agent can independently verify it in the Unity Editor without human intervention.

## The Testability Rule

> Every criterion names **what**, **where**, and **how to observe it using Unity tools**.

If any of those three are missing, the criterion is not testable.

## Good vs Bad Criteria for Agents

| Bad | Why it fails | Good |
|-----|--------------|------|
| "Player moves smoothly" | Subjective, no metric. | `PlayerController` velocity > `0` on input, verified by Play Mode test. |
| "UI looks good" | No component, no check. | `MainMenu` prefab contains a `Button` labeled "Start". |
| "Enemy takes damage" | No specific method. | `EnemyHealth.TakeDamage(10)` reduces `currentHealth` by `10`, verified by Edit Mode test. |

## Verification Methods

Ensure criteria can be verified via:
1. **Code Appearance:** Script, method, or property exists in the project.
2. **Tests:** A specific test file passes in the Unity Test Runner.
3. **Scene Checks:** A GameObject exists with specific components and values.
4. **Screenshots:** Visual validation via Game or Scene view captures.
