# Design Intelligence -- Industry-to-Design Mapping

Maps product types to complete design recommendations: layout pattern, visual style, color palette, typography, effects, and anti-patterns. Use this to make informed design decisions instead of defaulting to generic blue/white.

## Quick Lookup Table

| Product Type | Style | Palette Name |
|:---|:---|:---|
| SaaS Dashboard | Minimalism | Slate Professional |
| Developer Tool | Dark Mode Premium | Terminal Dark |
| AI / Chatbot | Aurora UI | Nebula Glow |
| API Platform | Brutalism | Ink & Signal |
| Analytics Tool | Bento Grid | Data Calm |
| Banking | Minimalism | Trust Navy |
| Crypto / Fintech | Dark Mode Premium | Midnight Volt |
| Personal Finance | Soft UI | Sage Ledger |
| Invoice / Billing | Editorial | Paper Charcoal |
| Medical Clinic | Minimalism | Clinical Blue |
| Mental Health / Wellness | Soft UI | Calm Lavender |
| Fitness Tracker | Glassmorphism | Energy Pulse |
| General Shop | Minimalism | Commerce Neutral |
| Luxury / Fashion | Editorial | Noir Couture |
| Food Delivery | Claymorphism | Tomato Fresh |
| Marketplace | Bento Grid | Bazaar Warm |
| Beauty / Spa | Soft UI | Blush Petal |
| Restaurant / Cafe | Editorial | Espresso Bean |
| Hotel / Travel Booking | Glassmorphism | Horizon Azure |
| Social Media | Glassmorphism | Pop Spectrum |
| Messaging / Chat | Minimalism | Chat Slate |
| Music / Podcast | Dark Mode Premium | Vinyl Night |
| Video / Streaming | Dark Mode Premium | Cinema Black |
| Task Manager | Minimalism | Focus Stone |
| Note-Taking | Soft UI | Parchment Ink |
| Calendar / Scheduling | Bento Grid | Week Breeze |
| Portfolio / Agency | Brutalism | Studio Mono |
| Photography | Editorial | Gallery Bone |
| E-Learning | Claymorphism | Campus Teal |
| Language Learning | Aurora UI | Polyglot Spark |

## How to Use This File

1. Identify the user's product type from their description
2. Look up the matching entry below
3. Apply the recommended style, palette, typography, and anti-patterns
4. If no exact match, pick the closest category
5. The palette hex values map to CSS variables: primary, accent, surface (background), and text
6. Cross-reference `css-system.md` for the base 6 palettes (Slate, Ocean, Forest, Sunset, Berry, Rose) -- entries here extend beyond those

---

## Tech and SaaS

### SaaS Dashboard
- **Pattern**: Sidebar + Header + Content Grid with KPI cards at top
- **Style**: Minimalism
- **Palette**: Primary: #2563eb, Accent: #10b981, Surface: #f8fafc, Text: #1e293b (Slate Professional)
- **Typography**: Heading: Inter (600-700), Body: Inter (400-500). Mood: Clean, systematic, no-nonsense
- **Key Effects**: Subtle card shadows (0 1px 3px rgba(0,0,0,.08)), 1px borders, smooth hover lifts
- **Anti-Patterns**: Avoid decorative gradients, rounded blob shapes, and playful illustrations -- SaaS users want density and clarity
- **Navigation**: Collapsible sidebar with icon+label, top bar for user/search

### Developer Tool
- **Pattern**: Split pane (sidebar tree + main editor/content area) with command palette
- **Style**: Dark Mode Premium
- **Palette**: Primary: #a78bfa, Accent: #34d399, Surface: #0f172a, Text: #e2e8f0 (Terminal Dark)
- **Typography**: Heading: JetBrains Mono (700), Body: IBM Plex Sans (400). Mood: Technical, precise, code-native
- **Key Effects**: Monospace code blocks with syntax highlighting tones, subtle glow on active elements, sharp 1px borders
- **Anti-Patterns**: Avoid soft rounded corners, pastel colors, large hero images -- developers expect information density and keyboard-first design
- **Navigation**: Tab bar or sidebar tree, command palette (Cmd+K), breadcrumbs

### AI / Chatbot
- **Pattern**: Chat thread (messages list + input bar) with optional side panel for settings/history
- **Style**: Aurora UI
- **Palette**: Primary: #6366f1, Accent: #a855f7, Surface: #0f0b1a, Text: #e0e7ff (Nebula Glow)
- **Typography**: Heading: Space Grotesk (600), Body: DM Sans (400). Mood: Futuristic yet approachable
- **Key Effects**: Gradient mesh background (subtle), typing indicator pulse, message fade-in animation
- **Anti-Patterns**: Avoid robotic/cold aesthetics, overly dark themes without accent relief, walls of monospace text -- chat UIs need warmth and rhythm
- **Navigation**: Conversation list sidebar, inline settings, floating action for new chat

### API Platform
- **Pattern**: Documentation layout -- sidebar nav + content area with code examples and endpoint tables
- **Style**: Brutalism
- **Palette**: Primary: #18181b, Accent: #f59e0b, Surface: #fafaf9, Text: #1c1917 (Ink & Signal)
- **Typography**: Heading: Space Mono (700), Body: Source Sans 3 (400). Mood: Direct, utilitarian, high-signal
- **Key Effects**: Hard shadows (4px 4px 0 #18181b), thick borders (2-3px), monospace code blocks with yellow highlights
- **Anti-Patterns**: Avoid gradients, rounded cards, decorative imagery -- API docs need scannable structure, not visual flair
- **Navigation**: Sticky sidebar with section anchors, top version selector, search bar

### Analytics Tool
- **Pattern**: Bento grid of chart cards with filters bar at top, expandable detail panels
- **Style**: Bento Grid
- **Palette**: Primary: #0369a1, Accent: #0d9488, Surface: #f1f5f9, Text: #334155 (Data Calm)
- **Typography**: Heading: Plus Jakarta Sans (600), Body: Inter (400). Mood: Data-focused, structured, readable
- **Key Effects**: Chart container cards with subtle shadow, color-coded data series, smooth number transitions
- **Anti-Patterns**: Avoid 3D charts, excessive chart types on one page, rainbow color scales -- analytics needs consistency and legibility at a glance
- **Navigation**: Top tabs for views/date ranges, sidebar for saved reports

---

## Finance

### Banking
- **Pattern**: Hero balance card + Transaction list + Quick actions grid
- **Style**: Minimalism
- **Palette**: Primary: #1e3a5f, Accent: #047857, Surface: #f7f9fb, Text: #1a2332 (Trust Navy)
- **Typography**: Heading: DM Sans (600-700), Body: DM Sans (400). Mood: Trustworthy, stable, institutional
- **Key Effects**: Balance card with subtle gradient (#1e3a5f to #2d5a87), crisp dividers, green/red for +/- amounts
- **Anti-Patterns**: Avoid neon accents, playful rounded shapes, casual typefaces -- banking apps need gravitas and precision
- **Navigation**: Bottom tabs (Home, Cards, Transfers, More), top greeting bar

### Crypto / Fintech
- **Pattern**: Portfolio summary hero + Live price ticker + Holdings list + Chart panel
- **Style**: Dark Mode Premium
- **Palette**: Primary: #00d4aa, Accent: #8b5cf6, Surface: #09090b, Text: #fafafa (Midnight Volt)
- **Typography**: Heading: Outfit (700), Body: Inter (400). Mood: Bold, modern, high-energy
- **Key Effects**: Animated sparkline charts, green/red price change badges, glowing active tab indicator
- **Anti-Patterns**: Avoid light/airy themes, serif fonts, slow transitions -- crypto users expect real-time energy and dark interfaces
- **Navigation**: Bottom tabs with portfolio/markets/trade/wallet, pull-to-refresh

### Personal Finance
- **Pattern**: Monthly overview card + Budget category progress bars + Recent transactions
- **Style**: Soft UI
- **Palette**: Primary: #4a7c59, Accent: #d97706, Surface: #f5f1eb, Text: #3d3929 (Sage Ledger)
- **Typography**: Heading: Nunito (700), Body: Nunito (400). Mood: Warm, approachable, encouraging
- **Key Effects**: Soft inset shadows on budget bars, rounded progress indicators, gentle color transitions
- **Anti-Patterns**: Avoid harsh reds for overspending (use muted amber), complex data tables, financial jargon in UI labels -- personal finance should feel empowering, not stressful
- **Navigation**: Bottom tabs (Overview, Budgets, Transactions, Goals)

### Invoice / Billing
- **Pattern**: Invoice list with status badges + Detail view with line items table + Create form
- **Style**: Editorial
- **Palette**: Primary: #374151, Accent: #2563eb, Surface: #ffffff, Text: #111827 (Paper Charcoal)
- **Typography**: Heading: Literata (600), Body: Source Sans 3 (400). Mood: Professional, paper-like, precise
- **Key Effects**: Paper-white cards with thin borders, status pills (paid/pending/overdue), clean table rows with hover highlight
- **Anti-Patterns**: Avoid colorful themes, playful icons, rounded cards -- invoicing needs a professional, document-like aesthetic
- **Navigation**: Top tabs (All, Drafts, Sent, Paid), sidebar for clients/settings

---

## Healthcare

### Medical Clinic
- **Pattern**: Appointment card (next visit) + Doctor list + Services grid + Book flow
- **Style**: Minimalism
- **Palette**: Primary: #0c6291, Accent: #38b2ac, Surface: #f0f7fa, Text: #1a3344 (Clinical Blue)
- **Typography**: Heading: Poppins (600), Body: Open Sans (400). Mood: Clean, clinical, reassuring
- **Key Effects**: White cards with soft blue borders, doctor avatar circles, calendar date picker with blue highlight
- **Anti-Patterns**: Avoid dark themes, aggressive colors (red/orange as primary), stock photo grids -- medical apps need to feel safe and calming
- **Navigation**: Bottom tabs (Home, Appointments, Doctors, Profile)

### Mental Health / Wellness
- **Pattern**: Daily check-in mood picker + Journal entry + Meditation/exercise cards + Progress chart
- **Style**: Soft UI
- **Palette**: Primary: #7c6bb5, Accent: #e8927c, Surface: #f4f0f9, Text: #3b3252 (Calm Lavender)
- **Typography**: Heading: Quicksand (600), Body: Quicksand (400). Mood: Gentle, calming, personal
- **Key Effects**: Neumorphic mood buttons, soft gradients on hero sections, breathing animation circles
- **Anti-Patterns**: Avoid sharp edges, bright saturated colors, data-heavy dashboards, clinical/sterile aesthetics -- wellness apps should feel like a warm, private space
- **Navigation**: Bottom tabs (Today, Journal, Meditate, Progress), minimal top bar

### Fitness Tracker
- **Pattern**: Today's stats ring/arc + Activity feed + Workout cards + Leaderboard
- **Style**: Glassmorphism
- **Palette**: Primary: #ef4444, Accent: #f97316, Surface: #1a1a2e, Text: #f1f5f9 (Energy Pulse)
- **Typography**: Heading: Bebas Neue (400), Body: Roboto (400). Mood: Energetic, motivating, athletic
- **Key Effects**: Frosted glass cards over dark gradient, circular progress rings with glow, bold stat numbers
- **Anti-Patterns**: Avoid pastel softness, thin fonts, excessive whitespace -- fitness apps need energy, bold typography, and visual momentum
- **Navigation**: Bottom tabs (Today, Workouts, Social, Profile), floating start-workout button

---

## E-Commerce

### General Shop
- **Pattern**: Hero banner + Category grid + Product cards (image, title, price, rating) + Cart
- **Style**: Minimalism
- **Palette**: Primary: #171717, Accent: #dc2626, Surface: #ffffff, Text: #262626 (Commerce Neutral)
- **Typography**: Heading: Plus Jakarta Sans (700), Body: Inter (400). Mood: Modern, trustworthy, conversion-focused
- **Key Effects**: Product card hover scale (1.02), add-to-cart micro-animation, skeleton loading states
- **Anti-Patterns**: Avoid text-heavy layouts, small product images, hidden prices, auto-playing carousels -- shoppers need fast scanning and immediate price visibility
- **Navigation**: Bottom tabs (Home, Categories, Cart, Account), sticky search bar

### Luxury / Fashion
- **Pattern**: Full-bleed editorial hero + Lookbook grid + Product detail with large imagery + Minimal cart
- **Style**: Editorial
- **Palette**: Primary: #1a1a1a, Accent: #a3865b, Surface: #faf8f5, Text: #1a1a1a (Noir Couture)
- **Typography**: Heading: Playfair Display (700), Body: Lato (300-400). Mood: Elegant, editorial, aspirational
- **Key Effects**: Parallax-style image scroll, gold accent on CTAs, letter-spaced uppercase labels, generous whitespace
- **Anti-Patterns**: Avoid bright colors, busy layouts, star ratings prominently displayed, discount badges -- luxury needs restraint, space, and sophistication
- **Navigation**: Hamburger or minimal top nav, no bottom tabs -- keep chrome minimal

### Food Delivery
- **Pattern**: Location header + Restaurant cards with time/rating + Menu list + Cart drawer + Order tracking
- **Style**: Claymorphism
- **Palette**: Primary: #dc2626, Accent: #f59e0b, Surface: #fffbf0, Text: #292524 (Tomato Fresh)
- **Typography**: Heading: Fredoka (600), Body: Nunito Sans (400). Mood: Friendly, appetizing, fast
- **Key Effects**: Soft puffy card shadows, food item cards with rounded corners (16px), bouncy add-to-cart animation
- **Anti-Patterns**: Avoid dark themes, thin/elegant typography, minimalist imagery -- food apps need warmth, color, and mouth-watering presentation
- **Navigation**: Bottom tabs (Home, Search, Orders, Account), sticky cart summary bar

### Marketplace
- **Pattern**: Category bento grid + Product/listing cards with seller info + Filter sidebar/sheet + Detail with reviews
- **Style**: Bento Grid
- **Palette**: Primary: #b45309, Accent: #0f766e, Surface: #faf7f2, Text: #1c1917 (Bazaar Warm)
- **Typography**: Heading: Sora (600), Body: Karla (400). Mood: Diverse, bustling, trustworthy
- **Key Effects**: Category tiles with icon+color background, trust badges, multi-image product carousels
- **Anti-Patterns**: Avoid monochrome palettes, single-column layouts, hiding seller info -- marketplaces need visual variety and trust signals
- **Navigation**: Top search bar, bottom tabs (Home, Categories, Sell, Messages, Profile)

---

## Services

### Beauty / Spa
- **Pattern**: Featured treatment hero + Service menu cards + Stylist profiles + Booking calendar
- **Style**: Soft UI
- **Palette**: Primary: #c2657a, Accent: #d4a574, Surface: #fdf2f0, Text: #4a2c3d (Blush Petal)
- **Typography**: Heading: Cormorant Garamond (600), Body: Lato (400). Mood: Luxurious, feminine, serene
- **Key Effects**: Soft neumorphic service cards, rose-toned gradients, circular stylist avatars with soft shadow
- **Anti-Patterns**: Avoid sharp/techy aesthetics, dark modes, bold primary colors, dense information grids -- spa booking needs to feel relaxing before you arrive
- **Navigation**: Bottom tabs (Home, Services, Book, Profile), calendar drawer

### Restaurant / Cafe
- **Pattern**: Hero image + Hours/location card + Menu sections (starters, mains, drinks) + Reservation form
- **Style**: Editorial
- **Palette**: Primary: #3e2723, Accent: #c0793e, Surface: #faf6f1, Text: #2c1810 (Espresso Bean)
- **Typography**: Heading: Playfair Display (700), Body: Source Serif 4 (400). Mood: Artisanal, warm, inviting
- **Key Effects**: Menu items with em-dash dividers, serif headings with generous line-height, warm-toned food photography placeholders
- **Anti-Patterns**: Avoid tech-startup aesthetics, blue color schemes, complex navigation hierarchies, small text -- restaurant apps should feel like reading a well-designed physical menu
- **Navigation**: Scrolling single-page with sticky section tabs (Menu, Reserve, About, Contact)

### Hotel / Travel Booking
- **Pattern**: Destination search hero + Property cards (image, rating, price/night) + Date picker + Detail with gallery + Booking flow
- **Style**: Glassmorphism
- **Palette**: Primary: #0369a1, Accent: #f97316, Surface: #f0f9ff, Text: #0c4a6e (Horizon Azure)
- **Typography**: Heading: Outfit (600-700), Body: Nunito Sans (400). Mood: Aspirational, open, adventure-ready
- **Key Effects**: Frosted glass search bar over hero image, destination cards with parallax tilt, calendar with highlighted date range
- **Anti-Patterns**: Avoid text-heavy listings without imagery, dark/moody themes, small property images -- travel booking sells through visuals and aspiration
- **Navigation**: Top search bar, bottom tabs (Explore, Trips, Saved, Profile)

---

## Social and Content

### Social Media
- **Pattern**: Feed of cards (avatar + content + engagement bar) + Stories row + Create post FAB + Profile grid
- **Style**: Glassmorphism
- **Palette**: Primary: #4f46e5, Accent: #ec4899, Surface: #f8faff, Text: #1e1b4b (Pop Spectrum)
- **Typography**: Heading: Plus Jakarta Sans (700), Body: DM Sans (400). Mood: Vibrant, social, expressive
- **Key Effects**: Frosted glass story circles, heart animation on double-tap, smooth pull-to-refresh, avatar ring gradients
- **Anti-Patterns**: Avoid corporate/formal aesthetics, monotone palettes, dense text layouts -- social apps thrive on visual energy and personality
- **Navigation**: Bottom tabs (Feed, Search, Create, Notifications, Profile), modal for create

### Messaging / Chat
- **Pattern**: Conversation list (avatar + last message + timestamp) + Chat thread (bubbles + input) + Contact profile
- **Style**: Minimalism
- **Palette**: Primary: #2563eb, Accent: #64748b, Surface: #ffffff, Text: #0f172a (Chat Slate)
- **Typography**: Heading: Inter (600), Body: Inter (400). Mood: Fast, functional, invisible design
- **Key Effects**: Message bubbles with tail, typing indicator dots, read receipts, smooth keyboard push animation
- **Anti-Patterns**: Avoid heavy visual themes, complex navigation, decorative elements between messages -- messaging UI should be invisible, letting content breathe
- **Navigation**: Tab bar (Chats, Calls, Contacts, Settings), swipe actions on conversation rows

### Music / Podcast
- **Pattern**: Now-playing bar (persistent) + Browse/home grid + Playlist detail + Full-screen player with artwork
- **Style**: Dark Mode Premium
- **Palette**: Primary: #22c55e, Accent: #a78bfa, Surface: #121212, Text: #e5e5e5 (Vinyl Night)
- **Typography**: Heading: Montserrat (700), Body: Figtree (400). Mood: Immersive, moody, rhythm-aware
- **Key Effects**: Album art color extraction for player background, progress bar glow, vinyl-spin animation on play
- **Anti-Patterns**: Avoid light themes as default, small album art, text-heavy layouts without visual anchors -- music apps sell through album art and immersive playback
- **Navigation**: Bottom tabs (Home, Search, Library, Premium), persistent mini-player above tabs

### Video / Streaming
- **Pattern**: Hero spotlight + Continue watching row + Category rows (horizontal scroll) + Video player fullscreen
- **Style**: Dark Mode Premium
- **Palette**: Primary: #e50914, Accent: #fafafa, Surface: #141414, Text: #e5e5e5 (Cinema Black)
- **Typography**: Heading: Archivo (700), Body: Roboto (400). Mood: Cinematic, immersive, binge-worthy
- **Key Effects**: Auto-playing hero trailer, horizontal scroll card rows with hover preview, smooth player expand/collapse
- **Anti-Patterns**: Avoid white backgrounds, small thumbnails, list-based layouts without visual hierarchy -- streaming apps are visual-first, content-discovery engines
- **Navigation**: Top tabs (Home, New, My List, Downloads), profile switcher

---

## Productivity

### Task Manager
- **Pattern**: Task list with checkboxes + Project/board columns (kanban) + Quick-add bar + Due date grouping
- **Style**: Minimalism
- **Palette**: Primary: #57534e, Accent: #7c3aed, Surface: #fafaf9, Text: #1c1917 (Focus Stone)
- **Typography**: Heading: Inter (600), Body: Inter (400). Mood: Focused, distraction-free, productive
- **Key Effects**: Checkbox strike-through animation, smooth drag-and-drop placeholders, priority color dots (red/amber/blue)
- **Anti-Patterns**: Avoid decorative elements, gamification badges on the main view, complex onboarding -- task managers need zero friction between thinking and capturing
- **Navigation**: Sidebar (projects/labels), top view switcher (list/board/calendar)

### Note-Taking
- **Pattern**: Note list sidebar + Editor canvas (rich text) + Folder/tag organization + Search
- **Style**: Soft UI
- **Palette**: Primary: #44403c, Accent: #0891b2, Surface: #fdfcfb, Text: #292524 (Parchment Ink)
- **Typography**: Heading: Merriweather (700), Body: Source Serif 4 (400). Mood: Thoughtful, literary, focused writing
- **Key Effects**: Paper-texture background (subtle CSS noise), soft inset editor area, smooth note list transitions
- **Anti-Patterns**: Avoid bright colors competing with content, complex toolbars visible by default, grid layouts for notes -- note apps should feel like a blank page, not a dashboard
- **Navigation**: Sidebar (notebooks/tags), top toolbar (format/share), Cmd+K search

### Calendar / Scheduling
- **Pattern**: Month/week/day toggle views + Event cards with color coding + Quick-create modal + Agenda list
- **Style**: Bento Grid
- **Palette**: Primary: #1d4ed8, Accent: #f43f5e, Surface: #f5f7ff, Text: #1e293b (Week Breeze)
- **Typography**: Heading: Outfit (600), Body: Inter (400). Mood: Organized, time-aware, structured
- **Key Effects**: Color-coded event blocks, smooth view transitions (month to week), today highlight ring, drag-to-create
- **Anti-Patterns**: Avoid cramming too many events visually, using only text (no color blocks), hiding the current time indicator -- calendars need instant temporal orientation
- **Navigation**: Top view switcher (Day/Week/Month), sidebar for calendars/filters

---

## Creative

### Portfolio / Agency
- **Pattern**: Full-screen project hero + Project grid/masonry + About section + Contact form
- **Style**: Brutalism
- **Palette**: Primary: #18181b, Accent: #facc15, Surface: #fafafa, Text: #09090b (Studio Mono)
- **Typography**: Heading: Space Grotesk (700), Body: Work Sans (400). Mood: Bold, confident, design-forward
- **Key Effects**: Hard geometric shapes, oversized typography for project titles, cursor-follow interactions, high contrast
- **Anti-Patterns**: Avoid safe/corporate templates, stock imagery, cookie-cutter card grids, blue primary colors -- portfolios must demonstrate design taste, not template defaults
- **Navigation**: Horizontal top nav or hamburger, no bottom tabs -- content is the navigation

### Photography
- **Pattern**: Full-bleed gallery grid (masonry) + Lightbox overlay + About/bio + Contact
- **Style**: Editorial
- **Palette**: Primary: #292524, Accent: #a8a29e, Surface: #faf9f7, Text: #1c1917 (Gallery Bone)
- **Typography**: Heading: Cormorant Garamond (500), Body: Jost (300). Mood: Minimal, gallery-like, images speak
- **Key Effects**: Masonry layout with subtle hover zoom, lightbox with smooth fade, generous padding around images
- **Anti-Patterns**: Avoid colorful UI elements competing with photos, busy navigation, watermark-heavy overlays, small thumbnails -- photography portfolios must let the work breathe
- **Navigation**: Minimal top nav (Gallery, About, Contact), no bottom chrome

---

## Education

### E-Learning
- **Pattern**: Course catalog cards + Lesson list with progress + Video player + Quiz/exercise panel + Certificate
- **Style**: Claymorphism
- **Palette**: Primary: #0d7377, Accent: #f59e0b, Surface: #f0fafb, Text: #134e4a (Campus Teal)
- **Typography**: Heading: Poppins (600), Body: Nunito (400). Mood: Friendly, structured, encouraging
- **Key Effects**: Puffy course cards with rounded corners, progress bars with milestone markers, confetti on completion
- **Anti-Patterns**: Avoid overwhelming dashboards, tiny text on mobile, corporate training aesthetics, hiding progress -- learners need constant feedback on where they are
- **Navigation**: Bottom tabs (Learn, My Courses, Explore, Profile), lesson sidebar for course detail

### Language Learning
- **Pattern**: Daily streak/progress hero + Lesson cards (levels/units) + Practice exercise (multiple choice, fill-blank) + Leaderboard
- **Style**: Aurora UI
- **Palette**: Primary: #7c3aed, Accent: #06b6d4, Surface: #faf5ff, Text: #2e1065 (Polyglot Spark)
- **Typography**: Heading: Fredoka (600), Body: Nunito (400). Mood: Playful, gamified, motivating
- **Key Effects**: Gradient mesh hero, XP progress animations, streak flame icon with pulse, level-up celebration overlay
- **Anti-Patterns**: Avoid academic/textbook aesthetics, dense vocabulary lists without visual context, removing gamification elements -- language apps thrive on dopamine loops and daily habit reinforcement
- **Navigation**: Bottom tabs (Home, Practice, Leaderboard, Profile), top streak counter

---

## Style Glossary

**Minimalism**: Maximum clarity through reduction. Generous whitespace, limited color palette, thin borders or none, typography-driven hierarchy. No decoration that does not serve function.

**Glassmorphism**: Frosted glass effect using `backdrop-filter: blur()` with semi-transparent backgrounds. Layered depth, light borders, works best on colorful or image backgrounds.

**Neumorphism**: Soft extruded shapes using dual box-shadows (light + dark) on a flat background. Creates a "pressed into clay" feel. Use sparingly -- poor contrast if overdone.

**Brutalism**: Raw, bold, intentionally unpolished. Thick borders, hard shadows, monospace type, high contrast. Rejects conventional beauty for directness and personality.

**Soft UI**: Gentle aesthetic with rounded corners (12-20px), muted colors, soft shadows, and warm tones. Related to neumorphism but with better contrast and more color variety.

**Bento Grid**: Content organized in a grid of varying-sized rectangular tiles (like a bento box). Each tile is a self-contained unit. Clean gaps between tiles, consistent padding within.

**Dark Mode Premium**: Dark backgrounds (#09-#14 range) with high-contrast accents. Conveys sophistication, reduces eye strain, makes colors pop. Requires careful contrast ratios for accessibility.

**Claymorphism**: Soft, puffy, 3D-like elements with rounded corners and colorful shadows. Feels tactile and playful. Good for consumer apps targeting broad audiences.

**Aurora UI**: Gradient mesh backgrounds with soft color transitions (often purple/blue/green). Feels futuristic and dynamic. Use as subtle background, not overwhelming.

**Editorial / Magazine**: Typography-driven layouts inspired by print design. Serif headings, generous line-height, column-based content, large pull quotes. Conveys authority and craftsmanship.

**Retro / Y2K**: Nostalgic throwback with chunky shapes, bright colors, pixel-adjacent elements, playful gradients, and 2000s-era web aesthetics. Use for entertainment or youth-targeted products.
