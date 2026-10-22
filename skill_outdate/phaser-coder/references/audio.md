# Audio

## Loading

```javascript
preload() {
  this.load.audio('bgm', ['assets/audio/bgm.ogg', 'assets/audio/bgm.mp3']);
  this.load.audio('jump', 'assets/audio/jump.wav');
  this.load.audioSprite('sfx', 'assets/audio/sfx.json', [
    'assets/audio/sfx.ogg', 'assets/audio/sfx.mp3'
  ]);
}
```

## Playing Sounds

```javascript
// Simple play
this.sound.play('jump');

// With config
this.sound.play('jump', { volume: 0.5, rate: 1.2 });

// Stored reference
const bgm = this.sound.add('bgm', { loop: true, volume: 0.3 });
bgm.play();
bgm.pause();
bgm.resume();
bgm.stop();

// Audio sprites
this.sound.playAudioSprite('sfx', 'explosion');
```

## Sound Manager

```javascript
this.sound.setVolume(0.5);     // master volume
this.sound.setMute(true);
this.sound.pauseAll();
this.sound.resumeAll();
this.sound.stopAll();

// Check if Web Audio is available
if (this.sound.locked) {
  // Audio context locked — need user interaction
  this.sound.once('unlocked', () => { bgm.play(); });
}
```

## Markers (regions within a track)

```javascript
const music = this.sound.add('soundtrack');
music.addMarker({ name: 'intro', start: 0, duration: 10 });
music.addMarker({ name: 'loop', start: 10, duration: 60 });
music.play('intro');
music.once('complete', () => music.play('loop', { loop: true }));
```

## Gotchas

- Browsers require user interaction before playing audio — Phaser handles this with `sound.locked` / `sound.once('unlocked')`
- Provide multiple formats (OGG + MP3) for cross-browser support — Phaser picks the best one
- `this.sound` is shared across scenes — stopping a scene doesn't stop its sounds unless you explicitly `stopAll()`
- Audio sprites (multiple SFX in one file) reduce HTTP requests — good for mobile
- Web Audio API has a limit on simultaneous sounds — pool/reuse for rapid-fire SFX
