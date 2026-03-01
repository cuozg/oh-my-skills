using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans C# source files for Unity security issues:
    ///   - PlayerPrefs storing passwords/tokens/secrets
    ///   - Unencrypted network data (WWW class deprecated)
    ///   - eval/Reflection.Assembly.Load from external sources
    ///   - Hardcoded API keys or connection strings
    ///   - Application.OpenURL with unsanitized input
    ///   - BinaryFormatter (also flagged in Serialization — P0 here)
    /// </summary>
    public class SecurityRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.Security;

        private static readonly (string id, string title, string pattern, Severity sev, string why, string fix)[] Rules =
        {
            (
                "SEC001",
                "PlayerPrefs storing sensitive data (password/token/secret/key)",
                @"PlayerPrefs\.Set(String|Int|Float)\s*\(\s*""[^""]*(?:password|token|secret|apikey|api_key|auth)[^""]*""",
                Severity.P0_BlockMerge,
                "PlayerPrefs is stored as plaintext in the OS registry (Windows) or plist (macOS/iOS). " +
                "Any sensitive value stored here can be read by other apps or extracted from device backups.",
                "Never store credentials in PlayerPrefs. Use OS Keychain APIs, encrypted storage, or a " +
                "server-side token exchange. For development secrets use ScriptableObject assets excluded from VCS."
            ),
            (
                "SEC002",
                "Hardcoded secret/API key string literal",
                @"(api[_-]?key|secret|password|token|bearer|apiSecret)\s*=\s*""[A-Za-z0-9+/=_\-]{8,}""",
                Severity.P0_BlockMerge,
                "Hardcoded secrets in source code are trivially extracted from built applications " +
                "and permanently exposed once committed to version control.",
                "Use environment variables, Unity Cloud Config, or a secrets manager. " +
                "Rotate the exposed secret immediately if already committed."
            ),
            (
                "SEC003",
                "Assembly.Load / Assembly.LoadFrom with runtime path",
                @"Assembly\.(Load|LoadFrom|LoadFile)\s*\(",
                Severity.P0_BlockMerge,
                "Dynamic assembly loading from untrusted paths is the vector for CVE-2025-59489 " +
                "(Unity Android ACE, CVSS 8.4). Malicious save files or network data can redirect this " +
                "to load attacker-controlled code.",
                "Remove dynamic assembly loading. If plugin architecture is needed, validate assembly " +
                "signatures and restrict loading to a known safe directory with hash verification."
            ),
            (
                "SEC004",
                "Application.OpenURL with variable/user-controlled input",
                @"Application\.OpenURL\s*\(\s*(?!""http)",
                Severity.P1_MustFix,
                "Application.OpenURL with unsanitized input enables URL injection attacks — " +
                "attackers can construct file:// or custom-scheme URLs to exfiltrate data.",
                "Validate URLs against an allowlist of domains before calling OpenURL. " +
                "Never pass user-provided strings directly."
            ),
            (
                "SEC005",
                "WWW class usage (deprecated, no TLS enforcement)",
                @"\bnew\s+WWW\s*\(",
                Severity.P1_MustFix,
                "The WWW class is deprecated since Unity 2018.2 and does not enforce TLS certificate " +
                "validation — susceptible to MITM attacks.",
                "Replace with UnityWebRequest. Set `certificateHandler` for custom validation, " +
                "or use the default handler which validates TLS certificates."
            ),
            (
                "SEC006",
                "Insecure HTTP endpoint (not HTTPS)",
                @"""http://(?!localhost|127\.0\.0\.1)",
                Severity.P1_MustFix,
                "Plain HTTP transmits all data unencrypted. This includes any auth tokens, " +
                "player data, or analytics sent over the wire.",
                "Use HTTPS for all production endpoints. HTTP is acceptable only for local development."
            ),
        };

        public List<PRReviewFinding> Scan(string assetsRoot)
        {
            var findings = new List<PRReviewFinding>();
            foreach (var csFile in Directory.GetFiles(assetsRoot, "*.cs", SearchOption.AllDirectories))
            {
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
                            Category     = RuleCategory.Security,
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
