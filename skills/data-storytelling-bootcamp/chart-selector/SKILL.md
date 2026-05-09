---
name: chart-selector
version: "1.0.0"
description: >
  Recommend optimal chart types based on data types, relationship types, audience, and message.
  Applies the Who-What-How framework and the four data relationship categories from the
  Data Storytelling Bootcamp. Use when choosing visualizations, picking chart types, deciding
  how to display data, or when asked "what chart should I use?".
  Triggers: "what chart", "pick a chart", "best visualization", "chart type", "how to display",
  "which graph", "recommend a chart", "data relationship type".
author: Tolu
trigger_patterns:
  - "what chart should I use"
  - "best visualization for this data"
  - "which chart type"
  - "pick a chart"
  - "how to display this data"
  - "recommend a chart"
  - "which graph"
  - "data relationship type"
  - "how to visualize"
tags: ["data-storytelling", "visualization", "chart-selection", "data-analysis"]
metadata:
  source: "Data Storytelling Bootcamp by Joy Hopkins, Data Society (April 2026)"
  core_frameworks: ["Who-What-How", "Four Data Relationship Categories", "Data Classification Hierarchy"]
---

# Chart Selector Skill

## Purpose
Recommend the optimal chart type for any dataset and message by walking through a structured decision tree.

## Core Principle
**Start with the question, not the chart type.** Apply Who → What → How.

---

## Step 1: Data Classification

First, classify the data:

```
Is it Quantitative or Qualitative?

Qualitative:
  Nominal — no inherent order (colors, zip codes, departments)
  Ordinal — has order (small/medium/large, Likert scales, rankings)

Quantitative:
  Discrete — countable, gaps (number of children, ticket count)
  Continuous — measurable, any value (revenue, temperature, time)
```

**Litmus tests:**
- "Would you average it?" → Yes = Quantitative, No = Qualitative
- "Staircase or ramp?" → Staircase = Discrete, Ramp = Continuous
- Zip codes, phone numbers, IDs → Qualitative/Nominal (they're labels, not measurements)

---

## Step 2: Identify the Data Relationship

What question is the chart answering? Map to one of four categories:

| Relationship | Question It Answers | Go-To Charts |
|---|---|---|
| **Comparison** | Which is bigger/smaller? How do categories compare? | Bar chart, line chart, grouped bar |
| **Composition** | What makes up the whole? How do parts relate to total? | Pie (≤5 slices), stacked bar, tree map, waterfall |
| **Distribution** | How is data spread? Where are the clusters/outliers? | Histogram, box plot, violin plot |
| **Relationship** | How do variables relate? Does X predict Y? | Scatter plot, bubble chart, heat map |

---

## Step 3: Apply Constraints

Answer these before selecting the final chart:

1. **How many variables?** Single variable = simple chart. Multiple = grouped, stacked, or faceted.
2. **How many data points?** <10 = bar/column. 10-100 = scatter or line. >100 = heat map or aggregated.
3. **Is there a time component?** Yes = line chart or area chart. No = bar chart or scatter.
4. **Need grouping?** Yes = grouped bar, stacked bar, faceted small multiples.
5. **Could this be a simple number or sentence instead?** If the message is a single value, skip the chart.

---

## Step 4: Chart-Specific Rules

### Bar Charts
- **Use for:** Comparison of qualitative categories
- **Rule:** Qualitative data only on one axis
- **Sort:** By the dimension that matters (not alphabetical)
- **Orientation:** Horizontal bars when labels are long

### Line Charts
- **Use for:** Trends over time, continuous data
- **Rule:** Continuous data only — "if you can rearrange x-axis labels, don't use a line chart"
- **Multiple lines:** Max 4-5 before readability drops

### Pie / Donut Charts
- **Use for:** Part-to-whole composition
- **Rule:** Maximum 4-5 slices
- **Avoid donut** — removes the central angles being compared
- **Consider tree map instead** — "brains do better with rectangles than pie slices"

### Scatter Plots
- **Use for:** Relationship between two quantitative variables
- **Rule:** Both axes must be quantitative
- **Add trend line** when showing correlation
- **Remember:** Correlation ≠ causation

### Histograms
- **Use for:** Distribution shape of a single quantitative variable
- **Rule:** X-axis is continuous, bins are adjustable
- **Don't confuse with bar charts** — bars touch in histograms

### Box Plots
- **Use for:** Summary statistics and outlier detection
- **Rule:** Univariate — one variable at a time
- **Always include n** (sample size)

### Area Charts
- **Use for:** Composition over time (stacked area)
- **Rule:** Only when line represents a composite/total
- **Avoid** for simple trends — use line chart instead

### Tree Maps
- **Use for:** Hierarchical composition, part-to-whole with many categories
- **Advantage:** Handles more categories than pie charts
- **Joy's favorite** for composition charts

### Heat Maps
- **Use for:** Matrix-style data, density, patterns across two dimensions
- **Rule:** Color must encode a quantitative variable
- **Accessible colors** — avoid red-green only

### Waterfall Charts
- **Use for:** Sequential contribution to a total (how we got from A to B)
- **Rule:** Shows incremental positive/negative contributions

### Bubble Charts
- **Use for:** 3-4 dimensions (x, y, size, optionally color)
- **Rule:** Size must encode a meaningful variable
- **Label directly** — legend + size encoding is hard to read

### Maps
- **Use for:** Geographic data only
- **Rule:** Don't use maps when a bar chart tells the story better
- **Beware** area distortion (large states vs small states)

---

## Step 5: Final Check

Before finalizing the recommendation:

1. **Does this chart answer the specific question?** Not a related question — THE question.
2. **One chart, one message?** If trying to show multiple things, split into multiple charts.
3. **Is a chart even needed?** A single number, sentence, or table might be better.
4. **Will the audience understand it?** Match complexity to audience data literacy.
5. **Have you considered multiple charts?** "There's no rule that says you've got to get it all in one visualization."

---

## Output Format

For each recommendation:

```
PRIMARY RECOMMENDATION: [Chart Type]
- Data relationship: [Comparison/Composition/Distribution/Relationship]
- Data types: [Qualitative/Quantitative, Nominal/Ordinal/Discrete/Continuous]
- Why: [1-2 sentence justification]

ALTERNATIVES:
1. [Chart Type] — [when to use instead]
2. [Chart Type] — [when to use instead]

AVOID:
- [Chart Type] — [why it would be wrong for this data/question]

SIMPLEST OPTION:
- ["Just use a number/sentence" or specific minimal chart]
```
