# JNJ JJIM Brand Guide — Frontend Slides Integration

Complete brand system extracted from JJIM PowerPoint template for HTML presentation generation.

**Audience:** INTERNAL Johnson & Johnson / JJIM audiences only.
**External audiences:** Use official J&J corporate templates.

---

## Template Source

- File: `JJIM template.pptx`
- Dimensions: 13.3" × 7.5" (widescreen 16:9)
- Slide layouts: 56 (title, section, content, chart, team, timeline, image combos)
- Theme name: `JNJ`

---

## Typography

### Primary Fonts (Proprietary — PPTX only)

| Role | Font | Usage |
|------|------|-------|
| Heading | Johnson Display | Titles, section headers, key statements |
| Body | Johnson Text | Body copy, bullets, captions, chart labels |

### Web Fallbacks (HTML presentations)

| Role | Fallback | Weight | Google Fonts URL |
|------|-----------|--------|------------------|
| Heading | Outfit | 600, 700 | `https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&display=swap` |
| Body | Nunito Sans | 400, 500 | `https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500&display=swap` |

### Text Rules

- All text LEFT-aligned (never center-aligned body text)
- Bold: sparingly for emphasis
- Italics: light emphasis only
- **J&J Red (#EB1700) is for titles/headers ONLY — never body text**
- Minimum 10pt for chart text; titles always larger
- Use indent levels (not manual bullets) to maintain spacing

---

## Brand Colors

### Core Palette

| Name | Hex | Role |
|------|-----|------|
| J&J Red | `#EB1700` | Headers, section accents, emphasis (NEVER body text) |
| Black | `#000000` | Primary text, chart color #2 |
| White | `#FFFFFF` | Backgrounds, chart backgrounds |
| Light Gray | `#F1EFED` | Slide backgrounds (contrast for white images) |

### Warm Grays

| Name | Hex | Usage |
|------|-----|-------|
| Warm Gray | `#C4BDB6` | Borders, neutral accents, chart color #3 |
| Mid Gray | `#D5CFC9` | Subtle backgrounds |
| Tone Gray | `#A39992` | Secondary neutral |
| Brown | `#6E6159` | Dark neutral accent |

### Data Visualization Colors (FIXED ORDER — DO NOT REORDER)

| Position | Hex | Name | Restriction |
|----------|-----|------|-------------|
| 1 | `#EB1700` | J&J Red | Primary data series |
| 2 | `#000000` | Black | Secondary data series |
| 3 | `#C4BDB6` | Warm Gray | Tertiary data series |
| 4 | `#004686` | Dark Blue | **Data viz only** |
| 5 | `#68D2FF` | Light Blue | **Data viz only** |
| 6 | `#541981` | Purple | Sixth data series |

This order is accessibility-tested. Changing it breaks WCAG compliance.

---

## Chart Style Rules

Apply to ALL data visualizations (bar charts, line charts, pie charts, word clouds):

1. **White outlines**: `1.5pt solid white` around every data element
2. **Gridlines**: `0.75pt medium gray` (#A0A0A0) — if present
3. **Axis titles**: ON when relevant
4. **Labels**: Centered, black text, readable size
5. **Chart background**: Always white (`#FFFFFF`)
6. **Slide background**: Light gray (`#F1EFED`) if chart has white elements (avoids white-on-white)
7. **Blues**: Use ONLY in data visualizations, never as accent/branding outside charts
8. **Comparison**: Prefer separate charts over cramming many colors into one chart

### CSS for Charts

```css
.jj-chart {
    background: #FFFFFF;
    border: none;
}

.jj-chart .data-element {
    stroke: #FFFFFF;
    stroke-width: 1.5px;
}

.jj-chart .gridline {
    stroke: #A0A0A0;
    stroke-width: 0.75px;
}

.jj-chart .axis-title {
    fill: #000000;
    font-family: 'Nunito Sans', sans-serif;
}

.jj-chart .label {
    fill: #000000;
    text-anchor: middle;
}
```

---

## Layout Discipline

### Grid & Alignment

- Use built-in template layouts and placeholders
- All content LEFT-aligned
- Maintain consistent spacing via guides
- No freeform placement unless necessary

### Slide Backgrounds

- Default: White (`#FFFFFF`)
- When images have white backgrounds: Light gray (`#F1EFED`) to avoid white-on-white
- Section headers: Can use J&J Red (`#EB1700`) or Gray (`#F1EFED`) backgrounds

### Content Density

- Headline + support style (short, scannable)
- Maximum 4-6 bullet points per content slide
- Prefer splitting content across slides over cramming

---

## Images

- Use image placeholders; crop thoughtfully
- SVG/PNG preferred for icons and graphics
- If image has white background → set slide background to `#F1EFED`
- Add alt text to every image

---

## Icons (STRICT)

- Only approved icons from J&J brand library
- Allowed colors:
  - **Black** (default)
  - **J&J Red** `#EB1700` (emphasis)
  - **White** (only when on red background)
- No other icon colors permitted

---

## Accessibility Requirements

Every slide must meet these standards:

1. **Color independence**: Visuals understood at a glance, not by color alone
2. **Alt text**: Include suggested alt-text for every image/visual
3. **Text size**: Minimum 10pt for chart text; titles always larger
4. **Contrast**: High contrast — white/gray backgrounds with dark text
5. **Chart comparison**: Separate charts preferred over multi-color single charts

---

## Slide Layout Reference (56 layouts from template)

### Title Slides
- Title Slide, Accessible, With Image, With Panel Images

### Section Headers
- Standard, With Panel, Red with Panel, Gray, With Full Image, With Full Dark Image, Red with Image, With Image

### Agenda
- 3 variants with icon grid patterns

### Key Slides
- Key Statement: Single focused statement
- Key Numbers: 4-up metric cards with icons (Standard + Accessible)

### Content
- Title + Right Content, Title + Content, Two Content, Three Content, Four Content, Eight Content

### Content + Images
- Three Images + Text, Four Content with Images, Image + Caption, Image + Content, Image Right Side, Two/Three Images + Content, Image + Content + Caption, Two Images + Content + Captions (side-by-side and stacked)

### Charts & Tables
- Text + Chart, Three Chart, Table

### Team
- 1 person, 1-2 person, 3 person, 4 person, 6 person, 12 person grids

### Timeline
- Multi-point horizontal timeline with SmartArt

### End Slides
- Standard + Accessible

---

## CSS Variables Summary

```css
:root {
    /* Primary brand */
    --jj-red: #EB1700;
    --jj-black: #000000;
    --jj-white: #FFFFFF;
    --jj-bg-light: #F1EFED;

    /* Warm grays */
    --jj-gray-warm: #C4BDB6;
    --jj-gray-mid: #D5CFC9;
    --jj-gray-tone: #A39992;
    --jj-brown: #6E6159;

    /* Data visualization (fixed order) */
    --jj-chart-1: #EB1700;
    --jj-chart-2: #000000;
    --jj-chart-3: #C4BDB6;
    --jj-chart-4: #004686;
    --jj-chart-5: #68D2FF;
    --jj-chart-6: #541981;

    /* Typography */
    --jj-font-heading: 'Outfit', sans-serif;
    --jj-font-body: 'Nunito Sans', sans-serif;

    /* Chart styling */
    --jj-chart-outline: #FFFFFF;
    --jj-chart-outline-width: 1.5px;
    --jj-gridline-color: #A0A0A0;
    --jj-gridline-width: 0.75px;
}
```

---

## Output Style (Agent Guidelines)

When generating JNJ JJIM slides:

1. Ask ONLY minimum clarifying questions (audience, purpose, length, key message)
2. Produce:
   - (a) Slide-by-slide outline
   - (b) Suggested visuals per slide with alt-text
   - (c) Actual slide text in JJIM style (short, scannable, headline + support)
3. Tone: Professional, crisp, internal-facing
4. Always use the JJIM style preset from STYLE_PRESETS.md
5. If audience is external → flag that official J&J templates should be used instead
