# HTML to Prefab Patterns

## Table of Contents
- [Button Patterns](#button-patterns)
- [Panel/Card Structures](#panelcard-structures)
- [Form Layouts](#form-layouts)
- [Navigation Patterns](#navigation-patterns)
- [List/Grid Layouts](#listgrid-layouts)
- [Modal/Popup Patterns](#modalpopup-patterns)
- [Tab Systems](#tab-systems)
- [Scroll Content](#scroll-content)
- [Responsive Considerations](#responsive-considerations)

---

## Button Patterns

### Simple Button
**HTML:**
```html
<button class="btn-primary">Play Now</button>
```
**Prefab hierarchy:**
```
Button_PlayNow (Button component)
  └── Text_Label (TextMeshProUGUI: "Play Now")
```
**Configuration:**
- Button: Navigation = None, Transition = ColorTint or SpriteSwap
- RectTransform: Size matches design spec exactly

### Icon + Text Button
**HTML:**
```html
<button class="btn-icon">
  <img src="icon-play.png" />
  <span>Start Game</span>
</button>
```
**Prefab hierarchy:**
```
Button_StartGame (Button, HorizontalLayoutGroup)
  ├── Image_Icon (Image: icon sprite, preserveAspect=true)
  └── Text_Label (TextMeshProUGUI: "Start Game")
```
**Configuration:**
- HorizontalLayoutGroup: spacing from design, childAlignment = MiddleCenter
- ContentSizeFitter on button if auto-sizing needed

### Button Group (row of buttons)
**HTML:**
```html
<div class="button-group">
  <button>Option A</button>
  <button>Option B</button>
  <button>Option C</button>
</div>
```
**Prefab hierarchy:**
```
Panel_ButtonGroup (HorizontalLayoutGroup)
  ├── Button_OptionA (Button)
  │   └── Text_Label
  ├── Button_OptionB (Button)
  │   └── Text_Label
  └── Button_OptionC (Button)
      └── Text_Label
```

---

## Panel/Card Structures

### Simple Card
**HTML:**
```html
<div class="card">
  <img class="card-image" src="hero.png" />
  <div class="card-body">
    <h3>Hero Name</h3>
    <p>Description text here</p>
  </div>
</div>
```
**Prefab hierarchy:**
```
Panel_Card (Image: background, VerticalLayoutGroup)
  ├── Image_CardImage (Image: hero sprite, preserveAspect=true)
  └── Panel_CardBody (VerticalLayoutGroup)
      ├── Text_Title (TextMeshProUGUI: "Hero Name", bold)
      └── Text_Description (TextMeshProUGUI: description)
```

### Card with Header/Footer
**HTML:**
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
  <div class="card-footer">
    <button>Action</button>
  </div>
</div>
```
**Prefab hierarchy:**
```
Panel_Card (Image: bg, VerticalLayoutGroup)
  ├── Panel_Header (Image: header bg)
  │   └── Text_Title
  ├── Panel_Body (VerticalLayoutGroup, padding)
  │   └── Text_Content
  └── Panel_Footer (HorizontalLayoutGroup)
      └── Button_Action
          └── Text_Label
```

---

## Form Layouts

### Input Field
**HTML:**
```html
<div class="form-group">
  <label>Username</label>
  <input type="text" placeholder="Enter username" />
</div>
```
**Prefab hierarchy:**
```
Panel_FormGroup (VerticalLayoutGroup, spacing=4)
  ├── Text_Label (TextMeshProUGUI: "Username")
  └── InputField_Username (TMP_InputField)
      ├── Text Area
      │   ├── Placeholder (TextMeshProUGUI: "Enter username")
      │   └── Text (TextMeshProUGUI)
      └── Image_Background
```

### Form with Multiple Fields
**HTML:**
```html
<form>
  <div class="form-group"><label>Name</label><input /></div>
  <div class="form-group"><label>Email</label><input type="email" /></div>
  <button type="submit">Submit</button>
</form>
```
**Prefab hierarchy:**
```
Panel_Form (VerticalLayoutGroup, spacing=12)
  ├── Panel_FieldName (VerticalLayoutGroup)
  │   ├── Text_LabelName
  │   └── InputField_Name
  ├── Panel_FieldEmail (VerticalLayoutGroup)
  │   ├── Text_LabelEmail
  │   └── InputField_Email
  └── Button_Submit
      └── Text_Label
```

### Toggle/Checkbox
**HTML:**
```html
<label class="checkbox">
  <input type="checkbox" /> Remember me
</label>
```
**Prefab hierarchy:**
```
Toggle_RememberMe (Toggle component)
  ├── Image_Background (Image: checkbox bg)
  │   └── Image_Checkmark (Image: checkmark sprite)
  └── Text_Label (TextMeshProUGUI: "Remember me")
```

### Dropdown/Select
**HTML:**
```html
<select>
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```
**Prefab hierarchy:**
```
Dropdown_Selection (TMP_Dropdown)
  ├── Text_Label (selected value display)
  ├── Image_Arrow (dropdown arrow icon)
  └── Template (ScrollRect - dropdown list template)
      └── Viewport
          └── Content
              └── Item (Toggle)
                  ├── Image_Background
                  ├── Image_Checkmark
                  └── Text_Label
```

---

## Navigation Patterns

### Top Navigation Bar
**HTML:**
```html
<nav class="navbar">
  <div class="nav-brand">Logo</div>
  <div class="nav-items">
    <a href="#" class="active">Home</a>
    <a href="#">Shop</a>
    <a href="#">Profile</a>
  </div>
</nav>
```
**Prefab hierarchy:**
```
Panel_Navbar (Image: bg, HorizontalLayoutGroup)
  ├── Image_Logo (Image: brand logo)
  └── Panel_NavItems (HorizontalLayoutGroup, spacing=16)
      ├── Button_Home (Button, active state styling)
      │   └── Text_Label
      ├── Button_Shop (Button)
      │   └── Text_Label
      └── Button_Profile (Button)
          └── Text_Label
```

### Bottom Tab Bar
**HTML:**
```html
<div class="tab-bar">
  <button class="tab active"><img /><span>Home</span></button>
  <button class="tab"><img /><span>Search</span></button>
  <button class="tab"><img /><span>Settings</span></button>
</div>
```
**Prefab hierarchy:**
```
Panel_TabBar (Image: bg, HorizontalLayoutGroup, childForceExpandWidth=true)
  ├── Button_TabHome (VerticalLayoutGroup, childAlignment=MiddleCenter)
  │   ├── Image_Icon
  │   └── Text_Label
  ├── Button_TabSearch (VerticalLayoutGroup)
  │   ├── Image_Icon
  │   └── Text_Label
  └── Button_TabSettings (VerticalLayoutGroup)
      ├── Image_Icon
      └── Text_Label
```

### Breadcrumb
**HTML:**
```html
<nav class="breadcrumb">
  <a>Home</a> > <a>Category</a> > <span>Current</span>
</nav>
```
**Prefab hierarchy:**
```
Panel_Breadcrumb (HorizontalLayoutGroup, spacing=8)
  ├── Button_Home (TextMeshProUGUI link style)
  ├── Text_Separator (TextMeshProUGUI: ">")
  ├── Button_Category (TextMeshProUGUI link style)
  ├── Text_Separator (TextMeshProUGUI: ">")
  └── Text_Current (TextMeshProUGUI: non-clickable)
```

---

## List/Grid Layouts

### Vertical List
**HTML:**
```html
<ul class="list">
  <li class="list-item">Item 1</li>
  <li class="list-item">Item 2</li>
  <li class="list-item">Item 3</li>
</ul>
```
**Prefab hierarchy:**
```
ScrollView_List (ScrollRect, vertical only)
  └── Viewport (Mask)
      └── Content (VerticalLayoutGroup, ContentSizeFitter: preferredHeight)
          ├── Panel_Item1 (LayoutElement)
          ├── Panel_Item2 (LayoutElement)
          └── Panel_Item3 (LayoutElement)
```

### Grid Layout
**HTML:**
```html
<div class="grid" style="grid-template-columns: repeat(3, 1fr)">
  <div class="grid-item">A</div>
  <div class="grid-item">B</div>
  <!-- ... -->
</div>
```
**Prefab hierarchy:**
```
ScrollView_Grid (ScrollRect)
  └── Viewport (Mask)
      └── Content (GridLayoutGroup)
          ├── Panel_ItemA
          ├── Panel_ItemB
          └── ...
```
**Configuration:**
- GridLayoutGroup: cellSize from design, constraint = FixedColumnCount(3)
- ContentSizeFitter: verticalFit = PreferredSize

---

## Modal/Popup Patterns

### Simple Modal
**HTML:**
```html
<div class="modal-overlay">
  <div class="modal">
    <div class="modal-header">
      <h2>Title</h2>
      <button class="close">&times;</button>
    </div>
    <div class="modal-body">Content here</div>
    <div class="modal-footer">
      <button>Cancel</button>
      <button>Confirm</button>
    </div>
  </div>
</div>
```
**Prefab hierarchy:**
```
Panel_ModalOverlay (Image: semi-transparent black, stretch-all, Button for dismiss)
  └── Panel_Modal (Image: modal bg, centered anchors)
      ├── Panel_Header (HorizontalLayoutGroup)
      │   ├── Text_Title
      │   └── Button_Close
      │       └── Text_X
      ├── Panel_Body (VerticalLayoutGroup, padding)
      │   └── Text_Content
      └── Panel_Footer (HorizontalLayoutGroup, spacing=12)
          ├── Button_Cancel
          │   └── Text_Label
          └── Button_Confirm
              └── Text_Label
```

### Confirmation Dialog
**Prefab hierarchy:**
```
Panel_ConfirmDialog (Image: overlay)
  └── Panel_Dialog (Image: bg, VerticalLayoutGroup)
      ├── Text_Message
      └── Panel_Actions (HorizontalLayoutGroup)
          ├── Button_No
          └── Button_Yes
```

---

## Tab Systems

### Horizontal Tabs
**HTML:**
```html
<div class="tabs">
  <div class="tab-headers">
    <button class="active">Tab 1</button>
    <button>Tab 2</button>
  </div>
  <div class="tab-content">
    <div class="tab-pane active">Content 1</div>
    <div class="tab-pane">Content 2</div>
  </div>
</div>
```
**Prefab hierarchy:**
```
Panel_TabSystem (VerticalLayoutGroup)
  ├── Panel_TabHeaders (HorizontalLayoutGroup)
  │   ├── Toggle_Tab1 (Toggle, ToggleGroup ref, isOn=true)
  │   │   ├── Image_Background
  │   │   └── Text_Label
  │   └── Toggle_Tab2 (Toggle, ToggleGroup ref)
  │       ├── Image_Background
  │       └── Text_Label
  └── Panel_TabContent
      ├── Panel_TabPane1 (active)
      └── Panel_TabPane2 (inactive)
```
**Key:** Use Toggle + ToggleGroup for tab switching. Script controls pane visibility.

---

## Scroll Content

### Scrollable Content Area
**HTML:**
```html
<div class="scroll-container" style="overflow-y: auto; max-height: 400px;">
  <div class="content">Long content here...</div>
</div>
```
**Prefab hierarchy:**
```
ScrollView (ScrollRect, vertical=true, horizontal=false)
  ├── Viewport (RectMask2D)
  │   └── Content (VerticalLayoutGroup, ContentSizeFitter: preferredHeight)
  │       └── ... child elements ...
  └── Scrollbar_Vertical (Scrollbar, direction=BottomToTop)
      └── Sliding Area
          └── Handle (Image)
```

---

## Responsive Considerations

### Anchor Strategies by Element Type

| Element Type | Anchor Pattern | Notes |
|---|---|---|
| Full-screen overlay | Stretch all (0,0)-(1,1) | Covers entire canvas |
| Centered popup | Center (0.5,0.5)-(0.5,0.5) | Fixed size, centered |
| Top bar | Top stretch (0,1)-(1,1) | Full width, fixed height |
| Bottom bar | Bottom stretch (0,1)-(1,0) | Full width, fixed height |
| Side panel | Left/Right stretch | Fixed width, full height |
| Content area | Stretch with offsets | Margins from edges |

### Safe Area Handling
- Always account for device notches/cutouts
- Apply SafeArea offsets to root UI panels
- Test with different aspect ratios (16:9, 18:9, 19.5:9, 4:3)

### Dynamic Content
- Use ContentSizeFitter for text that varies in length
- Use LayoutElement.preferredWidth/Height for fixed-size items in layout groups
- Use flexibleWidth/Height for proportional sizing
