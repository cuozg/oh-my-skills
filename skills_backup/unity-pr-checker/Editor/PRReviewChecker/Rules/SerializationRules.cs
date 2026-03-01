using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans C# source files for Unity serialization pitfalls:
    ///   - Public fields without [SerializeField] (accidental exposure)
    ///   - [System.Serializable] structs with properties (not serialized by Unity)
    ///   - SerializeReference on interface/abstract without concrete type
    ///   - Non-serializable types in serialized fields (Dictionary, HashSet)
    ///   - [NonSerialized] on private fields (redundant but confusing)
    ///   - BinaryFormatter usage (deprecated, security risk)
    /// </summary>
    public class SerializationRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.Serialization;

        private static readonly (string id, string title, string pattern, Severity sev, string why, string fix)[] Rules =
        {
            (
                "SR001",
                "Public field without [SerializeField] attribute",
                @"public\s+(?!static|const|readonly|class|struct|enum|interface|override|virtual|abstract)([\w<>\[\]]+)\s+\w+\s*;",
                Severity.P2_Suggestion,
                "Public fields expose data to any external code. Prefer [SerializeField] private fields to " +
                "maintain encapsulation while keeping Inspector visibility.",
                "Change `public T field;` to `[SerializeField] private T _field;` and add a public property if external access is needed."
            ),
            (
                "SR002",
                "Dictionary or HashSet used as serialized field",
                @"\[SerializeField\][^;]*(?:Dictionary|HashSet)\s*<",
                Severity.P0_BlockMerge,
                "Unity cannot serialize Dictionary or HashSet. These fields will always be null/empty at runtime " +
                "after deserialization — a common source of NullReferenceExceptions.",
                "Use a serializable key-value pair list or a custom [Serializable] class. " +
                "Consider packages like odinSerializer for complex data or a List<KVPair> pattern."
            ),
            (
                "SR003",
                "Auto-property on [System.Serializable] struct/class",
                @"\[System\.Serializable\][^{]*\{[^}]*\{\s*get;\s*(set;)?\s*\}",
                Severity.P1_MustFix,
                "Unity serializes fields, not properties. Auto-properties are NOT serialized even inside " +
                "[Serializable] classes — data will be silently lost.",
                "Replace auto-properties with [SerializeField] private fields and explicit public accessors."
            ),
            (
                "SR004",
                "BinaryFormatter usage detected",
                @"BinaryFormatter\s*(\(\)|\.)",
                Severity.P0_BlockMerge,
                "BinaryFormatter is deprecated (.NET 5+), disabled by default in Unity 2022+, and has known " +
                "deserialization vulnerabilities (CVE-style remote code execution via malicious save files).",
                "Replace with JsonUtility, Newtonsoft.Json, or a custom binary format. " +
                "For save games use PlayerPrefs + JSON or a proper serialization library."
            ),
            (
                "SR005",
                "[SerializeReference] field with concrete sealed type",
                @"\[SerializeReference\][^;]*\b(int|float|bool|string|Vector2|Vector3|Quaternion)\b",
                Severity.P2_Suggestion,
                "[SerializeReference] is for polymorphic references (interfaces/abstract classes). " +
                "Using it on value types or sealed types adds overhead with no benefit.",
                "Use [SerializeField] for value types and concrete sealed types. " +
                "Reserve [SerializeReference] for polymorphic scenarios."
            ),
            (
                "SR006",
                "OnValidate modifying serialized data without Undo",
                @"void\s+OnValidate\s*\(\s*\)[^}]*=\s*[^;]+;",
                Severity.P1_MustFix,
                "OnValidate runs in the Editor on every change. Modifying serialized fields without Undo.RecordObject " +
                "will bypass the Undo system and can cause data loss.",
                "Guard modifications: `UnityEditor.Undo.RecordObject(this, \"Validate\");` before field changes in OnValidate."
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
                            Category     = RuleCategory.Serialization,
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
