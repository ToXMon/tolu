# Style Presets Reference

Curated visual styles for Frontend Slides. Each preset is inspired by real design references — no generic "AI slop" aesthetics. **Abstract shapes only — no illustrations.**

**Viewport CSS:** For mandatory base styles, see [viewport-base.css](viewport-base.css). Include in every presentation.

---

## Dark Themes

### 1. Bold Signal

**Vibe:** Confident, bold, modern, high-impact

**Layout:** Colored card on dark gradient. Number top-left, navigation top-right, title bottom-left.

**Typography:**
- Display: `Archivo Black` (900)
- Body: `Space Grotesk` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
}
```

**Signature Elements:**
- Bold colored card as focal point (orange, coral, or vibrant accent)
- Large section numbers (01, 02, etc.)
- Navigation breadcrumbs with active/inactive opacity states
- Grid-based layout for precise alignment

---

### 2. Electric Studio

**Vibe:** Bold, clean, professional, high contrast

**Layout:** Split panel—white top, blue bottom. Brand marks in corners.

**Typography:**
- Display: `Manrope` (800)
- Body: `Manrope` (400/500)

**Colors:**
```css
:root {
    --bg-dark: #0a0a0a;
    --bg-white: #ffffff;
    --accent-blue: #4361ee;
    --text-dark: #0a0a0a;
    --text-light: #ffffff;
}
```

**Signature Elements:**
- Two-panel vertical split
- Accent bar on panel edge
- Quote typography as hero element
- Minimal, confident spacing

---

### 3. Creative Voltage

**Vibe:** Bold, creative, energetic, retro-modern

**Layout:** Split panels—electric blue left, dark right. Script accents.

**Typography:**
- Display: `Syne` (700/800)
- Mono: `Space Mono` (400/700)

**Colors:**
```css
:root {
    --bg-primary: #0066ff;
    --bg-dark: #1a1a2e;
    --accent-neon: #d4ff00;
    --text-light: #ffffff;
}
```

**Signature Elements:**
- Electric blue + neon yellow contrast
- Halftone texture patterns
- Neon badges/callouts
- Script typography for creative flair

---

### 4. Dark Botanical

**Vibe:** Elegant, sophisticated, artistic, premium

**Layout:** Centered content on dark. Abstract soft shapes in corner.

**Typography:**
- Display: `Cormorant` (400/600) — elegant serif
- Body: `IBM Plex Sans` (300/400)

**Colors:**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;
}
```

**Signature Elements:**
- Abstract soft gradient circles (blurred, overlapping)
- Warm color accents (pink, gold, terracotta)
- Thin vertical accent lines
- Italic signature typography
- **No illustrations—only abstract CSS shapes**

---

## Light Themes

### 5. Notebook Tabs

**Vibe:** Editorial, organized, elegant, tactile

**Layout:** Cream paper card on dark background. Colorful tabs on right edge.

**Typography:**
- Display: `Bodoni Moda` (400/700) — classic editorial
- Body: `DM Sans` (400/500)

**Colors:**
```css
:root {
    --bg-outer: #2d2d2d;
    --bg-page: #f8f6f1;
    --text-primary: #1a1a1a;
    --tab-1: #98d4bb; /* Mint */
    --tab-2: #c7b8ea; /* Lavender */
    --tab-3: #f4b8c5; /* Pink */
    --tab-4: #a8d8ea; /* Sky */
    --tab-5: #ffe6a7; /* Cream */
}
```

**Signature Elements:**
- Paper container with subtle shadow
- Colorful section tabs on right edge (vertical text)
- Binder hole decorations on left
- Tab text must scale with viewport: `font-size: clamp(0.5rem, 1vh, 0.7rem)`

---

### 6. Pastel Geometry

**Vibe:** Friendly, organized, modern, approachable

**Layout:** White card on pastel background. Vertical pills on right edge.

**Typography:**
- Display: `Plus Jakarta Sans` (700/800)
- Body: `Plus Jakarta Sans` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #c8d9e6;
    --card-bg: #faf9f7;
    --pill-pink: #f0b4d4;
    --pill-mint: #a8d4c4;
    --pill-sage: #5a7c6a;
    --pill-lavender: #9b8dc4;
    --pill-violet: #7c6aad;
}
```

**Signature Elements:**
- Rounded card with soft shadow
- **Vertical pills on right edge** with varying heights (like tabs)
- Consistent pill width, heights: short → medium → tall → medium → short
- Download/action icon in corner

---

### 7. Split Pastel

**Vibe:** Playful, modern, friendly, creative

**Layout:** Two-color vertical split (peach left, lavender right).

**Typography:**
- Display: `Outfit` (700/800)
- Body: `Outfit` (400/500)

**Colors:**
```css
:root {
    --bg-peach: #f5e6dc;
    --bg-lavender: #e4dff0;
    --text-dark: #1a1a1a;
    --badge-mint: #c8f0d8;
    --badge-yellow: #f0f0c8;
    --badge-pink: #f0d4e0;
}
```

**Signature Elements:**
- Split background colors
- Playful badge pills with icons
- Grid pattern overlay on right panel
- Rounded CTA buttons

---

### 8. Vintage Editorial

**Vibe:** Witty, confident, editorial, personality-driven

**Layout:** Centered content on cream. Abstract geometric shapes as accent.

**Typography:**
- Display: `Fraunces` (700/900) — distinctive serif
- Body: `Work Sans` (400/500)

**Colors:**
```css
:root {
    --bg-cream: #f5f3ee;
    --text-primary: #1a1a1a;
    --text-secondary: #555;
    --accent-warm: #e8d4c0;
}
```

**Signature Elements:**
- Abstract geometric shapes (circle outline + line + dot)
- Bold bordered CTA boxes
- Witty, conversational copy style
- **No illustrations—only geometric CSS shapes**

## Brand Systems

### 13. JNJ JJIM (Johnson & Johnson Internal)

**Vibe:** Professional, clean, authoritative, on-brand corporate

**Layout:** Widescreen 16:9. Left-aligned content. White or light gray backgrounds. Red accent bars/headers. Structured grid with generous whitespace.

**Typography:**
- Display: `Johnson Display` (proprietary) — Google Fonts fallback: `Outfit` (600/700)
- Body: `Johnson Text` (proprietary) — Google Fonts fallback: `Nunito Sans` (400/500)
- **Minimum 10pt for chart text. Titles always larger.**

**Colors:**
```css
:root {
    /* Primary brand */
    --jj-red: #EB1700;          /* J&J Red — titles/headers ONLY, never body text */
    --jj-black: #000000;        /* Primary text */
    --jj-white: #FFFFFF;        /* Backgrounds, chart backgrounds */
    --jj-bg-light: #F1EFED;     /* Light gray slide background (contrast for white images) */

    /* Warm grays */
    --jj-gray-warm: #C4BDB6;    /* Neutral accent, borders */
    --jj-gray-mid: #D5CFC9;     /* Subtle backgrounds */
    --jj-gray-tone: #A39992;    /* Secondary neutral */
    --jj-brown: #6E6159;        /* Dark neutral accent */

    /* Data visualization (fixed order for accessibility) */
    --jj-chart-1: #EB1700;      /* Red */
    --jj-chart-2: #000000;      /* Black */
    --jj-chart-3: #C4BDB6;      /* Warm gray */
    --jj-chart-4: #004686;      /* Dark blue — data viz only */
    --jj-chart-5: #68D2FF;      /* Light blue — data viz only */
    --jj-chart-6: #541981;      /* Purple */
}
```

**Chart Color Rules (DO NOT REORDER):**
1. Apply chart colors in exact sequence: `--jj-chart-1` through `--jj-chart-6`
2. White outline (`1.5pt solid white`) around all data elements
3. Gridlines: `0.75pt medium gray` (#A0A0A0)
4. Axis titles: ON when relevant
5. Labels: centered, black, readable
6. Blues (`--jj-chart-4`, `--jj-chart-5`) for data visualization ONLY
7. Chart backgrounds: always white

**Signature Elements:**
- Red accent bar or band for section headers (not body text)
- Clean left-aligned layouts with consistent spacing guides
- White card containers on light gray (`#F1EFED`) backgrounds
- Subtle warm gray borders and dividers
- Data visualizations with white-outlined elements on white backgrounds
- Minimal icon usage — black default, red emphasis, white on red backgrounds only

**Accessibility Requirements:**
- Visuals understood at a glance, never by color alone
- Alt text on every image (include suggested alt-text line per visual)
- Separate charts for comparison instead of relying on many colors
- Minimum 10pt for all chart-adjacent text
- High contrast: white/gray backgrounds with dark text

**Slide Layouts (from JJIM template — 56 layouts):**

| Layout Type | Variants |
|-------------|----------|
| Title | Standard, Accessible, With Image, With Panel Images |
| Section Header | Standard, With Panel, Red with Panel, Gray, With Full Image, With Full Dark Image, Red with Image, With Image |
| Agenda | 3 variants with icon grid patterns |
| Key Statement | Single focused statement |
| Key Numbers | Standard + Accessible (4-up metric cards with icons) |
| Quote | Standard + Accessible |
| Content | Title + Right Content, Title + Content, Two Content, Three Content, Four Content, Eight Content |
| Content + Images | Three Images + Text, Four Content with Images, Image + Caption, Image + Content, Image Right Side, Two/Three Images + Content |
| Chart | Text + Chart, Three Chart |
| Table | Standard table layout |
| Team | 1, 1-2, 3, 4, 6, 12 person grids |
| Timeline | Multi-point horizontal timeline |
| End | Standard + Accessible |

**Icon Rules (STRICT):**
- Only approved icons from J&J brand library
- Colors: black (default), J&J red (#EB1700, emphasis), white on red backgrounds
- Prefer SVG/PNG format

**Internal vs External Guardrail:**
- This JJIM system is for INTERNAL Johnson & Johnson / JJIM audiences
- For external or executive corporate forums, use official J&J corporate templates instead

---

## Specialty Themes

### 14. Neon Cyber

**Vibe:** Futuristic, techy, confident

**Typography:** `Clash Display` + `Satoshi` (Fontshare)

**Colors:** Deep navy (#0a0f1c), cyan accent (#00ffcc), magenta (#ff00aa)

**Signature:** Particle backgrounds, neon glow, grid patterns

---

### 15. Terminal Green

**Vibe:** Developer-focused, hacker aesthetic

**Typography:** `JetBrains Mono` (monospace only)

**Colors:** GitHub dark (#0d1117), terminal green (#39d353)

**Signature:** Scan lines, blinking cursor, code syntax styling

---

### 16. Swiss Modern

**Vibe:** Clean, precise, Bauhaus-inspired

**Typography:** `Archivo` (800) + `Nunito` (400)

**Colors:** Pure white, pure black, red accent (#ff3300)

**Signature:** Visible grid, asymmetric layouts, geometric shapes

---

### 17. Paper & Ink

**Vibe:** Editorial, literary, thoughtful

**Typography:** `Cormorant Garamond` + `Source Serif 4`

**Colors:** Warm cream (#faf9f7), charcoal (#1a1a1a), crimson accent (#c41e3a)

**Signature:** Drop caps, pull quotes, elegant horizontal rules

---

## Font Pairing Quick Reference

| Preset | Display Font | Body Font | Source |
|--------|--------------|-----------|--------|
| Bold Signal | Archivo Black | Space Grotesk | Google |
| Electric Studio | Manrope | Manrope | Google |
| Creative Voltage | Syne | Space Mono | Google |
| Dark Botanical | Cormorant | IBM Plex Sans | Google |
| Notebook Tabs | Bodoni Moda | DM Sans | Google |
| Pastel Geometry | Plus Jakarta Sans | Plus Jakarta Sans | Google |
| Split Pastel | Outfit | Outfit | Google |
| Vintage Editorial | Fraunces | Work Sans | Google |
| JNJ JJIM | Johnson Display | Johnson Text | Proprietary (fallback: Outfit + Nunito Sans) |
| Neon Cyber | Clash Display | Satoshi | Fontshare |
| Terminal Green | JetBrains Mono | JetBrains Mono | JetBrains |
---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Inter, Roboto, Arial, system fonts as display

**Colors:** `#6366f1` (generic indigo), purple gradients on white

**Layouts:** Everything centered, generic hero sections, identical card grids

**Decorations:** Realistic illustrations, gratuitous glassmorphism, drop shadows without purpose

---

## CSS Gotchas

### Negating CSS Functions

**WRONG — silently ignored by browsers (no console error):**
```css
right: -clamp(28px, 3.5vw, 44px);   /* Browser ignores this */
margin-left: -min(10vw, 100px);      /* Browser ignores this */
```

**CORRECT — wrap in `calc()`:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* Works */
margin-left: calc(-1 * min(10vw, 100px));     /* Works */
```

CSS does not allow a leading `-` before function names. The browser silently discards the entire declaration — no error, the element just appears in the wrong position. **Always use `calc(-1 * ...)` to negate CSS function values.**

