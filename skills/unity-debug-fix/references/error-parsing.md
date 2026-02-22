# Error Parsing Guide

## From Stack Trace
```
NullReferenceException: Object reference not set to an instance of an object
  at PlayerController.TakeDamage (System.Int32 damage) [0x00012] in /Assets/Scripts/PlayerController.cs:42
  at EnemyAI.Attack () [0x00034] in /Assets/Scripts/EnemyAI.cs:87
  at EnemyAI.Update () [0x00056] in /Assets/Scripts/EnemyAI.cs:31
```

Extract:
- **Error**: NullReferenceException
- **Crash Site**: `PlayerController.cs:42` — `TakeDamage` method
- **Call Chain**: `EnemyAI.Update:31` -> `EnemyAI.Attack:87` -> `PlayerController.TakeDamage:42`
- **Direction**: Read bottom-to-top (trigger -> crash)

## From Compiler Error
```
Assets/Scripts/GameManager.cs(15,25): error CS0246: The type or namespace name 'PlayerData' could not be found
```

Extract:
- **Error**: CS0246 — missing type
- **File**: `GameManager.cs:15`
- **Subject**: `PlayerData` type
