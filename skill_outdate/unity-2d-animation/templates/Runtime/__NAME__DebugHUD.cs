using System.Linq;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;

namespace __NAME__
{
    /// <summary>
    /// IMGUI test overlay for the __NAME__ subject (no Canvas/EventSystem needed): live Animator state + parameters,
    /// and one button per clip that previews it in place, bypassing the state machine.
    ///
    /// Preview plays the clip through a PlayableGraph on the same Animator (the graph output overrides the
    /// controller while it lives) and pauses the Rigidbody2D, so the subject stays put. "Live" destroys the
    /// graph and hands control back to the Animator Controller + input.
    /// Automation (verify step, via `unity command eval`): FindFirstObjectByType&lt;__NAME__DebugHUD&gt;() then
    /// Preview(clip) / PoseAt(clip, normalizedTime) / Live() / KeyBackground(true|false).
    /// </summary>
    public class __NAME__DebugHUD : MonoBehaviour
    {
        const float ReferenceHeight = 720f;   // GUI authored at 720p, scaled to the screen

        [SerializeField] Animator animator;

        Rigidbody2D body;
        PlayableGraph graph;
        AnimationClipPlayable playable;
        string previewClip;
        string[] clipNames = new string[0];
        GUIStyle titleStyle;
        Color savedBackground;
        Vector3 savedCamPos;
        float savedCamSize;
        bool keyed;
        Renderer[] hiddenOthers = new Renderer[0];

        /// <summary>Names of every clip on the Animator Controller.</summary>
        public string[] ClipNames => clipNames;
        /// <summary>Clip being previewed, or null when live.</summary>
        public string PreviewClip => previewClip;

        void Awake()
        {
            // Test scene only: keep Play mode ticking while the Editor is in the background, so CLI-driven
            // captures and state checks work without stealing focus (an unfocused Editor otherwise freezes
            // frames, and SpriteSkin stops re-deforming).
            Application.runInBackground = true;
            if (animator == null) animator = FindFirstObjectByType<Animator>();
            if (animator == null || animator.runtimeAnimatorController == null) return;
            Transform root = animator.transform.parent != null ? animator.transform.parent : animator.transform;
            body = root.GetComponent<Rigidbody2D>();
            clipNames = animator.runtimeAnimatorController.animationClips.Select(c => c.name).Distinct().ToArray();
        }

        void OnDestroy() => DestroyGraph();

        /// <summary>Plays <paramref name="clip"/> in place from the start (loops if the clip loops).</summary>
        public void Preview(string clip)
        {
            AnimationClip c = animator.runtimeAnimatorController.animationClips.FirstOrDefault(x => x.name == clip);
            if (c == null) { Debug.LogError($"[__NAME__DebugHUD] No clip '{clip}'"); return; }
            DestroyGraph();
            playable = AnimationPlayableUtilities.PlayClip(animator, c, out graph);
            previewClip = clip;
            if (body != null) { body.linearVelocity = Vector2.zero; body.simulated = false; }
        }

        /// <summary>Freezes <paramref name="clip"/> at <paramref name="normalizedTime"/> (0..1) for captures.</summary>
        public void PoseAt(string clip, float normalizedTime)
        {
            if (previewClip != clip || !graph.IsValid()) Preview(clip);
            playable.SetTime(normalizedTime * playable.GetAnimationClip().length);
            playable.SetSpeed(0);
            graph.Evaluate();
        }

        /// <summary>Back to the Animator Controller + physics/input.</summary>
        public void Live()
        {
            DestroyGraph();
            previewClip = null;
            if (body != null) body.simulated = true;
        }

        /// <summary>
        /// Solid magenta background, Environment and every other subject's renderers hidden, and the camera zoomed
        /// onto the subject (more pixels per joint), so check_frames.py can find see-through gaps and unoutlined
        /// edges. The framing is fixed on the first call (repeat calls keep it), so every sample of a session shares
        /// one camera and frames stay comparable pixel for pixel. Pass false to restore.
        /// </summary>
        public void KeyBackground(bool on)
        {
            Camera cam = Camera.main;
            CameraFollow2D follow = cam.GetComponent<CameraFollow2D>();
            if (on && !keyed)
            {
                savedBackground = cam.backgroundColor;
                savedCamPos = cam.transform.position;
                savedCamSize = cam.orthographicSize;
            }
            if (follow != null) follow.enabled = !on;   // keep the zoomed framing still while capturing
            if (on && !keyed)
            {
                // Frame the subject's renderers with 25% margin (poses that reach out stay in view). Done once per
                // key session: re-framing per pose would recentre the camera and shift static parts between frames.
                Renderer[] rs = animator.GetComponentsInChildren<Renderer>();
                Bounds b = rs[0].bounds;
                foreach (Renderer r in rs) b.Encapsulate(r.bounds);
                cam.transform.position = new Vector3(b.center.x, b.center.y, cam.transform.position.z);
                cam.orthographicSize = Mathf.Max(b.extents.y, b.extents.x / cam.aspect) * 1.25f;
            }
            else if (!on && keyed)
            {
                cam.transform.position = savedCamPos;
                cam.orthographicSize = savedCamSize;
            }
            cam.backgroundColor = on ? Color.magenta : (keyed ? savedBackground : cam.backgroundColor);
            GameObject env = GameObject.Find("Environment");
            if (env != null) foreach (Renderer r in env.GetComponentsInChildren<Renderer>()) r.enabled = !on;
            // Other subjects dropped into the test scene would land in the captures: hide them while keyed.
            if (on && !keyed)
            {
                Transform self = animator.transform.root;
                hiddenOthers = FindObjectsByType<Renderer>(FindObjectsSortMode.None)
                    .Where(r => r.enabled && r.transform.root != self && (env == null || !r.transform.IsChildOf(env.transform)))
                    .ToArray();
                foreach (Renderer r in hiddenOthers) r.enabled = false;
            }
            else if (!on && keyed)
            {
                foreach (Renderer r in hiddenOthers) if (r != null) r.enabled = true;
                hiddenOthers = new Renderer[0];
            }
            keyed = on;
        }

        void DestroyGraph()
        {
            if (graph.IsValid()) graph.Destroy();
        }

        void OnGUI()
        {
            if (animator == null) return;
            float scale = Screen.height / ReferenceHeight;
            GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1f));
            titleStyle ??= new GUIStyle(GUI.skin.label) { fontStyle = FontStyle.Bold, fontSize = 15 };

            GUILayout.BeginArea(new Rect(10f, 10f, 360f, 400f), GUI.skin.box);
            GUILayout.Label("__NAME__ Animation Test", titleStyle);
            if (body != null) GUILayout.Label("A/D or ←/→ move · Left Shift run · Space jump");
            GUILayout.Label(previewClip != null ? $"Preview: {previewClip} (in place)" : $"Live · State: {CurrentStateName()}");
            foreach (AnimatorControllerParameter p in animator.parameters)
                GUILayout.Label($"  {p.name}: {ParamValue(p)}");

            if (GUILayout.Button("Live (state machine + input)")) Live();
            for (int i = 0; i < clipNames.Length; i += 4)
            {
                GUILayout.BeginHorizontal();
                for (int j = i; j < Mathf.Min(i + 4, clipNames.Length); j++)
                    if (GUILayout.Button(clipNames[j])) Preview(clipNames[j]);
                GUILayout.EndHorizontal();
            }
            GUILayout.EndArea();
        }

        string CurrentStateName()
        {
            if (animator.runtimeAnimatorController == null) return "-";
            int hash = animator.GetCurrentAnimatorStateInfo(0).shortNameHash;
            return clipNames.FirstOrDefault(n => Animator.StringToHash(n) == hash) ?? "?";   // states are named like clips
        }

        string ParamValue(AnimatorControllerParameter p) => p.type switch
        {
            AnimatorControllerParameterType.Float => animator.GetFloat(p.nameHash).ToString("F2"),
            AnimatorControllerParameterType.Int => animator.GetInteger(p.nameHash).ToString(),
            AnimatorControllerParameterType.Bool => animator.GetBool(p.nameHash).ToString(),
            _ => "trigger",
        };
    }
}
