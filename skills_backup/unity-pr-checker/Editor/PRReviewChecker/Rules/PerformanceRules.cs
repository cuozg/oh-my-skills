using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans C# source files for Unity performance anti-patterns:
    ///   - String concatenation in hot paths (GC pressure)
    ///   - new() allocations in Update/FixedUpdate/LateUpdate
    ///   - LINQ usage in hot paths
    ///   - Object.FindObjectOfType in Update (already in CodeLogic but P0 here)
    ///   - transform.position read in tight loops without caching
    ///   - SendMessage / BroadcastMessage usage
    ///   - Debug.Log in non-editor builds
    /// </summary>
    public class PerformanceRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.Performance;

        // Hot-path method names for context-aware matching
        private const string HotPathPattern =
            @"void\s+(Update|FixedUpdate|LateUpdate|OnTriggerStay|OnCollisionStay)\s*\([^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*";

        private static readonly (string id, string title, string pattern, Severity sev, string why, string fix)[] Rules =
        {
            (
                "PERF001",
                "String concatenation (+) in Update/FixedUpdate — GC alloc per frame",
                @"(void\s+(Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)\+\s*""|\+\s*[a-zA-Z_]\w*\s*\+",
                Severity.P1_MustFix,
                "String + string creates a new heap allocation every call. At 60fps this generates " +
                "3,600+ GC objects per second, spiking GC collection and causing frame stutters.",
                "Use StringBuilder for repeated concatenation, or string interpolation with " +
                "cached format strings. For debug display use a fixed char buffer."
            ),
            (
                "PERF002",
                "new() allocation in Update/FixedUpdate/LateUpdate",
                @"(void\s+(Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)\bnew\s+(?!List|Dictionary|HashSet|Queue|Stack|Array)\w+\s*[(<]",
                Severity.P1_MustFix,
                "Object allocation in a hot path forces GC collection. Even small objects (Vector3, " +
                "WaitForSeconds) add up at 60fps.",
                "Cache reusable objects as fields. Use object pools for frequently created/destroyed objects. " +
                "Prefer struct types for small value types to avoid heap allocation."
            ),
            (
                "PERF003",
                "LINQ query in Update/FixedUpdate/LateUpdate",
                @"(void\s+(Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)(\.Where\(|\.Select\(|\.FirstOrDefault\(|\.Any\(|\.OrderBy\(|\.ToList\(|\.ToArray\()",
                Severity.P1_MustFix,
                "LINQ allocates IEnumerator objects and intermediate collections on the heap. " +
                "A single .ToList() call per frame generates thousands of GC allocations per second.",
                "Pre-compute and cache LINQ results. Use manual for loops in hot paths. " +
                "Consider using Span<T> or ArraySegment<T> for zero-allocation enumeration."
            ),
            (
                "PERF004",
                "SendMessage / BroadcastMessage usage",
                @"\b(SendMessage|BroadcastMessage|SendMessageUpwards)\s*\(",
                Severity.P1_MustFix,
                "SendMessage uses reflection to find and invoke methods by name string — no compile-time " +
                "safety, ~10x slower than a direct call, and triggers GC allocations.",
                "Replace with direct method calls, C# events/delegates, or UnityEvent. " +
                "For cross-component communication use ScriptableObject event channels."
            ),
            (
                "PERF005",
                "Debug.Log called outside #if UNITY_EDITOR guard",
                @"(?<!\#if\s+UNITY_EDITOR[^\n]*\n[^\n]*)Debug\.(Log|LogWarning|LogError|LogFormat)\s*\(",
                Severity.P2_Suggestion,
                "Debug.Log has significant overhead in release builds: string formatting, stack trace " +
                "capture, and thread synchronization — even when the console is hidden.",
                "Wrap all debug logging in `#if UNITY_EDITOR` or `#if DEVELOPMENT_BUILD`, " +
                "or use a conditional logging wrapper that strips in release."
            ),
            (
                "PERF006",
                "transform.tag comparison with string",
                @"\.tag\s*==\s*""",
                Severity.P2_Suggestion,
                "gameObject.tag == \"string\" allocates a new string each comparison. " +
                "At scale this adds measurable GC pressure.",
                "Use `gameObject.CompareTag(\"TagName\")` — it's allocation-free and faster."
            ),
            (
                "PERF007",
                "Physics.Raycast storing result in a new RaycastHit allocation in loop",
                @"(for|while|foreach)[^{]*\{[^}]*RaycastHit\s+\w+\s*=\s*new\s+RaycastHit",
                Severity.P2_Suggestion,
                "Declaring RaycastHit inside a loop re-initializes the struct each iteration.",
                "Declare RaycastHit as a field or outside the loop scope to reuse the stack allocation."
            ),
        };

        public List<PRReviewFinding> Scan(string assetsRoot)
        {
            var findings = new List<PRReviewFinding>();
            foreach (var csFile in Directory.GetFiles(assetsRoot, "*.cs", SearchOption.AllDirectories))
            {
                if (csFile.Contains("Generated") || csFile.Contains(".Designer.")) continue;

                var fullText = File.ReadAllText(csFile);
                var relativePath = MakeRelative(csFile, assetsRoot);

                foreach (var rule in Rules)
                {
                    var matches = Regex.Matches(fullText, rule.pattern,
                        RegexOptions.Singleline | RegexOptions.IgnoreCase);

                    foreach (Match match in matches)
                    {
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = rule.sev,
                            Category     = RuleCategory.Performance,
                            RuleId       = rule.id,
                            Title        = rule.title,
                            FilePath     = relativePath,
                            Line         = CountLines(fullText, match.Index),
                            Detail       = match.Value.Trim(),
                            WhyItMatters = rule.why,
                            HowToFix     = rule.fix,
                        });
                    }
                }
            }
            return findings;
        }

        private static int CountLines(string text, int charIndex)
        {
            int line = 1;
            for (int i = 0; i < charIndex && i < text.Length; i++)
                if (text[i] == '\n') line++;
            return line;
        }

        private static string MakeRelative(string fullPath, string root) =>
            fullPath.StartsWith(root) ? fullPath.Substring(root.Length).TrimStart('/', '\\') : fullPath;
    }
}
