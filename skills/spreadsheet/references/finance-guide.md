# Finance-Specific Guide

## Finance requirements
- Format zeros as `-`.
- Negative numbers should be red and in parentheses.
- Format multiples as `5.2x`.
- Always specify units in headers (e.g., `Revenue ($mm)`).
- Cite sources for all raw inputs in cell comments.
- For new financial models with no user-specified style:
  - Blue text: hardcoded inputs
  - Black: formulas
  - Green: internal workbook links
  - Red: external links
  - Yellow fill: key assumptions that need attention

## Investment banking layouts
If the spreadsheet is an IB-style model (LBO, DCF, 3-statement, valuation):
- Totals should sum the range directly above.
- Hide gridlines and use horizontal borders above totals across relevant columns.
- Section headers should be merged cells with dark fill and white text.
- Column labels for numeric data should be right-aligned; row labels should be left-aligned.
- Indent submetrics under their parent line items.
