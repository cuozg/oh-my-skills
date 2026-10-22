using UnityEngine;

namespace Rig2D
{
    /// <summary>
    /// Smooth 2D tracking camera with velocity-based look-ahead.
    ///
    /// SETUP: add to the Main Camera (orthographic), assign <see cref="target"/> (the character root).
    /// The camera keeps its own Z so it never clips into the 2D plane.
    /// </summary>
    [DisallowMultipleComponent]
    public class CameraFollow2D : MonoBehaviour
    {
        [Tooltip("Transform to follow (character root).")]
        [SerializeField] Transform target;
        [Tooltip("World offset from the target (keeps the character slightly below centre).")]
        [SerializeField] Vector2 offset = new(0f, 1f);
        [Tooltip("SmoothDamp time; lower = snappier.")]
        [SerializeField] float smoothTime = 0.2f;
        [Tooltip("How far ahead (units) the camera leads in the movement direction.")]
        [SerializeField] float lookAhead = 1.0f;
        [Tooltip("Clamp the camera so it never goes below minY.")]
        [SerializeField] bool clampY;
        [SerializeField] float minY = 0f;

        Rigidbody2D targetBody;
        Vector3 velocity;
        float currentLookAhead;
        float lookAheadVelocity;

        /// <summary>Assign a new follow target at runtime.</summary>
        public void SetTarget(Transform newTarget)
        {
            target = newTarget;
            targetBody = target != null ? target.GetComponent<Rigidbody2D>() : null;
        }

        void Start()
        {
            SetTarget(target);
            // Snap on start so the first frame doesn't swoop in from the scene origin.
            if (target != null) transform.position = Desired(0f);
        }

        void LateUpdate()
        {
            if (target == null) return;

            // Lead toward the movement direction; smoothed separately so turning around doesn't jerk.
            float dir = 0f;
            if (targetBody != null && Mathf.Abs(targetBody.linearVelocity.x) > 0.1f)
                dir = Mathf.Sign(targetBody.linearVelocity.x);
            currentLookAhead = Mathf.SmoothDamp(currentLookAhead, dir * lookAhead, ref lookAheadVelocity, 0.5f);

            transform.position = Vector3.SmoothDamp(transform.position, Desired(currentLookAhead), ref velocity, smoothTime);
        }

        Vector3 Desired(float ahead)
        {
            Vector3 p = target.position;
            float y = p.y + offset.y;
            if (clampY) y = Mathf.Max(y, minY);
            return new Vector3(p.x + offset.x + ahead, y, transform.position.z);
        }
    }
}
