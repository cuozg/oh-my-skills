using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans C# source files for Unity code-logic pitfalls:
    ///   - Unity Object null checks using == null (operator overload trap)
    ///   - Camera.main in Update/FixedUpdate/LateUpdate
    ///   - Find* calls outside Awake/Start
    ///   - Empty catch blocks
    ///   - Coroutine started without null guard
    ///   - GetComponent inside Update loop
    /// </summary>
    public class CodeLogicRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.CodeLogic;

        // ---------------------------------------------------------------
        // Rule patterns: (ruleId, title, pattern, severity, why, fix)
        // ---------------------------------------------------------------
        private static readonly (string id, string title, string pattern, Severity sev, string why, string fix)[] Rules =
        {
            (
                "CL001",
                "Unity Object null check using == null",
                @"if\s*\(\s*\w+\s*==\s*null\s*\)|if\s*\(\s*null\s*==\s*\w+\s*\)",
                Severity.P1_MustFix,
                "Unity overloads == for destroyed objects. obj == null returns true for destroyed objects but " +
                "using ReferenceEquals or 'is null' will NOT catch destroyed objects.",
                "Use 'if (!obj)' or 'obj == null' explicitly — but never 'obj is null' or 'obj?.Method()' on " +
                "UnityEngine.Object subclasses for destroyed-object checks."
            ),
            (
                "CL002",
                "Camera.main accessed in hot path (Update/FixedUpdate/LateUpdate)",
                @"(void\s+Update|void\s+FixedUpdate|void\s+LateUpdate)[^}]*Camera\.main",
                Severity.P1_MustFix,
                "Camera.main calls FindObjectOfType internally — O(n) scan every frame.",
                "Cache Camera.main in Awake/Start: `private Camera _cam; void Awake() { _cam = Camera.main; }`"
            ),
            (
                "CL003",
                "GameObject.Find / FindObjectOfType outside Awake/Start",
                @"(GameObject\.Find|FindObjectOfType|FindObjectsOfType)\s*[<(]",
                Severity.P1_MustFix,
                "Find* methods are O(n) scene scans. Called per-frame they will spike CPU.",
                "Cache results in Awake/Start. Use dependency injection or ScriptableObject channels instead."
            ),
            (
                "CL004",
                "Empty catch block swallows exceptions",
                @"catch\s*(\([^)]*\))?\s*\{\s*\}",
                Severity.P1_MustFix,
                "Silent failures hide bugs and make debugging extremely difficult.",
                "At minimum: `catch (Exception e) { Debug.LogException(e); }` — or re-throw."
            ),
            (
                "CL005",
                "GetComponent called inside Update loop",
                @"(void\s+Update|void\s+FixedUpdate|void\s+LateUpdate)[^}]*GetComponent\s*[<(]",
                Severity.P1_MustFix,
                "GetComponent is not free — involves a native-to-managed bridge call every frame.",
                "Cache component references in Awake: `private Rigidbody _rb; void Awake() { _rb = GetComponent<Rigidbody>(); }`"
            ),
            (
                "CL006",
                "StartCoroutine without null/active guard",
                @"StartCoroutine\s*\(",
                Severity.P2_Suggestion,
                "StartCoroutine on a disabled or destroyed GameObject throws MissingReferenceException.",
                "Guard with: `if (this != null && gameObject.activeInHierarchy) StartCoroutine(...);`"
            ),
            (
                "CL007",
                "Destroy called without null check",
                @"Destroy\s*\(\s*\w+\s*\)",
                Severity.P2_Suggestion,
                "Calling Destroy(null) is safe, but Destroy on an already-destroyed object logs a warning.",
                "Use `if (obj != null) Destroy(obj);` for clarity and to suppress spurious warnings."
            ),
        };

        public List<PRReviewFinding> Scan(string assetsRoot)
        {
            var findings = new List<PRReviewFinding>();
            foreach (var csFile in Directory.GetFiles(assetsRoot, "*.cs", SearchOption.AllDirectories))
            {
                // Skip generated and Editor-only test files
                if (csFile.Contains("Generated") || csFile.Contains(".Designer.")) continue;

                var lines = File.ReadAllLines(csFile);
                var fullText = string.Join("\n", lines);
                var relativePath = MakeRelative(csFile, assetsRoot);

                foreach (var rule in Rules)
                {
                    var matches = Regex.Matches(fullText, rule.pattern,
                        RegexOptions.Singleline | RegexOptions.IgnoreCase);

                    foreach (Match match in matches)
                    {
                        int lineNum = CountLines(fullText, match.Index);
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = rule.sev,
                            Category     = RuleCategory.CodeLogic,
                            RuleId       = rule.id,
                            Title        = rule.title,
                            FilePath     = relativePath,
                            Line         = lineNum,
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
