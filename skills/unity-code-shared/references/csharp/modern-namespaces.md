# Modern C# Features — Part 3: Namespaces & Organization

Global using directives, file-scoped namespaces, and namespace best practices.

---

## Global Using Directives

```csharp
// ✅ GOOD: GlobalUsings.cs in project root
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using UnityEngine;
global using UnityEngine.Events;

// Now all files in project can use these without explicit using statements
// File.cs (no using statements needed)
public class Player
{
    private List<Item> inventory; // List is available globally
}

// ✅ GOOD: Organize in separate GlobalUsings.cs file
// GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;
global using UnityEngine;

// ❌ BAD: Scattered global usings across multiple files
// File1.cs
global using System.Collections.Generic;
// File2.cs
global using System.Linq;
// (Fragmented and hard to maintain)
```

---

## File-Scoped Namespaces

```csharp
// ✅ GOOD: File-scoped namespace (C# 10+)
namespace GameLogic;

public class Player
{
    public string Name { get; set; }
}

public class Team
{
    public List<Player> Members { get; set; }
}

// ✅ GOOD: Reduces nesting, more readable
// Compare to old syntax:
// namespace GameLogic
// {
//     public class Player { ... }
//     public class Team { ... }
// } // Extra closing brace, extra indentation

// ❌ BAD: Multiple namespaces in one file (rare but bad)
// namespace GameLogic { ... }
// namespace UILogic { ... } // Split into separate files
```

---

## Combining Global Using + File-Scoped Namespaces

```csharp
// ✅ GOOD: GlobalUsings.cs
// Assets/Scripts/GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using UnityEngine;
global using Game.Player;

// ✅ GOOD: Player.cs (very clean)
// Assets/Scripts/Game/Player/Player.cs
namespace Game.Player;

public class Player
{
    public string Name { get; set; }
    public List<Item> Inventory { get; set; }
}
```

---

Continue in **modern-advanced.md** for Target-Typed new, Deconstruction, and more.
