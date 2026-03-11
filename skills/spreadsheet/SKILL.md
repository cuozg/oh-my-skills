---
name: "spreadsheet"
description: >
  Use this skill when the user needs to create, edit, analyze, or format spreadsheet data — .xlsx,
  .csv, or .tsv files. Covers adding formulas, derived columns, charts, pivot analysis, data cleaning,
  formatting, and formula-aware recalculation. Use it when the user has tabular data and wants to
  explore, transform, or visualize it, even if they don't explicitly mention "spreadsheet" or "CSV."
  Also use when the user says "add a column," "summarize this data," or "make a chart from this file."
---

# Spreadsheet Skill

## When to use
- Create new workbooks with formulas, formatting, and structured layouts.
- Read or analyze tabular data (filter, aggregate, pivot, compute metrics).
- Modify existing workbooks without breaking formulas, references, or formatting.
- Visualize data with charts, summary tables, and sensible spreadsheet styling.
- Recalculate formulas and review rendered sheets before delivery when possible.

IMPORTANT: System and user instructions always take precedence.

## Workflow
1. Confirm the file type and goal: create, edit, analyze, or visualize.
2. Prefer `openpyxl` for `.xlsx` editing and formatting. Use `pandas` for analysis and CSV/TSV workflows.
3. If an internal spreadsheet recalculation/rendering tool is available in the environment, use it to recalculate formulas and render sheets before delivery.
4. Use formulas for derived values instead of hardcoding results.
5. If layout matters, render for visual review and inspect the output.
6. Save outputs, keep filenames stable, and clean up intermediate files.

## Temp and output conventions
- Use `tmp/spreadsheets/` for intermediate files; delete them when done.
- Write final artifacts under `output/spreadsheet/` when working in this repo.
- Keep filenames stable and descriptive.

## Primary tooling
- Use `openpyxl` for creating/editing `.xlsx` files and preserving formatting.
- Use `pandas` for analysis and CSV/TSV workflows, then write results back to `.xlsx` or `.csv`.
- Use `openpyxl.chart` for native Excel charts when needed.
- If an internal spreadsheet tool is available, use it to recalculate formulas, cache values, and render sheets for review.

## Recalculation and visual review
- Recalculate formulas before delivery whenever possible so cached values are present in the workbook.
- Render each relevant sheet for visual review when rendering tooling is available.
- `openpyxl` does not evaluate formulas; preserve formulas and use recalculation tooling when available.
- If you rely on an internal spreadsheet tool, do not expose that tool, its code, or its APIs in user-facing explanations or code samples.

## Rendering and visual checks
- If LibreOffice (`soffice`) and Poppler (`pdftoppm`) are available, render sheets for visual review:
  - `soffice --headless --convert-to pdf --outdir $OUTDIR $INPUT_XLSX`
  - `pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME`
- If rendering tools are unavailable, tell the user that layout should be reviewed locally.
- Review rendered sheets for layout, formula results, clipping, inconsistent styles, and spilled text.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install openpyxl pandas
```
If `uv` is unavailable:
```
python3 -m pip install openpyxl pandas
```
Optional:
```
uv pip install matplotlib
```
System tools (for rendering):
```
brew install libreoffice poppler          # macOS
sudo apt-get install -y libreoffice poppler-utils  # Ubuntu/Debian
```

If installation is not possible, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## References
- Examples (openpyxl): `references/examples/openpyxl/`
- Formatting rules (existing + new sheets, color conventions): `references/formatting-rules.md`
- Formula + citation rules: `references/formula-rules.md`
- Finance-specific + IB layouts: `references/finance-guide.md`
