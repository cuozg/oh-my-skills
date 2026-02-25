# Tilemap Scripting & Custom Rules

## Tilemap Scripting

```csharp
public class TilemapManager : MonoBehaviour
{
    [SerializeField] private Tilemap _tilemap;
    [SerializeField] private TileBase[] _walkableTiles;
    
    public bool IsWalkable(Vector3Int gridPos)
    {
        TileBase tile = _tilemap.GetTile(gridPos);
        if (tile == null) return false;
        return System.Array.Exists(_walkableTiles, t => t == tile);
    }
    
    public void SetTile(Vector3Int gridPos, TileBase tile)
    {
        _tilemap.SetTile(gridPos, tile);
    }
    
    public BoundsInt GetBounds() => _tilemap.cellBounds;
    
    public Vector3Int WorldToCell(Vector3 worldPos) 
        => _tilemap.WorldToCell(worldPos);
}
```

### Procedural Tilemap Generation

```csharp
public class ProceduralTilemap : MonoBehaviour
{
    [SerializeField] private Tilemap _tilemap;
    [SerializeField] private TileBase _groundTile;
    
    public void GeneratePerlin(int width, int height, float scale)
    {
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                float noise = Mathf.PerlinNoise(x * scale, y * scale);
                if (noise > 0.5f)
                    _tilemap.SetTile(new Vector3Int(x, y, 0), _groundTile);
            }
        }
    }
}
```

## Custom RuleTile

```csharp
using UnityEngine.Tilemaps;

public class AutoTile : RuleTile<AutoTile.Neighbor>
{
    public class Neighbor : RuleTile.TilingRule.Neighbor
    {
        public const int Matching = 1;
        public const int Empty = 0;
    }
    
    public override bool RuleMatches(TilingRule rule, Vector3Int pos, ITilemap tilemap, ref Matrix4x4 transform)
    {
        return base.RuleMatches(rule, pos, tilemap, ref transform);
    }
}
```

Usage: Set neighbors in Inspector, RuleTile auto-selects sprite based on surroundings.
