#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace PRReviewChecker
{
    /// <summary>
    /// Unity EditorWindow that runs all PR review checks against the current project
    /// and displays findings with severity badges, category tabs, fix hints, and file-jump links.
    ///
    /// Open via: Tools > PR Review Checker
    /// </summary>
    public class PRReviewCheckerWindow : EditorWindow
    {
        // ---------------------------------------------------------------
        // Menu
        // ---------------------------------------------------------------

        [MenuItem("Tools/PR Review Checker", priority = 1000)]
        public static void ShowWindow()
        {
            var wnd = GetWindow<PRReviewCheckerWindow>("PR Review Checker");
            wnd.minSize = new Vector2(700, 500);
        }

        // ---------------------------------------------------------------
        // State
        // ---------------------------------------------------------------

        private List<PRReviewFinding> _allFindings   = new List<PRReviewFinding>();
        private bool                  _isScanning    = false;
        private float                 _scanProgress  = 0f;
        private string                _scanStatus    = "";
        private DateTime              _lastScanTime;
        private bool                  _hasScanned    = false;

        // Filtering
        private int                   _selectedTab   = 0;  // 0 = All
        private Severity?             _severityFilter = null;
        private string                _searchText    = "";
        private Vector2               _scrollPos;

        // Detail panel
        private PRReviewFinding       _selectedFinding;
        private Vector2               _detailScroll;
        private bool                  _showDetail    = false;

        // ---------------------------------------------------------------
        // Styles (lazy-initialized)
        // ---------------------------------------------------------------

        private GUIStyle _headerStyle;
        private GUIStyle _p0Style;
        private GUIStyle _p1Style;
        private GUIStyle _p2Style;
        private GUIStyle _rowSelectedStyle;
        private GUIStyle _rowNormalStyle;
        private bool     _stylesInitialized;

        private void InitStyles()
        {
            if (_stylesInitialized) return;
            _stylesInitialized = true;

            _headerStyle = new GUIStyle(EditorStyles.boldLabel)
            {
                fontSize = 13,
                alignment = TextAnchor.MiddleLeft,
            };

            Color p0Color = new Color(0.85f, 0.2f, 0.2f);
            Color p1Color = new Color(0.9f, 0.55f, 0f);
            Color p2Color = new Color(0.25f, 0.55f, 0.85f);

            _p0Style = MakeBadgeStyle(p0Color);
            _p1Style = MakeBadgeStyle(p1Color);
            _p2Style = MakeBadgeStyle(p2Color);

            _rowSelectedStyle = new GUIStyle(EditorStyles.label)
            {
                normal = { background = MakeTexture(new Color(0.17f, 0.36f, 0.53f, 0.8f)) },
            };
            _rowNormalStyle = new GUIStyle(EditorStyles.label);
        }

        private static GUIStyle MakeBadgeStyle(Color bg)
        {
            var style = new GUIStyle(EditorStyles.miniLabel)
            {
                alignment  = TextAnchor.MiddleCenter,
                fontStyle  = FontStyle.Bold,
                normal     = { background = MakeTexture(bg), textColor = Color.white },
                padding    = new RectOffset(4, 4, 2, 2),
                margin     = new RectOffset(2, 2, 2, 2),
            };
            return style;
        }

        private static Texture2D MakeTexture(Color c)
        {
            var t = new Texture2D(1, 1);
            t.SetPixel(0, 0, c);
            t.Apply();
            return t;
        }

        // ---------------------------------------------------------------
        // Tabs
        // ---------------------------------------------------------------

        private static readonly string[] TabNames =
        {
            "All", "Code Logic", "Serialization", "Security", "Performance", "Prefabs", "Assets",
        };

        private static readonly RuleCategory?[] TabCategories =
        {
            null,
            RuleCategory.CodeLogic,
            RuleCategory.Serialization,
            RuleCategory.Security,
            RuleCategory.Performance,
            RuleCategory.PrefabIntegrity,
            RuleCategory.AssetSettings,
        };

        // ---------------------------------------------------------------
        // GUI
        // ---------------------------------------------------------------

        private void OnGUI()
        {
            InitStyles();

            DrawHeader();
            DrawToolbar();
            DrawTabs();

            var filtered = GetFilteredFindings();

            if (_showDetail && _selectedFinding != null)
            {
                DrawSplitView(filtered);
            }
            else
            {
                DrawFindingsList(filtered);
            }

            if (_isScanning)
                DrawProgressOverlay();
        }

        private void DrawHeader()
        {
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            GUILayout.Label("🔍 PR Review Checker", _headerStyle ?? EditorStyles.boldLabel,
                GUILayout.ExpandWidth(false));

            GUILayout.FlexibleSpace();

            if (_hasScanned)
            {
                var sevCounts = PRReviewEngine.GetSeverityCounts(_allFindings);
                DrawBadge($"⛔ {sevCounts[Severity.P0_BlockMerge]} P0", _p0Style ?? EditorStyles.miniLabel);
                DrawBadge($"⚠️ {sevCounts[Severity.P1_MustFix]} P1", _p1Style ?? EditorStyles.miniLabel);
                DrawBadge($"💡 {sevCounts[Severity.P2_Suggestion]} P2", _p2Style ?? EditorStyles.miniLabel);
                GUILayout.Space(10);
                GUILayout.Label($"Last scan: {_lastScanTime:HH:mm:ss}", EditorStyles.miniLabel,
                    GUILayout.ExpandWidth(false));
            }

            GUILayout.Space(8);

            GUI.enabled = !_isScanning;
            if (GUILayout.Button("▶ Run Scan", EditorStyles.toolbarButton, GUILayout.Width(80)))
                RunScan();
            GUI.enabled = true;

            if (_hasScanned && GUILayout.Button("📋 Copy Report", EditorStyles.toolbarButton, GUILayout.Width(90)))
                CopyReportToClipboard();

            EditorGUILayout.EndHorizontal();
        }

        private void DrawBadge(string text, GUIStyle style)
        {
            GUILayout.Label(text, style, GUILayout.ExpandWidth(false));
        }

        private void DrawToolbar()
        {
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

            // Severity filter
            GUILayout.Label("Severity:", EditorStyles.miniLabel, GUILayout.ExpandWidth(false));
            if (GUILayout.Toggle(_severityFilter == null, "All", EditorStyles.toolbarButton, GUILayout.Width(30)))
                _severityFilter = null;
            if (GUILayout.Toggle(_severityFilter == Severity.P0_BlockMerge, "P0", EditorStyles.toolbarButton, GUILayout.Width(28)))
                _severityFilter = Severity.P0_BlockMerge;
            if (GUILayout.Toggle(_severityFilter == Severity.P1_MustFix, "P1", EditorStyles.toolbarButton, GUILayout.Width(28)))
                _severityFilter = Severity.P1_MustFix;
            if (GUILayout.Toggle(_severityFilter == Severity.P2_Suggestion, "P2", EditorStyles.toolbarButton, GUILayout.Width(28)))
                _severityFilter = Severity.P2_Suggestion;

            GUILayout.Space(10);

            // Search
            GUILayout.Label("🔎", EditorStyles.miniLabel, GUILayout.ExpandWidth(false));
            _searchText = EditorGUILayout.TextField(_searchText, EditorStyles.toolbarSearchField,
                GUILayout.MinWidth(120), GUILayout.MaxWidth(250));
            if (GUILayout.Button("✕", EditorStyles.toolbarButton, GUILayout.Width(18)))
                _searchText = "";

            GUILayout.FlexibleSpace();
            EditorGUILayout.EndHorizontal();
        }

        private void DrawTabs()
        {
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            for (int i = 0; i < TabNames.Length; i++)
            {
                int count = TabCategories[i] == null
                    ? _allFindings.Count
                    : _allFindings.Count(f => f.Category == TabCategories[i]);

                string label = count > 0 ? $"{TabNames[i]} ({count})" : TabNames[i];

                if (GUILayout.Toggle(_selectedTab == i, label, EditorStyles.toolbarButton))
                    _selectedTab = i;
            }
            EditorGUILayout.EndHorizontal();
        }

        private void DrawFindingsList(List<PRReviewFinding> findings)
        {
            if (!_hasScanned)
            {
                DrawEmptyState("Click ▶ Run Scan to analyze your project.", MessageType.Info);
                return;
            }

            if (findings.Count == 0)
            {
                DrawEmptyState("✅ No issues found for this filter!", MessageType.Info);
                return;
            }

            // Column headers
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            GUILayout.Label("Sev",      EditorStyles.miniLabel, GUILayout.Width(36));
            GUILayout.Label("Cat",      EditorStyles.miniLabel, GUILayout.Width(88));
            GUILayout.Label("Rule",     EditorStyles.miniLabel, GUILayout.Width(52));
            GUILayout.Label("Title",    EditorStyles.miniLabel, GUILayout.ExpandWidth(true));
            GUILayout.Label("File",     EditorStyles.miniLabel, GUILayout.Width(200));
            GUILayout.Label("Line",     EditorStyles.miniLabel, GUILayout.Width(40));
            EditorGUILayout.EndHorizontal();

            _scrollPos = EditorGUILayout.BeginScrollView(_scrollPos);
            foreach (var f in findings)
            {
                bool isSelected = f == _selectedFinding;
                var rowStyle = isSelected ? _rowSelectedStyle : _rowNormalStyle;

                EditorGUILayout.BeginHorizontal(rowStyle);

                // Severity badge
                DrawSeverityBadge(f.Severity);

                // Category
                GUILayout.Label(CategoryShort(f.Category), EditorStyles.miniLabel, GUILayout.Width(88));

                // Rule ID
                GUILayout.Label(f.RuleId, EditorStyles.miniLabel, GUILayout.Width(52));

                // Title (clickable to open detail)
                if (GUILayout.Button(f.Title, EditorStyles.label, GUILayout.ExpandWidth(true)))
                {
                    _selectedFinding = f;
                    _showDetail = true;
                }

                // File (clickable to open in IDE)
                string shortFile = Path.GetFileName(f.FilePath);
                if (GUILayout.Button(shortFile, EditorStyles.linkLabel, GUILayout.Width(200)))
                    OpenFileAtLine(f.FilePath, f.Line);

                // Line
                GUILayout.Label(f.Line > 0 ? f.Line.ToString() : "—",
                    EditorStyles.miniLabel, GUILayout.Width(40));

                EditorGUILayout.EndHorizontal();
            }
            EditorGUILayout.EndScrollView();

            GUILayout.Label($"Showing {findings.Count} finding(s)", EditorStyles.centeredGreyMiniLabel);
        }

        private void DrawSplitView(List<PRReviewFinding> findings)
        {
            float splitRatio = 0.55f;
            float listHeight = position.height * splitRatio;

            // List pane
            GUILayout.BeginVertical(GUILayout.Height(listHeight));
            DrawFindingsList(findings);
            GUILayout.EndVertical();

            // Splitter
            GUILayout.Box("", GUILayout.ExpandWidth(true), GUILayout.Height(2));

            // Detail pane
            GUILayout.BeginVertical(GUILayout.ExpandHeight(true));
            DrawDetailPanel(_selectedFinding);
            GUILayout.EndVertical();
        }

        private void DrawDetailPanel(PRReviewFinding f)
        {
            if (f == null) return;

            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            GUILayout.Label($"Detail: {f.RuleId} — {f.Title}", EditorStyles.boldLabel);
            GUILayout.FlexibleSpace();
            if (GUILayout.Button("✕ Close", EditorStyles.toolbarButton, GUILayout.Width(60)))
                _showDetail = false;
            EditorGUILayout.EndHorizontal();

            _detailScroll = EditorGUILayout.BeginScrollView(_detailScroll);

            DrawSeverityBadge(f.Severity);
            GUILayout.Space(4);

            DrawDetailField("File",   string.IsNullOrEmpty(f.FilePath) ? "—" : f.FilePath);
            DrawDetailField("Line",   f.Line > 0 ? f.Line.ToString() : "—");
            DrawDetailField("Detail", f.Detail);

            GUILayout.Space(6);
            EditorGUILayout.HelpBox(f.WhyItMatters, MessageType.Warning);
            GUILayout.Space(4);
            EditorGUILayout.HelpBox("🔧 How to fix:\n" + f.HowToFix, MessageType.Info);

            GUILayout.Space(6);
            if (!string.IsNullOrEmpty(f.FilePath) && f.Line > 0)
            {
                if (GUILayout.Button($"📂 Open {Path.GetFileName(f.FilePath)} : {f.Line}"))
                    OpenFileAtLine(f.FilePath, f.Line);
            }

            EditorGUILayout.EndScrollView();
        }

        private static void DrawDetailField(string label, string value)
        {
            EditorGUILayout.BeginHorizontal();
            GUILayout.Label(label + ":", EditorStyles.boldLabel, GUILayout.Width(48));
            EditorGUILayout.SelectableLabel(value, GUILayout.ExpandWidth(true), GUILayout.Height(16));
            EditorGUILayout.EndHorizontal();
        }

        private void DrawSeverityBadge(Severity sev)
        {
            var (style, label) = sev switch
            {
                Severity.P0_BlockMerge => (_p0Style, "P0"),
                Severity.P1_MustFix    => (_p1Style, "P1"),
                _                      => (_p2Style, "P2"),
            };
            GUILayout.Label(label, style ?? EditorStyles.miniLabel, GUILayout.Width(28));
        }

        private void DrawProgressOverlay()
        {
            EditorUtility.DisplayProgressBar("PR Review Checker", _scanStatus, _scanProgress);
        }

        private static void DrawEmptyState(string msg, MessageType type)
        {
            GUILayout.Space(40);
            EditorGUILayout.HelpBox(msg, type);
        }

        // ---------------------------------------------------------------
        // Scan
        // ---------------------------------------------------------------

        private void RunScan()
        {
            _isScanning  = true;
            _scanStatus  = "Starting...";
            _scanProgress = 0f;
            Repaint();

            try
            {
                string assetsRoot = Application.dataPath;
                _allFindings = PRReviewEngine.RunAll(assetsRoot, (status, progress) =>
                {
                    _scanStatus   = status;
                    _scanProgress = progress;
                    Repaint();
                });
            }
            finally
            {
                _isScanning  = false;
                _hasScanned  = true;
                _lastScanTime = DateTime.Now;
                EditorUtility.ClearProgressBar();
                Repaint();

                int p0Count = _allFindings.Count(f => f.Severity == Severity.P0_BlockMerge);
                if (p0Count > 0)
                    Debug.LogError($"[PRReviewChecker] Scan complete: {p0Count} P0 issue(s) — MERGE BLOCKED");
                else
                    Debug.Log($"[PRReviewChecker] Scan complete: {_allFindings.Count} findings");
            }
        }

        // ---------------------------------------------------------------
        // Filtering
        // ---------------------------------------------------------------

        private List<PRReviewFinding> GetFilteredFindings()
        {
            var results = _allFindings.AsEnumerable();

            // Category tab
            if (TabCategories[_selectedTab] != null)
                results = results.Where(f => f.Category == TabCategories[_selectedTab]);

            // Severity filter
            if (_severityFilter != null)
                results = results.Where(f => f.Severity == _severityFilter);

            // Search
            if (!string.IsNullOrEmpty(_searchText))
            {
                var q = _searchText.ToLowerInvariant();
                results = results.Where(f =>
                    (f.Title    != null && f.Title.ToLowerInvariant().Contains(q)) ||
                    (f.FilePath != null && f.FilePath.ToLowerInvariant().Contains(q)) ||
                    (f.RuleId   != null && f.RuleId.ToLowerInvariant().Contains(q)));
            }

            return results.ToList();
        }

        // ---------------------------------------------------------------
        // Actions
        // ---------------------------------------------------------------

        private void CopyReportToClipboard()
        {
            var sb = new System.Text.StringBuilder();
            sb.AppendLine("# PR Review Checker Report");
            sb.AppendLine($"Generated: {_lastScanTime:yyyy-MM-dd HH:mm:ss}");
            sb.AppendLine($"Total findings: {_allFindings.Count}");
            sb.AppendLine();

            var sevCounts = PRReviewEngine.GetSeverityCounts(_allFindings);
            sb.AppendLine($"| Severity | Count |");
            sb.AppendLine($"|----------|-------|");
            sb.AppendLine($"| P0 Block Merge | {sevCounts[Severity.P0_BlockMerge]} |");
            sb.AppendLine($"| P1 Must Fix    | {sevCounts[Severity.P1_MustFix]} |");
            sb.AppendLine($"| P2 Suggestion  | {sevCounts[Severity.P2_Suggestion]} |");
            sb.AppendLine();
            sb.AppendLine("## Findings");
            sb.AppendLine("| Sev | Category | Rule | Title | File | Line |");
            sb.AppendLine("|-----|----------|------|-------|------|------|");

            foreach (var f in _allFindings)
            {
                sb.AppendLine($"| {f.Severity} | {f.Category} | {f.RuleId} | {f.Title} | {Path.GetFileName(f.FilePath)} | {f.Line} |");
            }

            EditorGUIUtility.systemCopyBuffer = sb.ToString();
            Debug.Log("[PRReviewChecker] Report copied to clipboard.");
        }

        private static void OpenFileAtLine(string relativePath, int line)
        {
            // relativePath is relative to Assets/ — construct full path
            string fullPath = Path.Combine(
                Application.dataPath.Replace("/Assets", ""),
                "Assets",
                relativePath.TrimStart('/', '\\'));

            if (!File.Exists(fullPath))
                fullPath = relativePath; // try as-is (already absolute or asset path)

            var asset = AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(
                "Assets/" + relativePath.TrimStart('/', '\\'));

            if (asset != null)
                AssetDatabase.OpenAsset(asset, line);
            else
                EditorUtility.OpenWithDefaultApp(fullPath);
        }

        // ---------------------------------------------------------------
        // Helpers
        // ---------------------------------------------------------------

        private static string CategoryShort(RuleCategory cat) => cat switch
        {
            RuleCategory.CodeLogic      => "Code Logic",
            RuleCategory.Serialization  => "Serialize",
            RuleCategory.Security       => "Security",
            RuleCategory.Performance    => "Perf",
            RuleCategory.PrefabIntegrity => "Prefab",
            RuleCategory.AssetSettings  => "Assets",
            _                           => cat.ToString(),
        };
    }
}
#endif
