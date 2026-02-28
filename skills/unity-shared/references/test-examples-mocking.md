# Test Patterns: Mocking & Parameterization

## Pattern: Mocking Dependencies

```csharp
// Interface-based mock with tracking
public class MockAudioService : IAudioService
{
    public int PlayCount { get; private set; }
    public string LastClipPlayed { get; private set; }
    public bool ShouldThrow { get; set; }

    public void PlaySFX(string clipId, float volume = 1f)
    {
        if (ShouldThrow) throw new InvalidOperationException("Audio unavailable");
        PlayCount++;
        LastClipPlayed = clipId;
    }
    public void StopAll() { PlayCount = 0; }
}

// Usage with MonoBehaviour
[TestFixture]
public class PlayerControllerTests
{
    private GameObject _playerGo;
    private PlayerController _controller;
    private MockAudioService _mockAudio;

    [SetUp]
    public void SetUp()
    {
        _playerGo = new GameObject("TestPlayer");
        _controller = _playerGo.AddComponent<PlayerController>();
        _mockAudio = new MockAudioService();
        _controller.Initialize(_mockAudio);
    }

    [TearDown] public void TearDown() => Object.Destroy(_playerGo);

    [Test]
    public void TakeDamage_PlaysDamageSound()
    {
        _controller.TakeDamage(10);
        Assert.AreEqual("sfx_damage", _mockAudio.LastClipPlayed);
    }

    [Test]
    public void TakeDamage_AudioUnavailable_DoesNotThrow()
    {
        _mockAudio.ShouldThrow = true;
        Assert.DoesNotThrow(() => _controller.TakeDamage(10));
    }
}
```

## Pattern: Parameterized Tests

```csharp
[TestFixture]
public class DamageCalculatorTests
{
    // TestCase: inline values
    [TestCase(100, 30, 70)]
    [TestCase(100, 0, 100)]
    [TestCase(100, 100, 0)]
    [TestCase(100, 150, 0)]   // overkill clamps
    [TestCase(0, 10, 0)]      // already dead
    public void CalculateFinalHealth_ReturnsExpected(int maxHp, int damage, int expected)
    {
        Assert.AreEqual(expected, DamageCalculator.CalculateFinalHealth(maxHp, damage));
    }

    // TestCaseSource: complex data
    private static IEnumerable<TestCaseData> ElementalDamageData()
    {
        yield return new TestCaseData(Element.Fire, Element.Ice, 2.0f).SetName("Fire vs Ice = 2x");
        yield return new TestCaseData(Element.Fire, Element.Fire, 0.5f).SetName("Fire vs Fire = 0.5x");
        yield return new TestCaseData(Element.Fire, Element.Earth, 1.0f).SetName("Fire vs Earth = 1x");
    }

    [TestCaseSource(nameof(ElementalDamageData))]
    public void GetElementalMultiplier_ReturnsCorrect(Element atk, Element def, float expected)
    {
        Assert.AreEqual(expected, DamageCalculator.GetElementalMultiplier(atk, def), 0.001f);
    }
}
```
