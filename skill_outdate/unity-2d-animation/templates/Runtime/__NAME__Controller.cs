using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

namespace __NAME__
{
    /// <summary>
    /// Side-scrolling movement for the rigged __NAME__ (characters only; object subjects don't get this file).
    /// Moves the Rigidbody2D from input (New Input System), flips the Visual child to face the movement direction,
    /// checks ground contact, and feeds the Animator.
    ///
    /// Animator parameters written (each only if the controller defines it, so unused ones cost nothing):
    ///   Speed (float, |vx|) · IsGrounded (bool) · VelocityY (float) · Jump (trigger, on take-off)
    /// Controls: A/D or ←/→ (gamepad stick / d-pad) move · hold Left Shift run · Space (gamepad South) jump.
    /// SETUP: root = Rigidbody2D (Freeze Rotation Z) + collider + this; child "Visual" = Animator + bones + parts.
    /// Only Visual is flipped, so physics on the root never gets a negative scale.
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    [DisallowMultipleComponent]
    public class __NAME__Controller : MonoBehaviour
    {
        static readonly int SpeedHash = Animator.StringToHash("Speed");
        static readonly int GroundedHash = Animator.StringToHash("IsGrounded");
        static readonly int VelocityYHash = Animator.StringToHash("VelocityY");
        static readonly int JumpHash = Animator.StringToHash("Jump");

        [Header("Movement")]
        [Tooltip("Walk speed (units/s). Keep it between the Animator's walk and run thresholds.")]
        [SerializeField] float walkSpeed = 2f;
        [Tooltip("Run speed (units/s). Keep it above the Animator's run threshold.")]
        [SerializeField] float runSpeed = 5f;
        [Tooltip("How fast horizontal speed ramps up toward the target (units/s²).")]
        [SerializeField] float acceleration = 20f;
        [Tooltip("How fast horizontal speed ramps down when input is released or reversed (units/s²).")]
        [SerializeField] float deceleration = 25f;

        [Header("Jump")]
        [Tooltip("Upward launch speed (units/s); 0 disables jumping. Height ≈ v² / (2·9.81·gravityScale).")]
        [SerializeField] float jumpSpeed = 9f;
        [Tooltip("Contacts whose normal.y is above this count as ground (0.5 ≈ slopes up to 60°; walls ignored).")]
        [SerializeField] float groundNormalMinY = 0.5f;
        [Tooltip("Seconds after take-off during which stale ground contacts are ignored.")]
        [SerializeField] float jumpGroundIgnore = 0.1f;

        [Header("References")]
        [Tooltip("Auto-found in children when empty.")]
        [SerializeField] Animator animator;
        [Tooltip("Child holding bones + sprites; its X scale is flipped to turn around. Auto = first child.")]
        [SerializeField] Transform visual;
        [Tooltip("True when the source art faces right at scale +1.")]
        [SerializeField] bool artFacesRight = true;

        Rigidbody2D body;
        InputAction moveAction, runAction, jumpAction;
        readonly ContactPoint2D[] contacts = new ContactPoint2D[8];
        readonly HashSet<int> animParams = new();
        float targetSpeedX;
        bool jumpRequested;
        float groundIgnoreUntil;

        /// <summary>Configured walk speed (units/s).</summary>
        public float WalkSpeed => walkSpeed;
        /// <summary>Configured run speed (units/s).</summary>
        public float RunSpeed => runSpeed;
        /// <summary>The value last sent to the Animator "Speed" parameter.</summary>
        public float CurrentSpeed { get; private set; }
        /// <summary>True while standing on ground (updated every physics step).</summary>
        public bool IsGrounded { get; private set; } = true;

        void Awake()
        {
            body = GetComponent<Rigidbody2D>();
            body.freezeRotation = true;
            body.interpolation = RigidbodyInterpolation2D.Interpolate;
            body.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

            if (animator == null) animator = GetComponentInChildren<Animator>();
            if (visual == null && transform.childCount > 0) visual = transform.GetChild(0);
            if (animator != null)
                foreach (AnimatorControllerParameter p in animator.parameters) animParams.Add(p.nameHash);

            // Actions built in code so the controller is self-contained (no .inputactions asset needed).
            moveAction = new InputAction("Move", InputActionType.Value, expectedControlType: "Axis");
            moveAction.AddCompositeBinding("1DAxis").With("Negative", "<Keyboard>/a").With("Positive", "<Keyboard>/d");
            moveAction.AddCompositeBinding("1DAxis").With("Negative", "<Keyboard>/leftArrow").With("Positive", "<Keyboard>/rightArrow");
            moveAction.AddCompositeBinding("1DAxis").With("Negative", "<Gamepad>/dpad/left").With("Positive", "<Gamepad>/dpad/right");
            moveAction.AddBinding("<Gamepad>/leftStick/x");
            runAction = new InputAction("Run", InputActionType.Button);
            runAction.AddBinding("<Keyboard>/leftShift");
            runAction.AddBinding("<Gamepad>/leftStickPress");
            jumpAction = new InputAction("Jump", InputActionType.Button);
            jumpAction.AddBinding("<Keyboard>/space");
            jumpAction.AddBinding("<Gamepad>/buttonSouth");
        }

        void OnEnable() { moveAction.Enable(); runAction.Enable(); jumpAction.Enable(); }
        void OnDisable() { moveAction.Disable(); runAction.Disable(); jumpAction.Disable(); }
        void OnDestroy() { moveAction.Dispose(); runAction.Dispose(); jumpAction.Dispose(); }

        void Update()
        {
            float input = moveAction.ReadValue<float>();
            targetSpeedX = input * (runAction.IsPressed() ? runSpeed : walkSpeed);
            // Only turn on real input so releasing the key keeps the last facing direction.
            if (Mathf.Abs(input) > 0.01f) Face(input > 0f);
            if (jumpAction.WasPressedThisFrame()) Jump();

            // Actual body velocity (not input) so walking into a wall reads as idle.
            CurrentSpeed = Mathf.Abs(body.linearVelocity.x);
            if (animator == null) return;
            if (animParams.Contains(SpeedHash)) animator.SetFloat(SpeedHash, CurrentSpeed);
            if (animParams.Contains(GroundedHash)) animator.SetBool(GroundedHash, IsGrounded);
            if (animParams.Contains(VelocityYHash)) animator.SetFloat(VelocityYHash, body.linearVelocity.y);
        }

        void FixedUpdate()
        {
            IsGrounded = CheckGrounded();
            Vector2 v = body.linearVelocity;
            // Accelerate when speeding up in the same direction, decelerate when stopping or reversing.
            bool speedingUp = Mathf.Abs(targetSpeedX) > Mathf.Abs(v.x) && Mathf.Sign(targetSpeedX) == Mathf.Sign(v.x);
            float rate = (speedingUp || Mathf.Approximately(v.x, 0f)) ? acceleration : deceleration;
            v.x = Mathf.MoveTowards(v.x, targetSpeedX, rate * Time.fixedDeltaTime);

            // Jump applied here (not in Update) so the physics step can't overwrite the launch velocity.
            if (jumpRequested)
            {
                jumpRequested = false;
                if (IsGrounded && jumpSpeed > 0f)
                {
                    v.y = jumpSpeed;
                    IsGrounded = false;
                    groundIgnoreUntil = Time.time + jumpGroundIgnore;
                    if (animator != null && animParams.Contains(JumpHash)) animator.SetTrigger(JumpHash);
                }
            }
            body.linearVelocity = v;
        }

        /// <summary>Request a jump on the next physics step (ignored while airborne).</summary>
        public void Jump() => jumpRequested = true;

        /// <summary>Grounded = touching a collider with an upward contact normal (ignored briefly after take-off).</summary>
        bool CheckGrounded()
        {
            if (Time.time < groundIgnoreUntil) return false;
            int n = body.GetContacts(contacts);
            for (int i = 0; i < n; i++)
                if (contacts[i].normal.y > groundNormalMinY) return true;
            return false;
        }

        /// <summary>Flips the visual child so the art faces the given direction.</summary>
        void Face(bool right)
        {
            if (visual == null) return;
            Vector3 s = visual.localScale;
            s.x = Mathf.Abs(s.x) * ((right == artFacesRight) ? 1f : -1f);
            visual.localScale = s;
        }
    }
}
