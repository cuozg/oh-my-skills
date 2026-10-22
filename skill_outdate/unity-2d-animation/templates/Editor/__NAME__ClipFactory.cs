using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;
using Pose = __NAME__.EditorTools.__NAME__RigBuilder.Pose;

namespace __NAME__.EditorTools
{
    /// <summary>
    /// Procedural clips + Animator wiring for the __NAME__ subject.
    ///
    /// EDIT HERE: <see cref="Specs"/> lists the clips (name, length, loop, motion) and <see cref="Wire"/> adds the
    /// parameters/transitions. Recipes per animation type: unity-2d-animation skill, references/animation.md.
    ///
    /// Engine (generic, rarely edited): every bone of the rig is keyed in every clip — rotation z = rest angle +
    /// Motion.rot offset, position = rest + Motion.pos offset, scale = Motion.scale multiplier (default 1) —
    /// sampled at KeysPerCycle+1 keys with clamped-auto tangents, so clips stay editable in the Animation window
    /// and no pose leaks between states. Bones without a motion are keyed at rest.
    /// </summary>
    internal static class __NAME__ClipFactory
    {
        const float Tau = Mathf.PI * 2f;
        const int KeysPerCycle = 24;

        /// <summary>Per-bone offsets as functions of normalized clip time s = 0..1.</summary>
        internal class Motion
        {
            public readonly Dictionary<string, Func<float, float>> rot = new();     // degrees, + = CCW
            public readonly Dictionary<string, Func<float, Vector2>> pos = new();   // units, parent space
            public readonly Dictionary<string, Func<float, Vector2>> scale = new(); // multiplier, 1 = rest
        }

        internal struct Spec
        {
            public string name; public float length; public bool loop; public Motion motion;
            public Spec(string name, float length, bool loop, Motion motion)
            { this.name = name; this.length = length; this.loop = loop; this.motion = motion; }
        }

        // ============================================ EDIT: clips ============================================

        /// <summary>Clips to bake, in order. The first one is the Animator entry state.</summary>
        static IEnumerable<Spec> Specs()
        {
            // Rest pose: proves the rig binds before any motion exists. Replace/extend with real clips.
            yield return new Spec("Rest", 1f, true, new Motion());
        }

        /// <summary>
        /// Subject-specific parameters + transitions. <paramref name="states"/> = one state per clip, keyed by
        /// clip name. Default: no transitions (the HUD previews each clip directly).
        /// </summary>
        internal static void Wire(AnimatorController ctrl, Dictionary<string, AnimatorState> states)
        {
        }

        // ======================================== motion helpers =============================================

        /// <summary>Sine of the cycle: amp · sin(2π(s·freq + phase)).</summary>
        static float Wave(float s, float amp, float phase = 0f, float freq = 1f) => amp * Mathf.Sin(Tau * (s * freq + phase));

        /// <summary>Swing-phase bump: 0 while the limb moves back (stance), smooth 0..1..0 while it moves forward.</summary>
        static float Lift(float s, float phase = 0f)
        {
            float c = Mathf.Cos(Tau * (s + phase));
            return c > 0f ? Mathf.Pow(c, 1.5f) : 0f;
        }

        /// <summary>Ease-in 0 -> 1 reached at s = <paramref name="end"/>, then held (one-shot pose blends).</summary>
        static float Ease(float s, float end = 1f) => Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(s / end));

        /// <summary>One-shot 0..1..0 bump starting at <paramref name="delay"/>; peaks early when skew &lt; 1; ends at 0 at s=1.</summary>
        static float Bump(float s, float delay = 0f, float skew = 0.6f)
            => Mathf.Sin(Mathf.PI * Mathf.Pow(Mathf.Clamp01((s - delay) / (1f - delay)), skew));

        /// <summary>
        /// Three-bone limb cycle (upper/lower/end, e.g. Thigh/Shin/Foot): upper swings ±upper°, lower + end fold
        /// back during the swing so the foot clears the ground. Negative fold = back for a limb pointing down
        /// on a subject facing right.
        /// </summary>
        static void Limb(Motion m, string upper, string lower, string end, float phase, float swing, float fold, float endFold)
        {
            m.rot[upper] = s => Wave(s, swing, phase);
            if (lower != null) m.rot[lower] = s => -fold * Lift(s, phase);
            if (end != null) m.rot[end] = s => -endFold * Lift(s, phase);
        }

        /// <summary>Follow-through chain (tail, hair, cloth, antenna): each segment swings more and later.</summary>
        static void Chain(Motion m, string[] bones, float baseAmp, float ampGrowth, float lag, float offset = 0f, float freq = 1f)
        {
            for (int i = 0; i < bones.Length; i++)
            {
                float amp = baseAmp + ampGrowth * i, delay = lag * i;
                m.rot[bones[i]] = s => offset + amp * Mathf.Sin(Tau * s * freq - delay);
            }
        }

        /// <summary>Static pose offsets scaled by an envelope w(s) (e.g. Ease for one-shots, Bump for impacts).</summary>
        static void Hold(Motion m, Func<float, float> w, params (string bone, float deg)[] pose)
        {
            foreach (var (bone, deg) in pose) m.rot[bone] = s => deg * w(s);
        }

        // ============================================== engine ===============================================

        /// <summary>Bakes every <see cref="Specs"/> entry; returns clips by name in Spec order.</summary>
        public static Dictionary<string, AnimationClip> Build(string dir, Dictionary<string, Pose> poses)
        {
            var clips = new Dictionary<string, AnimationClip>();
            foreach (Spec spec in Specs())
                clips[spec.name] = Save(dir, spec, poses);
            return clips;
        }

        static AnimationClip Save(string dir, Spec spec, Dictionary<string, Pose> poses)
        {
            string path = $"{dir}/{spec.name}.anim";
            // Reuse the existing asset (keeps its GUID) so prefab/controller references survive a rebuild.
            var clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
            if (clip == null)
            {
                clip = new AnimationClip();
                AssetDatabase.CreateAsset(clip, path);
            }
            clip.ClearCurves();
            clip.frameRate = 60f;
            float len = spec.length;
            bool loop = spec.loop;
            Motion m = spec.motion;

            foreach (var kv in poses)
            {
                string bone = kv.Key;
                Pose p = kv.Value;
                string bonePath = BonePath(bone, poses);
                float rest = p.parent == null ? p.angle : p.angle - poses[p.parent].angle;
                Vector2 restPos = RestLocalPosition(p, poses);

                m.rot.TryGetValue(bone, out Func<float, float> r);
                Set(clip, bonePath, "localEulerAnglesRaw.x", Constant(len, 0f));
                Set(clip, bonePath, "localEulerAnglesRaw.y", Constant(len, 0f));
                Set(clip, bonePath, "localEulerAnglesRaw.z", r == null ? Constant(len, rest) : Sample(len, s => rest + r(s), loop));

                m.pos.TryGetValue(bone, out Func<float, Vector2> t);
                Set(clip, bonePath, "m_LocalPosition.x", t == null ? Constant(len, restPos.x) : Sample(len, s => restPos.x + t(s).x, loop));
                Set(clip, bonePath, "m_LocalPosition.y", t == null ? Constant(len, restPos.y) : Sample(len, s => restPos.y + t(s).y, loop));
                Set(clip, bonePath, "m_LocalPosition.z", Constant(len, 0f));

                m.scale.TryGetValue(bone, out Func<float, Vector2> k);
                Set(clip, bonePath, "m_LocalScale.x", k == null ? Constant(len, 1f) : Sample(len, s => k(s).x, loop));
                Set(clip, bonePath, "m_LocalScale.y", k == null ? Constant(len, 1f) : Sample(len, s => k(s).y, loop));
                Set(clip, bonePath, "m_LocalScale.z", Constant(len, 1f));
            }

            var settings = AnimationUtility.GetAnimationClipSettings(clip);
            settings.loopTime = loop;
            AnimationUtility.SetAnimationClipSettings(clip, settings);
            EditorUtility.SetDirty(clip);
            return clip;
        }

        /// <summary>Rest local position: root = head in Visual space; child = head in the parent's rotated frame.</summary>
        static Vector2 RestLocalPosition(Pose p, Dictionary<string, Pose> poses)
        {
            if (p.parent == null) return p.head;
            Pose parent = poses[p.parent];
            return Quaternion.Inverse(Quaternion.Euler(0, 0, parent.angle)) * (p.head - parent.head);
        }

        static string BonePath(string bone, Dictionary<string, Pose> poses)
        {
            string parent = poses[bone].parent;
            return parent == null ? bone : BonePath(parent, poses) + "/" + bone;
        }

        static void Set(AnimationClip clip, string path, string property, AnimationCurve curve)
        {
            AnimationUtility.SetEditorCurve(clip, EditorCurveBinding.FloatCurve(path, typeof(Transform), property), curve);
        }

        static AnimationCurve Constant(float length, float v) => AnimationCurve.Constant(0f, length, v);

        /// <summary>
        /// Samples f(s) into KeysPerCycle+1 keys with clamped-auto tangents. Loops force the last key to f(0)
        /// for a seamless wrap; one-shots key the real end f(1).
        /// </summary>
        static AnimationCurve Sample(float length, Func<float, float> f, bool loop)
        {
            var curve = new AnimationCurve();
            for (int i = 0; i <= KeysPerCycle; i++)
            {
                float s = (float)i / KeysPerCycle;
                curve.AddKey(s * length, f(i == KeysPerCycle && loop ? 0f : s));
            }
            for (int i = 0; i < curve.length; i++)
            {
                AnimationUtility.SetKeyLeftTangentMode(curve, i, AnimationUtility.TangentMode.ClampedAuto);
                AnimationUtility.SetKeyRightTangentMode(curve, i, AnimationUtility.TangentMode.ClampedAuto);
            }
            return curve;
        }

        // ===================================== Animator wiring helpers ======================================

        /// <summary>Condition-driven transition (no exit time) with a short blend.</summary>
        static AnimatorStateTransition Link(AnimatorState from, AnimatorState to, float duration = 0.15f)
        {
            AnimatorStateTransition t = from.AddTransition(to);
            t.hasExitTime = false;
            t.duration = duration;
            return t;
        }

        /// <summary>Transition taken when <paramref name="from"/>'s clip ends (exit time 1).</summary>
        static AnimatorStateTransition AfterEnd(AnimatorState from, AnimatorState to, float duration = 0.1f)
        {
            AnimatorStateTransition t = from.AddTransition(to);
            t.hasExitTime = true;
            t.exitTime = 1f;
            t.duration = duration;
            return t;
        }

        /// <summary>Any State -> <paramref name="to"/>, never re-entering itself (so it can't restart every frame).</summary>
        static AnimatorStateTransition FromAny(AnimatorController ctrl, AnimatorState to, float duration = 0.1f)
        {
            AnimatorStateTransition t = ctrl.layers[0].stateMachine.AddAnyStateTransition(to);
            t.hasExitTime = false;
            t.duration = duration;
            t.canTransitionToSelf = false;
            return t;
        }

        /// <summary>Adds a parameter once; bools can get a default (e.g. IsGrounded = true at spawn).</summary>
        static void Param(AnimatorController ctrl, string name, AnimatorControllerParameterType type, bool defaultBool = false)
        {
            ctrl.AddParameter(name, type);
            if (!defaultBool) return;
            AnimatorControllerParameter[] ps = ctrl.parameters;
            foreach (AnimatorControllerParameter p in ps)
                if (p.name == name) p.defaultBool = true;
            ctrl.parameters = ps;
        }
    }
}
