---
name: tufte-design
description: Apply Edward Tufte's information design principles to any data visualization, chart, dashboard, or infographic. Use when the user asks to produce, design, critique, or improve a chart, graph, dashboard, KPI tile, table-with-data, sparkline, small multiple, time series, distribution plot, choropleth, or any other visual that communicates quantitative or categorical information.
version: "1.0.0"
author: adapted-from-aref-vc-tufte-claude-skill
tags: ["visualization", "tufte", "chart", "data-viz", "dashboard", "infographic", "design"]
trigger_patterns:
  - "make a chart"
  - "visualize"
  - "viz"
  - "data viz"
  - "graph"
  - "dashboard"
  - "infographic"
  - "tufte"
  - "plot"
  - "design a KPI"
  - "improve this chart"
  - "critique this visual"
  - "what chart should I use"
---

# Tufte Design — Visual Display by the Book

This skill turns "make me a chart" into a Tufte-compliant chart. Distilled from *The Visual Display of Quantitative Information* (1983/2001), *Envisioning Information* (1990), and *Visual Explanations* (1997).

Source: [aref-vc/tufte-claude-skill](https://github.com/aref-vc/tufte-claude-skill)

## Output Stacks

Two output modes, selected by project context or user request:

1. **Self-contained HTML/SVG** — single file, inline SVG, no external deps. For one-offs, embeds, screenshots, slide decks.
2. **React (Recharts + D3 fallback)** — for React projects. Recharts where the chart type fits; raw D3-in-React where it doesn't (slopegraph, sparkline-in-table, small multiples).

## Workflow

When invoked, work through these steps in order:

1. **Apply the 10 principles** (below) to frame every decision.
2. **Pick the chart type** from the chart-selection table based on data shape and goal.
3. **Apply the kill list** before rendering — strip things that don't belong.
4. **Produce the chart** in the user's preferred stack.
5. **Run the checklist** before declaring it done. Twelve items, takes 30 seconds.

Default strictness: Tufte rules apply by default. If the user explicitly requests something on the kill list ("I need a pie because the CFO wants one"), comply, but note the Tufte alternative in a one-line comment.

---

## The 10 Principles

### 1. Show the data

> "Above all else show the data." — VDQI, p. 92

The most important thing in any data graphic is the data. Everything else — gridlines, titles, axes, labels, legends, frames, color, shapes — is overhead that competes for attention. When in doubt, take it out.

### 2. Maximize the data-ink ratio

> "Maximize the data-ink ratio, within reason." — VDQI, p. 96

Data-ink is ink (or pixels) that would change if the data changed. Non-data-ink is everything else. Ask of every visual element: "if I changed the underlying data, would this change?" If not, it's a candidate for deletion.

### 3. Erase non-data-ink

> "Erase non-data-ink, within reason." — VDQI, p. 96

Drop the chart border, drop the gridlines (or fade them to near-white), drop ticks at minor units, drop the axis line where the data doesn't reach (use a range frame). Replace cross-hatching with light gray fills.

### 4. Erase redundant data-ink

> "Erase redundant data-ink, within reason." — VDQI, p. 100

Pick one encoding per quantity. A number with a sparkline is two encodings of one thing — both useful, both used differently. A bar with its value printed on top *and* gridlines *and* an axis label *and* a colored fill is one thing repeated.

### 5. Graphical integrity — never lie

The "lie factor" is the ratio of effect-size-in-graphic to effect-size-in-data. Anything outside 0.95–1.05 is a lie.

Concrete violations:
- Truncated y-axes that exaggerate change
- Area encoding a one-dimensional value
- 3D perspective that compresses distant bars
- Inconsistent scales across small multiples
- Dual-axis charts that invite false correlation

### 6. Use small multiples for any cross-cut

> "At the heart of quantitative reasoning is a single question: Compared to what?" — VDQI, p. 67

Don't overlay six lines on one chart. Make six small charts, identical scales, lined up. The eye reads parallelism faster than it untangles overlap.

### 7. Layering and separation

Data on top, labels next, scaffolding (axes, gridlines) faintest. Watch for the *1+1=3 effect* — when two heavy elements interact to create unintended visual noise.

### 8. Micro/macro readings

> "To clarify, add detail." — *Envisioning Information*

From across the room: one shape, one story. Up close: every individual data point legible. Good charts reward proximity.

### 9. The smallest effective difference

> "Make all visual distinctions as subtle as possible, but still clear and effective." — *Visual Explanations*, p. 73

Don't separate two categories with red vs blue when light gray vs dark gray does the job. Reserve high-contrast color for the one or two values you want the reader to focus on.

### 10. Word-data integration

Charts should sit inside sentences, not float in boxes labeled "Figure 1." Numbers should appear next to their visual. Sparklines belong in tables, in paragraphs, on dashboards.

Tufte's own five-line summary from VDQI p.105:

> Above all else show the data.
> Maximize the data-ink ratio.
> Erase non-data-ink.
> Erase redundant data-ink.
> Revise and edit.

---

## Chart Selection

Pick the chart from the data and goal, not from familiarity.

### Step 1 — Name the data

| Type | Looks like |
|---|---|
| **Single number with context** | "Revenue is $4.2M, up from $3.8M last quarter" |
| **One variable, many items** | Sales by product, latency by endpoint, headcount by team |
| **One variable over time** | Daily active users, monthly revenue |
| **Two variables, many items** | Price vs. rating, size vs. churn |
| **Distribution** | Response times, salaries, ages |
| **Part-to-whole** | Revenue mix, traffic sources |
| **Flow / transition** | Funnel stages, cohort retention |
| **Geographic** | Sales by state, latency by region |

### Step 2 — Name the goal

| Goal | Test |
|---|---|
| **Compare** | Reader will rank, pick a winner, spot the laggard |
| **Track** | Reader will look at one thing across time |
| **Relate** | Reader will see if X is connected to Y |
| **Distribute** | Reader will understand the spread, the typical, the outliers |
| **Locate** | Reader will find where something is |

### Step 3 — The table

| Data | Goal | Use | Don't use |
|---|---|---|---|
| Single number with context | Compare | Sparkline + number side by side | KPI card with giant number alone |
| One variable, many items | Compare / rank | Sorted dot plot or horizontal bar | Pie chart, donut, treemap |
| One variable over time | Track | Line chart with range frame | Bar chart for continuous time, dual-axis line |
| Two variables, many items | Relate | Scatterplot, range frame, no grid | Bubble chart with size encoding a third variable |
| Two snapshots, many items | Compare change | Slopegraph | Side-by-side bars, before/after pair charts |
| Distribution | Distribute | Strip plot, dot plot, or histogram with thin bars | Boxplot for non-statistical audience, violin plot for general use |
| Part-to-whole, small n (≤6) | Compare shares | Sorted bar with direct labels, or a small table | Pie chart |
| Part-to-whole, large n | Compare shares | Sorted bar; group long tail | Treemap, donut, sunburst |
| Flow through stages | Track drop-off | Sorted horizontal bar (funnel) or sparkline column in a table | Funnel chart with 3D, Sankey for simple flows |
| Geographic | Locate / compare | Choropleth in single-hue sequential, small annotations | Choropleth with rainbow, bubble map sized by raw count |
| Multivariate, many items | Compare across dimensions | Small multiples (one chart per dimension, shared scale) | Radar/spider chart, parallel coordinates for general audiences |
| Multivariate table | Compare values | Table with sparklines and conditional shading | Heatmap for any small table (just show numbers) |

### Step 4 — Gut checks

Before drawing, ask:

1. **Could a small table do this job?** If n ≤ ~15 and exact values matter, a table beats a chart.
2. **Could a single sentence do this job?** "Revenue grew 22% to $4.2M" needs no chart.
3. **Am I about to add a second axis?** Don't. Use small multiples.
4. **Am I about to encode three things in one chart?** Pick one quantity per channel.
5. **Am I sorting by alphabetical?** Almost always wrong. Sort by the value the reader cares about.

### Step 5 — Sorting

- **Bar / dot plot**: by value, descending. Largest at top.
- **Time series**: time, ascending left to right.
- **Funnel**: by stage, in the order users flow through.
- **Geographic**: by region category, then value within.

Alphabetical is for indexes and directories. Almost never for data graphics.

---

## Kill List

Remove these from any Tufte-compliant chart unless the user explicitly overrides.

### Visual decoration

| Kill | Replace with |
|---|---|
| Drop shadows | Nothing |
| Gradient fills on bars | Flat fill |
| Bevels, glow, embossing | Flat shapes |
| 3D bars / pies / surfaces | 2D version |
| Background images behind data | White or near-white background |
| Patterned fills (stripes, dots, crosshatch) | Gray tints |
| Icons inside data marks | Direct labels |

### Chart types to avoid

| Kill | Replace with |
|---|---|
| Pie chart | Sorted bar or small table |
| Donut chart | Sorted bar |
| 3D pie | Sorted bar |
| Radar / spider chart | Small multiples or sorted bar |
| Funnel chart with 3D taper | Horizontal bars by stage |
| Bubble chart for one variable | Bar or dot plot |
| Word cloud | Sorted bar |
| Stacked area for many categories | Small multiples |

### Axis and grid

| Kill | Replace with |
|---|---|
| Dual y-axis | Two small charts side by side |
| Heavy black gridlines | Light gray, or omit |
| Tick marks at every minor unit | Ticks at labeled values only |
| Chart border / frame box | Range frame (axes only span data) |
| Y-axis truncated without note (on bars) | Start at zero, or use a line chart |
| Logarithmic scale without label | Label clearly; consider linear with annotations |

### Labels and legends

| Kill | Replace with |
|---|---|
| Legend placed away from data | Direct labels next to data |
| Color-coded legend with 7+ items | Small multiples or direct labels |
| Title bar with chart background color | Plain text title, left-aligned |
| All-caps headers | Sentence case or title case |
| Bold + italic + underline on same label | One emphasis, applied sparingly |

### Color

| Kill | Replace with |
|---|---|
| Rainbow / jet scale for ordered data | Sequential single-hue (light to dark) |
| Red + green only (deuteranopia) | Add value/luminance difference |
| Saturated color on every bar | Gray for context, accent for focal |
| More than 4 colors in one chart | Group small categories or use small multiples |
| Color as decoration only | One color, used to signal |

### Dashboard sins

| Kill | Replace with |
|---|---|
| Giant KPI tile with no context | Number + sparkline + delta |
| Gauges / speedometers | Number + threshold marker |
| Traffic-light status circles only | Number + colored dot + threshold |
| Identical-looking charts in a grid (different scales) | Shared scale or annotation |
| Animated transitions for static data | Static layout |

---

## Keep List

These belong in most Tufte charts:

- Direct labels on data (no legends)
- Sparklines next to numbers
- Small multiples for any cross-cut
- Range frames (axes only span where data exists)
- Subtle gridlines (white-on-light, or omit)
- A single accent color, used to signal not to decorate
- Sorted categories (rarely alphabetical, almost never as-input)
- Tables when n ≤ ~20 and exact values matter

---

## Pre-Publish Checklist

Twelve items. Walk through before declaring any chart done.

### Data
- [ ] Is the data sorted by the value the reader cares about (not alphabetical, not as-input)?
- [ ] Are all data points visible, or is the chart hiding outliers behind summary lines?
- [ ] If categories were grouped into "Other", is that group small enough not to mislead?

### Honesty
- [ ] Lie factor between 0.95 and 1.05? (Visual change matches numerical change.)
- [ ] Bar charts start at zero?
- [ ] Truncated line-chart axes have the baseline labeled?
- [ ] No area or volume encoding a single number?

### Ink
- [ ] Gridlines either light gray or absent?
- [ ] No chart border / frame box (range frame only where needed)?
- [ ] No redundant encoding (bar + number + label + axis tick all saying the same thing)?
- [ ] One accent color, used for focal data only?

### Labels
- [ ] Direct labels on data, not a separate legend (unless ≥ 5 categories)?
- [ ] Numbers formatted readably (4.2M not 4,200,000)?

---

## Style Tokens

### HTML/SVG

```css
:root {
  --ink:    #1a1a1a;   /* data, text */
  --paper:  #fafaf7;   /* background */
  --rule:   #d8d4cc;   /* dividers */
  --muted:  #8a857c;   /* captions */
  --accent: #b3261e;   /* the one focal color */
  --gray-1: #efece4;   /* faintest gridline */
  --gray-2: #c8c2b5;   /* light element */
  --gray-3: #6b665d;   /* secondary text */
}

.tick   { font: 10px/1 "SF Mono", "Berkeley Mono", monospace; fill: var(--gray-3); }
.label  { font: 12px/1.2 "Charter", Georgia, serif; fill: var(--ink); }
.value  { font: 11px/1 "SF Mono", monospace; fill: var(--ink); font-weight: 600; }
.axis   { stroke: var(--gray-3); stroke-width: 0.5; fill: none; }
.grid   { stroke: var(--gray-1); stroke-width: 0.5; }
```

### React / TypeScript

```ts
export const tufte = {
  ink: "#1a1a1a",
  paper: "#fafaf7",
  rule: "#d8d4cc",
  muted: "#8a857c",
  accent: "#b3261e",
  gray1: "#efece4",
  gray2: "#c8c2b5",
  gray3: "#6b665d",
  fontSerif: '"Charter", "Iowan Old Style", Georgia, serif',
  fontMono: '"SF Mono", "Berkeley Mono", monospace',
};
```

---

## Code Patterns

### Sparkline (HTML/SVG)

```html
<svg viewBox="0 0 120 30" width="120" height="30">
  <polyline fill="none" stroke="#1a1a1a" stroke-width="1.2"
    points="0,22 12,20 24,17 36,14 48,15 60,11 72,9 84,6 96,4 108,3 120,2"/>
  <circle cx="120" cy="2" r="2" fill="#b3261e"/>
</svg>
```

### Inline sparkline next to value

```html
<span class="metric">
  <span class="num">780K</span>
  <svg class="spark" viewBox="0 0 80 16" width="80" height="16">
    <polyline fill="none" stroke="currentColor" stroke-width="1"
      points="0,14 10,13 20,11 30,9 40,8 50,6 60,4 70,3 80,1"/>
  </svg>
  <span class="delta">+12%</span>
</span>
```

### Dot plot (HTML/SVG)

```html
<svg viewBox="0 0 420 280" width="100%" height="260">
  <line x1="120" y1="40" x2="120" y2="240" class="axis"/>
  <text x="115" y="44" text-anchor="end" class="tick">500</text>
  <text x="115" y="244" text-anchor="end" class="tick">0</text>
  <line x1="120" y1="40" x2="400" y2="40" class="grid"/>
  <!-- one row per item, sorted desc -->
  <line x1="120" y1="60" x2="288" y2="60" stroke="#c8c2b5" stroke-width="0.5"/>
  <circle cx="288" cy="60" r="4" fill="#1a1a1a"/>
  <text x="115" y="64" text-anchor="end" class="label">Atlas</text>
  <text x="296" y="64" class="value">420</text>
</svg>
```

### Line chart with range frame

```html
<svg viewBox="0 0 420 280" width="100%" height="260">
  <line x1="60" y1="60" x2="60" y2="220" class="axis"/>
  <text x="55" y="64" text-anchor="end" class="tick">800</text>
  <text x="55" y="224" text-anchor="end" class="tick">400</text>
  <line x1="60" y1="60" x2="380" y2="60" class="grid"/>
  <polyline fill="none" stroke="#1a1a1a" stroke-width="1.5"
    points="70,200 110,196 140,180 170,170 200,150 230,140 260,120 290,110 320,95 350,75"/>
  <circle cx="70" cy="200" r="2" fill="#6b665d"/>
  <text x="70" y="216" class="tick" text-anchor="middle">Jan · 400</text>
  <circle cx="350" cy="75" r="3" fill="#b3261e"/>
  <text x="350" y="68" class="tick" text-anchor="middle" fill="#b3261e">Oct · 780</text>
</svg>
```

### Small multiples

```html
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
  <figure>
    <figcaption class="label">North · 420</figcaption>
    <svg viewBox="0 0 100 50">
      <polyline fill="none" stroke="#1a1a1a" stroke-width="1.2" points="..."/>
    </svg>
  </figure>
  <!-- repeat for South, East, West with IDENTICAL scales -->
</div>
```

Rules: all panels share the same x/y scale, arranged in meaningful order, one label per panel.

### Sparkline-in-table (dashboard replacement)

```html
<table style="border-collapse: collapse; font-family: Charter, serif;">
  <thead>
    <tr style="border-bottom: 0.5px solid #1a1a1a;">
      <th style="text-align:left; font-size: 9px; letter-spacing: 0.08em; text-transform: uppercase; color: #6b665d;">Metric</th>
      <th style="text-align:right; font-size: 9px; text-transform: uppercase; color: #6b665d;">Now</th>
      <th style="text-align:center; font-size: 9px; text-transform: uppercase; color: #6b665d;">10mo</th>
      <th style="text-align:right; font-size: 9px; text-transform: uppercase; color: #6b665d;">vs Target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Revenue</td>
      <td class="value" style="text-align:right;">$4.2M</td>
      <td><svg viewBox="0 0 80 16" width="80" height="16"><polyline fill="none" stroke="#1a1a1a" stroke-width="1" points="0,14 ..."/></svg></td>
      <td class="value" style="text-align:right;">+5% ↑</td>
    </tr>
  </tbody>
</table>
```

### React: Tufte-compliant LineChart (Recharts)

```tsx
import { LineChart, Line, XAxis, YAxis, ReferenceDot } from "recharts";
import { tufte } from "./tufte-theme";

const data = [
  { month: "Jan", mau: 410 }, { month: "Feb", mau: 432 },
  { month: "Oct", mau: 780 },
];
const last = data[data.length - 1];

export function MAUChart() {
  return (
    <LineChart width={500} height={220} data={data}
      margin={{ top: 30, right: 60, bottom: 30, left: 30 }}>
      <XAxis dataKey="month"
        axisLine={{ stroke: tufte.gray3, strokeWidth: 0.5 }}
        tickLine={false}
        tick={{ fill: tufte.gray3, fontSize: 10, fontFamily: tufte.fontMono }}
        interval={9} />
      <YAxis
        axisLine={{ stroke: tufte.gray3, strokeWidth: 0.5 }}
        tickLine={false}
        tick={{ fill: tufte.gray3, fontSize: 10, fontFamily: tufte.fontMono }}
        domain={["dataMin", "dataMax"]}
        ticks={[Math.min(...data.map(d => d.mau)), Math.max(...data.map(d => d.mau))]} />
      <Line type="monotone" dataKey="mau" stroke={tufte.ink}
        strokeWidth={1.5} dot={false} isAnimationActive={false} />
      <ReferenceDot x={last.month} y={last.mau} r={3} fill={tufte.accent} stroke="none" />
    </LineChart>
  );
}
```

Key moves: no `<CartesianGrid>`, no `<Tooltip>` for static views, no `<Legend>` for single series, range frame via `domain`, `dot={false}`, `isAnimationActive={false}`, one accent `<ReferenceDot>`.

### React: Dot Plot (D3-in-React)

```tsx
import { scaleLinear } from "d3-scale";
import { tufte } from "./tufte-theme";

type Datum = { name: string; value: number };

export function DotPlot({ data, focal }: { data: Datum[]; focal?: string }) {
  const sorted = [...data].sort((a, b) => b.value - a.value);
  const max = Math.max(...sorted.map(d => d.value));
  const x = scaleLinear().domain([0, max]).range([120, 380]);
  const rowH = 28;
  const height = sorted.length * rowH + 40;

  return (
    <svg viewBox={`0 0 420 ${height}`} width="100%">
      <line x1={120} y1={20} x2={120} y2={height - 20} stroke={tufte.gray3} strokeWidth={0.5} />
      {sorted.map((d, i) => {
        const y = 40 + i * rowH;
        const isFocal = d.name === focal;
        return (
          <g key={d.name}>
            <line x1={120} y1={y} x2={x(d.value)} y2={y} stroke={tufte.gray2} strokeWidth={0.5} />
            <circle cx={x(d.value)} cy={y} r={4} fill={isFocal ? tufte.accent : tufte.ink} />
            <text x={115} y={y + 4} textAnchor="end" style={{ fontFamily: tufte.fontSerif, fontSize: 12, fill: tufte.ink }}>{d.name}</text>
            <text x={x(d.value) + 8} y={y + 4} style={{ fontFamily: tufte.fontMono, fontSize: 11, fill: tufte.ink, fontWeight: 600 }}>{d.value}</text>
          </g>
        );
      })}
    </svg>
  );
}
```

### React: Slopegraph

```tsx
type SlopeDatum = { name: string; before: number; after: number };

export function Slopegraph({ data }: { data: SlopeDatum[] }) {
  const allValues = data.flatMap(d => [d.before, d.after]);
  const y = scaleLinear()
    .domain([Math.min(...allValues), Math.max(...allValues)])
    .range([220, 30]);

  return (
    <svg viewBox="0 0 420 280" width="100%">
      {data.map(d => {
        const declined = d.after < d.before;
        return (
          <g key={d.name}>
            <line x1={84} y1={y(d.before)} x2={336} y2={y(d.after)}
              stroke={declined ? tufte.accent : tufte.ink} strokeWidth={1} />
            <circle cx={84} cy={y(d.before)} r={3} fill={tufte.ink} />
            <circle cx={336} cy={y(d.after)} r={3} fill={tufte.ink} />
            <text x={80} y={y(d.before) + 4} textAnchor="end" style={labelStyle}>{d.name} · {d.before}</text>
            <text x={340} y={y(d.after) + 4} textAnchor="start" style={labelStyle}>{d.after}</text>
          </g>
        );
      })}
    </svg>
  );
}
```

---

## What to never include in SVG

- `<svg>` with `style="filter: drop-shadow(...)"` — chartjunk
- `<defs><linearGradient>` for bar fills — chartjunk
- `<rect>` chart border around the whole SVG — non-data-ink
- `<g class="gridlines">` with `stroke="#000"` or any saturated color
- Legend boxes when ≤ 4 series — label directly

---

## When NOT to activate

This skill does not apply to:
- Logo design, illustration, or decorative graphics
- Flowcharts, architecture diagrams, hand-drawn sketches
- Pure typography or layout that has no quantitative data

---

## Reference Files

Full reference files with extended examples are in `docs/`:

| File | Purpose |
|---|---|
| `docs/principles.md` | 10 rules with extended practical interpretation |
| `docs/chart-selection.md` | Full chart-selection decision table |
| `docs/kill-list.md` | Complete kill list with replacement table |
| `docs/checklist.md` | 12-item pre-publish checklist |
| `docs/preset-html-svg.md` | Style tokens + working SVG patterns |
| `docs/preset-react.md` | Recharts theme + D3 patterns |
