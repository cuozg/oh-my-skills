# Formatting Rules

## Existing formatted spreadsheets
- Render and inspect a provided spreadsheet before modifying it when possible.
- Preserve existing formatting and style exactly.
- Match styles for any newly filled cells that were previously blank.
- Never overwrite established formatting unless the user explicitly asks for a redesign.

## New or unstyled spreadsheets
- Use appropriate number and date formats.
- Dates should render as dates, not plain numbers.
- Percentages should usually default to one decimal place unless the data calls for something else.
- Currencies should use the appropriate currency format.
- Headers should be visually distinct from raw inputs and derived cells.
- Use fill colors, borders, spacing, and merged cells sparingly and intentionally.
- Set row heights and column widths so content is readable without excessive whitespace.
- Do not apply borders around every filled cell.
- Group related calculations and make totals simple sums of the cells above them.
- Add whitespace to separate sections.
- Ensure text does not spill into adjacent cells.
- Avoid unsupported spreadsheet data-table features such as `=TABLE`.

## Color conventions (if no style guidance)
- Blue: user input
- Black: formulas and derived values
- Green: linked or imported values
- Gray: static constants
- Orange: review or caution
- Light red: error or flag
- Purple: control or logic
- Teal: visualization anchors and KPI highlights
