# Responsive Design — ScrollRect & Layout Recipes

## 6. ScrollRect Configuration

```
Horizontal: false, Vertical: true
Movement Type: Elastic, Elasticity: 0.1
Inertia: true, Deceleration: 0.135
Scrollbar Visibility: AutoHideAndExpandViewport
```

**Required structure**: ScrollView → Viewport (Mask/RectMask2D, full stretch) → Content (top-anchor, pivot top, VLG/GLG + ContentSizeFitter)

**Mask vs RectMask2D**: Use RectMask2D for rectangular clips (better perf). Use Mask only for rounded/shaped clips.

## 7. Layout Recipes

### Resource Bar (top)
Top Stretch-H, H=80. HLG spacing=20, Force Expand Width=true, padding 40,40,0,0. Children: LayoutElement flexibleWidth=1.

### Scrollable Card List (middle)
Full Stretch with offsets for header/footer. ScrollView → Viewport (RectMask2D) → Content (VLG spacing=16, ContentSizeFitter vertical=PreferredSize).

### Bottom Tab Bar
Bottom Stretch-H, H=120. HLG spacing=0, Force Expand Width=true. Children: LayoutElement flexibleWidth=1 (center tab=1.5).

### Centered Popup
Center anchor. VLG padding=40,40,30,30, spacing=20. ContentSizeFitter vertical=PreferredSize. Header(80) + Body(flex) + Footer(100).

## 8. Resolution Test Checklist

| Device | Resolution | Check |
|--------|-----------|-------|
| iPhone SE | 750×1334 | Narrow width |
| iPhone 15 | 1179×2556 | Tall + notch |
| Galaxy S24 | 1080×2340 | Android standard |
| iPad Mini | 1488×2266 | Tablet proportions |
| iPad Pro 12.9 | 2048×2732 | Largest tablet |

Verify: no clipping/overlap, touch ≥44pt, safe area, smooth scroll, full bg coverage.
