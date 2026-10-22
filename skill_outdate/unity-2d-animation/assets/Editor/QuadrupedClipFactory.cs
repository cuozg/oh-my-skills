using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using Pose = Rig2D.EditorTools.SkinnedRigBuilder.Pose;

namespace Rig2D.EditorTools
{
    /// <summary>
    /// Procedurally keys Idle / Walk / Run on a quadruped skeleton. Bone naming convention:
    /// Pelvis, Spine, Neck, Head, Tail1..3, {BackLeft,BackRight,FrontLeft,FrontRight}{Thigh,Shin,Hoof}.
    /// Motions for bones the rig does not have are ignored; bones without a motion are keyed at rest.
    /// Every bone gets a rotation curve = rest angle + periodic offset, sampled into keyframes
    /// (clamped-auto tangents), so the clips stay fully editable in the Animation window.
    ///
    /// Keyframe timing (cycle s = 0..1, keys every 1/24 of the cycle, last key = first key for a seamless loop):
    ///  Idle  2.4 s : breathing bob (Pelvis y ±0.007), Spine ±0.6°, Neck/Head gentle nod, tail sway with lag.
    ///  Walk  0.7 s : 4-beat lateral walk — BackLeft 0, FrontLeft .25, BackRight .5, FrontRight .75;
    ///                thigh ±25°, knee fold 35° during swing, double bob per cycle, head nod, tail sway.
    ///  Run   0.45 s: transverse gallop — BackLeft 0, BackRight .1, FrontLeft .5, FrontRight .6;
    ///                thigh ±32°, knee fold 45°, suspension bob 0.045, body rock ±3°, neck stretched forward,
    ///                tail streaming back.
    /// </summary>
    internal static class QuadrupedClipFactory
    {
        internal struct Clips { public AnimationClip idle, walk, run; }

        const float Tau = Mathf.PI * 2f;
        const int KeysPerCycle = 24;

        /// <summary>Per-bone rotation offsets (degrees) + pelvis translation, as functions of cycle phase s.</summary>
        class Motion
        {
            public readonly Dictionary<string, Func<float, float>> rot = new();
            public Func<float, Vector2> pelvisOffset = _ => Vector2.zero;
        }

        public static Clips Build(string dir, Dictionary<string, Pose> poses)
        {
            return new Clips
            {
                idle = Save(dir, "Idle", 2.4f, Idle(), poses),
                walk = Save(dir, "Walk", 0.7f, Walk(), poses),
                run = Save(dir, "Run", 0.45f, Run(), poses),
            };
        }

        // ---------------------------------------------- motions ----------------------------------------------

        static Motion Idle()
        {
            var m = new Motion { pelvisOffset = s => new Vector2(0f, 0.007f * Mathf.Sin(Tau * s)) };
            m.rot["Spine"] = s => 0.6f * Mathf.Sin(Tau * s);
            // Front legs counter-rotate the spine sway so the front hooves stay planted.
            m.rot["FrontLeftThigh"] = s => -0.6f * Mathf.Sin(Tau * s);
            m.rot["FrontRightThigh"] = s => -0.6f * Mathf.Sin(Tau * s);
            m.rot["Neck"] = s => 1.5f * Mathf.Sin(Tau * s - 0.6f);
            m.rot["Head"] = s => -1.0f * Mathf.Sin(Tau * s - 1.0f);
            Tail(m, 0f, 3f, 5f, 7f, 0.7f);
            return m;
        }

        static Motion Walk()
        {
            var m = new Motion { pelvisOffset = s => new Vector2(0f, 0.012f * Mathf.Cos(2f * Tau * s)) };
            Leg(m, "BackLeft", 0.00f, 25f, 35f, 20f);
            Leg(m, "FrontLeft", 0.25f, 25f, 35f, 20f);
            Leg(m, "BackRight", 0.50f, 25f, 35f, 20f);
            Leg(m, "FrontRight", 0.75f, 25f, 35f, 20f);
            m.rot["Spine"] = s => 1.0f * Mathf.Sin(2f * Tau * s);
            m.rot["Neck"] = s => 2.0f * Mathf.Sin(2f * Tau * s + 0.8f);
            m.rot["Head"] = s => -1.5f * Mathf.Sin(2f * Tau * s + 0.8f);
            Tail(m, 0f, 4f, 6f, 8f, 0.6f);
            return m;
        }

        static Motion Run()
        {
            var m = new Motion { pelvisOffset = s => new Vector2(0f, 0.045f * Mathf.Sin(Tau * (s + 0.25f))) };
            Leg(m, "BackLeft", 0.00f, 32f, 45f, 22f);
            Leg(m, "BackRight", 0.10f, 32f, 45f, 22f);
            Leg(m, "FrontLeft", 0.50f, 32f, 45f, 22f);
            Leg(m, "FrontRight", 0.60f, 32f, 45f, 22f);
            m.rot["Pelvis"] = s => 3f * Mathf.Sin(Tau * s);                    // rocking-horse body pitch
            m.rot["Spine"] = s => 2f * Mathf.Sin(Tau * s + 0.6f);
            m.rot["Neck"] = s => -10f - 4f * Mathf.Sin(Tau * s + 0.6f);        // neck stretched forward
            m.rot["Head"] = s => 6f + 2f * Mathf.Sin(Tau * s + 1.2f);          // keep the face roughly level
            // Negative offsets uncurl the tail so it streams behind the body.
            m.rot["Tail1"] = s => -5f + 4f * Mathf.Sin(Tau * s - 0.5f);
            m.rot["Tail2"] = s => -18f + 9f * Mathf.Sin(Tau * s - 1.1f);
            m.rot["Tail3"] = s => -15f + 14f * Mathf.Sin(Tau * s - 1.7f);
            return m;
        }

        /// <summary>
        /// One leg cycle offset by <paramref name="phase"/>. Thigh swings sinusoidally (+ = forward);
        /// while it moves forward (swing phase) the shin and hoof fold back to lift the hoof off the ground.
        /// </summary>
        static void Leg(Motion m, string leg, float phase, float thigh, float shin, float hoof)
        {
            m.rot[leg + "Thigh"] = s => thigh * Mathf.Sin(Tau * (s + phase));
            m.rot[leg + "Shin"] = s => -shin * Lift(s + phase);
            m.rot[leg + "Hoof"] = s => -hoof * Lift(s + phase);
        }

        /// <summary>0 during stance, smooth 0..1..0 bump during swing (when the thigh moves forward).</summary>
        static float Lift(float s)
        {
            float c = Mathf.Cos(Tau * s);
            return c > 0f ? Mathf.Pow(c, 1.5f) : 0f;
        }

        /// <summary>Tail sway: each segment swings more and later than its parent -> follow-through.</summary>
        static void Tail(Motion m, float offset, float a1, float a2, float a3, float lag)
        {
            m.rot["Tail1"] = s => offset + a1 * Mathf.Sin(Tau * s);
            m.rot["Tail2"] = s => offset + a2 * Mathf.Sin(Tau * s - lag);
            m.rot["Tail3"] = s => offset + a3 * Mathf.Sin(Tau * s - 2f * lag);
        }

        // ---------------------------------------------- baking -----------------------------------------------

        static AnimationClip Save(string dir, string name, float length, Motion motion, Dictionary<string, Pose> poses)
        {
            string path = $"{dir}/{name}.anim";
            // Reuse the existing asset (keeps its GUID) so prefab/controller references survive a rebuild.
            var clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
            if (clip == null)
            {
                clip = new AnimationClip();
                AssetDatabase.CreateAsset(clip, path);
            }
            clip.ClearCurves();
            clip.frameRate = 60f;

            foreach (var kv in poses)
            {
                string bone = kv.Key;
                Pose p = kv.Value;
                string bonePath = BonePath(bone, poses);
                float rest = p.parent == null ? p.angle : p.angle - poses[p.parent].angle;
                motion.rot.TryGetValue(bone, out Func<float, float> f);

                // Every bone is keyed in every clip so no pose can leak between states.
                Set(clip, bonePath, "localEulerAnglesRaw.x", Constant(length, 0f));
                Set(clip, bonePath, "localEulerAnglesRaw.y", Constant(length, 0f));
                Set(clip, bonePath, "localEulerAnglesRaw.z",
                    f == null ? Constant(length, rest) : Sample(length, s => rest + f(s)));

                if (p.parent == null)
                {
                    Vector2 h = p.head;
                    Set(clip, bonePath, "m_LocalPosition.x", Sample(length, s => h.x + motion.pelvisOffset(s).x));
                    Set(clip, bonePath, "m_LocalPosition.y", Sample(length, s => h.y + motion.pelvisOffset(s).y));
                    Set(clip, bonePath, "m_LocalPosition.z", Constant(length, 0f));
                }
            }

            var settings = AnimationUtility.GetAnimationClipSettings(clip);
            settings.loopTime = true;
            AnimationUtility.SetAnimationClipSettings(clip, settings);
            EditorUtility.SetDirty(clip);
            return clip;
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

        /// <summary>Samples f over one cycle into KeysPerCycle+1 keys with clamped-auto tangents.</summary>
        static AnimationCurve Sample(float length, Func<float, float> f)
        {
            var curve = new AnimationCurve();
            for (int i = 0; i <= KeysPerCycle; i++)
            {
                float s = (float)i / KeysPerCycle;
                curve.AddKey(s * length, f(i == KeysPerCycle ? 0f : s));   // exact loop closure
            }
            for (int i = 0; i < curve.length; i++)
            {
                AnimationUtility.SetKeyLeftTangentMode(curve, i, AnimationUtility.TangentMode.ClampedAuto);
                AnimationUtility.SetKeyRightTangentMode(curve, i, AnimationUtility.TangentMode.ClampedAuto);
            }
            return curve;
        }
    }
}
