
### 2D Platformer Controller

```csharp
[RequireComponent(typeof(Rigidbody2D))]
[RequireComponent(typeof(CapsuleCollider2D))]
public class PlatformerController2D : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float _moveSpeed = 8f;
    [SerializeField] private float _acceleration = 60f;
    [SerializeField] private float _deceleration = 40f;

    [Header("Jump")]
    [SerializeField] private float _jumpForce = 14f;
    [SerializeField] private float _fallMultiplier = 2.5f;
    [SerializeField] private float _lowJumpMultiplier = 2f;
    [SerializeField] private float _coyoteTime = 0.1f;
    [SerializeField] private float _jumpBufferTime = 0.1f;

    [Header("Ground Check")]
    [SerializeField] private Transform _groundCheck;
    [SerializeField] private float _groundCheckRadius = 0.15f;
    [SerializeField] private LayerMask _groundLayer;

    private Rigidbody2D _rb;
    private float _moveInput;
    private bool _isGrounded;
    private float _lastGroundedTime;
    private float _lastJumpPressedTime;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody2D>();
        _rb.freezeRotation = true;
        _rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
    }

    private void Update()
    {
        _moveInput = Input.GetAxisRaw("Horizontal");
        if (Input.GetButtonDown("Jump"))
            _lastJumpPressedTime = _jumpBufferTime;
        _lastJumpPressedTime -= Time.deltaTime;
        _lastGroundedTime -= Time.deltaTime;
    }

    private void FixedUpdate()
    {
        _isGrounded = Physics2D.OverlapCircle(
            _groundCheck.position, _groundCheckRadius, _groundLayer);
        if (_isGrounded) _lastGroundedTime = _coyoteTime;
        ApplyMovement();
        ApplyJump();
        ApplyBetterJumpGravity();
    }

    private void ApplyMovement()
    {
        float targetSpeed = _moveInput * _moveSpeed;
        float speedDiff = targetSpeed - _rb.linearVelocity.x;
        float accelRate = Mathf.Abs(targetSpeed) > 0.01f ? _acceleration : _deceleration;
        _rb.AddForce(Vector2.right * speedDiff * accelRate);
    }

    private void ApplyJump()
    {
        if (_lastJumpPressedTime > 0 && _lastGroundedTime > 0)
        {
            _rb.linearVelocity = new Vector2(_rb.linearVelocity.x, _jumpForce);
            _lastJumpPressedTime = 0;
            _lastGroundedTime = 0;
        }
    }

    private void ApplyBetterJumpGravity()
    {
        if (_rb.linearVelocity.y < 0)
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_fallMultiplier - 1) * Time.fixedDeltaTime);
        else if (_rb.linearVelocity.y > 0 && !Input.GetButton("Jump"))
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_lowJumpMultiplier - 1) * Time.fixedDeltaTime);
    }
}
```
