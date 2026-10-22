using UnityEngine;

namespace Rig2D
{
    /// <summary>
    /// IMGUI overlay for testing the character animations in Play mode (no Canvas/EventSystem needed).
    /// Shows controls, live Speed and Animator state, plus buttons to preview Idle/Walk/Run in place.
    ///
    /// SETUP: drop on any GameObject in the test scene; references auto-resolve when left empty.
    /// </summary>
    public class AnimationDebugHUD : MonoBehaviour
    {
        const float ReferenceHeight = 720f;   // GUI is authored at 720p and scaled to the screen

        [SerializeField] Character2DController controller;
        [SerializeField] Animator animator;

        GUIStyle titleStyle;

        void Awake()
        {
            if (controller == null) controller = FindFirstObjectByType<Character2DController>();
            if (animator == null && controller != null) animator = controller.GetComponentInChildren<Animator>();
        }

        void OnGUI()
        {
            if (controller == null) return;

            // Uniform scale keeps the HUD readable on HiDPI / large Game views.
            float scale = Screen.height / ReferenceHeight;
            GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1f));
            titleStyle ??= new GUIStyle(GUI.skin.label) { fontStyle = FontStyle.Bold, fontSize = 15 };

            GUILayout.BeginArea(new Rect(10f, 10f, 290f, 210f), GUI.skin.box);
            GUILayout.Label("2D Animation Test", titleStyle);
            GUILayout.Label("A/D or ←/→ : Walk");
            GUILayout.Label("Hold Left Shift : Run");
            GUILayout.Label($"Speed: {controller.CurrentSpeed:F2}    State: {CurrentStateName()}");
            GUILayout.Label($"Mode: {(controller.IsPreviewing ? "Preview (in place)" : "Input")}");

            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Input")) controller.SetPreviewSpeed(null);
            if (GUILayout.Button("Idle")) controller.SetPreviewSpeed(0f);
            if (GUILayout.Button("Walk")) controller.SetPreviewSpeed(controller.WalkSpeed);
            if (GUILayout.Button("Run")) controller.SetPreviewSpeed(controller.RunSpeed);
            GUILayout.EndHorizontal();
            GUILayout.EndArea();
        }

        string CurrentStateName()
        {
            if (animator == null || animator.runtimeAnimatorController == null) return "-";
            AnimatorStateInfo info = animator.GetCurrentAnimatorStateInfo(0);
            if (info.IsName("Idle")) return "Idle";
            if (info.IsName("Walk")) return "Walk";
            if (info.IsName("Run")) return "Run";
            return "?";
        }
    }
}
