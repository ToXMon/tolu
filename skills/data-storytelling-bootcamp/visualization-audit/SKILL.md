---
name: visualization-audit
version: "1.0.0"
description: >
  Audit, critique, and declutter data visualizations using the cognitive load framework,
  11-point visual design checklist, and 7-step decluttering workflow from the Data Storytelling Bootcamp.
  Use when reviewing charts, improving visualizations, decluttering, or auditing for accessibility and honesty.
  Triggers: "review chart", "improve visualization", "declutter", "audit chart", "chart critique",
  "visualization feedback", "make this chart better".
author: Tolu
trigger_patterns:
  - "review this chart"
  - "improve this visualization"
  - "declutter my chart"
  - "audit this visualization"
  - "chart critique"
  - "visualization feedback"
  - "make this chart better"
  - "fix this chart"
tags: ["data-storytelling", "visualization", "design", "audit"]
metadata:
  source: "Data Storytelling Bootcamp by Joy Hopkins, Data Society (April 2026)"
  core_frameworks: ["Cognitive Load Framework", "11-Point Visual Design Checklist", "Decluttering Workflow"]
---

# Visualization Audit Skill

## Purpose
Systematically critique and improve data visualizations by reducing cognitive load, removing clutter, and ensuring every element serves the story.

## Core Principle
**Cognitive load is the enemy.** Every visual element costs brain power. If removing it doesn't hurt the story, remove it.

---

## Step 1: The Element Audit

For every element in the chart, answer three questions:

| Question | Action if Yes |
|----------|---------------|
| Does it serve the story? | Keep |
| Can it be removed without losing the story? | Remove |
| Is it redundant with another element? | Remove |

If any element fails, flag it for removal.

---

## Step 2: Decluttering Workflow (7 Steps)

Apply in this exact order:

1. **Remove 3D effects** — 3D is almost never justified. Accept only if the third dimension encodes meaning AND the chart is interactive.
2. **Remove background fills** — Light/white backgrounds only. No colored backgrounds.
3. **Remove borders** — Borders add visual noise without adding information.
4. **Remove gridlines** — If needed, use light, thin gridlines. Better: remove entirely and use direct labels.
5. **Add direct labels** — Replace separate legends with labels directly on or next to data elements.
6. **Apply grayscale + one highlight color** — All data elements in grayscale except the one you want to draw attention to. Orange-blue is the safest color combination.
7. **Reduce decimal precision** — Round to the precision that matters for the story. Never show more decimals than the audience needs.

---

## Step 3: Visual Design Checklist (11 Points)

- [ ] **Light backgrounds** — No dark or colored chart backgrounds
- [ ] **Meaningful sorting** — Sorted by the dimension that matters for the story (not alphabetical)
- [ ] **Grouping** — Related items visually grouped
- [ ] **Direct labels** — Labels on data, not in separate legends
- [ ] **Size = importance** — Larger elements should be more important
- [ ] **Color with meaning** — Every color choice encodes information
- [ ] **Natural reading order** — Follows left-to-right, top-to-bottom expectations
- [ ] **Data gap marking** — Missing data clearly indicated, not hidden
- [ ] **Closed regions** — Axes and boundaries clear where needed
- [ ] **Accessible colors** — Orange-blue safe default, never rely on red-green alone
- [ ] **Clear labels** — Every axis, title, and annotation is readable and precise

---

## Step 4: Honesty Checks

Verify the chart is not accidentally (or intentionally) misleading:

- **Y-axis starts at zero?** If not, there must be a compelling reason stated.
- **Full time range shown?** No cherry-picked date ranges that change the story.
- **Proportional representation?** Area, bubble size, and bar lengths are proportional.
- **No dual-axis without justification?** Dual axes create false correlation impressions.
- **Correlation ≠ causation?** Chart doesn't imply causation from correlational data.
- **Context provided?** Chart includes comparison points, benchmarks, or historical context.
- **Unfavorable findings included?** Not hiding data that contradicts the story.

---

## Step 5: Output Format

For each audit, produce:

### Diagnosis
- **Overall assessment** (1-2 sentences)
- **Cognitive load score**: Low / Medium / High
- **Honesty score**: Clean / Caution / Misleading

### Specific Issues
| # | Element | Issue | Fix |
|---|---------|-------|-----|
| 1 | ... | ... | ... |

### Before/After Specification
- List every change to make
- Priority order (highest impact first)

### Recommended Chart Type
- If the current chart type is wrong, recommend the correct one with justification
- Reference the chart selection decision tree if needed

---

## Hard Rules

- **One chart = one message.** If the chart tries to tell multiple stories, split into multiple charts.
- **Audience only knows what you tell them.** If the chart requires explanation beyond labels, redesign it.
- **Ink on the page should mean something.** Every pixel should earn its place.
- **3D is almost never justified.** The two acceptance criteria: third dimension encodes meaning AND chart is interactive.
- **Pie charts: max 4-5 slices, part-to-whole only.** Consider tree maps instead.
- **Direct labels > separate legends.** Always.
- **Y-axis starts at zero** unless there's a compelling reason documented.
- **Sort by the dimension that matters.** Never default to alphabetical.
