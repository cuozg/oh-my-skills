using UnityEngine;
using UnityEngine.InputSystem;

namespace Rig2D
{
    /// <summary>
    /// Side-scrolling movement for the rigged 2D character.
    /// Reads horizontal input + run modifier (New Input System), moves the Rigidbody2D, flips the visual
    /// to face the movement direction and feeds the current speed into the Animator "Speed" parameter.
    ///
    /// SETUP
    /// 1. Root GameObject: Rigidbody2D (Freeze Rotation Z), CapsuleCollider2D, this component.
    /// 2. Child "Visual": Animator (<Name>.controller) + bones + skinned sprites. Only this child is flipped,
    ///    so physics (collider/rigidbody) on the root never gets a negative scale.
    /// 3. Controls: A/D or Left/Right arrows (gamepad left stick / d-pad) to walk, hold Left Shift to run.
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    [DisallowMultipleComponent]
    public class Character2DController : MonoBehaviour
    {
        // Cached hash: avoids string lookups on the Animator every frame.
        static readonly int SpeedHash = Animator.StringToHash("Speed");

        [Header("Movement")]
        [Tooltip("Walk speed (units/s). Must stay between the Animator thresholds 0.1 (Idle<->Walk) and 3.0 (Walk<->Run).")]
        [SerializeField] float walkSpeed = 2f;
        [Tooltip("Run speed (units/s). Must be above the Animator Walk<->Run threshold of 3.0.")]
        [SerializeField] float runSpeed = 5f;
        [Tooltip("How fast horizontal speed ramps up toward the target (units/s²).")]
        [SerializeField] float acceleration = 20f;
        [Tooltip("How fast horizontal speed ramps down when input is released or reversed (units/s²).")]
        [SerializeField] float deceleration = 25f;

        [Header("References")]
        [Tooltip("Animator driving Idle/Walk/Run. Auto-found in children when empty.")]
        [SerializeField] Animator animator;
        [Tooltip("Child holding bones + sprites; its X scale is flipped to turn around. Auto = first child.")]
        [SerializeField] Transform visual;
        [Tooltip("True when the source art faces right at scale +1.")]
        [SerializeField] bool artFacesRight = true;

        Rigidbody2D body;
        InputAction moveAction;
        InputAction runAction;
        float targetSpeedX;
        float? previewSpeed;

        /// <summary>Configured walk speed (units/s).</summary>
        public float WalkSpeed => walkSpeed;
        /// <summary>Configured run speed (units/s).</summary>
        public float RunSpeed => runSpeed;
        /// <summary>The value last sent to the Animator "Speed" parameter.</summary>
        public float CurrentSpeed { get; private set; }
        /// <summary>True while a debug preview speed overrides player input.</summary>
        public bool IsPreviewing => previewSpeed.HasValue;
        /// <summary>The active preview speed, or null when driven by input.</summary>
        public float? PreviewSpeed => previewSpeed;

        void Awake()
        {
            body = GetComponent<Rigidbody2D>();
            // Defensive physics config: an upright character must never tip over or tunnel through ground.
            body.freezeRotation = true;
            body.interpolation = RigidbodyInterpolation2D.Interpolate;
            body.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

            if (animator == null) animator = GetComponentInChildren<Animator>();
            if (visual == null && transform.childCount > 0) visual = transform.GetChild(0);

            // Actions are built in code so the controller is self-contained (no .inputactions asset needed).
            moveAction = new InputAction("Move", InputActionType.Value, expectedControlType: "Axis");
            moveAction.AddCompositeBinding("1DAxis")
                .With("Negative", "<Keyboard>/a").With("Positive", "<Keyboard>/d");
            moveAction.AddCompositeBinding("1DAxis")
                .With("Negative", "<Keyboard>/leftArrow").With("Positive", "<Keyboard>/rightArrow");
            moveAction.AddCompositeBinding("1DAxis")
                .With("Negative", "<Gamepad>/dpad/left").With("Positive", "<Gamepad>/dpad/right");
            moveAction.AddBinding("<Gamepad>/leftStick/x");

            runAction = new InputAction("Run", InputActionType.Button);
            runAction.AddBinding("<Keyboard>/leftShift");
            runAction.AddBinding("<Gamepad>/leftStickPress");
        }

        void OnEnable()
        {
            moveAction.Enable();
            runAction.Enable();
        }

        void OnDisable()
        {
            moveAction.Disable();
            runAction.Disable();
        }

        void OnDestroy()
        {
            moveAction.Dispose();
            runAction.Dispose();
        }

        void Update()
        {
            if (previewSpeed.HasValue)
            {
                // Treadmill preview: stand still and force the Animator speed so each clip can be inspected.
                targetSpeedX = 0f;
                CurrentSpeed = previewSpeed.Value;
            }
            else
            {
                float input = moveAction.ReadValue<float>();
                bool running = runAction.IsPressed();
                targetSpeedX = input * (running ? runSpeed : walkSpeed);

                // Only turn on real input so releasing the key keeps the last facing direction.
                if (Mathf.Abs(input) > 0.01f) Face(input > 0f);

                // Use the actual body velocity (not the input) so the anim matches what you see,
                // e.g. walking into a wall reads as Idle.
                CurrentSpeed = Mathf.Abs(body.linearVelocity.x);
            }

            if (animator != null) animator.SetFloat(SpeedHash, CurrentSpeed);
        }

        void FixedUpdate()
        {
            Vector2 v = body.linearVelocity;
            // Accelerate when speeding up in the same direction, decelerate when stopping or reversing.
            bool speedingUp = Mathf.Abs(targetSpeedX) > Mathf.Abs(v.x) && Mathf.Sign(targetSpeedX) == Mathf.Sign(v.x);
            float rate = (speedingUp || Mathf.Approximately(v.x, 0f)) ? acceleration : deceleration;
            v.x = Mathf.MoveTowards(v.x, targetSpeedX, rate * Time.fixedDeltaTime);
            body.linearVelocity = v;   // y untouched -> gravity still applies
        }

        /// <summary>
        /// Override input with a fixed Animator speed (character stays in place). Pass null to return to input.
        /// </summary>
        public void SetPreviewSpeed(float? speed)
        {
            previewSpeed = speed;
        }

        /// <summary>Flips the visual child so the art faces the given direction.</summary>
        void Face(bool right)
        {
            if (visual == null) return;
            Vector3 s = visual.localScale;
            float sign = (right == artFacesRight) ? 1f : -1f;
            s.x = Mathf.Abs(s.x) * sign;
            visual.localScale = s;
        }
    }
}
