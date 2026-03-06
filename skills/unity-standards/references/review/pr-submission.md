# PR Review Submission

## API & Payload

```bash
# Submit review — ALL comments in single POST call
gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input review.json
# Get head SHA
gh api repos/{owner}/{repo}/pulls/{pr} --jq '.head.sha'
```

```json
{
  "event": "REQUEST_CHANGES",
  "body": "{summary — see Body Template below}",
  "comments": [
    { "path": "Assets/Scripts/Player.cs", "line": 42, "side": "RIGHT",
      "body": "**🔴 Issue Title** — `CRITICAL`\n...\n```suggestion\n{fix}\n```" }
  ]
}
```

`line` = right-side file line number (not diff position). `side` always `RIGHT`. Max 32 KB/comment. Group by file.

## Body Template

Post as `body` field. Omit rows with 0 findings.
````
## 📋 Code Review — PR #{number}
{1-2 sentence verdict}
| | Category | Findings | Top Severity |
|---|---|:---:|---|
| 💥 | Breaking / Crash Risk | {n} | 🔴 `CRITICAL` |
| ⚠️ | Bugs / Incorrect Behavior | {n} | 🟠 `HIGH` |
| 🎮 | Unity-Specific Risks | {n} | 🟡 `MEDIUM` |
| 💡 | Improvements | {n} | 🔵 `LOW` / ⚪ `STYLE` |
**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT
````

## Event Decision

| Decision | Condition |
|---|---|
| `REQUEST_CHANGES` | Any 🔴 CRITICAL or ≥2 🟠 HIGH |
| `REQUEST_CHANGES` or `COMMENT` | 1 🟠 HIGH — reviewer judgment |
| `COMMENT` | Only 🟡/🔵/⚪ (no blockers) |
| `APPROVE` | Zero 🔴/🟠 + all addressed |

## Inline Comment Examples

**CRITICAL** — cause, impact, suggestion required:
````
**🔴 Null reference crash in trigger handler** — `CRITICAL`
`other.GetComponent<DamageDealer>().damageAmount` assumes every collider has a DamageDealer.
```suggestion
if (other.TryGetComponent<DamageDealer>(out var dealer))
    TakeDamage(dealer.damageAmount);
```
````

**HIGH** — lifecycle cleanup gap:
````
**🟠 Public events not cleaned up on destroy** — `HIGH`
External subscribers hold delegate references after `Destroy(gameObject)`, preventing GC.
```suggestion
private void OnDestroy()
{
    OnPlayerDied = null;
    OnHealthChanged = null;
}
```
````

**MEDIUM** — problem + suggestion:
````
**🟡 GetComponent called every frame** — `MEDIUM`
Per-frame `GetComponent<SpriteRenderer>()` in Update causes lookup overhead.
```suggestion
private SpriteRenderer _spriteRenderer;
private void Awake() => _spriteRenderer = GetComponent<SpriteRenderer>();
```
````

**LOW/STYLE** — compact, suggestion optional:
````
**🔵 Exposed mutable collection** — `LOW`
`GetAllItems()` returns the internal list, allowing external mutation.
```suggestion
public IReadOnlyList<ItemData> GetAllItems() => items.AsReadOnly();
```
````
