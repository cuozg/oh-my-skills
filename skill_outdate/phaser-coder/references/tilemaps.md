# Tilemaps

## Tiled Workflow

1. Create map in **Tiled** editor → export as JSON
2. Load in Phaser → create layers → set collision

## Loading

```javascript
preload() {
  this.load.tilemapTiledJSON('level1', 'assets/maps/level1.json');
  this.load.image('tiles', 'assets/tilesets/tileset.png');
  // For extruded tilesets (prevents bleeding):
  this.load.image('tiles', 'assets/tilesets/tileset-extruded.png');
}
```

## Creating the Map

```javascript
create() {
  const map = this.make.tilemap({ key: 'level1' });

  // tilesetName must match the name in Tiled
  const tileset = map.addTilesetImage('terrain', 'tiles');
  // With extruded margins:
  // const tileset = map.addTilesetImage('terrain', 'tiles', 16, 16, 1, 2);

  // Layer names must match Tiled layer names
  const bgLayer = map.createLayer('Background', tileset, 0, 0);
  const groundLayer = map.createLayer('Ground', tileset, 0, 0);
  const decorLayer = map.createLayer('Decorations', tileset, 0, 0);

  // Collision by tile index
  groundLayer.setCollisionByExclusion([-1]); // all tiles except empty

  // Or by property set in Tiled
  groundLayer.setCollisionByProperty({ collides: true });

  // Or specific tile indices
  groundLayer.setCollision([1, 2, 3, 15, 16, 17]);

  // Physics collider
  this.physics.add.collider(player, groundLayer);

  // World bounds from map size
  this.physics.world.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
  this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
}
```

## Object Layers

Spawn entities from Tiled object layers:

```javascript
const spawnPoints = map.getObjectLayer('Spawns').objects;
spawnPoints.forEach(obj => {
  if (obj.name === 'player') {
    this.player = this.physics.add.sprite(obj.x, obj.y, 'player');
  } else if (obj.type === 'enemy') {
    this.enemies.create(obj.x, obj.y, 'enemy');
  }
});

// Access custom properties set in Tiled
const door = map.findObject('Objects', obj => obj.name === 'door');
const targetScene = door.properties.find(p => p.name === 'target').value;
```

## Dynamic Tiles

```javascript
// Replace tile at position
groundLayer.putTileAt(5, tileX, tileY);

// Remove tile
groundLayer.removeTileAt(tileX, tileY);

// Get tile at world position
const tile = groundLayer.getTileAtWorldXY(pointer.worldX, pointer.worldY);
if (tile) {
  tile.index = 10; // change tile
}

// Tile callbacks
groundLayer.setTileIndexCallback([42], (sprite, tile) => {
  // Triggered when physics body overlaps this tile index
  tile.index = -1; // remove
}, this);
```

## Multiple Tilesets

```javascript
const terrain = map.addTilesetImage('terrain', 'terrain-img');
const buildings = map.addTilesetImage('buildings', 'buildings-img');

// Pass array of tilesets to createLayer if layer uses multiple
const layer = map.createLayer('World', [terrain, buildings]);
```

## Gotchas

- Layer and tileset names are **case-sensitive** and must exactly match Tiled export
- Object layer coordinates in Tiled use top-left origin — sprites default to center origin, so objects may appear offset by half their size
- Tile bleeding (lines between tiles) → use extruded tilesets (1px margin/spacing) or set `roundPixels: true` in camera
- `setCollisionByProperty` requires you to set custom properties on tiles in Tiled's tileset editor
- Large tilemaps: use `cullPadding` and layer culling is automatic — don't worry about manual culling
