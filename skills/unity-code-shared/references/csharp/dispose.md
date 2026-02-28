# C# Quality & Code Hygiene — Part 3: Resource Management & Collections

Dispose pattern, collection initialization.

## Dispose Pattern

```csharp
// ✅ GOOD: IDisposable for unmanaged resources
public sealed class TextureManager : IDisposable
{
    private Texture2D? texture;
    private bool disposed;

    public void Dispose()
    {
        if (disposed) return;
        if (texture != null)
        {
            UnityEngine.Object.Destroy(texture);
            texture = null;
        }
        disposed = true;
    }
}

// ❌ BAD: Forgetting to dispose
public class TextureManager
{
    private Texture2D texture; // Never disposed → memory leak
}
```

## Collection Initialization

```csharp
// ✅ GOOD: Initialize collections to avoid null
private readonly List<Player> players = new();
private readonly Dictionary<string, Item> items = new();
private readonly HashSet<int> visitedIds = new();

// ❌ BAD: Null collections
private List<Player> players; // Null until first use → NullReferenceException
```

---

Continue in **strings.md** for string handling, magic numbers, and boolean parameters.
